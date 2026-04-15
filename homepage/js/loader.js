// ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
// SECTION LOADER ??? Fail-safe dynamic section injection
// Sections live in /sections/*.html ??? NEVER in index.html
// ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

const loadSection = async (id, file, callback) => {
  try {
    const res = await fetch(file);
    if (!res.ok) throw new Error(`HTTP ${res.status} ??? Failed to load ${file}`);
    const html = await res.text();
    const container = document.getElementById(id);
    if (!container) throw new Error(`Container #${id} not found in DOM`);
    container.innerHTML = html;
    if (callback) callback();
  } catch (err) {
    console.error(`SECTION LOAD ERROR: ${id}`, err);
  }
};

// ?????? Why MLRIT init ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
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
  var section    = document.getElementById('events');
  var bgVideo    = document.getElementById('evBgVideo');
  var evText     = document.getElementById('evText');
  var evQuote    = document.getElementById('evQuote');
  var evName     = document.getElementById('evName');
  var evRole     = document.getElementById('evRole');
  var mainThumb  = document.getElementById('evMainThumb');
  var muteBtn    = document.getElementById('evMuteBtn');
  var evExplore  = document.getElementById('evExplore');
  var miniThumbs = document.querySelectorAll('.ev-mini-thumb');

  if (!section || !bgVideo) return;

  // ── Explore prompt: center when out of view, settle to top-left when scrolled into view ──
  if (evExplore) {
    var exploreIO = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        evExplore.classList.add('is-settled');
      } else {
        evExplore.classList.remove('is-settled');
      }
    }, { threshold: 0.15 });
    exploreIO.observe(section);
  }

  // Ensure all mini-thumb videos are paused (thumbnail only)
  document.querySelectorAll('.ev-mini-thumb video').forEach(function (v) {
    v.pause();
  });

  var events = [
    { src: 'events/e1.mp4', quote: 'A celebration of technical brilliance and innovation that defines the spirit of MLRIT.', name: 'Zignasa',      role: 'Technical Fest'      },
    { src: 'events/e2.mp4', quote: 'Where bold ideas meet real-world challenges — students push boundaries and build solutions.', name: 'IC',       role: 'Innovation Challenge' },
    { src: 'events/e3.mp4', quote: 'The annual championship that brings out the best engineers, thinkers, and creators on campus.', name: 'Zenith', role: 'Technical Fest'      },
    { src: 'events/e4.mp4', quote: 'A vibrant cultural extravaganza that celebrates art, music, dance, and the soul of MLRIT.', name: 'Navrat Naveli', role: 'Cultural Fest'   }
  ];

  var current = 0;
  var isMuted = true;

  // ── INITIAL STATE: load first video, blurred, NOT playing ──
  bgVideo.src    = events[0].src;
  bgVideo.muted  = isMuted;
  bgVideo.load();
  // Do NOT call play() here — video visible but paused

  if (evQuote) evQuote.textContent = '\u201c' + events[0].quote + '\u201d';
  if (evName)  evName.textContent  = events[0].name;
  if (evRole)  evRole.textContent  = events[0].role;

  // ── Select event by index ──
  function selectEvent(i) {
    if (i < 0 || i >= events.length) return;

    // Stop any mini-thumb preview videos
    document.querySelectorAll('.ev-mini-thumb video').forEach(function (v) {
      v.pause();
      v.currentTime = 0;
    });

    // Update bg video source — do NOT play, do NOT change blur
    bgVideo.pause();
    bgVideo.src   = events[i].src;
    bgVideo.muted = isMuted;
    bgVideo.load();

    // Update text
    if (evQuote) evQuote.textContent = '\u201c' + events[i].quote + '\u201d';
    if (evName)  evName.textContent  = events[i].name;
    if (evRole)  evRole.textContent  = events[i].role;

    // Update active state
    miniThumbs.forEach(function (th, j) { th.classList.toggle('is-active', j === i); });
    current = i;
  }

  // ── Mini-thumb — selection only ──
  miniThumbs.forEach(function (t, i) {
    t.addEventListener('mouseenter', function () { selectEvent(i); });
    t.addEventListener('click', function () { selectEvent(i); });
  });

  // ── TASK 5: Main thumb hover — play bg video, remove blur, hide overlay ──
  if (mainThumb) {
    mainThumb.addEventListener('mouseenter', function () {
      // Ensure mini-thumb preview does NOT play
      var preview = mainThumb.querySelector('video');
      if (preview) { preview.pause(); preview.currentTime = 0; }

      // Play background video
      bgVideo.play().catch(function () {});

      // Remove blur
      bgVideo.style.filter = 'blur(0px)';

      // Hide overlay text
      if (evText) evText.style.opacity = '0';
    });

    // ── TASK 6: Mouse leave — pause, restore blur, show overlay ──
    mainThumb.addEventListener('mouseleave', function () {
      bgVideo.pause();
      bgVideo.style.filter = 'blur(12px)';
      if (evText) evText.style.opacity = '1';
    });
  }

  // ── Prev / Next ──
  var btnPrev = document.getElementById('evPrev');
  var btnNext = document.getElementById('evNext');
  if (btnPrev) btnPrev.addEventListener('click', function () {
    selectEvent(((current - 1) % events.length + events.length) % events.length);
  });
  if (btnNext) btnNext.addEventListener('click', function () {
    selectEvent((current + 1) % events.length);
  });

  // ── Touch swipe ──
  var touchX = 0;
  section.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
  section.addEventListener('touchend',   function (e) {
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) {
      selectEvent(dx < 0 ? (current + 1) % events.length : ((current - 1) % events.length + events.length) % events.length);
    }
  });

  // ── Mute toggle ──
  if (muteBtn) {
    muteBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      isMuted = !isMuted;
      bgVideo.muted = isMuted;
      document.querySelectorAll('.alumni-video').forEach(function (v) { v.muted = isMuted; });
      var off = muteBtn.querySelector('.ev-mute-btn__off');
      var on  = muteBtn.querySelector('.ev-mute-btn__on');
      if (off) off.style.display = isMuted ? '' : 'none';
      if (on)  on.style.display  = isMuted ? 'none' : '';
    });
  }
}

// ?????? Boot ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
const init = () => {
  initRankings();
  initWhyMLRIT();
  initEvents();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
