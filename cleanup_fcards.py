#!/usr/bin/env python3
"""Clean up orphaned fcard__back blocks and stray closing divs after upgrade."""
import re, os, subprocess

targets = ['ece.html', 'eee.html', 'mechanical.html', 'aeronautical.html', 'mba.html', 'freshman.html']
base = 'c:/mlr/homepage/departments'

for filename in targets:
    filepath = os.path.join(base, filename)
    dept = filename.replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count before
    back_before = content.count('fcard__back')

    # Remove orphaned fcard__back blocks (they sit between hover cards now)
    # Pattern: optional whitespace + <div class="fcard__back"> ... </div> + optional stray </div>
    content = re.sub(
        r'\s*<div class="fcard__back">.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # Also remove any remaining fcard__inner or fcard__front wrappers
    content = re.sub(r'\s*<div class="fcard__inner">\s*', '', content)
    content = re.sub(r'\s*<div class="fcard__front">\s*', '', content)

    # Update the faculty panel description text
    content = content.replace(
        'Hover to flip. Click "View Publications" for the full research profile.',
        'Hover for details. Click "View Research" for full profile.'
    )

    # Also update spec from generic "Engineering" to use the back-spec data
    # (This was lost because the regex extracted from back-spec but the back blocks
    #  were orphaned — the specs are already in the hover cards from the transform)

    # Clean up any double blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    back_after = content.count('fcard__back')
    print(f'{dept}: fcard__back {back_before} -> {back_after}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify JS
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if m:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(m.group(1))
        r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        print(f'  JS: {"OK" if r.returncode == 0 else "ERR: " + r.stderr[:100]}')

    # Verify hover cards
    hover = content.count('fcard__hover-info')
    print(f'  hover_cards: {hover}')

print('\nDone.')
