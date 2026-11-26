document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("mobile-menu-toggle");
    const navLinks = document.getElementById("primary-nav");

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }
});
