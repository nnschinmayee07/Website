#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply hover raise + orange streak effects to all department pages + OBE portal links."""
import sys, io, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'
OBE_URL = 'http://103.15.62.235/ioncudos_mlrit_tier1/'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ 1. LAB CARD HOVER ═══
    old = '.lab-card { background: #f9f8f5; border-radius: 8px; padding: 16px 18px; border-left: 3px solid #18453B; }'
    new = '.lab-card { background: #f9f8f5; border-radius: 8px; padding: 16px 18px; border-left: 3px solid #18453B; transition: transform 0.25s ease, box-shadow 0.25s ease, border-left-color 0.25s ease; cursor: default; }\n    .lab-card:hover { transform: translateY(-4px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); border-left-color: #E85D1F; }'
    if old in content and 'lab-card:hover' not in content:
        content = content.replace(old, new)
        changes.append('lab-card hover')

    # ═══ 2. CARD HOVER ═══
    old = '.card { background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }'
    new = '.card { background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); transition: transform 0.25s ease, box-shadow 0.25s ease; }\n    .card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }'
    if old in content and 'card:hover { transform' not in content:
        content = content.replace(old, new)
        changes.append('card hover')

    # ═══ 3. CARD--ACCENT HOVER ═══
    old = '.card--accent { border-top: 3px solid #18453B; }'
    new = '.card--accent { border-top: 3px solid #18453B; transition: transform 0.25s ease, box-shadow 0.25s ease, border-top-color 0.25s ease; }\n    .card--accent:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); border-top-color: #E85D1F; }'
    if old in content and 'card--accent:hover' not in content:
        content = content.replace(old, new)
        changes.append('card--accent hover')

    # ═══ 4. ACCORDION HEADER HOVER ═══
    old = '.sub-accordion__header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; font-family: \'Raleway\', sans-serif; font-size: 0.88rem; font-weight: 700; color: #0B0F1A; border-left: 3px solid #18453B; transition: background 0.2s; }\n    .sub-accordion__header:hover { background: rgba(24,69,59,0.04); }'
    new = '.sub-accordion__header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; font-family: \'Raleway\', sans-serif; font-size: 0.88rem; font-weight: 700; color: #0B0F1A; border-left: 3px solid #18453B; transition: background 0.2s, border-left-color 0.25s, transform 0.2s; }\n    .sub-accordion__header:hover { background: rgba(24,69,59,0.04); border-left-color: #E85D1F; transform: translateX(4px); }'
    if 'border-left-color: #E85D1F; transform: translateX' not in content:
        if old in content:
            content = content.replace(old, new)
            changes.append('accordion header hover')

    # ═══ 5. OBE LIST ITEM HOVER ═══
    old = '.obe-list li { font-size: 0.88rem; color: #444; padding: 8px 0 8px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); position: relative; }\n    .obe-list li::before { content: \'\'; position: absolute; left: 0; top: 14px; width: 6px; height: 6px; border-radius: 50%; background: #E85D1F; }'
    new = """.obe-list li { font-size: 0.88rem; color: #444; padding: 8px 0 8px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); position: relative; transition: transform 0.2s ease, color 0.2s ease; cursor: default; }
    .obe-list li:hover { transform: translateX(6px); color: #0B0F1A; }
    .obe-list li::before { content: ''; position: absolute; left: 0; top: 14px; width: 6px; height: 6px; border-radius: 50%; background: #E85D1F; transition: transform 0.2s ease, background 0.2s ease; }
    .obe-list li:hover::before { transform: scale(1.5); background: #E85D1F; }
    .obe-list li a { color: inherit; text-decoration: none; display: block; }
    .obe-list li a:hover { color: #E85D1F; }"""
    if 'obe-list li:hover' not in content:
        if old in content:
            content = content.replace(old, new)
            changes.append('obe-list hover')

    # ═══ 6. OBE PORTAL LINKS ═══
    # Wrap plain OBE list items in <a> tags pointing to OBE portal
    obe_items = [
        'Educational Objectives and Outcomes',
        'OBE Process Manual',
        'Course Outcomes Description Booklets',
        'Course Outcomes (COs) Attainment',
        'Program Outcomes (POs) Attainment',
    ]
    obe_fixed = 0
    for item in obe_items:
        plain = f'<li>{item}</li>'
        linked = f'<li><a href="{OBE_URL}" target="_blank">{item}</a></li>'
        if plain in content:
            content = content.replace(plain, linked)
            obe_fixed += 1
    if obe_fixed:
        changes.append(f'obe-portal links ({obe_fixed})')

    # Also fix OBE portal card link if present
    if 'OBE Assessment System' in content or 'OBE Portal' in content:
        if OBE_URL not in content:
            changes.append('obe-portal card link: already absent or different')

    # ═══ SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # ═══ VERIFY JS ═══
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else 'ERR'
    else:
        js = 'NO_SCRIPT'

    print(f'{dept}: JS={js} changes={changes}')

print('\nDone.')
