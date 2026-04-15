#!/usr/bin/env python3
"""Add in-panel sidebar to each tab panel in all department pages."""
import glob, os, re, subprocess

SIDEBAR_CSS = """
    /* ── In-panel sidebar ── */
    .panel-layout { display: flex; gap: 0; }
    .panel-sidebar {
      width: 180px; min-width: 180px; padding: 20px 0; border-right: 1px solid rgba(0,0,0,0.06);
      position: sticky; top: 48px; height: fit-content; align-self: flex-start;
    }
    .panel-sidebar__item {
      display: flex; align-items: center; padding: 8px 16px; cursor: pointer;
      border-left: 3px solid transparent; transition: all 0.2s; text-decoration: none; color: inherit;
    }
    .panel-sidebar__item:hover { background: rgba(232,93,31,0.04); border-left-color: rgba(232,93,31,0.3); }
    .panel-sidebar__item.is-active { border-left-color: #E85D1F; background: rgba(232,93,31,0.06); }
    .panel-sidebar__dot { width: 5px; height: 5px; border-radius: 50%; background: rgba(0,0,0,0.15); margin-right: 10px; flex-shrink: 0; transition: background 0.2s; }
    .panel-sidebar__item.is-active .panel-sidebar__dot { background: #E85D1F; }
    .panel-sidebar__label { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 600; color: #888; transition: color 0.2s; }
    .panel-sidebar__item.is-active .panel-sidebar__label { color: #3A3A3A; font-weight: 700; }
    .panel-sidebar__item:hover .panel-sidebar__label { color: #555; }
    .panel-content { flex: 1; min-width: 0; padding-left: 32px; }
"""

TAB_ITEMS = {
    'overview': [('HOD Message', 'hod-msg'), ('Vision, Mission', 'vm-section'), ('Teaching', 'teaching-method'), ('Labs', 'labs-section')],
    'objectives': [('PEOs', 'peo-section'), ('Outcomes', 'po-section'), ('OBE', 'obe-section')],
    'faculty': [('All Faculty', 'faculty-grid-section')],
    'academics': [('Syllabus PDFs', 'syll-pdfs'), ('Catalog', 'catalog-section'), ('Explorer', 'syll-explorer')],
    'achievements': [('Achievements', 'achieve-section'), ('Placements', 'placement-section'), ('Publications', 'pub-section'), ('Internships', 'intern-section')],
}

SIDEBAR_JS = """
    // Panel sidebar scroll
    (function () {
      document.querySelectorAll('.panel-sidebar__item').forEach(function (item) {
        item.addEventListener('click', function (e) {
          e.preventDefault();
          var targetId = item.getAttribute('data-scroll-to');
          var el = document.getElementById(targetId);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            var siblings = item.parentElement.querySelectorAll('.panel-sidebar__item');
            siblings.forEach(function (s) { s.classList.remove('is-active'); });
            item.classList.add('is-active');
          }
        });
      });
    })();"""

def build_sidebar(tab_key):
    items = TAB_ITEMS.get(tab_key, [])
    if not items:
        return ''
    html = '    <nav class="panel-sidebar">\n'
    for i, (label, target) in enumerate(items):
        active = ' is-active' if i == 0 else ''
        html += f'      <a class="panel-sidebar__item{active}" data-scroll-to="{target}"><span class="panel-sidebar__dot"></span><span class="panel-sidebar__label">{label}</span></a>\n'
    html += '    </nav>\n'
    return html

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    bn = os.path.basename(filepath)
    if bn in ('faculty-profile.html', 'ug.html', 'pg.html') or bn.startswith('cse-'):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'dept-tabs' not in content or 'panel-sidebar' in content:
        continue

    dept = bn.replace('.html', '')

    # 1. Add CSS
    content = content.replace(
        '    @media (max-width: 768px) {',
        SIDEBAR_CSS + '\n    @media (max-width: 768px) {'
    )
    # Responsive
    if '.qbar { display: none; }' in content:
        content = content.replace(
            '      .qbar { display: none; }',
            '      .qbar { display: none; }\n      .panel-sidebar { display: none; }\n      .panel-content { padding-left: 0; }'
        )

    # 2. For each panel, wrap content in panel-layout with sidebar
    for tab_key in TAB_ITEMS:
        panel_id = f'panel-{tab_key}'
        sidebar = build_sidebar(tab_key)

        # Find panel heading
        pattern = rf'(id="{panel_id}"[^>]*>)\s*\n(\s*<h2[^>]*>.*?</h2>)\s*\n'
        match = re.search(pattern, content)
        if match:
            old_text = match.group(0)
            heading = match.group(2).strip()
            # Replace: keep heading above layout, then sidebar + content wrapper
            new_text = match.group(1) + '\n    ' + heading + '\n    <div class="panel-layout">\n' + sidebar + '    <div class="panel-content">\n'
            content = content.replace(old_text, new_text)

    # 3. Close panel-content + panel-layout before each panel's </div>
    # Find each panel's closing </div> (the one just before next panel or before <script>)
    # Replace "  </div>" that closes a panel with "    </div>\n    </div>\n  </div>"
    panel_ids = ['panel-overview', 'panel-objectives', 'panel-faculty', 'panel-academics', 'panel-achievements']

    for i, pid in enumerate(panel_ids):
        if pid not in content:
            continue
        # Find the start of this panel
        pstart = content.index(f'id="{pid}"')

        if i < len(panel_ids) - 1:
            # Find start of next panel
            next_pid = panel_ids[i + 1]
            if next_pid in content:
                pend = content.index(f'id="{next_pid}"', pstart + 1)
                # Find the </div> just before next panel
                before_next = content[pstart:pend]
                # The last </div>\n before the next panel is the panel close
                last_close = before_next.rfind('  </div>')
                if last_close > 0:
                    abs_pos = pstart + last_close
                    content = content[:abs_pos] + '    </div>\n    </div>\n  </div>\n\n  ' + content[abs_pos + len('  </div>') + 1:]
        else:
            # Last panel - find </div> before <script>
            script_idx = content.index('\n  <script>', pstart)
            before_script = content[pstart:script_idx]
            last_close = before_script.rfind('  </div>')
            if last_close > 0:
                abs_pos = pstart + last_close
                content = content[:abs_pos] + '    </div>\n    </div>\n  </div>\n\n' + content[abs_pos + len('  </div>') + 1:]

    # 4. Add IDs if missing
    id_adds = [
        ('Vision and Mission', 'vm-section'),
        ('Innovative Teaching', 'teaching-method'),
        ('Academic Laboratories', 'labs-section'),
        ('Online Course Catalog', 'catalog-section'),
        ('Roll of Honour', 'honour-section'),
    ]
    for text, id_val in id_adds:
        old = f'>{text}</'
        new = f' id="{id_val}">{text}</'
        if old in content and new not in content:
            content = content.replace(old, new, 1)

    # 5. Add JS
    if 'Panel sidebar scroll' not in content:
        content = content.replace('\n  </script>', SIDEBAR_JS + '\n  </script>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else 'ERR'
    else:
        js = 'NONE'

    scount = content.count('panel-sidebar">')
    print(f'{dept}: {scount} sidebars, js={js}')
