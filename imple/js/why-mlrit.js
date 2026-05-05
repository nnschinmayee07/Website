// ── Why MLRIT: slide-in video on scroll ───────────────────────────────
(function () {
  var el = document.querySelector('.why-section__right');
  if (!el) return;

  var obs = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) {
      el.classList.add('is-visible');
      obs.disconnect();
    }
  }, { threshold: 0.15 });

  obs.observe(el);
})();
