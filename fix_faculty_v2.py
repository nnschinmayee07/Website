import re, glob

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in filepath or 'ug.html' in filepath or 'pg.html' in filepath:
        continue

    dept = filepath.rsplit('\\', 1)[-1].rsplit('/', 1)[-1].replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract ALL faculty data from anywhere in the file
    photos = re.findall(r'<img src="(images/[^"]+)"[^>]*alt="([^"]*)"', content)
    names = re.findall(r'<div class="faculty-item__name">(.*?)</div>', content)
    roles = re.findall(r'<div class="faculty-item__role">(.*?)</div>', content)

    # Filter only faculty photos (not logo etc)
    faculty_photos = [(src, alt) for src, alt in photos if 'images/' + dept + '/' in src or 'images/cse/' in src]

    count = min(len(names), len(roles))
    if count == 0:
        print(f'{dept}: NO faculty data found, skipping')
        continue

    print(f'{dept}: found {count} faculty (photos={len(faculty_photos)} names={len(names)} roles={len(roles)})')

    def get_initials(name):
        parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Miss','').replace('Prof.','').replace('&amp;','').strip().split()
        if len(parts) >= 2:
            return parts[0][0].upper() + parts[-1][0].upper()
        return parts[0][:2].upper() if parts else 'XX'

    # Build clean faculty items
    items_html = []
    for i in range(count):
        name = names[i]
        role = roles[i]
        photo_src = faculty_photos[i][0] if i < len(faculty_photos) else ''
        initials = get_initials(name)

        if photo_src:
            img = f'<img src="{photo_src}" alt="{name}" onerror="this.style.display=\'none\';this.parentElement.textContent=\'{initials}\'" />'
        else:
            img = initials

        items_html.append(f'''            <div class="faculty-item">
              <div class="faculty-item__photo">{img}</div>
              <div class="faculty-item__name">{name}</div>
              <div class="faculty-item__role">{role}</div>
            </div>''')

    new_lane = '<div class="faculty-lane">\n' + '\n'.join(items_html) + '\n          </div>'

    # Replace the entire panel-faculty content
    panel_match = re.search(
        r'(<div class="dept-panel"[^>]*id="panel-faculty">)\s*(.*?)\s*(</div>\s*<!--)',
        content, re.DOTALL
    )

    if panel_match:
        new_panel = panel_match.group(1) + f'''
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Scroll to explore. Click on a profile to view full research details and publications.</p>
    {new_lane}
  ''' + panel_match.group(3)
        content = content[:panel_match.start()] + new_panel + content[panel_match.end():]
        print(f'  panel replaced')
    else:
        print(f'  WARNING: panel-faculty not found for replacement')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('\nDone.')
