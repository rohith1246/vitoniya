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

  // 8. MNC Hero Reveal System
  const heroRevealElements = document.querySelectorAll('.hero-mnc .reveal');
  const triggerHeroEntrance = () => {
    heroRevealElements.forEach((el, index) => {
      setTimeout(() => {
        el.classList.add('visible');
      }, index * 120);
    });
  };

  if (introOverlay) {
    const observer = new MutationObserver(() => {
      if (introOverlay.classList.contains('fade-out')) {
        setTimeout(triggerHeroEntrance, 150);
      }
    });
    observer.observe(introOverlay, { attributes: true, attributeFilter: ['class'] });
  } else {
    triggerHeroEntrance();
  }
  setTimeout(triggerHeroEntrance, 2000);

  // 9. Kinetic Typography Rotator
  const kineticRotator = document.getElementById('kinetic-rotator');
  if (kineticRotator) {
    const phrases = [
      "Intelligent Digital Solutions.",
      "Enterprise AI Systems.",
      "Autonomous Workflow Engines.",
      "Distributed Cloud Platforms.",
      "Mission-Critical Software."
    ];
    let phraseIndex = 0;

    setInterval(() => {
      kineticRotator.classList.add('slide-out');
      setTimeout(() => {
        phraseIndex = (phraseIndex + 1) % phrases.length;
        kineticRotator.textContent = phrases[phraseIndex];
        kineticRotator.classList.remove('slide-out');
        kineticRotator.classList.add('slide-in');
        setTimeout(() => {
          kineticRotator.classList.remove('slide-in');
        }, 350);
      }, 350);
    }, 3600);
  }

  // 10. Interactive 3D Holographic Core (Three.js with 3D Canvas Fallback)
  const canvas3D = document.getElementById('hero-3d-canvas');
  const stage3D = document.getElementById('hero-3d-stage');
  const consoleCard = document.getElementById('console-card');
  const hudCoords = document.getElementById('hud-coords');
  const consoleFps = document.getElementById('console-fps');

  if (canvas3D && stage3D) {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Interaction State
    let targetRotationX = 0.2;
    let targetRotationY = 0.3;
    let currentRotationX = 0.2;
    let currentRotationY = 0.3;
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;

    // Mouse / Touch Drag Tracking
    const onPointerDown = (e) => {
      isDragging = true;
      prevMouseX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
      prevMouseY = e.clientY || (e.touches && e.touches[0].clientY) || 0;
    };

    const onPointerMove = (e) => {
      const clientX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
      const clientY = e.clientY || (e.touches && e.touches[0].clientY) || 0;

      if (isDragging) {
        const deltaX = clientX - prevMouseX;
        const deltaY = clientY - prevMouseY;
        targetRotationY += deltaX * 0.008;
        targetRotationX += deltaY * 0.008;
        prevMouseX = clientX;
        prevMouseY = clientY;
      } else {
        // Subtle tilt on hover
        const rect = window.innerWidth;
        const normX = (clientX / rect - 0.5) * 2;
        targetRotationY = normX * 0.4 + 0.3;
      }

      // Update HUD telemetry coordinates based on rotation
      if (hudCoords) {
        const lat = (17.3850 + currentRotationX * 1.5).toFixed(4);
        const lng = (78.4867 + currentRotationY * 1.5).toFixed(4);
        hudCoords.textContent = `${lat}° N, ${lng}° E`;
      }
    };

    const onPointerUp = () => {
      isDragging = false;
    };

    window.addEventListener('mousemove', onPointerMove, { passive: true });
    window.addEventListener('mouseup', onPointerUp);
    if (consoleCard) {
      consoleCard.addEventListener('mousedown', onPointerDown);
      consoleCard.addEventListener('touchstart', onPointerDown, { passive: true });
    }
    stage3D.addEventListener('mousedown', onPointerDown);
    stage3D.addEventListener('touchstart', onPointerDown, { passive: true });
    window.addEventListener('touchmove', onPointerMove, { passive: true });
    window.addEventListener('touchend', onPointerUp);

    // Check if Three.js is loaded
    if (typeof THREE !== 'undefined' && !prefersReducedMotion) {
      try {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, stage3D.offsetWidth / stage3D.offsetHeight, 0.1, 1000);
        camera.position.z = 7;

        const renderer = new THREE.WebGLRenderer({
          canvas: canvas3D,
          alpha: true,
          antialias: true,
          powerPreference: 'high-performance'
        });
        renderer.setSize(stage3D.offsetWidth, stage3D.offsetHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        // Group containing all 3D components
        const coreGroup = new THREE.Group();
        scene.add(coreGroup);

        // 1. Geodesic Sphere Wireframe (Forest Green)
        const sphereGeo = new THREE.IcosahedronGeometry(2.4, 2);
        const wireMat = new THREE.MeshBasicMaterial({
          color: 0x0F3D2E,
          wireframe: true,
          transparent: true,
          opacity: 0.28
        });
        const sphereMesh = new THREE.Mesh(sphereGeo, wireMat);
        coreGroup.add(sphereMesh);

        // 2. Vertex Points (Earth Gold Glow)
        const pointsMat = new THREE.PointsMaterial({
          color: 0xB8945A,
          size: 0.08,
          transparent: true,
          opacity: 0.85
        });
        const pointsMesh = new THREE.Points(sphereGeo, pointsMat);
        coreGroup.add(pointsMesh);

        // 3. Inner Rotating Torus Knot (Technical Parametric Core)
        const knotGeo = new THREE.TorusKnotGeometry(1.2, 0.22, 64, 12, 2, 3);
        const knotMat = new THREE.MeshBasicMaterial({
          color: 0xB8945A,
          wireframe: true,
          transparent: true,
          opacity: 0.35
        });
        const knotMesh = new THREE.Mesh(knotGeo, knotMat);
        coreGroup.add(knotMesh);

        // 4. Subtle Orbital Data Rings
        const ringGeo = new THREE.RingGeometry(3.0, 3.03, 64);
        const ringMat = new THREE.MeshBasicMaterial({
          color: 0x0F3D2E,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.15
        });
        const ring1 = new THREE.Mesh(ringGeo, ringMat);
        ring1.rotation.x = Math.PI / 3;
        coreGroup.add(ring1);

        const ring2 = new THREE.Mesh(ringGeo, ringMat);
        ring2.rotation.y = Math.PI / 4;
        coreGroup.add(ring2);

        // Resize handler
        const onResize = () => {
          if (!stage3D.offsetWidth) return;
          camera.aspect = stage3D.offsetWidth / stage3D.offsetHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(stage3D.offsetWidth, stage3D.offsetHeight);
        };
        window.addEventListener('resize', onResize);

        // Animation loop
        let lastTime = performance.now();
        let frameCount = 0;
        let fpsTimer = performance.now();

        const animate3D = (time) => {
          requestAnimationFrame(animate3D);

          // Calculate FPS
          frameCount++;
          if (time - fpsTimer >= 1000) {
            if (consoleFps) {
              consoleFps.textContent = `${frameCount} FPS`;
            }
            frameCount = 0;
            fpsTimer = time;
          }

          // Smooth lerp rotation
          currentRotationX += (targetRotationX - currentRotationX) * 0.05;
          currentRotationY += (targetRotationY - currentRotationY) * 0.05;

          // Continuous gentle auto-spin
          targetRotationY += 0.0012;

          coreGroup.rotation.x = currentRotationX;
          coreGroup.rotation.y = currentRotationY;

          // Counter-rotate inner knot for multi-axis depth
          knotMesh.rotation.x -= 0.002;
          knotMesh.rotation.y += 0.003;

          renderer.render(scene, camera);
        };

        requestAnimationFrame(animate3D);
      } catch (err) {
        console.warn('WebGL init fallback:', err);
        initCanvasFallback();
      }
    } else {
      initCanvasFallback();
    }

    // High-performance 2D Canvas 3D Projection Engine Fallback
    function initCanvasFallback() {
      const ctx = canvas3D.getContext('2d');
      let w = (canvas3D.width = stage3D.offsetWidth || 500);
      let h = (canvas3D.height = stage3D.offsetHeight || 500);

      window.addEventListener('resize', () => {
        w = canvas3D.width = stage3D.offsetWidth || 500;
        h = canvas3D.height = stage3D.offsetHeight || 500;
      });

      // Generate 3D sphere points
      const numPoints = 140;
      const points = [];
      for (let i = 0; i < numPoints; i++) {
        const phi = Math.acos(-1 + (2 * i) / numPoints);
        const theta = Math.sqrt(numPoints * Math.PI) * phi;
        points.push({
          x: Math.cos(theta) * Math.sin(phi),
          y: Math.sin(theta) * Math.sin(phi),
          z: Math.cos(phi)
        });
      }

      const renderFallback = () => {
        ctx.clearRect(0, 0, w, h);
        const cx = w * 0.55;
        const cy = h * 0.5;
        const radius = Math.min(w, h) * 0.32;

        currentRotationX += (targetRotationX - currentRotationX) * 0.05;
        currentRotationY += (targetRotationY - currentRotationY) * 0.05;
        targetRotationY += 0.002;

        const cosY = Math.cos(currentRotationY);
        const sinY = Math.sin(currentRotationY);
        const cosX = Math.cos(currentRotationX);
        const sinX = Math.sin(currentRotationX);

        const projected = points.map((p) => {
          // Rotate Y
          const x1 = p.x * cosY - p.z * sinY;
          const z1 = p.z * cosY + p.x * sinY;
          // Rotate X
          const y2 = p.y * cosX - z1 * sinX;
          const z2 = z1 * cosX + p.y * sinX;

          const scale = 300 / (300 + z2 * radius);
          return {
            px: cx + x1 * radius * scale,
            py: cy + y2 * radius * scale,
            z: z2,
            scale: scale
          };
        });

        // Draw connecting wireframe lines
        ctx.strokeStyle = 'rgba(15, 61, 46, 0.12)';
        ctx.lineWidth = 0.8;
        for (let i = 0; i < projected.length; i++) {
          for (let j = i + 1; j < projected.length; j++) {
            const dx = projected[i].px - projected[j].px;
            const dy = projected[i].py - projected[j].py;
            const dist = dx * dx + dy * dy;
            if (dist < 2200) {
              ctx.beginPath();
              ctx.moveTo(projected[i].px, projected[i].py);
              ctx.lineTo(projected[j].px, projected[j].py);
              ctx.stroke();
            }
          }
        }

        // Draw node points
        projected.forEach((p) => {
          const alpha = (p.z + 1) * 0.45;
          ctx.beginPath();
          ctx.arc(p.px, p.py, 2.5 * p.scale, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(184, 148, 90, ${Math.max(0.15, alpha)})`;
          ctx.fill();
        });

        requestAnimationFrame(renderFallback);
      };

      renderFallback();
    }
  }
});

