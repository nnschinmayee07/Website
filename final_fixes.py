#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""Final consistency fixes across all department pages."""
import re, os, subprocess

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
pdf_fix_targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html']
base = 'c:/mlr/homepage/departments'

results = {}

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ 1. HERO ANCHOR FIX ═══
    if 'id="page-top"' not in content:
        old = '<div class="dept-hero">'
        if old in content:
            content = content.replace(old, '<div class="dept-hero" id="page-top">', 1)
            changes.append('1. Added id="page-top" to .dept-hero')
        else:
            changes.append('1. SKIP - .dept-hero not found or already has id')
    else:
        changes.append('1. SKIP - id="page-top" already present')

    # ═══ 2. TAB UX FIX — window.scrollTo ═══
    if "updateSidebar('overview');" in content and 'window.scrollTo(0, 0)' not in content:
        content = content.replace(
            "updateSidebar('overview');",
            "updateSidebar('overview');\n      window.scrollTo(0, 0);",
            1  # only first occurrence
        )
        changes.append('2. Added window.scrollTo(0, 0) after updateSidebar init')
    elif 'window.scrollTo(0, 0)' in content:
        changes.append('2. SKIP - window.scrollTo already present')
    else:
        changes.append('2. SKIP - updateSidebar init not found')

    # ═══ 3. PDF UI FIX (ECE, EEE, MECH, AERO only) ═══
    if filename in pdf_fix_targets:
        # Add white-space: nowrap to .subject-pdf
        old_pdf = '.subject-pdf { font-family: \'Raleway\', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 4px 12px; border: 1px solid rgba(232,93,31,0.3); border-radius: 6px; transition: all 0.2s; }'
        new_pdf = '.subject-pdf { font-family: \'Raleway\', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 4px 12px; border: 1px solid rgba(232,93,31,0.3); border-radius: 6px; transition: all 0.2s; white-space: nowrap; }'
        if old_pdf in content:
            content = content.replace(old_pdf, new_pdf)
            changes.append('3a. Added white-space: nowrap to .subject-pdf')
        elif 'white-space: nowrap' in content and '.subject-pdf' in content:
            changes.append('3a. SKIP - white-space: nowrap already present')
        else:
            changes.append('3a. SKIP - .subject-pdf rule not found in expected format')

        # Add .subject-pdf--disabled class after .subject-pdf:hover
        if '.subject-pdf--disabled' not in content:
            old_hover = ".subject-pdf:hover { background: #E85D1F; color: #fff; }"
            new_hover = ".subject-pdf:hover { background: #E85D1F; color: #fff; }\n    .subject-pdf--disabled { color: #aaa; border-color: #ddd; pointer-events: none; background: #f5f5f5; }"
            if old_hover in content:
                content = content.replace(old_hover, new_hover)
                changes.append('3b. Added .subject-pdf--disabled class')
            else:
                changes.append('3b. SKIP - .subject-pdf:hover not found')
        else:
            changes.append('3b. SKIP - .subject-pdf--disabled already present')
    else:
        changes.append('3. N/A - not a PDF fix target')

    # ═══ 4. FACULTY CARD CONSISTENCY ═══
    if '.fcard { height: auto; }' in content:
        content = content.replace('.fcard { height: auto; }', '.fcard { height: 240px; }')
        changes.append('4. Fixed .fcard { height: auto } → { height: 240px }')
    elif '.fcard { height: 240px; }' in content:
        changes.append('4. SKIP - .fcard height already 240px')
    else:
        changes.append('4. SKIP - .fcard height rule not found in media query')

    # ═══ 5. PANEL WIDTH FIX ═══
    # Remove .dept-panel { max-width: 1100px; } from media query
    if '.dept-panel { max-width: 1100px; }' in content:
        content = content.replace('\n      .dept-panel { max-width: 1100px; }', '')
        # Also try without leading newline
        content = content.replace('      .dept-panel { max-width: 1100px; }\n', '')
        changes.append('5. Removed .dept-panel { max-width: 1100px } from media query')
    else:
        changes.append('5. SKIP - max-width: 1100px not present')

    # ═══ 6. FRESHMAN JS CLEANUP ═══
    if filename == 'freshman.html':
        # Remove the qbar switcher IIFE (minified single line)
        qbar_pattern = re.search(
            r'\n    \(function\(\)\{var tabs=document\.querySelectorAll\(\'\.dept-tab\'\);var panels=document\.querySelectorAll\(\'\.dept-panel\'\);var qbtns=document\.querySelectorAll\(\'\.qbar__btn\'\).*?\}\)\(\);\n',
            content
        )
        if qbar_pattern:
            content = content[:qbar_pattern.start()] + '\n' + content[qbar_pattern.end():]
            changes.append('6. Removed qbar switcher IIFE')
        else:
            changes.append('6. SKIP - qbar switcher not found')
    else:
        changes.append('6. N/A - not freshman')

    # ═══ 7. FRESHMAN PUB FILTER ═══
    if filename == 'freshman.html':
        has_pub_cards = 'class="pub-card"' in content or "class='pub-card'" in content
        has_pub_filter = 'pubFilters' in content or 'pub-filter' in content
        if has_pub_cards and not has_pub_filter:
            # Add publication filter IIFE (minified, same as other depts)
            pub_filter_js = """    // Publication filter
    (function(){var f=document.getElementById('pubFilters');var c=document.querySelectorAll('.pub-card');if(!f||!c.length)return;f.addEventListener('click',function(e){var b=e.target.closest('.pub-filter');if(!b)return;var y=b.getAttribute('data-year');f.querySelectorAll('.pub-filter').forEach(function(x){x.classList.remove('is-active')});b.classList.add('is-active');c.forEach(function(card){var m=(y==='all'||card.getAttribute('data-pub-year')===y);if(m){card.classList.remove('is-hidden');card.style.display='flex'}else{card.classList.add('is-hidden');setTimeout(function(){if(card.classList.contains('is-hidden'))card.style.display='none'},350)}});});})();"""
            # Insert before achievement toggle
            achieve_marker = '// Achievement toggle' if '// Achievement toggle' in content else "(function(){document.querySelectorAll('[data-achieve]')"
            if achieve_marker in content:
                # Find the achieve line
                idx = content.index(achieve_marker)
                # Find start of that line
                line_start = content.rfind('\n', 0, idx)
                content = content[:line_start] + '\n' + pub_filter_js + '\n' + content[line_start:]
                changes.append('7. Added publication filter IIFE')
            else:
                changes.append('7. SKIP - could not find insertion point')
        elif not has_pub_cards:
            changes.append('7. SKIP - no .pub-card elements found')
        else:
            changes.append('7. SKIP - publication filter already present')
    else:
        changes.append('7. N/A - not freshman')

    # ═══ SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # ═══ VERIFY JS ═══
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js_ok = r.returncode == 0
        if not js_ok:
            changes.append(f'JS ERROR: {r.stderr[:120]}')
        else:
            changes.append('JS: OK')
    else:
        changes.append('JS: NO SCRIPT FOUND')

    results[dept] = changes

# ═══ PRINT REPORT ═══
for dept, changes in results.items():
    print(f'\n{"="*50}')
    print(f' {dept.upper()}')
    print(f'{"="*50}')
    for c in changes:
        print(f'  {c}')

print(f'\n{"="*50}')
print(' VERIFICATION')
print(f'{"="*50}')

# Cross-check all files
for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'page-top': 'id="page-top"' in content,
        'scrollTo': 'window.scrollTo(0, 0)' in content,
        'fcard-240': '.fcard { height: 240px; }' in content,
        'no-1100': '.dept-panel { max-width: 1100px; }' not in content,
        'no-qbar': 'qbar__btn' not in content or dept != 'freshman',
    }
    if filename in pdf_fix_targets:
        checks['nowrap'] = 'white-space: nowrap' in content
        checks['disabled'] = 'subject-pdf--disabled' in content

    status = ' '.join(f'{k}={"OK" if v else "FAIL"}' for k, v in checks.items())
    print(f'  {dept}: {status}')
