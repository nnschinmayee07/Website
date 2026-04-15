import re, glob

# ═══════════════════════════════════════════
# PATCH 1: Remove faculty popup CSS + HTML hover clouds
# PATCH 2: Update OBE section with real PO/PSO content
# PATCH 3: Update faculty click to go directly to profile
# ═══════════════════════════════════════════

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in filepath or 'ug.html' in filepath or 'pg.html' in filepath:
        continue

    dept = filepath.rsplit('/', 1)[1].replace('.html', '')
    print(f'\nPatching {dept}...')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ─── PATCH 1: Remove popup CSS ───
    # Remove the popup display rule (hover shows popup)
    content = content.replace(
        '.faculty-item:hover .faculty-popup { display: block; animation: popIn 0.25s ease; }',
        '/* popup removed — click goes to profile page */'
    )

    # ─── PATCH 2: Remove all popup HTML divs from faculty items ───
    # Pattern: <div class="faculty-popup">...</div> (at the end of each faculty-item)
    content = re.sub(
        r'\s*<div class="faculty-popup">.*?</div>\s*(?=</div>\s*(?:<div class="faculty-item"|</div>))',
        '\n',
        content,
        flags=re.DOTALL
    )

    # ─── PATCH 3: Replace OBE placeholder with real content ───
    # Find the OBE section
    obe_placeholder = '''    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>B.Tech</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>'''

    obe_real_btech = '''    <div class="panel-sub">Programme Outcomes (POs)</div>
    <div style="max-width:780px;">
      <div class="obe-list-numbered">
        <p><strong>PO1:</strong> Apply knowledge of mathematics, science, engineering fundamentals, and engineering specialization to solve complex engineering problems.</p>
        <p><strong>PO2:</strong> Identify, formulate, review research literature, and analyze complex engineering problems reaching substantiated conclusions.</p>
        <p><strong>PO3:</strong> Design solutions for complex engineering problems considering public health, safety, cultural, societal, and environmental factors.</p>
        <p><strong>PO4:</strong> Conduct investigations using research methods, experimental design, data analysis, and synthesis to validate conclusions.</p>
        <p><strong>PO5:</strong> Create, select, and apply appropriate techniques, resources, and modern engineering and IT tools including prediction and modeling.</p>
        <p><strong>PO6:</strong> Assess societal, health, safety, legal, and cultural implications relevant to professional engineering responsibilities.</p>
        <p><strong>PO7:</strong> Demonstrate awareness of professional engineering solutions' impact on society and environmental sustainability.</p>
        <p><strong>PO8:</strong> Apply ethical principles and commit to professional ethics, responsibilities, and norms of engineering practice.</p>
        <p><strong>PO9:</strong> Function effectively as an individual, team member, or leader in diverse and multidisciplinary environments.</p>
        <p><strong>PO10:</strong> Communicate complex engineering activities effectively through reports, documentation, presentations, and clear instructions.</p>
        <p><strong>PO11:</strong> Demonstrate knowledge and understanding of engineering and management principles and apply these to one's own work.</p>
        <p><strong>PO12:</strong> Recognize the need for and pursue continuous, independent learning amid technological advancements.</p>
      </div>
    </div>

    <div class="panel-sub">Programme Specific Outcomes (PSOs)</div>
    <div style="max-width:780px;">
      <p><strong>PSO1:</strong> Master software system structures and development methodologies to tackle contemporary computing challenges.</p>
      <p><strong>PSO2:</strong> Develop intelligent and autonomous systems to cater societal needs in health care, e-commerce, banking, agriculture, cyber security, and insurance.</p>
    </div>

    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>B.Tech</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>'''

    content = content.replace(obe_placeholder, obe_real_btech)

    # Also handle MBA which has different OBE structure
    obe_mba_placeholder = '''    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>MBA</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>'''

    obe_mba_real = '''    <div class="panel-sub">Programme Outcomes (POs)</div>
    <div style="max-width:780px;">
      <div class="obe-list-numbered">
        <p><strong>PO1:</strong> Apply management concepts and practices to analyze business situations and make effective decisions.</p>
        <p><strong>PO2:</strong> Develop leadership, teamwork, and communication skills for managing diverse organizational environments.</p>
        <p><strong>PO3:</strong> Demonstrate ethical reasoning and social responsibility in business practices.</p>
        <p><strong>PO4:</strong> Utilize analytical and quantitative tools for data-driven decision making.</p>
        <p><strong>PO5:</strong> Exhibit entrepreneurial mindset and innovation in creating business value.</p>
        <p><strong>PO6:</strong> Understand global business dynamics and their implications for strategic management.</p>
      </div>
    </div>

    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>MBA</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>'''

    content = content.replace(obe_mba_placeholder, obe_mba_real)

    # ─── PATCH 4: Add OBE Portal link ───
    old_handbook = '    <div class="panel-sub">Handbook</div>'
    new_before_handbook = '''    <div class="panel-sub" style="margin-top:28px;">OBE Portal</div>
    <div class="card" style="max-width:500px;">
      <h3>OBE Assessment System</h3>
      <p>Access the Outcome Based Education portal for CO/PO attainment data and assessment tools.</p>
      <a href="http://103.15.62.235/ioncudos_mlrit_tier1/" target="_blank" style="font-family:Raleway,sans-serif;font-size:0.78rem;font-weight:700;color:#E85D1F;text-decoration:none;">Open OBE Portal &rarr;</a>
    </div>

    <div class="panel-sub">Handbook</div>'''
    content = content.replace(old_handbook, new_before_handbook)

    # ─── PATCH 5: Update faculty click JS — remove popup data extraction, use data attributes ───
    old_faculty_js = '''    // Faculty profile click
    (function () {
      document.querySelectorAll('.faculty-item').forEach(function (item) {
        item.addEventListener('click', function () {
          var popup = item.querySelector('.faculty-popup');
          if (!popup) return;
          var name = popup.querySelector('.faculty-popup__name');
          var role = popup.querySelector('.faculty-popup__role');
          var qual = popup.querySelector('.faculty-popup__detail');
          var photo = item.querySelector('.faculty-item__photo img');
          var tags = popup.querySelectorAll('.faculty-popup__tag');
          var n = name ? name.textContent : '';
          var r = role ? role.textContent : '';
          var q = qual ? qual.textContent.replace('Qualification: ', '') : '';
          var p = photo ? photo.getAttribute('src') : '';
          var areas = []; tags.forEach(function(t) { areas.push(t.textContent); });
          var id = n.toLowerCase().replace(/Dr\\.|Mr\\.|Mrs\\.|Ms\\.|Prof\\./g, '').trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
          window.location.href = 'faculty-profile.html?name=' + encodeURIComponent(n) + '&role=' + encodeURIComponent(r) + '&qual=' + encodeURIComponent(q) + '&photo=' + encodeURIComponent(p) + '&areas=' + encodeURIComponent(areas.join(',')) + '#' + id;
        });
      });
    })();'''

    new_faculty_js = '''    // Faculty profile click — direct to profile page
    (function () {
      document.querySelectorAll('.faculty-item').forEach(function (item) {
        item.addEventListener('click', function () {
          var nameEl = item.querySelector('.faculty-item__name');
          var roleEl = item.querySelector('.faculty-item__role');
          var photo = item.querySelector('.faculty-item__photo img');
          var n = nameEl ? nameEl.textContent : '';
          var r = roleEl ? roleEl.textContent : '';
          var p = photo ? photo.getAttribute('src') : '';
          var id = n.toLowerCase().replace(/Dr\\.|Mr\\.|Mrs\\.|Ms\\.|Prof\\./g, '').trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
          window.location.href = 'faculty-profile.html?name=' + encodeURIComponent(n) + '&role=' + encodeURIComponent(r) + '&photo=' + encodeURIComponent(p) + '#' + id;
        });
      });
    })();'''

    content = content.replace(old_faculty_js, new_faculty_js)

    # ─── PATCH 6: Add CSS for PO numbered list ───
    content = content.replace(
        '.obe-list li::before { content:',
        '''.obe-list-numbered p { font-size: 0.88rem; color: #444; line-height: 1.6; margin-bottom: 10px; max-width: none; }
    .obe-list-numbered p strong { color: #18453B; font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.78rem; letter-spacing: 0.04em; }
    .obe-list li::before { content:'''
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify
    popups_remaining = content.count('faculty-popup">')
    po_count = content.count('<strong>PO')
    print(f'  popups remaining: {popups_remaining}, POs: {po_count}')

print('\nAll done.')
