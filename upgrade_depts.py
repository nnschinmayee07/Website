#!/usr/bin/env python3
"""Upgrade all non-CSE department pages:
1. Replace flip cards with CSE hover cards
2. Add scroll-spy, auto-accordion, sidebar accordion logic
3. Fix body background to white
"""
import re, os, subprocess

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

# ─── NEW CSS (CSE hover card style) ───
NEW_FCARD_CSS = """    .fcard-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
    .fcard { width: 100%; aspect-ratio: 3/4; border-radius: 12px; overflow: hidden; position: relative; cursor: pointer; background: linear-gradient(135deg, #2A2F40, #3A4050); }
    .fcard img { width: 100%; height: 100%; object-fit: cover; object-position: top; transition: transform 0.4s ease; }
    .fcard:hover img { transform: scale(1.05); }
    .fcard__ini { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 2rem; color: rgba(255,255,255,0.3); position: absolute; inset: 0; }
    .fcard__overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px 18px; background: linear-gradient(transparent, rgba(0,0,0,0.85)); z-index: 2; transition: opacity 0.3s; }
    .fcard__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.85rem; color: #fff; }
    .fcard__role { font-size: 0.68rem; color: rgba(255,255,255,0.6); }

    .fcard::before { content: ''; position: absolute; top: 0; right: 0; width: 100%; height: 100%; background: #E85D1F; clip-path: circle(0% at 100% 0%); transition: clip-path 0.5s cubic-bezier(0.25,0.46,0.45,0.94); z-index: 3; }
    .fcard:hover::before { clip-path: circle(150% at 100% 0%); }

    .fcard::after { content: ''; position: absolute; inset: 0; background: rgba(11,15,26,0.85); opacity: 0; transition: opacity 0.3s ease 0.15s; z-index: 4; }
    .fcard:hover::after { opacity: 1; }
    .fcard:hover .fcard__overlay { opacity: 0; }

    .fcard__hover-info { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; text-align: center; z-index: 5; opacity: 0; transform: translateY(10px); transition: opacity 0.35s ease 0.2s, transform 0.35s ease 0.2s; }
    .fcard:hover .fcard__hover-info { opacity: 1; transform: translateY(0); }
    .fcard__hover-name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.05rem; color: #fff; margin-bottom: 4px; }
    .fcard__hover-role { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-bottom: 12px; }
    .fcard__hover-spec { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600; color: #E85D1F; margin-bottom: 20px; letter-spacing: 0.04em; }
    .fcard__hover-btn { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; color: #fff; text-decoration: none; padding: 8px 20px; border: 1px solid #fff; border-radius: 6px; transition: all 0.2s; }
    .fcard__hover-btn:hover { background: #fff; color: #0B0F1A; }"""

# ─── NEW JS (scroll-spy + auto-accordion) ───
NEW_JS_ADDITIONS = """
    // Scroll-spy — separate IIFE
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
    })();

    // Auto open/close accordions on scroll
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

# ─── UPGRADED SIDEBAR CLICK HANDLER ───
OLD_SIDEBAR_SCROLL = """          // Scroll to target after a brief delay to let panel show
          if (target) {
            setTimeout(function () {
              var el = document.getElementById(target);
              if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 50);
          }"""

NEW_SIDEBAR_SCROLL = """          // Scroll to target — close other accordions, open the right one
          if (target) {
            setTimeout(function () {
              var el = document.getElementById(target);
              if (!el) return;
              // Close all open accordions first
              document.querySelectorAll('.sub-accordion.is-open').forEach(function(a) {
                a.classList.remove('is-open');
              });
              // Open accordion if target is inside one or is the header
              var accordion = el.closest ? el.closest('.sub-accordion') : null;
              if (!accordion && el.parentElement && el.parentElement.classList && el.parentElement.classList.contains('sub-accordion')) {
                accordion = el.parentElement;
              }
              if (accordion) accordion.classList.add('is-open');
              el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 120);
          }"""

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ═══ 1. FIX BACKGROUND ═══
    content = content.replace('background: #F4F1EA;', 'background: #FFFFFF;')

    # ═══ 2. REPLACE FLIP CARD CSS WITH HOVER CARD CSS ═══
    # Remove old flip card CSS block
    old_css = re.search(
        r'    \.fcard-grid \{[^}]+\}\s*\n'
        r'    \.fcard \{[^}]+perspective[^}]+\}\s*\n'
        r'    \.fcard__inner \{[^}]+\}\s*\n'
        r'    \.fcard:hover \.fcard__inner \{[^}]+\}\s*\n'
        r'    \.fcard__front, \.fcard__back \{[^}]+\}\s*\n'
        r'    \.fcard__front \{[^}]+\}\s*\n'
        r'    \.fcard__front img \{[^}]+\}\s*\n'
        r'    \.fcard__ini \{[^}]+\}\s*\n'
        r'    \.fcard__overlay \{[^}]+\}\s*\n'
        r'    \.fcard__name \{[^}]+\}\s*\n'
        r'    \.fcard__role \{[^}]+\}\s*\n'
        r'    \.fcard__back \{[^}]+\}\s*\n'
        r'    \.fcard__back-name \{[^}]+\}\s*\n'
        r'    \.fcard__back-role \{[^}]+\}\s*\n'
        r'    \.fcard__back-spec \{[^}]+\}\s*\n'
        r'    \.fcard__back-btn \{[^}]+\}\s*\n'
        r'    \.fcard__back-btn:hover \{[^}]+\}',
        content
    )

    if old_css:
        content = content[:old_css.start()] + NEW_FCARD_CSS + content[old_css.end():]
        print(f'  {dept}: CSS replaced (regex match)')
    else:
        # Fallback: replace line by line
        # Remove old classes and insert new
        lines = content.split('\n')
        new_lines = []
        skip_until_next = False
        inserted = False
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detect start of old fcard CSS
            if '.fcard-grid {' in line and not inserted:
                # Skip all old fcard CSS lines until we hit a non-fcard line
                while i < len(lines) and ('fcard' in lines[i] or lines[i].strip() == ''):
                    if lines[i].strip() == '' and i+1 < len(lines) and 'fcard' not in lines[i+1]:
                        break
                    i += 1
                new_lines.append(NEW_FCARD_CSS)
                inserted = True
                continue
            new_lines.append(line)
            i += 1

        if inserted:
            content = '\n'.join(new_lines)
            print(f'  {dept}: CSS replaced (line-by-line)')
        else:
            print(f'  {dept}: WARNING - could not find fcard CSS')

    # ═══ 3. TRANSFORM FLIP CARD HTML TO HOVER CARD HTML ═══
    # Pattern: each flip card block
    def transform_fcard(match):
        block = match.group(0)
        # Extract data
        author = re.search(r'data-author="([^"]*)"', block)
        img = re.search(r'<img src="([^"]*)" alt="([^"]*)" onerror="[^"]*"', block)
        ini = re.search(r'<div class="fcard__ini"[^>]*>([^<]*)</div>', block)
        name = re.search(r'<div class="fcard__name">([^<]*)</div>', block)
        role = re.search(r'<div class="fcard__role">([^<]*)</div>', block)
        back_name = re.search(r'<div class="fcard__back-name">([^<]*)</div>', block)
        back_role = re.search(r'<div class="fcard__back-role">([^<]*)</div>', block)
        back_spec = re.search(r'<div class="fcard__back-spec">([^<]*)</div>', block)
        back_btn = re.search(r'<a href="([^"]*)" class="fcard__back-btn">([^<]*)</a>', block)

        if not author or not name:
            return block  # Can't transform, leave as-is

        author_val = author.group(1)
        img_src = img.group(1) if img else ''
        img_alt = img.group(2) if img else name.group(1)
        ini_val = ini.group(1) if ini else 'XX'
        name_val = name.group(1)
        role_val = role.group(1) if role else ''
        spec_val = back_spec.group(1) if back_spec else 'Engineering'
        btn_href = back_btn.group(1) if back_btn else f'faculty-profile.html?name={name_val.replace(" ", "%20")}'
        btn_text = 'View Research'

        return f'''          <div class="fcard" data-author="{author_val}">
              <img src="{img_src}" alt="{img_alt}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'" />
              <div class="fcard__ini" style="display:none">{ini_val}</div>
              <div class="fcard__overlay">
                <div class="fcard__name">{name_val}</div>
                <div class="fcard__role">{role_val}</div>
              </div>
              <div class="fcard__hover-info">
                <div class="fcard__hover-name">{name_val}</div>
                <div class="fcard__hover-role">{role_val}</div>
                <div class="fcard__hover-spec">{spec_val}</div>
                <a href="{btn_href}" class="fcard__hover-btn">{btn_text}</a>
              </div>
          </div>'''

    # Match each flip card block
    content = re.sub(
        r'          <div class="fcard" data-author="[^"]*">.*?</div>\s*</div>\s*</div>',
        transform_fcard,
        content,
        flags=re.DOTALL
    )

    # Clean up any leftover fcard__inner or fcard__front wrappers that didn't match
    # (shouldn't happen but just in case)
    content = content.replace('<div class="fcard__inner">', '')
    content = content.replace('<div class="fcard__front">', '')

    # Count cards
    hover_cards = content.count('fcard__hover-info')
    flip_cards = content.count('fcard__back')
    print(f'  {dept}: hover_cards={hover_cards} remaining_flip={flip_cards}')

    # ═══ 4. UPGRADE SIDEBAR CLICK HANDLER ═══
    if OLD_SIDEBAR_SCROLL in content:
        content = content.replace(OLD_SIDEBAR_SCROLL, NEW_SIDEBAR_SCROLL)
        print(f'  {dept}: sidebar scroll upgraded')
    else:
        print(f'  {dept}: sidebar scroll already upgraded or not found')

    # ═══ 5. ADD SCROLL-SPY + AUTO-ACCORDION JS ═══
    if 'Scroll-spy' not in content:
        # Insert before </script>
        content = content.replace('\n  </script>', NEW_JS_ADDITIONS + '\n  </script>')
        print(f'  {dept}: scroll-spy + auto-accordion added')
    else:
        print(f'  {dept}: scroll-spy already present')

    # ═══ 6. FIX RESPONSIVE FCARD ═══
    # Update responsive breakpoint for fcard
    content = content.replace(
        '      .fcard { height: 240px; }',
        '      .fcard { height: auto; }'
    )

    # ═══ 7. FIX PANEL CSS TO MATCH CSE ═══
    content = content.replace(
        '.dept-panel { display: none; padding: 48px; max-width: 1100px; margin: 0 auto; }',
        '.dept-panel { display: none; padding: 40px 48px; max-width: none; margin: 0; }'
    )

    # ═══ 8. SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # ═══ 9. VERIFY JS ═══
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else f'ERR: {r.stderr[:100]}'
    else:
        js = 'NO_SCRIPT'

    changed = content != original
    print(f'{dept}: JS={js} changed={changed}\n')

print('Done.')
