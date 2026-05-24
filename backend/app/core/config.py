from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ultraflow"
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    JWT_SECRET: str = "ultraflow-secret-key-change-in-production"
    MIMO_API_KEY: str = ""
    MIMO_BASE_URL: str = "https://token-plan-cn.xiaomimimo.com/v1"
    MIMO_MODEL: str = "mimo-v2.5"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
