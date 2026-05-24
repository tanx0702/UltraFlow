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
