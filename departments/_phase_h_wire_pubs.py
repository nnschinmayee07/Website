"""
Phase H — wire scraped publications into the achievements panel of the 5
dept HTMLs. For each dept we gather all entries from faculty_pubs.json,
build a publication-card list, and replace the current placeholder text
under the 'Faculty Publications' subsection.

For depts with no scraped pubs we keep an honest note pointing to mlrit.ac.in.
"""
from pathlib import Path
import json
import re
import html as html_mod

HERE = Path(__file__).resolve().parent
PUBS = json.loads((HERE / "faculty_pubs.json").read_text(encoding="utf-8"))

PAGES = {
    "csit":   "csit.html",
    "it":     "it.html",
    "aiml":   "aiml.html",
    "cse-cs": "cse-cs.html",
    "cse-ds": "cse-ds.html",
}

PUBS_PLACEHOLDER_RE = re.compile(
    r'(<div class="panel-sub" id="pub-section">Faculty Publications</div>\s*)'
    r'<p>[^<]*</p>',
    re.I,
)


def safe(t: str) -> str:
    """Lightly clean a scraped string for HTML rendering."""
    t = t.strip()
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\s+", " ", t)
    return t


def build_pub_block(dept: str) -> str:
    """Collect this dept's publications from PUBS db and build the HTML."""
    entries = []
    for key, v in PUBS.items():
        if not key.startswith(f"{dept}/"):
            continue
        for r in v.get("research", []):
            entries.append({
                "title":  r.get("title", ""),
                "venue":  r.get("venue", ""),
                "year":   r.get("year", ""),
                "author": v.get("name", ""),
            })

    if not entries:
        return (
            '<div class="panel-sub" id="pub-section">Faculty Publications</div>\n'
            '<p>Faculty publications for this department are listed on each '
            'individual faculty profile page on '
            '<a href="https://mlrit.ac.in/" style="color:#E85D1F;text-decoration:none;">mlrit.ac.in</a>. '
            'A consolidated departmental publications list is pending ingestion.</p>'
        )

    # De-dupe by title
    seen = set()
    deduped = []
    for e in entries:
        if e["title"] in seen:
            continue
        seen.add(e["title"])
        deduped.append(e)

    # Sort by year desc (empty years go last)
    deduped.sort(key=lambda e: int(e["year"]) if e["year"].isdigit() else 0, reverse=True)
    deduped = deduped[:12]

    cards = []
    for e in deduped:
        title = safe(e["title"])
        venue = safe(e["venue"])
        year_h = safe(e["year"]) or "—"
        author = safe(e["author"])
        # Year-attribute for the existing filter widget compat
        year_attr = e["year"] if e["year"].isdigit() else "all"
        cards.append(
            '          <div class="pub-card" data-pub-year="' + year_attr + '">\n'
            '            <div class="pub-card__body">\n'
            f'              <div class="pub-card__title">{title}</div>\n'
            f'              <div class="pub-card__authors">{author}</div>\n'
            f'              <div class="pub-card__journal">{venue}</div>\n'
            '            </div>\n'
            f'            <span class="pub-card__year">{year_h}</span>\n'
            '          </div>'
        )

    pubs_html = (
        '<div class="panel-sub" id="pub-section">Faculty Publications</div>\n'
        '<p>Selected publications from departmental faculty, ingested from the '
        'individual profile pages on mlrit.ac.in.</p>\n'
        '<div class="pub-list" id="pubList">\n'
        + "\n".join(cards) +
        '\n        </div>'
    )
    return pubs_html


# ---- Find the existing publications section to replace ----------------------
# The section spans from <div class="panel-sub" id="pub-section">...</div>
# until the end of the achievements panel (the next </div> at the right depth).
# Simpler approach: replace from "<div class='panel-sub' id='pub-section'>"
# up to the closing of panel-achievements (a `</div>` that is followed by the
# committees TAB comment). We use a non-greedy match.

PUB_SECTION_RE = re.compile(
    r'<div class="panel-sub" id="pub-section">.*?'
    r'(?=\s*</div>\s*<!-- ═══ TAB 6:|\s*</div>\s*<!-- ═══ TAB 6 |\s*</div>\s*<!-- == TAB)',
    re.DOTALL,
)


def patch(name: str, dept: str) -> None:
    p = HERE / name
    text = p.read_text(encoding="utf-8")
    new_block = build_pub_block(dept)
    new_text, n = PUB_SECTION_RE.subn(new_block, text, count=1)
    if n == 0:
        print(f"{name}: FAIL — pub section not located")
        return
    p.write_text(new_text, encoding="utf-8")
    pubs_count = sum(1 for k in PUBS if k.startswith(f"{dept}/") and PUBS[k].get("research"))
    print(f"{name}: replaced pub section ({pubs_count} faculty contribute pubs)")


for dept, name in PAGES.items():
    patch(name, dept)
