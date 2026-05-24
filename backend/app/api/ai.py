import uuid
from datetime import datetime

import jwt
from bson import ObjectId
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import get_settings
from app.core.database import habits_collection, users_collection
from app.models.ai import ChatRequest, ChatResponse, ConfirmHabitRequest, HabitCardData
from app.models.habit import Frequency
from app.services.ai import (
    assemble_prompt,
    build_user_context,
    call_mimo,
    load_conversation,
    parse_llm_output,
    save_message,
    validate_extracted_habit,
)

router = APIRouter(prefix="/ai", tags=["ai"])


async def get_current_user(token: str | None = Header(None, alias="token")) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="未登录")
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="无效token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效token")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    user["_id"] = str(user["_id"])
    return user


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    conversation_id = request.conversationId or str(uuid.uuid4())

    # Load conversation history
    history = await load_conversation(conversation_id)

    # Build user context
    user_doc = current_user
    user_context = await build_user_context(user_doc)

    # Assemble system prompt
    persona = user_doc.get("coachPersona", "rational_mentor")
    system_prompt = assemble_prompt(persona, user_context)

    # Build messages
    messages = history + [{"role": "user", "content": request.message}]

    try:
        raw = await call_mimo(system_prompt, messages)
        parsed = parse_llm_output(raw)
    except Exception as e:
        print(f"[AI ERROR] {type(e).__name__}: {e}")
        return ChatResponse(
            reply="抱歉，我正在思考中，请稍后再试～",
            conversationId=conversation_id,
            extractedHabit=None,
        )

    reply = parsed.get("reply", "")
    extracted = validate_extracted_habit(parsed.get("extractedHabit"))
    extracted_habit = None
    if extracted:
        extracted_habit = HabitCardData(
            action=extracted.get("action", "CREATE_HABIT"),
            habitName=extracted["habitName"],
            target=extracted["target"],
            frequency=Frequency(extracted.get("frequency", "daily")),
            reminderTime=extracted.get("reminderTime"),
        )

    # Persist conversation
    await save_message(conversation_id, "user", request.message)
    await save_message(conversation_id, "assistant", reply, extracted)

    return ChatResponse(
        reply=reply,
        conversationId=conversation_id,
        extractedHabit=extracted_habit,
    )


@router.post("/confirm-habit")
async def confirm_habit(request: ConfirmHabitRequest, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    habit_doc = {
        "userId": current_user["_id"],
        "name": request.habitName,
        "target": request.target,
        "frequency": request.frequency.value,
        "reminderTime": request.reminderTime,
        "status": "active",
        "streak": 0,
        "bestStreak": 0,
        "totalCheckIns": 0,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await habits_collection.insert_one(habit_doc)

    return {
        "_id": str(result.inserted_id),
        "name": request.habitName,
        "target": request.target,
        "frequency": request.frequency.value,
        "reminderTime": request.reminderTime,
        "status": "active",
        "streak": 0,
        "bestStreak": 0,
        "totalCheckIns": 0,
        "createdAt": now.isoformat(),
        "updatedAt": now.isoformat(),
    }
