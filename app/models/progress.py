"""Student enrollment and lesson completion tracking models."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Enrollment(Base):
    """Links a user to an enrolled course."""

    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_enrollment"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class LessonProgress(Base):
    """Tracks whether a user has completed a specific lesson."""

    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_records")
