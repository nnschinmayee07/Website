/* ============================================================
   MLRIT Placements — placements.js
   Premium interactions · v4.0
   ============================================================ */

/* ── 1. Stats Wall: entry animation + mouse/scroll parallax ── */
(function () {
  const wall = document.getElementById('pl-wall');
  if (!wall) return;

  const ghosts = Array.from(wall.querySelectorAll('.pl-wall__ghost[data-parallax]'));
  const state  = ghosts.map(() => ({ mx: 0, my: 0, sy: 0, bright: 1.0 }));
  let raf = false;

  function flush() {
    ghosts.forEach((g, i) => {
      const s = state[i];
      g.style.translate = `${s.mx.toFixed(1)}px ${(s.my + s.sy).toFixed(1)}px`;
      g.style.filter = s.bright > 1.02 ? `brightness(${s.bright.toFixed(2)})` : '';
    });
    raf = false;
  }
  function queue() { if (!raf) { requestAnimationFrame(flush); raf = true; } }

  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) wall.classList.add('is-visible');
  }, { threshold: 0.18 }).observe(wall);

  wall.addEventListener('mousemove', (e) => {
    const r  = wall.getBoundingClientRect();
    const cx = e.clientX - r.left;
    const cy = e.clientY - r.top;
    const nx = (cx - r.width  * 0.5) / (r.width  * 0.5);
    const ny = (cy - r.height * 0.5) / (r.height * 0.5);

    ghosts.forEach((g, i) => {
      const sp = parseFloat(g.dataset.parallax) || 0.06;
      state[i].mx = nx * sp * 280;
      state[i].my = ny * sp * 180;

      /* Proximity brightness — ghost glows as cursor approaches its center */
      const gr   = g.getBoundingClientRect();
      const gCx  = gr.left + gr.width  / 2 - r.left;
      const gCy  = gr.top  + gr.height / 2 - r.top;
      const dist = Math.hypot(cx - gCx, cy - gCy);
      const prox = Math.max(0, 1 - dist / (Math.hypot(r.width, r.height) * 0.55));
      state[i].bright = 1 + prox * 7;
    });
    queue();
  }, { passive: true });

  wall.addEventListener('mouseleave', () => {
    state.forEach(s => { s.mx = 0; s.my = 0; s.bright = 1.0; });
    queue();
  });

  window.addEventListener('scroll', () => {
    const rect  = wall.getBoundingClientRect();
    const wallH = wall.offsetHeight;
    const depth = 1 - rect.bottom / (wallH + window.innerHeight);
    ghosts.forEach((g, i) => {
      const sp     = parseFloat(g.dataset.parallax) || 0.06;
      state[i].sy  = depth * sp * wallH * 0.5;
    });
    wall.style.opacity = rect.top < 0
      ? (1 - Math.max(0, Math.min(1, -rect.top / wallH)) * 0.15).toFixed(3)
      : '1';
    queue();
  }, { passive: true });
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
        ${older.map(y => `
          <div class="pl-year-row">
            <span class="pl-year-row__year">${y.year}</span>
            <div class="pl-year-row__val">${y.offers}<span class="pl-year-row__lbl">Offers</span></div>
            <div class="pl-year-row__val">${y.companies}<span class="pl-year-row__lbl">Companies</span></div>
            <div class="pl-year-row__val">₹${y.highest} LPA<span class="pl-year-row__lbl">Highest</span></div>
          </div>`).join('')}
      </div>`;

    observeFade(yearContainer.querySelector('.pl-fade'));

    const rowsEl = document.getElementById('pl-year-history-rows');
    if (rowsEl) {
      const rows = rowsEl.querySelectorAll('.pl-year-row');
      new IntersectionObserver(([entry]) => {
        if (!entry.isIntersecting) return;
        rows.forEach((row, i) => {
          setTimeout(() => row.classList.add('is-visible'), i * 80);
        });
      }, { threshold: 0.1 }).observe(rowsEl);
    }
  }

  /* 4c. Recruiters — handled by pl-globe.js (globe replaces entire section inner).
          Flat grid renders only if globe script did not run. */
  const grid = document.getElementById('pl-recruiters-grid');
  if (grid && typeof recruiters !== 'undefined') {
    const visible = recruiters.slice(0, 8);
    const hidden  = recruiters.slice(8);

    grid.innerHTML = visible.map(r => `
      <div class="pl-recruiter-card">
        <img src="${r.logo}" alt="${r.name}" loading="lazy" title="${r.name}" />
      </div>`).join('');

    if (hidden.length) {
      const extra = document.createElement('div');
      extra.className = 'pl-extra-content';
      extra.innerHTML = `
        <div class="pl-recruiters__grid-inner">
          ${hidden.map(r => `
            <div class="pl-recruiter-card stagger-in">
              <img src="${r.logo}" alt="${r.name}" loading="lazy" title="${r.name}" />
            </div>`).join('')}
        </div>`;

      const btn = makeExpandBtn(`View All ${recruiters.length} Recruiters`, 'Show Less');
      grid.parentElement.appendChild(extra);
      grid.parentElement.appendChild(btn);
      bindExpand(extra, btn);
    }
  }

  /* 4d. MoUs — Narrative timeline blocks (all shown, no expand) */
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
      </div>`).join('');

    mouGrid.querySelectorAll('.pl-fade').forEach(observeFade);
  }

  /* 4f. Gallery — Narrative story strips (blur→sharpen reveal) */
  const galleryGrid = document.getElementById('pl-gallery-grid');
  if (galleryGrid && typeof gallery !== 'undefined') {
    let html = '';
    let pairFlip = false;

    for (let i = 0; i < gallery.length; ) {
      const img = gallery[i];

      if (i === 0) {
        html += `
          <div class="pl-gs pl-gs--hero">
            <div class="pl-gs__img">
              <img src="${img.src}" alt="${img.alt}" loading="eager" />
              <figcaption class="pl-gs__cap">
                <span class="pl-gs__cap-tag">MLRIT · Campus</span>
                <span class="pl-gs__cap-title">${img.alt}</span>
              </figcaption>
            </div>
          </div>`;
        i++;
      } else {
        const next = gallery[i + 1];
        html += `
          <div class="pl-gs pl-gs--pair${pairFlip ? ' pl-gs--flip' : ''}">
            <div class="pl-gs__img pl-gs__img--dom">
              <img src="${img.src}" alt="${img.alt}" loading="lazy" />
              <figcaption class="pl-gs__cap">
                <span class="pl-gs__cap-tag">On Campus</span>
                <span class="pl-gs__cap-title">${img.alt}</span>
              </figcaption>
            </div>
            ${next ? `<div class="pl-gs__img pl-gs__img--sup">
              <img src="${next.src}" alt="${next.alt}" loading="lazy" />
              <figcaption class="pl-gs__cap">
                <span class="pl-gs__cap-tag">On Campus</span>
                <span class="pl-gs__cap-title">${next.alt}</span>
              </figcaption>
            </div>` : ''}
          </div>`;
        pairFlip = !pairFlip;
        i += next ? 2 : 1;
      }
    }

    galleryGrid.innerHTML = html;

    const gsIO = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-visible');
        gsIO.unobserve(e.target);
      });
    }, { threshold: 0.1 });

    galleryGrid.querySelectorAll('.pl-gs').forEach(s => gsIO.observe(s));
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

  /* ── Story strips: directional reveal ── */
  (function () {
    const stripIO = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          stripIO.unobserve(entry.target);
        }
      });
    }, { threshold: 0.18 });

    document.querySelectorAll('.pl-train__strip').forEach(strip => stripIO.observe(strip));
  })();

  /* Recruiter interactions handled by pl-globe.js */

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
      '.pl-wall__item-num, .pl-statgrid__value, ' +
      '.pl-year-featured__val, .pl-year-row__val, ' +
      '.pl-infra__stat-num'
    ).forEach(el => counterIO.observe(el));
  })();

});
