from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str = "AI Todo Application"
    API_VERSION: str = "v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database settings
    DATABASE_URL: str
    
    # Auth settings
    AUTH_SECRET: str
    AUTH_FRONTEND_URL: str
    
    # Allowed origins for CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()