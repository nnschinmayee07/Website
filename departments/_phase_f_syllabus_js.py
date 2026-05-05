"""
Phase F follow-up: replace the cyber-security-themed Syllabus Explorer
data in csit.html and it.html with sensible standard B.Tech CS/IT subjects.
subjectDetails is emptied (we don't have authoritative topic-level data),
so clicking a subject simply expands without showing fabricated detail.

The Syllabus PDF link target is also corrected per dept.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent

# Generic, defensible BTech CS/IT subjects — close to the institute's core
# CS/IT curriculum without inventing specifics.
PROGRAMS_REPLACEMENT = """      var programs = {
        btech: {
          1: {
            1: ['Mathematics-I (Calculus & Linear Algebra)', 'Engineering Physics', 'Programming for Problem Solving (C)', 'Basic Electrical Engineering', 'English Communication', 'Programming Lab', 'Engineering Workshop'],
            2: ['Mathematics-II (Differential Equations & Vector Calculus)', 'Engineering Chemistry', 'Data Structures', 'Electronic Devices and Circuits', 'Environmental Science', 'Data Structures Lab', 'Chemistry Lab']
          },
          2: {
            3: ['Probability and Statistics', 'Discrete Mathematics', 'Object Oriented Programming through Java', 'Database Management Systems', 'Computer Organization & Architecture', 'Java Lab', 'DBMS Lab'],
            4: ['Operating Systems', 'Design and Analysis of Algorithms', 'Computer Networks', 'Software Engineering', 'Web Technologies', 'OS Lab', 'CN Lab']
          },
          3: {
            5: ['Machine Learning', 'Compiler Design', 'Cloud Computing', 'Information Security', 'Professional Elective-I', 'ML Lab', 'Mini Project'],
            6: ['Artificial Intelligence', 'Big Data Analytics', 'Mobile Application Development', 'Internet of Things', 'Professional Elective-II', 'Open Elective-I', 'Seminar']
          },
          4: {
            7: ['Deep Learning', 'Professional Elective-III', 'Professional Elective-IV', 'Open Elective-II', 'Project Phase-I', 'Industry Internship'],
            8: ['Professional Elective-V', 'Professional Elective-VI', 'Project Phase-II', 'Comprehensive Viva']
          }
        }
      };"""

SUBJECT_DETAILS_REPLACEMENT = """      var subjectDetails = {};"""

PROGRAMS_RE = re.compile(r'      var programs = \{.*?\n      \};', re.DOTALL)
SUBJECT_DETAILS_RE = re.compile(r'      var subjectDetails = \{.*?\n      \};', re.DOTALL)


def patch(name: str, syllabus_pdf_path: str) -> None:
    p = HERE / name
    text = p.read_text(encoding="utf-8")
    actions = []

    new_text, n = PROGRAMS_RE.subn(PROGRAMS_REPLACEMENT, text, count=1)
    if n:
        actions.append("programs")
    text = new_text

    new_text, n = SUBJECT_DETAILS_RE.subn(SUBJECT_DETAILS_REPLACEMENT, text, count=1)
    if n:
        actions.append("subjectDetails")
    text = new_text

    # Also fix the syllabus PDF path (was syllabus/csit/r25/cs-r25-syllabus.pdf in csit;
    # for it we want syllabus/it/r25/...). Both are placeholder paths anyway.
    new_pdf = re.sub(
        r'pdf: "syllabus/[^/]+/r25/[^"]+"',
        f'pdf: "{syllabus_pdf_path}"',
        text,
        count=1,
    )
    if new_pdf != text:
        actions.append("syllabus-pdf-path")
    text = new_pdf

    p.write_text(text, encoding="utf-8")
    print(f"{name}: {', '.join(actions) if actions else '(no changes)'}")


patch("csit.html", "syllabus/csit/r25/csit-r25-syllabus.pdf")
patch("it.html",   "syllabus/it/r25/it-r25-syllabus.pdf")
