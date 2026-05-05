// Programs tab toggle — switches between UG and PG grids
(function () {
  var tabBtns = document.querySelectorAll('.tab-btn');
  var ugGrid  = document.getElementById('ug-grid');
  var pgGrid  = document.getElementById('pg-grid');
  if (!tabBtns.length || !ugGrid || !pgGrid) return;

  tabBtns.forEach(function (btn, idx) {
    btn.addEventListener('click', function () {
      tabBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');

      if (idx === 0) {
        ugGrid.style.display = '';
        pgGrid.style.display = 'none';
      } else {
        ugGrid.style.display = 'none';
        pgGrid.style.display = '';
        /* trigger reveal animation for PG grid on first show */
        requestAnimationFrame(function () {
          pgGrid.classList.add('is-visible');
        });
      }
    });
  });
})();

// Scroll-triggered reveal (IntersectionObserver)
// Source: COLLEGE-WEBSITE-main/js/navbar.js (Mounith)
(function () {
  const els = document.querySelectorAll('.reveal, .reveal-stagger, .reveal-left');
  if (!els.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  els.forEach(el => obs.observe(el));
})();
