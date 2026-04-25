// Event Showcase: cursor, logo slideshow, expand, mute
// Source: COLLEGE-WEBSITE-main/js/navbar.js (Mounith)
(function () {
  const section   = document.querySelector('.event-showcase');
  if (!section) return;

  const cursor    = document.getElementById('esCursor');
  const muteBtn   = document.getElementById('esMute');
  const video     = document.getElementById('esVideo');
  const logos     = Array.from(section.querySelectorAll('.es__logo'));
  const dots      = section.querySelectorAll('.es__dot');

  let currentIdx   = 0;
  let slideTimer   = null;
  let expandedLogo = null;
  let isPaused     = false;

  // ── Custom cursor tracking ──
  const interactiveEls = section.querySelectorAll('.es__logo, .es__mute, .btn');

  function updateCursor(e) {
    const rect = section.getBoundingClientRect();
    cursor.style.left = (e.clientX - rect.left) + 'px';
    cursor.style.top  = (e.clientY - rect.top)  + 'px';
  }

  section.addEventListener('mousemove', updateCursor, { passive: true });
  section.addEventListener('mouseenter', () => section.classList.add('cursor-visible'));
  section.addEventListener('mouseleave', () => section.classList.remove('cursor-visible', 'cursor-shrink'));

  interactiveEls.forEach(el => {
    el.addEventListener('mouseenter', () => section.classList.add('cursor-shrink'));
    el.addEventListener('mouseleave', () => section.classList.remove('cursor-shrink'));
  });

  // ── Slideshow ──
  function showLogo(idx) {
    currentIdx = idx;
    logos.forEach((l, i) => {
      l.classList.toggle('is-active', i === idx);
    });
    dots.forEach(d => d.classList.toggle('is-active', d.dataset.index === String(idx)));
  }

  function advance() {
    if (isPaused || expandedLogo) return;
    showLogo((currentIdx + 1) % logos.length);
  }

  function startSlide() {
    clearInterval(slideTimer);
    slideTimer = setInterval(advance, 4000);
  }

  showLogo(0);
  startSlide();

  // ── Logo expand → centre ──
  function expandLogo(logo) {
    if (expandedLogo === logo) return;
    collapseLogo();
    isPaused = true;

    const idx   = logo.dataset.index;
    const img   = logo.querySelector('.es__logo-img');
    const panel = section.querySelector(`.es__panel[data-panel="${idx}"]`);
    const sRect = section.getBoundingClientRect();
    const iRect = img.getBoundingClientRect();

    const fromX = iRect.left + iRect.width  / 2 - sRect.left;
    const fromY = iRect.top  + iRect.height / 2 - sRect.top;
    const toX   = sRect.width  / 2;
    const toY   = sRect.height * 0.42;
    const dx    = toX - fromX;
    const dy    = toY - fromY;
    const scale = (sRect.width * 0.38) / iRect.width;

    img.style.transform = `translate(${dx}px, ${dy}px) scale(${scale})`;
    logo.classList.add('is-expanded');
    section.classList.add('logo-expanded');
    expandedLogo = logo;

    if (panel) setTimeout(() => panel.classList.add('is-visible'), 280);
    dots.forEach(d => d.classList.toggle('is-active', d.dataset.index === idx));
  }

  function collapseLogo() {
    if (!expandedLogo) return;
    const img   = expandedLogo.querySelector('.es__logo-img');
    const idx   = expandedLogo.dataset.index;
    const panel = section.querySelector(`.es__panel[data-panel="${idx}"]`);

    img.style.transform = '';
    expandedLogo.classList.remove('is-expanded');
    section.classList.remove('logo-expanded');
    if (panel) panel.classList.remove('is-visible');
    expandedLogo = null;
    isPaused = false;
    startSlide();
  }

  logos.forEach(logo => {
    logo.addEventListener('mouseenter', () => expandLogo(logo));
    logo.addEventListener('mouseleave', collapseLogo);
    logo.addEventListener('focus',      () => expandLogo(logo));
    logo.addEventListener('blur',       collapseLogo);
  });

  // ── Mute toggle ──
  if (muteBtn && video) {
    section.classList.add('is-muted');
    muteBtn.addEventListener('click', () => {
      video.muted = !video.muted;
      section.classList.toggle('is-muted', video.muted);
    });
  }
})();
