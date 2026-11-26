"""Password hashing (bcrypt) and JWT session token helpers."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from app.config import get_settings

settings = get_settings()


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(user_id: int, role: str) -> str:
    """Create a signed JWT token containing user ID and role."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token; return None if invalid or expired."""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
