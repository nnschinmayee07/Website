import re

def extract(content, pattern, default=''):
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1) if m else default

def rebuild_dept(dept, title_short, title_full, eyebrow, overview_text, vision, mission, peos, catalog_links, faculty_count):
    with open(f'c:/mlr/homepage/departments/{dept}.html', encoding='utf-8') as f:
        old = f.read()

    # Extract faculty lane
    m = re.search(r'(<div class="faculty-lane">.*?</div>\s*</section>)', old, re.DOTALL)
    faculty_html = re.sub(r'\s*</section>\s*$', '', m.group(1)) if m else '<div class="faculty-lane">Faculty data unavailable</div>'

    # Extract achievements
    m = re.search(r'(<div class="achieve-grid">.*?</div>\s*</section>)', old, re.DOTALL)
    achieve_html = re.sub(r'\s*</section>\s*$', '', m.group(1)) if m else ''

    # Extract publications
    m = re.search(r'(<div class="pub-filters".*?</div>\s*</section>)', old, re.DOTALL)
    pubs_html = re.sub(r'\s*</section>\s*$', '', m.group(1)) if m else ''

    # Extract internships
    m = re.search(r'(<div class="intern-stats">.*?<p class="intern-note">.*?</p>)', old, re.DOTALL)
    intern_html = m.group(1) if m else ''

    # Extract JS data
    m = re.search(r'(var programs = \{.*?\n\s+\};)', old, re.DOTALL)
    programs_js = m.group(1) if m else 'var programs = {};'

    m = re.search(r'(var subjectDetails = \{.*?\n\s+\};)', old, re.DOTALL)
    subjects_js = m.group(1) if m else 'var subjectDetails = {};'

    m = re.search(r'(var syllabusUrls = \{.*?\};)', old, re.DOTALL)
    urls_js = m.group(1) if m else "var syllabusUrls = { btech: '#', mtech: '#' };"

    # Read CSE template for CSS
    with open('c:/mlr/homepage/departments/cse.html', encoding='utf-8') as f:
        cse = f.read()

    css_match = re.search(r'(<style>.*?</style>)', cse, re.DOTALL)
    css_block = css_match.group(1) if css_match else '<style></style>'

    # PEO cards
    peo_html = ''
    for i, peo in enumerate(peos, 1):
        peo_html += '      <div class="card card--accent" style="text-align:center;">\n'
        peo_html += '        <div class="peo-num">PEO ' + str(i) + '</div>\n'
        peo_html += '        <p>' + peo + '</p>\n'
        peo_html += '      </div>\n'

    # Catalog links
    catalog_html = ''
    for label, sub, url in catalog_links:
        catalog_html += '      <a href="' + url + '" target="_blank" class="catalog-item">\n'
        catalog_html += '        <span class="catalog-item__icon">&#128196;</span>\n'
        catalog_html += '        <div><span class="catalog-item__text">' + label + '</span><span class="catalog-item__sub">' + sub + '</span></div>\n'
        catalog_html += '      </a>\n'

    # OBE M.Tech block
    obe_mtech = ''
    if dept != 'mba':
        obe_mtech = '''<div class="obe-col">
        <h4>M.Tech</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>'''

    btech_or_mba = 'B.Tech' if dept != 'mba' else 'MBA'

    # Prog pills (MBA has no M.Tech toggle)
    if dept == 'mba':
        prog_pills = '''    <div class="pill-row" id="yearPills"></div>'''
        prog_pills_init = ''
    else:
        prog_pills = '''    <div class="pill-row" id="progPills">
      <button class="pill is-active" data-prog="btech">B.Tech</button>
      <button class="pill" data-prog="mtech">M.Tech</button>
    </div>
    <div class="pill-row" id="yearPills"></div>'''
        prog_pills_init = '''
      if (window.location.hash === '#mtech') {
        var mtechBtn = progPills.querySelector('[data-prog="mtech"]');
        if (mtechBtn) mtechBtn.click();
      }
      progPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill');
        if (!btn) return;
        currentProg = btn.getAttribute('data-prog');
        progPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active');
        buildYearPills();
      });'''

    prog_pills_var = 'var progPills = document.getElementById("progPills");\n      ' if dept != 'mba' else ''
    js_current_prog = 'btech' if dept != 'mba' else '1'
    js_curriculum_ref = 'programs[currentProg]' if dept != 'mba' else 'curriculum'
    js_curriculum_year = 'programs[currentProg][year]' if dept != 'mba' else 'curriculum[year]'
    js_subjects_ref = 'programs[currentProg][selectedYear][sem]' if dept != 'mba' else 'curriculum[selectedYear][sem]'
    js_pdf_ref = 'syllabusUrls[currentProg]' if dept != 'mba' else "\"#\""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title_short} Department — MLRIT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/navbar.css" />
  <link rel="stylesheet" href="../css/main.css" />
  {css_block}
</head>
<body>

  <header class="site-header">
    <div class="masthead">
      <div class="container masthead__inner">
        <a href="../index.html" class="masthead__logo" aria-label="MLRIT Home">
          <img src="../mlrit-logo-transparent.png" alt="MLRIT Logo" />
        </a>
        <div class="masthead__tagline">
          <span>Marri Laxman Reddy Institute of Technology</span>
        </div>
        <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      </div>
    </div>
  </header>

  <div class="dept-hero">
    <div class="dept-hero__eyebrow">{eyebrow}</div>
    <div class="dept-hero__title">{title_full}</div>
  </div>

  <nav class="dept-tabs" id="deptTabs">
    <a class="dept-tab is-active" data-tab="overview">Overview</a>
    <a class="dept-tab" data-tab="objectives">Objectives &amp; OBE</a>
    <a class="dept-tab" data-tab="faculty">Faculty Profiles</a>
    <a class="dept-tab" data-tab="academics">Academics &amp; Syllabus</a>
    <a class="dept-tab" data-tab="achievements">Achievements &amp; Research</a>
  </nav>

  <!-- TAB 1: Overview -->
  <div class="dept-panel is-active" id="panel-overview">
    <h2 class="panel-heading">About the Department</h2>
    {overview_text}
    <div class="panel-sub">Vision &amp; Mission</div>
    <div class="two-col">
      <div class="card card--accent"><h3>Vision</h3><p>{vision}</p></div>
      <div class="card card--accent"><h3>Mission</h3><p>{mission}</p></div>
    </div>
  </div>

  <!-- TAB 2: Objectives & OBE -->
  <div class="dept-panel" id="panel-objectives">
    <h2 class="panel-heading">Programme Educational Objectives</h2>
    <div class="three-col">
{peo_html}    </div>
    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>{btech_or_mba}</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>
      {obe_mtech}
    </div>
    <div class="panel-sub">Handbook</div>
    <div class="card" style="max-width:500px;">
      <h3>{title_short} Department Handbook</h3>
      <p>{title_full} — Academic Year 2025–26</p>
    </div>
  </div>

  <!-- TAB 3: Faculty -->
  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Scroll to explore {faculty_count} faculty members. Hover for research details, click for full profile.</p>
    {faculty_html}
  </div>

  <!-- TAB 4: Academics -->
  <div class="dept-panel" id="panel-academics">
    <h2 class="panel-heading">Academics &amp; Syllabus</h2>
    <div class="panel-sub">Course Catalog</div>
    <div class="catalog-grid">
{catalog_html}    </div>
    <div class="panel-sub">Semester-wise Syllabus Explorer</div>
    <p style="font-style:italic; color:#666; margin-bottom:20px;">Select programme, year and semester to browse subjects.</p>
    {prog_pills}
    <div class="pill-row" id="semPills" style="display:none;"></div>
    <div class="subject-list" id="subjectList"></div>
  </div>

  <!-- TAB 5: Achievements & Research -->
  <div class="dept-panel" id="panel-achievements">
    <h2 class="panel-heading">Achievements</h2>
    {achieve_html}
    <div class="panel-sub">Publications</div>
    {pubs_html}
    <div class="panel-sub">Internships &amp; Placements</div>
    {intern_html}
  </div>

  <script>
    // Tab switching
    (function () {{
      var tabs = document.querySelectorAll('.dept-tab');
      var panels = document.querySelectorAll('.dept-panel');
      tabs.forEach(function (tab) {{
        tab.addEventListener('click', function () {{
          tabs.forEach(function (t) {{ t.classList.remove('is-active'); }});
          panels.forEach(function (p) {{ p.classList.remove('is-active'); }});
          tab.classList.add('is-active');
          var panel = document.getElementById('panel-' + tab.getAttribute('data-tab'));
          if (panel) panel.classList.add('is-active');
        }});
      }});
      var hash = window.location.hash.replace('#', '');
      if (hash) {{ var target = document.querySelector('[data-tab="' + hash + '"]'); if (target) target.click(); }}
    }})();

    // Syllabus selector
    (function () {{
      {programs_js}
      {urls_js}
      {subjects_js}
      {prog_pills_var}var yearPills = document.getElementById('yearPills');
      var semPillsRow = document.getElementById('semPills');
      var subjectList = document.getElementById('subjectList');
      var currentProg = '{js_current_prog}';
      var selectedYear = null;

      function buildYearPills() {{
        var curriculum = {js_curriculum_ref};
        var years = Object.keys(curriculum);
        yearPills.innerHTML = '';
        years.forEach(function (y) {{
          var pill = document.createElement('button');
          pill.className = 'pill';
          pill.setAttribute('data-year', y);
          pill.textContent = 'Year ' + y;
          yearPills.appendChild(pill);
        }});
        semPillsRow.innerHTML = ''; semPillsRow.style.display = 'none';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
        selectedYear = null;
      }}

      buildYearPills();
      {prog_pills_init}

      yearPills.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pill');
        if (!btn) return;
        var year = parseInt(btn.getAttribute('data-year'));
        selectedYear = year;
        yearPills.querySelectorAll('.pill').forEach(function (p) {{ p.classList.remove('is-active'); }});
        btn.classList.add('is-active');
        var sems = Object.keys({js_curriculum_year});
        semPillsRow.innerHTML = '';
        sems.forEach(function (sem) {{
          var pill = document.createElement('button');
          pill.className = 'pill';
          pill.setAttribute('data-sem', sem);
          pill.textContent = 'Sem ' + sem;
          semPillsRow.appendChild(pill);
        }});
        semPillsRow.style.display = 'flex';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
      }});

      semPillsRow.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pill');
        if (!btn || !selectedYear) return;
        var sem = parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function (p) {{ p.classList.remove('is-active'); }});
        btn.classList.add('is-active');
        var subjects = {js_subjects_ref};
        if (!subjects) return;
        var html = '';
        subjects.forEach(function (name, i) {{
          var units = subjectDetails[name];
          var unitsHtml = '';
          if (units && units.length) {{
            unitsHtml = '<div class="subject-units"><ol>';
            units.forEach(function (u) {{ unitsHtml += '<li>' + u + '</li>'; }});
            unitsHtml += '</ol></div>';
          }}
          html += '<div class="subject-row" onclick="this.classList.toggle(\\'is-expanded\\')"><span class="subject-num">' + (i + 1) + '.</span><span class="subject-name">' + name + '</span><span class="subject-toggle">&#9654;</span><a href="' + {js_pdf_ref} + '" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">PDF</a></div>' + unitsHtml;
        }});
        subjectList.innerHTML = html;
        subjectList.classList.remove('is-visible');
        void subjectList.offsetWidth;
        subjectList.classList.add('is-visible');
      }});
    }})();

    // Publication filter
    (function () {{
      var filters = document.getElementById('pubFilters');
      var cards = document.querySelectorAll('.pub-card');
      if (!filters || !cards.length) return;
      filters.addEventListener('click', function (e) {{
        var btn = e.target.closest('.pub-filter');
        if (!btn) return;
        var year = btn.getAttribute('data-year');
        filters.querySelectorAll('.pub-filter').forEach(function (f) {{ f.classList.remove('is-active'); }});
        btn.classList.add('is-active');
        cards.forEach(function (card) {{
          var match = (year === 'all' || card.getAttribute('data-pub-year') === year);
          if (match) {{ card.classList.remove('is-hidden'); card.style.display = 'flex'; }}
          else {{ card.classList.add('is-hidden'); setTimeout(function () {{ if (card.classList.contains('is-hidden')) card.style.display = 'none'; }}, 350); }}
        }});
      }});
    }})();

    // Achievement toggle
    (function () {{
      document.querySelectorAll('[data-achieve]').forEach(function (card) {{
        var toggle = card.querySelector('.achieve-toggle');
        card.addEventListener('click', function () {{
          var expanded = card.classList.toggle('is-expanded');
          if (toggle) toggle.textContent = expanded ? 'Read Less' : 'Read More';
        }});
      }});
    }})();

    // Faculty profile click
    (function () {{
      document.querySelectorAll('.faculty-item').forEach(function (item) {{
        item.addEventListener('click', function () {{
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
          var areas = []; tags.forEach(function(t) {{ areas.push(t.textContent); }});
          var id = n.toLowerCase().replace(/Dr\\.|Mr\\.|Mrs\\.|Ms\\.|Prof\\./g, '').trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
          window.location.href = 'faculty-profile.html?name=' + encodeURIComponent(n) + '&role=' + encodeURIComponent(r) + '&qual=' + encodeURIComponent(q) + '&photo=' + encodeURIComponent(p) + '&areas=' + encodeURIComponent(areas.join(',')) + '#' + id;
        }});
      }});
    }})();
  </script>
</body>
</html>'''

    # Fix escaped quotes
    html = html.replace("\\\\'is-expanded\\\\'", "'is-expanded'")

    with open(f'c:/mlr/homepage/departments/{dept}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{dept}: rebuilt ({len(html)} bytes)')

# Department configs
configs = {
    'ece': {
        'title_short': 'ECE',
        'title_full': 'Department of Electronics &amp; Communication Engineering',
        'eyebrow': 'B.Tech &middot; Electronics &amp; Communication Engineering',
        'overview': '<p>The ECE Department was established in 2005 with an initial intake of 60 students. Following the institution\'s autonomous status in 2015, the department now offers a four-year B.Tech program with 120 students and two postgraduate programs in Embedded Systems. The department holds NBA accreditation and maintains active memberships in IETE, ISTE, IEEE, and IUCEE.</p>',
        'vision': 'To provide quality technical education with innovation and importance to R&amp;D, fulfilling societal needs while achieving academic excellence in preparing globally competent engineers.',
        'mission': 'Adopt innovative student-centric learning approaches, foster research-oriented perspectives, enable national and international competitive capabilities, and strengthen core competencies through experiential curriculum.',
        'peos': ['Excel in core engineering with foundational mathematics and science knowledge', 'Develop solid fundamentals for lifelong professional and higher education success', 'Demonstrate effective design, management, and leadership skills at national and multinational levels'],
        'catalog': [
            ('B.Tech Course Catalog — R25', 'Latest regulation', 'http://files.mlrit.ac.in/uploads/ECE/R25_ECE.pdf'),
            ('B.Tech Course Catalog — R22', '2022 regulation', 'http://files.mlrit.ac.in/uploads/ECE/R22_ECE.pdf'),
            ('M.Tech Course Catalog — R22', 'PG regulation', 'https://mlrit.ac.in/curriculum/ece-m-tech-r22-syllabus/'),
        ],
        'fac_count': 36,
    },
    'eee': {
        'title_short': 'EEE',
        'title_full': 'Department of Electrical &amp; Electronics Engineering',
        'eyebrow': 'B.Tech &middot; Electrical &amp; Electronics Engineering',
        'overview': '<p>The EEE department offers state-of-the-art facilities and experienced faculty. It features acoustically-designed classrooms, well-equipped laboratories with modern instruments, and integration of seminars and workshops to support comprehensive technical education. The department has a 260 kWp rooftop solar plant installation.</p>',
        'vision': 'To impart students with strong fundamental and applied knowledge to identify, analyze and research on upcoming energy related challenges that provide optimal solutions to the society and nation needs.',
        'mission': 'Deliver core and advanced knowledge across all EEE domains, foster research and innovation to address emerging challenges, and develop entrepreneurial and leadership capabilities for eco-friendly energy solutions.',
        'peos': ['Excel in core engineering with mathematics and science foundations', 'Build problem-solving skills through research while instilling human values', 'Demonstrate design, management, and leadership expertise at national and multinational organizations'],
        'catalog': [
            ('B.Tech Course Catalog — R22', '2022 regulation', 'https://files.mlrit.ac.in/syllabus/EEE/22/EEE-R22.pdf'),
            ('B.Tech Course Catalog — MLR20', '2020 regulation', 'https://mlrit.ac.in/curriculum/eee-mlr20-syllabus/'),
        ],
        'fac_count': 17,
    },
    'mechanical': {
        'title_short': 'Mechanical',
        'title_full': 'Department of Mechanical Engineering',
        'eyebrow': 'B.Tech &middot; Mechanical Engineering',
        'overview': '<p>The Mechanical Engineering Department endeavors to be recognized globally for outstanding education and research. The department offers undergraduate and postgraduate (M.Tech) programs with specializations in Advanced Composite Materials, Product Life Cycle Management, and Nondestructive Testing. Active partnerships with Mahindra &amp; Mahindra and Pennar Industries.</p>',
        'vision': 'To be recognized globally for outstanding education and research leading to well qualified engineers, who are innovative, entrepreneurial and successful in advanced fields of mechanical engineering to cater the ever changing industrial demands.',
        'mission': 'Deliver high-quality education to develop globally competitive engineers and entrepreneurs, while providing academic environment of excellence, state of the art research facilities, leadership, ethical guidelines and lifelong learning.',
        'peos': ['Excellence in undergraduate and postgraduate studies and professional careers', 'Data analysis, synthesis, and product design capabilities across specializations', 'Strong communication, ethical standards, and emerging technology leadership'],
        'catalog': [
            ('B.Tech Course Catalog — R25', 'Latest regulation', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_UG-R25.pdf'),
            ('B.Tech Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/mechanical-r22-syllabus/'),
            ('M.Tech Course Catalog — R25', 'PG latest', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_PG-R25.pdf'),
            ('M.Tech Course Catalog — R22', 'PG regulation', 'https://mlrit.ac.in/curriculum/mechanical-m-tech-r22-syllabus/'),
        ],
        'fac_count': 20,
    },
    'aeronautical': {
        'title_short': 'Aeronautical',
        'title_full': 'Department of Aeronautical Engineering',
        'eyebrow': 'B.Tech &middot; Aeronautical Engineering',
        'overview': '<p>The Aeronautical Engineering department provides excellent infrastructure and state-of-the-art laboratories for graduate research and innovation in aerospace engineering. Features include Flight Simulation Lab, Digital Manufacturing Lab, and Centre for Innovation and Entrepreneurship. Active collaborations with DRDO, Tata Advanced Systems, and Boeing India.</p>',
        'vision': 'To be a centre of excellence in Aeronautical engineering with emphasis on Research and Innovation to serve the needs of industry with human values to build strong nation.',
        'mission': 'Consistently produce top quality Aeronautical engineers with core and multidisciplinary skills, who can become ace leaders and successful entrepreneurs with human values.',
        'peos': ['Prepare students for successful careers in industrial, academic, and entrepreneurial sectors', 'Develop technical problem-solving abilities through data analysis and product design', 'Foster communication skills, ethical attitudes, and leadership in emerging technology'],
        'catalog': [
            ('B.Tech Course Catalog — R25', 'Latest regulation', 'https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_Aero_Syllabus.pdf'),
            ('B.Tech Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/aeronautical-r22-syllabus/'),
            ('M.Tech Course Catalog — R22', 'PG regulation', 'https://mlrit.ac.in/curriculum/aeronautical-m-tech-r22-syllabus/'),
        ],
        'fac_count': 19,
    },
    'mba': {
        'title_short': 'MBA',
        'title_full': 'Department of Master of Business Administration',
        'eyebrow': 'MBA &middot; Master of Business Administration',
        'overview': '<p>The MBA program at MLRIT emphasizes how innovation, business and technology are inseparable for business sustenance and long term growth. It prepares students for management roles across all industries through quality education and industry exposure. The department has an active Entrepreneurship Cell and regular guest lectures from CXO-level professionals.</p>',
        'vision': 'Centre of Excellence for Management Studies with special focus on innovation, Research, entrepreneurial skills, and team working skills.',
        'mission': 'Student-centered education emphasizing innovation, research, and entrepreneurship. Social impact projects incorporating human values, diversity, and ethics. Development of analytical and decision-making abilities for effective leadership.',
        'peos': ['Apply management theories to handle business and entrepreneurial challenges', 'Develop critical thinking for better decision-making and innovation', 'Build value-based leadership competencies and contribute effectively to organizational teams'],
        'catalog': [
            ('MBA Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/mba-r22-syllabus/'),
            ('MBA Course Catalog — MLR20', '2020 regulation', 'https://mlrit.ac.in/curriculum/mba-mlr20-syllabus/'),
        ],
        'fac_count': 15,
    },
}

for dept, cfg in configs.items():
    rebuild_dept(
        dept=dept,
        title_short=cfg['title_short'],
        title_full=cfg['title_full'],
        eyebrow=cfg['eyebrow'],
        overview_text=cfg['overview'],
        vision=cfg['vision'],
        mission=cfg['mission'],
        peos=cfg['peos'],
        catalog_links=cfg['catalog'],
        faculty_count=cfg['fac_count'],
    )
