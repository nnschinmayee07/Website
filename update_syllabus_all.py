#!/usr/bin/env python3
"""Update all department pages to use regulation-based syllabus selector like CSE."""
import re

base = 'c:/mlr/homepage/departments'

# Department syllabus configurations
DEPTS = {
    'ece': {
        'regulations': {
            'r25': {'label': 'R25', 'pdf': 'syllabus/pdfs/ece-r25-syllabus.pdf', 'size': '3.8 MB'},
            'r22': {'label': 'R22', 'pdf': 'syllabus/pdfs/ece-r22-syllabus.pdf', 'size': '2.4 MB'},
            'mlr20': {'label': 'MLR20', 'pdf': 'syllabus/pdfs/ece-mlr20-syllabus.pdf', 'size': '3.6 MB'},
        },
    },
    'eee': {
        'regulations': {
            'r22': {'label': 'R22', 'pdf': 'syllabus/pdfs/eee-r22-syllabus.pdf', 'size': '5.4 MB'},
            'mlr18': {'label': 'MLR18', 'pdf': 'syllabus/pdfs/eee-mlr18-syllabus.pdf', 'size': '2.0 MB'},
        },
    },
    'mechanical': {
        'regulations': {
            'r25': {'label': 'R25', 'pdf': 'syllabus/pdfs/mech-r25-syllabus.pdf', 'size': '6.0 MB'},
            'r22': {'label': 'R22', 'pdf': 'syllabus/pdfs/mech-r22-complete.pdf', 'size': '9.4 MB'},
        },
    },
    'aeronautical': {
        'regulations': {
            'r25': {'label': 'R25', 'pdf': 'syllabus/pdfs/aero-r25-syllabus.pdf', 'size': '1.7 MB'},
            'r22': {'label': 'R22', 'pdf': 'syllabus/pdfs/aero-r22-complete.pdf', 'size': '2.6 MB'},
        },
    },
    'mba': {
        'regulations': {
            'r22': {'label': 'R22', 'pdf': '#', 'size': ''},
        },
    },
}

# New CSS classes needed (add if missing)
new_css = '''    .subject-code { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 700; color: #18453B; background: rgba(24,69,59,0.08); padding: 2px 8px; border-radius: 4px; flex-shrink: 0; letter-spacing: 0.04em; }
    .full-syllabus-btn { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 0.85rem; font-weight: 700; color: #fff; background: #18453B; padding: 10px 24px; border-radius: 8px; text-decoration: none; transition: background 0.2s, transform 0.2s; }
    .full-syllabus-btn:hover { background: #0D3320; transform: translateY(-1px); }'''

for dept, cfg in DEPTS.items():
    filepath = f'{base}/{dept}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add new CSS if missing
    if '.subject-code' not in content and '.subject-pdf' in content:
        content = content.replace(
            '    .subject-pdf {',
            new_css + '\n    .subject-pdf {'
        )

    if '.full-syllabus-btn' not in content:
        content = content.replace(
            '    .subject-pdf:hover {',
            '    .subject-pdf--disabled { color: #aaa; border-color: #ddd; pointer-events: none; background: #f5f5f5; }\n    .full-syllabus-btn { display: inline-block; font-family: \'Raleway\', sans-serif; font-size: 0.85rem; font-weight: 700; color: #fff; background: #18453B; padding: 10px 24px; border-radius: 8px; text-decoration: none; transition: background 0.2s; }\n    .full-syllabus-btn:hover { background: #0D3320; }\n    .subject-pdf:hover {'
        )

    # 2. Build download buttons HTML
    download_btns = ''
    for reg_key, reg in cfg['regulations'].items():
        if reg['pdf'] != '#':
            download_btns += f'      <a href="{reg["pdf"]}" download class="catalog-item"><div><span class="catalog-item__text">{reg["label"]} Complete Syllabus</span><span class="catalog-item__sub">{reg["size"]}</span></div></a>\n'

    # 3. Build regulation pills HTML
    first_reg = list(cfg['regulations'].keys())[0]
    reg_pills = ''
    for i, (reg_key, reg) in enumerate(cfg['regulations'].items()):
        active = ' is-active' if i == 0 else ''
        reg_pills += f'<button class="pill{active}" data-reg="{reg_key}">{reg["label"]}</button>'

    # 4. Build JS regulations object from existing programs data
    # Extract the current programs JS data
    programs_match = re.search(r'(var programs = \{.*?\n\s+\};)', content, re.DOTALL)
    if not programs_match:
        # Try curriculum for MBA
        programs_match = re.search(r'(var curriculum = \{.*?\n\s+\};)', content, re.DOTALL)

    if not programs_match:
        print(f'{dept}: NO programs/curriculum data found, skipping')
        continue

    old_programs = programs_match.group(1)

    # For the regulations JS, we wrap the existing data under the first regulation key
    # and point all other regs to the same data (since we only have one set of subject names)
    regs_js = 'var regulations = {\n'
    for reg_key, reg in cfg['regulations'].items():
        pdf_path = reg['pdf']
        regs_js += f'        "{reg_key}": {{ label: "{reg["label"]}", pdf: "{pdf_path}", data: '
        if 'var programs' in old_programs:
            # Use btech data
            regs_js += 'programs.btech },\n'
        else:
            # MBA - use curriculum directly
            regs_js += 'curriculum },\n'
    regs_js += '      };\n'

    # 5. Replace the HTML syllabus section
    # Find and replace the old pills + subject list HTML
    old_html_patterns = [
        # Pattern with progPills
        r'<div class="pill-row" id="progPills">.*?</div>\s*<div class="pill-row" id="yearPills"></div>\s*<div class="pill-row" id="semPills"[^>]*></div>\s*<div class="subject-list" id="subjectList"></div>',
        # Pattern with just yearPills (MBA)
        r'<div class="pill-row" id="yearPills">.*?</div>\s*<div class="pill-row" id="semPills"[^>]*></div>\s*<div class="subject-list" id="subjectList"></div>',
    ]

    new_html = f'''<div class="panel-sub">Download Syllabus PDF</div>
    <div class="catalog-grid">
{download_btns}    </div>

    <div class="panel-sub">Semester-wise Syllabus Explorer</div>
    <p style="font-style:italic;color:#666;">Select regulation, year and semester to browse subjects.</p>
    <div class="pill-row" id="regPills">{reg_pills}</div>
    <div class="pill-row" id="yearPills"></div>
    <div class="pill-row" id="semPills" style="display:none;"></div>
    <div class="subject-list" id="subjectList"></div>
    <div id="fullSyllabusBtn" style="display:none; margin-top:20px;"></div>'''

    replaced = False
    for pattern in old_html_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_html + content[match.end():]
            replaced = True
            break

    if not replaced:
        print(f'{dept}: Could not find old selector HTML')
        continue

    # 6. Replace the JS syllabus logic
    # Find the old syllabus IIFE and replace its internals
    # We need to replace progPills/yearPills logic with regPills logic

    # Build the new JS
    is_mba = dept == 'mba'

    new_syllabus_js = f'''    // Syllabus selector
    (function () {{
      {old_programs}
      {regs_js}
      var subjectDetails = {{}};''' + '''
      // Try to get existing subjectDetails
      '''

    # Extract existing subjectDetails if any
    sd_match = re.search(r'(var subjectDetails = \{.*?\n\s+\};)', content, re.DOTALL)
    if sd_match:
        new_syllabus_js = f'''    // Syllabus selector
    (function () {{
      {old_programs}
      {regs_js}
      {sd_match.group(1)}'''

    new_syllabus_js += f'''
      var regPills = document.getElementById('regPills');
      var yearPills = document.getElementById('yearPills');
      var semPillsRow = document.getElementById('semPills');
      var subjectList = document.getElementById('subjectList');
      var fullSyllabusBtn = document.getElementById('fullSyllabusBtn');
      var currentReg = '{first_reg}';
      var selectedYear = null;

      function buildYearPills() {{
        var regData = regulations[currentReg].data;
        var years = Object.keys(regData);
        yearPills.innerHTML = '';
        years.forEach(function (y) {{
          var p = document.createElement('button');
          p.className = 'pill'; p.setAttribute('data-year', y);
          p.textContent = 'Year ' + y; yearPills.appendChild(p);
        }});
        semPillsRow.innerHTML = ''; semPillsRow.style.display = 'none';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
        if (fullSyllabusBtn) fullSyllabusBtn.style.display = 'none';
        selectedYear = null;
      }}
      buildYearPills();

      regPills.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pill'); if (!btn) return;
        currentReg = btn.getAttribute('data-reg');
        regPills.querySelectorAll('.pill').forEach(function (p) {{ p.classList.remove('is-active'); }});
        btn.classList.add('is-active'); buildYearPills();
      }});

      yearPills.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pill'); if (!btn) return;
        var year = parseInt(btn.getAttribute('data-year')); selectedYear = year;
        yearPills.querySelectorAll('.pill').forEach(function (p) {{ p.classList.remove('is-active'); }}); btn.classList.add('is-active');
        var sems = Object.keys(regulations[currentReg].data[year]);
        semPillsRow.innerHTML = '';
        sems.forEach(function (s) {{
          var p = document.createElement('button'); p.className = 'pill';
          p.setAttribute('data-sem', s); p.textContent = 'Sem ' + s; semPillsRow.appendChild(p);
        }});
        semPillsRow.style.display = 'flex'; subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
        if (fullSyllabusBtn) fullSyllabusBtn.style.display = 'none';
      }});

      semPillsRow.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pill'); if (!btn || !selectedYear) return;
        var sem = parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function (p) {{ p.classList.remove('is-active'); }}); btn.classList.add('is-active');
        var subjects = regulations[currentReg].data[selectedYear][sem]; if (!subjects) return;
        var pdfUrl = regulations[currentReg].pdf;
        var html = '';
        subjects.forEach(function (name, i) {{
          var subName = typeof name === 'object' ? name[1] : name;
          var subCode = typeof name === 'object' ? name[0] : '';
          var units = subjectDetails[subName]; var uh = '';
          if (units && units.length) {{ uh = '<div class="subject-units"><ol>'; units.forEach(function (u) {{ uh += '<li>' + u + '</li>'; }}); uh += '</ol></div>'; }}
          var codeHtml = subCode ? '<span class="subject-code">' + subCode + '</span>' : '<span class="subject-num">' + (i+1) + '.</span>';
          html += '<div class="subject-row" onclick="this.classList.toggle(\\'is-expanded\\')">' + codeHtml + '<span class="subject-name">' + subName + '</span><span class="subject-toggle">&#9654;</span><a href="' + pdfUrl + '" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">PDF</a></div>' + uh;
        }});
        subjectList.innerHTML = html; subjectList.classList.remove('is-visible'); void subjectList.offsetWidth; subjectList.classList.add('is-visible');
        if (fullSyllabusBtn) {{
          fullSyllabusBtn.innerHTML = '<a href="' + pdfUrl + '" target="_blank" class="full-syllabus-btn">Download Full ' + regulations[currentReg].label + ' Syllabus &rarr;</a>';
          fullSyllabusBtn.style.display = 'block';
        }}
      }});
    }})();'''

    # Replace the old syllabus IIFE
    # Find it by looking for the pattern "// Syllabus" section
    old_syll_match = re.search(r'    // Syllabus.*?\n    \}\)\(\);', content, re.DOTALL)
    if old_syll_match:
        content = content[:old_syll_match.start()] + new_syllabus_js + content[old_syll_match.end():]
    else:
        print(f'{dept}: Could not find old syllabus JS')
        continue

    # 7. Remove SWAYAM section if present
    content = re.sub(r'\s*<div class="panel-sub">SWAYAM.*?</p>\s*', '\n', content, flags=re.DOTALL)

    # 8. Remove old "Online Course Catalog" or "Course Catalog" that used external links
    # Keep only our new download section

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify JS
    import subprocess
    js_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if js_match:
        with open('c:/mlr/test_js.js', 'w', encoding='utf-8') as jf:
            jf.write(js_match.group(1))
        result = subprocess.run(['node', '--check', 'c:/mlr/test_js.js'], capture_output=True, text=True)
        js_ok = 'OK' if result.returncode == 0 else 'ERROR: ' + result.stderr[:100]
    else:
        js_ok = 'NO SCRIPT'

    regs = list(cfg['regulations'].keys())
    print(f'{dept}: updated — regs={regs} js={js_ok}')

print('\nDone.')
