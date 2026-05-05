"""
Phase C (csit + it): replace the cloned CSE-CS faculty grid with the real
CSIT and IT faculty rosters scraped from
  https://mlrit.ac.in/faculty_categories/cs-it/
  https://mlrit.ac.in/faculty_categories/it/

The fcard template is preserved exactly. Image paths point to
images/<dept>/<slug>.jpg; the existing onerror handler shows initials when
the image is missing, which is the case for these new departments.
"""
from pathlib import Path
import re
from urllib.parse import quote

HERE = Path(__file__).resolve().parent

# ---------- faculty rosters --------------------------------------------------

CSIT_FACULTY = [
    # (name, designation, specialization_or_blank, is_hod)
    ("Dr. D.B.K. Kamesh",        "Professor & HOD",     "",  True),
    ("Ms. P. Nishitha",          "Assistant Professor", "",  False),
    ("D. Rajeshwari",            "Assistant Professor", "",  False),
    ("A. Nirisha",               "Assistant Professor", "",  False),
    ("P. Poojasree",             "Assistant Professor", "",  False),
    ("Rajkumar Bhookya",         "Assistant Professor", "",  False),
    ("Devolla Manogna",          "Assistant Professor", "",  False),
    ("S. Anudeep",               "Assistant Professor", "",  False),
    ("Banothu Seva",             "Assistant Professor", "",  False),
    ("Ms. Madhavi Banala",       "Assistant Professor", "",  False),
    ("N. Thulasi Chithra",       "Assistant Professor", "",  False),
    ("V. Srikanth",              "Assistant Professor", "",  False),
    ("T. Gandhi",                "Assistant Professor", "",  False),
    ("Mrs. T. Mounika",          "Assistant Professor", "",  False),
    ("Mrs. S. Parvathi",         "Assistant Professor", "",  False),
    ("N. Sandhya",               "Assistant Professor", "",  False),
    ("Mrs. M. Srividya",         "Assistant Professor", "",  False),
    ("Ms. D. Neelima Priyadarshini", "Assistant Professor", "", False),
    ("Ms. N. Vijayasri",         "Assistant Professor", "",  False),
    ("S. Navya",                 "Assistant Professor", "",  False),
]

IT_FACULTY = [
    ("Dr. N V Raja Sekhar Reddy",  "Professor & HOD",     "",  True),
    ("Dr. Dhilli Rao Gorja",       "Associate Professor", "",  False),
    ("Mrs. K. Neeraja",            "Associate Professor", "PhD, JNTUH (2020)", False),
    ("Mr. Vikram Raju",            "Associate Professor", "PhD, Manipal University (2020)", False),
    ("Dr. Mopur Vijaya Bhaskar Reddy", "Associate Professor", "", False),
    ("Mrs. IVS. Haritha",          "Assistant Professor", "",  False),
    ("Mrs. G. Anitha",             "Assistant Professor", "",  False),
    ("Vemuri Nitin",               "Assistant Professor", "",  False),
    ("Mrs. Shruthi Patel",         "Assistant Professor", "",  False),
    ("Mr. D. Sandeep",             "Assistant Professor", "",  False),
    ("J. Adilakshmi",              "Assistant Professor", "",  False),
    ("Bhasker Boddu",              "Assistant Professor", "",  False),
    ("P. Laxmaiah",                "Assistant Professor", "",  False),
    ("B. Varija",                  "Assistant Professor", "",  False),
    ("Ms. B. Sushma",              "Assistant Professor", "",  False),
    ("G. Sathyanarayan",           "Assistant Professor", "",  False),
    ("Mr. Mohd Anwar Ali",         "Assistant Professor", "",  False),
    ("M. Harshini",                "Assistant Professor", "",  False),
    ("J. Shubangi",                "Assistant Professor", "",  False),
    ("Agosh M C",                  "Faculty",             "",  False),
    ("Venkatesh G",                "Faculty",             "",  False),
    ("Hm Lijo Mon",                "Faculty",             "",  False),
]

# ---------- helpers ----------------------------------------------------------


def slug(name: str) -> str:
    """Generate a filename-safe slug from a name."""
    s = name.lower()
    s = re.sub(r"\b(dr|mr|mrs|ms|hm)\b\.?", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def initials(name: str) -> str:
    """Two-letter initials from a name, ignoring honorific prefixes."""
    cleaned = re.sub(r"\b(Dr|Mr|Mrs|Ms|Hm)\b\.?", "", name)
    parts = re.findall(r"[A-Za-z]+", cleaned)
    if len(parts) == 0:
        return "??"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def stripped_name(name: str) -> str:
    """Display-friendly compaction (single spaces, no double-prefix)."""
    return re.sub(r"\s+", " ", name).strip()


HOD_BADGE = (
    '<div style="position:absolute;top:10px;left:10px;z-index:6;'
    'font-family:\'Raleway\',sans-serif;font-size:0.6rem;font-weight:800;'
    'letter-spacing:0.1em;text-transform:uppercase;color:#fff;background:#1F6B24;'
    'padding:3px 8px;border-radius:4px;">HOD</div>'
)


def fcard(name: str, role: str, spec: str, is_hod: bool, dept_slug: str) -> str:
    nm = stripped_name(name)
    sl = slug(name)
    ini = initials(name)
    photo = f"images/{dept_slug}/{sl}.jpg"
    spec_html = (spec or "—")
    profile_url = (
        f'faculty-profile.html?name={quote(nm)}&role={quote(role)}'
        f'&photo={quote(photo)}'
    )
    return f"""          <div class="fcard" data-author="{nm}"{' style="position:relative;"' if is_hod else ''}>
              <img src="{photo}" alt="{nm}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'" />
              <div class="fcard__ini" style="display:none">{ini}</div>{(chr(10) + '              ' + HOD_BADGE) if is_hod else ''}
              <div class="fcard__overlay">
                <div class="fcard__name">{nm}</div>
                <div class="fcard__role">{role}</div>
              </div>
              <div class="fcard__hover-info">
                <div class="fcard__hover-name">{nm}</div>
                <div class="fcard__hover-role">{role}</div>
                <div class="fcard__hover-spec">{spec_html}</div>
                <a href="{profile_url}" class="fcard__hover-btn">View Research</a>
              </div>
          </div>
"""


def build_grid_inner(roster, dept_slug: str) -> str:
    body = "\n".join(fcard(n, r, s, h, dept_slug) for n, r, s, h in roster)
    return body + "        "


# Match the entire fcard-grid contents (between its opening tag and the </div>
# that immediately precedes the </div> closing the panel-faculty)
GRID_RE = re.compile(
    r'(<div id="faculty-grid-section" class="fcard-grid">)(.*?)(\n        </div>\n      </div>)',
    re.DOTALL,
)


def patch(path: Path, roster, dept_slug: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_inner = "\n" + build_grid_inner(roster, dept_slug)
    new_text, count = GRID_RE.subn(
        lambda m: m.group(1) + new_inner + m.group(3), text, count=1
    )
    if count == 0:
        print(f"FAIL: faculty-grid block not located in {path.name}")
        return
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.name}: replaced grid with {len(roster)} faculty cards")


if __name__ == "__main__":
    patch(HERE / "csit.html", CSIT_FACULTY, "csit")
    patch(HERE / "it.html",   IT_FACULTY,   "it")
