// ═══════════════════════════════════════════════════════════════
// SECTION LOADER — Fail-safe dynamic section injection
// Sections live in /sections/*.html — NEVER in index.html
// ═══════════════════════════════════════════════════════════════

const loadSection = async (id, file, callback) => {
  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(`HTTP ${res.status} — Failed to load ${file}`);
    const html = await res.text();
    const container = document.getElementById(id);
    if (!container) throw new Error(`Container #${id} not found in DOM`);
    container.innerHTML = html;
    if (callback) callback();
  } catch (err) {
    console.error(`SECTION LOAD ERROR: ${id}`, err);
  }
};

// ── Why MLRIT init ──────────────────────────────────────────────
function initWhyMLRIT() {
  const section = document.getElementById('why-mlrit');
  const vid     = document.getElementById('whyVideo');
  const muteBtn = document.getElementById('whyMute');

  if (!section || !vid) return;

  // Scroll-based autoplay
  const io = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      vid.play().catch(() => {});
      vid.classList.add('is-playing');
    } else {
      vid.pause();
      vid.classList.remove('is-playing');
    }
  }, { threshold: 0.4 });
  io.observe(section);

  // Mute toggle
  if (muteBtn) {
    const off = muteBtn.querySelector('.vid-mute-btn__off');
    const on  = muteBtn.querySelector('.vid-mute-btn__on');
    muteBtn.addEventListener('click', e => {
      e.stopPropagation();
      vid.muted = !vid.muted;
      if (off) off.style.display = vid.muted ? '' : 'none';
      if (on)  on.style.display  = vid.muted ? 'none' : '';
    });
  }
}

// ── Events init ─────────────────────────────────────────────────
function initEvents() {
  var section   = document.getElementById('events');
  var bgVideo   = document.getElementById('evBgVideo');
  var bgScrim   = document.querySelector('.ev-bg-scrim');
  var beam      = document.getElementById('evBeam');
  var tagline   = document.getElementById('evTagline');
  var content   = document.getElementById('evContent');
  var evText    = document.getElementById('evText');
  var evQuote   = document.getElementById('evQuote');
  var evName    = document.getElementById('evName');
  var evRole    = document.getElementById('evRole');
  var mainThumb = document.getElementById('evMainThumb');
  var thumbVid  = document.getElementById('evThumbVid');
  var muteBtn   = document.getElementById('evMuteBtn');
  var miniThumbs = document.querySelectorAll('.ev-mini-thumb');
  if (!section || !bgVideo) return;

  var events = [
    { src: 'events/e1.mp4', quote: 'A celebration of technical brilliance and innovation that defines the spirit of MLRIT.', name: 'Zignasa', role: 'Technical Fest' },
    { src: 'events/e2.mp4', quote: 'Where bold ideas meet real-world challenges — students push boundaries and build solutions.', name: 'IC', role: 'Innovation Challenge' },
    { src: 'events/e3.mp4', quote: 'The annual championship that brings out the best engineers, thinkers, and creators on campus.', name: 'Zenith', role: 'Technical Fest' },
    { src: 'events/e4.mp4', quote: "A vibrant cultural extravaganza that celebrates art, music, dance, and the soul of MLRIT.", name: 'Navrat Naveli', role: 'Cultural Fest' }
  ];

  var current = 0;
  var isMuted = true;

  function goTo(idx) {
    current = ((idx % events.length) + events.length) % events.length;
    var ev = events[current];
    bgVideo.src = ev.src; bgVideo.muted = isMuted; bgVideo.load(); bgVideo.play().catch(function(){});
    if (thumbVid) { thumbVid.src = ev.src; thumbVid.muted = isMuted; thumbVid.load(); thumbVid.play().catch(function(){}); }
    if (evQuote) evQuote.textContent = '\u201c' + ev.quote + '\u201d';
    if (evName)  evName.textContent  = ev.name;
    if (evRole)  evRole.textContent  = ev.role;
    miniThumbs.forEach(function(t, i) {
      t.classList.toggle('is-active', i === current);
    });
  }

  // Fallback src — assign first mini-thumb video src if bgVideo has none
  var firstThumbVid = miniThumbs[0] ? miniThumbs[0].querySelector('video') : null;
  if (firstThumbVid && !bgVideo.getAttribute('src')) {
    var fallbackSrc = firstThumbVid.getAttribute('src') || firstThumbVid.currentSrc;
    if (fallbackSrc) { bgVideo.src = fallbackSrc; bgVideo.muted = true; bgVideo.load(); bgVideo.play().catch(function(){}); }
  }

  miniThumbs.forEach(function(t, i) {
    t.addEventListener('mouseenter', function() {
      // 1. Stop ALL mini-thumb videos — never let preview play
      document.querySelectorAll('.ev-mini-thumb video').forEach(function(v) {
        v.pause();
        v.currentTime = 0;
      });

      // 2. Switch background video using attribute src (reliable, avoids absolute vs relative mismatch)
      var vid = t.querySelector('video');
      var newSrc = vid ? vid.getAttribute('src') : null;
      if (!newSrc) return;

      bgVideo.pause();
      bgVideo.src = newSrc;
      bgVideo.muted = isMuted;
      bgVideo.load();

      // 3. Play background video
      bgVideo.play().catch(function() {});

      // 4. Remove blur
      bgVideo.style.filter = 'blur(0px)';
      bgVideo.style.opacity = '1';
      if (evText) evText.classList.add('is-hidden');
    });

    t.addEventListener('mouseleave', function() {
      bgVideo.pause();
      bgVideo.style.filter = '';        /* restores CSS default: blur(12px) */
      bgVideo.style.opacity = '1';
      if (evText) evText.classList.remove('is-hidden');
    });

    t.addEventListener('click', function() { goTo(i); });
  });

  var btnPrev = document.getElementById('evPrev');
  var btnNext = document.getElementById('evNext');
  if (btnPrev) btnPrev.addEventListener('click', function() { goTo(current - 1); });
  if (btnNext) btnNext.addEventListener('click', function() { goTo(current + 1); });

  var touchX = 0;
  section.addEventListener('touchstart', function(e) { touchX = e.touches[0].clientX; }, { passive: true });
  section.addEventListener('touchend', function(e) {
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) goTo(dx < 0 ? current + 1 : current - 1);
  });

  if (muteBtn) {
    muteBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      isMuted = !isMuted;
      bgVideo.muted = isMuted;
      if (thumbVid) thumbVid.muted = isMuted;
      document.querySelectorAll('.alumni-video').forEach(function(v) { v.muted = isMuted; });
      var off = muteBtn.querySelector('.ev-mute-btn__off');
      var on  = muteBtn.querySelector('.ev-mute-btn__on');
      if (off) off.style.display = isMuted ? '' : 'none';
      if (on)  on.style.display  = isMuted ? 'none' : '';
    });
  }

  var introTimers = [];
  function resetIntro() {
    introTimers.forEach(clearTimeout); introTimers = [];
    section.classList.remove('is-visible');
    if (beam)    { beam.classList.remove('is-firing'); void beam.offsetWidth; }
    if (tagline) { tagline.classList.remove('is-hero','is-visible','is-settled'); void tagline.offsetWidth; }
    if (content) content.classList.remove('is-ready');
    bgVideo.pause();
    if (thumbVid) thumbVid.pause();
    current = 0;
  }

  function runIntro() {
    section.classList.add('is-visible');
    // Start bg video playing (blurred) from intro start
    bgVideo.muted = isMuted;
    bgVideo.play().catch(function(){});
    console.log('[Events] runIntro — bgVideo src:', bgVideo.src);
    introTimers.push(setTimeout(function() {
      if (tagline) {
        tagline.classList.add('is-hero');
        requestAnimationFrame(function() { requestAnimationFrame(function() { if (tagline) tagline.classList.add('is-visible'); }); });
      }
    }, 500));
    introTimers.push(setTimeout(function() {
      if (beam) { void beam.offsetWidth; beam.classList.add('is-firing'); }
    }, 900));
    introTimers.push(setTimeout(function() {
      if (tagline) tagline.classList.add('is-settled');
    }, 1600));
    introTimers.push(setTimeout(function() {
      if (content) content.classList.add('is-ready');
      goTo(0);
    }, 2800));
  }

  var io = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
      resetIntro();
      requestAnimationFrame(function() { requestAnimationFrame(runIntro); });
    }
  }, { threshold: 0.4 });
  io.observe(section);

}

// ── Boot ────────────────────────────────────────────────────────
const init = () => {
  loadSection('accreditations-slot', 'sections/accreditations.html');
  loadSection('why-mlrit-slot',      'sections/why-mlrit.html',      initWhyMLRIT);
  loadSection('events-slot',         'sections/events.html',         initEvents);
};

document.addEventListener('DOMContentLoaded', init);
