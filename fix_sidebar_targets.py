#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all sidebar nav target mismatches across department pages."""
import sys, io, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    fixes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ FIX 1: Move labs-section id from __header to parent sub-accordion ═══
    # Old: <div class="sub-accordion__header"id="labs-section">Academic Laboratories
    # New: id on parent sub-accordion div, not the header
    lab_header = re.search(
        r'<div class="sub-accordion__header"\s*id="labs-section">(Academic Laboratories[^<]*)',
        content
    )
    if lab_header:
        old = lab_header.group(0)
        lab_text = lab_header.group(1)
        # Remove id from header
        new_header = f'<div class="sub-accordion__header">{lab_text}'
        content = content.replace(old, new_header)
        # Add id to parent sub-accordion div (the one right before this header)
        content = content.replace(
            f'<div class="sub-accordion">\n        <div class="sub-accordion__header">{lab_text}',
            f'<div id="labs-section" class="sub-accordion">\n        <div class="sub-accordion__header">{lab_text}'
        )
        fixes.append('labs-section: moved id to parent accordion')

    # ═══ FIX 2: Add id to history sub-accordion if missing ═══
    if 'id="history-section"' not in content:
        history_header = re.search(r'<div class="sub-accordion">\s*\n\s*<div class="sub-accordion__header">History of the Department', content)
        if history_header:
            content = content.replace(
                history_header.group(0),
                history_header.group(0).replace(
                    '<div class="sub-accordion">',
                    '<div id="history-section" class="sub-accordion">'
                )
            )
            fixes.append('history-section: added id')

    # ═══ FIX 3: Add id="catalog-section" to Course Catalog panel-sub ═══
    if 'id="catalog-section"' not in content:
        # Find the panel-sub that says "Course Catalog" without an id
        old_catalog = '<div class="panel-sub">Course Catalog</div>'
        new_catalog = '<div class="panel-sub" id="catalog-section">Course Catalog</div>'
        if old_catalog in content:
            content = content.replace(old_catalog, new_catalog, 1)
            fixes.append('catalog-section: added id')
        else:
            # Maybe it's "Online Course Catalog"
            old_catalog2 = '<div class="panel-sub">Online Course Catalog</div>'
            new_catalog2 = '<div class="panel-sub" id="catalog-section">Online Course Catalog</div>'
            if old_catalog2 in content:
                content = content.replace(old_catalog2, new_catalog2, 1)
                fixes.append('catalog-section: added id (Online variant)')
            else:
                fixes.append('catalog-section: WARNING - no Course Catalog panel-sub found')

    # ═══ FIX 4: Fix duplicate honour-section sidebar items ═══
    # Some pages have "Achievements" and "Honours" both pointing to honour-section
    # Need: "Achievements" -> achieve-section, "Honours" -> honour-section
    # Check if achieve-section id exists
    if 'id="achieve-section"' not in content:
        # Add it to the achieve-grid or first achieve element
        old_achieve = '<div class="achieve-grid">'
        new_achieve = '<div id="achieve-section" class="achieve-grid">'
        if old_achieve in content and 'id="achieve-section"' not in content:
            content = content.replace(old_achieve, new_achieve, 1)
            fixes.append('achieve-section: added id')

    # Fix sidebar: first achievements item should target achieve-section
    # Pattern: two ds-items both targeting honour-section
    sidebar_lines = content.split('\n')
    new_lines = []
    first_honour_fixed = False
    for line in sidebar_lines:
        if ('data-ds-tab="achievements"' in line and
            'data-ds-target="honour-section"' in line and
            'Achievements</span>' in line and
            not first_honour_fixed):
            # This "Achievements" label should point to achieve-section
            line = line.replace('data-ds-target="honour-section"', 'data-ds-target="achieve-section"')
            line = line.replace('>Achievements<', '>Achievements<')
            first_honour_fixed = True
            fixes.append('sidebar: Achievements now targets achieve-section')
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # ═══ FIX 5: Add sidebar "History" item if missing for overview tab ═══
    if 'data-ds-target="history-section"' not in content and 'id="history-section"' in content:
        # Find the labs-section sidebar item and add history before it
        labs_sidebar = re.search(r'(    <a class="ds-item" data-ds-tab="overview" data-ds-target="labs-section">.*?</a>)', content)
        if labs_sidebar:
            history_item = '    <a class="ds-item" data-ds-tab="overview" data-ds-target="history-section"><span class="ds-item__dot"></span><span class="ds-item__label">History</span></a>\n'
            content = content[:labs_sidebar.start()] + history_item + content[labs_sidebar.start():]
            fixes.append('sidebar: added History nav item')

    # ═══ FIX 6: Ensure "Roll of Honour" label (not just "Honours") ═══
    content = content.replace(
        '<span class="ds-item__label">Honours</span>',
        '<span class="ds-item__label">Roll of Honour</span>'
    )

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

    # Verify all targets now exist
    broken = []
    for m in re.finditer(r'data-ds-target="([^"]*)"', content):
        target_id = m.group(1)
        if f'id="{target_id}"' not in content:
            broken.append(target_id)

    print(f'\n{dept}: JS={js}')
    for f_item in fixes:
        print(f'  {f_item}')
    if broken:
        print(f'  STILL BROKEN: {broken}')
    else:
        print(f'  All targets resolved')

print('\nDone.')
