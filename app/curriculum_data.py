"""Structured long-form curriculum data for VitoniyaEdu."""

CURRICULUM_DATA = [
    {
        "title": "Java & Data Structures Foundations",
        "slug": "java-dsa-foundations",
        "subtitle": "Master complexity analysis, arrays, hashing, binary search, and interview patterns in Java.",
        "description": (
            "A practical, step-by-step track for engineering students and backend developers. "
            "Learn how to reason about time and space complexity, write clean Java code, and solve "
            "core LeetCode placement patterns methodically."
        ),
        "category": "DSA & Java",
        "level": "Beginner",
        "modules": [
            {
                "title": "Module 1: Java & Complexity Basics",
                "lessons": [
                    {
                        "title": "Time & Space Complexity (Big-O Intuition)",
                        "duration_mins": 20,
                        "content_md": (
                            "## Why Big-O Matters in Real Interviews\n\n"
                            "Two solutions can produce the exact same output on a 10-element test case while behaving completely differently in production or online assessments. "
                            "Big-O notation measures how the number of operations (time) and extra memory (space) grow as the input size `n` increases.\n\n"
                            "### Core Complexity Classes\n\n"
                            "- **O(1) — Constant Time:** Accessing `arr[i]`, pushing onto a stack, or looking up a key in a `HashMap`.\n"
                            "- **O(log n) — Logarithmic Time:** Cutting the remaining search space in half each step, such as Binary Search on a sorted array.\n"
                            "- **O(n) — Linear Time:** A single pass over an array, linked list, or string.\n"
                            "- **O(n log n) — Linearithmic Time:** Efficient divide-and-conquer sorting like Merge Sort or `Arrays.sort()`.\n"
                            "- **O(n^2) — Quadratic Time:** Nested loops comparing all pairs `(i, j)`. Usually causes Time Limit Exceeded (TLE) when `n > 10^4`.\n\n"
                            "### Constraint Cheat Sheet for Coding Tests\n\n"
                            "Before writing code, inspect the input constraint `n`:\n"
                            "1. If `n <= 10^3`, an **O(n^2)** solution passes safely.\n"
                            "2. If `n <= 10^5`, you need **O(n log n)** or **O(n)**.\n"
                            "3. If `n >= 10^9`, you likely need **O(log n)** or **O(1)** math.\n\n"
                            "### Example: Optimizing O(n^2) to O(n)\n\n"
                            "```java\n"
                            "// O(n) duplicate check using extra O(n) space\n"
                            "Set<Integer> seen = new HashSet<>();\n"
                            "for (int num : nums) {\n"
                            "    if (!seen.add(num)) {\n"
                            "        return true;\n"
                            "    }\n"
                            "}\n"
                            "return false;\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a Java program that benchmarks a nested loop vs. a single-pass `HashSet` lookup on 50,000 integers.\n"
                            "- Solve **LeetCode #217 (Contains Duplicate)** and analyze both its time and auxiliary space complexity."
                        ),
                    },
                    {
                        "title": "Arrays, Loops & In-Place Swaps",
                        "duration_mins": 22,
                        "content_md": (
                            "## How Arrays Work in Memory\n\n"
                            "An array stores elements in contiguous memory locations. Because every element has the same byte width, Java calculates the memory address of `arr[i]` in **O(1)** time. "
                            "However, inserting or deleting in the middle requires shifting elements, which costs **O(n)**.\n\n"
                            "### The Two-Pointer In-Place Pattern\n\n"
                            "Whenever a problem asks you to reverse, partition, or deduplicate an array with **O(1) extra space**, use two indices moving toward each other or tracking the write boundary.\n\n"
                            "```java\n"
                            "public static void reverse(int[] arr, int left, int right) {\n"
                            "    while (left < right) {\n"
                            "        int temp = arr[left];\n"
                            "        arr[left] = arr[right];\n"
                            "        arr[right] = temp;\n"
                            "        left++;\n"
                            "        right--;\n"
                            "    }\n"
                            "}\n"
                            "```\n\n"
                            "### Common Edge Cases to Check\n\n"
                            "- Empty array (`arr.length == 0`) or single element (`arr.length == 1`).\n"
                            "- Off-by-one boundary errors (`right = arr.length - 1`, never `arr.length`).\n"
                            "- Integer overflow when summing large array elements (use `long` for running sums).\n\n"
                            "### Actionable Practice Task\n\n"
                            "1. Implement `rotateRight(int[] nums, int k)` using three calls to `reverse()` (remember `k = k % nums.length`).\n"
                            "2. Solve **LeetCode #26 (Remove Duplicates from Sorted Array)** and **LeetCode #283 (Move Zeroes)** without allocating a second array."
                        ),
                    },
                    {
                        "title": "Binary Search & Search Space Reduction",
                        "duration_mins": 25,
                        "content_md": (
                            "## Beyond Searching a Sorted Array\n\n"
                            "Binary Search finds an element in a sorted collection of 1,000,000 items in at most **20 comparisons** (`log2(10^6) ≈ 20`). "
                            "More importantly, the same template solves optimization problems like finding minimum shipping capacity or peak elements.\n\n"
                            "### Bug-Free Binary Search Template\n\n"
                            "Always compute `mid` safely to avoid 32-bit signed integer overflow:\n\n"
                            "```java\n"
                            "public int binarySearch(int[] nums, int target) {\n"
                            "    int low = 0, high = nums.length - 1;\n"
                            "    while (low <= high) {\n"
                            "        int mid = low + (high - low) / 2;\n"
                            "        if (nums[mid] == target) return mid;\n"
                            "        if (nums[mid] < target) low = mid + 1;\n"
                            "        else high = mid - 1;\n"
                            "    }\n"
                            "    return -1;\n"
                            "}\n"
                            "```\n\n"
                            "### Finding First or Last Occurrence (Lower/Upper Bound)\n\n"
                            "When duplicates exist, do not stop immediately at `nums[mid] == target`. Record `ans = mid` and continue shrinking either `high = mid - 1` (for first index) or `low = mid + 1` (for last index).\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Trace `low`, `mid`, and `high` by hand on `[1, 3, 5, 7, 9, 11]` searching for `7` and `6`.\n"
                            "- Solve **LeetCode #704 (Binary Search)** and **LeetCode #34 (Find First and Last Position)**."
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
                            "## Trading Memory for Speed with HashMap\n\n"
                            "A `HashMap<K, V>` maps keys to values with average **O(1)** `put`, `get`, and `containsKey` operations. "
                            "In interviews, whenever you find yourself checking if a previously seen value satisfies a condition, reach for a `HashMap`.\n\n"
                            "### Pattern 1: Complement Lookup (Two Sum)\n\n"
                            "```java\n"
                            "public int[] twoSum(int[] nums, int target) {\n"
                            "    Map<Integer, Integer> seen = new HashMap<>();\n"
                            "    for (int i = 0; i < nums.length; i++) {\n"
                            "        int complement = target - nums[i];\n"
                            "        if (seen.containsKey(complement)) {\n"
                            "            return new int[]{seen.get(complement), i};\n"
                            "        }\n"
                            "        seen.put(nums[i], i);\n"
                            "    }\n"
                            "    return new int[]{};\n"
                            "}\n"
                            "```\n\n"
                            "### Pattern 2: Frequency Counting\n\n"
                            "Use `map.getOrDefault(key, 0) + 1` to count character or element occurrences without writing verbose `if/else` null checks.\n\n"
                            "### Actionable Practice Task\n\n"
                            "1. Dry-run `twoSum` on `nums = [3, 2, 4]`, `target = 6` and verify why inserting *after* checking prevents using the same index twice.\n"
                            "2. Solve **LeetCode #1 (Two Sum)**, **#242 (Valid Anagram)**, and **#169 (Majority Element)**."
                        ),
                    },
                    {
                        "title": "Sliding Window for Subarray Problems",
                        "duration_mins": 24,
                        "content_md": (
                            "## When to Use Sliding Window\n\n"
                            "Use Sliding Window when a problem asks for the longest, shortest, or count of **contiguous subarrays or substrings** that satisfy a constraint.\n\n"
                            "### Fixed vs. Variable Window\n\n"
                            "- **Fixed Window (`size k`):** Add the incoming element at `right` and subtract the outgoing element at `right - k`.\n"
                            "- **Variable Window:** Expand `right` each iteration, then run a `while` loop moving `left` forward whenever the window becomes invalid.\n\n"
                            "```java\n"
                            "int left = 0, maxLen = 0;\n"
                            "Set<Character> window = new HashSet<>();\n"
                            "for (int right = 0; right < s.length(); right++) {\n"
                            "    char ch = s.charAt(right);\n"
                            "    while (window.contains(ch)) {\n"
                            "        window.remove(s.charAt(left++));\n"
                            "    }\n"
                            "    window.add(ch);\n"
                            "    maxLen = Math.max(maxLen, right - left + 1);\n"
                            "}\n"
                            "```\n\n"
                            "### Why It Runs in O(n)\n\n"
                            "Even though there is a `while` loop inside a `for` loop, both `left` and `right` only move forward at most `n` times total. Each character is added once and removed at most once (**2n operations = O(n)**).\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Solve **LeetCode #3 (Longest Substring Without Repeating Characters)** and **LeetCode #121 (Best Time to Buy and Sell Stock)**."
                        ),
                    },
                    {
                        "title": "Recursion & Call Stack Foundations",
                        "duration_mins": 24,
                        "content_md": (
                            "## Thinking Recursively Without Confusion\n\n"
                            "Recursion solves a large problem by delegating smaller subproblems of the same shape to the function itself. "
                            "Every recursive method has two mandatory parts:\n\n"
                            "1. **Base Case:** The smallest input whose answer is known directly (prevents `StackOverflowError`).\n"
                            "2. **Recursive Step:** Moves closer to the base case on every call.\n\n"
                            "### Visualizing the Call Stack\n\n"
                            "Each recursive call allocates a new **stack frame** holding its local variables and return address. "
                            "Therefore, recursion of depth `d` uses **O(d) stack memory** even if you create zero arrays.\n\n"
                            "```java\n"
                            "// Generate all subsets (Backtracking template)\n"
                            "void backtrack(int idx, int[] nums, List<Integer> path, List<List<Integer>> res) {\n"
                            "    if (idx == nums.length) {\n"
                            "        res.add(new ArrayList<>(path));\n"
                            "        return;\n"
                            "    }\n"
                            "    path.add(nums[idx]);                  // Choose\n"
                            "    backtrack(idx + 1, nums, path, res);  // Explore\n"
                            "    path.remove(path.size() - 1);         // Undo (Backtrack)\n"
                            "    backtrack(idx + 1, nums, path, res);  // Skip\n"
                            "}\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Draw the recursion tree for `nums = [1, 2]` showing every `choose` and `skip` branch.\n"
                            "- Solve **LeetCode #78 (Subsets)** and **LeetCode #509 (Fibonacci Number)**."
                        ),
                    },
                ],
            },
        ],
    },
    {
        "title": "FastAPI & PostgreSQL Backend Engineering",
        "slug": "fastapi-postgresql-backend",
        "subtitle": "Build production APIs with SQLAlchemy, JWT auth, Pydantic validation, and Render deployment.",
        "description": (
            "Go beyond toy tutorials. Learn how to structure a maintainable FastAPI service, model relational "
            "schemas in PostgreSQL, enforce Role-Based Access Control with HttpOnly cookies, and deploy cleanly."
        ),
        "category": "Backend & AI",
        "level": "Intermediate",
        "modules": [
            {
                "title": "Module 1: FastAPI Architecture & Database",
                "lessons": [
                    {
                        "title": "Project Layout, Routers & Dependency Injection",
                        "duration_mins": 22,
                        "content_md": (
                            "## Why Modular Structure Matters\n\n"
                            "Putting all routes, SQL queries, and configuration into a single `main.py` works for 50 lines, then becomes impossible to maintain. "
                            "Production FastAPI services separate concerns into `config.py`, `database.py`, `models/`, `routers/`, and `dependencies.py`.\n\n"
                            "### Clean Database Session Injection\n\n"
                            "Using `Depends(get_db)` ensures each incoming HTTP request gets a fresh SQLAlchemy session and closes it deterministically in a `finally` block—even if an exception occurs.\n\n"
                            "```python\n"
                            "def get_db():\n"
                            "    db = SessionLocal()\n"
                            "    try:\n"
                            "        yield db\n"
                            "    finally:\n"
                            "        db.close()\n"
                            "```\n\n"
                            "### APIRouter Organization\n\n"
                            "Group related endpoints (`auth`, `admin`, `api`) into separate `APIRouter` modules and mount them inside `app/main.py` with `app.include_router(...)`. "
                            "FastAPI automatically organizes them by tags inside Swagger UI at `/docs`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Inspect `/docs` on a running FastAPI server and verify how `tags=['API']` groups endpoints cleanly."
                        ),
                    },
                    {
                        "title": "Relational Modeling with SQLAlchemy 2.0 & PostgreSQL",
                        "duration_mins": 26,
                        "content_md": (
                            "## Enforcing Data Integrity at the Database Layer\n\n"
                            "Never rely solely on frontend checks or Python `if` statements to protect data consistency. "
                            "Use PostgreSQL foreign keys, `NOT NULL` constraints, and `UniqueConstraint` rules so invalid rows are impossible.\n\n"
                            "```python\n"
                            "class Enrollment(Base):\n"
                            "    __tablename__ = 'enrollments'\n"
                            "    __table_args__ = (UniqueConstraint('user_id', 'course_id', name='uq_user_course'),)\n\n"
                            "    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n"
                            "    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))\n"
                            "    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id', ondelete='CASCADE'))\n"
                            "```\n\n"
                            "### Avoiding the N+1 Query Problem\n\n"
                            "When rendering a course along with all its modules and lessons, lazy loading triggers extra SQL queries inside loops. "
                            "Use `selectinload(Course.modules).selectinload(Module.lessons)` so SQLAlchemy fetches the full hierarchy in minimal queries.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Design a schema with `users`, `courses`, and `enrollments` and add `ondelete='CASCADE'` to child foreign keys."
                        ),
                    },
                    {
                        "title": "Pydantic Validation & Clean Error Responses",
                        "duration_mins": 20,
                        "content_md": (
                            "## Automatic Request Validation\n\n"
                            "One of FastAPI's biggest advantages over Flask is built-in validation via Pydantic type annotations. "
                            "Invalid field types or missing parameters are automatically rejected with **HTTP 422 Unprocessable Entity** and clear field-level details.\n\n"
                            "### Custom Exception Handlers for HTML vs. API\n\n"
                            "When an application serves both browser pages and JSON `/api/*` endpoints, return clean HTML error pages (`404`, `403`) for browsers while returning structured JSON errors for API clients.\n\n"
                            "```python\n"
                            "@app.exception_handler(HTTPException)\n"
                            "async def custom_http_handler(request: Request, exc: HTTPException):\n"
                            "    if request.url.path.startswith('/api/'):\n"
                            "        return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})\n"
                            "    return templates.TemplateResponse(request, 'errors/404.html', status_code=exc.status_code)\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Test hitting a missing URL and verify your app returns a styled 404 page instead of raw JSON."
                        ),
                    },
                ],
            },
            {
                "title": "Module 2: Authentication & Production Deployment",
                "lessons": [
                    {
                        "title": "Implementing HttpOnly JWT Cookies & Role Guards",
                        "duration_mins": 28,
                        "content_md": (
                            "## Secure Browser Sessions Without localStorage\n\n"
                            "Storing JWT tokens in `localStorage` exposes them to any malicious JavaScript (XSS). "
                            "Storing signed JWTs inside `HttpOnly`, `SameSite=Lax` cookies prevents client-side scripts from reading the token while automatically sending it on page requests.\n\n"
                            "### Reusable RBAC Dependency\n\n"
                            "```python\n"
                            "def require_roles(*allowed_roles: str):\n"
                            "    def _guard(current_user: User = Depends(get_current_user)) -> User:\n"
                            "        if current_user.role not in allowed_roles:\n"
                            "            raise HTTPException(status_code=403, detail='Permission denied')\n"
                            "        return current_user\n"
                            "    return _guard\n"
                            "```\n\n"
                            "### Password Hashing Best Practices\n\n"
                            "Always hash passwords with a per-user salt using `bcrypt` before saving to PostgreSQL, and verify using `bcrypt.checkpw()`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Sign up as a `student` user and verify that requesting `/admin` returns HTTP `403 Forbidden`."
                        ),
                    },
                    {
                        "title": "Deploying FastAPI + PostgreSQL on Render",
                        "duration_mins": 22,
                        "content_md": (
                            "## ASGI vs. WSGI in Production\n\n"
                            "Flask uses WSGI (sync workers), whereas FastAPI is an ASGI framework. When deploying with Gunicorn on Render, you must specify `UvicornWorker`:\n\n"
                            "```bash\n"
                            "gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT\n"
                            "```\n\n"
                            "### Production Checklist\n\n"
                            "1. Pin Python version via `.python-version` (for example `3.11.8`) so cloud hosts match your tested local runtime.\n"
                            "2. Normalize `postgres://` URLs to `postgresql://` for SQLAlchemy 2.0 compatibility.\n"
                            "3. Store secrets (`JWT_SECRET`, `DATABASE_URL`, `ADMIN_PASSWORD`) in Environment Variables—never commit `.env` to GitHub.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Verify `/api/health` returns `{\"status\": \"ok\"}` after every deployment."
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
                            "## What Examiners Expect in CPU Scheduling Questions\n\n"
                            "CPU scheduling determines which process in the Ready Queue gets CPU execution next. "
                            "In B.Tech Operating Systems exams, you are almost always asked to draw a Gantt chart and compute Average Turnaround Time and Average Waiting Time.\n\n"
                            "### Core Algorithms Side by Side\n\n"
                            "- **FCFS (First-Come, First-Served):** Non-preemptive FIFO queue. Easy to implement, but causes the **Convoy Effect** when short processes get stuck behind one long CPU-bound job.\n"
                            "- **SJF (Shortest Job First):** Provably gives minimum average waiting time among non-preemptive algorithms, but requires knowing burst lengths in advance and can starve long jobs.\n"
                            "- **SRTF (Shortest Remaining Time First):** Preemptive version of SJF.\n"
                            "- **Round Robin (RR):** Preemptive with a fixed **Time Quantum (`q`)**. Fair response time for interactive systems, though too small a `q` increases context-switch overhead.\n\n"
                            "### Must-Memorize Formulas\n\n"
                            "1. **Turnaround Time (TAT)** = `Completion Time (CT) - Arrival Time (AT)`\n"
                            "2. **Waiting Time (WT)** = `Turnaround Time (TAT) - Burst Time (BT)`\n"
                            "3. **Response Time (RT)** = `First CPU Time - Arrival Time (AT)`\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Draw the Gantt chart for processes `P1(BT=5), P2(BT=3), P3(BT=8), P4(BT=6)` all arriving at `AT=0` using Round Robin with `q = 2`.\n"
                            "- Compute Average TAT and Average WT step by step."
                        ),
                    },
                    {
                        "title": "Deadlocks: 4 Coffman Conditions & Banker's Algorithm",
                        "duration_mins": 24,
                        "content_md": (
                            "## Understanding Deadlocks Clearly\n\n"
                            "A deadlock occurs when a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the same set.\n\n"
                            "### The 4 Coffman Necessary Conditions\n\n"
                            "Deadlock can only happen if **all four** conditions hold simultaneously:\n"
                            "1. **Mutual Exclusion:** At least one resource must be held in a non-shareable mode.\n"
                            "2. **Hold and Wait:** A process holds at least one resource while waiting to acquire additional resources.\n"
                            "3. **No Preemption:** Resources cannot be forcibly taken away; they must be released voluntarily.\n"
                            "4. **Circular Wait:** A closed cycle `P0 -> P1 -> ... -> Pn -> P0` exists where each process waits on the next.\n\n"
                            "### Deadlock Avoidance with Banker's Algorithm\n\n"
                            "Banker's Algorithm checks whether granting a resource request leaves the system in a **Safe State** (there exists at least one execution sequence where every process finishes):\n\n"
                            "- Compute `Need[i][j] = Max[i][j] - Allocation[i][j]`.\n"
                            "- Repeatedly pick a process `i` whose `Need[i] <= Available`, simulate it finishing, and add `Allocation[i]` back to `Available`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write down one practical method to break each of the 4 Coffman conditions (e.g., total ordering of resources breaks Circular Wait)."
                        ),
                    },
                    {
                        "title": "Paging, Virtual Memory & Page Replacement (LRU vs FIFO)",
                        "duration_mins": 24,
                        "content_md": (
                            "## Why Operating Systems Use Paging\n\n"
                            "Contiguous memory allocation suffers from external fragmentation (wasted holes between processes). "
                            "Paging solves this by splitting physical RAM into fixed-size **Frames** and a process's logical memory into equal-sized **Pages**.\n\n"
                            "### Address Translation & TLB\n\n"
                            "A logical address splits into `(Page Number p, Offset d)`. The CPU uses the **Page Table** (accelerated by a hardware **TLB cache**) to translate `p` into physical Frame Number `f`, keeping offset `d` unchanged.\n\n"
                            "### Page Replacement Policies\n\n"
                            "When a **Page Fault** occurs and all RAM frames are full, the OS must pick a victim page:\n"
                            "- **FIFO:** Evicts the oldest loaded page. Simple queue, but suffers from **Belady's Anomaly** (allocating more frames can counter-intuitively cause *more* page faults).\n"
                            "- **Optimal:** Evicts the page not used for the longest time in the future (benchmark only).\n"
                            "- **LRU (Least Recently Used):** Evicts the page unused for the longest time in the past. Good practical approximation of Optimal and immune to Belady's Anomaly.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Simulate `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2` with **3 frames** under both FIFO and LRU and compare the total Page Fault counts."
                        ),
                    },
                ],
            },
            {
                "title": "Module 2: DBMS Normalization & Transactions",
                "lessons": [
                    {
                        "title": "Database Normalization (1NF, 2NF, 3NF, BCNF with Examples)",
                        "duration_mins": 28,
                        "content_md": (
                            "## Why Normalize Relational Tables?\n\n"
                            "Storing repeated data in one giant table causes **Insertion, Update, and Deletion Anomalies**. "
                            "Normalization splits tables cleanly using functional dependencies so each fact lives in one authoritative place.\n\n"
                            "### Step-by-Step Normal Forms\n\n"
                            "1. **First Normal Form (1NF):** Every column holds atomic (indivisible) values — no comma-separated lists or nested arrays.\n"
                            "2. **Second Normal Form (2NF):** Must be in 1NF and have **no Partial Dependency** (every non-prime attribute must depend on the *entire* composite primary key, not just part of it).\n"
                            "3. **Third Normal Form (3NF):** Must be in 2NF and have **no Transitive Dependency** (`Key -> A` and `A -> B` where `A` and `B` are non-key attributes).\n"
                            "4. **Boyce-Codd Normal Form (BCNF):** For every non-trivial functional dependency `X -> Y`, `X` must be a **Super Key**.\n\n"
                            "### Concrete Example\n\n"
                            "Consider `Enrollment(StudentID, CourseID, StudentName, CourseTitle)` with composite key `(StudentID, CourseID)`:\n"
                            "- `StudentID -> StudentName` is a **partial dependency** (violates 2NF).\n"
                            "- Solution: Split into `Students(StudentID, StudentName)`, `Courses(CourseID, CourseTitle)`, and `Enrollments(StudentID, CourseID)`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Decompose `Employee(EmpID, DeptID, DeptName, DeptLocation)` into 3NF tables and identify each primary and foreign key."
                        ),
                    },
                    {
                        "title": "ACID Properties & Transaction States in DBMS",
                        "duration_mins": 20,
                        "content_md": (
                            "## What Is a Database Transaction?\n\n"
                            "A transaction is a single logical unit of work consisting of one or more SQL operations (such as debiting ₹5,000 from Account A and crediting ₹5,000 to Account B). Either the whole unit succeeds, or none of it takes effect.\n\n"
                            "### The 4 ACID Guarantees\n\n"
                            "- **Atomicity (All or Nothing):** Ensured by the Transaction Recovery Manager via Undo/Redo logs.\n"
                            "- **Consistency:** A valid database state transitions strictly to another valid state honoring all constraints and triggers.\n"
                            "- **Isolation:** Concurrent transactions execute without exposing dirty/uncommitted intermediate writes (enforced via locks or MVCC).\n"
                            "- **Durability:** Once `COMMIT` succeeds, changes persist in non-volatile storage even across power loss.\n\n"
                            "### Transaction Lifecycle States\n\n"
                            "`Active` &rarr; `Partially Committed` &rarr; `Committed` (success path), or `Active / Partially Committed` &rarr; `Failed` &rarr; `Aborted` (rollback path).\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a PostgreSQL `BEGIN; ... COMMIT;` block transferring balance between two accounts, and explain what `ROLLBACK;` restores if the second `UPDATE` fails."
                        ),
                    },
                ],
            },
            {
                "title": "Module 3: Java OOP Exam & Viva Essentials",
                "lessons": [
                    {
                        "title": "Abstract Class vs Interface & Exception Handling in Java",
                        "duration_mins": 22,
                        "content_md": (
                            "## Abstract Class vs. Interface (Most Asked Viva Question)\n\n"
                            "Both let you define abstract contracts in Java, but they serve different design purposes:\n\n"
                            "- **Abstract Class:** Models an **is-a** base concept. Can hold instance fields, constructors, and concrete helper methods. A subclass can `extends` only **one** abstract class.\n"
                            "- **Interface:** Models a **can-do** capability (`Comparable`, `Payable`). A class can `implements` **multiple** interfaces, enabling clean polymorphism.\n\n"
                            "```java\n"
                            "interface Payable {\n"
                            "    void processPayment(double amount);\n"
                            "}\n\n"
                            "class UpiPayment implements Payable {\n"
                            "    public void processPayment(double amount) {\n"
                            "        System.out.println(\"Paid via UPI: \" + amount);\n"
                            "    }\n"
                            "}\n"
                            "```\n\n"
                            "### Checked vs. Unchecked Exceptions\n\n"
                            "- **Checked (`IOException`, `SQLException`):** Verified at compile time; must be caught or declared with `throws`.\n"
                            "- **Unchecked (`NullPointerException`, `ArithmeticException`):** Subclasses of `RuntimeException`; indicate programming bugs or invalid inputs.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a Java class using `try-catch-finally` (and `try-with-resources`) to safely divide two user-supplied integers."
                        ),
                    },
                    {
                        "title": "Java Collections Framework (List, Set, Map Cheat Sheet)",
                        "duration_mins": 24,
                        "content_md": (
                            "## Choosing the Right Java Collection\n\n"
                            "Knowing `java.util` collections saves hundreds of lines in both lab exams and DSA coding rounds.\n\n"
                            "- **`ArrayList<T>`:** Resizable array. **O(1)** random `get(i)`, **O(1)** amortized `add()`, **O(n)** middle insert/remove.\n"
                            "- **`LinkedList<T>` / `ArrayDeque<T>`:** Use `ArrayDeque` for fast Stacks (`push`/`pop`) and Queues (`offer`/`poll`) in BFS/DFS.\n"
                            "- **`HashSet<T>`:** Stores unique elements in **O(1)** average time (no guaranteed order). Use `TreeSet` if sorted order is needed (**O(log n)**).\n"
                            "- **`HashMap<K, V>`:** Key-value store with **O(1)** lookup. Use `TreeMap` for sorted keys.\n\n"
                            "```java\n"
                            "Map<String, Integer> freq = new HashMap<>();\n"
                            "for (String word : words) {\n"
                            "    freq.put(word, freq.getOrDefault(word, 0) + 1);\n"
                            "}\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a Java program reading a sentence and printing each unique word sorted alphabetically along with its frequency."
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
            "Stop memorizing SQL syntax passively. Practice the exact SELECT, JOIN, GROUP BY, subquery, "
            "CTE, and window-function queries companies ask freshers in first-round screening."
        ),
        "category": "SQL & Databases",
        "level": "Beginner",
        "modules": [
            {
                "title": "Module 1: Joins, Grouping & Subqueries",
                "lessons": [
                    {
                        "title": "INNER JOIN vs LEFT JOIN & Finding Unmatched Rows",
                        "duration_mins": 22,
                        "content_md": (
                            "## Why Joins Decide Most SQL Screening Rounds\n\n"
                            "Relational databases split data across normalized tables. Mastering joins lets you recombine entities cleanly without missing edge cases.\n\n"
                            "### INNER JOIN vs. LEFT JOIN\n\n"
                            "- **`INNER JOIN`:** Keeps only rows where the join key matches in **both** tables.\n"
                            "- **`LEFT JOIN`:** Keeps **every** row from the left table and fills `NULL` for columns on the right when no match exists.\n\n"
                            "### Finding Missing Relationships (`IS NULL` Anti-Join)\n\n"
                            "A classic placement question: *Find all registered students who have never enrolled in any course.*\n\n"
                            "```sql\n"
                            "SELECT u.id, u.full_name, u.email\n"
                            "FROM users u\n"
                            "LEFT JOIN enrollments e ON u.id = e.user_id\n"
                            "WHERE e.id IS NULL;\n"
                            "```\n\n"
                            "### Common Trap with `COUNT(*)` vs `COUNT(col)`\n\n"
                            "In a `LEFT JOIN`, `COUNT(*)` counts the unmatched `NULL` row as `1`, whereas `COUNT(e.id)` correctly ignores `NULL` and returns `0`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a query listing every course title alongside its total enrollment count (`0` for courses with no students yet)."
                        ),
                    },
                    {
                        "title": "GROUP BY, HAVING & Finding the 2nd Highest Salary",
                        "duration_mins": 24,
                        "content_md": (
                            "## WHERE vs. HAVING (Order of SQL Execution)\n\n"
                            "SQL logically executes clauses in this order: `FROM` &rarr; `WHERE` &rarr; `GROUP BY` &rarr; `HAVING` &rarr; `SELECT` &rarr; `ORDER BY`.\n\n"
                            "- Use **`WHERE`** to filter individual rows *before* grouping.\n"
                            "- Use **`HAVING`** to filter aggregated groups (like `HAVING COUNT(*) > 5`) *after* `GROUP BY`.\n\n"
                            "### Classic Question: 2nd Highest Distinct Salary\n\n"
                            "```sql\n"
                            "SELECT MAX(salary) AS second_highest_salary\n"
                            "FROM employees\n"
                            "WHERE salary < (SELECT MAX(salary) FROM employees);\n"
                            "```\n\n"
                            "Why this works even on empty tables or duplicate top salaries: `MAX()` safely returns `NULL` if no second-highest salary exists, and `< (SELECT MAX...)` skips ties at the top.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a query returning departments (`dept_id`) that have at least 3 employees earning strictly above `45000`."
                        ),
                    },
                ],
            },
            {
                "title": "Module 2: Window Functions, CTEs & Indexing",
                "lessons": [
                    {
                        "title": "Window Functions (ROW_NUMBER, RANK, DENSE_RANK) & B-Tree Indexes",
                        "duration_mins": 26,
                        "content_md": (
                            "## Ranking Rows Without Collapsing Groups\n\n"
                            "Unlike `GROUP BY` which collapses rows into one summary row per group, window functions (`OVER (...)`) keep every original row while computing group-aware rankings or running totals.\n\n"
                            "```sql\n"
                            "SELECT name, department, salary,\n"
                            "       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank\n"
                            "FROM employees;\n"
                            "```\n\n"
                            "### Comparing Ranking Functions on Ties (`100, 100, 90`)\n\n"
                            "- `ROW_NUMBER()`: `1, 2, 3` (strictly unique)\n"
                            "- `RANK()`: `1, 1, 3` (leaves gaps after ties)\n"
                            "- `DENSE_RANK()`: `1, 1, 2` (no gaps — best for Top-N salaries per department)\n\n"
                            "### How B-Tree Indexes Speed Up Queries\n\n"
                            "Without an index, PostgreSQL performs a **Sequential Scan** (`O(n)`). Adding a B-Tree index (`CREATE INDEX idx_users_email ON users(email);`) reduces lookups to **O(log n)**, at the cost of slightly slower writes.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Wrap the `DENSE_RANK()` query in a CTE and return only the **top 2 earners per department** (`WHERE dept_rank <= 2`)."
                        ),
                    },
                    {
                        "title": "Common Table Expressions (CTEs) & Self Joins",
                        "duration_mins": 22,
                        "content_md": (
                            "## Writing Readable Multi-Step Queries with `WITH`\n\n"
                            "Deeply nested subqueries are hard to debug in interviews. A **CTE (`WITH ... AS`)** gives each intermediate result a clear name so your SQL reads top-to-bottom.\n\n"
                            "```sql\n"
                            "WITH dept_avg AS (\n"
                            "    SELECT dept_id, AVG(salary) AS avg_sal\n"
                            "    FROM employees\n"
                            "    GROUP BY dept_id\n"
                            ")\n"
                            "SELECT e.name, e.salary, d.avg_sal\n"
                            "FROM employees e\n"
                            "JOIN dept_avg d ON e.dept_id = d.dept_id\n"
                            "WHERE e.salary > d.avg_sal;\n"
                            "```\n\n"
                            "### Self Joins for Hierarchies\n\n"
                            "When employees and their managers live in the same `employees(id, name, manager_id)` table, join the table to itself using distinct aliases (`e` and `m`):\n\n"
                            "```sql\n"
                            "SELECT e.name AS employee, m.name AS manager\n"
                            "FROM employees e\n"
                            "LEFT JOIN employees m ON e.manager_id = m.id;\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Write a Self Join query finding all employees who earn **more** than their direct manager."
                        ),
                    },
                ],
            },
        ],
    },
    {
        "title": "Web Programming & JavaScript Essentials",
        "slug": "web-programming-javascript",
        "subtitle": "Master semantic HTML, responsive CSS Grid/Flexbox, async JavaScript, and Fetch API.",
        "description": (
            "Designed for both B.Tech Web Programming exams and frontend/full-stack interviews. "
            "Learn how browsers render pages, build mobile-first layouts, and write clean asynchronous JavaScript."
        ),
        "category": "Web & Frontend",
        "level": "Beginner",
        "modules": [
            {
                "title": "Module 1: Semantic HTML & Responsive CSS",
                "lessons": [
                    {
                        "title": "Semantic HTML5, Forms & Accessibility Basics",
                        "duration_mins": 20,
                        "content_md": (
                            "## Why Semantic Tags Beat Generic Divs\n\n"
                            "Using `<header>`, `<nav>`, `<main>`, `<article>`, `<aside>`, and `<footer>` gives screen readers and search engines like Google an accurate map of your page structure.\n\n"
                            "### Essential Form & Accessibility Rules\n\n"
                            "- Every `<input>` must have a matching `<label for='...'>`.\n"
                            "- Use native `<button type='submit'>` instead of clickable `<div>` elements so keyboard `Enter` and `Tab` navigation work automatically.\n"
                            "- Include one clear `<h1>` per page and maintain ordered heading levels (`h1` &rarr; `h2` &rarr; `h3`).\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Audit one HTML form and verify you can navigate and submit it using only your keyboard (`Tab` and `Enter`)."
                        ),
                    },
                    {
                        "title": "Responsive Flexbox, CSS Grid & Media Queries",
                        "duration_mins": 24,
                        "content_md": (
                            "## Choosing Between Flexbox and CSS Grid\n\n"
                            "- **Flexbox (`display: flex`):** Best for **1-dimensional** rows or columns (navbars, button groups, card footers).\n"
                            "- **CSS Grid (`display: grid`):** Best for **2-dimensional** page layouts and responsive card grids.\n\n"
                            "```css\n"
                            ".card-grid {\n"
                            "    display: grid;\n"
                            "    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));\n"
                            "    gap: 1.5rem;\n"
                            "}\n"
                            "```\n\n"
                            "That single rule automatically adapts from 3 columns on desktop to 1 column on mobile phones without writing fragile width percentages.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Build a 2-column sidebar + content layout with CSS Grid that collapses cleanly into 1 column below `900px`."
                        ),
                    },
                ],
            },
            {
                "title": "Module 2: Modern JavaScript & Browser APIs",
                "lessons": [
                    {
                        "title": "DOM Manipulation, Events & Fetch API (Async/Await)",
                        "duration_mins": 24,
                        "content_md": (
                            "## Interacting with the Browser Without Frameworks\n\n"
                            "Every frontend framework compiles down to DOM manipulation. Mastering `querySelector`, `addEventListener`, and `fetch` makes you effective in any stack.\n\n"
                            "```javascript\n"
                            "async function loadCourses() {\n"
                            "    const res = await fetch('/api/courses');\n"
                            "    if (!res.ok) throw new Error('Failed to fetch courses');\n"
                            "    const courses = await res.json();\n"
                            "    console.log(courses);\n"
                            "}\n"
                            "```\n\n"
                            "### Always Check `res.ok`\n\n"
                            "Unlike Axios, native `fetch()` only rejects on network failures—not HTTP `404` or `500` responses. Always check `if (!res.ok)` before calling `res.json()`.\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Fetch `/api/courses` from the browser console and render each course title into a `<ul>` element."
                        ),
                    },
                    {
                        "title": "JavaScript Closures, Promises & Event Loop Explained",
                        "duration_mins": 25,
                        "content_md": (
                            "## The Most Tested JavaScript Interview Trio\n\n"
                            "1. **Closure:** A function remembers variables from its outer lexical scope even after the outer function has finished returning.\n"
                            "2. **Promise:** Represents an eventual completion (`fulfilled`) or failure (`rejected`) of an asynchronous operation.\n"
                            "3. **Event Loop:** JavaScript executes synchronous code on a single Call Stack, then drains **Microtasks** (`.then`, `await`) before picking the next **Macrotask** (`setTimeout`).\n\n"
                            "```javascript\n"
                            "console.log('1');\n"
                            "setTimeout(() => console.log('2'), 0);\n"
                            "Promise.resolve().then(() => console.log('3'));\n"
                            "console.log('4');\n"
                            "// Output order: 1, 4, 3, 2\n"
                            "```\n\n"
                            "### Actionable Practice Task\n\n"
                            "- Trace the output order above and explain why `'3'` prints before `'2'`."
                        ),
                    },
                ],
            },
        ],
    },
]
