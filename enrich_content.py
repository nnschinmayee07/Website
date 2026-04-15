import re, glob

# ═══════════════════════════════════════
# Department-specific enrichment data
# ═══════════════════════════════════════

dept_data = {
    'cse': {
        'history': 'The Department of Computer Science and Engineering was established in 2005 with an initial intake of 60 students. The intake was progressively increased — 120 in 2007, 180 in 2012, 240 in 2013, and 840 in 2024. An additional 10% seats are available under the lateral entry scheme. The M.Tech programme in CSE commenced in 2011 with an intake of 6.',
        'nba': 'The B.Tech (CSE) program has been accredited by the National Board of Accreditation (NBA) since 2008, demonstrating sustained quality in engineering education. The department consistently meets NBA\'s outcome-based education criteria.',
        'labs': [
            ('Case Tools &amp; Web Technologies Lab', '69 systems — Software design tools, web development frameworks'),
            ('Data Structures &amp; Web Services Lab', '30 systems — M.Tech data structures and web services'),
            ('Cryptography &amp; Network Security Lab', '30 systems — Encryption, network protection, security protocols'),
            ('Mobile Application Development Lab', '36 systems — Android Studio, Flutter, app development'),
            ('Operating Systems Lab', '60 systems — OS concepts, process management, Linux'),
            ('Java Programming Lab', '60 systems — JDK, OOP concepts, enterprise Java'),
            ('Cloud Computing Lab', '30 systems — Cloud infrastructure, AWS, virtualization'),
            ('Linux Programming Lab', '30 systems — System programming, shell scripting'),
            ('Project Work Lab', '60 systems — Final year projects and mini-projects'),
            ('Object Oriented Programming Lab', '36 systems — C++, OOP principles'),
            ('Data Mining &amp; Warehousing Lab', '30 systems — Informatica, Weka, data analysis'),
            ('Database Management Systems Lab', '36 systems — SQL, database design, Oracle'),
        ],
        'honour': [
            ('2013', 'Sheekha Singh', 'University Topper', '86%'),
            ('2015', 'V. Bhavana', 'University Rank Holder', '84%'),
            ('2011', 'Pankaj Agarwal', 'University Rank Holder', '84%'),
            ('2012', 'S. Geetha Veera Lakshmi', 'Department Topper', '81%'),
            ('2014', 'M. Mounika', 'Department Topper', '81%'),
            ('2016', 'Hari Priya D S', 'Department Topper', '80.82%'),
            ('2018', 'Nallagari Sravani', 'Department Topper', '79.12%'),
        ],
        'student_achieve': [
            'Smart India Hackathon — National Finalists (Team CodeCraft, 2024)',
            '140+ NPTEL certifications in a single semester — NPTEL Discipline Star',
            'IEEE Student Branch — Engineering Project Expo with 15+ college participation',
            'CSI Student Chapter — Annual workshops, coding competitions, tech talks',
            'Amazon ML Summer School — 8 students selected (2024)',
        ],
    },
    'ece': {
        'history': 'The ECE Department was established in 2005 with an initial intake of 60 students. Following the institution\'s autonomous status in 2015, the department now offers B.Tech with 120 intake and M.Tech in Embedded Systems. Active memberships in IETE, ISTE, IEEE, and IUCEE.',
        'nba': 'The B.Tech ECE programme holds NBA accreditation, reflecting its commitment to outcome-based education and continuous quality improvement.',
        'labs': [
            ('Cadence Centre of Excellence', 'VLSI design tools, Cadence Virtuoso, digital design'),
            ('MATLAB Centre of Excellence', 'Signal processing, simulation, algorithm development'),
            ('Embedded Systems &amp; Robotics Lab', 'ARM processors, RTOS, sensor interfacing'),
            ('LabVIEW Centre of Excellence', 'Virtual instrumentation, data acquisition'),
            ('Microprocessors Lab', '8086/8051 programming, interfacing peripherals'),
            ('DSP Lab', 'Digital signal processing, filter design'),
            ('Communication Systems Lab', 'AM/FM modulation, antenna measurements'),
            ('VLSI Design Lab', 'FPGA programming, Verilog, synthesis'),
        ],
        'honour': [
            ('2015', 'K. Sai Priya', 'University Rank Holder', '83%'),
            ('2016', 'R. Anusha', 'Department Topper', '80%'),
            ('2018', 'M. Kavitha', 'Department Topper', '78%'),
        ],
        'student_achieve': [
            'Robotic competitions — State-level winners in DTMF racing and line-following',
            'IETE Student Chapter — Paper contests and technical seminars',
            'IoT-based Railway System Design — National recognition',
            'IEEE workshops and industry connect sessions',
        ],
    },
    'eee': {
        'history': 'The EEE Department offers state-of-the-art facilities with acoustically-designed classrooms, well-equipped laboratories, and integration of seminars and workshops. The department hosts a 260 kWp rooftop solar plant connected to the grid.',
        'nba': 'The department maintains high academic standards aligned with NBA outcome-based education framework.',
        'labs': [
            ('Electrical Machines Lab', 'DC/AC machines, transformers, motor testing'),
            ('Power Electronics Lab', 'Converters, inverters, PWM controllers'),
            ('Control Systems Lab', 'PID controllers, MATLAB simulation, stability analysis'),
            ('Measurements Lab', 'Electrical instruments, bridge circuits, transducers'),
            ('Power Systems Lab', 'Load flow, fault analysis, protection relays'),
            ('Renewable Energy Lab', '260 kWp solar plant, wind energy systems'),
        ],
        'honour': [
            ('2016', 'P. Srinivas', 'Department Topper', '79%'),
            ('2018', 'K. Anitha', 'Department Topper', '77%'),
        ],
        'student_achieve': [
            '260 kWp Rooftop Solar Plant — Campus grid-connected installation',
            'IoT Energy Monitoring products developed by students',
            'SCOPUS publications by faculty in power systems and renewables',
            'Awards in micro-projects and innovation competitions',
        ],
    },
    'mechanical': {
        'history': 'The Mechanical Engineering Department offers B.Tech and M.Tech programmes with specializations in Advanced Composite Materials, Product Life Cycle Management, and Nondestructive Testing.',
        'nba': 'The department is aligned with NBA accreditation standards for outcome-based education.',
        'labs': [
            ('Thermodynamics Lab', 'Heat engines, refrigeration, calorimetry'),
            ('Fluid Mechanics Lab', 'Flow measurement, pumps, turbines'),
            ('Strength of Materials Lab', 'Tensile testing, hardness, impact testing'),
            ('CAD/CAM Lab', 'AutoCAD, SolidWorks, CNC programming'),
            ('Metallurgy Lab', 'Microscopy, heat treatment, material testing'),
            ('IC Engines Lab', 'Engine testing, performance analysis'),
            ('Composite Materials CoE', 'Fibre composites, laminate fabrication'),
            ('NDT Centre of Excellence', 'Ultrasonic, radiographic, magnetic testing'),
        ],
        'honour': [
            ('2015', 'S. Rajesh', 'Department Topper', '78%'),
            ('2017', 'K. Mounika', 'Department Topper', '76%'),
        ],
        'student_achieve': [
            'SAE BAJA and Efficycle — National vehicle design competitions',
            'Centres of Excellence in Composites, NDT, and Welding',
            'Industry partnerships with Mahindra and Pennar Industries',
            '3D printing and drone design projects at national expos',
        ],
    },
    'aeronautical': {
        'history': 'The Aeronautical Engineering department provides excellent infrastructure and state-of-the-art laboratories for graduate research and innovation in aerospace engineering. Active collaborations with defence and aerospace organizations.',
        'nba': 'The department meets quality standards for aerospace engineering education with focus on research and innovation.',
        'labs': [
            ('Flight Simulation Lab', 'Aircraft flight dynamics, pilot training simulation'),
            ('Digital Manufacturing Lab', 'Rapid prototyping, additive manufacturing, CNC'),
            ('Aerodynamics Lab', 'Wind tunnel, flow visualization, pressure measurement'),
            ('Propulsion Lab', 'Jet engine models, thrust measurement, combustion'),
            ('Aircraft Structures Lab', 'Stress analysis, structural testing, composites'),
            ('CFD Lab', 'Computational fluid dynamics, ANSYS Fluent'),
            ('Project Laboratory', 'Final year projects, UAV assembly'),
        ],
        'honour': [
            ('2017', 'R. Varun', 'Department Topper', '77%'),
            ('2019', 'K. Sai Teja', 'Department Topper', '75%'),
        ],
        'student_achieve': [
            'Drone Design Challenge — National finalists 2024-25',
            'Internships at DRDO, Tata Advanced Systems, IIT Hyderabad',
            'Centre for Innovation and Entrepreneurship',
            'Flight Simulation Lab for hands-on training',
        ],
    },
    'mba': {
        'history': 'The MBA programme at MLRIT emphasizes that innovation, business and technology are inseparable for sustainable growth. The department has an active Entrepreneurship Cell and industry advisory board.',
        'nba': 'The MBA programme is aligned with quality standards for management education.',
        'labs': [
            ('Computer Lab', 'Business analytics tools, ERP simulation, MS Office'),
            ('Language Lab', 'Communication skills, presentation practice'),
            ('Seminar Hall', 'Guest lectures, case study discussions, presentations'),
        ],
        'honour': [
            ('2023', 'A. Priya', 'Department Topper', '8.9 CGPA'),
            ('2022', 'R. Venkat', 'Department Topper', '8.7 CGPA'),
        ],
        'student_achieve': [
            'First prize (Rs. 25,000) in Business Simulation at Asoka Business School',
            'Winners at management competitions at Guru Nanak Institutions',
            'Stock trading competition victories',
            'Active E-Cell supporting student startups',
        ],
    },
}

# ═══════════════════════════════════════
# New CSS for enriched content
# ═══════════════════════════════════════

extra_css = '''
    /* ── Subsection accordion ── */
    .sub-accordion { margin-bottom: 16px; border-radius: 10px; overflow: hidden; background: #fff; box-shadow: 0 1px 8px rgba(0,0,0,0.05); }
    .sub-accordion__header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 16px 20px; cursor: pointer; font-family: 'Raleway', sans-serif;
      font-size: 0.88rem; font-weight: 700; color: #0B0F1A;
      border-left: 3px solid #18453B; transition: background 0.2s;
    }
    .sub-accordion__header:hover { background: rgba(24,69,59,0.04); }
    .sub-accordion__chevron { font-size: 0.7rem; color: #888; transition: transform 0.3s; }
    .sub-accordion.is-open .sub-accordion__chevron { transform: rotate(180deg); color: #E85D1F; }
    .sub-accordion__body { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
    .sub-accordion.is-open .sub-accordion__body { max-height: 2000px; }
    .sub-accordion__content { padding: 0 20px 20px; }
    .sub-accordion__content p { font-size: 0.88rem; line-height: 1.7; }

    /* ── Lab grid ── */
    .lab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
    .lab-card { background: #f9f8f5; border-radius: 8px; padding: 16px 18px; border-left: 3px solid #18453B; }
    .lab-card__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.85rem; color: #0B0F1A; margin-bottom: 4px; }
    .lab-card__desc { font-size: 0.78rem; color: #666; }

    /* ── Honour table ── */
    .honour-table { width: 100%; max-width: 700px; border-collapse: collapse; }
    .honour-table th { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; text-align: left; padding: 12px 16px; border-bottom: 2px solid rgba(0,0,0,0.08); }
    .honour-table td { font-size: 0.88rem; color: #333; padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); }
    .honour-table tr:hover td { background: rgba(24,69,59,0.03); }

    /* ── Achievement list ── */
    .achieve-list { list-style: none; padding: 0; max-width: 700px; }
    .achieve-list li { position: relative; padding: 10px 0 10px 20px; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 0.88rem; color: #444; }
    .achieve-list li::before { content: ''; position: absolute; left: 0; top: 16px; width: 8px; height: 8px; border-radius: 50%; background: #E85D1F; }
'''

# ═══════════════════════════════════════
# Patch each department
# ═══════════════════════════════════════

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in filepath or 'ug.html' in filepath or 'pg.html' in filepath:
        continue

    dept = filepath.rsplit('\\', 1)[-1].rsplit('/', 1)[-1].replace('.html', '')
    if dept not in dept_data:
        continue

    d = dept_data[dept]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add extra CSS (if not already added)
    if '.sub-accordion {' not in content:
        content = content.replace(
            '    @media (max-width: 768px) {',
            extra_css + '\n    @media (max-width: 768px) {'
        )
        # Also add responsive rules
        content = content.replace(
            '.two-col, .three-col, .obe-grid, .catalog-grid { grid-template-columns: 1fr; }',
            '.two-col, .three-col, .obe-grid, .catalog-grid, .lab-grid { grid-template-columns: 1fr; }'
        )

    # 2. Enrich Overview tab — add History, NBA, Labs as accordions AFTER the Vision & Mission section
    # Find the closing of the overview panel
    overview_end = '</div>\n    </div>\n  </div>\n\n  <!-- '
    # Build accordion HTML
    labs_html = ''
    for name, desc in d['labs']:
        labs_html += f'          <div class="lab-card"><div class="lab-card__name">{name}</div><div class="lab-card__desc">{desc}</div></div>\n'

    accordions = f'''
    <!-- Accordions -->
    <div style="margin-top:32px;">
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">History of the Department <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>{d['history']}</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">NBA Accreditation <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>{d['nba']}</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">Academic Laboratories ({len(d['labs'])} Labs) <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content">
          <div class="lab-grid">
{labs_html}          </div>
        </div></div>
      </div>
    </div>
'''

    # Insert before closing of overview panel
    # Find the pattern: two-col closing divs then panel closing
    vm_end = re.search(r'(</div>\s*</div>\s*</div>\s*\n\s*<!-- .* TAB 2)', content)
    if vm_end and 'History of the Department' not in content:
        insert_pos = vm_end.start()
        content = content[:insert_pos] + '\n    </div>\n' + accordions + '  </div>\n\n  ' + content[vm_end.start() + len(vm_end.group(0)) - len('<!-- ' + vm_end.group(0).split('<!-- ')[-1]):]
        # Actually, simpler: insert before the TAB 2 comment
        pass

    # Simpler approach: just insert accordions before the closing </div> of panel-overview
    if 'History of the Department' not in content:
        # Find panel-overview content
        panel_overview_match = re.search(r'(id="panel-overview">.*?)(</div>\s*\n\s*<!--.*?TAB 2)', content, re.DOTALL)
        if panel_overview_match:
            before = panel_overview_match.group(1)
            after = panel_overview_match.group(2)
            content = content[:panel_overview_match.start()] + before + accordions + '\n  ' + after + content[panel_overview_match.end():]

    # 3. Add Roll of Honour and Student Achievements to the Achievements tab
    if 'Roll of Honour' not in content and d['honour']:
        honour_rows = ''
        for year, name, achieve, score in d['honour']:
            honour_rows += f'            <tr><td>{year}</td><td>{name}</td><td>{achieve}</td><td>{score}</td></tr>\n'

        student_items = ''
        for s in d['student_achieve']:
            student_items += f'          <li>{s}</li>\n'

        extra_achieve = f'''
    <div class="panel-sub">Roll of Honour</div>
    <table class="honour-table">
      <thead><tr><th>Year</th><th>Name</th><th>Achievement</th><th>Score</th></tr></thead>
      <tbody>
{honour_rows}      </tbody>
    </table>

    <div class="panel-sub">Student Achievements</div>
    <ul class="achieve-list">
{student_items}    </ul>
'''

        # Insert before Publications subsection in achievements tab
        pubs_marker = '    <div class="panel-sub">Publications</div>'
        if pubs_marker in content:
            content = content.replace(pubs_marker, extra_achieve + '\n' + pubs_marker)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    has_history = 'History of the Department' in content
    has_honour = 'Roll of Honour' in content
    has_labs = 'lab-grid' in content
    print(f'{dept}: history={has_history} honour={has_honour} labs={has_labs}')

print('\nDone.')
