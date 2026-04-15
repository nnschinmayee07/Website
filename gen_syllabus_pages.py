#!/usr/bin/env python3
"""Generate local syllabus HTML files for each regulation."""

base = 'c:/mlr/homepage/departments'

regs = {
    'R25': ('r25', {
        'Year 1 Semester 1': [('A7BS01','Matrices and Calculus'),('A7PH01','Advanced Engineering Physics'),('A7CS01','Programming for Problem Solving'),('A7EE01','Basic Electrical Engineering'),('A7ME01','Computer Aided Engineering Drawing'),('A7PH01L','Adv. Engg. Physics Lab'),('A7CS01L','Programming Lab'),('A7EE01L','Basic Electrical Lab'),('A7CS02L','IOT and IT Workshop')],
        'Year 1 Semester 2': [('A7BS02','ODE and Vector Calculus'),('A7CH01','Engineering Chemistry'),('A7CS02','Data Structures'),('A7EC01','Electronic Devices and Applications'),('A7EN01','English for Skill Enhancement'),('A7CH01L','Chemistry Lab'),('A7CS02L','Data Structures Lab'),('A7EN01L','English Communication Lab'),('A7ME02L','Engineering Workshop'),('A7CS03L','Python Programming Lab')],
        'Year 2 Semester 3': [('A7BS03','Mathematical and Statistical Foundations'),('A7CS03','Computer Organization and Architecture'),('A7CS04','OOP through Java'),('A7CS05','Software Engineering'),('A7CS06','Database Management System'),('A7BS03L','Computational Math Lab'),('A7CS04L','Java Lab'),('A7CS05L','SE Lab'),('A7CS06L','DBMS Lab'),('A7CS07','Web Technologies')],
        'Year 2 Semester 4': [('A7BS04','Discrete Mathematics'),('A7CS08','Operating Systems'),('A7CS09','Algorithms Design and Analysis'),('A7CS10','Computer Networks'),('A7CS11','Artificial Intelligence'),('A7CS12','Innovation and Entrepreneurship'),('A7CS08L','OS Lab'),('A7CS10L','CN Lab'),('A7CS11L','AI Lab'),('A7CS13','Data Visualization'),('A7MC01','Indian Knowledge System')],
        'Year 3 Semester 5': [('A7CS14','Machine Learning'),('A7CS15','Automata and Compiler Design'),('A7CS16','Natural Language Processing'),('A7CSPE1','Professional Elective-I'),('A7CSOE1','Open Elective-I'),('A7CS14L','ML Lab'),('A7CS16L','NLP Lab'),('A7CS15L','Compiler Design Lab'),('A7CS17','Field Based Research Project'),('A7CS18','UI Design')],
        'Year 3 Semester 6': [('A7CS19','Generative AI'),('A7CS20','Deep Learning'),('A7HS01','Business Economics'),('A7CSPE2','Professional Elective-II'),('A7CSOE2','Open Elective-II'),('A7CS19L','Generative AI Lab'),('A7CS20L','Deep Learning Lab'),('A7CS21L','Chatbots Lab'),('A7EN02L','Employability Skills Lab'),('A7CS22','Prompt Engineering'),('A7MC02','Environmental Science')],
        'Year 4 Semester 7': [('A7CS23','Reinforcement Learning'),('A7CS24','Data Analytics and Visualization'),('A7HS02','Fundamentals of Management'),('A7CSPE3','Professional Elective-III'),('A7CSPE4','Professional Elective-IV'),('A7CSOE3','Open Elective-III'),('A7CS23L','RL Lab'),('A7CS24L','Data Analytics Lab'),('A7CS25','Summer Internship')],
        'Year 4 Semester 8': [('A7CSPE5','Professional Elective-V'),('A7CSPE6','Professional Elective-VI'),('A7CS26','Project Work')],
    }),
    'R22': ('r22', {
        'Year 1 Semester 1': [('22BS01','Mathematics-I'),('22PH01','Engineering Physics'),('22CS01','Programming for Problem Solving (C)'),('22EE01','Basic Electrical Engineering'),('22ME01','Engineering Drawing'),('22PH01L','Physics Lab'),('22CS01L','C Programming Lab'),('22EN01L','English Lab'),('22ME02L','Workshop')],
        'Year 1 Semester 2': [('22BS02','Mathematics-II'),('22CH01','Engineering Chemistry'),('22CS02','Data Structures'),('22EC01','Electronic Devices'),('22EN01','English Communication'),('22CH01L','Chemistry Lab'),('22CS02L','DS Lab'),('22CS03L','Python Lab'),('22MC01','Environmental Science')],
        'Year 2 Semester 3': [('22BS03','Probability and Statistics'),('22CS03','Computer Organization'),('22CS04','OOP through Java'),('22CS05','Discrete Mathematics'),('22CS06','Digital Logic Design'),('22CS04L','Java Lab'),('22CS06L','Digital Lab'),('22BS03L','Statistics Lab')],
        'Year 2 Semester 4': [('22CS07','DBMS'),('22CS08','Operating Systems'),('22CS09','DAA'),('22CS10','Software Engineering'),('22CS11','Computer Networks'),('22CS07L','DBMS Lab'),('22CS08L','OS Lab'),('22CS11L','CN Lab')],
        'Year 3 Semester 5': [('22CS12','Compiler Design'),('22CS13','Machine Learning'),('22CS14','Web Technologies'),('22CS15','Information Security'),('22CSPE1','Elective-I'),('22CS13L','ML Lab'),('22CS14L','Web Lab'),('22CS16','Mini Project')],
        'Year 3 Semester 6': [('22CS17','AI'),('22CS18','Cloud Computing'),('22CS19','Data Mining'),('22CSPE2','Elective-II'),('22CSPE3','Elective-III'),('22CS18L','Cloud Lab'),('22CS20','Seminar')],
        'Year 4 Semester 7': [('22CS21','Deep Learning'),('22CS22','Big Data Analytics'),('22CSPE4','Elective-IV'),('22CSPE5','Elective-V'),('22CS23','Project-I'),('22CS21L','DL Lab'),('22CS24','Industry Internship')],
        'Year 4 Semester 8': [('22CSPE6','Elective-VI'),('22CS25','Project-II'),('22CS26','Comprehensive Viva')],
    }),
    'MLR20': ('mlr20', {
        'Year 1 Semester 1': [('20BS01','Mathematics-I'),('20PH01','Engineering Physics'),('20CS01','Problem Solving using C'),('20EE01','Basic Electrical Engg'),('20ME01','Engineering Graphics'),('20PH01L','Physics Lab'),('20CS01L','C Lab'),('20EN01L','English Lab')],
        'Year 1 Semester 2': [('20BS02','Mathematics-II'),('20CH01','Engineering Chemistry'),('20CS02','Data Structures'),('20EC01','Basic Electronics'),('20EN01','English'),('20CH01L','Chemistry Lab'),('20CS02L','DS Lab'),('20ME02L','Workshop')],
        'Year 2 Semester 3': [('20BS03','Mathematics-III'),('20CS03','OOP Java'),('20CS04','Computer Organization'),('20CS05','Discrete Mathematics'),('20CS06','DBMS'),('20CS03L','Java Lab'),('20CS06L','DBMS Lab'),('20BS03L','Math Lab')],
        'Year 2 Semester 4': [('20CS07','OS'),('20CS08','DAA'),('20CS09','Computer Networks'),('20CS10','Software Engineering'),('20CS11','FLAT'),('20CS07L','OS Lab'),('20CS09L','CN Lab'),('20CS12','Professional Ethics')],
        'Year 3 Semester 5': [('20CS13','Compiler Design'),('20CS14','Web Technologies'),('20CS15','ML'),('20CS16','Info Security'),('20CSPE1','Elective-I'),('20CS15L','ML Lab'),('20CS14L','Web Lab'),('20CS17','Mini Project')],
        'Year 3 Semester 6': [('20CS18','AI'),('20CS19','Cloud Computing'),('20CS20','Data Mining'),('20CSPE2','Elective-II'),('20CSPE3','Elective-III'),('20CS19L','Cloud Lab'),('20CS21','Seminar')],
        'Year 4 Semester 7': [('20CS22','Big Data'),('20CS23','IoT'),('20CSPE4','Elective-IV'),('20CSPE5','Elective-V'),('20CS24','Project-I'),('20CS23L','IoT Lab'),('20CS25','Internship')],
        'Year 4 Semester 8': [('20CSPE6','Elective-VI'),('20CS26','Project-II'),('20CS27','Comprehensive Viva')],
    }),
    'MLR18': ('mlr18', {
        'Year 1 Semester 1': [('18BS01','Mathematics-I'),('18PH01','Engineering Physics'),('18CS01','Computer Programming (C)'),('18EE01','Basic Electrical Engg'),('18ME01','Engineering Drawing'),('18PH01L','Physics Lab'),('18CS01L','C Lab'),('18EN01L','English Lab')],
        'Year 1 Semester 2': [('18BS02','Mathematics-II'),('18CH01','Engineering Chemistry'),('18CS02','Data Structures'),('18EC01','Electronic Devices'),('18EN01','English'),('18CH01L','Chemistry Lab'),('18CS02L','DS Lab'),('18ME02L','Workshop')],
        'Year 2 Semester 3': [('18BS03','Mathematics-III'),('18CS03','OOP (C++)'),('18CS04','Computer Organization'),('18CS05','Discrete Mathematics'),('18CS06','DBMS'),('18CS03L','C++ Lab'),('18CS06L','DBMS Lab')],
        'Year 2 Semester 4': [('18CS07','OS'),('18CS08','DAA'),('18CS09','Computer Networks'),('18CS10','Software Engineering'),('18CS11','FLAT'),('18CS07L','OS Lab'),('18CS09L','CN Lab')],
        'Year 3 Semester 5': [('18CS12','Compiler Design'),('18CS13','Web Technologies'),('18CS14','ML'),('18CS15','Info Security'),('18CSPE1','Elective-I'),('18CS14L','ML Lab'),('18CS13L','Web Lab'),('18CS16','Mini Project')],
        'Year 3 Semester 6': [('18CS17','AI'),('18CS18','Cloud Computing'),('18CS19','Data Mining'),('18CSPE2','Elective-II'),('18CSPE3','Elective-III'),('18CS18L','Cloud Lab'),('18CS20','Seminar')],
        'Year 4 Semester 7': [('18CS21','Big Data'),('18CS22','IoT'),('18CSPE4','Elective-IV'),('18CSPE5','Elective-V'),('18CS23','Project-I'),('18CS22L','IoT Lab'),('18CS24','Internship')],
        'Year 4 Semester 8': [('18CSPE6','Elective-VI'),('18CS25','Project-II'),('18CS26','Comprehensive Viva')],
    }),
}

for reg_label, (reg_key, semesters) in regs.items():
    sems_html = ''
    for sem_name, subjects in semesters.items():
        rows = ''
        for code, name in subjects:
            pdf_path = f'syllabus/pdfs/{reg_key}/{code}.pdf'
            rows += f'        <tr><td><span class="code">{code}</span></td><td>{name}</td><td><a href="{pdf_path}" target="_blank" class="pdf-link">PDF</a></td></tr>\n'
        sems_html += f'    <div class="sem">\n      <h2>{sem_name}</h2>\n      <table>\n        <thead><tr><th>Code</th><th>Subject</th><th>Syllabus</th></tr></thead>\n        <tbody>\n{rows}        </tbody>\n      </table>\n    </div>\n'

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CSE {reg_label} Syllabus — MLRIT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <style>
    *,*::before,*::after {{box-sizing:border-box;margin:0;padding:0;}}
    body {{font-family:'Inter',sans-serif;background:#F4F1EA;color:#3A3A3A;line-height:1.7;}}
    .header {{background:#0B0F1A;padding:20px 32px;display:flex;align-items:center;gap:16px;}}
    .header a {{color:rgba(255,255,255,0.6);font-family:'Raleway',sans-serif;font-size:0.82rem;font-weight:600;text-decoration:none;}}
    .header a:hover {{color:#E85D1F;}}
    .header h1 {{font-family:'Playfair Display',serif;font-size:1.4rem;color:#fff;}}
    .content {{max-width:900px;margin:0 auto;padding:40px 32px;}}
    .sem {{margin-bottom:36px;}}
    .sem h2 {{font-family:'Raleway',sans-serif;font-size:0.82rem;font-weight:800;color:#18453B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid rgba(24,69,59,0.12);}}
    table {{width:100%;border-collapse:collapse;}}
    th {{font-family:'Raleway',sans-serif;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#888;text-align:left;padding:10px 14px;border-bottom:2px solid rgba(0,0,0,0.08);}}
    td {{font-size:0.88rem;padding:10px 14px;border-bottom:1px solid rgba(0,0,0,0.05);}}
    tr:hover td {{background:rgba(24,69,59,0.03);}}
    .code {{font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#18453B;background:rgba(24,69,59,0.08);padding:2px 8px;border-radius:4px;}}
    .pdf-link {{font-family:'Raleway',sans-serif;font-size:0.7rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:3px 10px;border:1px solid rgba(232,93,31,0.3);border-radius:5px;}}
    .pdf-link:hover {{background:#E85D1F;color:#fff;}}
    .note {{font-size:0.82rem;color:#888;font-style:italic;margin-bottom:24px;}}
  </style>
</head>
<body>
  <div class="header">
    <a href="cse.html#academics">&larr; Back to CSE</a>
    <h1>CSE {reg_label} Syllabus</h1>
  </div>
  <div class="content">
    <p class="note">Full semester-wise subject list for B.Tech CSE under {reg_label} regulation. Subject PDFs: departments/syllabus/pdfs/{reg_key}/[code].pdf</p>
{sems_html}  </div>
</body>
</html>'''

    filepath = f'{base}/cse-{reg_key}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Created: cse-{reg_key}.html')
