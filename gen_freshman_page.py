#!/usr/bin/env python3
import re

css = open('c:/mlr/cse_css.txt', encoding='utf-8').read()

faculty = []
for line in open('c:/mlr/freshman_faculty.txt', encoding='utf-8'):
    parts = line.strip().split('|')
    if len(parts) == 4:
        faculty.append(parts)

def ini(name):
    p = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Sri','').strip().split()
    return (p[0][0] + p[-1][0]).upper() if len(p) >= 2 else p[0][:2].upper()

fac = ''
for fn, nm, rl, sp in faculty:
    i = ini(nm)
    au = nm.replace('Dr. ','').replace('Mr. ','').replace('Mrs. ','').strip()
    fac += '          <div class="fcard" data-author="' + au + '">\n'
    fac += '            <div class="fcard__inner">\n'
    fac += '              <div class="fcard__front">\n'
    fac += '                <img src="images/freshman/' + fn + '" alt="' + nm + '" onerror="this.style.display=\'none\';this.parentElement.querySelector(\'.fcard__ini\').style.display=\'flex\'" />\n'
    fac += '                <div class="fcard__ini" style="display:none">' + i + '</div>\n'
    fac += '                <div class="fcard__overlay"><div class="fcard__name">' + nm + '</div><div class="fcard__role">' + rl + '</div></div>\n'
    fac += '              </div>\n'
    fac += '              <div class="fcard__back">\n'
    fac += '                <div class="fcard__back-name">' + nm + '</div>\n'
    fac += '                <div class="fcard__back-role">' + rl + '</div>\n'
    fac += '                <div class="fcard__back-spec">' + sp + '</div>\n'
    fac += '                <a href="faculty-profile.html?name=' + nm.replace(' ','%20') + '&role=' + rl.replace(' ','%20').replace(',','%2C') + '&photo=images/freshman/' + fn + '" class="fcard__back-btn">View Profile</a>\n'
    fac += '              </div>\n'
    fac += '            </div>\n'
    fac += '          </div>\n'

page = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Freshman Engineering — MLRIT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/navbar.css" />
  <link rel="stylesheet" href="../css/main.css" />
  ''' + css + '''
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
    <a href="ug.html" class="dept-nav__link dept-nav__link--active">Undergraduate</a>
    <a href="pg.html" class="dept-nav__link">Postgraduate</a>
    <span class="dept-nav__sep"></span>
    <span class="dept-nav__link dept-nav__link--dept">Freshman Engineering</span>
  </nav>

  <div class="dept-hero">
    <div class="dept-hero__eyebrow">First Year — All Branches</div>
    <div class="dept-hero__title">Freshman Engineering Department</div>
  </div>

  <nav class="dept-tabs" id="deptTabs">
    <a class="dept-tab is-active" data-tab="overview">Overview</a>
    <a class="dept-tab" data-tab="objectives">Objectives</a>
    <a class="dept-tab" data-tab="faculty">Faculty Profiles</a>
    <a class="dept-tab" data-tab="academics">Academics</a>
    <a class="dept-tab" data-tab="achievements">Achievements</a>
  </nav>

  <div class="qbar" id="qbar">
    <a class="qbar__btn is-active" data-qtab="overview"><span class="qbar__abbr">OV</span><span class="qbar__label">Overview</span></a>
    <a class="qbar__btn" data-qtab="objectives"><span class="qbar__abbr">OB</span><span class="qbar__label">Objectives</span></a>
    <a class="qbar__btn" data-qtab="faculty"><span class="qbar__abbr">FA</span><span class="qbar__label">Faculty</span></a>
    <a class="qbar__btn" data-qtab="academics"><span class="qbar__abbr">AC</span><span class="qbar__label">Academics</span></a>
    <a class="qbar__btn" data-qtab="achievements"><span class="qbar__abbr">AH</span><span class="qbar__label">Achievements</span></a>
  </div>

  <div class="dept-panel is-active" id="panel-overview">
    <h2 class="panel-heading">About the Department</h2>
    <div class="hod-msg">
      <div class="hod-msg__photo"><img src="images/freshman/achireddy.jpg" alt="Dr. Ch Achi Reddy" /></div>
      <div class="hod-msg__content">
        <div class="hod-msg__label">From the HOD's Desk</div>
        <p class="hod-msg__text">"The Freshman Engineering Department lays the foundation for every engineer at MLRIT. With 57 dedicated faculty across Physics, Chemistry, Mathematics, English, and Engineering Sciences, we ensure every first-year student builds a strong base in fundamentals. Our innovative practices including micro-projects, COTS, EPICS, and active learning methodologies prepare students for the rigour of their chosen specialisations."</p>
        <div class="hod-msg__name">Dr. Ch Achi Reddy, HOD</div>
      </div>
    </div>
    <p>The Freshman Engineering Department (FED) at MLRIT serves all first-year B.Tech students across all branches. The department covers foundational subjects in Mathematics, Physics, Chemistry, English Communication, and introductory Engineering courses. With 57 faculty members including 12 Professors, 6 Associate Professors, and 39 Assistant Professors, the department ensures a strong academic foundation.</p>
    <div class="panel-sub">Vision and Mission</div>
    <div class="two-col">
      <div class="card card--accent"><h3>Vision</h3><p>To achieve excellence in teaching humanities and basic sciences while preparing students to tackle emerging global challenges and become expert professionals in their fields.</p></div>
      <div class="card card--accent"><h3>Mission</h3><p>Encourage practical application through experience, develop communication across disciplines, excel in knowledge and human resource development, provide soft skills and behavioural training, and create an environment inspiring creativity and innovation.</p></div>
    </div>
    <div class="panel-sub">Innovative Teaching Methodology</div>
    <p>First-Year Micro Projects, Concept Oriented Tutorials (COTS), Engineering Projects in Community Service (EPICS), Student Platform for Engineering Education Development (SPEED), active learning methodologies, and seminars on communication skills.</p>
    <div style="margin-top:32px;">
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">Academic Laboratories (10 Labs) <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><div class="lab-grid">
          <div class="lab-card"><div class="lab-card__name">Advanced Engineering Physics Lab</div><div class="lab-card__desc">Optics, mechanics, modern physics</div></div>
          <div class="lab-card"><div class="lab-card__name">Computer Aided Engineering Drawing Lab</div><div class="lab-card__desc">AutoCAD, projections, technical drawing</div></div>
          <div class="lab-card"><div class="lab-card__name">Engineering Chemistry Lab</div><div class="lab-card__desc">Water analysis, electrochemistry, polymers</div></div>
          <div class="lab-card"><div class="lab-card__name">Programming for Problem Solving Lab</div><div class="lab-card__desc">C programming, algorithms</div></div>
          <div class="lab-card"><div class="lab-card__name">Basic Electrical Engineering Lab</div><div class="lab-card__desc">DC/AC circuits, transformers</div></div>
          <div class="lab-card"><div class="lab-card__name">English Communication Skills Lab</div><div class="lab-card__desc">LSRW, presentations, soft skills</div></div>
          <div class="lab-card"><div class="lab-card__name">Engineering Workshop</div><div class="lab-card__desc">Fitting, carpentry, welding, sheet metal</div></div>
          <div class="lab-card"><div class="lab-card__name">Python Programming Lab</div><div class="lab-card__desc">Python basics, data structures</div></div>
          <div class="lab-card"><div class="lab-card__name">Data Structures Lab</div><div class="lab-card__desc">Arrays, linked lists, trees</div></div>
          <div class="lab-card"><div class="lab-card__name">IOT and IT Workshop</div><div class="lab-card__desc">Arduino, sensors, IoT basics</div></div>
        </div></div></div>
      </div>
    </div>
  </div>

  <div class="dept-panel" id="panel-objectives">
    <h2 class="panel-heading">Programme Educational Objectives</h2>
    <div class="three-col">
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 1</div><p>Build strong fundamentals in mathematics, science, and engineering for core disciplines.</p></div>
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 2</div><p>Develop communication, analytical thinking, and problem-solving skills.</p></div>
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 3</div><p>Instil values of teamwork, ethics, creativity, and lifelong learning.</p></div>
    </div>
    <div class="panel-sub">Programme Outcomes (POs)</div>
    <div class="obe-list-numbered" style="max-width:780px;">
      <p><strong>PO1:</strong> Apply knowledge of mathematics, science, and engineering fundamentals.</p>
      <p><strong>PO2:</strong> Identify, formulate, and analyze complex engineering problems.</p>
      <p><strong>PO3:</strong> Design solutions considering health, safety, and environmental factors.</p>
      <p><strong>PO4:</strong> Conduct investigations using research methods and data analysis.</p>
      <p><strong>PO5:</strong> Apply appropriate techniques, resources, and modern tools.</p>
      <p><strong>PO6:</strong> Assess societal, health, safety implications of engineering practice.</p>
      <p><strong>PO7:</strong> Understand impact of engineering solutions on society and environment.</p>
      <p><strong>PO8:</strong> Apply ethical principles and professional norms.</p>
      <p><strong>PO9:</strong> Function effectively in diverse teams.</p>
      <p><strong>PO10:</strong> Communicate complex activities effectively.</p>
      <p><strong>PO11:</strong> Apply engineering and management principles.</p>
      <p><strong>PO12:</strong> Pursue continuous, independent learning.</p>
    </div>
    <div class="panel-sub">OBE Portal</div>
    <div class="card" style="max-width:500px;"><h3>OBE Assessment System</h3><p>CO/PO attainment data and assessment tools.</p><a href="http://103.15.62.235/ioncudos_mlrit_tier1/" target="_blank" style="font-family:Raleway;font-size:0.78rem;font-weight:700;color:#E85D1F;text-decoration:none;">Open OBE Portal &rarr;</a></div>
  </div>

  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>57 faculty across Physics, Chemistry, Mathematics, English, and Engineering Sciences.</p>
    <div class="fcard-grid">
''' + fac + '''    </div>
  </div>

  <div class="dept-panel" id="panel-academics">
    <h2 class="panel-heading">Academics</h2>
    <div class="panel-sub">Syllabus PDFs</div>
    <div class="catalog-grid" style="grid-template-columns:1fr;">
      <div class="catalog-item" style="justify-content:space-between;">
        <div><span class="catalog-item__text">R25 First Year Syllabus (All Branches)</span><span class="catalog-item__sub">Place PDF at: departments/syllabus/freshman/r25.pdf</span></div>
        <div class="syll-actions">
          <a href="syllabus/freshman/r25.pdf" target="_blank" class="syll-btn syll-btn--view">View</a>
          <a href="syllabus/freshman/r25.pdf" download class="syll-btn syll-btn--download">Download</a>
        </div>
      </div>
    </div>
    <div class="panel-sub">Semester 1 Subjects</div>
    <div style="max-width:700px;">
      <div class="subject-row"><span class="subject-code">A7BS01</span><span class="subject-name">Matrices and Calculus</span></div>
      <div class="subject-row"><span class="subject-code">A7PH01</span><span class="subject-name">Advanced Engineering Physics</span></div>
      <div class="subject-row"><span class="subject-code">A7CS01</span><span class="subject-name">Programming for Problem Solving</span></div>
      <div class="subject-row"><span class="subject-code">A7EE01</span><span class="subject-name">Basic Electrical Engineering</span></div>
      <div class="subject-row"><span class="subject-code">A7ME01</span><span class="subject-name">Computer Aided Engineering Drawing</span></div>
      <div class="subject-row"><span class="subject-code">A7PH01L</span><span class="subject-name">Advanced Engineering Physics Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7CS01L</span><span class="subject-name">Programming for Problem Solving Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7EE01L</span><span class="subject-name">Basic Electrical Engineering Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7CS02L</span><span class="subject-name">IOT and IT Workshop</span></div>
    </div>
    <div class="panel-sub">Semester 2 Subjects</div>
    <div style="max-width:700px;">
      <div class="subject-row"><span class="subject-code">A7BS02</span><span class="subject-name">ODE and Vector Calculus</span></div>
      <div class="subject-row"><span class="subject-code">A7CH01</span><span class="subject-name">Engineering Chemistry</span></div>
      <div class="subject-row"><span class="subject-code">A7CS02</span><span class="subject-name">Data Structures</span></div>
      <div class="subject-row"><span class="subject-code">A7EC01</span><span class="subject-name">Electronic Devices and Applications</span></div>
      <div class="subject-row"><span class="subject-code">A7EN01</span><span class="subject-name">English for Skill Enhancement</span></div>
      <div class="subject-row"><span class="subject-code">A7CH01L</span><span class="subject-name">Engineering Chemistry Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7CS02L</span><span class="subject-name">Data Structures Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7EN01L</span><span class="subject-name">English Communication Skills Lab</span></div>
      <div class="subject-row"><span class="subject-code">A7ME02L</span><span class="subject-name">Engineering Workshop</span></div>
      <div class="subject-row"><span class="subject-code">A7CS03L</span><span class="subject-name">Python Programming Lab</span></div>
    </div>
  </div>

  <div class="dept-panel" id="panel-achievements">
    <h2 class="panel-heading">Achievements</h2>
    <div class="achieve-grid">
      <div class="card achieve-card" data-achieve><h4>First-Year Micro Projects</h4><p>All first-year students undertake micro projects integrating concepts from multiple subjects, developing early research and teamwork skills.</p><span class="achieve-toggle">Read More</span></div>
      <div class="card achieve-card" data-achieve><h4>EPICS — Engineering Projects in Community Service</h4><p>Students work on community-oriented engineering projects addressing real-world problems in healthcare, agriculture, and sanitation.</p><span class="achieve-toggle">Read More</span></div>
      <div class="card achieve-card" data-achieve><h4>SPEED — Student Platform for Engineering Education Development</h4><p>Peer learning platform where senior students mentor freshmen in academics, coding, and soft skills development.</p><span class="achieve-toggle">Read More</span></div>
      <div class="card achieve-card" data-achieve><h4>Concept Oriented Tutorials (COTS)</h4><p>Weekly tutorials focusing on conceptual understanding with problem-solving sessions in small groups.</p><span class="achieve-toggle">Read More</span></div>
      <div class="card achieve-card" data-achieve><h4>Communication Skills Development</h4><p>Dedicated seminars and workshops on presentation skills, GD, technical writing, and interview preparation from day one.</p><span class="achieve-toggle">Read More</span></div>
    </div>
    <div class="panel-sub">Student Achievements</div>
    <ul class="achieve-list">
      <li>First-year students winning prizes in inter-college technical quiz competitions</li>
      <li>EPICS projects selected for state-level innovation exhibitions</li>
      <li>100+ students completing NPTEL certifications in first year</li>
      <li>Micro-project expo showcasing 200+ student projects annually</li>
      <li>Active participation in NSS, NCC, and sports from first semester</li>
    </ul>
  </div>

  <script>
    (function(){var tabs=document.querySelectorAll('.dept-tab');var panels=document.querySelectorAll('.dept-panel');var qbtns=document.querySelectorAll('.qbar__btn');function sw(id){tabs.forEach(function(t){t.classList.remove('is-active')});panels.forEach(function(p){p.classList.remove('is-active')});qbtns.forEach(function(q){q.classList.remove('is-active')});var tab=document.querySelector('[data-tab="'+id+'"]');var panel=document.getElementById('panel-'+id);var qbtn=document.querySelector('[data-qtab="'+id+'"]');if(tab)tab.classList.add('is-active');if(panel)panel.classList.add('is-active');if(qbtn)qbtn.classList.add('is-active')}tabs.forEach(function(t){t.addEventListener('click',function(){sw(t.getAttribute('data-tab'))})});qbtns.forEach(function(b){b.addEventListener('click',function(){sw(b.getAttribute('data-qtab'))})});var hash=window.location.hash.replace('#','');if(hash)sw(hash)})();
    (function(){document.querySelectorAll('[data-achieve]').forEach(function(card){var toggle=card.querySelector('.achieve-toggle');card.addEventListener('click',function(){var expanded=card.classList.toggle('is-expanded');if(toggle)toggle.textContent=expanded?'Read Less':'Read More'})})})();
    (function(){document.querySelectorAll('.fcard').forEach(function(item){item.addEventListener('click',function(){var backBtn=item.querySelector('.fcard__back-btn');if(backBtn){var n=item.querySelector('.fcard__back-name');var r=item.querySelector('.fcard__back-role');var img=item.querySelector('.fcard__front img');window.location.href='faculty-profile.html?name='+encodeURIComponent(n?n.textContent:'')+'&role='+encodeURIComponent(r?r.textContent:'')+'&photo='+encodeURIComponent(img?img.getAttribute('src'):'')}})})})();
  </script>

</body>
</html>'''

with open('c:/mlr/homepage/departments/freshman.html', 'w', encoding='utf-8') as f:
    f.write(page)

print('freshman.html created: ' + str(len(page)) + ' bytes, ' + str(len(faculty)) + ' faculty')
