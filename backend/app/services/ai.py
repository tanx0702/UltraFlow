import json
import re
from datetime import datetime, timezone

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.core.database import chat_history_collection, habits_collection
from app.prompts import BASE_SYSTEM_PROMPT, FEW_SHOT_EXAMPLES, PERSONA_VARIANTS, SAFETY_RULES

# ─── Valid Values ─────────────────────────────────────────────────────────────

VALID_ACTIONS = {"CREATE_HABIT", "ADJUST_HABIT", "PAUSE_HABIT", None}
VALID_FREQUENCIES = {"daily", "weekly"}

MAX_HISTORY_MESSAGES = 20


# ─── Prompt Assembly ──────────────────────────────────────────────────────────


def assemble_prompt(persona: str, user_context: str) -> str:
    persona_prompt = PERSONA_VARIANTS.get(persona, PERSONA_VARIANTS["rational_mentor"])
    parts = [BASE_SYSTEM_PROMPT, persona_prompt, SAFETY_RULES, FEW_SHOT_EXAMPLES]
    if user_context:
        parts.append(f"## 用户上下文\n\n{user_context}")
    return "\n\n".join(parts)


async def build_user_context(user_doc: dict | None) -> str:
    if not user_doc:
        return ""

    nickname = user_doc.get("nickname", "用户")
    persona = user_doc.get("coachPersona", "rational_mentor")

    user_id = user_doc.get("userId") or user_doc.get("_id")

    context = (
        f"- 昵称：{nickname}\n"
        f"- 当前人设：{persona}\n"
        f"- 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )

    if user_id:
        habits = await habits_collection.find(
            {"userId": user_id, "status": "active"}
        ).to_list(50)

        if habits:
            habit_lines = []
            for h in habits:
                habit_lines.append(
                    f"  - {h['name']}（目标：{h['target']}，"
                    f"{h['frequency']}，提醒 {h.get('reminderTime', '无')}）"
                )
            context += "- 已有活跃习惯：\n" + "\n".join(habit_lines) + "\n"
        else:
            context += "- 已有活跃习惯：无\n"

    return context


# ─── LLM API Call ──────────────────────────────────────────────────────────────


async def call_llm(system_prompt: str, messages: list[dict]) -> str:
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)
    completion = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "system", "content": system_prompt}, *messages],
        response_format={"type": "json_object"},
        max_completion_tokens=settings.LLM_MAX_TOKENS,
        temperature=settings.LLM_TEMPERATURE,
    )
    return completion.choices[0].message.content


# ─── Output Parsing ───────────────────────────────────────────────────────────


def parse_llm_output(raw: str) -> dict:
    # 优先直接解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 正则提取 markdown 代码块中的 JSON
    m = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # 兜底正则提取大括号内容
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    return {"reply": raw.strip(), "extractedHabit": None}


def validate_extracted_habit(habit: dict | None) -> dict | None:
    if habit is None:
        return None

    if not isinstance(habit, dict):
        return None

    if habit.get("action") not in VALID_ACTIONS:
        return None

    name = habit.get("habitName")
    if not name or len(name) > 20:
        return None

    if not habit.get("target"):
        return None

    freq = habit.get("frequency")
    if freq not in VALID_FREQUENCIES:
        habit["frequency"] = "daily"

    reminder = habit.get("reminderTime")
    if reminder:
        try:
            datetime.strptime(reminder, "%H:%M")
        except ValueError:
            habit["reminderTime"] = None

    return habit


# ─── Conversation History ─────────────────────────────────────────────────────


async def load_conversation(conversation_id: str) -> list[dict]:
    cursor = chat_history_collection.find(
        {"conversationId": conversation_id}
    ).sort("createdAt", 1)
    docs = await cursor.to_list(length=200)
    messages = []
    for doc in docs:
        messages.append({"role": doc["role"], "content": doc["content"]})
    return messages[-MAX_HISTORY_MESSAGES:]


async def save_message(
    conversation_id: str,
    role: str,
    content: str,
    user_id: str = "",
    extracted_habit: dict | None = None,
):
    doc = {
        "conversationId": conversation_id,
        "userId": user_id,
        "role": role,
        "content": content,
        "extractedHabit": extracted_habit,
        "createdAt": datetime.now(timezone.utc),
    }
    await chat_history_collection.insert_one(doc)