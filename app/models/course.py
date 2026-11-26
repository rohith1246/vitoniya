"""Course, Module, and Lesson ORM models."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Course(Base):
    """Top-level learning track or course."""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, default="Engineering")
    level: Mapped[str] = mapped_column(String(40), nullable=False, default="Beginner")
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    modules = relationship(
        "Module",
        back_populates="course",
        order_by="Module.order_index",
        cascade="all, delete-orphan",
    )
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    @property
    def total_lessons(self) -> int:
        return sum(len(m.lessons) for m in self.modules)


class Module(Base):
    """Section/chapter grouping lessons inside a course."""

    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    course = relationship("Course", back_populates="modules")
    lessons = relationship(
        "Lesson",
        back_populates="module",
        order_by="Lesson.order_index",
        cascade="all, delete-orphan",
    )


class Lesson(Base):
    """Individual video/reading lesson inside a module."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[Optional[str]] = mapped_column(String(220), nullable=True, index=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content_md: Mapped[str] = mapped_column(Text, nullable=False, default="")
    duration_mins: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    module = relationship("Module", back_populates="lessons")
    progress_records = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")
