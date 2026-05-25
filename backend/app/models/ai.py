from pydantic import BaseModel, Field
from typing import Optional
from app.models.habit import Frequency


class HabitCardData(BaseModel):
    action: str = "CREATE_HABIT"
    habitName: str
    target: str
    frequency: Frequency
    reminderTime: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversationId: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    conversationId: Optional[str] = None
    extractedHabit: Optional[HabitCardData] = None


class ConfirmHabitRequest(BaseModel):
    habitName: str
    target: str
    frequency: Frequency
    reminderTime: Optional[str] = None
    force: bool = False
