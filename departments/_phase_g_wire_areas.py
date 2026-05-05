"""
Phase G - update each fcard's <div class="fcard__hover-spec"> in the 5 dept
HTMLs with the real research areas pulled from faculty_profiles.json.

Faculty with no areas in the JSON keep the existing "—" placeholder.
"""
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
DB = HERE / "faculty_profiles.json"

PAGES = {
    "csit":   "csit.html",
    "it":     "it.html",
    "aiml":   "aiml.html",
    "cse-cs": "cse-cs.html",
    "cse-ds": "cse-ds.html",
}

db = json.loads(DB.read_text(encoding="utf-8"))

# Post-filter: drop tokens that are clearly NOT research areas
JUNK_TOKENS = {
    "regular", "ug degree", "pg degree", "btech", "mtech", "bsc", "msc", "phd",
    "n/a", "na", "none", "-", "—", "ms", "mr", "mrs", "dr",
    "cse", "ece", "eee", "it", "csit", "ds", "cs", "aiml", "aero", "mech", "mba",
    "computer science", "computer science engineering", "computer science and engineering",
    "cse-ai&ml", "cse-aiml", "cse(aiml)", "cse(ds)", "cse(cs)", "cse-ds", "cse-cs",
    "data science",
    "information technology", "electronics", "electrical", "mechanical engineering",
    "aeronautical engineering", "aeronautical",
    "freshman engineering", "mathematics", "physics", "chemistry", "english",
    "professor", "associate professor", "assistant professor",
}


def clean_areas(areas):
    out = []
    for a in areas:
        s = a.strip(" .;:-–—`'\"\\/").strip()
        if not s:
            continue
        if s.lower() in JUNK_TOKENS:
            continue
        # Drop pure-uppercase abbreviations that look like dept codes
        if len(s) <= 4 and s.isupper():
            continue
        out.append(s)
    return out


PATTERN = re.compile(
    r'(?P<before><div class="fcard"[^>]*data-author="[^"]*"[^>]*>\s*'
    r'<img src="images/(?P<dept>[^/]+)/(?P<slug>[^."]+)\.jpg"[^>]*/>'
    r'.*?<div class="fcard__hover-spec">)(?P<current>[^<]*)(?P<after></div>)',
    re.DOTALL,
)


def patch(name: str) -> tuple[int, int]:
    p = HERE / name
    text = p.read_text(encoding="utf-8")
    updated = total = 0

    def repl(m):
        nonlocal updated, total
        total += 1
        dept = m.group("dept")
        slug = m.group("slug")
        before = m.group("before")
        current = m.group("current")
        after = m.group("after")
        key = f"{dept}/{slug}"
        entry = db.get(key)
        cleaned = clean_areas(entry.get("areas", []) if entry else [])
        if cleaned:
            spec = ", ".join(cleaned[:3])
            if len(spec) > 80:
                spec = spec[:77].rstrip(" ,") + "..."
        else:
            spec = "—"
        if spec != current:
            updated += 1
        return f"{before}{spec}{after}"

    new_text = PATTERN.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
    return updated, total


for dept, name in PAGES.items():
    u, t = patch(name)
    print(f"{name:<14} updated {u}/{t} fcards with research areas")
