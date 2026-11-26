"""Student learning workspace: dashboard, enrollment, lesson player, progress."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.dependencies import require_roles
from app.models.course import Course, Lesson, Module
from app.models.progress import Enrollment, LessonProgress
from app.models.user import User
from app.templating import templates

router = APIRouter(tags=["Learning"])


@router.get("/dashboard")
def student_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student", "admin")),
):
    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )

    completed_ids = {
        row[0]
        for row in db.query(LessonProgress.lesson_id)
        .filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.is_completed.is_(True),
        )
        .all()
    }

    enrolled_cards = []
    for enr in enrollments:
        course = (
            db.query(Course)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
            .filter(Course.id == enr.course_id)
            .first()
        )
        if not course:
            continue

        all_lessons = [lesson for mod in course.modules for lesson in mod.lessons]
        total = len(all_lessons)
        done = sum(1 for l in all_lessons if l.id in completed_ids)
        pct = int((done / total) * 100) if total > 0 else 0

        next_lesson = next((l for l in all_lessons if l.id not in completed_ids), None)
        if not next_lesson and all_lessons:
            next_lesson = all_lessons[0]

        enrolled_cards.append(
            {
                "course": course,
                "total_lessons": total,
                "completed_lessons": done,
                "progress_pct": pct,
                "next_lesson": next_lesson,
            }
        )

    return templates.TemplateResponse(
        request,
        "learn/dashboard.html",
        {
            "user": current_user,
            "enrolled_cards": enrolled_cards,
        },
    )


@router.post("/courses/{slug}/enroll")
def enroll_course(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student", "admin")),
):
    course = db.query(Course).filter(Course.slug == slug, Course.is_published.is_(True)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id, Enrollment.course_id == course.id)
        .first()
    )
    if not existing:
        db.add(Enrollment(user_id=current_user.id, course_id=course.id))
        db.commit()

    first_lesson = (
        db.query(Lesson)
        .join(Module, Lesson.module_id == Module.id)
        .filter(Module.course_id == course.id)
        .order_by(Module.order_index.asc(), Lesson.order_index.asc())
        .first()
    )
    if first_lesson:
        return RedirectResponse(
            url=f"/learn/{course.slug}/{first_lesson.id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/learn/{slug}/{lesson_id}")
def lesson_player(
    slug: str,
    lesson_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student", "admin")),
):
    course = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.slug == slug)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrolled = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id, Enrollment.course_id == course.id)
        .first()
    )
    if not enrolled and current_user.role != "admin":
        return RedirectResponse(url=f"/courses/{slug}", status_code=status.HTTP_303_SEE_OTHER)

    ordered_lessons = [lesson for mod in course.modules for lesson in mod.lessons]
    current_idx = next((i for i, l in enumerate(ordered_lessons) if l.id == lesson_id), None)
    if current_idx is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    current_lesson = ordered_lessons[current_idx]
    prev_lesson = ordered_lessons[current_idx - 1] if current_idx > 0 else None
    next_lesson = ordered_lessons[current_idx + 1] if current_idx + 1 < len(ordered_lessons) else None

    completed_ids = {
        row[0]
        for row in db.query(LessonProgress.lesson_id)
        .filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.is_completed.is_(True),
        )
        .all()
    }

    total_lessons = len(ordered_lessons)
    completed_count = sum(1 for l in ordered_lessons if l.id in completed_ids)
    progress_pct = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0

    return templates.TemplateResponse(
        request,
        "learn/lesson.html",
        {
            "user": current_user,
            "course": course,
            "lesson": current_lesson,
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "completed_ids": completed_ids,
            "is_completed": current_lesson.id in completed_ids,
            "progress_pct": progress_pct,
        },
    )


@router.post("/learn/{slug}/{lesson_id}/toggle")
def toggle_lesson_complete(
    slug: str,
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student", "admin")),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id == lesson_id,
        )
        .first()
    )
    if progress:
        progress.is_completed = not progress.is_completed
        progress.completed_at = datetime.now(timezone.utc) if progress.is_completed else None
    else:
        db.add(
            LessonProgress(
                user_id=current_user.id,
                lesson_id=lesson_id,
                is_completed=True,
                completed_at=datetime.now(timezone.utc),
            )
        )
    db.commit()

    return RedirectResponse(
        url=f"/learn/{slug}/{lesson_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
