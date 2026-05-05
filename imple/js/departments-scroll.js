// ── Programs: Scroll-to-Stack (smooth lerp) ───────────────────────────
// Cards start in a list. On scroll they collapse ONE BY ONE into a stack.
// Uses lerp interpolation for buttery smooth motion.
(function () {
  'use strict';

  var section   = document.getElementById('programs');
  var ugStack   = document.getElementById('ugStack');
  var pgStack   = document.getElementById('pgStack');
  var counter   = document.getElementById('deptCounter');
  var tabBtns   = document.querySelectorAll('.tab-btn[data-tab]');
  var activeTab = 'ug';

  if (!section || !ugStack) return;

  var GAP   = 14;    // matches CSS .dept-stack gap
  var PEEK  = 8;     // px each buried card peeks
  var LERP  = 0.055;  // smoothing factor — lower = slower, silkier
  var SNAP  = 0.3;   // px threshold to snap and stop animating

  /* ── State: current positions per card (for lerp) ─────────────── */
  var cardStates = []; // { el, current, target }
  var running    = false;

  function initStates(wrapper) {
    cardStates = [];
    var cards = wrapper.querySelectorAll('.dept-card');
    cards.forEach(function (card) {
      cardStates.push({ el: card, current: 0, target: 0 });
    });
  }

  /* ── Helpers ────────────────────────────────────────────────────── */

  function getTopbarH() {
    var tb = document.querySelector('.programs-topbar');
    return tb ? tb.offsetHeight : 80;
  }

  function pinColumns(wrapper) {
    wrapper.style.top = (getTopbarH() + 16) + 'px';
  }

  function easeOut(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /* ── Set section height: viewport + just enough scroll for collapse ── */
  function setSectionHeight(wrapper) {
    var stacks = wrapper.querySelectorAll('.dept-stack');
    var maxCollapse = 0;
    stacks.forEach(function (stack) {
      var cards = stack.querySelectorAll('.dept-card');
      var n = cards.length;
      if (n <= 1) return;
      var cardH = cards[0].offsetHeight;
      var total = (n - 1) * (cardH + GAP - PEEK);
      if (total > maxCollapse) maxCollapse = total;
    });
    // Section = viewport + scroll needed (divided by COLLAPSE_ZONE since
    // animation only uses that fraction of total scroll)
    var needed = window.innerHeight + Math.ceil(maxCollapse / 0.88) + 40;
    section.style.minHeight = needed + 'px';
  }

  /* ── Calculate targets from scroll position ─────────────────────── */

  function calcTargets(wrapper) {
    var rect     = section.getBoundingClientRect();
    var sectionH = section.offsetHeight;
    var viewH    = window.innerHeight;

    var scrollP = -rect.top / (sectionH - viewH);
    scrollP = Math.max(0, Math.min(1, scrollP));

    var stacks = wrapper.querySelectorAll('.dept-stack');
    var idx    = 0;

    stacks.forEach(function (stack) {
      var cards = stack.querySelectorAll('.dept-card');
      var n     = cards.length;
      if (n <= 1) { idx += n; return; }

      var cardH = cards[0].offsetHeight;
      var collapseAmount = cardH + GAP - PEEK;

      var COLLAPSE_ZONE = 0.88;
      var movingCards = n - 1;

      // Card 0 stays at 0
      if (cardStates[idx]) cardStates[idx].target = 0;
      idx++;

      for (var i = 1; i < n; i++) {
        var segStart = ((i - 1) / movingCards) * COLLAPSE_ZONE;
        var segEnd   = (i / movingCards) * COLLAPSE_ZONE;

        var cardP = (scrollP - segStart) / (segEnd - segStart);
        cardP = Math.max(0, Math.min(1, cardP));
        cardP = easeOut(cardP);

        var shift = i * collapseAmount * cardP;

        if (cardStates[idx]) {
          cardStates[idx].target = -shift;
        }
        idx++;
      }
    });

    // Update counter
    if (counter) {
      var total   = cardStates.length;
      var stacked = 0;
      cardStates.forEach(function (s) {
        if (Math.abs(s.target - s.current) < 2 && s.target !== 0) stacked++;
      });
      stacked++; // card 0 always stacked
      counter.textContent =
        String(Math.min(stacked, total)).padStart(2, '0') + ' / ' +
        String(total).padStart(2, '0');
    }
  }

  /* ── Animation loop — lerps current toward target ──────────────── */

  function tick() {
    var needsUpdate = false;

    for (var i = 0; i < cardStates.length; i++) {
      var s    = cardStates[i];
      var diff = s.target - s.current;

      if (Math.abs(diff) < SNAP) {
        // Close enough — snap
        if (s.current !== s.target) {
          s.current = s.target;
          s.el.style.transform = s.current === 0
            ? ''
            : 'translateY(' + s.current.toFixed(1) + 'px)';
        }
      } else {
        // Lerp toward target
        s.current += diff * LERP;
        s.el.style.transform = 'translateY(' + s.current.toFixed(1) + 'px)';
        needsUpdate = true;
      }
    }

    if (needsUpdate) {
      requestAnimationFrame(tick);
    } else {
      running = false;
    }
  }

  function startLoop() {
    if (!running) {
      running = true;
      requestAnimationFrame(tick);
    }
  }

  /* ── Tab switching ──────────────────────────────────────────────── */

  function switchTab(tab) {
    if (tab === activeTab) return;
    activeTab = tab;

    if (tab === 'pg') {
      ugStack.style.display = 'none';
      pgStack.style.display = '';
      setSectionHeight(pgStack);
      pinColumns(pgStack);
      initStates(pgStack);
      calcTargets(pgStack);
    } else {
      if (pgStack) pgStack.style.display = 'none';
      ugStack.style.display = '';
      setSectionHeight(ugStack);
      pinColumns(ugStack);
      initStates(ugStack);
      calcTargets(ugStack);
    }

    tabBtns.forEach(function (btn) {
      btn.classList.toggle('tab-btn--active', btn.dataset.tab === tab);
    });

    startLoop();
  }

  tabBtns.forEach(function (btn) {
    btn.addEventListener('click', function () { switchTab(btn.dataset.tab); });
  });

  /* ── Scroll listener ────────────────────────────────────────────── */

  function onScroll() {
    var w = activeTab === 'pg' ? pgStack : ugStack;
    calcTargets(w);
    startLoop();
  }

  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── Resize ─────────────────────────────────────────────────────── */

  window.addEventListener('resize', function () {
    var w = activeTab === 'pg' ? pgStack : ugStack;
    setSectionHeight(w);
    pinColumns(ugStack);
    if (pgStack) pinColumns(pgStack);
    initStates(w);
    calcTargets(w);
    startLoop();
  });

  /* ── Init ────────────────────────────────────────────────────────── */

  setSectionHeight(ugStack);
  pinColumns(ugStack);
  initStates(ugStack);
  calcTargets(ugStack);
  // Apply initial positions immediately
  cardStates.forEach(function (s) {
    s.current = s.target;
    if (s.current !== 0) {
      s.el.style.transform = 'translateY(' + s.current.toFixed(1) + 'px)';
    }
  });
  if (pgStack) pinColumns(pgStack);

}());
