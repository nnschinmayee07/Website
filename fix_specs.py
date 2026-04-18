#!/usr/bin/env python3
"""Recover faculty specializations from git and update hover cards."""
import re, os, subprocess

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')
    rel_path = f'homepage/departments/{filename}'

    # Get original file from git
    r = subprocess.run(['git', 'show', f'HEAD:{rel_path}'], capture_output=True, cwd='c:/mlr')
    if r.returncode != 0:
        print(f'{dept}: ERROR reading git')
        continue
    original = r.stdout.decode('utf-8', errors='replace')

    # Extract author → spec from original
    specs = {}
    for m in re.finditer(
        r'data-author="([^"]*)".*?fcard__back-spec">([^<]*)<',
        original, re.DOTALL
    ):
        specs[m.group(1)] = m.group(2)

    print(f'{dept}: {len(specs)} specs from git')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # For each card, find and replace the generic spec
    fixed = 0
    for author, spec in specs.items():
        # Use regex to find this specific card's hover-spec
        pattern = re.escape(f'data-author="{author}"') + r'.*?fcard__hover-spec">Engineering<'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # Replace just the spec text in this match
            old = f'fcard__hover-spec">Engineering<'
            new = f'fcard__hover-spec">{spec}<'
            # Replace only within this match region
            start = match.start()
            end = match.end()
            region = content[start:end]
            region = region.replace(old, new, 1)
            content = content[:start] + region + content[end:]
            fixed += 1

    print(f'  fixed {fixed}')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    remaining = content.count('hover-spec">Engineering<')
    total = content.count('fcard__hover-spec')
    print(f'  generic: {remaining}/{total}')

print('\nDone.')
