#!/usr/bin/env python3
"""Regenerate ALL semester HTML files with corrected R25 data from MLRIT."""
import os

base = 'c:/mlr/homepage/departments/syllabus/cse'

data = {
    'r25': {
        1: {
            1: [('A7BS01','Matrices and Calculus'),('A7BS08','Advanced Engineering Physics'),('A7CS01','Programming for Problem Solving'),('A7EE04','Basic Electrical Engineering'),('A7ME02','Computer Aided Engineering Drawing'),('A7BS09','Advanced Engineering Physics Lab'),('A7CS02','Programming for Problem Solving Lab'),('A7EE05','Basic Electrical Engineering Lab'),('A7CS06','IOT and IT Workshop')],
            2: [('A7BS02','Ordinary Differential Equations and Vector Calculus'),('A7BS10','Engineering Chemistry'),('A7CS03','Data Structures'),('A7EC01','Electronic Devices and Applications'),('A7HS01','English for Skill Enhancement'),('A7BS11','Engineering Chemistry Lab'),('A7CS04','Data Structures Lab'),('A7HS02','English Language and Communication Skills Lab'),('A7ME03','Engineering Workshop'),('A7CS05','Python Programming Lab')],
        },
        2: {
            3: [('A7BS03','Mathematical and Statistical Foundations'),('A7CS08','Computer Organization and Architecture'),('A7CS09','Object Oriented Programming through Java'),('A7CS11','Software Engineering'),('A7CS13','Database Management System'),('A7BS07','Computational Mathematics Lab'),('A7CS10','OOP through Java Lab'),('A7CS12','Software Engineering Lab'),('A7CS14','Database Management Systems Lab'),('A7CS53','Web Technologies')],
            4: [('A7CS07','Discrete Mathematics'),('A7CS15','Operating Systems'),('A7CS17','Algorithms Design and Analysis'),('A7CS18','Computer Networks'),('A7AI01','Artificial Intelligence'),('A7HS08','Innovation and Entrepreneurship'),('A7CS16','Operating Systems Lab'),('A7CS19','Computer Networks Lab'),('A7AI02','Artificial Intelligence Lab'),('A7DS03','Data Visualization (R/Power BI)'),('A7HS05','Indian Knowledge System')],
        },
        3: {
            5: [('A7AI03','Machine Learning'),('A7CS20','Automata and Compiler Design'),('A7AI04','Natural Language Processing'),('PE-I','Professional Elective-I'),('OE-I','Open Elective-I'),('A7AI05','Machine Learning Lab'),('A7AI06','Natural Language Processing Lab'),('A7CS21','Compiler Design Lab'),('A7AI07','Field Based Research Project'),('A7CS45','UI Design (Flutter/Android Studio)'),('A7HS04','Gender Sensitization / Human Values')],
            6: [('A7AI09','Generative AI'),('A7AI10','Deep Learning'),('A7HS06','Business Economics and Financial Analysis'),('PE-II','Professional Elective-II'),('OE-II','Open Elective-II'),('A7AI11','Generative AI Lab'),('A7AI12','Deep Learning Lab'),('A7AI13','Chatbots Lab'),('A7HS03','English for Employability Skills Lab'),('A7AI14','Prompt Engineering'),('A7BS12','Environmental Science')],
        },
        4: {
            7: [('A7AI15','Reinforcement Learning'),('A7AI17','Data Analytics and Visualization'),('A7HS07','Fundamentals of Management'),('PE-III','Professional Elective-III'),('PE-IV','Professional Elective-IV'),('OE-III','Open Elective-III'),('A7AI16','Reinforcement Learning Lab'),('A7AI18','Data Analytics and Visualization Lab'),('A7AI19','Summer Internship')],
            8: [('PE-V','Professional Elective-V'),('PE-VI','Professional Elective-VI'),('A7AI26','Project Work')],
        },
    },
    'r22': {
        1: {
            1: [('22BS01','Linear Algebra and Calculus'),('22CS01','Programming for Problem Solving'),('22HS01','English for Skill Enhancement'),('22EE01','Basic Electrical and Electronics Engineering'),('22EC01','Electronic Devices and Applications'),('22CS01L','Programming Lab'),('22HS01L','English Communication Lab'),('22CS02','Introduction to IoT'),('22MC01','Seminar')],
            2: [('22BS02','Numerical Methods and Integral Transforms'),('22PH01','Applied Physics'),('22CH01','Engineering Chemistry'),('22ME01','Engineering Drawing'),('22PH01L','Applied Physics Lab'),('22CS03L','Python Programming Lab'),('22CS04','Elements of CSE'),('22MC02','Environmental Science')],
        },
        2: {
            3: [('22BS03','Computer Oriented Statistical Methods'),('22CS05','Digital Electronics and Computer Organization'),('22CS06','Data Structures'),('22CS07','Object Oriented Programming through Java'),('22CS08','Software Engineering'),('22CS06L','Data Structures Lab'),('22CS07L','Java Lab'),('22CS09','Data Visualization using R'),('22MC03','Gender Sensitization')],
            4: [('22BS04','Discrete Mathematics'),('22HS02','Business Economics and Financial Analysis'),('22CS10','Database Management Systems'),('22CS11','Operating Systems'),('22CS12','Software Testing Fundamentals'),('22CS10L','DBMS Lab'),('22CS11L','OS Lab'),('22CS13','Skill Development'),('22MC04','Constitution of India')],
        },
        3: {
            5: [('22CS14','Design and Analysis of Algorithms'),('22CS15','Cloud and DevOps'),('22CS16','Computer Networks'),('22CS16L','Computer Networks Lab'),('22CS15L','Cloud and DevOps Lab'),('22HS03L','Advanced Communication Skills Lab'),('22MC05','Human Values and Professional Ethics'),('22CSPE1','Professional Elective-I'),('22CSPE2','Professional Elective-II')],
            6: [('22CS17','Introduction to Artificial Intelligence'),('22CS18','Automata and Compiler Design'),('22CS19','Data Mining and Machine Learning'),('22CS19L','Data Mining and ML Lab'),('22MC06','Environmental Science (LE)'),('22CSPE3','Professional Elective-III'),('22CSPE4','Professional Elective-IV')],
        },
        4: {
            7: [('22CS20','Distributed Computing'),('22CS21','Cryptography and Network Security'),('22CS21L','CNS Lab'),('22CSPE5','Professional Elective-V'),('22CSPE6','Professional Elective-VI'),('22CS22','Research Project Phase-I')],
            8: [('22HS04','Organizational Behaviour'),('22CSPE7','Professional Elective-VII'),('22CS23','Research Project Phase-II')],
        },
    },
    'mlr20': {
        1: {
            1: [('20BS01','Linear Algebra and Calculus'),('20PH01','Applied Physics'),('20EE01','Basic Electrical and Electronics Engineering'),('20ME01','Engineering Graphics'),('20PH01L','Applied Physics Lab'),('20CS01','Introduction to IoT'),('20ME02L','Engineering Workshop')],
            2: [('20BS02','Advanced Calculus'),('20CH01','Applied Chemistry'),('20CS02','Programming for Problem Solving'),('20HS01','English'),('20CS02L','Programming Lab'),('20CH01L','Chemistry Lab'),('20HS01L','English Communication Lab')],
        },
        2: {
            3: [('20BS03','Probability and Statistics'),('20BS04','Discrete Mathematics'),('20CS03','Database Management System'),('20CS04','Python Programming'),('20CS03L','Data Structures Lab'),('20CS05L','DBMS Lab'),('20MC01','Environmental Studies')],
            4: [('20CS06','Digital Electronics and Computer Organization'),('20HS02','Business Economics and Financial Analysis'),('20CS07','Object Oriented Programming'),('20CS08','Design and Analysis of Algorithms'),('20CS09L','Advanced Data Structures Lab'),('20CS07L','OOP Lab'),('20MC02','Gender Sensitization')],
        },
        3: {
            5: [('20CS10','Web Technologies'),('20CS11','Automata and Compiler Design'),('20CS12','Operating Systems'),('20CS10L','Web Technologies Lab'),('20CS13L','Linux Programming Lab'),('20MC03','Human Values and Professional Ethics'),('20CSPE1','Professional Elective-I')],
            6: [('20CS14','Software Engineering'),('20CS15','Computer Networks'),('20CS16','Machine Learning'),('20CS15L','Network Simulation Lab'),('20CS16L','Machine Learning Lab'),('20CSPE2','Professional Elective-II'),('20CSPE3','Professional Elective-III')],
        },
        4: {
            7: [('20CS17','Big Data Analytics'),('20CS17L','Big Data Analytics Lab'),('20CSPE4','Professional Elective-IV'),('20CSPE5','Professional Elective-V'),('20CS18','Project Phase-I'),('20CS19','Internship')],
            8: [('20HS03','Management Science'),('20CSPE6','Professional Elective-VI'),('20CS20','Project Phase-II')],
        },
    },
    'mlr18': {
        1: {
            1: [('18BS01','Linear Algebra and Calculus'),('18PH01','Applied Physics'),('18EE01','Basic Electrical Engineering'),('18ME01','Engineering Graphics and Design'),('18PH01L','Applied Physics Lab'),('18EE01L','Basic Electrical Lab'),('18ME02L','Workshop Practices'),('18MC01','Social Innovation')],
            2: [('18BS02','Advanced Calculus'),('18CH01','Chemistry'),('18CS01','Programming for Problem Solving'),('18HS01','English'),('18CS01L','Programming Lab'),('18CH01L','Chemistry Lab'),('18HS01L','English Communication Lab'),('18MC02','Engineering Exploration')],
        },
        2: {
            3: [('18BS03','Probability and Statistics'),('18BS04','Discrete Structures'),('18CS02','Data Structures'),('18CS03','Database Management Systems'),('18EC01','Electronic Devices'),('18CS02L','Data Structures Lab'),('18CS03L','DBMS Lab'),('18MC03','Environmental Science')],
            4: [('18CS04','Digital Electronics'),('18CS05','Computer Organization and Architecture'),('18CS06','Object Oriented Programming'),('18CS07','Design and Analysis of Algorithms'),('18HS02','Business Economics and Financial Analysis'),('18CS04L','Digital Electronics Lab'),('18CS06L','OOP Lab'),('18MC04','Gender Sensitization')],
        },
        3: {
            5: [('18CS08','Web Technologies'),('18CS09','Formal Language and Automata Theory'),('18CS10','Operating Systems'),('18CS08L','Web Technologies Lab'),('18HS03L','Advanced Communication Skills Lab'),('18MC05','Constitution of India'),('18CSPE1','Professional Elective-I')],
            6: [('18CS11','Compiler Design'),('18CS12','Computer Networks'),('18CS13','Linux Programming'),('18CS12L','Network Simulation Lab'),('18CS13L','Linux Programming Lab'),('18MC06','Indian Traditional Knowledge'),('18CSPE2','Professional Elective-II'),('18CSPE3','Professional Elective-III')],
        },
        4: {
            7: [('18CS14','Big Data Analytics'),('18CS14L','Big Data Analytics Lab'),('18CSPE4','Professional Elective-IV'),('18CSPE5','Professional Elective-V'),('18CS15','Project Phase-I'),('18CS16','Internship')],
            8: [('18HS04','Operations Research'),('18CSPE6','Professional Elective-VI'),('18CS17','Project Phase-II')],
        },
    },
}

count = 0
for reg, years in data.items():
    for year, sems in years.items():
        for sem, subjects in sems.items():
            folder = f'{base}/{reg}/year{year}'
            os.makedirs(folder, exist_ok=True)
            filepath = f'{folder}/sem{sem}.html'
            reg_upper = reg.upper()

            labs = len([s for s in subjects if s[0].endswith('L') or 'Lab' in s[1] or 'Workshop' in s[1]])
            electives = len([s for s in subjects if 'PE' in s[0] or 'OE' in s[0] or 'Elective' in s[1]])

            rows = ''
            for code, name in subjects:
                rows += f'        <tr><td><span class="code">{code}</span></td><td>{name}</td></tr>\n'

            page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CSE {reg_upper} Year {year} Sem {sem}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <style>
    *,*::before,*::after {{box-sizing:border-box;margin:0;padding:0;}}
    body {{font-family:'Inter',sans-serif;background:#FFFFFF;color:#3A3A3A;line-height:1.7;}}
    .header {{background:#0B0F1A;padding:20px 32px;display:flex;align-items:center;gap:16px;}}
    .header a {{color:rgba(255,255,255,0.6);font-family:'Raleway',sans-serif;font-size:0.82rem;font-weight:600;text-decoration:none;}}
    .header a:hover {{color:#E85D1F;}}
    .header h1 {{font-family:'Playfair Display',serif;font-size:1.3rem;color:#fff;}}
    .header .reg {{font-family:'Raleway',sans-serif;font-size:0.72rem;font-weight:700;color:#E85D1F;background:rgba(232,93,31,0.12);padding:4px 12px;border-radius:12px;}}
    .content {{max-width:800px;margin:0 auto;padding:40px 32px;}}
    .title {{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:#0B0F1A;margin-bottom:8px;}}
    .subtitle {{font-family:'Raleway',sans-serif;font-size:0.78rem;font-weight:700;color:#18453B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:24px;}}
    table {{width:100%;border-collapse:collapse;margin-top:16px;}}
    th {{font-family:'Raleway',sans-serif;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#888;text-align:left;padding:12px 16px;border-bottom:2px solid rgba(0,0,0,0.08);}}
    td {{font-size:0.92rem;padding:14px 16px;border-bottom:1px solid rgba(0,0,0,0.05);}}
    tr:hover td {{background:rgba(232,93,31,0.03);}}
    .code {{font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#18453B;background:rgba(24,69,59,0.08);padding:3px 10px;border-radius:4px;letter-spacing:0.04em;}}
    .stats {{display:flex;gap:16px;margin-bottom:24px;}}
    .stat {{background:#FAFAF8;border-radius:10px;padding:16px 24px;text-align:center;flex:1;border-top:3px solid #18453B;}}
    .stat__num {{font-family:'Playfair Display',serif;font-weight:700;font-size:1.4rem;color:#18453B;}}
    .stat__label {{font-size:0.68rem;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-top:2px;}}
    .back-btn {{display:inline-block;margin-top:28px;font-family:'Raleway',sans-serif;font-size:0.82rem;font-weight:700;color:#fff;background:#18453B;padding:10px 24px;border-radius:8px;text-decoration:none;transition:background 0.2s;}}
    .back-btn:hover {{background:#E85D1F;}}
  </style>
</head>
<body>
  <div class="header">
    <a href="../../../cse.html#academics">&larr; Back to CSE</a>
    <h1>Semester {sem} Syllabus</h1>
    <span class="reg">{reg_upper}</span>
  </div>
  <div class="content">
    <div class="title">B.Tech CSE — Year {year}, Semester {sem}</div>
    <div class="subtitle">Regulation: {reg_upper} | {len(subjects)} Subjects</div>
    <div class="stats">
      <div class="stat"><div class="stat__num">{len(subjects)}</div><div class="stat__label">Subjects</div></div>
      <div class="stat"><div class="stat__num">{labs}</div><div class="stat__label">Labs</div></div>
      <div class="stat"><div class="stat__num">{electives}</div><div class="stat__label">Electives</div></div>
    </div>
    <table>
      <thead><tr><th>Code</th><th>Subject</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table>
    <a href="../../../cse.html#academics" class="back-btn">&larr; Back to CSE Academics</a>
  </div>
</body>
</html>'''

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page)
            count += 1

print(f'Regenerated {count} semester HTML files')
for reg in ['r25', 'r22', 'mlr20', 'mlr18']:
    sems = []
    for year in [1,2,3,4]:
        d = f'{base}/{reg}/year{year}'
        if os.path.exists(d):
            for s in sorted(os.listdir(d)):
                sems.append(f'year{year}/{s}')
    print(f'  {reg}: {len(sems)} files')
