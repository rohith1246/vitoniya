"""Initial database seeding for Admin user and practical, SEO-ready courses."""

import re

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.course import Course, Lesson, Module
from app.models.user import User
from app.security import hash_password

settings = get_settings()


def slugify_text(text: str) -> str:
    """Convert any title into a clean URL-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "lesson"


def _add_course_with_modules(db: Session, data: dict) -> None:
    if db.query(Course).filter(Course.slug == data["slug"]).first():
        return

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
        mod = Module(course_id=course.id, title=mod_data["title"], order_index=m_idx)
        db.add(mod)
        db.flush()

        for l_idx, lesson_data in enumerate(mod_data["lessons"], start=1):
            db.add(
                Lesson(
                    module_id=mod.id,
                    title=lesson_data["title"],
                    slug=slugify_text(lesson_data["title"]),
                    duration_mins=lesson_data["duration_mins"],
                    order_index=l_idx,
                    content_md=lesson_data["content_md"],
                )
            )


def _backfill_lesson_slugs(db: Session) -> None:
    """Ensure every existing lesson has a unique slug inside its course."""
    lessons_without_slug = db.query(Lesson).filter(Lesson.slug.is_(None)).all()
    if not lessons_without_slug:
        return
    for lesson in lessons_without_slug:
        base = slugify_text(lesson.title)
        lesson.slug = f"{base}-{lesson.id}" if db.query(Lesson).filter(Lesson.slug == base).first() else base
    db.commit()


def seed_initial_data(db: Session) -> None:
    """Create initial admin account, backfill slugs, and seed practical courses by slug."""
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

    courses_to_seed = [
        {
            "title": "Java & Data Structures Foundations",
            "slug": "java-dsa-foundations",
            "subtitle": "Master arrays, hashing, recursion, and problem-solving patterns in Java.",
            "description": (
                "A structured track designed for engineering students and backend developers. "
                "Learn how to reason about time complexity, write clean Java code, and solve "
                "core LeetCode interview patterns step by step."
            ),
            "category": "DSA & Java",
            "level": "Beginner",
            "modules": [
                {
                    "title": "Module 1: Java & Complexity Basics",
                    "lessons": [
                        {
                            "title": "Time & Space Complexity (Big-O Intuition)",
                            "duration_mins": 18,
                            "content_md": (
                                "Understanding Big-O is about predicting how your code scales when input size `n` grows.\n\n"
                                "Core complexity classes you must know:\n"
                                "- **O(1):** Constant lookup (array index access, HashMap `get`/`put`).\n"
                                "- **O(log n):** Halving the search space each step (Binary Search).\n"
                                "- **O(n):** Single pass over an array or string.\n"
                                "- **O(n log n):** Efficient sorting (`Arrays.sort` on objects, Merge Sort).\n"
                                "- **O(n^2):** Nested loops over the same array — optimize whenever `n > 10^4`.\n\n"
                                "Actionable Practice Task:\n"
                                "1. Write a Java loop that prints pairs `(i, j)` and count operations for `n = 100`.\n"
                                "2. Replace nested lookup with a `HashSet` and verify why it drops from O(n^2) to O(n)."
                            ),
                        },
                        {
                            "title": "Arrays, Loops & In-Place Swaps",
                            "duration_mins": 22,
                            "content_md": (
                                "Arrays store elements in contiguous memory, giving O(1) random access by index.\n\n"
                                "Core Java pattern — reversing an array in-place with O(1) extra space:\n"
                                "```java\n"
                                "int left = 0, right = arr.length - 1;\n"
                                "while (left < right) {\n"
                                "    int temp = arr[left];\n"
                                "    arr[left++] = arr[right];\n"
                                "    arr[right--] = temp;\n"
                                "}\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Implement `rotateRight(int[] nums, int k)` using 3 in-place reversals.\n"
                                "- Solve LeetCode #26 (Remove Duplicates from Sorted Array) using two pointers."
                            ),
                        },
                    ],
                },
                {
                    "title": "Module 2: Arrays, Hashing & Two Pointers",
                    "lessons": [
                        {
                            "title": "HashMap Frequency Counting & Two Sum",
                            "duration_mins": 25,
                            "content_md": (
                                "A `HashMap` turns O(n^2) pair searches into O(n) single-pass solutions.\n\n"
                                "```java\n"
                                "Map<Integer, Integer> seen = new HashMap<>();\n"
                                "for (int i = 0; i < nums.length; i++) {\n"
                                "    int complement = target - nums[i];\n"
                                "    if (seen.containsKey(complement)) {\n"
                                "        return new int[]{seen.get(complement), i};\n"
                                "    }\n"
                                "    seen.put(nums[i], i);\n"
                                "}\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Trace this code on `[2, 7, 11, 15]` with `target = 9` on paper.\n"
                                "- Solve LeetCode #1 (Two Sum) and #242 (Valid Anagram) using `HashMap`."
                            ),
                        },
                        {
                            "title": "Sliding Window for Subarray Problems",
                            "duration_mins": 24,
                            "content_md": (
                                "Use Sliding Window whenever a problem asks for **contiguous** subarrays or substrings.\n\n"
                                "Steps:\n"
                                "1. Expand the `right` pointer to include new elements into the window.\n"
                                "2. Shrink the `left` pointer while the window condition is violated.\n"
                                "3. Record the best window length or sum at each valid step.\n\n"
                                "Actionable Practice Task:\n"
                                "- Solve LeetCode #3 (Longest Substring Without Repeating Characters) using a `HashSet` window."
                            ),
                        },
                    ],
                },
            ],
        },
        {
            "title": "FastAPI & PostgreSQL Backend Engineering",
            "slug": "fastapi-postgresql-backend",
            "subtitle": "Build production APIs with SQLAlchemy, JWT auth, and Role-Based Access Control.",
            "description": (
                "Go beyond toy tutorials. Learn how to structure a FastAPI service, model relational "
                "schemas in PostgreSQL, secure routes with HttpOnly JWT cookies, and deploy cleanly."
            ),
            "category": "Backend & AI",
            "level": "Intermediate",
            "modules": [
                {
                    "title": "Module 1: FastAPI Architecture & Database",
                    "lessons": [
                        {
                            "title": "Project Layout, Routers & Dependency Injection",
                            "duration_mins": 20,
                            "content_md": (
                                "Clean FastAPI applications separate configuration, database sessions, ORM models, and route modules.\n\n"
                                "Using `Depends(get_db)` ensures every request receives a scoped PostgreSQL session that closes safely when the response finishes.\n\n"
                                "Actionable Practice Task:\n"
                                "- Create a `/api/health` router and inject a database session with `Depends(get_db)`."
                            ),
                        },
                        {
                            "title": "Relational Modeling with SQLAlchemy 2.0 & PostgreSQL",
                            "duration_mins": 26,
                            "content_md": (
                                "Define normalized tables with foreign keys and unique constraints so invalid states "
                                "(like duplicate course enrollments) are rejected at the database level.\n\n"
                                "```python\n"
                                "class Enrollment(Base):\n"
                                "    __tablename__ = 'enrollments'\n"
                                "    __table_args__ = (UniqueConstraint('user_id', 'course_id'),)\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Sketch a 3-table schema (`users`, `courses`, `enrollments`) with primary and foreign keys."
                            ),
                        },
                    ],
                },
                {
                    "title": "Module 2: Authentication & RBAC",
                    "lessons": [
                        {
                            "title": "Implementing HttpOnly JWT Cookies & Role Guards",
                            "duration_mins": 28,
                            "content_md": (
                                "Storing signed JWTs inside `HttpOnly` cookies protects browser sessions from JavaScript XSS access.\n\n"
                                "With a reusable `require_roles('admin')` dependency, unauthorized users receive HTTP 403 before route logic executes.\n\n"
                                "Actionable Practice Task:\n"
                                "- Protect an `/admin` endpoint with `require_roles('admin')` and verify a `student` token receives 403."
                            ),
                        },
                    ],
                },
            ],
        },
        {
            "title": "B.Tech CSE Exam & Lab Survival Guide (OS, DBMS, Java)",
            "slug": "btech-jntuh-exam-lab-guide",
            "subtitle": "Unit-wise solved core concepts, lab programs, and viva answers for engineering students.",
            "description": (
                "Written specifically for B.Tech Computer Science students preparing for university semester exams, "
                "practical lab vivas, and technical interviews. Covers high-weightage Operating Systems, DBMS, and Java OOP topics."
            ),
            "category": "B.Tech & Exams",
            "level": "Beginner",
            "modules": [
                {
                    "title": "Module 1: Operating Systems High-Weightage Topics",
                    "lessons": [
                        {
                            "title": "CPU Scheduling Algorithms Compared (FCFS, SJF, Round Robin)",
                            "duration_mins": 25,
                            "content_md": (
                                "CPU scheduling decides which process in the ready queue gets CPU time next. This is one of the most repeated 10-mark questions in B.Tech Operating Systems exams.\n\n"
                                "Key algorithms to compare:\n"
                                "- **FCFS (First-Come, First-Served):** Non-preemptive; simple queue, but suffers from the Convoy Effect when a long process arrives first.\n"
                                "- **SJF (Shortest Job First):** Gives minimum average waiting time, but can starve long processes.\n"
                                "- **Round Robin (RR):** Preemptive with a fixed Time Quantum `q`; ideal for time-sharing systems.\n\n"
                                "Exam Formula Checklist:\n"
                                "- **Turnaround Time (TAT)** = Completion Time - Arrival Time\n"
                                "- **Waiting Time (WT)** = Turnaround Time - Burst Time\n\n"
                                "Actionable Practice Task:\n"
                                "1. Draw a Gantt chart for 4 processes with burst times `[5, 3, 8, 6]` using Round Robin (`q = 2`).\n"
                                "2. Compute Average Waiting Time and verify each step."
                            ),
                        },
                        {
                            "title": "Deadlocks: 4 Coffman Conditions & Banker's Algorithm",
                            "duration_mins": 22,
                            "content_md": (
                                "A deadlock happens when processes hold resources and wait forever for resources held by other processes.\n\n"
                                "All **4 Coffman Conditions** must hold simultaneously for a deadlock:\n"
                                "1. **Mutual Exclusion:** Only one process can use a resource at a time.\n"
                                "2. **Hold and Wait:** A process holds at least one resource while waiting for more.\n"
                                "3. **No Preemption:** Resources cannot be forcibly taken away.\n"
                                "4. **Circular Wait:** A closed chain of processes waits on each other.\n\n"
                                "How to answer in exams & vivas:\n"
                                "- **Deadlock Prevention** breaks at least one of the 4 conditions.\n"
                                "- **Banker's Algorithm** checks `Need = Max - Allocation` to guarantee a **Safe Sequence** before granting resources.\n\n"
                                "Actionable Practice Task:\n"
                                "- Practice one 5-process Banker's Algorithm safety matrix by computing the `Need` matrix first."
                            ),
                        },
                        {
                            "title": "Paging, Virtual Memory & Page Replacement (LRU vs FIFO)",
                            "duration_mins": 24,
                            "content_md": (
                                "Paging divides physical memory into fixed-size **Frames** and logical memory into equal-sized **Pages**, eliminating external fragmentation.\n\n"
                                "Page Replacement Rules when a Page Fault occurs:\n"
                                "- **FIFO:** Evicts the oldest loaded page. Simple, but suffers from **Belady's Anomaly** (more frames can cause more faults).\n"
                                "- **LRU (Least Recently Used):** Evicts the page unused for the longest time. Close to Optimal and avoids Belady's Anomaly.\n\n"
                                "Actionable Practice Task:\n"
                                "- Count total Page Faults for reference string `7, 0, 1, 2, 0, 3, 0, 4` with 3 frames using FIFO and LRU."
                            ),
                        },
                    ],
                },
                {
                    "title": "Module 2: DBMS Normalization & Transactions",
                    "lessons": [
                        {
                            "title": "Database Normalization (1NF, 2NF, 3NF, BCNF with Examples)",
                            "duration_mins": 26,
                            "content_md": (
                                "Normalization removes redundant data and insertion/update/deletion anomalies.\n\n"
                                "Quick Cheat Sheet:\n"
                                "- **1NF:** Atomic (single) values in every cell; no repeating groups.\n"
                                "- **2NF:** In 1NF + **No Partial Dependency** (non-key attributes must depend on the entire composite primary key).\n"
                                "- **3NF:** In 2NF + **No Transitive Dependency** (`A -> B` and `B -> C` where `B` is non-prime).\n"
                                "- **BCNF:** Stronger 3NF — for every functional dependency `X -> Y`, `X` must be a **Super Key**.\n\n"
                                "Actionable Practice Task:\n"
                                "- Take a denormalized table `Order(OrderID, StudentName, CourseID, CourseFee)` and split it cleanly into 3NF tables."
                            ),
                        },
                        {
                            "title": "ACID Properties & Transaction States in DBMS",
                            "duration_mins": 18,
                            "content_md": (
                                "A transaction is a logical unit of database work (such as transferring money between two bank accounts).\n\n"
                                "- **Atomicity:** All operations succeed or none are applied (managed by Recovery Manager).\n"
                                "- **Consistency:** Database moves from one valid constraint-satisfying state to another.\n"
                                "- **Isolation:** Concurrent transactions do not corrupt each other's intermediate state (Concurrency Control).\n"
                                "- **Durability:** Once committed, changes survive power or disk crashes.\n\n"
                                "Actionable Practice Task:\n"
                                "- Explain in 3 lines why `UPDATE accounts` debit + credit must wrap inside `BEGIN; ... COMMIT;`."
                            ),
                        },
                    ],
                },
                {
                    "title": "Module 3: Java OOP Exam & Viva Essentials",
                    "lessons": [
                        {
                            "title": "Abstract Class vs Interface & Exception Handling in Java",
                            "duration_mins": 20,
                            "content_md": (
                                "One of the most common Java lab viva and interview questions:\n\n"
                                "- **Abstract Class:** Can have state (fields), constructors, and both abstract + concrete methods. A class can `extends` only one abstract class.\n"
                                "- **Interface:** Defines a capability contract (`implements`). Supports multiple inheritance of type.\n\n"
                                "```java\n"
                                "interface Payable {\n"
                                "    void processPayment(double amount);\n"
                                "}\n"
                                "class UpiPayment implements Payable {\n"
                                "    public void processPayment(double amount) {\n"
                                "        System.out.println(\"Paid via UPI: \" + amount);\n"
                                "    }\n"
                                "}\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Write a `try-catch-finally` Java program demonstrating `ArithmeticException` handling."
                            ),
                        },
                    ],
                },
            ],
        },
        {
            "title": "SQL & DBMS Queries for Campus Placements",
            "slug": "sql-dbms-placement-queries",
            "subtitle": "Write real PostgreSQL queries tested in coding rounds and backend interviews.",
            "description": (
                "Stop memorizing SQL definitions. Practice the exact SELECT, JOIN, GROUP BY, subquery, "
                "and window-function queries companies ask freshers in first-round screening."
            ),
            "category": "SQL & Databases",
            "level": "Beginner",
            "modules": [
                {
                    "title": "Module 1: Joins, Grouping & Subqueries",
                    "lessons": [
                        {
                            "title": "INNER JOIN vs LEFT JOIN & Finding Unmatched Rows",
                            "duration_mins": 20,
                            "content_md": (
                                "Understanding joins solves 60% of placement SQL problems.\n\n"
                                "- **INNER JOIN:** Returns only rows where keys match in both tables.\n"
                                "- **LEFT JOIN:** Keeps every row from the left table and fills `NULL` when no match exists on the right.\n\n"
                                "Classic placement pattern — find students who have **never** enrolled in any course:\n"
                                "```sql\n"
                                "SELECT u.id, u.full_name, u.email\n"
                                "FROM users u\n"
                                "LEFT JOIN enrollments e ON u.id = e.user_id\n"
                                "WHERE e.id IS NULL;\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Write a `LEFT JOIN` query listing every course along with `COUNT(e.id)` so courses with 0 enrollments still show `0`."
                            ),
                        },
                        {
                            "title": "GROUP BY, HAVING & Finding the 2nd Highest Salary",
                            "duration_mins": 22,
                            "content_md": (
                                "Never confuse `WHERE` and `HAVING`:\n"
                                "- **`WHERE`** filters individual rows *before* grouping.\n"
                                "- **`HAVING`** filters aggregated groups *after* `GROUP BY`.\n\n"
                                "Classic Interview Question — 2nd Highest Distinct Salary:\n"
                                "```sql\n"
                                "SELECT MAX(salary) AS second_highest\n"
                                "FROM employees\n"
                                "WHERE salary < (SELECT MAX(salary) FROM employees);\n"
                                "```\n\n"
                                "Actionable Practice Task:\n"
                                "- Write a query returning departments (`dept_id`) that have more than 5 employees earning above 50,000."
                            ),
                        },
                    ],
                },
                {
                    "title": "Module 2: Window Functions & Indexing",
                    "lessons": [
                        {
                            "title": "Window Functions (ROW_NUMBER, RANK, DENSE_RANK) & B-Tree Indexes",
                            "duration_mins": 24,
                            "content_md": (
                                "Window functions compute rankings across rows **without collapsing** them like `GROUP BY` does.\n\n"
                                "```sql\n"
                                "SELECT name, department, salary,\n"
                                "       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank\n"
                                "FROM employees;\n"
                                "```\n\n"
                                "Key difference:\n"
                                "- `ROW_NUMBER()`: `1, 2, 3, 4` (always unique)\n"
                                "- `RANK()`: `1, 2, 2, 4` (skips after ties)\n"
                                "- `DENSE_RANK()`: `1, 2, 2, 3` (no gaps — best for Nth highest salary per department)\n\n"
                                "Actionable Practice Task:\n"
                                "- Wrap the query above in a CTE (`WITH ranked AS (...)`) and select only `WHERE dept_rank <= 3`."
                            ),
                        },
                    ],
                },
            ],
        },
    ]

    for c_data in courses_to_seed:
        _add_course_with_modules(db, c_data)

    db.commit()
