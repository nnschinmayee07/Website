// ═══════════════════════════════════════════════════════════════
// WHY MLRIT — Scroll-based video autoplay + fade-in
// ═══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  const section = document.getElementById('why-mlrit');
  const video = document.getElementById('whyVideo');

  if (!section || !video) return;

  // Dynamic "Years of Excellence" stat
  var yearsEl = document.getElementById('mlritYears');
  if (yearsEl) {
    var years = new Date().getFullYear() - 2005;
    yearsEl.innerHTML = years + '<span class="why-stat__unit">+</span>';
  }
})();
