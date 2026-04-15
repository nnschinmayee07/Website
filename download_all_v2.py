#!/usr/bin/env python3
"""Download ALL individual subject PDFs for ALL departments."""
import urllib.request, os, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = 'c:/mlr/homepage/departments/syllabus/pdfs'

def dl(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return True
    try:
        urllib.request.urlretrieve(url, path)
        return os.path.getsize(path) > 1000
    except:
        return False

# MECHANICAL R22
mech_urls = [
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/LINEAR-ALGEBRA-&-CALCULUS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/APPLIED-PHYSICS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/ENGINEERING-CHEMISTRY.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/ENGINEERING-GRAPHICS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/APPLIED-PHYSICS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/ENGINEERING-CHEMISTRY-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/ENGINEERING-WORKSHOP-PRACTICES.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-1/ENVIRONMENTAL-SCIENCE.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/NUMERICAL-METHODS-AND-INTEGRAL-TRANSFORMS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/ENGLISH-FOR-SKILL-ENHANCEMENT.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/ENGINEERING-MECHANICS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/PROGRAMMING-FOR-PROBLEM-SOLVING.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/ELEMENTS-OF-MECHANICAL-ENGINEERING-DESIGN.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/ENGLISH-LANGUAGE-AND-COMMUNICATION-SKILLS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/1-2/PROGRAMMING-FOR-PROBLEM-SOLVING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/PROBABILITY-STATISTICS-AND-COMPLEX-ANALYSIS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/STRENGTH-OF-MATERIALS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/MATERIAL-SCIENCE-AND-METALLURGY.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/MANUFACTURING-PROCESSES.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/THERMODYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/MANUFACTURING-PROCESSES-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/STRENGTH-OF-MATERIALS-AND-MATERIAL-SCIENCE-AND-METALLURGY-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-1/PYTHON-LAB-FOR-MECHANICAL-APPLICATIONS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/FLUID-MECHANICS-AND-HYDRAULIC-MACHINES.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/THERMAL-ENGINEERING--I.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/THEORY-OF-MACHINES--I.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/DESIGN-OF--MACHINE-ELEMENTS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/FLUID-MECHANICS-AND-HYDRAULIC-MACHINES-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/2-2/COMPUTER-AIDED-MACHINE-DRAWING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/BUSINESS_ECONOMICS_AND_FINANCIAL_ANALYSIS.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/MACHINE_DESIGN.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/THEORY_OF_MACHINES-II.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/CADCAM.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/THERMAL_ENGINEERING-II.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/CAD_LAB.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-1/THERMAL_ENGINEERING_LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-2/HEAT_TRANSFER.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-2/MACHINE_TOOLS.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-2/FINITE_ELEMENT_ANALYSIS.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-2/HEAT_TRANSFER_LAB.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/3-2/MACHINE_TOOLS_LAB.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/4-1/COMPOSITE_MATERIALS.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/4-1/ENGINEERING_METROLOGY_&_INSTRUMENTATION.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/4-1/COMPOSITE_MATERIALS_LAB.pdf',
    'http://files.mlrit.ac.in/curriculum/MECH/Mech-R22/4-1/ENGINEERING_METROLOGY_&_INSTRUMENTATION_LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/MECH/Mech-R22/4-2/RESEARCH_PROJECT_PHASE-II.pdf',
]

# AERONAUTICAL R22
aero_urls = [
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/LINEAR-ALGEBRA-&-CALCULUS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/APPLIED-PHYSICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/ENGLISH-FOR-SKILL-ENHANCEMENT.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/ENGINEERING-GRAPHICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/APPLIED-PHYSICS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/ENGLISH-LANGUAGE-AND-COMMUNICATION-SKILLS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-1/ENGINEERING-WORKSHOP-PRACTICES.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/NUMERICAL-METHODS-AND-INTEGRAL-TRANSFORMS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/ENGINEERING-CHEMISTRY.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/ENGINEERING-MECHANICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/PROGRAMMING-FOR-PROBLEM-SOLVING.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/ELEMENTS-OF-AERONAUTICAL-ENGINEERING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/ENGINEERING-CHEMISTRY-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/PROGRAMMING-FOR-PROBLEM-SOLVING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/1-2/ENVIRONMENTAL-SCIENCE.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/AIRPLANE-PERFORMANCE.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/SOLID-MECHANICS-FOR-AERONAUTICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/AERODYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/AERO-THERMODYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/SOLID-MECHANICS-FOR-AERONAUTICS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-1/AERODYNAMICS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/IOT-BASED-DRONE-SYSTEMS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/AEROSPACE-PROPULSION.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/AEROSPACE-STRUCTURES.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/PROBABILITY,-STATISTICS-AND-COMPLEX.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/FLIGHT-SIMULATION-AND-PROPULSION-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/IOT-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/AIRCRAFT-INTERIOR-DESIGN-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/2-2/PYTHON-COMPUTING-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/SMART-AEROSPACE-STRUCTURES.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/AI-FOR-AERODYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/AIRCRAFT-STABILITY-AND-CONTROL.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/AIRCRAFT-PRODUCTION-TECHNOLOGY.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/AEROSPACE-STRUCTURES-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-1/AIRCRAFT-PRODUCTION-TECHNOLOGY-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/UAV-DESIGN.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/AIR-TRANSPORTATION-SYSTEM.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/UAV-DESIGN-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/COMPUTATIONAL-STRUCTURAL-ANALYSIS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/VIBRATION-AND-STRUCTURAL-DYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/EXPERIMENTAL-STRESS-ANALYSIS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/FATIGUE-AND-FRACTURE-MECHANICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/3-2/FINITE-ELEMENT-ANALYSIS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/MECHANICS-OF-COMPOSITE-STRUCTURES.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/COMPUTATIONAL-FLUID-DYNAMICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/COMPOSITES-AND-ANALYSIS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/COMPUTATIONAL-FLUID-DYNAMICS-LAB.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/HELICOPTER-ENGINEERING.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/AERO-ELASTICITY.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-1/AVIONICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-2/MANAGEMENT-SCIENCE.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-2/FUNDAMENTALS-OF-COMBUSTION.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-2/ROCKET-AND-MISSILES.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-2/SPACE-MECHANICS.pdf',
    'https://files.mlrit.ac.in/curriculum/aero/AERO-R22/4-2/ADVANCED-PROPULSION.pdf',
]

# Download function for URL lists
def download_batch(name, urls, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    ok = fail = 0
    for url in urls:
        fname = url.rsplit('/', 1)[-1]
        fpath = os.path.join(out_folder, fname)
        if dl(url, fpath):
            ok += 1
        else:
            fail += 1
            if os.path.exists(fpath):
                os.remove(fpath)
    print(f'{name}: {ok} ok, {fail} fail')

# Download Mechanical R22 subjects
download_batch('Mechanical R22', mech_urls, f'{base}/mech-r22')

# Download Aeronautical R22 subjects
download_batch('Aeronautical R22', aero_urls, f'{base}/aero-r22')

# ECE R22 - try same pattern as CSE
ece_r22_sems = {
    '1-1': ['LINEAR-ALGEBRA-AND-CALCULUS','PROGRAMMING-FOR-PROBLEM-SOLVING','ENGLISH-FOR-SKILL-ENHANCEMENT','BASIC-ELECTRICAL-AND-ELECTRONICS-ENGINEERING','ELECTRONIC-DEVICES-AND-APPLICATIONS','PROGRAMMING-FOR-PROBLEM-SOLVING-LAB','ENGLISH-LANGUAGE-AND-COMMUNICATION-SKILLS-LAB','INTRODUCTION-TO-INTERNET-OF-THINGS'],
    '1-2': ['NUMERICAL-METHODS-AND-INTEGRAL-TRANSFORMS','APPLIED-PHYSICS','ENGINEERING-CHEMISTRY','ENGINEERING-DRAWING','APPLIED-PHYSICS-LAB','PYTHON-PROGRAMMING-LAB','ELEMENTS-OF-ELECTRONICS-AND-COMMUNICATION-ENGINEERING','ENVIRONMENTAL-SCIENCE'],
    '2-1': ['COMPUTER-ORIENTED-STATISTICAL-METHODS','SIGNALS-AND-SYSTEMS','ELECTRONIC-CIRCUITS','DIGITAL-SYSTEM-DESIGN','ELECTROMAGNETIC-THEORY','ELECTRONIC-CIRCUITS-LAB','DIGITAL-SYSTEM-DESIGN-LAB','GENDER-SENSITIZATION'],
    '2-2': ['BUSINESS-ECONOMICS-AND-FINANCIAL-ANALYSIS','ANALOG-COMMUNICATIONS','CONTROL-SYSTEMS','LINEAR-INTEGRATED-CIRCUITS','ANALOG-COMMUNICATIONS-LAB','CONTROL-SYSTEMS-LAB','LINEAR-INTEGRATED-CIRCUITS-LAB','CONSTITUTION-OF-INDIA'],
}

ece_urls = []
for sem, subjects in ece_r22_sems.items():
    for subj in subjects:
        ece_urls.append(f'https://files.mlrit.ac.in/curriculum/all/ece/ECE-R22/{sem}/{subj}.pdf')

download_batch('ECE R22', ece_urls, f'{base}/ece-r22')

# EEE R22 - try pattern
eee_r22_sems = {
    '1-1': ['LINEAR-ALGEBRA-AND-CALCULUS','APPLIED-PHYSICS','ENGINEERING-CHEMISTRY','ENGINEERING-GRAPHICS','APPLIED-PHYSICS-LAB','ENGINEERING-CHEMISTRY-LAB','ENGINEERING-WORKSHOP','ENVIRONMENTAL-SCIENCE'],
    '1-2': ['NUMERICAL-METHODS','ENGLISH-FOR-SKILL-ENHANCEMENT','PROGRAMMING-FOR-PROBLEM-SOLVING','BASIC-ELECTRONICS','PROGRAMMING-LAB','ENGLISH-LAB'],
    '2-1': ['ELECTRICAL-MACHINES-I','NETWORK-ANALYSIS','ELECTRONIC-DEVICES-AND-CIRCUITS','ELECTROMAGNETIC-FIELDS','ELECTRICAL-MACHINES-LAB','ELECTRONIC-DEVICES-LAB'],
    '2-2': ['ELECTRICAL-MACHINES-II','POWER-SYSTEMS-I','CONTROL-SYSTEMS','SIGNALS-AND-SYSTEMS','POWER-SYSTEMS-LAB','CONTROL-SYSTEMS-LAB'],
}

eee_urls = []
for sem, subjects in eee_r22_sems.items():
    for subj in subjects:
        eee_urls.append(f'https://files.mlrit.ac.in/curriculum/all/eee/EEE-R22/{sem}/{subj}.pdf')
        # Also try alternate pattern
        eee_urls.append(f'https://files.mlrit.ac.in/syllabus/EEE/22/{sem}/{subj}.pdf')

download_batch('EEE R22', eee_urls, f'{base}/eee-r22')

print('\nFinal counts:')
import glob
for d in sorted(glob.glob(f'{base}/*')):
    if os.path.isdir(d):
        count = len([f for f in os.listdir(d) if f.endswith('.pdf')])
        print(f'  {os.path.basename(d)}: {count} PDFs')
    elif d.endswith('.pdf'):
        size = os.path.getsize(d) // 1024
        print(f'  {os.path.basename(d)}: {size}KB')
