// ═══════════════════════════════════════════════════════════════
// RANKINGS SECTION — Count-up animations + hover effects
// ═══════════════════════════════════════════════════════════════

function initRankings() {
  'use strict';

  const section = document.querySelector('.achievements');
  if (!section) return;

  // Parse rank numbers
  const rankItems = section.querySelectorAll('.rank-row__num');
  const ranks = Array.from(rankItems).map(el => {
    const raw = el.textContent.trim();
    // Handle numeric (201) or alphanumeric (AAAA, #6)
    const isNumeric = /^\d+$/.test(raw);
    return { el, raw, isNumeric, value: isNumeric ? parseInt(raw, 10) : 0 };
  });

  // Easing function
  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  // Animate a single rank
  function animateRank(rank, delay) {
    if (!rank.isNumeric) return; // Skip non-numeric ranks

    setTimeout(() => {
      const duration = 1500;
      const start = performance.now();

      function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeOutQuart(progress);
        const current = Math.round(eased * rank.value);

        rank.el.textContent = current;

        if (progress < 1) {
          requestAnimationFrame(tick);
        } else {
          rank.el.textContent = rank.raw; // Restore original
        }
      }

      requestAnimationFrame(tick);
    }, delay);
  }

  // Run once when section enters viewport
  const observer = new IntersectionObserver(
    (entries) => {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();

      ranks.forEach((rank, i) => {
        if (rank.isNumeric) {
          rank.el.textContent = '0';
          animateRank(rank, i * 150);
        }
      });
    },
    { threshold: 0.3 }
  );

  observer.observe(section);
}
