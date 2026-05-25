import uuid
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.core.database import habits_collection
from app.core.deps import get_current_user
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
    user_id = current_user["_id"]
    await save_message(conversation_id, "user", request.message, user_id=user_id)
    await save_message(conversation_id, "assistant", reply, user_id=user_id, extracted_habit=extracted)

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
