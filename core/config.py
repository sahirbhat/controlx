from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "ControlX"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = ConfigDict(env_file=".env")

settings = Settings()