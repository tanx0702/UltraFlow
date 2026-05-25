import httpx
import jwt
import time
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from app.models.user import (
    LoginByCodeRequest,
    LoginByCodeResponse,
    UserObject,
    UserProfile,
    UpdateCoachPersonaRequest,
    UpdateReminderRequest,
)
from app.core.database import users_collection
from app.core.config import get_settings
from app.core.deps import get_current_user

router = APIRouter(tags=["user"])


def generate_token(user_id: str) -> str:
    settings = get_settings()
    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + 86400 * 30,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def format_user(doc: dict) -> UserObject:
    return UserObject(
        _id=str(doc["_id"]),
        openid=doc.get("openid", ""),
        nickname=doc.get("nickname", ""),
        avatar=doc.get("avatar", ""),
        coachPersona=doc.get("coachPersona", "rational_mentor"),
        reminderEnabled=doc.get("reminderEnabled", False),
        createdAt=doc.get("createdAt", datetime.utcnow()).isoformat() if isinstance(doc.get("createdAt"), datetime) else doc.get("createdAt", ""),
        updatedAt=doc.get("updatedAt", datetime.utcnow()).isoformat() if isinstance(doc.get("updatedAt"), datetime) else doc.get("updatedAt", ""),
    )


@router.post("/auth/login", response_model=LoginByCodeResponse)
async def login_by_code(request: LoginByCodeRequest):
    settings = get_settings()

    wechat_url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "js_code": request.code,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(wechat_url, params=params)
        data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise HTTPException(status_code=401, detail="微信登录失败")

    openid = data.get("openid")
    if not openid:
        raise HTTPException(status_code=401, detail="获取openid失败")

    now = datetime.utcnow()
    # 用 upsert 原子操作：有则更新，无则插入（避免并发登录产生重复记录）
    result = await users_collection.find_one_and_update(
        {"openid": openid},
        {"$set": {"updatedAt": now}},
        upsert=True,
        return_document=True,
    )
    user = result

    # 判断是否新用户（没有 coachPersona 说明是刚创建的）
    is_new_user = "coachPersona" not in user

    # 新用户补全默认字段
    if is_new_user:
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "nickname": f"用户{openid[-6:]}",
                "avatar": "",
                "coachPersona": "rational_mentor",
                "reminderEnabled": False,
                "createdAt": now,
            }},
        )
        user["nickname"] = f"用户{openid[-6:]}"
        user["coachPersona"] = "rational_mentor"

    token = generate_token(str(user["_id"]))

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"token": token, "lastLoginAt": now}},
    )

    return LoginByCodeResponse(
        token=token,
        user=format_user(user),
        isNewUser=is_new_user,
    )


@router.get("/user/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    user = current_user
    return UserProfile(
        _id=str(user["_id"]),
        openid=user.get("openid", ""),
        nickname=user.get("nickname", ""),
        avatar=user.get("avatar", ""),
        coachPersona=user.get("coachPersona", "rational_mentor"),
        reminderEnabled=user.get("reminderEnabled", False),
        createdAt=user.get("createdAt", datetime.utcnow()).isoformat() if isinstance(user.get("createdAt"), datetime) else str(user.get("createdAt", "")),
        updatedAt=user.get("updatedAt", datetime.utcnow()).isoformat() if isinstance(user.get("updatedAt"), datetime) else str(user.get("updatedAt", "")),
    )


@router.put("/user/coach-persona")
async def update_coach_persona(request: UpdateCoachPersonaRequest, current_user: dict = Depends(get_current_user)):
    result = await users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": {"coachPersona": request.coachPersona, "updatedAt": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"success": True, "coachPersona": request.coachPersona}


@router.put("/user/reminder")
async def update_reminder(request: UpdateReminderRequest, current_user: dict = Depends(get_current_user)):
    result = await users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": {"reminderEnabled": request.reminderEnabled, "updatedAt": datetime.utcnow()}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"success": True}


@router.post("/user/logout")
async def logout():
    return {"message": "已退出登录"}
