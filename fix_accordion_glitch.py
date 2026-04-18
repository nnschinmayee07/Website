#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix accordion glitch: 3 competing mechanisms fight over is-open state.
Root causes:
  1. onclick on entire accordion div (not just header) — clicking content toggles it
  2. Scroll-spy closes ALL accordions on every intersection — overrides manual state
  3. Auto-accordion opens/closes on threshold 0.5 — fights with both above

Fix:
  1. Remove onclick from accordion divs — use JS on header only
  2. Scroll-spy: only highlight sidebar, do NOT touch accordion state
  3. Remove auto-accordion IIFE entirely — it's the main cause of fighting
  4. Add proper header-only click handler in JS
"""
import sys, io, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALL = ['cse.html', 'ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in ALL:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ FIX 1: Remove onclick from sub-accordion divs ═══
    count = content.count('class="sub-accordion" onclick="this.classList.toggle(\'is-open\')"')
    if count:
        content = content.replace(
            'class="sub-accordion" onclick="this.classList.toggle(\'is-open\')"',
            'class="sub-accordion"'
        )
        changes.append(f'1. Removed {count} onclick from accordion divs')
    # Also handle id before class
    for m in re.finditer(r'(id="[^"]*") (class="sub-accordion") onclick="this\.classList\.toggle\(\'is-open\'\)"', content):
        pass  # Already handled by generic replace — check if any remain
    remaining = content.count("onclick=\"this.classList.toggle('is-open')\"")
    # Don't touch subject-row onclick — those are different
    accordion_onclick = len(re.findall(r'sub-accordion[^>]*onclick', content))
    if accordion_onclick:
        content = re.sub(
            r'(class="sub-accordion"[^>]*?) onclick="this\.classList\.toggle\(\'is-open\'\)"',
            r'\1',
            content
        )
        content = re.sub(
            r'(id="[^"]*" class="sub-accordion") onclick="this\.classList\.toggle\(\'is-open\'\)"',
            r'\1',
            content
        )
        changes.append(f'1b. Removed {accordion_onclick} more onclick via regex')

    # ═══ FIX 2: Replace scroll-spy to NOT touch accordion state ═══
    old_spy = """    // Scroll-spy — separate IIFE
    (function () {
      var targets = [];
      document.querySelectorAll('.ds-item[data-ds-target]').forEach(function(item) {
        var id = item.getAttribute('data-ds-target');
        var el = document.getElementById(id);
        if (el) targets.push({ el: el, item: item });
      });
      if (!targets.length) return;
      var spyReady = false;
      setTimeout(function () { spyReady = true; }, 600);
      var observer = new IntersectionObserver(function(entries) {
        if (!spyReady) return;
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          var matched = targets.find(function(t) { return t.el === entry.target; });
          if (!matched) return;
          if (matched.item.style.display === 'none') return;
          document.querySelectorAll('.ds-item').forEach(function(i) { i.classList.remove('is-active'); });
          matched.item.classList.add('is-active');
          document.querySelectorAll('.sub-accordion.is-open').forEach(function(a) {
            a.classList.remove('is-open');
          });
          var accordion = matched.el.closest ? matched.el.closest('.sub-accordion') : null;
          if (accordion) accordion.classList.add('is-open');
        });
      }, { threshold: 0.4, rootMargin: '-80px 0px -40% 0px' });
      targets.forEach(function(t) { observer.observe(t.el); });
    })();"""

    new_spy = """    // Scroll-spy — highlights sidebar only, does NOT touch accordion state
    (function () {
      var targets = [];
      document.querySelectorAll('.ds-item[data-ds-target]').forEach(function(item) {
        var id = item.getAttribute('data-ds-target');
        var el = document.getElementById(id);
        if (el) targets.push({ el: el, item: item });
      });
      if (!targets.length) return;
      var spyReady = false;
      setTimeout(function () { spyReady = true; }, 600);
      var observer = new IntersectionObserver(function(entries) {
        if (!spyReady) return;
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          var matched = targets.find(function(t) { return t.el === entry.target; });
          if (!matched) return;
          if (matched.item.style.display === 'none') return;
          document.querySelectorAll('.ds-item').forEach(function(i) { i.classList.remove('is-active'); });
          matched.item.classList.add('is-active');
        });
      }, { threshold: 0.3, rootMargin: '-80px 0px -40% 0px' });
      targets.forEach(function(t) { observer.observe(t.el); });
    })();"""

    if old_spy in content:
        content = content.replace(old_spy, new_spy)
        changes.append('2. Scroll-spy: removed accordion manipulation')
    else:
        changes.append('2. SKIP - scroll-spy pattern not found (checking variant)')

    # ═══ FIX 3: Remove auto-accordion IIFE entirely ═══
    old_auto = """    // Auto open/close accordions on scroll
    (function () {
      var accordions = document.querySelectorAll('.sub-accordion');
      if (!accordions.length) return;
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-open');
          } else {
            entry.target.classList.remove('is-open');
          }
        });
      }, { threshold: 0.5 });
      accordions.forEach(function (acc) { observer.observe(acc); });
    })();"""

    if old_auto in content:
        content = content.replace(old_auto, '')
        changes.append('3. Removed auto-accordion IIFE')
    else:
        changes.append('3. SKIP - auto-accordion not found')

    # ═══ FIX 4: Add header-only click handler for accordions ═══
    accordion_handler = """    // Accordion toggle — header clicks only (no content click interference)
    (function () {
      document.querySelectorAll('.sub-accordion__header').forEach(function (header) {
        header.addEventListener('click', function (e) {
          e.stopPropagation();
          var accordion = header.parentElement;
          if (accordion && accordion.classList.contains('sub-accordion')) {
            accordion.classList.toggle('is-open');
          }
        });
      });
    })();"""

    if 'Accordion toggle' not in content:
        # Insert before </script>
        content = content.replace('\n  </script>', '\n' + accordion_handler + '\n  </script>')
        changes.append('4. Added header-only accordion click handler')
    else:
        changes.append('4. SKIP - accordion handler already present')

    # ═══ SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # ═══ VERIFY JS ═══
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else f'ERR: {r.stderr[:100]}'
    else:
        js = 'NO_SCRIPT'

    print(f'\n{dept}: JS={js}')
    for c in changes:
        print(f'  {c}')

print('\nDone.')
