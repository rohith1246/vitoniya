"""JSON API endpoints for health checks and OpenAPI documentation."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.course import Course
from app.models.user import User

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/health")
def health_check():
    """Service health check for Render and uptime monitors."""
    return {"status": "ok", "service": "vitoniya-edu"}


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    """Return authenticated user profile and RBAC role."""
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.get("/courses")
def list_published_courses(db: Session = Depends(get_db)):
    """Return published courses as JSON."""
    courses = db.query(Course).filter(Course.is_published.is_(True)).order_by(Course.id.asc()).all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "subtitle": c.subtitle,
            "category": c.category,
            "level": c.level,
        }
        for c in courses
    ]
