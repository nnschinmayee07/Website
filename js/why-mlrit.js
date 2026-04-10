// ═══════════════════════════════════════════════════════════════
// WHY MLRIT — Scroll-based video autoplay + fade-in
// ═══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  const section = document.getElementById('why-mlrit');
  const video = document.getElementById('whyVideo');

  if (!section || !video) return;

  // Scroll-based autoplay
  const playObserver = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        video.play().catch(() => {});
        video.classList.add('is-playing');
      } else {
        video.pause();
        video.classList.remove('is-playing');
      }
    },
    { threshold: 0.5 }
  );

  playObserver.observe(section);

  // Full-section reveal + content pull-in
  const left = section.querySelector('.why-section__left');
  const right = section.querySelector('.why-section__right');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reducedMotion) {
    // Show everything immediately — no animation
    section.classList.add('is-revealed');
    if (left) left.classList.add('is-visible');
    if (right) right.classList.add('is-visible');
  } else {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          // Phase 1: reveal the section shell
          section.classList.add('is-revealed');
          // Phase 2: content slides in (CSS transition-delay handles the stagger)
          if (left) left.classList.add('is-visible');
          if (right) right.classList.add('is-visible');
          revealObserver.unobserve(section);
        }
      },
      { threshold: 0.05, rootMargin: '0px 0px -20px 0px' }
    );

    revealObserver.observe(section);
  }
})();
