// ═══════════════════════════════════════════════════════════════
// ALUMNI — Exact sequence: sweep (0–200ms) → overlay (200–240ms) → video (250ms+)
// Video visibility is JS-controlled (no CSS transition = no fade delay)
// ═══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  document.querySelectorAll('.alumni-card').forEach(function (card) {
    var vid = card.querySelector('.alumni-card__video');
    if (!vid) return;

    var playTimer = null;

    card.addEventListener('mouseenter', function () {
      // Sweep completes at 200ms, overlay fully opaque by ~240ms.
      // Fire at 250ms — no overlap, no early play.
      playTimer = setTimeout(function () {
        vid.style.opacity = '1';
        vid.currentTime = 0;
        vid.play().catch(function () {});
      }, 250);
    });

    card.addEventListener('mouseleave', function () {
      clearTimeout(playTimer);
      vid.pause();
      vid.style.opacity = '0';
    });
  });
})();
