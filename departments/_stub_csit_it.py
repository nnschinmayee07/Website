"""
Phase A stub generator: clone cse-cs.html into csit.html and it.html.

Performs targeted string replacements so each page identifies as the right
department, then injects a yellow "DRAFT" banner at the top of the About panel
so it is obvious the content has not yet been scraped/ingested (Phase B).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "cse-cs.html"

DRAFT_BANNER = (
    '\n        <div style="background:#FFF8E1;border:1px solid #F1C400;'
    'border-left:4px solid #E85D1F;padding:14px 18px;border-radius:8px;'
    'margin:0 0 20px;font-size:0.88rem;color:#5C4A00;">'
    '<strong>Draft page.</strong> Content for this department has not yet been ingested. '
    'The structure mirrors the rest of the UG departments; sections will be filled in Phase B.'
    '</div>\n'
)


def make_page(dest_name: str, replacements: list[tuple[str, str]]) -> None:
    text = SRC.read_text(encoding="utf-8")

    for old, new in replacements:
        if old not in text:
            print(f"WARN: pattern not found in source: {old[:60]!r}")
        text = text.replace(old, new)

    # Inject draft banner immediately after the About panel-heading
    marker = '<h2 class="panel-heading">About the Department</h2>'
    if marker in text:
        text = text.replace(marker, marker + DRAFT_BANNER, 1)
    else:
        print("WARN: 'About the Department' heading not found — banner not inserted")

    out = HERE / dest_name
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} ({len(text):,} bytes)")


# --- CSIT --------------------------------------------------------------------
make_page(
    "csit.html",
    [
        ("CSE (Cyber Security) Department — MLRIT",
         "Computer Science & Information Technology Department — MLRIT"),
        ('class="dept-nav__link dept-nav__link--dept">Cyber Security Department<',
         'class="dept-nav__link dept-nav__link--dept">CS & IT Department<'),
        ("B.Tech — Computer Science &amp; Engineering (Cyber Security)",
         "B.Tech — Computer Science & Information Technology"),
        ("Department of CSE — Cyber Security",
         "Department of Computer Science & Information Technology"),
        # syllabus path swaps so links don't 404 silently into the wrong dept
        ("syllabus/cse-cs/", "syllabus/csit/"),
        ("CSE Cyber Security", "CS & IT"),
    ],
)

# --- IT ----------------------------------------------------------------------
make_page(
    "it.html",
    [
        ("CSE (Cyber Security) Department — MLRIT",
         "Information Technology Department — MLRIT"),
        ('class="dept-nav__link dept-nav__link--dept">Cyber Security Department<',
         'class="dept-nav__link dept-nav__link--dept">IT Department<'),
        ("B.Tech — Computer Science &amp; Engineering (Cyber Security)",
         "B.Tech — Information Technology"),
        ("Department of CSE — Cyber Security",
         "Department of Information Technology"),
        ("syllabus/cse-cs/", "syllabus/it/"),
        ("CSE Cyber Security", "Information Technology"),
    ],
)
