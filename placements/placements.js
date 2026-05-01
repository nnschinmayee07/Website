/* ============================================================
   MLRIT Placements — placements.js
   Premium interactions · v4.0
   ============================================================ */

/* ── 1. Stats Wall: entry animation + hover video ── */
(function () {
  const wall = document.getElementById('pl-wall');
  const vid  = document.getElementById('plWallVideo');
  if (!wall) return;

  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) wall.classList.add('is-visible');
  }, { threshold: 0.18 }).observe(wall);

  if (vid) {
    wall.addEventListener('mouseenter', () => {
      vid.play().catch(() => {});
      wall.classList.add('video-active');
    });
    wall.addEventListener('mouseleave', () => {
      vid.pause();
      vid.currentTime = 0;
      wall.classList.remove('video-active');
    });
  }
})();


/* ── 2. Expand / collapse helpers ── */
function makeExpandBtn(label, collapseLabel) {
  const btn = document.createElement('button');
  btn.className       = 'pl-expand-btn';
  btn.dataset.label   = label;
  btn.dataset.collapse = collapseLabel || 'Show Less';
  btn.innerHTML       = `${label} <i class="pl-btn-arrow">↓</i>`;
  return btn;
}

function bindExpand(extra, btn) {
  let open = false;
  btn.addEventListener('click', () => {
    open = !open;
    btn.classList.toggle('is-open', open);

    if (open) {
      extra.style.maxHeight = extra.scrollHeight + 'px';
      extra.classList.add('is-open');
      btn.innerHTML = `${btn.dataset.collapse} <i class="pl-btn-arrow">↓</i>`;

      extra.querySelectorAll('.stagger-in').forEach((el, i) => {
        el.style.transitionDelay = `${i * 55}ms`;
        requestAnimationFrame(() => el.classList.add('is-visible'));
      });
      extra.querySelectorAll('.masonry-in').forEach((el, i) => {
        el.style.transitionDelay = `${i * 75}ms`;
        requestAnimationFrame(() => el.classList.add('is-visible'));
      });
    } else {
      extra.style.maxHeight = '0';
      extra.classList.remove('is-open');
      btn.innerHTML = `${btn.dataset.label} <i class="pl-btn-arrow">↓</i>`;
      extra.querySelectorAll('.stagger-in, .masonry-in').forEach(el => {
        el.style.transitionDelay = '0ms';
        el.classList.remove('is-visible');
      });
    }
  });
}


/* ── 3. Scroll-reveal observer ── */
const scrollIO = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    scrollIO.unobserve(entry.target);
  });
}, { threshold: 0.12 });

function observeFade(el) { scrollIO.observe(el); }


/* ── 4. Content render ── */
document.addEventListener('DOMContentLoaded', function () {

  /* 4a. Overview — moved into hero; no render needed */

  /* 4b. Year-wise stats — scroll-triggered stagger (no expand button) */
  const yearContainer = document.getElementById('pl-yearstats-content');
  if (yearContainer && typeof yearwiseStats !== 'undefined') {
    const [latest, ...older] = yearwiseStats;

    yearContainer.innerHTML = `
      <div class="pl-year-featured pl-fade">
        <div class="pl-year-featured__year">${latest.year}</div>
        <div class="pl-year-featured__stat">
          <span class="pl-year-featured__val">${latest.offers}</span>
          <span class="pl-year-featured__lbl">Job Offers</span>
        </div>
        <div class="pl-year-featured__stat">
          <span class="pl-year-featured__val">${latest.companies}</span>
          <span class="pl-year-featured__lbl">Companies</span>
        </div>
        <div class="pl-year-featured__stat">
          <span class="pl-year-featured__val">₹${latest.highest} LPA</span>
          <span class="pl-year-featured__lbl">Highest Package</span>
        </div>
      </div>
      <div class="pl-year-list" id="pl-year-history-rows">
        ${older.map(y => {
          const details = (typeof yearwiseDetails !== 'undefined' && yearwiseDetails[y.year]) || [];
          return `<div class="pl-year-wrap">
            <div class="pl-year-row">
              <span class="pl-year-row__year">${y.year}</span>
              <div class="pl-year-row__val">${y.offers}<span class="pl-year-row__lbl">Offers</span></div>
              <div class="pl-year-row__val">${y.companies}<span class="pl-year-row__lbl">Companies</span></div>
              <div class="pl-year-row__val">₹${y.highest} LPA<span class="pl-year-row__lbl">Highest</span></div>
            </div>
            ${details.length ? `<div class="pl-year-detail">
              <div class="pl-year-detail__inner">
              <table class="pl-year-detail__table">
                <thead><tr><th>S.No</th><th>Company</th><th>Role</th><th>Salary</th><th>Selects</th></tr></thead>
                <tbody>${details.map((d, j) => `<tr><td>${j + 1}</td><td>${d.company}</td><td>${d.role}</td><td>${d.salary}</td><td>${d.selects}</td></tr>`).join('')}</tbody>
              </table>
              </div>
            </div>` : ''}
          </div>`;
        }).join('')}
      </div>`;

    observeFade(yearContainer.querySelector('.pl-fade'));

    const rowsEl = document.getElementById('pl-year-history-rows');
    if (rowsEl) {
      const rows = Array.from(rowsEl.querySelectorAll('.pl-year-row'));

      new IntersectionObserver(([entry]) => {
        if (!entry.isIntersecting) return;
        rows.forEach((row, i) => {
          setTimeout(() => row.classList.add('is-visible'), i * 80);
        });
      }, { threshold: 0.1 }).observe(rowsEl);

      /* Hover: show this year's detail, hide all others */
      const wraps = Array.from(rowsEl.querySelectorAll('.pl-year-wrap'));
      wraps.forEach(wrap => {
        const detail = wrap.querySelector('.pl-year-detail');
        if (!detail) return;
        wrap.addEventListener('mouseenter', () => {
          wraps.forEach(w => {
            const d = w.querySelector('.pl-year-detail');
            if (d) d.classList.remove('is-active');
            w.classList.remove('is-hovered');
          });
          detail.classList.add('is-active');
          wrap.classList.add('is-hovered');
        });
        wrap.addEventListener('mouseleave', () => {
          detail.classList.remove('is-active');
          wrap.classList.remove('is-hovered');
        });
      });
    }
  }

  /* 4c. Recruiters — single infinite-scroll logo band with 4-side tilt */
  const row1 = document.getElementById('plLogoRow1');
  if (row1 && typeof recruiters !== 'undefined') {
    const makeItem = r => `<div class="pl-logo-item" title="${r.name}">
      <img src="${r.logo}" alt="${r.name}" loading="lazy" />
    </div>`;

    /* Duplicate for seamless loop */
    row1.innerHTML = [...recruiters, ...recruiters].map(makeItem).join('');

    /* 4-side tilt effect on each card */
    row1.querySelectorAll('.pl-logo-item').forEach(card => {
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width  / 2) / (r.width  / 2);
        const y = (e.clientY - r.top  - r.height / 2) / (r.height / 2);
        card.style.transition = 'transform 0.08s ease, border-color 0.3s, background 0.3s, box-shadow 0.3s';
        card.style.transform  = `perspective(500px) rotateX(${-y * 12}deg) rotateY(${x * 12}deg) scale(1.06)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transition = 'transform 0.45s ease, border-color 0.3s, background 0.3s, box-shadow 0.3s';
        card.style.transform  = '';
      });
    });
  }

  /* 4d. MoUs — Narrative timeline blocks with optional document links */
  const mouGrid = document.getElementById('pl-mou-grid');
  if (mouGrid && typeof mous !== 'undefined') {
    mouGrid.className = 'pl-mou__narrative';
    mouGrid.innerHTML = mous.map((m, i) => `
      <div class="pl-mou__row${i % 2 !== 0 ? ' pl-mou__row--alt' : ''} pl-fade">
        <div class="pl-mou__row-meta">
          ${m.type ? `<span class="pl-mou__type${m.type === 'Centre of Excellence' ? ' pl-mou__type--coe' : ''}">${m.type}</span>` : ''}
          ${m.package ? `<span class="pl-mou__metric">${m.package}</span>` : ''}
        </div>
        <div class="pl-mou__row-main">
          <h3 class="pl-mou__company">${m.name}</h3>
        </div>
        <p class="pl-mou__desc">${m.domain.replace(/&amp;/g, 'and')}</p>
        ${m.docs && m.docs.length ? `<div class="pl-mou__docs">${m.docs.map(d =>
          `<a href="${d.file}" class="pl-mou__doc-link" target="_blank" rel="noopener">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            ${d.label}</a>`).join('')}</div>` : ''}
      </div>`).join('');

    mouGrid.querySelectorAll('.pl-fade').forEach(observeFade);
  }

  /* 4f. Gallery — uniform grid */
  const galleryGrid = document.getElementById('pl-gallery-grid');
  if (galleryGrid && typeof gallery !== 'undefined') {
    galleryGrid.innerHTML = gallery.map((img, i) => `
      <div class="pl-drive-card pl-fade">
        <div class="pl-drive-card__img">
          <img src="${img.src}" alt="${img.alt}" loading="${i === 0 ? 'eager' : 'lazy'}" />
          <div class="pl-drive-card__overlay">
            <span class="pl-drive-card__tag">On Campus</span>
            <span class="pl-drive-card__title">${img.alt}</span>
          </div>
        </div>
      </div>`).join('');

    const gsIO = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-visible');
        gsIO.unobserve(e.target);
      });
    }, { threshold: 0.1 });

    galleryGrid.querySelectorAll('.pl-drive-card').forEach(c => gsIO.observe(c));
  }

  /* ── Scroll-reveal: wire all .pl-fade in static HTML ── */
  document.querySelectorAll('.pl-section-inner').forEach(sec => {
    sec.querySelectorAll('.pl-heading, .pl-label').forEach(el => {
      if (!el.classList.contains('pl-fade')) el.classList.add('pl-fade');
    });
    sec.querySelectorAll(
      '.pl-statgrid__card, .pl-training__block, .pl-infra__stat'
    ).forEach(el => {
      if (!el.classList.contains('pl-fade')) el.classList.add('pl-fade');
    });

    new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.pl-fade:not(.is-visible)').forEach((el, i) => {
        el.style.transitionDelay = `${i * 60}ms`;
        el.classList.add('is-visible');
      });
    }, { threshold: 0.08 }).observe(sec);
  });

  /* ── Sidebar visibility: appear only after hero leaves viewport ── */
  (function () {
    const sidebar = document.getElementById('plSidebar');
    const hero    = document.getElementById('pl-wall');
    if (!sidebar || !hero) return;
    new IntersectionObserver(([entry]) => {
      sidebar.classList.toggle('is-visible', !entry.isIntersecting);
    }, { threshold: 0 }).observe(hero);
  })();

  /* ── Sidebar: click → smooth scroll + active tracking on scroll ── */
  (function () {
    const items = Array.from(document.querySelectorAll('.pl-sidebar__item[data-section]'));
    if (!items.length) return;

    const sections = items.map(a => document.getElementById(a.dataset.section)).filter(Boolean);

    function setActive(id) {
      items.forEach(a => a.classList.toggle('is-active', a.dataset.section === id));
    }

    /* Smooth scroll on click */
    items.forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        const target = document.getElementById(a.dataset.section);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          setActive(a.dataset.section);
        }
      });
    });

    /* Scroll-spy — highlights whichever section occupies the upper half of viewport */
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { threshold: 0, rootMargin: '-20% 0px -55% 0px' });

    sections.forEach(s => io.observe(s));
  })();

  /* ── Counter: all numbers count up when scrolled into view ── */
  (function () {
    function parseNum(str) {
      const m = str.match(/^([^0-9]*)([0-9]+(?:\.[0-9]+)?)(.*)$/);
      if (!m) return null;
      const dec = m[2].includes('.') ? m[2].split('.')[1].length : 0;
      return { pre: m[1], val: parseFloat(m[2]), suf: m[3], dec };
    }

    function countUp(el) {
      /* Find first text node that contains a digit */
      let node = null;
      for (const n of el.childNodes) {
        if (n.nodeType === 3 && /\d/.test(n.textContent)) { node = n; break; }
      }
      if (!node) return;

      const p = parseNum(node.textContent.trim());
      if (!p || p.val === 0) return;

      const fmt  = v => p.pre + (p.dec ? v.toFixed(p.dec) : Math.round(v)) + p.suf;
      const ease = t => 1 - Math.pow(1 - t, 3);
      const dur  = 1500;
      let t0 = null;

      requestAnimationFrame(function tick(ts) {
        if (!t0) t0 = ts;
        const prog = Math.min((ts - t0) / dur, 1);
        node.textContent = fmt(p.val * ease(prog));
        if (prog < 1) requestAnimationFrame(tick);
      });
    }

    const counterIO = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        countUp(e.target);
        counterIO.unobserve(e.target);
      });
    }, { threshold: 0.5 });

    document.querySelectorAll(
      '.pl-statgrid__value, ' +
      '.pl-year-featured__val, .pl-year-row__val, ' +
      '.pl-infra__stat-num'
    ).forEach(el => counterIO.observe(el));
  })();

});
