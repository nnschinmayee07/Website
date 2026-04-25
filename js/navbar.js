// Keyboard accessibility: open dropdown on Enter/Space, close on Escape
document.querySelectorAll('.main-nav__item').forEach(item => {
  const link = item.querySelector('.main-nav__link');
  const dropdown = item.querySelector('.dropdown');
  if (!dropdown) return;

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
  document.querySelectorAll('.main-nav__item.is-open')
    .forEach(i => i.classList.remove('is-open'));
}

document.addEventListener('click', e => {
  if (!e.target.closest('.main-nav__item')) closeAll();
});

document.querySelectorAll('.main-nav__link').forEach(link => {
  link.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (!href || href === '#') {
      e.preventDefault();
    }
  });
});
