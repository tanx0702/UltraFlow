from fastapi import APIRouter, HTTPException
from datetime import datetime, date, timedelta
from bson import ObjectId
from app.models.habit import CheckInRequest, CheckInResponse, CheckInDateInfo, WeeklyStats
from app.core.database import habits_collection, checkins_collection

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.post("", response_model=CheckInResponse, status_code=201)
async def check_in(request: CheckInRequest, user_id: str = ""):
    today = date.today().isoformat()
    now = datetime.utcnow()

    existing = await checkins_collection.find_one({
        "habitId": request.habitId,
        "userId": user_id,
        "checkInDate": today,
    })
    if existing:
        raise HTTPException(status_code=409, detail="今日已打卡")

    checkin_doc = {
        "habitId": request.habitId,
        "userId": user_id,
        "checkInDate": today,
        "checkInTime": now,
        "note": request.note,
        "createdAt": now,
    }
    result = await checkins_collection.insert_one(checkin_doc)

    await habits_collection.update_one(
        {"_id": ObjectId(request.habitId)},
        {"$inc": {"totalCheckIns": 1}, "$set": {"updatedAt": now}},
    )

    return CheckInResponse(
        _id=str(result.inserted_id),
        habitId=request.habitId,
        userId=user_id,
        checkInDate=today,
        checkInTime=now.isoformat(),
        note=request.note,
        createdAt=now.isoformat(),
    )


@router.get("/today", response_model=list[CheckInResponse])
async def get_today_checkins(user_id: str = ""):
    today = date.today().isoformat()
    cursor = checkins_collection.find({"userId": user_id, "checkInDate": today})
    docs = await cursor.to_list(length=100)

    return [
        CheckInResponse(
            _id=str(d["_id"]),
            habitId=d["habitId"],
            userId=d.get("userId", ""),
            checkInDate=d["checkInDate"],
            checkInTime=d["checkInTime"].isoformat() if isinstance(d["checkInTime"], datetime) else str(d["checkInTime"]),
            note=d.get("note"),
            createdAt=d["createdAt"].isoformat() if isinstance(d["createdAt"], datetime) else str(d["createdAt"]),
        )
        for d in docs
    ]


@router.get("/dates", response_model=list[CheckInDateInfo])
async def get_checkin_dates(year: int, month: int, user_id: str = ""):
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"

    cursor = checkins_collection.find({
        "userId": user_id,
        "checkInDate": {"$gte": start_date, "$lt": end_date},
    })
    docs = await cursor.to_list(length=1000)

    date_counts: dict[str, int] = {}
    for d in docs:
        dt = d["checkInDate"]
        date_counts[dt] = date_counts.get(dt, 0) + 1

    active_habits = await habits_collection.count_documents({"status": "active"})

    result = []
    current = date(year, month, 1)
    end = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    while current < end:
        ds = current.isoformat()
        result.append(CheckInDateInfo(
            date=ds,
            count=date_counts.get(ds, 0),
            total=active_habits,
        ))
        current += timedelta(days=1)

    return result


@router.get("/week-stats", response_model=WeeklyStats)
async def get_week_stats(user_id: str = ""):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    cursor = checkins_collection.find({
        "userId": user_id,
        "checkInDate": {"$gte": week_start.isoformat(), "$lte": week_end.isoformat()},
    })
    docs = await cursor.to_list(length=1000)

    date_counts: dict[str, int] = {}
    for d in docs:
        dt = d["checkInDate"]
        date_counts[dt] = date_counts.get(dt, 0) + 1

    total_checkins = len(docs)
    active_habits = await habits_collection.count_documents({"status": "active"})
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
