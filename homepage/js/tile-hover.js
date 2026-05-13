/* Bevel tilt + shine sweep for Chronicle tiles */
(function () {
  'use strict';

  var TILT  = 10;
  var LIFT  = 'perspective(900px) rotateX({rx}deg) rotateY({ry}deg) scale3d(1.03,1.03,1.03) translateZ(18px)';
  var IN    = 'transform 0.12s ease-out, box-shadow 0.15s ease';
  var OUT   = 'transform 0.5s cubic-bezier(0.23,1,0.32,1), box-shadow 0.15s ease';

  function makeTile(el) {
    var shine = document.createElement('div');
    shine.className = 'tile__shine';
    el.appendChild(shine);
    el.classList.add('tile');

    var raf = null;
    var live = false;

    el.addEventListener('mouseenter', function () {
      live = true;
      el.style.transition = IN;
    });

    el.addEventListener('mousemove', function (e) {
      if (!live) return;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        var r  = el.getBoundingClientRect();
        var x  = e.clientX - r.left;
        var y  = e.clientY - r.top;
        var rx = ((y - r.height / 2) / (r.height / 2)) * -TILT;
        var ry = ((x - r.width  / 2) / (r.width  / 2)) *  TILT;
        el.style.transform = LIFT
          .replace('{rx}', rx.toFixed(2))
          .replace('{ry}', ry.toFixed(2));
        shine.style.setProperty('--mx', ((x / r.width)  * 100).toFixed(1) + '%');
        shine.style.setProperty('--my', ((y / r.height) * 100).toFixed(1) + '%');
      });
    });

    el.addEventListener('mouseleave', function () {
      live = false;
      cancelAnimationFrame(raf);
      el.style.transition = OUT;
      el.style.transform = '';
    });
  }

  function init() {
    document.querySelectorAll(
      '.chron-card, .chron-featured, .chron-sidebar-box, ' +
      '.chron-notices-board, .chron-subscribe, .chron-research-box, ' +
      '.chron-story-card, .chron-placements-box, .chron-the-box, .chron-quickstat'
    ).forEach(makeTile);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
