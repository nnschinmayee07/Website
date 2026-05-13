// ── Event Showcase — auto-cycling info · cursor · mute ──
(function () {
  var section  = document.querySelector('.event-showcase');
  if (!section) return;

  var video    = document.getElementById('esVideo');
  var cursor   = document.getElementById('esCursor');
  var muteBtn  = document.getElementById('esMute');
  var nextBtn  = document.getElementById('esNext');
  var infoWrap = document.querySelector('.es__info-inner');
  var logoImg  = document.getElementById('esInfoLogo');
  var tagEl    = document.getElementById('esInfoTag');
  var titleEl  = document.getElementById('esInfoTitle');
  var descEl   = document.getElementById('esInfoDesc');
  var dots     = document.querySelectorAll('.es__dot');

  // ── Event data ──
  var events = [
    {
      video: 'https://res.cloudinary.com/dhqhhtvym/video/upload/v1777366731/equinox.mp4',
      logo:  'assets/logo.svg',
      tag:   'Entrepreneurship Summit \u00b7 2024',
      title: 'The Equinox<br>E-Summit 2K24',
      desc:  "MLRIT\u2019s flagship annual summit bringing together entrepreneurs, investors, and innovators to inspire the next generation of leaders."
    },
    {
      type:  'embed',
      embed: 'https://www.instagram.com/reel/DRrMiTKjP8w/embed/',
      logo:  'assets/main-logo.svg',
      tag:   'Technical & Cultural Fest \u00b7 2025',
      title: 'Zignasa<br>2025',
      desc:  "MLRIT\u2019s grand annual extravaganza featuring technical competitions, hackathons, cultural performances, and celebrity nights."
    }
  ];

  var current = 0;
  var embed = document.getElementById('esEmbed');

  // ── Switch event with crossfade ──
  function goTo(idx) {
    if (idx === current) return;
    idx = (idx + events.length) % events.length;

    // Fade out
    if (infoWrap) infoWrap.classList.add('es-fading');

    setTimeout(function () {
      var ev = events[idx];

      // Swap media — video or Instagram embed
      if (ev.type === 'embed') {
        if (video) { video.pause(); video.style.display = 'none'; }
        if (embed) { embed.src = ev.embed; embed.style.display = 'block'; }
      } else {
        if (embed) { embed.src = ''; embed.style.display = 'none'; }
        if (video) {
          video.style.display = 'block';
          var src = video.querySelector('source');
          if (src) src.setAttribute('src', ev.video);
          video.load();
          video.play().catch(function () {});
        }
      }

      if (logoImg)  logoImg.src = ev.logo;
      if (tagEl)    tagEl.textContent = ev.tag;
      if (titleEl)  titleEl.innerHTML = ev.title;
      if (descEl)   descEl.textContent = ev.desc;

      // Update dots
      dots.forEach(function (d) { d.classList.remove('is-active'); });
      if (dots[idx]) dots[idx].classList.add('is-active');

      current = idx;

      // Fade in
      if (infoWrap) infoWrap.classList.remove('es-fading');
    }, 400);
  }

  // ── Next button ──
  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      goTo(current + 1);
    });
  }

  // ── Dot click navigation ──
  dots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      var idx = parseInt(dot.dataset.index, 10);
      goTo(idx);
    });
  });

  // ── 2. Custom cursor — only show after first mouse move ──
  var cursorX = 0, cursorY = 0, hasMoved = false, raf;

  function moveCursor() {
    if (cursor) {
      cursor.style.left = cursorX + 'px';
      cursor.style.top  = cursorY + 'px';
    }
    raf = requestAnimationFrame(moveCursor);
  }

  section.addEventListener('mousemove', function (e) {
    var rect = section.getBoundingClientRect();
    cursorX = e.clientX - rect.left;
    cursorY = e.clientY - rect.top;

    if (!hasMoved) {
      hasMoved = true;
      section.classList.add('cursor-visible');
      raf = requestAnimationFrame(moveCursor);
    }
  });

  section.addEventListener('mouseleave', function () {
    hasMoved = false;
    section.classList.remove('cursor-visible', 'cursor-shrink');
    cancelAnimationFrame(raf);
  });

  // Shrink cursor over interactive elements
  section.querySelectorAll('button, a, [role="button"]').forEach(function (el) {
    el.addEventListener('mouseenter', function () { section.classList.add('cursor-shrink'); });
    el.addEventListener('mouseleave', function () { section.classList.remove('cursor-shrink'); });
  });

  // ── 3. Mute / unmute toggle ──
  section.classList.add('is-muted');

  if (muteBtn && video) {
    muteBtn.addEventListener('click', function () {
      video.muted = !video.muted;
      section.classList.toggle('is-muted', video.muted);
    });
  }

  // ── 4. Pause / resume video on visibility ──
  var ioVideo = new IntersectionObserver(function (entries) {
    if (!video) return;
    if (entries[0].isIntersecting) {
      video.play().catch(function () {});
    } else {
      video.pause();
    }
  }, { threshold: 0 });
  ioVideo.observe(section);

})();
