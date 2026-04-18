#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining faculty profile links missing photo/role params."""
import sys, io, re, os, subprocess
from urllib.parse import quote
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    fixed = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build a map: for each fcard, extract img src, hover-name, hover-role
    # Then match to the hover-btn href within the same card
    cards = list(re.finditer(r'<div class="fcard" data-author="[^"]*">', content))

    for i, card_start in enumerate(cards):
        # Card ends at next card or at end of grid
        start = card_start.start()
        if i + 1 < len(cards):
            end = cards[i + 1].start()
        else:
            end = min(start + 2000, len(content))

        card_html = content[start:end]

        # Extract data
        img_m = re.search(r'<img src="([^"]*)"', card_html)
        name_m = re.search(r'fcard__hover-name">([^<]*)<', card_html)
        role_m = re.search(r'fcard__hover-role">([^<]*)<', card_html)
        href_m = re.search(r'href="(faculty-profile\.html\?[^"]*)"', card_html)

        if not href_m or not name_m:
            continue

        old_href = href_m.group(1)
        if '&photo=' in old_href and '&role=' in old_href:
            continue  # Already complete

        photo = img_m.group(1) if img_m else ''
        name = name_m.group(1)
        role = role_m.group(1) if role_m else ''

        new_href = 'faculty-profile.html?name=' + quote(name) + '&role=' + quote(role) + '&photo=' + quote(photo)

        # Replace in content (use absolute position)
        abs_href_start = start + href_m.start()
        abs_href_end = start + href_m.end()
        old_full = content[abs_href_start:abs_href_end]
        new_full = 'href="' + new_href + '"'
        content = content[:abs_href_start] + new_full + content[abs_href_end:]
        fixed += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify
    links = re.findall(r'href="(faculty-profile\.html\?[^"]+)"', content)
    complete = sum(1 for l in links if 'photo=' in l and 'role=' in l)
    incomplete = sum(1 for l in links if 'photo=' not in l or 'role=' not in l)

    # JS check
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js = 'OK' if r.returncode == 0 else 'ERR'
    else:
        js = '?'

    print(f'{dept}: +{fixed} fixed, complete={complete} incomplete={incomplete} JS={js}')

print('\nDone.')
