from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, date, timedelta, timezone
from bson import ObjectId
from app.models.habit import CheckInRequest, CheckInResponse, CheckInDateInfo, WeeklyStats
from app.core.database import habits_collection, checkins_collection
from app.core.deps import get_current_user

router = APIRouter(prefix="/checkins", tags=["checkins"])


async def _calc_streak(habit_id: str, user_id: str) -> tuple[int, int]:
    """计算当前连续打卡天数和历史最佳连续打卡天数。

    逻辑：从今天往前逐日检查是否有打卡记录，直到断开为止。
    返回 (current_streak, best_streak)。
    """
    today = date.today()
    # 查最近 365 天的打卡记录，按日期降序
    one_year_ago = today - timedelta(days=365)
    cursor = checkins_collection.find(
        {"habitId": habit_id, "userId": user_id, "checkInDate": {"$gte": datetime(one_year_ago.year, one_year_ago.month, one_year_ago.day)}},
        {"checkInDate": 1},
    ).sort("checkInDate", -1)
    docs = await cursor.to_list(length=365)

    checked_dates = set()
    for d in docs:
        dt = d["checkInDate"]
        if isinstance(dt, datetime):
            checked_dates.add(dt.date().isoformat())
        else:
            checked_dates.add(str(dt))

    # 从今天往前数连续天数
    current_streak = 0
    day = today
    while day.isoformat() in checked_dates:
        current_streak += 1
        day -= timedelta(days=1)

    # 从所有打卡记录中算历史最佳连续
    if not checked_dates:
        return current_streak, 0

    sorted_dates = sorted(checked_dates)
    best_streak = 1
    streak = 1
    for i in range(1, len(sorted_dates)):
        prev = date.fromisoformat(sorted_dates[i - 1])
        curr = date.fromisoformat(sorted_dates[i])
        if (curr - prev).days == 1:
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 1

    # 当前连续可能就是最佳
    best_streak = max(best_streak, current_streak)
    return current_streak, best_streak


@router.post("", response_model=CheckInResponse, status_code=201)
async def check_in(request: CheckInRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)

    # 用 ISODate 范围查重（同一习惯同一天）
    existing = await checkins_collection.find_one({
        "habitId": request.habitId,
        "userId": user_id,
        "checkInDate": {"$gte": today_start, "$lt": today_end},
    })
    if existing:
        raise HTTPException(status_code=409, detail="今日已打卡")

    checkin_doc = {
        "habitId": request.habitId,
        "userId": user_id,
        "checkInDate": today_start,
        "checkInTime": now,
        "note": request.note,
        "createdAt": now,
    }
    result = await checkins_collection.insert_one(checkin_doc)

    # 更新 totalCheckIns + streak
    current_streak, best_streak = await _calc_streak(request.habitId, user_id)
    await habits_collection.update_one(
        {"_id": ObjectId(request.habitId)},
        {"$inc": {"totalCheckIns": 1}, "$set": {"streak": current_streak, "bestStreak": best_streak, "updatedAt": now}},
    )

    return CheckInResponse(
        _id=str(result.inserted_id),
        habitId=request.habitId,
        userId=user_id,
        checkInDate=today_start.isoformat(),
        checkInTime=now.isoformat(),
        note=request.note,
        createdAt=now.isoformat(),
    )


@router.get("/today", response_model=list[CheckInResponse])
async def get_today_checkins(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)

    cursor = checkins_collection.find({"userId": user_id, "checkInDate": {"$gte": today_start, "$lt": today_end}})
    docs = await cursor.to_list(length=100)

    return [
        CheckInResponse(
            _id=str(d["_id"]),
            habitId=d["habitId"],
            userId=d.get("userId", ""),
            checkInDate=d["checkInDate"].date().isoformat() if isinstance(d["checkInDate"], datetime) else str(d["checkInDate"]),
            checkInTime=d["checkInTime"].isoformat() if isinstance(d["checkInTime"], datetime) else str(d["checkInTime"]),
            note=d.get("note"),
            createdAt=d["createdAt"].isoformat() if isinstance(d["createdAt"], datetime) else str(d["createdAt"]),
        )
        for d in docs
    ]


@router.get("/dates", response_model=list[CheckInDateInfo])
async def get_checkin_dates(year: int, month: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    cursor = checkins_collection.find({
        "userId": user_id,
        "checkInDate": {"$gte": start, "$lt": end},
    })
    docs = await cursor.to_list(length=1000)

    date_counts: dict[str, int] = {}
    for d in docs:
        dt = d["checkInDate"]
        ds = dt.date().isoformat() if isinstance(dt, datetime) else str(dt)
        date_counts[ds] = date_counts.get(ds, 0) + 1

    active_habits = await habits_collection.count_documents({"userId": user_id, "status": "active"})

    result = []
    current = date(year, month, 1)
    month_end = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    while current < month_end:
        ds = current.isoformat()
        result.append(CheckInDateInfo(
            date=ds,
            count=date_counts.get(ds, 0),
            total=active_habits,
        ))
        current += timedelta(days=1)

    return result


@router.get("/week-stats", response_model=WeeklyStats)
async def get_week_stats(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    ws = datetime(week_start.year, week_start.month, week_start.day, tzinfo=timezone.utc)
    we = datetime(week_end.year, week_end.month, week_end.day, tzinfo=timezone.utc) + timedelta(days=1)

    cursor = checkins_collection.find({
        "userId": user_id,
        "checkInDate": {"$gte": ws, "$lt": we},
    })
    docs = await cursor.to_list(length=1000)

    date_counts: dict[str, int] = {}
    for d in docs:
        dt = d["checkInDate"]
        ds = dt.date().isoformat() if isinstance(dt, datetime) else str(dt)
        date_counts[ds] = date_counts.get(ds, 0) + 1

    total_checkins = len(docs)
    active_habits = await habits_collection.count_documents({"userId": user_id, "status": "active"})
    total_possible = active_habits * 7
    check_in_rate = round(total_checkins / total_possible, 2) if total_possible > 0 else 0

    best_day = max(date_counts, key=date_counts.get) if date_counts else week_start.isoformat()

    missed_days = []
    current = week_start
    while current <= week_end:
        ds = current.isoformat()
        if ds not in date_counts:
            missed_days.append(ds)
        current += timedelta(days=1)

    return WeeklyStats(
        totalCheckIns=total_checkins,
        totalHabits=active_habits,
        checkInRate=check_in_rate,
        bestDay=best_day,
        missedDays=missed_days,
    )
