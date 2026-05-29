from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, date, timedelta, timezone
from bson import ObjectId
from app.models.habit import CheckInRequest, CheckInResponse, CheckInDateInfo, WeeklyStats, WeekDayStatus
from app.models.common import ApiResponse
from app.core.database import habits_collection, checkins_collection
from app.core.deps import get_current_user

router = APIRouter(prefix="/checkins", tags=["checkins"])


async def _calc_streak(habit_id: str, user_id: str, habit_doc: dict) -> tuple[int, int]:
    """计算当前连续和最佳连续。

    - daily / weekly_days / challenge：按天连续
    - weekly_count：按周连续（每周达标 >= weeklyCount 次）
    返回 (current_streak, best_streak)。
    """
    freq = habit_doc.get("frequency", "daily")
    if freq == "weekly":
        freq = "weekly_days"

    today = date.today()
    one_year_ago = today - timedelta(days=365)
    cursor = checkins_collection.find(
        {"habitId": habit_id, "userId": user_id, "checkInDate": {"$gte": datetime(one_year_ago.year, one_year_ago.month, one_year_ago.day)}},
        {"checkInDate": 1},
    ).sort("checkInDate", -1)
    docs = await cursor.to_list(length=365)

    # ── weekly_count：按周连续 ──
    if freq == "weekly_count":
        weekly_target = habit_doc.get("weeklyCount", 3)
        # 按 ISO 周分组计数
        week_counts: dict[str, int] = {}
        for d in docs:
            dt = d["checkInDate"]
            if isinstance(dt, datetime):
                dt_date = dt.date()
            else:
                dt_date = date.fromisoformat(str(dt))
            iso = dt_date.isocalendar()
            week_key = f"{iso[0]}-W{iso[1]:02d}"
            week_counts[week_key] = week_counts.get(week_key, 0) + 1

        # 生成过去 52 周的列表（从本周往前）
        current_iso = today.isocalendar()
        weeks = []
        for i in range(52):
            d = today - timedelta(days=i * 7)
            iso = d.isocalendar()
            wk = f"{iso[0]}-W{iso[1]:02d}"
            if wk not in [w[0] for w in weeks]:
                weeks.append((wk, week_counts.get(wk, 0)))

        current_streak = 0
        for wk, count in weeks:
            if count >= weekly_target:
                current_streak += 1
            else:
                break

        best_streak = 0
        run = 0
        for wk, count in weeks:
            if count >= weekly_target:
                run += 1
                best_streak = max(best_streak, run)
            else:
                run = 0
        best_streak = max(best_streak, current_streak)
        return current_streak, best_streak

    # ── daily / weekly_days / challenge：按天连续 ──
    checked_dates = set()
    for d in docs:
        dt = d["checkInDate"]
        if isinstance(dt, datetime):
            checked_dates.add(dt.date().isoformat())
        else:
            checked_dates.add(str(dt))

    current_streak = 0
    day = today
    while day.isoformat() in checked_dates:
        current_streak += 1
        day -= timedelta(days=1)

    # challenge 模式：按天连续，上限 targetDays
    if freq == "challenge":
        target = habit_doc.get("targetDays", 21)
        current_streak = min(current_streak, target)

    if not checked_dates:
        return current_streak, 0

    sorted_dates = sorted(checked_dates)
    best_streak = 1
    run = 1
    for i in range(1, len(sorted_dates)):
        prev = date.fromisoformat(sorted_dates[i - 1])
        curr = date.fromisoformat(sorted_dates[i])
        if (curr - prev).days == 1:
            run += 1
            best_streak = max(best_streak, run)
        else:
            run = 1

    best_streak = max(best_streak, current_streak)
    if freq == "challenge":
        best_streak = min(best_streak, target)
    return current_streak, best_streak


@router.post("", response_model=ApiResponse[CheckInResponse], status_code=201)
async def check_in(request: CheckInRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)

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

    habit_doc = await habits_collection.find_one({"_id": ObjectId(request.habitId)})
    current_streak, best_streak = await _calc_streak(request.habitId, user_id, habit_doc or {})
    await habits_collection.update_one(
        {"_id": ObjectId(request.habitId)},
        {"$inc": {"totalCheckIns": 1}, "$set": {"streak": current_streak, "bestStreak": best_streak, "updatedAt": now}},
    )

    return ApiResponse(
        data=CheckInResponse(
            _id=str(result.inserted_id),
            habitId=request.habitId,
            userId=user_id,
            checkInDate=today_start.isoformat(),
            checkInTime=now.isoformat(),
            note=request.note,
            createdAt=now.isoformat(),
        ),
    ).model_dump()


@router.get("/today", response_model=ApiResponse[list[CheckInResponse]])
async def get_today_checkins(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)

    cursor = checkins_collection.find({"userId": user_id, "checkInDate": {"$gte": today_start, "$lt": today_end}})
    docs = await cursor.to_list(length=100)

    return ApiResponse(data=[
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
    ]).model_dump()


@router.get("/dates", response_model=ApiResponse[list[CheckInDateInfo]])
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

    return ApiResponse(data=result).model_dump()


@router.get("/habit/{habit_id}", response_model=ApiResponse[list[CheckInDateInfo]])
async def get_habit_checkin_dates(
    habit_id: str,
    year: int,
    month: int,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["_id"]
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    docs = await checkins_collection.find({
        "userId": user_id,
        "habitId": habit_id,
        "checkInDate": {"$gte": start, "$lt": end},
    }).to_list(length=31)

    checked_dates = set()
    for d in docs:
        dt = d["checkInDate"]
        ds = dt.date().isoformat() if isinstance(dt, datetime) else str(dt)
        checked_dates.add(ds)

    result = []
    current = date(year, month, 1)
    month_end = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    while current < month_end:
        ds = current.isoformat()
        result.append(CheckInDateInfo(
            date=ds,
            count=1 if ds in checked_dates else 0,
            total=1,
        ))
        current += timedelta(days=1)

    return ApiResponse(data=result).model_dump()


@router.get("/week-days", response_model=ApiResponse[list[WeekDayStatus]])
async def get_week_day_statuses(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    total_habits = await habits_collection.count_documents({
        "userId": user_id, "status": "active"
    })

    day_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    result = []
    for i in range(7):
        d = monday + timedelta(days=i)
        start_dt = datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(days=1)
        count = await checkins_collection.count_documents({
            "userId": user_id,
            "checkInDate": {"$gte": start_dt, "$lt": end_dt},
        })
        result.append(WeekDayStatus(
            date=d.isoformat(),
            dayLabel=day_labels[i],
            checkInCount=count,
            totalHabits=total_habits,
            completed=(count >= total_habits and total_habits > 0),
            isToday=(d == today),
        ))
    return ApiResponse(data=result).model_dump()


@router.get("/week-stats", response_model=ApiResponse[WeeklyStats])
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

    return ApiResponse(
        data=WeeklyStats(
            totalCheckIns=total_checkins,
            totalHabits=active_habits,
            checkInRate=check_in_rate,
            bestDay=best_day,
            missedDays=missed_days,
        ),
    ).model_dump()
