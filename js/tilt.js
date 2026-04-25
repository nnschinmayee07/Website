/**
 * TiltedCard effect — pure vanilla JS
 */
(function () {
  'use strict';
  const D = { max: 10, scale: 1.03, speed: 450, perspective: 1200 };

  function initTilt(el) {
    const max = parseFloat(el.dataset.tiltMax) || D.max;
    const scale = parseFloat(el.dataset.tiltScale) || D.scale;
    const hasGlare = el.hasAttribute('data-tilt-glare');
    el.style.transformStyle = 'preserve-3d';
    el.style.willChange = 'transform';
    el.style.transition = `transform ${D.speed}ms cubic-bezier(0.03, 0.98, 0.52, 0.99)`;

    let glareEl = null;
    if (hasGlare) {
      const w = document.createElement('div'); w.className = 'tilt-glare-wrap';
      glareEl = document.createElement('div'); glareEl.className = 'tilt-glare';
      w.appendChild(glareEl); el.appendChild(w);
    }

    let rafId = null, rect = null;

    el.addEventListener('mouseenter', () => { rect = el.getBoundingClientRect(); el.style.transition = 'none'; });
    el.addEventListener('mousemove', e => {
      if (!rect || rafId) return;
      rafId = requestAnimationFrame(() => {
        const x = e.clientX - rect.left, y = e.clientY - rect.top;
        const cx = rect.width / 2, cy = rect.height / 2;
        const rX = ((y - cy) / cy) * -max, rY = ((x - cx) / cx) * max;
        el.style.transform = `perspective(${D.perspective}px) rotateX(${rX.toFixed(2)}deg) rotateY(${rY.toFixed(2)}deg) scale3d(${scale},${scale},${scale})`;
        if (glareEl) {
          const a = Math.atan2(y - cy, x - cx) * (180 / Math.PI) + 90;
          const i = Math.min(Math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / Math.max(cx, cy), 1);
          glareEl.style.transform = `rotate(${a.toFixed(1)}deg) translate(-50%, -50%)`;
          glareEl.style.opacity = (i * 0.18).toFixed(3);
        }
        rafId = null;
      });
    });
    el.addEventListener('mouseleave', () => {
      if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
      el.style.transition = `transform ${D.speed}ms cubic-bezier(0.03, 0.98, 0.52, 0.99)`;
      el.style.transform = `perspective(${D.perspective}px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)`;
      if (glareEl) glareEl.style.opacity = '0';
      rect = null;
    });
  }

  function init() { document.querySelectorAll('[data-tilt]').forEach(initTilt); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
