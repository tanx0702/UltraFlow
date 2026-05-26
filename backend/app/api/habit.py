from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from app.models.habit import (
    CreateHabitRequest,
    UpdateHabitRequest,
    HabitResponse,
    HabitStatus,
    Frequency,
)
from app.models.common import ApiResponse
from app.core.database import habits_collection
from app.core.deps import get_current_user

router = APIRouter(prefix="/habits", tags=["habits"])


def habit_doc_to_response(doc: dict) -> HabitResponse:
    created = doc.get("createdAt", datetime.utcnow())
    updated = doc.get("updatedAt", datetime.utcnow())
    return HabitResponse(
        _id=str(doc["_id"]),
        userId=doc.get("userId", ""),
        name=doc["name"],
        target=doc["target"],
        frequency=doc.get("frequency", "daily"),
        specificDays=doc.get("specificDays"),
        reminderTime=doc.get("reminderTime"),
        status=doc.get("status", "active"),
        streak=doc.get("streak", 0),
        bestStreak=doc.get("bestStreak", 0),
        totalCheckIns=doc.get("totalCheckIns", 0),
        createdAt=created.isoformat() if isinstance(created, datetime) else str(created),
        updatedAt=updated.isoformat() if isinstance(updated, datetime) else str(updated),
    )


@router.get("", response_model=ApiResponse[list[HabitResponse]])
async def get_habits(current_user: dict = Depends(get_current_user)):
    cursor = habits_collection.find({
        "userId": current_user["_id"],
        "status": {"$ne": HabitStatus.ARCHIVED.value},
    })
    habits = await cursor.to_list(length=100)
    return ApiResponse(data=[habit_doc_to_response(h) for h in habits]).model_dump()


@router.get("/today", response_model=ApiResponse[list[HabitResponse]])
async def get_today_habits(current_user: dict = Depends(get_current_user)):
    from datetime import date
    today = date.today()
    weekday = today.isoweekday()

    cursor = habits_collection.find({
        "userId": current_user["_id"],
        "status": HabitStatus.ACTIVE.value,
    })
    habits = await cursor.to_list(length=100)

    result = []
    for h in habits:
        freq = h.get("frequency", "daily")
        if freq == "daily":
            result.append(h)
        elif freq == "weekly":
            specific_days = h.get("specificDays", [])
            if not specific_days or weekday in specific_days:
                result.append(h)

    return ApiResponse(data=[habit_doc_to_response(h) for h in result]).model_dump()


@router.post("", response_model=ApiResponse[HabitResponse], status_code=201)
async def create_habit(request: CreateHabitRequest, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    habit_doc = {
        "userId": current_user["_id"],
        "name": request.name,
        "target": request.target,
        "frequency": request.frequency.value,
        "specificDays": request.specificDays,
        "reminderTime": request.reminderTime,
        "status": HabitStatus.ACTIVE.value,
        "streak": 0,
        "bestStreak": 0,
        "totalCheckIns": 0,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await habits_collection.insert_one(habit_doc)
    habit_doc["_id"] = result.inserted_id
    return ApiResponse(data=habit_doc_to_response(habit_doc)).model_dump()


@router.put("/{habit_id}", response_model=ApiResponse[HabitResponse])
async def update_habit(habit_id: str, request: UpdateHabitRequest):
    update_data = {"updatedAt": datetime.utcnow()}
    if request.name is not None:
        update_data["name"] = request.name
    if request.target is not None:
        update_data["target"] = request.target
    if request.reminderTime is not None:
        update_data["reminderTime"] = request.reminderTime

    result = await habits_collection.update_one(
        {"_id": ObjectId(habit_id)},
        {"$set": update_data},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="习惯不存在")

    habit = await habits_collection.find_one({"_id": ObjectId(habit_id)})
    return ApiResponse(data=habit_doc_to_response(habit)).model_dump()


@router.put("/{habit_id}/pause", response_model=ApiResponse[str])
async def pause_habit(habit_id: str):
    result = await habits_collection.update_one(
        {"_id": ObjectId(habit_id)},
        {"$set": {"status": HabitStatus.PAUSED.value, "updatedAt": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="习惯不存在")
    return ApiResponse(data="paused").model_dump()


@router.put("/{habit_id}/resume", response_model=ApiResponse[str])
async def resume_habit(habit_id: str):
    result = await habits_collection.update_one(
        {"_id": ObjectId(habit_id)},
        {"$set": {"status": HabitStatus.ACTIVE.value, "updatedAt": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="习惯不存在")
    return ApiResponse(data="active").model_dump()


@router.delete("/{habit_id}", response_model=ApiResponse[None])
async def delete_habit(habit_id: str):
    result = await habits_collection.update_one(
        {"_id": ObjectId(habit_id)},
        {"$set": {"status": HabitStatus.ARCHIVED.value, "updatedAt": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="习惯不存在")
    return ApiResponse().model_dump()
