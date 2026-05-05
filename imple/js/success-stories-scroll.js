// ── Success Stories: Auto-advancing carousel ─────────────────────────
(function () {
  var carousel = document.getElementById('ssCarousel');
  if (!carousel) return;

  var cards    = carousel.querySelectorAll('.ss-card');
  var prev     = document.getElementById('ssPrev');
  var next     = document.getElementById('ssNext');
  var dots     = document.querySelectorAll('.ss-dot');
  var total    = cards.length;
  var current  = 0;
  var timer    = null;
  var INTERVAL = 2000;

  function goTo(idx) {
    var nextIdx = (idx + total) % total;
    if (nextIdx === current) return;

    var leaving = cards[current];
    leaving.classList.add('is-leaving');
    leaving.classList.remove('is-active');

    current = nextIdx;
    var entering = cards[current];
    entering.classList.add('is-active');
    entering.classList.remove('is-leaving');

    leaving.addEventListener('transitionend', function onEnd() {
      leaving.classList.remove('is-leaving');
      leaving.removeEventListener('transitionend', onEnd);
    });

    dots.forEach(function (d, i) {
      d.classList.toggle('ss-dot--active', i === current);
    });
  }

  function startAuto() {
    timer = setInterval(function () { goTo(current + 1); }, INTERVAL);
  }

  function stopAuto() { clearInterval(timer); }

  if (prev) prev.addEventListener('click', function () { stopAuto(); goTo(current - 1); startAuto(); });
  if (next) next.addEventListener('click', function () { stopAuto(); goTo(current + 1); startAuto(); });

  dots.forEach(function (d) {
    d.addEventListener('click', function () {
      stopAuto();
      goTo(parseInt(d.dataset.idx, 10));
      startAuto();
    });
  });

  carousel.addEventListener('mouseenter', stopAuto);
  carousel.addEventListener('mouseleave', startAuto);

  startAuto();
})();
