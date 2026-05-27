from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ultraflow"
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    JWT_SECRET: str = "ultraflow-secret-key-change-in-production"

    # LLM API
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://token-plan-cn.xiaomimimo.com/v1"
    LLM_MODEL: str = "mimo-v2.5-pro"

    # LLM params
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1024

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
