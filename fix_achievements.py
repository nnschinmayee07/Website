#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix achievements sidebar order + honour table + achieve list across all dept pages."""
import sys, io, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

# ─── OLD honour table CSS ───
OLD_HONOUR = '.honour-table { width: 100%; max-width: 700px; border-collapse: collapse; }\n    .honour-table th { font-family: \'Raleway\', sans-serif; font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; text-align: left; padding: 12px 16px; border-bottom: 2px solid rgba(0,0,0,0.08); }\n    .honour-table td { font-size: 0.88rem; color: #333; padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); }'

NEW_HONOUR = """.honour-table { width: 100%; max-width: 700px; border-collapse: separate; border-spacing: 0 6px; }
    .honour-table th { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; text-align: left; padding: 12px 16px; border-bottom: 2px solid rgba(0,0,0,0.08); }
    .honour-table td { font-size: 0.88rem; color: #333; padding: 14px 16px; background: #fff; transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease; }
    .honour-table tr { transition: transform 0.2s ease; }
    .honour-table tbody tr:hover { transform: translateX(6px); }
    .honour-table tbody tr:hover td { background: rgba(232,93,31,0.06); box-shadow: 0 2px 12px rgba(232,93,31,0.1); }
    .honour-table tbody tr:hover td:first-child { border-left: 3px solid #E85D1F; }
    .honour-table td:first-child { border-radius: 8px 0 0 8px; border-left: 3px solid transparent; }
    .honour-table td:last-child { border-radius: 0 8px 8px 0; }
    .honour-table .honour-name { font-family: 'Raleway', sans-serif; font-weight: 700; color: #0B0F1A; }
    .honour-table .honour-badge { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 0.68rem; font-weight: 700; padding: 3px 10px; border-radius: 10px; letter-spacing: 0.04em; }
    .honour-badge--topper { background: rgba(232,93,31,0.12); color: #E85D1F; }
    .honour-badge--rank { background: rgba(24,69,59,0.1); color: #18453B; }
    .honour-table .honour-score { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.05rem; color: #18453B; }"""

# ─── OLD achieve-list CSS ───
OLD_ALIST = """.achieve-list { list-style: none; padding: 0; max-width: 700px; }
    .achieve-list li { position: relative; padding: 10px 0 10px 20px; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 0.88rem; color: #444; }
    .achieve-list li::before { content: ''; position: absolute; left: 0; top: 16px; width: 8px; height: 8px; border-radius: 50%; background: #E85D1F; }"""

NEW_ALIST = """.achieve-list { list-style: none; padding: 0; max-width: 700px; }
    .achieve-list li { position: relative; padding: 14px 16px 14px 28px; margin-bottom: 8px; border-radius: 8px; background: #fff; box-shadow: 0 1px 6px rgba(0,0,0,0.04); font-size: 0.88rem; color: #444; border-left: 3px solid transparent; transition: transform 0.2s ease, border-left-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease; cursor: default; }
    .achieve-list li:hover { transform: translateX(6px); border-left-color: #E85D1F; box-shadow: 0 4px 16px rgba(232,93,31,0.1); background: rgba(232,93,31,0.02); }
    .achieve-list li::before { content: ''; position: absolute; left: 10px; top: 20px; width: 8px; height: 8px; border-radius: 50%; background: #E85D1F; transition: transform 0.2s ease; }
    .achieve-list li:hover::before { transform: scale(1.4); }"""

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ 1. Fix honour table CSS ═══
    if OLD_HONOUR in content:
        content = content.replace(OLD_HONOUR, NEW_HONOUR)
        changes.append('honour-table CSS')

    # ═══ 2. Fix achieve-list CSS ═══
    if OLD_ALIST in content:
        content = content.replace(OLD_ALIST, NEW_ALIST)
        changes.append('achieve-list CSS')

    # ═══ 3. Remove old honour-table hover rule ═══
    content = content.replace(
        '.honour-table tr:hover td { background: rgba(232,93,31,0.03); }',
        '/* honour-table hover handled above */'
    )

    # ═══ 4. Add badges to honour table HTML ═══
    # Wrap names in honour-name span
    content = re.sub(
        r'<td>([A-Z][^<]+)</td><td>(University Topper)</td><td>([0-9.]+%)</td>',
        r'<td><span class="honour-name">\1</span></td><td><span class="honour-badge honour-badge--topper">\2</span></td><td><span class="honour-score">\3</span></td>',
        content
    )
    content = re.sub(
        r'<td>([A-Z][^<]+)</td><td>(University Rank Holder)</td><td>([0-9.]+%)</td>',
        r'<td><span class="honour-name">\1</span></td><td><span class="honour-badge honour-badge--rank">\2</span></td><td><span class="honour-score">\3</span></td>',
        content
    )
    content = re.sub(
        r'<td>([A-Z][^<]+)</td><td>(Department Topper)</td><td>([0-9.]+%)</td>',
        r'<td><span class="honour-name">\1</span></td><td><span class="honour-badge honour-badge--topper">\2</span></td><td><span class="honour-score">\3</span></td>',
        content
    )
    # Count badge additions
    badges = content.count('honour-badge')
    if badges:
        changes.append(f'honour badges ({badges})')

    # ═══ 5. Fix sidebar order ═══
    # Find achievement sidebar items and reorder
    sidebar_section = re.search(
        r'(    <a class="ds-item" data-ds-tab="achievements".*?)\n    (?=<a class="ds-item" data-ds-tab="(?!achievements)|</aside>)',
        content, re.DOTALL
    )
    if sidebar_section:
        old_sidebar = sidebar_section.group(1)
        # Extract individual items
        items = re.findall(r'<a class="ds-item" data-ds-tab="achievements"[^>]*>.*?</a>', old_sidebar)
        if items:
            # Build target->item map
            item_map = {}
            for item in items:
                target = re.search(r'data-ds-target="([^"]*)"', item)
                label = re.search(r'ds-item__label">([^<]*)<', item)
                if target:
                    item_map[target.group(1)] = item

            # Desired order based on panel content
            desired = ['achieve-section', 'honour-section', 'pub-section', 'intern-section', 'placement-section']
            reordered = []
            for d in desired:
                if d in item_map:
                    reordered.append(item_map[d])
            # Add any not in desired order
            for t, item in item_map.items():
                if t not in desired:
                    reordered.append(item)

            if reordered:
                new_sidebar = '\n'.join('    ' + item for item in reordered)
                content = content.replace(old_sidebar, new_sidebar)
                changes.append('sidebar reordered')

    # ═══ SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # JS check
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else 'ERR'
    else:
        js = '?'

    print(f'{dept}: JS={js} {changes}')

print('\nDone.')
