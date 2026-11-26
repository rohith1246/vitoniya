"""Public pages, SEO-indexable lesson reader, legal/support pages, and XML sitemap."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_optional_user
from app.models.course import Course, Module
from app.models.progress import Enrollment, LessonProgress
from app.models.user import User
from app.templating import templates

router = APIRouter(tags=["Public"])
settings = get_settings()


def _course_stats(courses: list[Course], user: Optional[User], db: Session) -> dict[int, dict]:
    """Compute real lesson duration and authenticated user progress per course."""
    completed_ids: set[int] = set()
    enrolled_ids: set[int] = set()

    if user:
        completed_ids = {
            r[0]
            for r in db.query(LessonProgress.lesson_id)
            .filter(LessonProgress.user_id == user.id, LessonProgress.is_completed.is_(True))
            .all()
        }
        enrolled_ids = {
            r[0]
            for r in db.query(Enrollment.course_id).filter(Enrollment.user_id == user.id).all()
        }

    stats: dict[int, dict] = {}
    for c in courses:
        lessons = [l for m in c.modules for l in m.lessons]
        total_mins = sum(l.duration_mins for l in lessons)
        total = len(lessons)
        done = sum(1 for l in lessons if l.id in completed_ids) if user else 0
        pct = int((done / total) * 100) if total > 0 else 0
        stats[c.id] = {
            "total_mins": total_mins,
            "is_enrolled": c.id in enrolled_ids,
            "progress_pct": pct,
            "first_lesson_id": lessons[0].id if lessons else None,
            "first_lesson_slug": lessons[0].slug if lessons else None,
        }
    return stats


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    courses = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.is_published.is_(True))
        .order_by(Course.created_at.asc())
        .all()
    )
    course_meta = _course_stats(courses, user, db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"user": user, "courses": courses, "course_meta": course_meta},
    )


@router.get("/courses")
def catalog(
    request: Request,
    q: Optional[str] = None,
    category: Optional[str] = None,
    level: Optional[str] = None,
    sort: Optional[str] = "newest",
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    query = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.is_published.is_(True))
    )
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Course.title.ilike(term),
                Course.subtitle.ilike(term),
                Course.description.ilike(term),
            )
        )
    if category and category != "All":
        query = query.filter(Course.category == category)
    if level and level != "All":
        query = query.filter(Course.level == level)

    if sort == "title":
        query = query.order_by(Course.title.asc())
    else:
        query = query.order_by(Course.created_at.asc())

    courses = query.all()
    if sort == "lessons":
        courses.sort(key=lambda c: c.total_lessons, reverse=True)

    categories = [
        row[0]
        for row in db.query(Course.category)
        .filter(Course.is_published.is_(True))
        .distinct()
        .all()
    ]
    course_meta = _course_stats(courses, user, db)

    return templates.TemplateResponse(
        request,
        "courses/catalog.html",
        {
            "user": user,
            "courses": courses,
            "course_meta": course_meta,
            "categories": categories,
            "search_query": q or "",
            "selected_category": category or "All",
            "selected_level": level or "All",
            "selected_sort": sort or "newest",
        },
    )


@router.get("/courses/{slug}")
def course_detail(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    course = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.slug == slug)
        .first()
    )
    if not course or (not course.is_published and (not user or user.role != "admin")):
        raise HTTPException(status_code=404, detail="This course is unavailable or does not exist.")

    stats = _course_stats([course], user, db)[course.id]
    first_lesson = None
    for mod in course.modules:
        if mod.lessons:
            first_lesson = mod.lessons[0]
            break

    return templates.TemplateResponse(
        request,
        "courses/detail.html",
        {
            "user": user,
            "course": course,
            "is_enrolled": stats["is_enrolled"],
            "progress_pct": stats["progress_pct"],
            "total_mins": stats["total_mins"],
            "first_lesson": first_lesson,
        },
    )


@router.get("/courses/{course_slug}/{lesson_slug}")
def public_lesson_reader(
    course_slug: str,
    lesson_slug: str,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Public SEO-indexable lesson page; logged-in students also get progress tracking."""
    course = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.slug == course_slug)
        .first()
    )
    if not course or (not course.is_published and (not user or user.role != "admin")):
        raise HTTPException(status_code=404, detail="Course not found.")

    ordered_lessons = [lesson for mod in course.modules for lesson in mod.lessons]
    current_idx = next(
        (i for i, l in enumerate(ordered_lessons) if l.slug == lesson_slug or str(l.id) == lesson_slug),
        None,
    )
    if current_idx is None:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    current_lesson = ordered_lessons[current_idx]
    prev_lesson = ordered_lessons[current_idx - 1] if current_idx > 0 else None
    next_lesson = ordered_lessons[current_idx + 1] if current_idx + 1 < len(ordered_lessons) else None

    completed_ids: set[int] = set()
    is_enrolled = False
    if user:
        is_enrolled = (
            db.query(Enrollment)
            .filter(Enrollment.user_id == user.id, Enrollment.course_id == course.id)
            .first()
            is not None
        )
        completed_ids = {
            row[0]
            for row in db.query(LessonProgress.lesson_id)
            .filter(LessonProgress.user_id == user.id, LessonProgress.is_completed.is_(True))
            .all()
        }

    total_lessons = len(ordered_lessons)
    completed_count = sum(1 for l in ordered_lessons if l.id in completed_ids) if user else 0
    progress_pct = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0

    return templates.TemplateResponse(
        request,
        "learn/lesson.html",
        {
            "user": user,
            "course": course,
            "lesson": current_lesson,
            "is_enrolled": is_enrolled,
            "chapter_number": current_idx + 1,
            "total_lessons": total_lessons,
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "completed_ids": completed_ids,
            "is_completed": current_lesson.id in completed_ids,
            "progress_pct": progress_pct,
            "is_public_seo": True,
        },
    )


@router.get("/about")
def about_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "about.html", {"user": user})


@router.get("/faq")
def faq_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "pages/faq.html", {"user": user})


@router.get("/contact")
def contact_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "pages/contact.html", {"user": user})


@router.get("/privacy")
def privacy_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "pages/privacy.html", {"user": user})


@router.get("/terms")
def terms_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "pages/terms.html", {"user": user})


@router.get("/robots.txt", include_in_schema=False)
def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Allow: /courses/\n"
        "Disallow: /admin\n"
        "Disallow: /dashboard\n"
        "Disallow: /learn\n"
        "Disallow: /api/\n"
        "Disallow: /login\n"
        "Disallow: /signup\n\n"
        f"Sitemap: {settings.SITE_URL}/sitemap.xml\n"
    )
    return Response(content=content, media_type="text/plain")


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml(db: Session = Depends(get_db)):
    courses = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.is_published.is_(True))
        .all()
    )
    urls = [
        f"  <url><loc>{settings.SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/courses</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/about</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/faq</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/contact</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>",
    ]
    for c in courses:
        urls.append(
            f"  <url><loc>{settings.SITE_URL}/courses/{c.slug}</loc><changefreq>weekly</changefreq><priority>0.85</priority></url>"
        )
        for mod in c.modules:
            for lesson in mod.lessons:
                if lesson.slug:
                    urls.append(
                        f"  <url><loc>{settings.SITE_URL}/courses/{c.slug}/{lesson.slug}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>"
                    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>"
    )
    return Response(content=xml, media_type="application/xml")
