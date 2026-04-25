// Programs tab toggle
// Source: COLLEGE-WEBSITE-main/index.html (Mounith)
const tabBtns = document.querySelectorAll('.tab-btn');
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

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
