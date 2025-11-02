"""Database helpers (stub)."""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MONGO_URI: Optional[str]

settings = Settings()
