#!/usr/bin/env python3
"""Comprehensive redesign of CSE page — 5 changes."""
import re

with open('c:/mlr/homepage/departments/cse.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ═══════════════════════════════════════
# 1. REMOVE DUPLICATE CONTENT IN ACHIEVEMENTS
# ═══════════════════════════════════════
# The duplicates are sections WITHOUT IDs after the ones WITH IDs
# Remove from "<div class="panel-sub">Roll of Honour</div>" (no id)
# to just before "</div>\n    </div>\n  </div>" that closes panel-achievements

# Find the second "Roll of Honour" (no id) and remove everything from there to the intern-note
dup_start = content.find('    <div class="panel-sub">Roll of Honour</div>')
if dup_start > 0:
    # Find the end — the intern-note closing + its parent divs before </div>\n  </div>
    dup_end_marker = '<p class="intern-note">Internship opportunities are facilitated through the Training and Placement Cell in collaboration with the CSE department.</p>'
    dup_end = content.find(dup_end_marker, dup_start)
    if dup_end > 0:
        dup_end = dup_end + len(dup_end_marker)
        # Also grab trailing </div> tags
        remaining = content[dup_end:]
        # Count closing divs that belong to the duplicate
        extra_close = 0
        for ch in remaining:
            if ch in ' \n\t':
                continue
            break
        # Remove the duplicate block
        content = content[:dup_start] + content[dup_end:]
        print('1. Removed duplicate content in achievements')

# ═══════════════════════════════════════
# 2. REDESIGN — WHITE SIDEBAR + WHITE PAGE
# ═══════════════════════════════════════

# Sidebar CSS changes
content = content.replace(
    'background: #0B0F1A; z-index: 35; padding-top: 120px;',
    'background: #FFFFFF; z-index: 35; padding-top: 120px; border-right: 1px solid rgba(0,0,0,0.08); box-shadow: 2px 0 12px rgba(0,0,0,0.04);'
)
# Remove old border-right if exists
content = content.replace(
    'border-right: 1px solid rgba(255,255,255,0.06);',
    ''
)

# Sidebar title color
content = content.replace(
    "color: rgba(255,255,255,0.2);",
    "color: #1A3A2E;"
)
# Sidebar title border
content = content.replace(
    "border-bottom: 1px solid rgba(255,255,255,0.06);",
    "border-bottom: 1px solid rgba(0,0,0,0.06);"
)

# Sidebar item label colors
content = content.replace(
    "color: rgba(255,255,255,0.35); transition: color 0.2s; white-space: nowrap;",
    "color: rgba(26,58,46,0.5); transition: color 0.2s; white-space: nowrap;"
)
content = content.replace(
    ".ds-item:hover .ds-item__label { color: rgba(255,255,255,0.65); }",
    ".ds-item:hover .ds-item__label { color: rgba(232,93,31,0.8); }"
)
content = content.replace(
    ".ds-item.is-active .ds-item__label { color: rgba(255,255,255,0.9); }",
    ".ds-item.is-active .ds-item__label { color: #E85D1F; font-weight: 700; }"
)

# Sidebar dot default color
content = content.replace(
    "background: rgba(255,255,255,0.15);",
    "background: rgba(0,0,0,0.1);"
)

# Sidebar scrollbar
content = content.replace(
    ".dark-sidebar::-webkit-scrollbar-thumb { background: rgba(232,93,31,0.2); border-radius: 2px; }",
    ".dark-sidebar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 2px; }"
)

# Page background
content = content.replace(
    "body { font-family: 'Inter', sans-serif; background: #F4F1EA; color: #3A3A3A; line-height: 1.7; }",
    "body { font-family: 'Inter', sans-serif; background: #FFFFFF; color: #3A3A3A; line-height: 1.7; }"
)

# Panel max-width fix
content = content.replace(
    ".dept-panel { display: none; padding: 48px; max-width: none; margin: 0 auto; }",
    ".dept-panel { display: none; padding: 0; max-width: none; margin: 0; }"
)
# If max-width: 1100px variant exists
content = content.replace(
    ".dept-panel { display: none; padding: 48px; max-width: 1100px; margin: 0 auto; }",
    ".dept-panel { display: none; padding: 0; max-width: none; margin: 0; }"
)

print('2. Redesigned to white sidebar + white page')

# ═══════════════════════════════════════
# 3. REPLACE FACULTY FLIP WITH HOVER CARDS
# ═══════════════════════════════════════

# Replace the fcard CSS entirely
old_fcard_css = """    /* ══ FEATURE 3: Faculty flip cards ══ */
    .fcard-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
    .fcard { width: 100%; height: 280px; perspective: 800px; cursor: pointer; }
    .fcard__inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s ease; transform-style: preserve-3d; }
    .fcard:hover .fcard__inner { transform: rotateY(180deg); }
    .fcard__front, .fcard__back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 10px; overflow: hidden; }
    .fcard__front { background: linear-gradient(135deg, #2A2F40, #3A4050); }
    .fcard__front img { width: 100%; height: 100%; object-fit: cover; object-position: top; }
    .fcard__ini { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 2rem; color: rgba(255,255,255,0.3); }
    .fcard__overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); }
    .fcard__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.82rem; color: #fff; }
    .fcard__role { font-size: 0.68rem; color: rgba(255,255,255,0.6); }
    .fcard__back { background: #0B0F1A; transform: rotateY(180deg); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; text-align: center; }
    .fcard__back-name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1rem; color: #fff; margin-bottom: 4px; }
    .fcard__back-role { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-bottom: 12px; }
    .fcard__back-spec { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600; color: #E85D1F; margin-bottom: 20px; letter-spacing: 0.04em; }
    .fcard__back-btn { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 8px 20px; border: 1px solid #E85D1F; border-radius: 6px; transition: all 0.2s; }
    .fcard__back-btn:hover { background: #E85D1F; color: #fff; }"""

new_fcard_css = """    /* ══ Faculty hover cards (alumni-style) ══ */
    .fcard-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
    .fcard { width: 100%; aspect-ratio: 3/4; border-radius: 12px; overflow: hidden; position: relative; cursor: pointer; background: linear-gradient(135deg, #2A2F40, #3A4050); }
    .fcard img { width: 100%; height: 100%; object-fit: cover; object-position: top; transition: transform 0.4s ease; }
    .fcard:hover img { transform: scale(1.05); }
    .fcard__ini { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 2rem; color: rgba(255,255,255,0.3); position: absolute; inset: 0; }
    .fcard__overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px 18px; background: linear-gradient(transparent, rgba(0,0,0,0.85)); z-index: 2; transition: opacity 0.3s; }
    .fcard__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.85rem; color: #fff; }
    .fcard__role { font-size: 0.68rem; color: rgba(255,255,255,0.6); }
    /* Orange sweep on hover */
    .fcard::before { content: ''; position: absolute; top: 0; right: 0; width: 100%; height: 100%; background: #E85D1F; clip-path: circle(0% at 100% 0%); transition: clip-path 0.5s cubic-bezier(0.25,0.46,0.45,0.94); z-index: 3; }
    .fcard:hover::before { clip-path: circle(150% at 100% 0%); }
    /* Dark overlay with info */
    .fcard::after { content: ''; position: absolute; inset: 0; background: rgba(11,15,26,0.85); opacity: 0; transition: opacity 0.3s ease 0.15s; z-index: 4; }
    .fcard:hover::after { opacity: 1; }
    .fcard:hover .fcard__overlay { opacity: 0; }
    /* Hover info panel */
    .fcard__hover-info { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; text-align: center; z-index: 5; opacity: 0; transform: translateY(10px); transition: opacity 0.35s ease 0.2s, transform 0.35s ease 0.2s; }
    .fcard:hover .fcard__hover-info { opacity: 1; transform: translateY(0); }
    .fcard__hover-name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.05rem; color: #fff; margin-bottom: 4px; }
    .fcard__hover-role { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-bottom: 12px; }
    .fcard__hover-spec { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600; color: #E85D1F; margin-bottom: 20px; letter-spacing: 0.04em; }
    .fcard__hover-btn { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; color: #fff; text-decoration: none; padding: 8px 20px; border: 1px solid #fff; border-radius: 6px; transition: all 0.2s; }
    .fcard__hover-btn:hover { background: #fff; color: #0B0F1A; }"""

if old_fcard_css in content:
    content = content.replace(old_fcard_css, new_fcard_css)
    print('3. Replaced flip cards with hover cards (CSS)')
else:
    print('3. WARN: Could not find exact old fcard CSS')

# Now update the HTML — replace fcard__inner/front/back structure with the new structure
# Old: <div class="fcard__inner"><div class="fcard__front">...<div class="fcard__back">...</div></div></div>
# New: img + overlay + hover-info (no inner/front/back wrappers)

def transform_fcard(match):
    full = match.group(0)
    # Extract data
    data_author = re.search(r'data-author="([^"]*)"', full)
    img_src = re.search(r'<img src="([^"]*)"', full)
    img_alt = re.search(r'alt="([^"]*)"', full)
    onerror = re.search(r'onerror="([^"]*)"', full)
    ini = re.search(r'<div class="fcard__ini"[^>]*>([^<]*)</div>', full)
    name_el = re.search(r'<div class="fcard__name">([^<]*)</div>', full)
    role_el = re.search(r'<div class="fcard__role">([^<]*)</div>', full)
    back_name = re.search(r'<div class="fcard__back-name">([^<]*)</div>', full)
    back_role = re.search(r'<div class="fcard__back-role">([^<]*)</div>', full)
    back_spec = re.search(r'<div class="fcard__back-spec">([^<]*)</div>', full)
    back_btn = re.search(r'<a href="([^"]*)" class="fcard__back-btn">([^<]*)</a>', full)

    author = data_author.group(1) if data_author else ''
    src = img_src.group(1) if img_src else ''
    alt = img_alt.group(1) if img_alt else ''
    onerr = onerror.group(1) if onerror else ''
    ini_text = ini.group(1) if ini else 'XX'
    name = name_el.group(1) if name_el else (back_name.group(1) if back_name else '')
    role = role_el.group(1) if role_el else (back_role.group(1) if back_role else '')
    spec = back_spec.group(1) if back_spec else ''
    btn_href = back_btn.group(1) if back_btn else '#'
    btn_text = back_btn.group(2) if back_btn else 'View Research'

    return f'''          <div class="fcard" data-author="{author}">
              <img src="{src}" alt="{alt}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'" />
              <div class="fcard__ini" style="display:none">{ini_text}</div>
              <div class="fcard__overlay">
                <div class="fcard__name">{name}</div>
                <div class="fcard__role">{role}</div>
              </div>
              <div class="fcard__hover-info">
                <div class="fcard__hover-name">{name}</div>
                <div class="fcard__hover-role">{role}</div>
                <div class="fcard__hover-spec">{spec}</div>
                <a href="{btn_href}" class="fcard__hover-btn">{btn_text}</a>
              </div>
          </div>'''

# Transform all fcard elements
content = re.sub(
    r'<div class="fcard" data-author="[^"]*">.*?</div>\s*</div>\s*</div>\s*</div>',
    transform_fcard,
    content,
    flags=re.DOTALL
)
print('3. Transformed fcard HTML to hover cards')

# ═══════════════════════════════════════
# 4. SUBTLE ORANGE INTERACTION EFFECTS
# ═══════════════════════════════════════

# Find position to insert new hover rules — before @media
media_pos = content.find('    @media (max-width: 768px)')
if media_pos > 0:
    hover_css = """
    /* ── Subtle orange interactions ── */
    .card:hover { box-shadow: 0 4px 20px rgba(232,93,31,0.08); }
    .sub-accordion__header:hover { border-left-color: #E85D1F; color: #E85D1F; }
    .sub-accordion.is-open .sub-accordion__header { border-left-color: #E85D1F; color: #E85D1F; }
    .honour-table tr:hover td { background: rgba(232,93,31,0.03); }
    .pub-card:hover { border-left-color: #E85D1F; box-shadow: 0 4px 20px rgba(232,93,31,0.08); }
    .achieve-card:hover { background: rgba(232,93,31,0.02); }

"""
    content = content[:media_pos] + hover_css + content[media_pos:]
    print('4. Added orange interaction effects')

# ═══════════════════════════════════════
# 5. STRUCTURE CONTENT — SECTION PADDING
# ═══════════════════════════════════════

# Add .panel-section CSS for structured content blocks
section_css = """
    /* ── Structured panel sections ── */
    .panel-heading { padding: 40px 48px 0; margin-bottom: 28px; }
    .panel-sub { margin-left: 48px; margin-right: 48px; }
    .dept-panel > *:not(.panel-heading):not(h2) { padding-left: 48px; padding-right: 48px; }
    .dept-panel .panel-layout, .dept-panel .fcard-grid, .dept-panel .two-col, .dept-panel .three-col, .dept-panel .catalog-grid, .dept-panel .achieve-grid, .dept-panel .obe-grid, .dept-panel .lab-grid, .dept-panel .placement-stats, .dept-panel .intern-grid, .dept-panel .honour-table, .dept-panel .achieve-list, .dept-panel .pub-filters, .dept-panel .pub-list { padding-left: 48px; padding-right: 48px; }

"""

# Insert before the orange interactions block
orange_pos = content.find('    /* ── Subtle orange interactions ── */')
if orange_pos > 0:
    content = content[:orange_pos] + section_css + content[orange_pos:]
    print('5. Added structured section padding')

# ═══════════════════════════════════════
# SAVE
# ═══════════════════════════════════════
with open('c:/mlr/homepage/departments/cse.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify JS
import subprocess
m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if m:
    with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
        jf.write(m.group(1))
    r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
    print(f'\nJS: {"OK" if r.returncode == 0 else "ERROR: " + r.stderr[:80]}')

print(f'Total size: {len(content)} bytes')
