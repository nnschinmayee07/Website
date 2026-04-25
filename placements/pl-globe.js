/* ============================================================
   MLRIT — pl-globe.js
   Recruiter Globe: one strong idea, executed precisely.
   Pure JS · No dependencies · Depth-correct 3D sphere projection
   ============================================================ */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    if (typeof recruiters === 'undefined') return;
    const section = document.querySelector('.pl-recruiters');
    if (!section) return;
    buildGlobe(section);
  });

  /* ─────────────────────────────────────────────
     BUILD
  ───────────────────────────────────────────── */
  function buildGlobe(section) {

    /* Minimal, focused header */
    section.innerHTML = `
      <div class="pl-section-inner pl-globe-header">
        <span class="pl-label">Global Network</span>
        <h2 class="pl-heading">Our Recruiters</h2>
        <p class="pl-globe-sub">
          Trusted by leading organisations across technology,
          engineering, consulting, and product — worldwide.
        </p>
      </div>
      <div class="pl-globe-stage" id="pl-globe-stage">
        <canvas class="pl-globe-canvas" id="pl-globe-canvas"></canvas>
        <div  class="pl-globe-field"  id="pl-globe-field"></div>
        <div  class="pl-globe-tip"    id="pl-globe-tip"></div>
      </div>
    `;

    const stage  = document.getElementById('pl-globe-stage');
    const canvas = document.getElementById('pl-globe-canvas');
    const field  = document.getElementById('pl-globe-field');
    const tip    = document.getElementById('pl-globe-tip');
    const ctx    = canvas.getContext('2d');

    /* ── Dimensions ── */
    let W, H, R;

    function resize() {
      W = stage.clientWidth;
      H = Math.max(Math.min(W * 0.66, 580), 340);
      R = Math.min(W, H) * 0.34;
      stage.style.height = H + 'px';

      const dpr = Math.min(devicePixelRatio, 2);
      canvas.width  = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width  = W + 'px';
      canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    /* ── Fibonacci sphere distribution (even spread, no clustering) ── */
    const GOLDEN = Math.PI * (3 - Math.sqrt(5));
    const nodes  = recruiters.map((rec, i) => {
      const t   = recruiters.length > 1 ? i / (recruiters.length - 1) : 0;
      const phi = Math.acos(1 - 2 * t);           /* polar inclination */
      const θ   = GOLDEN * i;                      /* azimuth */
      return {
        rec,
        lat: Math.PI / 2 - phi,
        lon: θ,
        el:  null,
        /* Smoothed per-frame values (lerped — no CSS transition conflict) */
        opacity: 0.1,
        scale:   0.55,
        blur:    1.5,
        gray:    0.9,
        /* Screen position */
        sx: 0, sy: 0, sz: 0
      };
    });

    /* ── Create DOM nodes ── */
    let hovIdx = -1;
    let selIdx = -1;

    nodes.forEach((node, i) => {
      const div = document.createElement('div');
      div.className = 'pl-globe-node';

      const img = document.createElement('img');
      img.src     = node.rec.logo;
      img.alt     = node.rec.name;
      img.loading = 'lazy';
      img.draggable = false;

      const label = document.createElement('span');
      label.className   = 'pl-globe-node__label';
      label.textContent = node.rec.name;

      div.appendChild(img);
      div.appendChild(label);
      field.appendChild(div);
      node.el = div;

      div.addEventListener('mouseenter', () => {
        hovIdx = i;
        tip.textContent = node.rec.name;
        tip.classList.add('is-on');
      });
      div.addEventListener('mouseleave', () => {
        hovIdx = -1;
        tip.classList.remove('is-on');
      });
      div.addEventListener('click', () => {
        selIdx = selIdx === i ? -1 : i;
      });
    });

    /* ── Mouse state ── */
    let mxNorm = 0, myNorm = 0;         /* normalised -1 → 1 */
    let tiltX  = 0, tiltY  = 0;         /* smoothed camera tilt */

    stage.addEventListener('mousemove', e => {
      const r = stage.getBoundingClientRect();
      mxNorm = (e.clientX - r.left - W * 0.5) / (W * 0.5);
      myNorm = (e.clientY - r.top  - H * 0.5) / (H * 0.5);
      tip.style.left = (e.clientX - r.left + 16) + 'px';
      tip.style.top  = (e.clientY - r.top  -  8) + 'px';
    }, { passive: true });

    stage.addEventListener('mouseleave', () => {
      mxNorm = 0; myNorm = 0;
      hovIdx = -1;
      tip.classList.remove('is-on');
    });

    /* ── 3D projection ── */
    let autoAngle = 0;

    function project(lat, lon) {
      /* Unit-sphere point */
      const x0 = Math.cos(lat) * Math.sin(lon + autoAngle);
      const y0 = Math.sin(lat);
      const z0 = Math.cos(lat) * Math.cos(lon + autoAngle);

      /* Rotate by camera tilt (pitch = X axis, yaw = Y axis) */
      const sinX = Math.sin(tiltX), cosX = Math.cos(tiltX);
      const sinY = Math.sin(tiltY), cosY = Math.cos(tiltY);

      const y1 =  y0 * cosX - z0 * sinX;
      const z1 =  y0 * sinX + z0 * cosX;
      const x2 =  x0 * cosY + z1 * sinY;
      const z2 = -x0 * sinY + z1 * cosY;

      return { x: x2, y: y1, z: z2 };
    }

    /* ── Lerp (used for depth-smoothing — avoids CSS transition conflict) ── */
    function lerp(a, b, t) { return a + (b - a) * t; }

    /* ── Draw wireframe ── */
    function drawWire() {
      ctx.clearRect(0, 0, W, H);
      const cx = W / 2, cy = H / 2;

      /* Front-lit sphere gradient */
      const sphG = ctx.createRadialGradient(
        cx - R * 0.24, cy - R * 0.24, 0,
        cx, cy, R
      );
      sphG.addColorStop(0,   'rgba(255,255,255,0.020)');
      sphG.addColorStop(0.65,'rgba(180,210,200,0.006)');
      sphG.addColorStop(1,   'rgba(0,0,0,0.030)');
      ctx.fillStyle = sphG;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fill();

      /* Atmosphere rim */
      const rimG = ctx.createRadialGradient(cx, cy, R * 0.9, cx, cy, R * 1.1);
      rimG.addColorStop(0, 'transparent');
      rimG.addColorStop(1, 'rgba(160,210,195,0.016)');
      ctx.fillStyle = rimG;
      ctx.beginPath();
      ctx.arc(cx, cy, R * 1.1, 0, Math.PI * 2);
      ctx.fill();

      /* Latitude rings (5 lines, depth-faded) */
      ctx.lineWidth = 0.55;
      for (let li = 1; li <= 5; li++) {
        const lat = (li / 6 - 0.5) * Math.PI;
        ctx.beginPath();
        let started = false;
        for (let a = 0; a <= Math.PI * 2 + 0.04; a += 0.05) {
          const p  = project(lat, a);
          const px = cx + p.x * R;
          const py = cy - p.y * R;
          ctx.globalAlpha = Math.max(0, (p.z + 1) / 2 * 0.20);
          if (!started) { ctx.moveTo(px, py); started = true; }
          else            ctx.lineTo(px, py);
        }
        ctx.strokeStyle = 'rgba(255,255,255,0.9)';
        ctx.stroke();
      }

      /* Longitude meridians (9 lines) */
      for (let li = 0; li < 9; li++) {
        const lon = (li / 9) * Math.PI * 2;
        ctx.beginPath();
        let started = false;
        for (let a = -Math.PI / 2; a <= Math.PI / 2 + 0.04; a += 0.05) {
          const p  = project(a, lon);
          const px = cx + p.x * R;
          const py = cy - p.y * R;
          ctx.globalAlpha = Math.max(0, (p.z + 1) / 2 * 0.16);
          if (!started) { ctx.moveTo(px, py); started = true; }
          else            ctx.lineTo(px, py);
        }
        ctx.strokeStyle = 'rgba(255,255,255,0.9)';
        ctx.stroke();
      }

      ctx.globalAlpha = 1;
    }

    /* ── Update logo node positions + depth styling ── */
    function updateNodes() {
      const cx     = W / 2, cy = H / 2;
      const SMOOTH = 0.05;    /* lerp speed — controls how fast depth transitions */

      nodes.forEach(node => {
        const p   = project(node.lat, node.lon);
        node.sx   = cx + p.x * R;
        node.sy   = cy - p.y * R;
        node.sz   = p.z;
      });

      nodes.forEach((node, i) => {
        const depth  = (node.sz + 1) / 2;      /* 0 = far back, 1 = front */
        const hov    = i === hovIdx;
        const sel    = i === selIdx;
        const active = hov || sel;

        /* Target visual properties based on depth + state */
        const tgtScale   = active ? 1.28                       : lerp(0.50, 1.0, depth);
        const tgtOpacity = active ? 0.96                       : lerp(0.08, 0.84, depth);
        const tgtBlur    = active ? 0                          : lerp(2.8, 0, depth);
        const tgtGray    = active ? 0                          : lerp(0.95, 0.78, depth);

        /* Hover uses faster lerp for snappy scale; depth transitions stay slow */
        const scaleSpeed = active ? 0.14 : SMOOTH;
        node.scale   = lerp(node.scale,   tgtScale,   scaleSpeed);
        node.opacity = lerp(node.opacity, tgtOpacity, SMOOTH);
        node.blur    = lerp(node.blur,    tgtBlur,    SMOOTH);
        node.gray    = lerp(node.gray,    tgtGray,    SMOOTH);

        /* z-index: depth order, active always on top */
        const zIdx = Math.round(depth * 100) + (active ? 60 : 0);

        /* Apply — transform is set directly (no CSS transition, lerp handles smoothness) */
        const el = node.el;
        el.style.left      = node.sx.toFixed(1) + 'px';
        el.style.top       = node.sy.toFixed(1) + 'px';
        el.style.transform = `translate(-50%,-50%) scale(${node.scale.toFixed(3)})`;
        el.style.opacity   = node.opacity.toFixed(3);
        el.style.filter    = `grayscale(${node.gray.toFixed(2)}) blur(${node.blur.toFixed(2)}px)`;
        el.style.zIndex    = zIdx;
      });
    }

    /* ── Animation loop ── */
    let rafId   = null;
    let running = false;
    let lastTs  = null;   /* tracks previous frame timestamp for time-delta rotation */

    /* Full revolution in ~165 s → 0.02280 rad/s → 0.00002280 rad/ms */
    const ROT_RAD_MS = 0.00002280;
    const TAU        = Math.PI * 2;

    function frame(ts) {
      /* Time-delta rotation — immune to pause/resume and frame-rate variation */
      const dt  = lastTs !== null ? ts - lastTs : 0;
      lastTs    = ts;
      autoAngle = (autoAngle + dt * ROT_RAD_MS) % TAU;

      /* Smooth tilt towards mouse target */
      tiltX = lerp(tiltX, myNorm * 0.07,  0.028);
      tiltY = lerp(tiltY, mxNorm * 0.10,  0.028);

      drawWire();
      updateNodes();

      rafId = requestAnimationFrame(frame);
    }

    function start() { if (!running) { running = true;  requestAnimationFrame(frame); } }
    function stop()  { running = false; cancelAnimationFrame(rafId); rafId = null; lastTs = null; }

    /* Pause when off-screen (performance) */
    new IntersectionObserver(([e]) => {
      e.isIntersecting ? start() : stop();
    }, { threshold: 0.05 }).observe(stage);

    resize();
    window.addEventListener('resize', resize, { passive: true });
  }

})();
