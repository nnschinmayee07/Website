#!/usr/bin/env python3
"""Fix all CSE panels — rebuild faculty, verify all content."""
import re

# Faculty specializations
SPECS = {
    'Dr. Ajmeera Kiran': 'Deep Learning, ML, IoT',
    'Dr. K. Srinivas Rao': 'RFID, Database, Data Mining',
    'Dr. N. Sirisha': 'Big Data, Network Security',
    'Dr. A. Balaram': 'VANETs, WSN, Cryptography',
    'Dr. V. Thrimurthulu': 'Image Processing, NLP, IoT',
    'Dr. K. Venkata Subbaiah': 'Wireless Mesh, AI, Security',
    'Dr. Kandrakunta Chinnaiah': 'Bioinformatics, WSN',
    'Dr. J. Mahalakshmi': 'Cloud, IoT',
    'Dr. G. John Samuel Babu': 'Cloud Computing, IoT',
    'Dr. K. Gagan Kumar': 'Image Processing, ML',
    'Dr. B. Sanjai Prasada Rao': 'Image Processing, ML, DL',
    'Dr. P. Michael Preetam Raj': 'Memristor, Neuromorphic',
    'Dr. M. Kalpana Chowdary': 'Image Processing, DL',
    'Dr. K. Pushpa Rani': 'Deep Learning, NLP',
    'Allam Sangeetha': 'ML, Deep Learning, OS',
}

def get_initials(name):
    p = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Prof.','').strip().split()
    return (p[0][0] + p[-1][0]).upper() if len(p) >= 2 else p[0][:2].upper()

# Load faculty data
faculty = []
for line in open('c:/mlr/cse_faculty_data.txt', encoding='utf-8'):
    parts = line.strip().split('|')
    if len(parts) == 3:
        faculty.append(parts)

print(f'Loaded {len(faculty)} faculty')

# Build faculty cards HTML
cards = []
for photo, name, role in faculty:
    ini = get_initials(name)
    spec = SPECS.get(name, 'Computer Science')
    author = name.replace('Dr. ', '').replace('Mr. ', '').replace('Mrs. ', '').replace('Ms. ', '').replace('Prof. ', '').strip()
    btn_href = f'faculty-profile.html?name={name.replace(" ","%20")}&role={role.replace(" ","%20").replace(",","%2C")}&photo={photo}'

    cards.append(f'''          <div class="fcard" data-author="{author}">
              <img src="{photo}" alt="{name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'" />
              <div class="fcard__ini" style="display:none">{ini}</div>
              <div class="fcard__overlay">
                <div class="fcard__name">{name}</div>
                <div class="fcard__role">{role}</div>
              </div>
              <div class="fcard__hover-info">
                <div class="fcard__hover-name">{name}</div>
                <div class="fcard__hover-role">{role}</div>
                <div class="fcard__hover-spec">{spec}</div>
                <a href="{btn_href}" class="fcard__hover-btn">View Research</a>
              </div>
          </div>''')

faculty_html = '\n'.join(cards)

# Read the file
with open('c:/mlr/homepage/departments/cse.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the faculty panel content
old_faculty = re.search(
    r'(<div class="dept-panel" id="panel-faculty">)\s*\n\s*(<h2 class="panel-heading">Faculty Profiles</h2>).*?(<div id="faculty-grid-section" class="fcard-grid">).*?(</div>\s*</div>\s*</div>)',
    content, re.DOTALL
)

if old_faculty:
    new_faculty = f'''  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Hover for details. Click "View Research" for full profile.</p>
    <div id="faculty-grid-section" class="fcard-grid">
{faculty_html}
    </div>
  </div>'''
    content = content[:old_faculty.start()] + new_faculty + content[old_faculty.end():]
    print(f'Faculty panel rebuilt with {len(faculty)} cards')
else:
    print('WARNING: Could not find faculty panel pattern')
    # Try simpler approach
    m = re.search(r'id="panel-faculty">.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    if m:
        new_fac = f'''id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Hover for details. Click "View Research" for full profile.</p>
    <div id="faculty-grid-section" class="fcard-grid">
{faculty_html}
    </div>
  </div>'''
        content = content[:m.start()] + new_fac + content[m.end():]
        print(f'Faculty rebuilt (alt method) with {len(faculty)} cards')

# Verify all panels exist and have content
for pid in ['panel-overview', 'panel-objectives', 'panel-faculty', 'panel-academics', 'panel-achievements']:
    if f'id="{pid}"' in content:
        # Get content length
        idx = content.index(f'id="{pid}"')
        snippet = content[idx:idx+200]
        print(f'  {pid}: found, starts with: {snippet[:80]}...')
    else:
        print(f'  {pid}: MISSING!')

# Save
with open('c:/mlr/homepage/departments/cse.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify JS
import subprocess
m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if m:
    with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
        jf.write(m.group(1))
    r = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
    print(f'\nJS: {"OK" if r.returncode == 0 else "ERROR"}')

# Count faculty cards in final file
final = open('c:/mlr/homepage/departments/cse.html', encoding='utf-8').read()
fcard_count = final.count('class="fcard"')
print(f'Faculty cards in file: {fcard_count}')
