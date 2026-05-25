import jwt
from bson import ObjectId
from fastapi import Header, HTTPException

from app.core.config import get_settings
from app.core.database import users_collection


async def get_current_user(token: str | None = Header(None, alias="token")) -> dict:
    """从 JWT token 中解析当前用户，所有需要登录的接口共用此依赖。"""
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
