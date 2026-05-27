import json
import re
from datetime import datetime, timezone

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.core.database import chat_history_collection, habits_collection
from app.prompts import BASE_SYSTEM_PROMPT, FEW_SHOT_EXAMPLES, PERSONA_VARIANTS, SAFETY_RULES

# ─── Valid Values ─────────────────────────────────────────────────────────────

VALID_ACTIONS = {"CREATE_HABIT", "ADJUST_HABIT", "PAUSE_HABIT", None}
VALID_FREQUENCIES = {"daily", "weekly", "weekly_days", "weekly_count", "challenge"}

MAX_HISTORY_MESSAGES = 20


# ─── Prompt Assembly ──────────────────────────────────────────────────────────


def assemble_prompt(persona: str, user_context: str) -> str:
    persona_prompt = PERSONA_VARIANTS.get(persona, PERSONA_VARIANTS["rational_mentor"])
    parts = [BASE_SYSTEM_PROMPT, persona_prompt, SAFETY_RULES, FEW_SHOT_EXAMPLES]
    if user_context:
        parts.append(f"## 用户上下文\n\n{user_context}")
    return "\n\n".join(parts)


def _format_frequency(freq: str, specific_days=None, weekly_count=None, target_days=None) -> str:
    if freq == "daily":
        return "每天"
    if freq in ("weekly_days", "weekly"):
        days = specific_days or []
        if days:
            day_names = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
            return "每周" + "、".join(day_names.get(d, str(d)) for d in sorted(days))
        return "每周"
    if freq == "weekly_count":
        n = weekly_count or 3
        return f"每周{n}次"
    if freq == "challenge":
        n = target_days or 21
        return f"坚持{n}天挑战"
    return freq


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
                freq = h.get("frequency", "daily")
                freq_text = _format_frequency(freq, h.get("specificDays"), h.get("weeklyCount"), h.get("targetDays"))
                habit_lines.append(
                    f"  - {h['name']}（目标：{h['target']}，"
                    f"{freq_text}，提醒 {h.get('reminderTime', '无')}）"
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

    # 旧值 "weekly" 归一化为 "weekly_days"
    if freq == "weekly":
        habit["frequency"] = "weekly_days"

    specific_days = habit.get("specificDays")
    if specific_days is not None:
        if not isinstance(specific_days, list) or not all(isinstance(d, int) and 1 <= d <= 7 for d in specific_days):
            habit["specificDays"] = None

    # 校验 weeklyCount（仅 weekly_count 有效）
    wc = habit.get("weeklyCount")
    if wc is not None:
        if not isinstance(wc, int) or wc < 1 or wc > 7:
            habit["weeklyCount"] = None
    if habit["frequency"] == "weekly_count" and habit.get("weeklyCount") is None:
        habit["weeklyCount"] = 3

    # 校验 targetDays（仅 challenge 有效）
    td = habit.get("targetDays")
    if td is not None:
        if not isinstance(td, int) or td < 1 or td > 365:
            habit["targetDays"] = None
    if habit["frequency"] == "challenge" and habit.get("targetDays") is None:
        habit["targetDays"] = 21

    # 非对应频率的字段清空
    if habit["frequency"] != "weekly_days":
        habit["specificDays"] = None
    if habit["frequency"] != "weekly_count":
        habit["weeklyCount"] = None
    if habit["frequency"] != "challenge":
        habit["targetDays"] = None

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