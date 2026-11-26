"""Application configuration loaded from environment variables."""

import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central settings for Vitoniya Edu."""

    APP_NAME: str = "Vitoniya Edu"
    COMPANY_NAME: str = "Vitoniya Labs"
    SITE_URL: str = os.getenv("SITE_URL", "https://vitoniya.com").rstrip("/")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # PostgreSQL in production (Render/Neon), SQLite fallback for local dev
    _raw_db_url: str = os.getenv("DATABASE_URL", "sqlite:///./vitoniya_edu.db")
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL: str = _raw_db_url

    JWT_SECRET: str = os.getenv("JWT_SECRET", "vitoniya-edu-dev-secret-change-in-prod")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days
    COOKIE_NAME: str = "vitoniya_session"
    COOKIE_SECURE: bool = os.getenv("ENVIRONMENT", "development") == "production"

    # Initial Admin Seed Credentials (override via .env in production)
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "rohith@vitoniya.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "VitoniyaAdmin@2026")
    ADMIN_NAME: str = os.getenv("ADMIN_NAME", "Rohith Vuppula")
    ADSENSE_CLIENT_ID: str = os.getenv("ADSENSE_CLIENT_ID", "").strip()


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
