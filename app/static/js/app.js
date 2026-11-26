document.addEventListener("DOMContentLoaded", () => {
    // Mobile navbar toggle
    const toggleBtn = document.getElementById("mobile-menu-toggle");
    const navLinks = document.getElementById("primary-nav");
    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("open");
            toggleBtn.setAttribute("aria-expanded", String(isOpen));
        });
    }

    // Mobile lesson syllabus toggle
    const syllabusBtn = document.getElementById("mobile-syllabus-toggle");
    const syllabusAside = document.getElementById("lesson-sidebar");
    if (syllabusBtn && syllabusAside) {
        syllabusBtn.addEventListener("click", () => {
            const isOpen = syllabusAside.classList.toggle("open");
            syllabusBtn.textContent = isOpen ? "Hide syllabus" : "Show course syllabus";
        });
    }

    // Password visibility toggles
    document.querySelectorAll("[data-password-toggle]").forEach((btn) => {
        btn.addEventListener("click", () => {
            const inputId = btn.getAttribute("data-password-toggle");
            const input = document.getElementById(inputId);
            if (!input) return;
            const showing = input.type === "text";
            input.type = showing ? "password" : "text";
            btn.textContent = showing ? "Show" : "Hide";
        });
    });

    // Submit loading state
    document.querySelectorAll("form[data-loading-text]").forEach((form) => {
        form.addEventListener("submit", () => {
            const submitBtn = form.querySelector("button[type='submit']");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = form.getAttribute("data-loading-text");
            }
        });
    });

    // Confirmation prompt for sensitive admin actions
    document.querySelectorAll("[data-confirm]").forEach((el) => {
        el.addEventListener("submit", (e) => {
            const msg = el.getAttribute("data-confirm");
            if (msg && !window.confirm(msg)) {
                e.preventDefault();
            }
        });
    });
});
