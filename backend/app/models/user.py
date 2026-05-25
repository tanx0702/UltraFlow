from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoginByCodeRequest(BaseModel):
    code: str = Field(..., min_length=1)


class UserObject(BaseModel):
    _id: str
    openid: str
    nickname: str
    avatar: str
    coachPersona: str = "rational_mentor"
    reminderEnabled: bool = False
    createdAt: str
    updatedAt: str


class LoginByCodeResponse(BaseModel):
    token: str
    user: UserObject
    isNewUser: bool


class UserProfile(BaseModel):
    _id: str
    openid: str
    nickname: str
    avatar: str
    coachPersona: str = "rational_mentor"
    reminderEnabled: bool = False
    createdAt: str
    updatedAt: str


class UpdateCoachPersonaRequest(BaseModel):
    coachPersona: str = Field(..., pattern="^(drill_sergeant|healing_friend|rational_mentor)$")


class UpdateReminderRequest(BaseModel):
    reminderEnabled: bool


class UpdateProfileRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None
