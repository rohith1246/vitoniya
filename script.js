/**
 * Vitoniya Global Technologies - Launching Soon Experience
 * Vanilla JavaScript - Zero dependencies, high performance
 */

document.addEventListener('DOMContentLoaded', () => {
  initTechCanvas();
  initNavigation();
  initEmailCopy();
  initModals();
});

/* ==========================================================================
   INTERACTIVE TECH CANVAS
   Subtle particle/network visualization with soft cyan nodes & connections
   ========================================================================== */
function initTechCanvas() {
  const canvas = document.getElementById('tech-canvas');
  if (!canvas) return;

  // Respect reduced motion settings
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const ctx = canvas.getContext('2d');
  let animationFrameId = null;
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  // Mouse interaction state
  const mouse = {
    x: -9999,
    y: -9999,
    radius: 120
  };

  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = -9999;
    mouse.y = -9999;
  });

  // Handle window resizing
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      initParticles();
    }, 150);
  });

  // Dynamic particle count based on screen area
  let particles = [];
  function initParticles() {
    particles = [];
    const count = Math.min(Math.floor((width * height) / 22000), 65);

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.45,
        vy: (Math.random() - 0.5) * 0.45,
        radius: Math.random() * 1.5 + 1,
        baseAlpha: Math.random() * 0.35 + 0.15
      });
    }
  }

  initParticles();

  // Animation Loop
  function render() {
    ctx.clearRect(0, 0, width, height);

    // Draw connecting lines between close particles
    const maxDistance = 130;
    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];

      // Update position
      p1.x += p1.vx;
      p1.y += p1.vy;

      // Bounce smoothly off edges
      if (p1.x < 0 || p1.x > width) p1.vx *= -1;
      if (p1.y < 0 || p1.y > height) p1.vy *= -1;

      // Mouse proximity interaction: subtle acceleration
      const dxMouse = mouse.x - p1.x;
      const dyMouse = mouse.y - p1.y;
      const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);

      if (distMouse < mouse.radius) {
        const force = (mouse.radius - distMouse) / mouse.radius;
        p1.x -= (dxMouse / distMouse) * force * 1.2;
        p1.y -= (dyMouse / distMouse) * force * 1.2;
      }

      // Draw particle node
      ctx.beginPath();
      ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0, 229, 255, ${p1.baseAlpha})`;
      ctx.fill();

      // Connect with neighbors
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < maxDistance) {
          const lineAlpha = (1 - distance / maxDistance) * 0.12;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(0, 229, 255, ${lineAlpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    animationFrameId = requestAnimationFrame(render);
  }

  // Throttle when page is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    } else {
      render();
    }
  });

  render();
}

/* ==========================================================================
   NAVIGATION & MOBILE DRAWER
   ========================================================================== */
function initNavigation() {
  const header = document.getElementById('site-header');
  const toggleBtn = document.getElementById('mobile-toggle');
  const drawer = document.getElementById('mobile-drawer');
  const mobileLinks = document.querySelectorAll('.mobile-link, .mobile-cta');

  // Sticky header background shift on scroll
  const handleScroll = () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  if (!toggleBtn || !drawer) return;

  function setDrawerState(isOpen) {
    toggleBtn.classList.toggle('is-active', isOpen);
    toggleBtn.setAttribute('aria-expanded', isOpen);
    drawer.classList.toggle('open', isOpen);
    drawer.setAttribute('aria-hidden', !isOpen);
  }

  toggleBtn.addEventListener('click', () => {
    const isOpen = drawer.classList.contains('open');
    setDrawerState(!isOpen);
  });

  // Close drawer on clicking any link
  mobileLinks.forEach((link) => {
    link.addEventListener('click', () => {
      setDrawerState(false);
    });
  });

  // Close drawer on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      setDrawerState(false);
    }
  });
}

/* ==========================================================================
   COPY EMAIL FUNCTIONALITY
   ========================================================================== */
function initEmailCopy() {
  const copyBtn = document.getElementById('btn-copy-email');
  const toast = document.getElementById('copy-toast');
  const email = 'info@vitoniya.com';

  if (!copyBtn) return;

  let toastTimer;

  copyBtn.addEventListener('click', async () => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(email);
      } else {
        // Fallback for non-HTTPS or legacy browsers
        const tempInput = document.createElement('input');
        tempInput.value = email;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
      }

      // Show toast
      if (toast) {
        clearTimeout(toastTimer);
        toast.classList.add('show');
        toastTimer = setTimeout(() => {
          toast.classList.remove('show');
        }, 2200);
      }
    } catch (err) {
      console.error('Could not copy email:', err);
    }
  });
}

/* ==========================================================================
   MODALS (PRIVACY & TERMS)
   ========================================================================== */
function initModals() {
  const openButtons = document.querySelectorAll('[data-modal]');
  const closeButtons = document.querySelectorAll('.modal-close, .modal-close-btn');
  const modalBackdrops = document.querySelectorAll('.modal-backdrop');

  openButtons.forEach((button) => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = button.getAttribute('data-modal');
      const targetModal = document.getElementById(modalId);
      if (targetModal) {
        openModal(targetModal);
      }
    });
  });

  closeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const parentModal = button.closest('.modal-backdrop');
      if (parentModal) {
        closeModal(parentModal);
      }
    });
  });

  modalBackdrops.forEach((backdrop) => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        closeModal(backdrop);
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModalEl = document.querySelector('.modal-backdrop.is-open');
      if (openModalEl) {
        closeModal(openModalEl);
      }
    }
  });

  function openModal(modalEl) {
    modalEl.classList.add('is-open');
    modalEl.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal(modalEl) {
    modalEl.classList.remove('is-open');
    modalEl.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
}
