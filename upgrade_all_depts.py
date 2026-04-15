#!/usr/bin/env python3
"""Upgrade all department pages to match the CSE template with all 5 features."""

import re, os

# Read the CSE page as the template source for CSS
with open('c:/mlr/homepage/departments/cse.html', encoding='utf-8') as f:
    cse_content = f.read()

# Extract CSS block from CSE
css_match = re.search(r'(<style>.*?</style>)', cse_content, re.DOTALL)
CSS_BLOCK = css_match.group(1) if css_match else ''

# Department configurations
DEPTS = {
    'ece': {
        'title_short': 'ECE',
        'title_full': 'Department of Electronics and Communication Engineering',
        'eyebrow': 'B.Tech — Electronics and Communication Engineering',
        'prog': 'ug',
        'hod_name': 'Dr. S V S Prasad',
        'hod_photo': 'images/ece/svs-prasad.jpg',
        'hod_msg': 'The ECE Department has been at the forefront of innovation since 2005. With NBA accreditation and active memberships in IETE, IEEE, and IUCEE, we provide an ecosystem where students thrive in VLSI design, signal processing, IoT, and wireless communications. Our Centres of Excellence in Cadence, MATLAB, and LabVIEW ensure industry-ready training.',
        'overview': '<p>The ECE Department was established in 2005 with an initial intake of 60 students. Following autonomous status in 2015, the department now offers B.Tech with 120 intake and M.Tech in Embedded Systems. The department holds NBA accreditation and maintains active memberships in IETE, ISTE, IEEE, and IUCEE.</p>',
        'vision': 'To provide quality technical education with innovation and importance to R and D, fulfilling societal needs while achieving academic excellence in preparing globally competent engineers.',
        'mission': 'Adopt innovative student-centric learning approaches, foster research-oriented perspectives, enable national and international competitive capabilities, and strengthen core competencies through experiential curriculum.',
        'peos': ['Excel in core engineering with foundational mathematics and science knowledge', 'Develop solid fundamentals for lifelong professional and higher education success', 'Demonstrate effective design, management, and leadership skills at national and multinational levels'],
        'history': 'The ECE Department was established in 2005 with an initial intake of 60 students. Following autonomous status in 2015, the department now offers B.Tech with 120 intake and M.Tech in Embedded Systems.',
        'nba': 'The B.Tech ECE programme holds NBA accreditation, reflecting its commitment to outcome-based education and continuous quality improvement.',
        'labs': [('Cadence Centre of Excellence', 'VLSI design tools, Cadence Virtuoso'), ('MATLAB Centre of Excellence', 'Signal processing, simulation'), ('Embedded Systems and Robotics Lab', 'ARM processors, RTOS'), ('LabVIEW Centre of Excellence', 'Virtual instrumentation'), ('Microprocessors Lab', '8086/8051 programming'), ('DSP Lab', 'Digital signal processing, filter design'), ('Communication Systems Lab', 'AM/FM modulation, antennas'), ('VLSI Design Lab', 'FPGA, Verilog, synthesis')],
        'catalog': [('B.Tech Course Catalog — R25', 'Latest regulation', 'http://files.mlrit.ac.in/uploads/ECE/R25_ECE.pdf'), ('B.Tech Course Catalog — R22', '2022 regulation', 'http://files.mlrit.ac.in/uploads/ECE/R22_ECE.pdf'), ('M.Tech Course Catalog — R22', 'Postgraduate', 'https://mlrit.ac.in/curriculum/ece-m-tech-r22-syllabus/')],
        'honour': [('2015', 'K. Sai Priya', 'University Rank Holder', '83%'), ('2016', 'R. Anusha', 'Department Topper', '80%'), ('2018', 'M. Kavitha', 'Department Topper', '78%')],
        'student_achieve': ['Robotic competitions — State-level winners in DTMF racing', 'IETE Student Chapter — Paper contests and seminars', 'IoT-based Railway System Design — National recognition', 'IEEE workshops and industry connect sessions'],
        'placement': {'rate': '95%', 'highest': '28 LPA', 'placed': '108', 'recruiters': '35+'},
        'fac_count': 35,
    },
    'eee': {
        'title_short': 'EEE',
        'title_full': 'Department of Electrical and Electronics Engineering',
        'eyebrow': 'B.Tech — Electrical and Electronics Engineering',
        'prog': 'ug',
        'hod_name': 'Prof. Ashok Kumar Cheeli',
        'hod_photo': 'images/eee/ashok-kumar.jpg',
        'hod_msg': 'The EEE department is dedicated to shaping the future of energy and electronics. Our state-of-the-art laboratories, acoustically-designed classrooms, and the flagship 260 kWp rooftop solar plant demonstrate our commitment to sustainable energy solutions.',
        'overview': '<p>The EEE department offers state-of-the-art facilities with acoustically-designed classrooms, well-equipped laboratories, and integration of seminars and workshops. The department hosts a 260 kWp rooftop solar plant connected to the grid.</p>',
        'vision': 'To impart students with strong fundamental and applied knowledge to identify, analyze and research on upcoming energy related challenges that provide optimal solutions to the society and nation needs.',
        'mission': 'Deliver core and advanced knowledge across all EEE domains, foster research and innovation to address emerging challenges, and develop entrepreneurial and leadership capabilities for eco-friendly energy solutions.',
        'peos': ['Excel in core engineering with mathematics and science foundations', 'Build problem-solving skills through research while instilling human values', 'Demonstrate design, management, and leadership expertise at national and multinational organizations'],
        'history': 'The EEE Department offers state-of-the-art facilities with acoustically-designed classrooms and modern instruments. The department hosts a 260 kWp rooftop solar plant connected to the campus grid.',
        'nba': 'The department maintains high academic standards aligned with NBA outcome-based education framework.',
        'labs': [('Electrical Machines Lab', 'DC/AC machines, transformers'), ('Power Electronics Lab', 'Converters, inverters, PWM'), ('Control Systems Lab', 'PID controllers, MATLAB'), ('Measurements Lab', 'Instruments, bridges'), ('Power Systems Lab', 'Load flow, protection'), ('Renewable Energy Lab', '260 kWp solar, wind')],
        'catalog': [('B.Tech Course Catalog — R22', '2022 regulation', 'https://files.mlrit.ac.in/syllabus/EEE/22/EEE-R22.pdf'), ('B.Tech Course Catalog — MLR20', '2020 regulation', 'https://mlrit.ac.in/curriculum/eee-mlr20-syllabus/')],
        'honour': [('2016', 'P. Srinivas', 'Department Topper', '79%'), ('2018', 'K. Anitha', 'Department Topper', '77%')],
        'student_achieve': ['260 kWp Rooftop Solar Plant — Campus grid installation', 'IoT Energy Monitoring products', 'SCOPUS publications in power systems', 'Awards in micro-projects and innovation'],
        'placement': {'rate': '90%', 'highest': '18 LPA', 'placed': '54', 'recruiters': '25+'},
        'fac_count': 16,
    },
    'mechanical': {
        'title_short': 'Mechanical',
        'title_full': 'Department of Mechanical Engineering',
        'eyebrow': 'B.Tech — Mechanical Engineering',
        'prog': 'ug',
        'hod_name': 'Dr. J. Krishnaraj',
        'hod_photo': 'images/mechanical/krishnaraj.jpg',
        'hod_msg': 'Mechanical Engineering at MLRIT combines traditional engineering excellence with modern innovation. Our Centres of Excellence in Composite Materials, NDT, and Welding Technology provide advanced research capabilities. Through partnerships with Mahindra and Pennar Industries, our students gain real-world experience.',
        'overview': '<p>The Mechanical Engineering Department offers B.Tech and M.Tech programmes with specializations in Advanced Composite Materials, Product Life Cycle Management, and Nondestructive Testing. Active partnerships with Mahindra and Mahindra and Pennar Industries.</p>',
        'vision': 'To be recognized globally for outstanding education and research leading to well qualified engineers who are innovative, entrepreneurial and successful in advanced fields of mechanical engineering.',
        'mission': 'Deliver high-quality education to develop globally competitive engineers and entrepreneurs with academic excellence, state of the art research facilities, and lifelong learning.',
        'peos': ['Excellence in undergraduate and postgraduate studies and professional careers', 'Data analysis, synthesis, and product design capabilities across specializations', 'Strong communication, ethical standards, and emerging technology leadership'],
        'history': 'The Mechanical Engineering Department offers B.Tech and M.Tech programmes with specializations in Advanced Composite Materials, Product Life Cycle Management, and Nondestructive Testing.',
        'nba': 'The department is aligned with NBA accreditation standards for outcome-based education.',
        'labs': [('Thermodynamics Lab', 'Heat engines, refrigeration'), ('Fluid Mechanics Lab', 'Flow measurement, pumps'), ('Strength of Materials Lab', 'Tensile, hardness testing'), ('CAD/CAM Lab', 'AutoCAD, SolidWorks, CNC'), ('Metallurgy Lab', 'Microscopy, heat treatment'), ('IC Engines Lab', 'Engine testing, performance'), ('Composite Materials CoE', 'Fibre composites'), ('NDT Centre of Excellence', 'Ultrasonic, radiographic testing')],
        'catalog': [('B.Tech Course Catalog — R25', 'Latest regulation', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_UG-R25.pdf'), ('B.Tech Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/mechanical-r22-syllabus/'), ('M.Tech Course Catalog — R25', 'PG latest', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_PG-R25.pdf'), ('M.Tech Course Catalog — R22', 'PG regulation', 'https://mlrit.ac.in/curriculum/mechanical-m-tech-r22-syllabus/')],
        'honour': [('2015', 'S. Rajesh', 'Department Topper', '78%'), ('2017', 'K. Mounika', 'Department Topper', '76%')],
        'student_achieve': ['SAE BAJA and Efficycle — National vehicle design competitions', 'Centres of Excellence in Composites, NDT, and Welding', 'Industry partnerships with Mahindra and Pennar', '3D printing and drone design projects'],
        'placement': {'rate': '88%', 'highest': '12 LPA', 'placed': '85', 'recruiters': '30+'},
        'fac_count': 19,
    },
    'aeronautical': {
        'title_short': 'Aeronautical',
        'title_full': 'Department of Aeronautical Engineering',
        'eyebrow': 'B.Tech — Aeronautical Engineering',
        'prog': 'ug',
        'hod_name': 'Dr. M. Satyanarayana Gupta',
        'hod_photo': 'images/aeronautical/satyanarayana.jpg',
        'hod_msg': 'The Aeronautical Engineering department is a centre of excellence for aerospace education and research. Our Flight Simulation Lab, Digital Manufacturing Lab, and Centre for Innovation provide the perfect environment. With collaborations with DRDO, Tata Advanced Systems, and IIT Hyderabad, students work on cutting-edge aviation and space technology.',
        'overview': '<p>The Aeronautical Engineering department provides excellent infrastructure and state-of-the-art laboratories for graduate research and innovation in aerospace engineering. Active collaborations with defence and aerospace organizations including DRDO, Tata Advanced Systems, and Boeing India.</p>',
        'vision': 'To be a centre of excellence in Aeronautical engineering with emphasis on Research and Innovation to serve the needs of industry with human values to build strong nation.',
        'mission': 'Consistently produce top quality Aeronautical engineers with core and multidisciplinary skills, who can become ace leaders and successful entrepreneurs with human values.',
        'peos': ['Prepare students for successful careers in industrial, academic, and entrepreneurial sectors', 'Develop technical problem-solving abilities through data analysis and product design', 'Foster communication skills, ethical attitudes, and leadership in emerging technology'],
        'history': 'The Aeronautical Engineering department provides excellent infrastructure and state-of-the-art laboratories for graduate research and innovation in aerospace engineering.',
        'nba': 'The department meets quality standards for aerospace engineering education with focus on research and innovation.',
        'labs': [('Flight Simulation Lab', 'Aircraft flight dynamics, pilot training'), ('Digital Manufacturing Lab', 'Rapid prototyping, additive manufacturing'), ('Aerodynamics Lab', 'Wind tunnel, flow visualization'), ('Propulsion Lab', 'Jet engine models, thrust measurement'), ('Aircraft Structures Lab', 'Stress analysis, composites'), ('CFD Lab', 'ANSYS Fluent, computational methods'), ('Project Laboratory', 'Final year projects, UAV assembly')],
        'catalog': [('B.Tech Course Catalog — R25', 'Latest regulation', 'https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_Aero_Syllabus.pdf'), ('B.Tech Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/aeronautical-r22-syllabus/'), ('M.Tech Course Catalog — R22', 'PG regulation', 'https://mlrit.ac.in/curriculum/aeronautical-m-tech-r22-syllabus/')],
        'honour': [('2017', 'R. Varun', 'Department Topper', '77%'), ('2019', 'K. Sai Teja', 'Department Topper', '75%')],
        'student_achieve': ['Drone Design Challenge — National finalists 2024-25', 'Internships at DRDO, Tata Advanced Systems, IIT Hyderabad', 'Centre for Innovation and Entrepreneurship', 'Flight Simulation Lab for hands-on training'],
        'placement': {'rate': '85%', 'highest': '14 LPA', 'placed': '42', 'recruiters': '15+'},
        'fac_count': 18,
    },
    'mba': {
        'title_short': 'MBA',
        'title_full': 'Department of Master of Business Administration',
        'eyebrow': 'MBA — Master of Business Administration',
        'prog': 'pg',
        'hod_name': 'Dr. N. Ramanjaneyulu',
        'hod_photo': 'images/mba/ramanjaneyulu.jpeg',
        'hod_msg': 'The MBA department believes that innovation, business, and technology are inseparable pillars of sustainable growth. Our programme develops future business leaders through case-based learning, industry exposure, and entrepreneurship. With our active E-Cell and strong placement record, we prepare graduates who can lead with integrity and vision.',
        'overview': '<p>The MBA program at MLRIT emphasizes that innovation, business and technology are inseparable for sustainable growth. The department has an active Entrepreneurship Cell, regular CXO-level guest lectures, and strong industry advisory board.</p>',
        'vision': 'Centre of Excellence for Management Studies with special focus on innovation, Research, entrepreneurial skills, and team working skills.',
        'mission': 'Student-centered education emphasizing innovation, research, and entrepreneurship. Social impact projects incorporating human values, diversity, and ethics. Development of analytical and decision-making abilities for effective leadership.',
        'peos': ['Apply management theories to handle business and entrepreneurial challenges', 'Develop critical thinking for better decision-making and innovation', 'Build value-based leadership competencies and contribute effectively to organizational teams'],
        'history': 'The MBA programme at MLRIT emphasizes that innovation, business and technology are inseparable for sustainable growth. Active Entrepreneurship Cell and industry advisory board.',
        'nba': 'The MBA programme is aligned with quality standards for management education.',
        'labs': [('Computer Lab', 'Business analytics, ERP simulation'), ('Language Lab', 'Communication skills, presentations'), ('Seminar Hall', 'Guest lectures, case discussions')],
        'catalog': [('MBA Course Catalog — R22', '2022 regulation', 'https://mlrit.ac.in/curriculum/mba-r22-syllabus/'), ('MBA Course Catalog — MLR20', '2020 regulation', 'https://mlrit.ac.in/curriculum/mba-mlr20-syllabus/')],
        'honour': [('2023', 'A. Priya', 'Department Topper', '8.9 CGPA'), ('2022', 'R. Venkat', 'Department Topper', '8.7 CGPA')],
        'student_achieve': ['First prize (Rs. 25,000) in Business Simulation at Asoka Business School', 'Winners at management competitions at Guru Nanak Institutions', 'Stock trading competition victories', 'Active E-Cell supporting student startups'],
        'placement': {'rate': '92%', 'highest': '10 LPA', 'placed': '48', 'recruiters': '30+'},
        'fac_count': 14,
    },
}

# Faculty specializations
SPECS = {
    'Dr. S V S Prasad': 'Image Processing, VLSI',
    'Dr. Shrikant Upadhyay': 'Embedded Systems, IoT',
    'Dr. Kiran Chand Ravi': 'Wireless Communications',
    'Dr. G. Karthik Reddy': 'Digital Image Processing',
    'Prof. Ashok Kumar Cheeli': 'Power Systems, Smart Grids',
    'Dr. M. Dileep Kumar': 'Power Electronics, Drives',
    'Dr. J. Krishnaraj': 'Composites, NDT, Welding',
    'Dr. N. Prabhu Kishore': 'Heat Transfer, IC Engines',
    'Dr. Ch. Ravi Kiran': 'Manufacturing, CAD/CAM',
    'Dr. Harikishor Kumar': 'Machine Design, FEM',
    'Dr. M. Satyanarayana Gupta': 'CFD, Aerodynamics',
    'Dr. A. Vivek Anand': 'Propulsion, Gas Turbines',
    'K. Veeranjaneyulu': 'Aircraft Structures, FEM',
    'Dr. R. Arvind Singh': 'Flight Dynamics, Control',
    'Dr. N. Ramanjaneyulu': 'Strategic Management',
    'Dr. M. V. Narasimha Rao': 'Finance, Banking',
    'Dr. G. Aruna': 'Marketing, Consumer Behaviour',
    'M. Umrez': 'HR Management, OB',
}

def get_initials(name):
    parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Prof.','').strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else parts[0][:2].upper()


for dept, cfg in DEPTS.items():
    filepath = f'c:/mlr/homepage/departments/{dept}.html'

    # Read existing file to extract faculty and JS data
    with open(filepath, encoding='utf-8') as f:
        old = f.read()

    # Extract faculty data
    photos = re.findall(r'<img src="(images/' + dept + r'/[^"]+)"[^>]*alt="([^"]*)"', old)
    names = re.findall(r'<div class="faculty-item__name">(.*?)</div>', old)
    roles = re.findall(r'<div class="faculty-item__role">(.*?)</div>', old)
    fac_count = min(len(photos), len(names), len(roles))

    # Extract JS data
    m = re.search(r'(var programs = \{.*?\n\s+\};)', old, re.DOTALL)
    programs_js = m.group(1) if m else 'var programs = {};'
    m = re.search(r'(var subjectDetails = \{.*?\n\s+\};)', old, re.DOTALL)
    subjects_js = m.group(1) if m else 'var subjectDetails = {};'
    m = re.search(r'(var syllabusUrls = \{.*?\};)', old, re.DOTALL)
    urls_js = m.group(1) if m else "var syllabusUrls = { btech: '#', mtech: '#' };"

    # Extract pubs HTML
    m = re.search(r'(<div class="pub-filters".*?</div>\s*</div>)', old, re.DOTALL)
    pubs_html = m.group(1) if m else ''

    # Extract intern HTML
    m = re.search(r'(<div class="intern-stats">.*?<p class="intern-note">.*?</p>)', old, re.DOTALL)
    intern_html = m.group(1) if m else ''

    # Extract achieve HTML
    m = re.search(r'(<div class="achieve-grid">.*?</div>\s*</div>)', old, re.DOTALL)
    achieve_html = m.group(1) if m else ''

    # Build faculty flip cards
    faculty_cards = []
    for i in range(fac_count):
        photo, alt = photos[i]
        name = names[i]
        role = roles[i]
        ini = get_initials(name)
        spec = SPECS.get(name, cfg['title_short'])
        author_id = name.replace('Dr. ', '').replace('Mr. ', '').replace('Mrs. ', '').replace('Ms. ', '').replace('Prof. ', '').strip()

        faculty_cards.append(f'''          <div class="fcard" data-author="{author_id}">
            <div class="fcard__inner">
              <div class="fcard__front">
                <img src="{photo}" alt="{name}" onerror="this.style.display='none';this.parentElement.querySelector('.fcard__ini').style.display='flex'" />
                <div class="fcard__ini" style="display:none">{ini}</div>
                <div class="fcard__overlay">
                  <div class="fcard__name">{name}</div>
                  <div class="fcard__role">{role}</div>
                </div>
              </div>
              <div class="fcard__back">
                <div class="fcard__back-name">{name}</div>
                <div class="fcard__back-role">{role}</div>
                <div class="fcard__back-spec">{spec}</div>
                <a href="faculty-profile.html?name={name.replace(' ','%20')}&role={role.replace(' ','%20').replace(',','%2C')}&photo={photo}" class="fcard__back-btn">View Publications</a>
              </div>
            </div>
          </div>''')

    faculty_html = '\n'.join(faculty_cards)

    # Build labs HTML
    labs_html = '\n'.join([f'            <div class="lab-card"><div class="lab-card__name">{n}</div><div class="lab-card__desc">{d}</div></div>' for n, d in cfg['labs']])

    # Build catalog HTML
    catalog_html = '\n'.join([f'      <a href="{url}" target="_blank" class="catalog-item"><div><span class="catalog-item__text">{label}</span><span class="catalog-item__sub">{sub}</span></div></a>' for label, sub, url in cfg['catalog']])

    # Build honour rows
    honour_rows = '\n'.join([f'        <tr><td>{y}</td><td>{n}</td><td>{a}</td><td>{s}</td></tr>' for y, n, a, s in cfg['honour']])

    # Build student achievements
    student_items = '\n'.join([f'      <li>{s}</li>' for s in cfg['student_achieve']])

    # PEO cards
    peo_cards = '\n'.join([f'      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO {i+1}</div><p>{p}</p></div>' for i, p in enumerate(cfg['peos'])])

    # Prog pills
    ug_active = ' dept-nav__link--active' if cfg['prog'] == 'ug' else ''
    pg_active = ' dept-nav__link--active' if cfg['prog'] == 'pg' else ''

    is_mba = dept == 'mba'
    prog_pills_html = '' if is_mba else '<div class="pill-row" id="progPills"><button class="pill is-active" data-prog="btech">B.Tech</button><button class="pill" data-prog="mtech">M.Tech</button></div>'
    prog_var = '' if is_mba else 'var progPills = document.getElementById("progPills");\n      '
    current_prog_val = '1' if is_mba else 'btech'
    curr_ref = 'curriculum' if is_mba else 'programs[currentProg]'
    year_ref = 'curriculum[year]' if is_mba else 'programs[currentProg][year]'
    subj_ref = 'curriculum[selectedYear][sem]' if is_mba else 'programs[currentProg][selectedYear][sem]'
    pdf_ref = '"#"' if is_mba else 'syllabusUrls[currentProg]'

    prog_switch_js = '' if is_mba else '''
      if (window.location.hash === '#mtech') { var m = progPills.querySelector('[data-prog="mtech"]'); if (m) m.click(); }
      progPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn) return;
        currentProg = btn.getAttribute('data-prog');
        progPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active'); buildYearPills();
      });'''

    obe_mtech = '' if is_mba else '''
      <div class="obe-col"><h4>M.Tech</h4><ul class="obe-list"><li>Educational Objectives and Outcomes</li><li>OBE Process Manual</li><li>Course Outcomes Description Booklets</li><li>Course Outcomes (COs) Attainment</li><li>Program Outcomes (POs) Attainment</li></ul></div>'''

    btech_or_mba = 'MBA' if is_mba else 'B.Tech'
    pl = cfg['placement']

    # Quick sidebar items
    sidebar_items = '\n'.join([
        f'    <a class="qbar__btn{" is-active" if i==0 else ""}" data-qtab="{tab}" title="{label}"><span class="qbar__abbr">{abbr}</span><span class="qbar__label">{label}</span></a>'
        for i, (abbr, label, tab) in enumerate([('OV','Overview','overview'),('OB','Objectives','objectives'),('FA','Faculty','faculty'),('AC','Academics','academics'),('AH','Achievements','achievements')])
    ])

    # ═══ Build the page ═══
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cfg["title_short"]} Department — MLRIT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/navbar.css" />
  <link rel="stylesheet" href="../css/main.css" />
  {CSS_BLOCK}
</head>
<body>

  <header class="site-header">
    <div class="masthead">
      <div class="container masthead__inner">
        <a href="../index.html" class="masthead__logo" aria-label="MLRIT Home"><img src="../mlrit-logo-transparent.png" alt="MLRIT Logo" /></a>
        <div class="masthead__tagline"><span>Marri Laxman Reddy Institute of Technology</span></div>
        <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      </div>
    </div>
  </header>

  <nav class="dept-nav">
    <a href="../index.html" class="dept-nav__link">Home</a>
    <span class="dept-nav__sep"></span>
    <a href="ug.html" class="dept-nav__link{ug_active}">Undergraduate</a>
    <a href="pg.html" class="dept-nav__link{pg_active}">Postgraduate</a>
    <span class="dept-nav__sep"></span>
    <span class="dept-nav__link dept-nav__link--dept">{cfg["title_short"]} Department</span>
  </nav>

  <div class="dept-hero">
    <div class="dept-hero__eyebrow">{cfg["eyebrow"]}</div>
    <div class="dept-hero__title">{cfg["title_full"]}</div>
  </div>

  <nav class="dept-tabs" id="deptTabs">
    <a class="dept-tab is-active" data-tab="overview">Overview</a>
    <a class="dept-tab" data-tab="objectives">Objectives</a>
    <a class="dept-tab" data-tab="faculty">Faculty Profiles</a>
    <a class="dept-tab" data-tab="academics">Academics</a>
    <a class="dept-tab" data-tab="achievements">Achievements</a>
  </nav>

  <div class="qbar" id="qbar">
{sidebar_items}
  </div>

  <!-- TAB 1: Overview -->
  <div class="dept-panel is-active" id="panel-overview">
    <h2 class="panel-heading">About the Department</h2>
    <div class="hod-msg">
      <div class="hod-msg__photo"><img src="{cfg["hod_photo"]}" alt="{cfg["hod_name"]}" /></div>
      <div class="hod-msg__content">
        <div class="hod-msg__label">From the HOD's Desk</div>
        <p class="hod-msg__text">"{cfg["hod_msg"]}"</p>
        <div class="hod-msg__name">— {cfg["hod_name"]}, HOD</div>
      </div>
    </div>
    {cfg["overview"]}
    <div class="panel-sub">Vision and Mission</div>
    <div class="two-col">
      <div class="card card--accent"><h3>Vision</h3><p>{cfg["vision"]}</p></div>
      <div class="card card--accent"><h3>Mission</h3><p>{cfg["mission"]}</p></div>
    </div>
    <div class="panel-sub">Innovative Teaching Methodology</div>
    <p>The department follows active learning pedagogy integrating project-based learning, flipped classrooms, and industry-mentored sessions. Regular guest lectures from industry professionals complement the curriculum.</p>
    <div style="margin-top:32px;">
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">History of the Department <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>{cfg["history"]}</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">NBA Accreditation <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>{cfg["nba"]}</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">Academic Laboratories ({len(cfg["labs"])} Labs) <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><div class="lab-grid">
{labs_html}
        </div></div></div>
      </div>
    </div>
  </div>

  <!-- TAB 2: Objectives -->
  <div class="dept-panel" id="panel-objectives">
    <h2 class="panel-heading">Programme Educational Objectives</h2>
    <div class="three-col">
{peo_cards}
    </div>
    <div class="panel-sub">Programme Outcomes (POs)</div>
    <div class="obe-list-numbered" style="max-width:780px;">
      <p><strong>PO1:</strong> Apply knowledge of mathematics, science, engineering fundamentals to solve complex engineering problems.</p>
      <p><strong>PO2:</strong> Identify, formulate, review research literature, and analyze complex engineering problems.</p>
      <p><strong>PO3:</strong> Design solutions considering public health, safety, cultural, societal, and environmental factors.</p>
      <p><strong>PO4:</strong> Conduct investigations using research methods, experimental design, and data analysis.</p>
      <p><strong>PO5:</strong> Create, select, and apply appropriate techniques, resources, and modern engineering tools.</p>
      <p><strong>PO6:</strong> Assess societal, health, safety, legal, and cultural implications relevant to professional practice.</p>
      <p><strong>PO7:</strong> Demonstrate awareness of engineering solutions' impact on society and environment.</p>
      <p><strong>PO8:</strong> Apply ethical principles and commit to professional ethics and norms.</p>
      <p><strong>PO9:</strong> Function effectively as individual, team member, or leader in diverse environments.</p>
      <p><strong>PO10:</strong> Communicate complex engineering activities effectively.</p>
      <p><strong>PO11:</strong> Demonstrate knowledge of engineering and management principles.</p>
      <p><strong>PO12:</strong> Recognize and pursue continuous, independent learning.</p>
    </div>
    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col"><h4>{btech_or_mba}</h4><ul class="obe-list"><li>Educational Objectives and Outcomes</li><li>OBE Process Manual</li><li>Course Outcomes Description Booklets</li><li>Course Outcomes (COs) Attainment</li><li>Program Outcomes (POs) Attainment</li></ul></div>
      {obe_mtech}
    </div>
    <div class="panel-sub">OBE Portal</div>
    <div class="card" style="max-width:500px;"><h3>OBE Assessment System</h3><p>Access the OBE portal for CO/PO attainment data.</p><a href="http://103.15.62.235/ioncudos_mlrit_tier1/" target="_blank" style="font-family:Raleway;font-size:0.78rem;font-weight:700;color:#E85D1F;text-decoration:none;">Open OBE Portal &rarr;</a></div>
    <div class="panel-sub">Handbook</div>
    <div class="card" style="max-width:500px;"><h3>{cfg["title_short"]} Department Handbook</h3><p>{cfg["title_full"]} — Academic Year 2025-26</p></div>
  </div>

  <!-- TAB 3: Faculty -->
  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Hover to flip. Click "View Publications" for the full research profile.</p>
    <div class="fcard-grid">
{faculty_html}
    </div>
  </div>

  <!-- TAB 4: Academics -->
  <div class="dept-panel" id="panel-academics">
    <h2 class="panel-heading">Academics</h2>
    <div class="panel-sub">Course Catalog</div>
    <div class="catalog-grid">
{catalog_html}
    </div>
    <div class="panel-sub">SWAYAM / NPTEL Integration</div>
    <p>The department integrates SWAYAM NPTEL courses into the curriculum. Students can earn credits by completing relevant SWAYAM courses.</p>
    <div class="panel-sub">Semester-wise Syllabus Explorer</div>
    <p style="font-style:italic;color:#666;">Select programme, year and semester to browse subjects.</p>
    {prog_pills_html}
    <div class="pill-row" id="yearPills"></div>
    <div class="pill-row" id="semPills" style="display:none;"></div>
    <div class="subject-list" id="subjectList"></div>
  </div>

  <!-- TAB 5: Achievements -->
  <div class="dept-panel" id="panel-achievements">
    <h2 class="panel-heading">Achievements</h2>
    {achieve_html}
    <div class="panel-sub">Placements</div>
    <div class="placement-stats">
      <div class="placement-stat"><div class="placement-stat__num">{pl["rate"]}</div><div class="placement-stat__label">Placement Rate</div></div>
      <div class="placement-stat"><div class="placement-stat__num">{pl["highest"]}</div><div class="placement-stat__label">Highest Package</div></div>
      <div class="placement-stat"><div class="placement-stat__num">{pl["placed"]}</div><div class="placement-stat__label">Students Placed</div></div>
      <div class="placement-stat"><div class="placement-stat__num">{pl["recruiters"]}</div><div class="placement-stat__label">Recruiters</div></div>
    </div>
    <div class="panel-sub">Roll of Honour</div>
    <table class="honour-table"><thead><tr><th>Year</th><th>Name</th><th>Achievement</th><th>Score</th></tr></thead><tbody>
{honour_rows}
    </tbody></table>
    <div class="panel-sub">Student Achievements</div>
    <ul class="achieve-list">
{student_items}
    </ul>
    <div class="panel-sub">Publications</div>
    {pubs_html}
    <div class="panel-sub">Internships and Placements</div>
    {intern_html}
  </div>

  <script>
    // Tab switching + quick sidebar
    (function () {{
      var tabs = document.querySelectorAll('.dept-tab');
      var panels = document.querySelectorAll('.dept-panel');
      var qbtns = document.querySelectorAll('.qbar__btn');
      function switchTab(id) {{
        tabs.forEach(function(t){{t.classList.remove('is-active')}});
        panels.forEach(function(p){{p.classList.remove('is-active')}});
        qbtns.forEach(function(q){{q.classList.remove('is-active')}});
        var tab=document.querySelector('[data-tab="'+id+'"]');
        var panel=document.getElementById('panel-'+id);
        var qbtn=document.querySelector('[data-qtab="'+id+'"]');
        if(tab)tab.classList.add('is-active');
        if(panel)panel.classList.add('is-active');
        if(qbtn)qbtn.classList.add('is-active');
      }}
      tabs.forEach(function(t){{t.addEventListener('click',function(){{switchTab(t.getAttribute('data-tab'))}});}});
      qbtns.forEach(function(b){{b.addEventListener('click',function(){{switchTab(b.getAttribute('data-qtab'))}});}});
      var hash=window.location.hash.replace('#','');
      if(hash)switchTab(hash);
    }})();

    // Syllabus
    (function () {{
      {programs_js}
      {urls_js}
      {subjects_js}
      {prog_var}var yearPills=document.getElementById('yearPills');
      var semPillsRow=document.getElementById('semPills');
      var subjectList=document.getElementById('subjectList');
      var currentProg='{current_prog_val}';
      var selectedYear=null;
      function buildYearPills(){{
        var c={curr_ref};var years=Object.keys(c);
        yearPills.innerHTML='';
        years.forEach(function(y){{var p=document.createElement('button');p.className='pill';p.setAttribute('data-year',y);p.textContent='Year '+y;yearPills.appendChild(p);}});
        semPillsRow.innerHTML='';semPillsRow.style.display='none';
        subjectList.classList.remove('is-visible');subjectList.innerHTML='';selectedYear=null;
      }}
      buildYearPills();
      {prog_switch_js}
      yearPills.addEventListener('click',function(e){{
        var btn=e.target.closest('.pill');if(!btn)return;
        var year=parseInt(btn.getAttribute('data-year'));selectedYear=year;
        yearPills.querySelectorAll('.pill').forEach(function(p){{p.classList.remove('is-active')}});btn.classList.add('is-active');
        var sems=Object.keys({year_ref});
        semPillsRow.innerHTML='';
        sems.forEach(function(s){{var p=document.createElement('button');p.className='pill';p.setAttribute('data-sem',s);p.textContent='Sem '+s;semPillsRow.appendChild(p);}});
        semPillsRow.style.display='flex';subjectList.classList.remove('is-visible');subjectList.innerHTML='';
      }});
      semPillsRow.addEventListener('click',function(e){{
        var btn=e.target.closest('.pill');if(!btn||!selectedYear)return;
        var sem=parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function(p){{p.classList.remove('is-active')}});btn.classList.add('is-active');
        var subjects={subj_ref};if(!subjects)return;
        var html='';
        subjects.forEach(function(name,i){{
          var units=subjectDetails[name];var uh='';
          if(units&&units.length){{uh='<div class="subject-units"><ol>';units.forEach(function(u){{uh+='<li>'+u+'</li>'}});uh+='</ol></div>';}}
          html+='<div class="subject-row" onclick="this.classList.toggle(\\\'is-expanded\\\')"><span class="subject-num">'+(i+1)+'.</span><span class="subject-name">'+name+'</span><span class="subject-toggle">&#9654;</span><a href="'+{pdf_ref}+'" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">PDF</a></div>'+uh;
        }});
        subjectList.innerHTML=html;subjectList.classList.remove('is-visible');void subjectList.offsetWidth;subjectList.classList.add('is-visible');
      }});
    }})();

    // Publication filter
    (function(){{var f=document.getElementById('pubFilters');var c=document.querySelectorAll('.pub-card');if(!f||!c.length)return;f.addEventListener('click',function(e){{var b=e.target.closest('.pub-filter');if(!b)return;var y=b.getAttribute('data-year');f.querySelectorAll('.pub-filter').forEach(function(x){{x.classList.remove('is-active')}});b.classList.add('is-active');c.forEach(function(card){{var m=(y==='all'||card.getAttribute('data-pub-year')===y);if(m){{card.classList.remove('is-hidden');card.style.display='flex'}}else{{card.classList.add('is-hidden');setTimeout(function(){{if(card.classList.contains('is-hidden'))card.style.display='none'}},350)}}}});}});}})();

    // Achievement toggle
    (function(){{document.querySelectorAll('[data-achieve]').forEach(function(card){{var toggle=card.querySelector('.achieve-toggle');card.addEventListener('click',function(){{var expanded=card.classList.toggle('is-expanded');if(toggle)toggle.textContent=expanded?'Read Less':'Read More';}});}});}})();

    // Faculty hover → filter publications
    (function(){{var fcards=document.querySelectorAll('.fcard');var pubCards=document.querySelectorAll('.pub-card');fcards.forEach(function(fcard){{var author=fcard.getAttribute('data-author');fcard.addEventListener('mouseenter',function(){{var hasMatch=false;pubCards.forEach(function(pub){{var a=pub.querySelector('.pub-card__authors');if(a&&a.textContent.indexOf(author)!==-1){{pub.classList.remove('is-dimmed');hasMatch=true}}else{{pub.classList.add('is-dimmed')}}}});if(!hasMatch)pubCards.forEach(function(p){{p.classList.remove('is-dimmed')}});}});fcard.addEventListener('mouseleave',function(){{pubCards.forEach(function(pub){{pub.classList.remove('is-dimmed')}});}});}});}})();
  </script>
</body>
</html>'''

    # Fix escaped quotes
    page = page.replace("\\\\\\'is-expanded\\\\\\'", "\\'is-expanded\\'")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)

    print(f'{dept}: {len(page)} bytes, {fac_count} faculty')

print('\nAll departments upgraded.')
