// ═══════════════════════════════════════════════════════════════
// PLACEMENTS — Count-up animations for stats
// ═══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  const section = document.getElementById('placements');
  if (!section) return;

  const items = section.querySelectorAll('.placement-stat__num');
  const stats = Array.from(items).map(el => {
    const unit = el.querySelector('.unit');
    const raw = el.childNodes[0] ? el.childNodes[0].textContent.trim() : '';
    const num = parseFloat(raw);
    return { el, num, unit };
  });

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function animateStat(stat, delay) {
    setTimeout(() => {
      const duration = 1500;
      const start = performance.now();

      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const current = Math.round(easeOutCubic(progress) * stat.num);

        if (stat.el.childNodes[0] && stat.el.childNodes[0].nodeType === Node.TEXT_NODE) {
          stat.el.childNodes[0].textContent = current;
        }

        if (progress < 1) {
          requestAnimationFrame(tick);
        }
      }

      requestAnimationFrame(tick);
    }, delay);
  }

  const observer = new IntersectionObserver(
    (entries) => {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();

      stats.forEach((stat, i) => {
        if (stat.el.childNodes[0] && stat.el.childNodes[0].nodeType === Node.TEXT_NODE) {
          stat.el.childNodes[0].textContent = '0';
        }
        animateStat(stat, i * 120);
      });
    },
    { threshold: 0.4 }
  );

  observer.observe(section);
})();
