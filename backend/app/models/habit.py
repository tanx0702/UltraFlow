from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"  # 旧值，向后兼容，读取时映射为 weekly_days
    WEEKLY_DAYS = "weekly_days"
    WEEKLY_COUNT = "weekly_count"
    CHALLENGE = "challenge"


class HabitStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CreateHabitRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    target: str = Field(..., min_length=1, max_length=100)
    frequency: Frequency = Frequency.DAILY
    specificDays: Optional[list[int]] = None
    weeklyCount: Optional[int] = Field(None, ge=1, le=7)
    targetDays: Optional[int] = Field(None, ge=1, le=365)
    reminderTime: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    icon: Optional[str] = None
    color: Optional[str] = None


class UpdateHabitRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    target: Optional[str] = Field(None, min_length=1, max_length=100)
    frequency: Optional[Frequency] = None
    specificDays: Optional[list[int]] = None
    weeklyCount: Optional[int] = Field(None, ge=1, le=7)
    targetDays: Optional[int] = Field(None, ge=1, le=365)
    reminderTime: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    icon: Optional[str] = None
    color: Optional[str] = None


class HabitResponse(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    name: str
    target: str
    frequency: Frequency
    specificDays: Optional[list[int]] = None
    weeklyCount: Optional[int] = None
    targetDays: Optional[int] = None
    reminderTime: Optional[str] = None
    icon: str = "📋"
    color: str = "#3B82F6"
    status: HabitStatus
    streak: int = 0
    bestStreak: int = 0
    totalCheckIns: int = 0
    createdAt: str
    updatedAt: str


class CheckInRequest(BaseModel):
    habitId: str
    note: Optional[str] = None


class CheckInResponse(BaseModel):
    id: str = Field(alias="_id")
    habitId: str
    userId: str
    checkInDate: str
    checkInTime: str
    note: Optional[str] = None
    createdAt: str


class CheckInDateInfo(BaseModel):
    date: str
    count: int
    total: int


class WeeklyStats(BaseModel):
    totalCheckIns: int
    totalHabits: int
    checkInRate: float
    bestDay: str
    missedDays: list[str]


class WeekDayStatus(BaseModel):
    date: str
    dayLabel: str
    checkInCount: int
    totalHabits: int
    completed: bool
    isToday: bool
