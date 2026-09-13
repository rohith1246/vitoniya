document.addEventListener('DOMContentLoaded', () => {
  // 1. Navigation & Header
  const header = document.getElementById('header');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link, .mobile-cta');
  const sections = document.querySelectorAll('section');
  const navLinks = document.querySelectorAll('.nav-link');

  // Sticky header class
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    // Active Nav Highlighting
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (scrollY >= (sectionTop - 200)) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').includes(current)) {
        link.classList.add('active');
      }
    });
  });

  // Mobile drawer toggle
  function toggleMenu() {
    mobileMenuBtn.classList.toggle('open');
    mobileDrawer.classList.toggle('open');
    document.body.style.overflow = mobileDrawer.classList.contains('open') ? 'hidden' : '';
  }

  mobileMenuBtn.addEventListener('click', toggleMenu);

  // Close mobile drawer on link click
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (mobileDrawer.classList.contains('open')) {
        toggleMenu();
      }
    });
  });

  // Close mobile drawer on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileDrawer.classList.contains('open')) {
      toggleMenu();
    }
  });

  // 2. Scroll Reveal
  const revealElements = document.querySelectorAll('.reveal');
  
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback for older browsers
    revealElements.forEach(el => el.classList.add('visible'));
  }

  // 4. Email Copy
  const copyBtn = document.getElementById('copy-email');
  const toast = document.getElementById('toast');

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText('info@vitoniya.com').then(() => {
        toast.classList.add('show');
        setTimeout(() => {
          toast.classList.remove('show');
        }, 3000);
      }).catch(err => {
        console.error('Failed to copy text: ', err);
      });
    });
  }

  // 5. Contact Form
  const contactForm = document.getElementById('contact-form');
  const formSuccess = document.getElementById('form-success');
  const formError = document.getElementById('form-error');
  const submitBtn = document.getElementById('submit-btn');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Basic validation
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      
      if (!name || !email || !message) {
        return; // HTML5 required attribute should catch this, but just in case
      }
      
      if (!emailRegex.test(email)) {
        return;
      }
      
      // Setup payload
      const formData = new FormData(contactForm);
      const payload = Object.fromEntries(formData.entries());
      
      // Loading state
      const originalBtnText = submitBtn.textContent;
      submitBtn.textContent = 'Sending...';
      submitBtn.disabled = true;
      formSuccess.hidden = true;
      formError.hidden = true;
      
      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        
        if (response.ok) {
          formSuccess.hidden = false;
          contactForm.reset();
        } else {
          formError.hidden = false;
        }
      } catch (error) {
        console.error('Error submitting form:', error);
        formError.hidden = false;
      } finally {
        submitBtn.textContent = originalBtnText;
        submitBtn.disabled = false;
      }
    });
  }

  // 6. Modals
  const modalTriggers = document.querySelectorAll('[data-modal]');
  const modals = document.querySelectorAll('.modal');
  const modalCloseBtns = document.querySelectorAll('.modal-close');

  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeModal() {
    modals.forEach(modal => {
      modal.classList.remove('open');
    });
    document.body.style.overflow = '';
  }

  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = trigger.getAttribute('data-modal');
      openModal(modalId);
    });
  });

  modalCloseBtns.forEach(btn => {
    btn.addEventListener('click', closeModal);
  });

  // Close modal on click outside
  modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  });
  
  // Close modal on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });

  // 7. Fullscreen Intro Animation Video Controller
  const introOverlay = document.getElementById('intro-video-overlay');
  const introVideo = document.getElementById('intro-splash-video');
  const skipIntroBtn = document.getElementById('skip-intro-btn');

  if (introOverlay && introVideo) {
    let hasDismissed = false;

    const dismissIntro = () => {
      if (hasDismissed) return;
      hasDismissed = true;
      introOverlay.classList.add('fade-out');
      document.body.style.overflow = '';
      setTimeout(() => {
        try {
          introVideo.pause();
        } catch (e) {}
      }, 900);
    };

    // Lock scroll during intro animation
    document.body.style.overflow = 'hidden';

    // Auto-dismiss when intro animation completes
    introVideo.addEventListener('ended', dismissIntro);

    // Skip button
    if (skipIntroBtn) {
      skipIntroBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dismissIntro();
      });
    }

    // Safety fallback: dismiss after 10.5 seconds if video stalls
    setTimeout(() => {
      dismissIntro();
    }, 10500);

    // Ensure video starts playing immediately
    introVideo.muted = true;
    introVideo.setAttribute('muted', '');
    introVideo.setAttribute('playsinline', '');
    const playPromise = introVideo.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        // If autoplay blocked, dismiss smoothly on first user click or touch
        const onAnyInput = () => {
          dismissIntro();
          window.removeEventListener('click', onAnyInput);
          window.removeEventListener('touchstart', onAnyInput);
        };
        window.addEventListener('click', onAnyInput, { passive: true });
        window.addEventListener('touchstart', onAnyInput, { passive: true });
      });
    }
  }

  // 8. Premium Hero Interactive System (Particles, Parallax & Entrance)
  const heroSection = document.getElementById('hero');
  const heroLeft = document.querySelector('.hero-left');
  const heroVisual = document.getElementById('hero-visual');
  const heroLogoWrap = document.getElementById('hero-logo-wrap');
  const particleCanvas = document.getElementById('hero-particles');

  // Trigger entrance when hero is visible
  const triggerHeroEntrance = () => {
    if (heroLeft) {
      heroLeft.classList.add('visible');
    }
  };

  // If intro overlay exists, wait for fade-out or trigger after 1.5s
  if (introOverlay) {
    const observer = new MutationObserver(() => {
      if (introOverlay.classList.contains('fade-out')) {
        setTimeout(triggerHeroEntrance, 200);
      }
    });
    observer.observe(introOverlay, { attributes: true, attributeFilter: ['class'] });
  } else {
    triggerHeroEntrance();
  }
  // Fallback entrance trigger
  setTimeout(triggerHeroEntrance, 2500);

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Parallax on mouse move
  if (heroSection && heroVisual && heroLogoWrap && !prefersReducedMotion) {
    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;
    let isHovering = false;

    heroSection.addEventListener('mousemove', (e) => {
      const rect = heroSection.getBoundingClientRect();
      const relX = (e.clientX - rect.left) / rect.width - 0.5;
      const relY = (e.clientY - rect.top) / rect.height - 0.5;
      mouseX = relX * 22;
      mouseY = relY * 22;
      isHovering = true;
    });

    heroSection.addEventListener('mouseleave', () => {
      mouseX = 0;
      mouseY = 0;
      isHovering = false;
    });

    const animateParallax = () => {
      currentX += (mouseX - currentX) * 0.06;
      currentY += (mouseY - currentY) * 0.06;

      heroVisual.style.transform = `translate3d(${currentX.toFixed(2)}px, ${currentY.toFixed(2)}px, 0)`;
      heroLogoWrap.style.transform = `translate(-50%, -50%) translate3d(${(-currentX * 0.6).toFixed(2)}px, ${(-currentY * 0.6).toFixed(2)}px, 0)`;

      requestAnimationFrame(animateParallax);
    };

    requestAnimationFrame(animateParallax);
  }

  // Particle Canvas Animation
  if (particleCanvas && !prefersReducedMotion) {
    const ctx = particleCanvas.getContext('2d');
    let width = (particleCanvas.width = particleCanvas.offsetWidth || 420);
    let height = (particleCanvas.height = particleCanvas.offsetHeight || 420);

    const resizeCanvas = () => {
      if (!particleCanvas.offsetWidth) return;
      width = particleCanvas.width = particleCanvas.offsetWidth;
      height = particleCanvas.height = particleCanvas.offsetHeight;
    };

    window.addEventListener('resize', resizeCanvas);

    // Create subtle particles
    const particleCount = 28;
    const particles = [];
    const colors = [
      'rgba(184, 148, 90, 0.45)', // Earth gold
      'rgba(184, 148, 90, 0.25)',
      'rgba(15, 61, 46, 0.35)',   // Forest green
      'rgba(15, 61, 46, 0.2)'
    ];

    for (let i = 0; i < particleCount; i++) {
      const angle = Math.random() * Math.PI * 2;
      const radius = 40 + Math.random() * (width * 0.42);
      particles.push({
        x: width / 2 + Math.cos(angle) * radius,
        y: height / 2 + Math.sin(angle) * radius,
        baseRadius: radius,
        angle: angle,
        speed: (0.0015 + Math.random() * 0.0025) * (Math.random() > 0.5 ? 1 : -1),
        size: 1 + Math.random() * 2,
        color: colors[Math.floor(Math.random() * colors.length)],
        driftY: (Math.random() - 0.5) * 0.2
      });
    }

    const renderParticles = () => {
      ctx.clearRect(0, 0, width, height);

      const centerX = width / 2;
      const centerY = height / 2;

      particles.forEach((p) => {
        p.angle += p.speed;
        p.y += p.driftY;

        // Recalculate orbital drift
        p.x = centerX + Math.cos(p.angle) * p.baseRadius;
        p.y = centerY + Math.sin(p.angle) * (p.baseRadius * 0.75);

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
      });

      requestAnimationFrame(renderParticles);
    };

    renderParticles();
  }
});

