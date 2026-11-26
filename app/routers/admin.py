"""Admin-only console for courses, modules, lessons, and user management."""

import re

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.dependencies import require_roles
from app.models.course import Course, Lesson, Module
from app.models.progress import Enrollment
from app.models.user import User
from app.templating import templates

router = APIRouter(prefix="/admin", tags=["Admin"])


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "course"


@router.get("")
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    courses = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .order_by(Course.created_at.desc())
        .all()
    )
    total_enrollments = db.query(Enrollment).count()

    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        {
            "user": current_user,
            "users": users,
            "courses": courses,
            "total_enrollments": total_enrollments,
        },
    )


@router.post("/courses/create")
def create_course(
    title: str = Form(...),
    subtitle: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    level: str = Form(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    base_slug = _slugify(title)
    slug = base_slug
    counter = 1
    while db.query(Course).filter(Course.slug == slug).first():
        counter += 1
        slug = f"{base_slug}-{counter}"

    course = Course(
        title=title.strip(),
        slug=slug,
        subtitle=subtitle.strip(),
        description=description.strip(),
        category=category.strip() or "Engineering",
        level=level.strip() or "Beginner",
        is_published=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    return RedirectResponse(url=f"/admin/courses/{course.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/courses/{course_id}/toggle-publish")
def toggle_course_publish(
    course_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.is_published = not course.is_published
    db.commit()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/courses/{course_id}")
def manage_course(
    course_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    course = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return templates.TemplateResponse(
        request,
        "admin/course_manage.html",
        {"user": current_user, "course": course},
    )


@router.post("/courses/{course_id}/modules")
def add_module(
    course_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    next_order = db.query(Module).filter(Module.course_id == course_id).count() + 1
    db.add(Module(course_id=course_id, title=title.strip(), order_index=next_order))
    db.commit()
    return RedirectResponse(url=f"/admin/courses/{course_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/modules/{module_id}/lessons")
def add_lesson(
    module_id: int,
    title: str = Form(...),
    duration_mins: int = Form(15),
    video_url: str = Form(""),
    content_md: str = Form(""),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    mod = db.query(Module).filter(Module.id == module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found")

    next_order = db.query(Lesson).filter(Lesson.module_id == module_id).count() + 1
    db.add(
        Lesson(
            module_id=module_id,
            title=title.strip(),
            duration_mins=max(1, duration_mins),
            video_url=video_url.strip() or None,
            content_md=content_md.strip(),
            order_index=next_order,
        )
    )
    db.commit()
    return RedirectResponse(url=f"/admin/courses/{mod.course_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    if user_id == current_user.id:
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

    target = db.query(User).filter(User.id == user_id).first()
    if target:
        target.is_active = not target.is_active
        db.commit()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
