"""Authentication and Role-Based Access Control (RBAC) dependencies."""

from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.security import decode_access_token

settings = get_settings()


class AuthRedirectException(Exception):
    """Raised when an unauthenticated browser request hits a protected HTML page."""


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Return the logged-in active User from cookie JWT, or None for guests."""
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        return None

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        return None

    user = db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first()
    return user


def get_current_user(
    request: Request,
    user: Optional[User] = Depends(get_optional_user),
) -> User:
    """Require an authenticated user; redirect HTML routes to /login, return 401 for APIs."""
    if user is None:
        if request.url.path.startswith("/api/"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        raise AuthRedirectException()
    return user


def require_roles(*allowed_roles: str) -> Callable:
    """RBAC dependency factory: allow only users whose role is in allowed_roles."""

    def _role_guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return current_user

    return _role_guard
