import os
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:changeme@db:5432/mydatabase"
)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRES_MINUTES", "1440"))  # default 24h


@lru_cache()
def get_settings():
    return Settings()
