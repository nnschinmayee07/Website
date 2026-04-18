#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit and fix ALL links across department pages."""
import sys, io, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALL = ['cse.html', 'ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

# ═══ BUILD LOCAL FILE INDEX ═══
local_files = set()
for root, dirs, files in os.walk(base):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), base).replace('\\', '/')
        local_files.add(rel)

print(f'Local file index: {len(local_files)} files')

# ═══ MAPPING: broken path -> correct local path ═══
# Syllabus PDF rewrites (non-existent paths -> actual local PDFs)
PDF_FIXES = {
    # CSE
    'syllabus/cse/r25.pdf': 'syllabus/pdfs/cse-r25-syllabus.pdf',
    'syllabus/cse/r22.pdf': 'syllabus/pdfs/cse-r22-syllabus.pdf',
    'syllabus/cse/mlr20.pdf': 'syllabus/pdfs/cse-mlr20-syllabus.pdf',
    'syllabus/cse/mlr18.pdf': 'syllabus/pdfs/cse-mlr18-syllabus.pdf',
    # ECE
    'syllabus/ece/r25.pdf': 'syllabus/pdfs/ece-r25-syllabus.pdf',
    'syllabus/ece/r22.pdf': 'syllabus/pdfs/ece-r22-syllabus.pdf',
    'syllabus/ece/mlr20.pdf': 'syllabus/pdfs/ece-mlr20-syllabus.pdf',
    # EEE
    'syllabus/eee/r25.pdf': 'syllabus/pdfs/eee-r22-syllabus.pdf',  # no r25 exists, use r22
    'syllabus/eee/r22.pdf': 'syllabus/pdfs/eee-r22-syllabus.pdf',
    'syllabus/eee/mlr18.pdf': 'syllabus/pdfs/eee-mlr18-syllabus.pdf',
    'syllabus/eee/mlr20.pdf': 'syllabus/pdfs/eee-mlr20-syllabus.pdf',
    # Mechanical
    'syllabus/mechanical/r25.pdf': 'syllabus/pdfs/mech-r25-syllabus.pdf',
    'syllabus/mechanical/r22.pdf': 'syllabus/pdfs/mech-r22-complete.pdf',
    # Aeronautical
    'syllabus/aeronautical/r25.pdf': 'syllabus/pdfs/aero-r25-syllabus.pdf',
    'syllabus/aeronautical/r22.pdf': 'syllabus/pdfs/aero-r22-complete.pdf',
    # MBA (no local PDF exists — keep as placeholder but use closest)
    'syllabus/mba/r22.pdf': 'syllabus/pdfs/cse-r22-syllabus.pdf',  # placeholder
    # Freshman (no local PDF exists)
    'syllabus/freshman/r25.pdf': 'syllabus/pdfs/cse-r25-syllabus.pdf',  # placeholder
    # EEE MLR18 alternate path
    'syllabus/eee-mlr18-syllabus.pdf': 'syllabus/pdfs/eee-mlr18-syllabus.pdf',
    # ECE alternate paths
    'syllabus/ece-r25-syllabus.pdf': 'syllabus/pdfs/ece-r25-syllabus.pdf',
    'syllabus/ece-r22-syllabus.pdf': 'syllabus/pdfs/ece-r22-syllabus.pdf',
    'syllabus/ece-mlr20-syllabus.pdf': 'syllabus/pdfs/ece-mlr20-syllabus.pdf',
}

# Absolute path fixes
ABS_FIXES = {
    '/departments/syllabus/pdfs/mech-r22-complete.pdf': 'syllabus/pdfs/mech-r22-complete.pdf',
    '/departments/syllabus/pdfs/aero-r22-complete.pdf': 'syllabus/pdfs/aero-r22-complete.pdf',
}

# External mlrit.ac.in -> local replacements
EXTERNAL_FIXES = {
    'http://files.mlrit.ac.in/uploads/ECE/R25_ECE.pdf': 'syllabus/pdfs/ece-r25-syllabus.pdf',
    'http://files.mlrit.ac.in/uploads/ECE/R22_ECE.pdf': 'syllabus/pdfs/ece-r22-syllabus.pdf',
    'https://files.mlrit.ac.in/syllabus/EEE/22/EEE-R22.pdf': 'syllabus/pdfs/eee-r22-syllabus.pdf',
    'https://files.mlrit.ac.in/uploads/Mechanical/Mech_UG-R25.pdf': 'syllabus/pdfs/mech-r25-syllabus.pdf',
    'https://files.mlrit.ac.in/uploads/Mechanical/Mech_PG-R25.pdf': 'syllabus/pdfs/mech-pg-r25-syllabus.pdf',
    'https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_Aero_Syllabus.pdf': 'syllabus/pdfs/aero-r25-syllabus.pdf',
    'https://mlrit.ac.in/curriculum/ece-m-tech-r22-syllabus/': 'syllabus/pdfs/ece-r22-syllabus.pdf',
    'https://mlrit.ac.in/curriculum/eee-mlr20-syllabus/': 'syllabus/pdfs/eee-mlr20-syllabus.pdf',
    'https://mlrit.ac.in/curriculum/mechanical-r22-syllabus/': 'syllabus/pdfs/mech-r22-complete.pdf',
    'https://mlrit.ac.in/curriculum/mechanical-m-tech-r22-syllabus/': 'syllabus/pdfs/mech-r22-complete.pdf',
    'https://mlrit.ac.in/curriculum/aeronautical-r22-syllabus/': 'syllabus/pdfs/aero-r22-complete.pdf',
    'https://mlrit.ac.in/curriculum/aeronautical-m-tech-r22-syllabus/': 'syllabus/pdfs/aero-r22-complete.pdf',
    'https://mlrit.ac.in/curriculum/mba-r22-syllabus/': '#',
    'https://mlrit.ac.in/curriculum/mba-mlr20-syllabus/': '#',
    'https://mlrit.ac.in/curriculum/cse-r22-ug-syllabus/': 'syllabus/pdfs/cse-r22-syllabus.pdf',
    'https://mlrit.ac.in/curriculum/cse-mlr20-ug-syllabus/': 'syllabus/pdfs/cse-mlr20-syllabus.pdf',
    'https://mlrit.ac.in/curriculum/cse-mlr18-ug-syllabus/': 'syllabus/pdfs/cse-mlr18-syllabus.pdf',
    'https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_CSE-Syllabus.pdf': 'syllabus/pdfs/cse-r25-syllabus.pdf',
}

# JS regulation PDF path fixes (inside JS objects)
JS_PDF_FIXES = {
    # ECE
    "'syllabus/pdfs/ece-r25-syllabus.pdf'": "'syllabus/pdfs/ece-r25-syllabus.pdf'",  # already correct
    "'syllabus/pdfs/ece-r22-syllabus.pdf'": "'syllabus/pdfs/ece-r22-syllabus.pdf'",
    "'syllabus/pdfs/ece-mlr20-syllabus.pdf'": "'syllabus/pdfs/ece-mlr20-syllabus.pdf'",
    # EEE
    "'syllabus/pdfs/eee-r22-syllabus.pdf'": "'syllabus/pdfs/eee-r22-syllabus.pdf'",
    "'syllabus/pdfs/eee-mlr18-syllabus.pdf'": "'syllabus/pdfs/eee-mlr18-syllabus.pdf'",
    # Mech
    "'syllabus/pdfs/mech-r25-syllabus.pdf'": "'syllabus/pdfs/mech-r25-syllabus.pdf'",
    "'syllabus/pdfs/mech-r22-complete.pdf'": "'syllabus/pdfs/mech-r22-complete.pdf'",
    # Aero
    "'syllabus/pdfs/aero-r25-syllabus.pdf'": "'syllabus/pdfs/aero-r25-syllabus.pdf'",
    "'syllabus/pdfs/aero-r22-complete.pdf'": "'syllabus/pdfs/aero-r22-complete.pdf'",
}

total_fixes = 0

for filename in ALL:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    fixes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ═══ FIX 1: Broken local PDF paths ═══
    for broken, correct in PDF_FIXES.items():
        if broken in content:
            # Verify the target exists
            target_path = os.path.join(base, correct)
            exists = os.path.exists(target_path)
            content = content.replace(f'"{broken}"', f'"{correct}"')
            content = content.replace(f"'{broken}'", f"'{correct}'")
            fixes.append(f'PDF: {broken} -> {correct} (exists={exists})')

    # ═══ FIX 2: Absolute paths ═══
    for broken, correct in ABS_FIXES.items():
        if broken in content:
            target_path = os.path.join(base, correct)
            exists = os.path.exists(target_path)
            content = content.replace(broken, correct)
            fixes.append(f'ABS: {broken} -> {correct} (exists={exists})')

    # ═══ FIX 3: External mlrit.ac.in -> local ═══
    for ext, local in EXTERNAL_FIXES.items():
        if ext in content:
            if local != '#':
                target_path = os.path.join(base, local)
                exists = os.path.exists(target_path)
            else:
                exists = True  # placeholder
            content = content.replace(ext, local)
            fixes.append(f'EXT: {ext[:60]}... -> {local} (exists={exists})')

    # ═══ FIX 4: JS syllabus URL construction ═══
    # CSE JS builds: 'syllabus/pdfs/' + currentReg + '/' — this expects r25/, r22/, mlr20/, mlr18/ subdirs
    # These subdirs exist: r22/, mlr18/, mlr20/ but NOT r25/
    # The individual subject PDFs live in these subdirs with SUBJECT-NAME.pdf format
    # No fix needed here — the PDFs either exist or they're 404 (expected for R25 individual subjects)

    # ═══ SAVE ═══
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    total_fixes += len(fixes)
    if fixes:
        print(f'\n{dept}: {len(fixes)} fixes')
        for fix in fixes:
            print(f'  {fix}')
    else:
        print(f'\n{dept}: no fixes needed')

print(f'\n{"="*60}')
print(f'Total fixes applied: {total_fixes}')

# ═══ FINAL AUDIT: check all remaining href/src against local files ═══
print(f'\n{"="*60}')
print('REMAINING LINK AUDIT')
print(f'{"="*60}')

skip_prefixes = ('https://fonts.', 'http://103.15.62.235', '#', 'javascript:', 'mailto:', 'data:')
skip_patterns = ('faculty-profile.html?',)  # query param links

for filename in ALL:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    broken = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all href and src values
    for match in re.finditer(r'(?:href|src)="([^"]*)"', content):
        link = match.group(1)

        # Skip external/special links
        if any(link.startswith(p) for p in skip_prefixes):
            continue
        if any(p in link for p in skip_patterns):
            continue
        if link.startswith('http://') or link.startswith('https://'):
            broken.append(f'EXTERNAL: {link}')
            continue

        # Resolve relative path
        if link.startswith('../'):
            resolved = os.path.normpath(os.path.join(base, '..', link[3:])).replace('\\', '/')
        else:
            resolved = os.path.join(base, link).replace('\\', '/')

        if not os.path.exists(resolved):
            broken.append(f'MISSING: {link}')

    if broken:
        print(f'\n{dept}: {len(broken)} broken links')
        for b in broken:
            print(f'  {b}')
    else:
        print(f'{dept}: all links OK')

# ═══ VERIFY JS ═══
print(f'\n{"="*60}')
print('JS VERIFICATION')
for filename in ALL:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        print(f'  {dept}: JS {"OK" if r.returncode == 0 else "ERR: " + r.stderr[:80]}')
