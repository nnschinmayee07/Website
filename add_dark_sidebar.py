#!/usr/bin/env python3
"""Add fixed dark left sidebar to all department pages."""
import glob, os, re, subprocess

SIDEBAR_CSS = """
    /* ── Dark left sidebar ── */
    .dark-sidebar {
      position: fixed; left: 0; top: 0; bottom: 0; width: 200px;
      background: #0B0F1A; z-index: 35; padding-top: 120px;
      overflow-y: auto; border-right: 1px solid rgba(255,255,255,0.06);
    }
    .dark-sidebar::-webkit-scrollbar { width: 4px; }
    .dark-sidebar::-webkit-scrollbar-thumb { background: rgba(232,93,31,0.2); border-radius: 2px; }
    .dark-sidebar__title {
      font-family: 'Raleway', sans-serif; font-size: 0.6rem; font-weight: 800;
      text-transform: uppercase; letter-spacing: 0.14em; color: rgba(255,255,255,0.2);
      padding: 0 20px 14px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 8px;
    }
    .ds-item {
      display: flex; align-items: center; padding: 8px 20px; cursor: pointer;
      border-left: 3px solid transparent; transition: all 0.2s; text-decoration: none; color: inherit;
    }
    .ds-item:hover { background: rgba(232,93,31,0.06); }
    .ds-item.is-active { border-left-color: #E85D1F; background: rgba(232,93,31,0.08); }
    .ds-item__dot {
      width: 5px; height: 5px; border-radius: 50%; background: rgba(255,255,255,0.15);
      flex-shrink: 0; margin-right: 12px; transition: all 0.2s;
    }
    .ds-item.is-active .ds-item__dot { background: #E85D1F; box-shadow: 0 0 6px rgba(232,93,31,0.4); }
    .ds-item__label {
      font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 600;
      color: rgba(255,255,255,0.35); transition: color 0.2s; white-space: nowrap;
      overflow: hidden; text-overflow: ellipsis;
    }
    .ds-item:hover .ds-item__label { color: rgba(255,255,255,0.65); }
    .ds-item.is-active .ds-item__label { color: rgba(255,255,255,0.9); }

    /* Push all content right to make room */
    .site-header, .dept-nav, .dept-hero, .dept-tabs, .dept-panel, .qbar, .streak {
      margin-left: 200px;
    }
    .qbar { right: 0; }
"""

SIDEBAR_RESPONSIVE = """      .dark-sidebar { display: none; }
      .site-header, .dept-nav, .dept-hero, .dept-tabs, .dept-panel, .qbar, .streak { margin-left: 0; }"""

# Sub-items per tab
TAB_ITEMS = {
    'overview': ['HOD Message', 'Vision, Mission', 'Teaching', 'History', 'Labs'],
    'objectives': ['PEOs', 'Outcomes (POs)', 'OBE', 'Handbook'],
    'faculty': ['All Faculty'],
    'academics': ['Syllabus PDFs', 'Course Catalog', 'Syllabus Explorer'],
    'achievements': ['Achievements', 'Placements', 'Honours', 'Publications', 'Internships'],
}

def build_sidebar_html():
    html = ''
    for tab, items in TAB_ITEMS.items():
        for label in items:
            html += f'    <a class="ds-item" data-ds-tab="{tab}" data-ds-label="{label}"><span class="ds-item__dot"></span><span class="ds-item__label">{label}</span></a>\n'
    return html

SIDEBAR_HTML = '''  <!-- Dark left sidebar -->
  <aside class="dark-sidebar" id="darkSidebar">
    <div class="dark-sidebar__title">Quick Nav</div>
''' + build_sidebar_html() + '  </aside>\n'

SIDEBAR_JS = """
    // Dark sidebar — show items for active tab
    (function () {
      var dsItems = document.querySelectorAll('.ds-item');
      var streak = document.getElementById('navStreak');

      function fireStreak() {
        if (!streak) return;
        streak.classList.remove('is-firing');
        void streak.offsetWidth;
        streak.classList.add('is-firing');
        setTimeout(function () { streak.classList.remove('is-firing'); }, 600);
      }

      function updateSidebar(activeTab) {
        dsItems.forEach(function (item) {
          var show = item.getAttribute('data-ds-tab') === activeTab;
          item.style.display = show ? 'flex' : 'none';
          item.classList.remove('is-active');
        });
        // Activate first visible item
        var first = document.querySelector('.ds-item[data-ds-tab="' + activeTab + '"]');
        if (first) first.classList.add('is-active');
      }

      // Hook into tab clicks
      document.querySelectorAll('.dept-tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
          updateSidebar(tab.getAttribute('data-tab'));
          fireStreak();
        });
      });

      // Hook into qbar clicks
      document.querySelectorAll('.qbar__btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          updateSidebar(btn.getAttribute('data-qtab'));
          fireStreak();
        });
      });

      // Sidebar item click — mark active + fire streak
      dsItems.forEach(function (item) {
        item.addEventListener('click', function () {
          var siblings = document.querySelectorAll('.ds-item[data-ds-tab="' + item.getAttribute('data-ds-tab') + '"]');
          siblings.forEach(function (s) { s.classList.remove('is-active'); });
          item.classList.add('is-active');
          fireStreak();
        });
      });

      // Initialize
      updateSidebar('overview');
    })();"""

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    bn = os.path.basename(filepath)
    if bn in ('faculty-profile.html', 'ug.html', 'pg.html') or bn.startswith('cse-'):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'dept-tabs' not in content:
        continue
    if 'dark-sidebar' in content:
        print(f'{bn}: already has dark sidebar, skipping')
        continue

    dept = bn.replace('.html', '')

    # 1. Add CSS before @media
    content = content.replace(
        '    @media (max-width: 768px) {',
        SIDEBAR_CSS + '\n    @media (max-width: 768px) {'
    )

    # 2. Add responsive rules
    if '.qbar { display: none; }' in content:
        content = content.replace(
            '      .qbar { display: none; }',
            '      .qbar { display: none; }\n' + SIDEBAR_RESPONSIVE
        )

    # 3. Add sidebar HTML right after <body>
    content = content.replace('<body>\n', '<body>\n' + SIDEBAR_HTML + '\n')

    # 4. Remove old fireStreak JS (we'll include it in the new sidebar JS)
    content = re.sub(r'\n    // Orange streak on tab click.*?\}\)\(\);', '', content, flags=re.DOTALL)
    content = re.sub(r'\n    // ── Orange streak on tab click ──.*?\}\)\(\);', '', content, flags=re.DOTALL)

    # 5. Add sidebar JS before </script>
    content = content.replace('\n  </script>', SIDEBAR_JS + '\n  </script>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify JS
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else 'ERR'
    else:
        js = 'NONE'

    print(f'{dept}: dark sidebar added, js={js}')
