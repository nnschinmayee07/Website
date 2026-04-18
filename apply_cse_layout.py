#!/usr/bin/env python3
"""Apply CSE flex layout to all other department pages."""
import re, os, subprocess

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ 1. REPLACE OLD SIDEBAR CSS WITH NEW ═══

    # Remove old: .dark-sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 200px; ... }
    content = re.sub(
        r'/\* ── Dark left sidebar ── \*/\s*\.dark-sidebar \{\s*position: fixed; left: 0; top: 0; bottom: 0; width: 200px;[^}]+\}',
        '''/* ── Body flex layout ── */
    .dept-body { display: flex; flex: 1; }
    .dept-body__panels { flex: 1; min-width: 0; }

    /* ── Left sidebar ── */
    .dark-sidebar {
      width: 220px; flex-shrink: 0; position: sticky; top: 0; height: 100vh;
      background: #FAFAF8; z-index: 35; padding-top: 24px;
      border-right: 1px solid rgba(0,0,0,0.05);
      overflow-y: auto; align-self: flex-start;
    }''',
        content
    )

    # Remove old: body { padding-left: 200px; }
    content = re.sub(r'\s*body \{ padding-left: 200px; \}', '', content)
    # Remove old: .dark-sidebar { position: fixed; left: 0; top: 0; }
    content = re.sub(r'\s*\.dark-sidebar \{ position: fixed; left: 0; top: 0; \}', '', content)
    # Remove old: .dept-panel { max-width: none; }
    content = re.sub(r'\s*\.dept-panel \{ max-width: none; \}', '', content)

    # Update responsive rules
    content = content.replace(
        '      .dark-sidebar { display: none; }\n      body { padding-left: 0; }',
        '      .dark-sidebar { display: none; }\n      .dept-body { display: block; }'
    )
    # Also handle variant without newline
    content = content.replace(
        '      .dark-sidebar { display: none; }\n      body { padding-left: 0; }\n      .dept-panel { max-width: 1100px; }',
        '      .dark-sidebar { display: none; }\n      .dept-body { display: block; }'
    )

    # Update sidebar background to match CSE's white design
    content = content.replace(
        'background: #0B0F1A; z-index: 35; padding-top: 120px;',
        'background: #FAFAF8; z-index: 35; padding-top: 24px;'
    )
    content = content.replace(
        'border-right: 1px solid rgba(255,255,255,0.06);',
        'border-right: 1px solid rgba(0,0,0,0.05);'
    )
    content = content.replace(
        'border-right: 1px solid rgba(255,255,255,0.05);',
        'border-right: 1px solid rgba(0,0,0,0.05);'
    )

    # Update sidebar label colors from white-on-dark to dark-on-light
    content = content.replace("color: rgba(255,255,255,0.2);", "color: #1A3A2E;")
    content = content.replace("color: rgba(255,255,255,0.35);", "color: rgba(26,58,46,0.5);")
    content = content.replace("color: rgba(255,255,255,0.65);", "color: rgba(232,93,31,0.8);")
    content = content.replace("color: rgba(255,255,255,0.9);", "color: #E85D1F;")
    content = content.replace("background: rgba(255,255,255,0.15);", "background: rgba(0,0,0,0.1);")
    content = content.replace("border-bottom: 1px solid rgba(255,255,255,0.06);", "border-bottom: 1px solid rgba(0,0,0,0.06);")
    content = content.replace(
        ".dark-sidebar::-webkit-scrollbar-thumb { background: rgba(232,93,31,0.2); border-radius: 2px; }",
        ".dark-sidebar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 2px; }"
    )

    # ═══ 2. RESTRUCTURE HTML ═══

    # Move sidebar from before <header> to after <nav class="dept-tabs">
    # Old: <body>\n  <aside class="dark-sidebar">...</aside>\n\n  <header>
    # New: <body>\n  <header>...<tabs>...<div class="dept-body"><aside>...<div class="dept-body__panels">

    # Extract sidebar HTML
    sidebar_match = re.search(
        r'(  <!-- Dark left sidebar -->\s*\n  <aside class="dark-sidebar".*?</aside>)',
        content, re.DOTALL
    )
    if not sidebar_match:
        sidebar_match = re.search(
            r'(  <aside class="dark-sidebar".*?</aside>)',
            content, re.DOTALL
        )

    if sidebar_match:
        sidebar_html = sidebar_match.group(1)
        # Remove sidebar from its old position
        content = content.replace(sidebar_html + '\n', '')
        content = content.replace(sidebar_html, '')

        # Find where to insert dept-body wrapper (after streak div or after tabs)
        # Pattern: after </nav> (dept-tabs) and before first <div class="dept-panel"
        streak_and_panel = re.search(
            r'(  <div class="streak"[^>]*></div>\s*\n)',
            content
        )
        if streak_and_panel:
            insert_point = streak_and_panel.end()
        else:
            # Find first panel
            first_panel = content.find('  <div class="dept-panel')
            insert_point = first_panel

        # Insert dept-body wrapper with sidebar
        wrapper_open = f'\n  <div class="dept-body">\n{sidebar_html}\n\n  <div class="dept-body__panels">\n'
        content = content[:insert_point] + wrapper_open + content[insert_point:]
    else:
        print(f'  {dept}: WARNING - sidebar HTML not found')

    # Add closing wrappers before </script>
    # Check if they don't already exist
    if '</div><!-- .dept-body__panels -->' not in content:
        content = content.replace(
            '\n  <script>',
            '\n  </div><!-- .dept-body__panels -->\n  </div><!-- .dept-body -->\n\n  <script>'
        )

    # Clean up any double blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # ═══ 3. SAVE AND VERIFY ═══
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
        js = 'NO_SCRIPT'

    # Verify structure
    has_dept_body = 'class="dept-body"' in content
    has_panels_wrap = 'dept-body__panels' in content
    has_sticky = 'position: sticky' in content
    no_padding_left = 'padding-left: 200px' not in content
    no_fixed_sidebar = 'position: fixed; left: 0; top: 0; bottom: 0' not in content

    print(f'{dept}: js={js} flex={has_dept_body} panels={has_panels_wrap} sticky={has_sticky} no_pad={no_padding_left} no_fixed={no_fixed_sidebar}')
