// ═══════════════════════════════════════════════════════════════
// SUCCESS STORIES — Scroll reveal + delayed belt start
// ═══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  const section = document.querySelector('.ss-section');
  if (!section) return;

  const track = document.querySelector('.ss-track');

  // Reveal all cards (including aria-hidden duplicates) once section enters view
  // Using section-level observer — not per-card — avoids issues with
  // off-screen duplicates never intersecting
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        section.querySelectorAll('.ss-card').forEach((card) => {
          card.classList.add('is-revealed');
        });
        // Start belt after 350ms — .is-playing enables animation-play-state: running
        if (track) {
          setTimeout(function () {
            track.classList.add('is-playing');
          }, 350);
        }
        observer.disconnect();
      }
    },
    { threshold: 0.1 }
  );

  observer.observe(section);
})();
