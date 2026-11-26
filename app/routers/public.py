"""Public pages and SEO endpoints (robots.txt, sitemap.xml)."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session, selectinload

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_optional_user
from app.models.course import Course, Module
from app.models.progress import Enrollment
from app.models.user import User
from app.templating import templates

router = APIRouter(tags=["Public"])
settings = get_settings()


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
    return templates.TemplateResponse(
        request,
        "index.html",
        {"user": user, "courses": courses},
    )


@router.get("/courses")
def catalog(
    request: Request,
    category: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    query = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.is_published.is_(True))
    )
    if category and category != "All":
        query = query.filter(Course.category == category)
    if level and level != "All":
        query = query.filter(Course.level == level)

    courses = query.order_by(Course.created_at.asc()).all()
    categories = [
        row[0]
        for row in db.query(Course.category)
        .filter(Course.is_published.is_(True))
        .distinct()
        .all()
    ]
    return templates.TemplateResponse(
        request,
        "courses/catalog.html",
        {
            "user": user,
            "courses": courses,
            "categories": categories,
            "selected_category": category or "All",
            "selected_level": level or "All",
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
        raise HTTPException(status_code=404, detail="Course not found")

    is_enrolled = False
    if user:
        is_enrolled = (
            db.query(Enrollment)
            .filter(Enrollment.user_id == user.id, Enrollment.course_id == course.id)
            .first()
            is not None
        )

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
            "is_enrolled": is_enrolled,
            "first_lesson": first_lesson,
        },
    )


@router.get("/about")
def about_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    return templates.TemplateResponse(request, "about.html", {"user": user})


@router.get("/robots.txt", include_in_schema=False)
def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
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
    courses = db.query(Course).filter(Course.is_published.is_(True)).all()
    urls = [
        f"  <url><loc>{settings.SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/courses</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>",
        f"  <url><loc>{settings.SITE_URL}/about</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>",
    ]
    for c in courses:
        urls.append(
            f"  <url><loc>{settings.SITE_URL}/courses/{c.slug}</loc><changefreq>weekly</changefreq><priority>0.85</priority></url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>"
    )
    return Response(content=xml, media_type="application/xml")
