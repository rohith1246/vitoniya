"""Shared Jinja2 template engine configuration."""

from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.config import get_settings

BASE_APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_APP_DIR / "templates"))
templates.env.globals["settings"] = get_settings()
