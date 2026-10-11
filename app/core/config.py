import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups"

DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DB_PATH = DATA_DIR / "knowledge.db"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Knowledge Graph"
    API_V1_STR: str = ""
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = DATA_DIR
    BACKUPS_DIR: Path = BACKUPS_DIR
    DATABASE_PATH: Path = DEFAULT_DB_PATH
    DATABASE_URL: str = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(case_sensitive=True, extra="ignore")

settings = Settings()
