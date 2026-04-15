#!/usr/bin/env python3
"""Add context-aware left sidebar + orange streak to ALL department pages."""
import re, glob, os

# ═══ New CSS to inject ═══
SIDEBAR_CSS = '''
    /* ── Context-aware left sidebar ── */
    .dept-body { display: flex; min-height: calc(100vh - 200px); }
    .ctx-sidebar {
      position: sticky; top: 48px; left: 0; width: 220px; min-width: 220px;
      height: calc(100vh - 48px); background: #0B0F1A; z-index: 30;
      display: flex; flex-direction: column; padding: 28px 0;
      overflow-y: auto; border-right: 1px solid rgba(255,255,255,0.05);
    }
    .ctx-sidebar::-webkit-scrollbar { width: 4px; }
    .ctx-sidebar::-webkit-scrollbar-thumb { background: rgba(232,93,31,0.2); border-radius: 2px; }
    .ctx-sidebar__title {
      font-family: 'Raleway', sans-serif; font-size: 0.62rem; font-weight: 800;
      text-transform: uppercase; letter-spacing: 0.14em; color: rgba(255,255,255,0.25);
      padding: 0 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px;
    }
    .ctx-sidebar__items { list-style: none; padding: 0; transition: opacity 0.25s ease; }
    .ctx-sidebar__items.is-fading { opacity: 0; }
    .ctx-item {
      display: flex; align-items: center; padding: 9px 20px; cursor: pointer;
      border-left: 3px solid transparent; transition: all 0.2s ease;
      text-decoration: none; color: inherit;
    }
    .ctx-item:hover { background: rgba(232,93,31,0.06); border-left-color: rgba(232,93,31,0.3); }
    .ctx-item.is-active { border-left-color: #E85D1F; background: rgba(232,93,31,0.08); }
    .ctx-item__dot {
      width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.15);
      flex-shrink: 0; transition: all 0.25s ease; margin-right: 12px;
    }
    .ctx-item.is-active .ctx-item__dot { background: #E85D1F; box-shadow: 0 0 6px rgba(232,93,31,0.4); }
    .ctx-item__label {
      font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600;
      color: rgba(255,255,255,0.4); transition: color 0.2s;
    }
    .ctx-item:hover .ctx-item__label { color: rgba(255,255,255,0.7); }
    .ctx-item.is-active .ctx-item__label { color: rgba(255,255,255,0.9); }
    .dept-main { flex: 1; min-width: 0; }

    /* ── Orange streak ── */
    @keyframes orange-streak {
      0%   { transform: scaleX(0); opacity: 1; }
      65%  { transform: scaleX(1); opacity: 1; }
      100% { transform: scaleX(1); opacity: 0; }
    }
    .streak {
      position: fixed; top: 0; left: 220px; right: 0; height: 3px;
      background: linear-gradient(90deg, #E85D1F 0%, rgba(232,93,31,0.4) 60%, transparent 100%);
      transform-origin: left; transform: scaleX(0); opacity: 0;
      z-index: 9999; pointer-events: none; border-radius: 0 2px 2px 0;
    }
    .streak.is-firing { animation: orange-streak 0.55s cubic-bezier(0.25,0.46,0.45,0.94) forwards; }
'''

SIDEBAR_RESPONSIVE = '''      .ctx-sidebar { display: none; }
      .streak { left: 0; }'''

# ═══ Sub-items per tab ═══
TAB_SUBITEMS = {
    'overview': [('About the Dept', 'about-dept'), ('HOD Message', 'hod-msg'), ('Teaching Methodology', 'teaching-method'), ('Labs', 'labs-section')],
    'objectives': [('Programme Objectives', 'peo-section'), ('Programme Outcomes', 'po-section'), ('OBE', 'obe-section'), ('Handbook', 'handbook-section')],
    'faculty': [('Faculty Grid', 'faculty-grid-section')],
    'academics': [('Syllabus PDFs', 'syll-pdfs'), ('Syllabus Explorer', 'syll-explorer')],
    'achievements': [('Achievements', 'achieve-section'), ('Placements', 'placement-section'), ('Publications', 'pub-section'), ('Internships', 'intern-section')],
}

def build_sidebar_html():
    items = ''
    for tab, subs in TAB_SUBITEMS.items():
        for label, target_id in subs:
            items += f'      <a class="ctx-item" data-ctx-tab="{tab}" data-ctx-target="{target_id}"><span class="ctx-item__dot"></span><span class="ctx-item__label">{label}</span></a>\n'
    return items

SIDEBAR_HTML = f'''  <div class="streak" id="navStreak"></div>

  <div class="dept-body">
    <!-- Context-aware sidebar -->
    <aside class="ctx-sidebar" id="ctxSidebar">
      <div class="ctx-sidebar__title">Quick Nav</div>
      <div class="ctx-sidebar__items" id="ctxItems">
{build_sidebar_html()}      </div>
    </aside>

    <!-- Main content wrapper -->
    <div class="dept-main">
'''

SIDEBAR_CLOSE = '''    </div>
  </div>'''

SIDEBAR_JS = '''
    // ── Context-aware sidebar ──
    (function () {
      var ctxItems = document.querySelectorAll('.ctx-item');
      var ctxContainer = document.getElementById('ctxItems');
      var streak = document.getElementById('navStreak');

      function fireStreak() {
        if (!streak) return;
        streak.classList.remove('is-firing');
        void streak.offsetWidth;
        streak.classList.add('is-firing');
        setTimeout(function () { streak.classList.remove('is-firing'); }, 600);
      }

      // Show only items matching the active tab
      function updateSidebar(activeTab) {
        if (ctxContainer) {
          ctxContainer.classList.add('is-fading');
          setTimeout(function () {
            ctxItems.forEach(function (item) {
              var itemTab = item.getAttribute('data-ctx-tab');
              item.style.display = (itemTab === activeTab) ? 'flex' : 'none';
              item.classList.remove('is-active');
            });
            ctxContainer.classList.remove('is-fading');
          }, 250);
        }
      }

      // Hook into existing tab switching
      var origTabs = document.querySelectorAll('.dept-tab');
      origTabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          var tabId = tab.getAttribute('data-tab');
          updateSidebar(tabId);
          fireStreak();
        });
      });

      // Also hook qbar buttons
      document.querySelectorAll('.qbar__btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var tabId = btn.getAttribute('data-qtab');
          updateSidebar(tabId);
          fireStreak();
        });
      });

      // Click on sidebar item -> scroll to target
      ctxItems.forEach(function (item) {
        item.addEventListener('click', function () {
          var targetId = item.getAttribute('data-ctx-target');
          var el = document.getElementById(targetId);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            ctxItems.forEach(function (i) { i.classList.remove('is-active'); });
            item.classList.add('is-active');
            fireStreak();
          }
        });
      });

      // Initialize: show overview items
      updateSidebar('overview');
    })();'''

# ═══ IDs to add to content elements ═══
ID_MAPPINGS = {
    'class="panel-heading">About the Department': 'id="about-dept" class="panel-heading">About the Department',
    'class="hod-msg"': 'id="hod-msg" class="hod-msg"',
    '>Innovative Teaching Methodology</div>': 'id="teaching-method">Innovative Teaching Methodology</div>',
    '>Academic Laboratories': 'id="labs-section">Academic Laboratories',
    '>Programme Educational Objectives</': 'id="peo-section">Programme Educational Objectives</',
    '>Programme Outcomes (POs)</': 'id="po-section">Programme Outcomes (POs)</',
    '>Outcome Based Education': 'id="obe-section">Outcome Based Education',
    '>Handbook</div>': 'id="handbook-section">Handbook</div>',
    'class="fcard-grid"': 'id="faculty-grid-section" class="fcard-grid"',
    '>Syllabus PDFs</div>': 'id="syll-pdfs">Syllabus PDFs</div>',
    '>Semester-wise Syllabus Explorer</div>': 'id="syll-explorer">Semester-wise Syllabus Explorer</div>',
    'class="achieve-grid"': 'id="achieve-section" class="achieve-grid"',
    '>Placements</div>': 'id="placement-section">Placements</div>',
    '>Publications</div>': 'id="pub-section">Publications</div>',
    '>Internships and Placements</div>': 'id="intern-section">Internships and Placements</div>',
}

# ═══ Process each department file ═══
for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    bn = os.path.basename(filepath)
    if bn in ('faculty-profile.html', 'ug.html', 'pg.html') or bn.startswith('cse-'):
        continue

    dept = bn.replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has sidebar
    if 'ctx-sidebar' in content:
        print(f'{dept}: already has sidebar, skipping')
        continue

    # Skip if no tabs
    if 'dept-tabs' not in content:
        print(f'{dept}: no tabs, skipping')
        continue

    # 1. Add CSS before @media
    media_pattern = '    @media (max-width: 768px) {'
    if media_pattern in content:
        content = content.replace(media_pattern, SIDEBAR_CSS + '\n' + media_pattern)
        # Add responsive rules inside media query
        content = content.replace(
            '      .qbar { display: none; }',
            '      .qbar { display: none; }\n' + SIDEBAR_RESPONSIVE
        )
        if '.qbar { display: none; }' not in content:
            # Try adding after the media opening
            content = content.replace(media_pattern + '\n', media_pattern + '\n' + SIDEBAR_RESPONSIVE + '\n')

    # 2. Add IDs to content elements (only first occurrence of each)
    for old, new in ID_MAPPINGS.items():
        if old in content and new not in content:
            content = content.replace(old, new, 1)

    # 3. Wrap content in sidebar layout
    # Find the qbar div and wrap everything after it in dept-body
    qbar_end = '  </div>\n\n  <!-- '
    # Find the first panel after qbar
    qbar_close_match = re.search(r'(  </div>\s*\n\s*<!-- .*TAB 1)', content)
    if qbar_close_match:
        insert_pos = qbar_close_match.start()
        # Insert sidebar HTML before TAB 1
        content = content[:insert_pos] + '  </div>\n\n' + SIDEBAR_HTML + '\n  ' + content[insert_pos + len(qbar_close_match.group(0)) - len('<!-- ' + qbar_close_match.group(0).split('<!-- ')[-1]):]
    else:
        # Simpler: insert after qbar closing div, before first panel
        first_panel = '  <div class="dept-panel is-active"'
        if first_panel in content:
            content = content.replace(first_panel, SIDEBAR_HTML + '\n  ' + first_panel)

    # 4. Close the dept-body wrapper before </script>
    content = content.replace('\n  <script>', SIDEBAR_CLOSE + '\n\n  <script>')

    # 5. Add sidebar JS before closing </script>
    content = content.replace('\n  </script>', SIDEBAR_JS + '\n  </script>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    has_sidebar = 'ctx-sidebar' in content
    has_streak = 'navStreak' in content
    print(f'{dept}: sidebar={has_sidebar} streak={has_streak}')

print('\nDone.')
