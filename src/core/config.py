from typing import Any, Dict, Optional

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Customer Support Assistant"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Groq API
    GROQ_API_KEY: str
    GROQ_API_URL: str = "https://api.groq.com/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 