import re, glob

# HOD data per department
hod_data = {
    'cse': {
        'name': 'Dr. Ajmeera Kiran',
        'photo': 'images/cse/ajmeera-kiran.jpg',
        'msg': 'Welcome to the Department of Computer Science and Engineering at MLRIT. Our department is committed to providing a world-class education that blends strong theoretical foundations with hands-on experience in cutting-edge technologies. With 64 dedicated faculty members, 12 advanced laboratories, and industry partnerships with Boeing, Cyient, and EPAM Systems, we prepare our students to excel in the ever-evolving technology landscape. I encourage every student to leverage our research facilities, participate in hackathons, and build innovative solutions that make a difference.',
    },
    'ece': {
        'name': 'Dr. S V S Prasad',
        'photo': 'images/ece/svs-prasad.jpg',
        'msg': 'The Department of Electronics and Communication Engineering at MLRIT has been at the forefront of innovation since 2005. With NBA accreditation and active memberships in IETE, IEEE, and IUCEE, we provide an ecosystem where students thrive in VLSI design, signal processing, IoT, and wireless communications. Our Centres of Excellence in Cadence, MATLAB, and LabVIEW ensure industry-ready training. I invite all students to embrace the spirit of curiosity and contribute to the advancement of communication technologies.',
    },
    'eee': {
        'name': 'Prof. Ashok Kumar Cheeli',
        'photo': 'images/eee/ashok-kumar.jpg',
        'msg': 'The EEE department is dedicated to shaping the future of energy and electronics. Our state-of-the-art laboratories, acoustically-designed classrooms, and the flagship 260 kWp rooftop solar plant demonstrate our commitment to sustainable energy solutions. We focus on power systems, smart grids, renewable energy, and electric drives — preparing engineers who will lead the green energy revolution.',
    },
    'mechanical': {
        'name': 'Dr. J. Krishnaraj',
        'photo': 'images/mechanical/krishnaraj.jpg',
        'msg': 'Mechanical Engineering at MLRIT combines traditional engineering excellence with modern innovation. Our Centres of Excellence in Composite Materials, NDT, and Welding Technology provide students with advanced research capabilities. Through partnerships with Mahindra and Pennar Industries, and active participation in SAE competitions, our students gain real-world experience that sets them apart in the industry.',
    },
    'aeronautical': {
        'name': 'Dr. M. Satyanarayana Gupta',
        'photo': 'images/aeronautical/satyanarayana.jpg',
        'msg': 'The Aeronautical Engineering department at MLRIT is a centre of excellence for aerospace education and research. Our Flight Simulation Lab, Digital Manufacturing Lab, and Centre for Innovation provide the perfect environment for aspiring aerospace engineers. With collaborations with DRDO, Tata Advanced Systems, and IIT Hyderabad, our students work on projects at the cutting edge of aviation and space technology.',
    },
    'mba': {
        'name': 'Dr. N. Ramanjaneyulu',
        'photo': 'images/mba/ramanjaneyulu.jpeg',
        'msg': 'The MBA department at MLRIT believes that innovation, business, and technology are inseparable pillars of sustainable growth. Our programme develops future business leaders through case-based learning, industry exposure, and entrepreneurship. With our active E-Cell, guest lectures from CXO-level professionals, and strong placement record, we prepare graduates who can lead organisations with integrity and vision.',
    },
}

# CSS to add for HOD section and interactive cards
new_css = '''
    /* ── HOD Message ── */
    .hod-msg {
      display: flex;
      gap: 28px;
      align-items: flex-start;
      background: #fff;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.06);
      margin-bottom: 36px;
      border-left: 4px solid #18453B;
    }
    .hod-msg__photo {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      overflow: hidden;
      flex-shrink: 0;
      border: 3px solid #18453B;
    }
    .hod-msg__photo img { width: 100%; height: 100%; object-fit: cover; }
    .hod-msg__content { flex: 1; }
    .hod-msg__label {
      font-family: 'Raleway', sans-serif;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: #E85D1F;
      margin-bottom: 8px;
    }
    .hod-msg__text {
      font-size: 0.92rem;
      color: #444;
      line-height: 1.8;
      font-style: italic;
      max-width: none;
    }
    .hod-msg__name {
      font-family: 'Raleway', sans-serif;
      font-size: 0.82rem;
      font-weight: 700;
      color: #18453B;
      margin-top: 12px;
    }

    /* ── Interactive cards ── */
    .card--interactive {
      cursor: pointer;
      transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
      border-left: 4px solid transparent;
    }
    .card--interactive:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 28px rgba(0,0,0,0.1);
      border-left-color: #E85D1F;
    }
    .card--interactive .card-expand {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.4s ease;
      margin-top: 0;
    }
    .card--interactive.is-open .card-expand {
      max-height: 500px;
      margin-top: 12px;
    }
    .card--interactive .card-toggle {
      font-family: 'Raleway', sans-serif;
      font-size: 0.68rem;
      font-weight: 700;
      color: #E85D1F;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      display: inline-block;
      margin-top: 8px;
    }
    .card--interactive .card-toggle::after {
      content: ' +';
    }
    .card--interactive.is-open .card-toggle::after {
      content: ' −';
    }

    @media (max-width: 768px) {
      .hod-msg { flex-direction: column; align-items: center; text-align: center; }
    }'''

for filepath in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in filepath or 'ug.html' in filepath or 'pg.html' in filepath:
        continue

    dept = filepath.rsplit('\\', 1)[-1].rsplit('/', 1)[-1].replace('.html', '')
    if dept not in hod_data:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    hod = hod_data[dept]

    # 1. Add new CSS before the responsive media query
    if '.hod-msg {' not in content:
        content = content.replace(
            '    @media (max-width: 768px) {',
            new_css + '\n    @media (max-width: 768px) {'
        )

    # 2. Add HOD message to Overview tab (after the heading, before the overview text)
    hod_html = f'''
    <!-- HOD's Message -->
    <div class="hod-msg">
      <div class="hod-msg__photo">
        <img src="{hod['photo']}" alt="{hod['name']}" />
      </div>
      <div class="hod-msg__content">
        <div class="hod-msg__label">From the HOD's Desk</div>
        <p class="hod-msg__text">"{hod['msg']}"</p>
        <div class="hod-msg__name">— {hod['name']}, HOD</div>
      </div>
    </div>

'''

    # Insert after panel-heading in overview
    old_overview_start = '    <h2 class="panel-heading">About the Department</h2>\n'
    if 'hod-msg' not in content:
        content = content.replace(
            old_overview_start,
            old_overview_start + hod_html
        )

    # 3. Make Vision & Mission cards interactive
    content = content.replace(
        '<div class="card card--accent">\n        <h3>Vision</h3>',
        '<div class="card card--accent card--interactive" onclick="this.classList.toggle(\'is-open\')">\n        <h3>Vision</h3>'
    )
    content = content.replace(
        '<div class="card card--accent">\n        <h3>Mission</h3>',
        '<div class="card card--accent card--interactive" onclick="this.classList.toggle(\'is-open\')">\n        <h3>Mission</h3>'
    )

    # Wrap vision/mission content in expandable div
    # Vision
    vision_match = re.search(r'(<h3>Vision</h3>\s*)<p>(.*?)</p>', content, re.DOTALL)
    if vision_match and 'card-expand' not in content[:vision_match.end() + 100]:
        old = vision_match.group(0)
        text = vision_match.group(2)
        preview = text[:80] + '...' if len(text) > 80 else text
        new = f'<h3>Vision</h3>\n        <p>{preview}</p>\n        <div class="card-expand"><p>{text}</p></div>\n        <span class="card-toggle">Details</span>'
        content = content.replace(old, new, 1)

    # Mission
    mission_match = re.search(r'(<h3>Mission</h3>\s*)<p>(.*?)</p>', content, re.DOTALL)
    if mission_match and 'card-expand' not in content[mission_match.start():mission_match.end() + 100]:
        old = mission_match.group(0)
        text = mission_match.group(2)
        preview = text[:80] + '...' if len(text) > 80 else text
        new = f'<h3>Mission</h3>\n        <p>{preview}</p>\n        <div class="card-expand"><p>{text}</p></div>\n        <span class="card-toggle">Details</span>'
        content = content.replace(old, new, 1)

    # 4. Make PEO cards interactive
    content = content.replace(
        '<div class="card card--accent" style="text-align:center;">',
        '<div class="card card--accent card--interactive" style="text-align:center;" onclick="this.classList.toggle(\'is-open\')">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    has_hod = 'hod-msg' in content
    has_interactive = 'card--interactive' in content
    print(f'{dept}: hod={has_hod} interactive={has_interactive}')

print('\nDone.')
