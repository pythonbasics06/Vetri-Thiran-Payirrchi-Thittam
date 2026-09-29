from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    app_name: str = Field(default=os.getenv("APP_NAME", "PocketSmart AI"))
    app_env: str = Field(default=os.getenv("APP_ENV", "development"))
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev-only-change-me"))
    gemini_api_key: str = Field(default=os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db"))
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "5"))
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            x.strip() for x in os.getenv(
                "ALLOWED_ORIGINS",
                "http://127.0.0.1:8000,http://localhost:8000"
            ).split(",") if x.strip()
        ]
    )

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
