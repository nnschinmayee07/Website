import re, glob

# The popup removal regex left broken HTML.
# We need to rebuild the faculty-lane from the remaining faculty-item data.

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in filepath or 'ug.html' in filepath or 'pg.html' in filepath:
        continue

    dept = filepath.rsplit('\\', 1)[-1].rsplit('/', 1)[-1].replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the faculty lane section
    lane_match = re.search(r'<div class="faculty-lane">(.*?)</div>\s*</div>', content, re.DOTALL)
    if not lane_match:
        print(f'{dept}: no faculty-lane found, skipping')
        continue

    lane_content = lane_match.group(1)

    # Extract each faculty item's data (name, role, photo src)
    items = []
    for m in re.finditer(r'<img src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/>', lane_content):
        photo = m.group(1)
        name = m.group(2)
        items.append((photo, name))

    # Also get roles
    roles = re.findall(r'<div class="faculty-item__role">(.*?)</div>', lane_content)

    # Get names from faculty-item__name divs
    names = re.findall(r'<div class="faculty-item__name">(.*?)</div>', lane_content)

    if len(names) != len(roles):
        print(f'{dept}: mismatch names={len(names)} roles={len(roles)}')
        # Use the shorter count
        count = min(len(names), len(roles), len(items))
    else:
        count = len(names)

    print(f'{dept}: rebuilding {count} faculty items')

    # Build clean faculty lane HTML
    def get_initials(name):
        parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Miss','').replace('Prof.','').replace('&amp;','').strip().split()
        if len(parts) >= 2:
            return parts[0][0].upper() + parts[-1][0].upper()
        return parts[0][:2].upper() if parts else 'XX'

    new_items = []
    for i in range(count):
        photo = items[i][0] if i < len(items) else ''
        name = names[i]
        role = roles[i] if i < len(roles) else ''
        initials = get_initials(name)

        img_tag = f'<img src="{photo}" alt="{name}" onerror="this.style.display=\'none\';this.parentElement.textContent=\'{initials}\'" />' if photo else initials

        new_items.append(f'''            <div class="faculty-item">
              <div class="faculty-item__photo">{img_tag}</div>
              <div class="faculty-item__name">{name}</div>
              <div class="faculty-item__role">{role}</div>
            </div>''')

    new_lane = '<div class="faculty-lane">\n' + '\n'.join(new_items) + '\n          </div>'

    # Replace the old broken lane
    old_lane_full = re.search(r'<div class="faculty-lane">.*?</div>\s*</div>', content, re.DOTALL)
    if old_lane_full:
        content = content[:old_lane_full.start()] + new_lane + content[old_lane_full.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('\nFaculty HTML rebuilt for all departments.')
