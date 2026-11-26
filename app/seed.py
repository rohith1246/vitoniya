"""Initial database seeding for Admin user and starter courses."""

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.course import Course, Lesson, Module
from app.models.user import User
from app.security import hash_password

settings = get_settings()


def seed_initial_data(db: Session) -> None:
    """Create initial admin account and starter courses if database is empty."""
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

    if db.query(Course).count() > 0:
        return

    # Course 1: Java & DSA
    dsa_course = Course(
        title="Java & Data Structures Foundations",
        slug="java-dsa-foundations",
        subtitle="Master arrays, hashing, recursion, and problem-solving patterns in Java.",
        description=(
            "A structured track designed for engineering students and backend developers. "
            "Learn how to reason about time complexity, write clean Java code, and solve "
            "core LeetCode interview patterns step by step."
        ),
        category="DSA & Java",
        level="Beginner",
        is_published=True,
    )
    db.add(dsa_course)
    db.flush()

    m1 = Module(course_id=dsa_course.id, title="Module 1: Java & Complexity Basics", order_index=1)
    m2 = Module(course_id=dsa_course.id, title="Module 2: Arrays, Hashing & Two Pointers", order_index=2)
    db.add_all([m1, m2])
    db.flush()

    db.add_all([
        Lesson(
            module_id=m1.id,
            title="Time & Space Complexity (Big-O Intuition)",
            duration_mins=18,
            order_index=1,
            content_md=(
                "Understanding Big-O is about predicting how your code scales when input size n grows.\n\n"
                "Key takeaways:\n"
                "- O(1): Constant lookup (array index, HashMap get).\n"
                "- O(log n): Halving search space each step (Binary Search).\n"
                "- O(n): Single pass over an array or list.\n"
                "- O(n^2): Nested loops over the same collection — optimize when n > 10^4.\n\n"
                "Practice tip: Always check constraints (e.g., n <= 10^5) before choosing an algorithm."
            ),
        ),
        Lesson(
            module_id=m1.id,
            title="Arrays, Loops & In-Place Swaps",
            duration_mins=22,
            order_index=2,
            content_md=(
                "Arrays store elements in contiguous memory, giving O(1) random access.\n\n"
                "Core Java pattern — reversing an array in-place with O(1) extra space:\n"
                "```java\n"
                "int left = 0, right = arr.length - 1;\n"
                "while (left < right) {\n"
                "    int temp = arr[left];\n"
                "    arr[left++] = arr[right];\n"
                "    arr[right--] = temp;\n"
                "}\n"
                "```"
            ),
        ),
        Lesson(
            module_id=m2.id,
            title="HashMap Frequency Counting & Two Sum",
            duration_mins=25,
            order_index=1,
            content_md=(
                "A HashMap turns O(n^2) pair searches into O(n) single-pass solutions.\n\n"
                "Two Sum Pattern:\n"
                "1. Iterate through nums[i].\n"
                "2. Compute complement = target - nums[i].\n"
                "3. Check if complement exists in map; otherwise store map.put(nums[i], i)."
            ),
        ),
        Lesson(
            module_id=m2.id,
            title="Sliding Window for Subarray Problems",
            duration_mins=24,
            order_index=2,
            content_md=(
                "Use Sliding Window when asked for contiguous subarrays or substrings.\n\n"
                "Steps:\n"
                "- Expand `right` pointer to include new elements.\n"
                "- Shrink `left` pointer while the window constraint is violated.\n"
                "- Update the best answer at each valid window."
            ),
        ),
    ])

    # Course 2: FastAPI & PostgreSQL
    fastapi_course = Course(
        title="FastAPI & PostgreSQL Backend Engineering",
        slug="fastapi-postgresql-backend",
        subtitle="Build production APIs with SQLAlchemy, JWT auth, and Role-Based Access Control.",
        description=(
            "Go beyond toy tutorials. Learn how to structure a FastAPI service, model relational "
            "schemas in PostgreSQL, secure routes with HttpOnly JWT cookies, and deploy cleanly."
        ),
        category="Backend & AI",
        level="Intermediate",
        is_published=True,
    )
    db.add(fastapi_course)
    db.flush()

    fm1 = Module(course_id=fastapi_course.id, title="Module 1: FastAPI Architecture & Database", order_index=1)
    fm2 = Module(course_id=fastapi_course.id, title="Module 2: Authentication & RBAC", order_index=2)
    db.add_all([fm1, fm2])
    db.flush()

    db.add_all([
        Lesson(
            module_id=fm1.id,
            title="Project Layout, Routers & Dependency Injection",
            duration_mins=20,
            order_index=1,
            content_md=(
                "Clean FastAPI apps separate configuration, database sessions, ORM models, and routers.\n\n"
                "Using `Depends(get_db)` ensures every request gets a clean database session that closes "
                "automatically after the response is sent."
            ),
        ),
        Lesson(
            module_id=fm1.id,
            title="Relational Modeling with SQLAlchemy 2.0 & PostgreSQL",
            duration_mins=26,
            order_index=2,
            content_md=(
                "Define normalized tables with foreign keys and unique constraints so invalid states "
                "(like duplicate enrollments) are impossible at the database level."
            ),
        ),
        Lesson(
            module_id=fm2.id,
            title="Implementing HttpOnly JWT Cookies & Role Guards",
            duration_mins=28,
            order_index=1,
            content_md=(
                "Storing JWTs in `HttpOnly` cookies protects browser sessions from XSS.\n\n"
                "With `require_roles('admin')`, protected endpoints reject unauthorized users cleanly "
                "with HTTP 403 before any business logic runs."
            ),
        ),
    ])

    db.commit()
