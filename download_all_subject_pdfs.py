#!/usr/bin/env python3
"""Download ALL individual subject PDFs from MLRIT for all departments."""

import urllib.request, os, ssl

# Disable SSL verification for mlrit.ac.in
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_out = 'c:/mlr/homepage/departments/syllabus/pdfs'

# CSE R22 individual subjects (from the fetched data)
cse_r22 = {
    '1-1': [
        'LINEAR-ALGEBRA-AND-CALCULUS', 'PROGRAMMING-FOR-PROBLEM-SOLVING', 'ENGLISH-FOR-SKILL-ENHANCEMENT',
        'BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING', 'ELECTRONIC-DEVICES-AND-APPLICATIONS',
        'PROGRAMMING-FOR-PROBLEM-SOLVING-LAB', 'ENGLISH-LANGUAGE-AND-COMMUNICATION-SKILLS-LAB',
        'INTRODUCTION-TO-INTERNET-OF-THINGS', 'SEMINAR'
    ],
    '1-2': [
        'NUMERICAL-METHODS-AND-INTEGRAL-TRANSFORMS', 'APPLIED-PHYSICS', 'ENGINEERING-CHEMISTRY',
        'ENGINEERING-DRAWING', 'APPLIED-PHYSICS-LAB', 'PYTHON-PROGRAMMING-LAB',
        'ELEMENTS-OF-COMPUTER-SCIENCE-AND-ENGINEERING', 'ENVIRONMENTAL-SCIENCE'
    ],
    '2-1': [
        'COMPUTER-ORIENTED-STATISTICAL-METHODS', 'DIGITAL-ELECTRONICS-AND-COMPUTER-ORGANIZATION',
        'DATA-STRUCTURES', 'OBJECT-ORIENTED-PROGRAMMING-THROUGH-JAVA', 'SOFTWARE-ENGINEERING',
        'DATA-STRUCTURES-LAB', 'OBJECT-ORIENTED-PROGRAMMING-THROUGH-JAVA-LAB',
        'SKILL-DEVELOPMENT-(DATA-VISUALIZATION-USING-R)', 'GENDER-SENSITIZATION'
    ],
    '2-2': [
        'DISCRETE-MATHEMATICS', 'BUSINESS-ECONOMICS-AND-FINANCIAL-ANALYSIS',
        'DATABASE-MANAGEMENT-SYSTEMS', 'OPERATING-SYSTEMS', 'SOFTWARE-TESTING-FUNDAMENTALS',
        'DATABASE-MANAGEMENT-SYSTEMS-LAB', 'OPERATING-SYSTEMS-LAB',
        'SKILL-DEVELOPMENT-COURSE', 'CONSTITUTION-OF-INDIA'
    ],
    '3-1': [
        'DESIGN_AND_ANALYSIS_OF_ALGORITHMS', 'CLOUD_AND_DEVOPS', 'COMPUTER_NETWORKS',
        'COMPUTER_NETWORKS_LAB', 'CLOUD_AND_DEVOPS_LAB', 'ADVANCED_COMMUNICATION_SKILLS_LAB',
        'HUMAN_VALUES_AND_PROFESSIONAL_ETHICS'
    ],
    '3-2': [
        'INTRODUCTION_TO_ARTIFICIAL_INTELLIGENCE', 'AUTOMATA_AND_COMPILER_DESIGN',
        'DATA_MINING_AND_MACHINE_LEARNING', 'DATA_MINING_AND_MACHINE_LEARNING_LAB'
    ],
    '4-1': [
        'DISTRIBUTED_COMPUTING', 'CRYPTOGRAPHY_AND_NETWORK_SECURITY',
        'CRYPTOGRAPHY_AND_NETWORK_SECURITY_LAB'
    ],
}

# CSE MLR18 individual subjects
cse_mlr18 = {
    '1-1': [
        'LINEAR--ALGEBRA-AND-CALCULUS', 'APPLIED-PHYSICS', 'BASIC-ELECTRICAL-ENGINEERING',
        'ENGINEERING-GRAPHICS-AND-DESIGN', 'APPLIED-PHYSICS-LABORATORY',
        'BASIC-ELECTRICAL-ENGINEERING-LAB', 'WORKSHOP-PRACTICES', 'SOCIAL-INNOVATION'
    ],
    '1-2': [
        'ADVANCED-CALCULAS', 'CHEMISTRY', 'PROGRAMMING-FOR-PROBLEM-SOLVING',
        'ENGLISH', 'PROGRAMMING-FOR-PROBLEM-SOLVING-LAB', 'CHEMISTRY-LAB',
        'ENGLISH-LANGUAGE-AND-COMMUNICATION-SKILLS-LABORATORY', 'ENGINEERING-EXPLORATION'
    ],
    '2-1': [
        'PROBABILITY-AND-STATISTICS', 'DISCRETE-STRUCTURES', 'DATA-STRUCTURES',
        'DATABASE-MANAGEMENT-SYSTEMS', 'ELECTRONIC-DEVICES',
        'DATA-STRUCTURES-LAB', 'DATABASE-MANAGEMENT-SYSTEMS-LAB', 'ENVIRONMENTAL-SCIENCE'
    ],
    '2-2': [
        'DIGITAL-ELECTRONICS', 'COMPUTER-ORGANIZATION-AND-ARCHITECTURE',
        'OBJECT-ORIENTED-PROGRAMMING', 'DESIGN-AND-ANALYSIS-OF-ALGORITHMS',
        'BUSINESS-ECONOMICS-AND-FINANCIAL-ANALYSIS',
        'ELECTRONIC-DEVICES-AND-DIGITAL-LOGIC-LAB', 'OBJECT-ORIENTED-PROGRAMMING-LAB',
        'GENDER-SENSITIZATION'
    ],
    '3-1': [
        'WEB-TECHNOLOGIES', 'FORMAL-LANGUAGE-AND-AUTOMATA-THEORY', 'OPERATING-SYSTEMS',
        'WEB-TECHNOLOGIES-LAB', 'ADVANCED-ENGLISH-COMMUNICATION-SKILLS-LAB', 'CONSTITUTION-OF-INDIA'
    ],
    '3-2': [
        'COMPLIER-DESIGN', 'COMPUTER-NETWORKS', 'LINUX-PROGRAMMING',
        'NETWORK-SIMULATION-LAB', 'LINUX-PROGRAMMING-LAB',
        'ESSENCE-OF-INDIAN-TRADITIONAL-KNOWLEDGE'
    ],
    '4-1': [
        'BIG-DATA-ANALYTICS', 'BIG-DATA-ANALYTICS-LAB'
    ],
    '4-2': [
        'OPERATIONS-RESEARCH'
    ],
}

# CSE MLR20 - key subjects
cse_mlr20 = {
    '1-1': ['linear-algebra-and-calculus', 'Applied-Physics', 'Basic-Electrical-and-Electronics-Engineering', 'Engineering-Graphics', 'Applied-Physics-Lab', 'Introduction-to-Internet-of-Things', 'Engineering-Workshop'],
    '1-2': ['Advanced-Calculus', 'Applied-Chemistry', 'Programming-for-Problem-Solving', 'English', 'Programming-for-problem-solving-Lab', 'Applied-Chemistry-Lab', 'English-Language-and-Communication-Skills-Lab'],
    '2-1': ['Probability-and-Statistics', 'Discrete-Mathematics', 'Database-Management-System', 'Python-Programming', 'Data-Structures-Lab', 'Database-Management-Systems-Lab', 'Environmental-Studies'],
    '2-2': ['Digital-Electronics-and-Computer-Organization', 'Business-Economics-and-Financial-Analysis', 'Object-oriented-Programming', 'Design-and-Analysis-of-Algorithms', 'Advanced-Data-Structures-Lab', 'Object-oriented-programming-lab', 'Gender-Sensitization'],
    '3-1': ['Web-technologies', 'Automata-and-compiler-design', 'Operating-systems', 'Web-echnologies-lab', 'Linux-Programming-Lab', 'Human-Values-and-Professional-Ethics'],
    '3-2': ['Software-Engineering', 'Computer-Networks', 'Machine-Learning', 'Network-Simulation-lab', 'Machine-Learning-Lab'],
    '4-1': ['Bid-data-Analytics', 'Big-Data-Analytics-Lab'],
}

def download_subjects(dept_code, reg_key, reg_folder, semesters):
    out_dir = f'{base_out}/{reg_key}'
    os.makedirs(out_dir, exist_ok=True)
    ok = 0
    fail = 0
    for sem, subjects in semesters.items():
        for subj in subjects:
            url = f'https://files.mlrit.ac.in/curriculum/all/{dept_code}/{reg_folder}/{sem}/{subj}.pdf'
            fname = f'{subj}.pdf'
            fpath = f'{out_dir}/{fname}'
            if os.path.exists(fpath) and os.path.getsize(fpath) > 1000:
                ok += 1
                continue
            try:
                urllib.request.urlretrieve(url, fpath)
                if os.path.getsize(fpath) > 1000:
                    ok += 1
                else:
                    os.remove(fpath)
                    fail += 1
            except Exception as e:
                fail += 1
    return ok, fail

# Download CSE R22
print('CSE R22 subjects...')
ok, fail = download_subjects('cse', 'r22', 'CSE-R22', cse_r22)
print(f'  R22: {ok} ok, {fail} fail')

# Download CSE MLR18
print('CSE MLR18 subjects...')
ok, fail = download_subjects('cse', 'mlr18', 'CSE-MLR18', cse_mlr18)
print(f'  MLR18: {ok} ok, {fail} fail')

# Download CSE MLR20
print('CSE MLR20 subjects...')
ok, fail = download_subjects('cse', 'mlr20', 'CSE-MLR20', cse_mlr20)
print(f'  MLR20: {ok} ok, {fail} fail')

# Also download complete syllabus PDFs for other departments
dept_pdfs = {
    'ece': [
        ('r25', 'http://files.mlrit.ac.in/uploads/ECE/R25_ECE.pdf', 'ece-r25-syllabus.pdf'),
        ('r22', 'http://files.mlrit.ac.in/uploads/ECE/R22_ECE.pdf', 'ece-r22-syllabus.pdf'),
    ],
    'eee': [
        ('r22', 'https://files.mlrit.ac.in/syllabus/EEE/22/EEE-R22.pdf', 'eee-r22-syllabus.pdf'),
    ],
    'mechanical': [
        ('r25', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_UG-R25.pdf', 'mech-r25-syllabus.pdf'),
        ('r25pg', 'https://files.mlrit.ac.in/uploads/Mechanical/Mech_PG-R25.pdf', 'mech-pg-r25-syllabus.pdf'),
    ],
    'aeronautical': [
        ('r25', 'https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_Aero_Syllabus.pdf', 'aero-r25-syllabus.pdf'),
    ],
}

print('\nOther department complete syllabus PDFs...')
for dept, pdfs in dept_pdfs.items():
    for reg, url, fname in pdfs:
        fpath = f'{base_out}/{fname}'
        if os.path.exists(fpath) and os.path.getsize(fpath) > 1000:
            print(f'  {fname}: already exists')
            continue
        try:
            urllib.request.urlretrieve(url, fpath)
            size = os.path.getsize(fpath)
            print(f'  {fname}: {size//1024}KB downloaded')
        except Exception as e:
            print(f'  {fname}: FAIL - {e}')

print('\nDone.')
