"""High-traffic Interview Question banks for Java, Python/FastAPI, SQL, GenAI/RAG, and System Design."""

INTERVIEW_GUIDES = [
    {
        "slug": "java-fresher-backend-interview-questions",
        "title": "Top Java & OOP Interview Questions for Freshers & Backend Roles",
        "category": "Java",
        "level": "Fresher / 0–2 Yrs",
        "summary": "Essential Core Java, JVM memory, HashMap internals, String pool, and multithreading questions asked by product companies and GCCs.",
        "qa": [
            {
                "q": "1. What is the difference between JDK, JRE, and JVM?",
                "a": (
                    "**JVM (Java Virtual Machine)** executes compiled bytecode (`.class` files) and provides platform independence. "
                    "**JRE (Java Runtime Environment)** includes the JVM plus standard runtime libraries needed to *run* Java programs. "
                    "**JDK (Java Development Kit)** includes the JRE plus development tools like `javac` (compiler) and `jdb` (debugger) needed to *build* Java applications."
                ),
            },
            {
                "q": "2. How does a HashMap work internally in Java?",
                "a": (
                    "`HashMap` stores entries in an array of buckets (`Node<K,V>[]`). When you call `put(key, value)`, Java computes `key.hashCode()`, mixes the bits, and maps it to a bucket index `(n - 1) & hash`. "
                    "If two different keys land in the same bucket (a **collision**), they are stored in a linked list inside that bucket—or converted into a balanced **Red-Black Tree** once a bucket exceeds 8 nodes (since Java 8), keeping worst-case lookup at `O(log n)`."
                ),
            },
            {
                "q": "3. Why are `equals()` and `hashCode()` overridden together?",
                "a": (
                    "The Java contract states: if two objects are equal according to `equals()`, they **must** return the same `hashCode()`. "
                    "If you override `equals()` without `hashCode()`, `HashMap` or `HashSet` may search the wrong bucket and fail to find an equal key."
                ),
            },
            {
                "q": "4. What is the difference between `==` and `.equals()`?",
                "a": (
                    "`==` compares **reference memory addresses** for objects (and actual values for primitives like `int`). "
                    "`.equals()` compares **logical content** (when overridden, such as in `String` or `Integer`). Always use `.equals()` for String comparison."
                ),
            },
            {
                "q": "5. Compare `String`, `StringBuilder`, and `StringBuffer`.",
                "a": (
                    "- **`String`:** Immutable; stored in the String Constant Pool. Concatenation inside loops creates extra garbage objects.\n"
                    "- **`StringBuilder`:** Mutable and fast, **not thread-safe**. Best choice for single-threaded string building.\n"
                    "- **`StringBuffer`:** Mutable and **thread-safe** (`synchronized` methods), slightly slower than `StringBuilder`."
                ),
            },
            {
                "q": "6. What is the difference between `ArrayList` and `LinkedList`?",
                "a": (
                    "`ArrayList` uses a dynamic contiguous array, giving `O(1)` random access via `get(i)` and `O(n)` middle insertions. "
                    "`LinkedList` uses doubly-linked nodes, giving `O(1)` head/tail insert/delete when holding a node reference, but `O(n)` index lookup and higher memory overhead per element."
                ),
            },
            {
                "q": "7. Why is `implements Runnable` preferred over `extends Thread`?",
                "a": (
                    "Java supports single class inheritance. Extending `Thread` wastes your only inheritance slot, whereas implementing `Runnable` lets your class still extend another class and cleanly separates the task logic from thread management (`ExecutorService`)."
                ),
            },
            {
                "q": "8. What is the difference between `final`, `finally`, and `finalize`?",
                "a": (
                    "- `final`: Keyword making a variable constant, a method non-overridable, or a class non-inheritable.\n"
                    "- `finally`: Block after `try/catch` that always executes (commonly used to close streams/connections).\n"
                    "- `finalize()`: Legacy `Object` method before garbage collection (deprecated since Java 9)."
                ),
            },
        ],
    },
    {
        "slug": "python-fastapi-interview-questions",
        "title": "Python & FastAPI Backend Interview Questions",
        "category": "Python & FastAPI",
        "level": "Fresher / Backend",
        "summary": "Most asked Python memory, GIL, decorators, async/await, Pydantic, and FastAPI dependency injection questions.",
        "qa": [
            {
                "q": "1. Why is FastAPI faster than Flask for modern AI and I/O-heavy backends?",
                "a": (
                    "Flask is traditionally WSGI-based (synchronous per worker unless paired with extra tooling), whereas FastAPI runs on **ASGI** (Starlette + Uvicorn) with native `async/await` support. "
                    "When waiting on external LLM APIs or database queries, FastAPI handles concurrent I/O efficiently without blocking the entire worker, and validates payloads in C/Rust speed via **Pydantic v2**."
                ),
            },
            {
                "q": "2. What is the difference between a Python `list` and a `tuple`?",
                "a": (
                    "Lists (`[]`) are **mutable** (elements can be added, removed, or changed), whereas tuples (`()`) are **immutable**. "
                    "Because tuples are immutable, they use slightly less memory and can serve as **dictionary keys** or `set` elements (if their contents are also immutable)."
                ),
            },
            {
                "q": "3. What is the Global Interpreter Lock (GIL) in Python?",
                "a": (
                    "The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time per process. "
                    "Because of the GIL, CPU-bound Python work scales better across **multiple processes** (`multiprocessing` / multiple Gunicorn workers), while I/O-bound work (network/DB calls) scales cleanly with **`asyncio`** or threads."
                ),
            },
            {
                "q": "4. Explain `*args` and `**kwargs` with a quick use case.",
                "a": (
                    "`*args` collects extra positional arguments into a tuple, and `**kwargs` collects extra keyword arguments into a dictionary. They are widely used in wrapper functions and decorators."
                ),
            },
            {
                "q": "5. What is a Decorator and a Generator (`yield`) in Python?",
                "a": (
                    "A **decorator** wraps another function to add behavior (like auth checks or logging) without modifying its core code. "
                    "A **generator** uses `yield` to produce items lazily one at a time instead of loading an entire list into memory."
                ),
            },
            {
                "q": "6. How does `Depends()` work in FastAPI?",
                "a": (
                    "`Depends()` is FastAPI's Dependency Injection system. You declare shared logic—like opening/closing a PostgreSQL session (`get_db`) or verifying an RBAC user role (`require_roles('admin')`)—once, and FastAPI automatically resolves, injects, and cleans it up per request."
                ),
            },
            {
                "q": "7. Difference between `is` and `==` in Python?",
                "a": (
                    "`==` checks **value equality** (`[1, 2] == [1, 2]` is `True`), whereas `is` checks **object identity** (whether both names point to the exact same object in memory; always use `is None` for `None` checks)."
                ),
            },
        ],
    },
    {
        "slug": "sql-dbms-interview-questions",
        "title": "SQL & DBMS Placement Interview Questions (With Queries)",
        "category": "SQL & DBMS",
        "level": "All Levels",
        "summary": "Core SQL queries, JOINs, DELETE vs TRUNCATE, indexing, normalization, and ACID questions asked in almost every tech screen.",
        "qa": [
            {
                "q": "1. Write an SQL query to find the 2nd highest distinct salary.",
                "a": (
                    "```sql\n"
                    "SELECT MAX(salary) AS second_highest\n"
                    "FROM employees\n"
                    "WHERE salary < (SELECT MAX(salary) FROM employees);\n"
                    "```\n"
                    "For the **Nth** highest salary per department, use `DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)` inside a CTE and filter `WHERE rnk = N`."
                ),
            },
            {
                "q": "2. Difference between `DELETE`, `TRUNCATE`, and `DROP`?",
                "a": (
                    "- **`DELETE` (DML):** Removes specific rows using `WHERE`; logged row-by-row and can be rolled back.\n"
                    "- **`TRUNCATE` (DDL):** Quickly removes **all** rows from a table without scanning individual rows while keeping the table structure.\n"
                    "- **`DROP` (DDL):** Completely deletes the table structure, indexes, and data."
                ),
            },
            {
                "q": "3. Difference between `WHERE` and `HAVING`?",
                "a": (
                    "`WHERE` filters individual rows **before** `GROUP BY` runs (cannot contain aggregate functions like `SUM` or `COUNT`). "
                    "`HAVING` filters aggregated groups **after** `GROUP BY` completes."
                ),
            },
            {
                "q": "4. How do Indexes speed up SQL queries, and what is the tradeoff?",
                "a": (
                    "A B-Tree index stores sorted key pointers so the database finds matching rows in `O(log n)` instead of doing a full `O(n)` table scan. "
                    "The tradeoff is extra disk space and slightly slower `INSERT`, `UPDATE`, and `DELETE` operations because every index must also be updated."
                ),
            },
            {
                "q": "5. Compare `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`.",
                "a": (
                    "`INNER JOIN` returns only matching rows from both tables. `LEFT JOIN` returns all rows from the left table plus matching right rows (or `NULL`). `FULL OUTER JOIN` returns all rows from both tables, filling `NULL` wherever a side has no match."
                ),
            },
            {
                "q": "6. Briefly explain ACID properties in DBMS.",
                "a": (
                    "**Atomicity** (all operations succeed or roll back), **Consistency** (constraints remain valid), **Isolation** (concurrent transactions do not corrupt each other), and **Durability** (committed data survives crashes)."
                ),
            },
        ],
    },
    {
        "slug": "genai-rag-ai-agents-interview-questions",
        "title": "GenAI, RAG & AI Agents Interview Questions (2026 Edition)",
        "category": "AI & Agents",
        "level": "Trending 2026",
        "summary": "Modern interview questions on LLM APIs, Embeddings, Vector Databases (pgvector), RAG pipelines, and Tool-Calling AI Agents.",
        "qa": [
            {
                "q": "1. What is RAG (Retrieval-Augmented Generation) and why use it instead of fine-tuning?",
                "a": (
                    "**RAG** retrieves relevant up-to-date documents from your own database at query time and injects them into the LLM prompt so the model answers grounded in real facts. "
                    "Compared to fine-tuning, RAG is much cheaper, updates instantly when your database changes, and dramatically reduces hallucinations."
                ),
            },
            {
                "q": "2. What are Embeddings and Vector Databases (like PostgreSQL `pgvector`)?",
                "a": (
                    "An **embedding** converts text into a fixed-length array of floating-point numbers capturing semantic meaning. "
                    "A **vector database** stores these embeddings and finds the most similar passages using cosine similarity or Euclidean distance—allowing search by *meaning* rather than exact keyword match."
                ),
            },
            {
                "q": "3. What is an AI Agent vs. a simple LLM chat wrapper?",
                "a": (
                    "A chat wrapper takes one prompt and returns text. An **AI Agent** operates in a reasoning loop: it decides *which tool to call* (SQL query, web search, API request), inspects the tool output, handles errors, and iterates until the goal is complete."
                ),
            },
            {
                "q": "4. How do you prevent LLM hallucinations and invalid JSON outputs in production?",
                "a": (
                    "1. Use **Structured Outputs / JSON Schema** enforcement (supported by Gemini and OpenAI APIs) validated with **Pydantic**.\n"
                    "2. Instruct the model via system prompts to say *'I don't know'* when retrieved RAG context lacks the answer.\n"
                    "3. Keep `temperature` low (`0.0–0.2`) for factual/classification tasks."
                ),
            },
            {
                "q": "5. How do you manage latency and API costs when calling LLMs from FastAPI?",
                "a": (
                    "Use smaller fast models (like Gemini Flash or Groq-hosted models) for routing/classification, cache repeated semantic queries in Redis/PostgreSQL, stream tokens with Server-Sent Events (SSE), and enforce max-token limits and rate limiting per user."
                ),
            },
        ],
    },
    {
        "slug": "system-design-interview-questions",
        "title": "System Design (HLD & LLD) Interview Questions",
        "category": "System Design",
        "level": "Intermediate",
        "summary": "Core scalability concepts tested in backend interviews: Load Balancing, Caching, Rate Limiting, SQL vs NoSQL, and Database Sharding.",
        "qa": [
            {
                "q": "1. How would you scale a read-heavy web platform from 100 to 100,000 users?",
                "a": (
                    "1. **Stateless App Tier behind a Load Balancer** (Nginx / Cloud LB) so you can add multiple backend instances horizontally.\n"
                    "2. **Cache Hot Reads** (like published course catalogs) in **Redis** using Cache-Aside.\n"
                    "3. **Database Read Replicas + Proper Indexing** so read traffic doesn't choke primary writes.\n"
                    "4. **CDN** for static CSS/JS/images."
                ),
            },
            {
                "q": "2. When should you choose PostgreSQL (SQL) vs. a NoSQL database?",
                "a": (
                    "Choose **PostgreSQL** when data is structured, relational, or requires ACID transactions (users, enrollments, payments, inventory). "
                    "Consider **NoSQL** (document/wide-column) when handling massive unstructured event streams or schemas that vary wildly per record."
                ),
            },
            {
                "q": "3. What is Rate Limiting and which algorithms implement it?",
                "a": (
                    "Rate limiting protects APIs and expensive LLM endpoints from abuse by capping requests per IP/user per time window. "
                    "Common algorithms include **Token Bucket** (allows controlled bursts), **Sliding Window Log**, and **Fixed Window Counter** (often backed by Redis `INCR` + `EXPIRE`)."
                ),
            },
            {
                "q": "4. Horizontal Scaling vs. Vertical Scaling?",
                "a": (
                    "**Vertical scaling** upgrades CPU/RAM on a single machine (simple, but hits hardware limits and creates a single point of failure). "
                    "**Horizontal scaling** adds more machines behind a load balancer (higher availability and virtually unlimited scale, requiring stateless services)."
                ),
            },
        ],
    },
]
