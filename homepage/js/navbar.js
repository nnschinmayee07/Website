/* =============================================
   NAVBAR — keyboard accessibility + click outside
   ============================================= */
(function () {
  const items = Array.from(document.querySelectorAll('.main-nav__item'));

  // Keyboard: Enter/Space opens, Escape closes
  items.forEach(item => {
    const link     = item.querySelector('.main-nav__link');
    const dropdown = item.querySelector('.dropdown, .support-panel');
    if (!link || !dropdown) return;

    link.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const isOpen = item.classList.contains('is-open');
        closeAll();
        if (!isOpen) item.classList.add('is-open');
      }
      if (e.key === 'Escape') closeAll();
    });
  });

  function closeAll() {
    items.forEach(i => i.classList.remove('is-open'));
  }

  // Close dropdowns on click outside
  document.addEventListener('click', e => {
    if (!e.target.closest('.main-nav__item')) closeAll();
  });

  // Prevent navigation on # links
  document.querySelectorAll('.main-nav__link').forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href === '#') {
        e.preventDefault();
      }
    });
  });
})();
