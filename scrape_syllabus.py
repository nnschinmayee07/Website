"""
MLRIT Syllabus Scraper
Fetches all curriculum pages from mlrit.ac.in and saves as structured local HTML files.
Structure: departments/syllabus/[dept]/[regulation]/year[n]/sem[n].html
"""

import os
import re
import requests
from bs4 import BeautifulSoup

# ── Colour palette ──────────────────────────────────────────────────────────
GREEN  = "#18453B"
ORANGE = "#E85D1F"
BG     = "#F4F1EA"

# ── All curriculum URLs ──────────────────────────────────────────────────────
URLS = {
    "cse": {
        "mlr18": "https://mlrit.ac.in/curriculum/cse-mlr18-ug-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/cse-mlr20-ug-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/cse-r22-ug-syllabus/",
        "r25":   "https://mlrit.ac.in/curriculum/cse-r25syllabus/",
    },
    "cse-aiml": {
        "mlr20": "https://mlrit.ac.in/curriculum/cse-aiml-mlr20-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/cse-aiml-r22-syllabus/",
        "r25":   "https://mlrit.ac.in/curriculum/cse-aiml-r25-syllabus/",
    },
    "cse-ds": {
        "mlr20": "https://mlrit.ac.in/curriculum/data-science-mlr20-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/csit-r22-syllabus/",
    },
    "ece": {
        "mlr18": "https://mlrit.ac.in/curriculum/ece-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/ece-mlr20-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/ece-r22-syllabus/",
    },
    "eee": {
        "mlr18": "https://mlrit.ac.in/curriculum/eee-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/eee-mlr20-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/eee-r22-syllabus/",
    },
    "mechanical": {
        "mlr18": "https://mlrit.ac.in/curriculum/mechanical-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/mechanical-mlr20-syllabus/",
    },
    "aeronautical": {
        "mlr18": "https://mlrit.ac.in/curriculum/aeronautical-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/aeronautical-mlr20-syllabus/",
        "r22":   "https://mlrit.ac.in/curriculum/aeronautical-r22-syllabus/",
        "mtech-mlr18": "https://mlrit.ac.in/curriculum/aeronautical-m-tech-mlr18-syllabus/",
    },
    "mba": {
        "mlr18": "https://mlrit.ac.in/curriculum/mba-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/mba-mlr20-syllabus/",
    },
    "cse-mtech": {
        "mlr18": "https://mlrit.ac.in/curriculum/cse-m-tech-mlr18-syllabus/",
        "mlr20": "https://mlrit.ac.in/curriculum/cse-m-tech-mlr20-syllabus/",
    },
}

# ── Semester heading patterns ────────────────────────────────────────────────
# Matches: I-I, I-II, II-I, II-II, III-I, III-II, IV-I, IV-II
# Also: "I B.Tech- I Semester", "II B.Tech- II Semester", etc.
SEM_PATTERNS = [
    (re.compile(r'^(I{1,3}V?|IV)\s*[-–]\s*(I{1,2})$', re.I), None),
    (re.compile(r'^(I{1,3}V?|IV)\s*B\.?Tech\.?\s*[-–]\s*(I{1,2})\s*Sem', re.I), None),
    (re.compile(r'^(I{1,3}V?|IV)\s*YEAR\s*[-–]\s*(I{1,2})\s*SEM', re.I), None),
    (re.compile(r'^(FIRST|SECOND|THIRD|FOURTH)\s*YEAR\s*[-–]\s*(FIRST|SECOND)\s*SEM', re.I), None),
    # Numeric format: 1-1, 1-2, 2-1, 2-2, 3-1, 3-2, 4-1, 4-2
    (re.compile(r'^([1-4])\s*[-–]\s*([12])$'), "numeric"),
]

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4}
ROMAN2 = {"FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4}

def roman_to_int(s):
    s = s.strip().upper()
    return ROMAN.get(s) or ROMAN2.get(s) or 0

def parse_sem_heading(text):
    """Return (year, sem) tuple or None."""
    text = text.strip()
    for pat, mode in SEM_PATTERNS:
        m = pat.match(text)
        if m:
            if mode == "numeric":
                return (int(m.group(1)), int(m.group(2)))
            y = roman_to_int(m.group(1))
            s = roman_to_int(m.group(2))
            if y and s:
                return (y, s)
    return None

def html_template(dept, regulation, year, sem, subjects, back_path):
    rows = ""
    for code, name in subjects:
        rows += f'<tr><td class="code">{code}</td><td>{name}</td></tr>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{dept.upper()} {regulation.upper()} — Year {year} Sem {sem} — MLRIT</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Inter',sans-serif;background:{BG};color:#1a1a1a;padding:40px;max-width:900px;margin:0 auto}}
  h1{{font-family:Georgia,serif;color:{GREEN};margin-bottom:6px;font-size:1.8rem}}
  .meta{{color:#666;font-size:0.88rem;margin-bottom:28px}}
  table{{width:100%;border-collapse:collapse}}
  th{{background:{GREEN};color:#fff;padding:10px 16px;text-align:left;font-size:0.78rem;letter-spacing:0.06em;text-transform:uppercase}}
  td{{padding:12px 16px;border-bottom:1px solid rgba(0,0,0,0.07);font-size:0.92rem}}
  tr:hover td{{background:rgba(24,69,59,0.04)}}
  .code{{font-family:monospace;color:{GREEN};font-weight:700;white-space:nowrap}}
  a.back{{display:inline-block;margin-bottom:24px;color:{ORANGE};text-decoration:none;font-weight:600;font-size:0.85rem}}
  a.back:hover{{text-decoration:underline}}
</style>
</head>
<body>
<a class="back" href="{back_path}">← Back to CSE Department</a>
<h1>{dept.upper()} — Year {year}, Semester {sem}</h1>
<p class="meta">Regulation: {regulation.upper()} &nbsp;|&nbsp; MLRIT — Marri Laxman Reddy Institute of Technology</p>
<table>
<thead><tr><th>Subject Code</th><th>Subject Name</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>"""

def scrape_and_save(dept, regulation, url):
    print(f"  Fetching {dept}/{regulation} → {url}")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f"    ✗ HTTP {r.status_code}")
            return 0
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return 0

    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.get_text(separator="\n")
    lines = [l.strip() for l in body.splitlines() if l.strip()]

    # Parse into semesters
    semesters = {}   # (year, sem) -> [(code, name), ...]
    current_sem = None

    i = 0
    while i < len(lines):
        line = lines[i]
        sem = parse_sem_heading(line)
        if sem:
            current_sem = sem
            semesters.setdefault(current_sem, [])
            i += 1
            continue

        # Subject code pattern: starts with A[0-9] or similar
        if current_sem and re.match(r'^[A-Z][0-9A-Z]{3,}$', line):
            code = line
            name = lines[i+1] if i+1 < len(lines) else ""
            # Skip if name looks like another code or heading
            if name and not re.match(r'^[A-Z][0-9A-Z]{3,}$', name) and not parse_sem_heading(name):
                semesters[current_sem].append((code, name))
                i += 2
                continue
        i += 1

    if not semesters:
        print(f"    ✗ No semester data parsed")
        return 0

    saved = 0
    for (year, sem), subjects in sorted(semesters.items()):
        if not subjects:
            continue
        folder = os.path.join("departments", "syllabus", dept, regulation, f"year{year}")
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, f"sem{sem}.html")
        # Relative back path
        back = "../" * 4 + "departments/cse.html"
        html = html_template(dept, regulation, year, sem, subjects, back)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"    ✓ Saved: {filepath} ({len(subjects)} subjects)")
        saved += 1

    return saved

# ── Main ─────────────────────────────────────────────────────────────────────
total = 0
failed = []

for dept, regs in URLS.items():
    print(f"\n{'='*50}")
    print(f"Department: {dept.upper()}")
    print('='*50)
    for regulation, url in regs.items():
        count = scrape_and_save(dept, regulation, url)
        if count == 0:
            failed.append(f"{dept}/{regulation}")
        total += count

print(f"\n{'='*50}")
print(f"DONE — {total} semester files created")
if failed:
    print(f"Failed ({len(failed)}): {', '.join(failed)}")
print('='*50)
