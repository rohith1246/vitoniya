"""Idempotent database seeding for Admin user and rich SEO curriculum."""

import re

from sqlalchemy.orm import Session

from app.config import get_settings
from app.curriculum_data import CURRICULUM_DATA
from app.models.course import Course, Lesson, Module
from app.models.user import User
from app.security import hash_password

settings = get_settings()


def slugify_text(text: str) -> str:
    """Convert any title into a clean URL-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "lesson"


def _sync_course(db: Session, data: dict) -> None:
    course = db.query(Course).filter(Course.slug == data["slug"]).first()
    if not course:
        course = Course(
            title=data["title"],
            slug=data["slug"],
            subtitle=data["subtitle"],
            description=data["description"],
            category=data["category"],
            level=data["level"],
            is_published=True,
        )
        db.add(course)
        db.flush()

    for m_idx, mod_data in enumerate(data["modules"], start=1):
        mod = (
            db.query(Module)
            .filter(Module.course_id == course.id, Module.title == mod_data["title"])
            .first()
        )
        if not mod:
            mod = Module(course_id=course.id, title=mod_data["title"], order_index=m_idx)
            db.add(mod)
            db.flush()

        for l_idx, lesson_data in enumerate(mod_data["lessons"], start=1):
            l_slug = slugify_text(lesson_data["title"])
            existing_lesson = (
                db.query(Lesson)
                .filter(
                    Lesson.module_id == mod.id,
                    (Lesson.slug == l_slug) | (Lesson.title == lesson_data["title"]),
                )
                .first()
            )
            if not existing_lesson:
                db.add(
                    Lesson(
                        module_id=mod.id,
                        title=lesson_data["title"],
                        slug=l_slug,
                        duration_mins=lesson_data["duration_mins"],
                        order_index=l_idx,
                        content_md=lesson_data["content_md"],
                    )
                )
            else:
                if not existing_lesson.slug:
                    existing_lesson.slug = l_slug
                # Automatically upgrade thin starter notes without overwriting longer custom edits
                if len(existing_lesson.content_md or "") < 900 and len(lesson_data["content_md"]) > len(existing_lesson.content_md or ""):
                    existing_lesson.content_md = lesson_data["content_md"]
                    existing_lesson.duration_mins = lesson_data["duration_mins"]


def _backfill_lesson_slugs(db: Session) -> None:
    """Ensure every existing lesson has a unique slug."""
    lessons_without_slug = db.query(Lesson).filter(Lesson.slug.is_(None)).all()
    if not lessons_without_slug:
        return
    for lesson in lessons_without_slug:
        base = slugify_text(lesson.title)
        lesson.slug = f"{base}-{lesson.id}" if db.query(Lesson).filter(Lesson.slug == base).first() else base
    db.commit()


def seed_initial_data(db: Session) -> None:
    """Create initial admin account, backfill slugs, and sync starter curriculum."""
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            full_name=settings.ADMIN_NAME,
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()

    _backfill_lesson_slugs(db)

    for c_data in CURRICULUM_DATA:
        _sync_course(db, c_data)

    db.commit()
