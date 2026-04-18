#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix faculty profile links: add photo and role params to all hover-btn hrefs."""
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

    # Find all hover-btn links that are missing photo or role params
    # Pattern: href="faculty-profile.html?name=XXX" (no &role= or &photo=)
    for m in re.finditer(r'<a href="(faculty-profile\.html\?name=[^"]*)" class="fcard__hover-btn"', content):
        old_href = m.group(1)
        if '&photo=' in old_href and '&role=' in old_href:
            continue  # Already complete

        # Search backwards from this position to find the card's img, name, role
        pos = m.start()
        # Look back up to 800 chars for the enclosing fcard
        region = content[max(0, pos-800):pos+len(m.group(0))]

        img_m = re.search(r'<img src="([^"]*)"', region)
        name_m = re.search(r'fcard__hover-name">([^<]*)<', region)
        role_m = re.search(r'fcard__hover-role">([^<]*)<', region)

        photo = img_m.group(1) if img_m else ''
        name = name_m.group(1) if name_m else ''
        role = role_m.group(1) if role_m else ''

        if name and photo:
            new_href = 'faculty-profile.html?name=' + quote(name) + '&role=' + quote(role) + '&photo=' + quote(photo)
            content = content.replace('"' + old_href + '"', '"' + new_href + '"', 1)
            fixed += 1

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

    print(f'{dept}: {fixed} links fixed, JS={js}')

print('\nDone.')
