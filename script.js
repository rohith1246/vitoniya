/**
 * Vitoniya Global Technologies - Corporate Web Experience
 * Vanilla JavaScript - Zero dependencies, high performance
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initEmailCopy();
  initModals();
});

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
    if (window.scrollY > 15) {
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
        // Fallback for non-HTTPS or legacy contexts
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
