from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# Collections
habits_collection = db["habits"]
users_collection = db["users"]
checkins_collection = db["checkins"]
chat_history_collection = db["chat_history"]


async def create_indexes():
    """启动时创建索引，加速常用查询。"""
    # users: openid 唯一索引（登录查重）
    await users_collection.create_index("openid", unique=True)

    # habits: userId + status（查活跃习惯）、userId + createdAt（按创建时间排序）
    await habits_collection.create_index([("userId", 1), ("status", 1)])
    await habits_collection.create_index([("userId", 1), ("createdAt", -1)])

    # checkins: habitId + checkInDate 唯一（防重复打卡）、userId + checkInDate（查用户打卡）
    await checkins_collection.create_index([("habitId", 1), ("checkInDate", 1)], unique=True)
    await checkins_collection.create_index([("userId", 1), ("checkInDate", -1)])

    # chat_history: conversationId + createdAt（按时间加载对话）
    await chat_history_collection.create_index([("conversationId", 1), ("createdAt", 1)])
