"""
Phase H — extract publication tables from each faculty's profile page on
mlrit.ac.in. We look for <h3> / <h4> / <strong> headers like
'Research Publications' / 'Journal Publications' / 'Conference Publications'
/ 'Books Published' and parse the immediately-following <table>.

Output: faculty_pubs.json with the schema:
  {
    "<dept>/<our_slug>": {
      "name": "...",
      "url": "...",
      "research": [{"title", "venue", "year"}, ...],
      "books":    [{"title", "publisher", "year"}, ...]
    }
  }

Reuses the PROFILES dict from _phase_g_scrape_profiles.py.
"""
from pathlib import Path
import urllib.request
import ssl
import re
import json
import time
import html as html_mod
import importlib.util
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / "faculty_pubs.json"

# Reuse profile URL map from _phase_g_*.py
spec = importlib.util.spec_from_file_location(
    "_p_g", HERE / "_phase_g_scrape_profiles.py"
)
mod = importlib.util.module_from_spec(spec)
sys.modules["_p_g"] = mod
spec.loader.exec_module(mod)
PROFILES = mod.PROFILES

ssl_ctx = ssl.create_default_context()


def fetch(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  FAIL fetch {url}: {type(e).__name__}: {e}")
        return None


# Strip inline tags inside a cell, leaving plain text
def cell_text(td_html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", td_html)
    t = html_mod.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# Pull rows from a <table>...</table> chunk
TR_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.DOTALL | re.I)
TD_RE = re.compile(r"<td\b[^>]*>(.*?)</td>", re.DOTALL | re.I)


def parse_table(table_html: str) -> list[list[str]]:
    rows = []
    for tr_m in TR_RE.finditer(table_html):
        cells = [cell_text(td_m.group(1)) for td_m in TD_RE.finditer(tr_m.group(1))]
        if cells:
            rows.append(cells)
    return rows


# Find header + next <table> after it
HEADER_PATTERNS = {
    "research": [
        r"Research\s+Publications",
        r"Journal\s+Publications",
        r"International\s+Journal\s+Publications",
        r"International\s+Conference\s+Publications",
        r"Conference\s+Publications",
    ],
    "books": [r"Books?\s+Published", r"Books?\s+Authored", r"\bBooks?\b"],
}


def find_table_after(html: str, header_pat: str) -> str | None:
    """Find the first <table>...</table> appearing after a header that
    matches header_pat. Skip matches inside <meta> tags."""
    for m in re.finditer(header_pat, html, re.I):
        # Skip meta / title hits (description text)
        prev = html[max(0, m.start() - 200):m.start()]
        if "<meta" in prev[-100:] or "<title" in prev[-100:]:
            continue
        # Find next <table>
        rest = html[m.end():]
        t = re.search(r"<table\b[^>]*>(.*?)</table>", rest, re.DOTALL | re.I)
        if t:
            return t.group(1)
    return None


HEADER_HINTS = (
    "title of the article", "title of the paper", "name of the journal",
    "name of the conference", "journal/ conference", "journal name",
    "publisher", "isbn", "year of publication", "volume", "issue", "pages",
    "s. no", "s.no", "sl. no", "sl.no", "url", "url link", "doi",
)


def looks_like_header(cells: list[str]) -> bool:
    joined = " | ".join(c.lower() for c in cells)
    return any(h in joined for h in HEADER_HINTS)


def parse_research_row(cells: list[str]) -> dict | None:
    """Heuristic: row is [S.No, Title, Venue, Vol, Issue, Pages, Year]
    or shorter variants. We pluck title, venue, year."""
    if len(cells) < 3:
        return None
    if looks_like_header(cells):
        return None
    # Year is usually the last numeric-looking 4-digit cell
    year = ""
    for c in reversed(cells):
        m = re.search(r"\b(19|20)\d{2}\b", c)
        if m:
            year = m.group(0)
            break
    title = cells[1] if len(cells) >= 2 else ""
    venue = cells[2] if len(cells) >= 3 else ""
    if not title or len(title) < 5:
        return None
    return {"title": title, "venue": venue, "year": year}


def parse_book_row(cells: list[str]) -> dict | None:
    if len(cells) < 3:
        return None
    if looks_like_header(cells):
        return None
    title = cells[1] if len(cells) >= 2 else ""
    publisher = cells[2] if len(cells) >= 3 else ""
    year = ""
    for c in cells:
        m = re.search(r"\b(19|20)\d{2}\b", c)
        if m:
            year = m.group(0)
            break
    if not title or len(title) < 5:
        return None
    return {"title": title, "publisher": publisher, "year": year}


PUB_TABLE_HINTS = (
    "title", "journal", "conference", "year of publication", "volume",
)


def parse_profile(html: str) -> dict:
    out = {"research": [], "books": []}

    # Research / journal / conference publications — try each pattern,
    # collect from each table found
    seen = set()
    for pat in HEADER_PATTERNS["research"]:
        table = find_table_after(html, pat)
        if not table:
            continue
        for row in parse_table(table):
            entry = parse_research_row(row)
            if entry and entry["title"] not in seen:
                seen.add(entry["title"])
                out["research"].append(entry)
        if out["research"]:
            break

    # Fallback: scan every <table> in the page for publication-shaped rows
    # (column headers mention 'title' AND ('journal' or 'year' or 'volume'))
    if not out["research"]:
        for tm in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, re.DOTALL | re.I):
            tbl = tm.group(1)
            rows = parse_table(tbl)
            if not rows or len(rows) < 2:
                continue
            header = " | ".join(c.lower() for c in rows[0])
            if "title" in header and ("journal" in header or "year" in header or "volume" in header):
                for row in rows[1:]:
                    entry = parse_research_row(row)
                    if entry and entry["title"] not in seen:
                        seen.add(entry["title"])
                        out["research"].append(entry)
            if out["research"]:
                break

    # Books
    seen_b = set()
    for pat in HEADER_PATTERNS["books"]:
        table = find_table_after(html, pat)
        if not table:
            continue
        for row in parse_table(table):
            entry = parse_book_row(row)
            if entry and entry["title"] not in seen_b:
                seen_b.add(entry["title"])
                out["books"].append(entry)
        if out["books"]:
            break

    return out


def main():
    db = {}
    if OUT.exists():
        try:
            db = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            db = {}

    total_ok = total_fail = 0
    for dept, faculty in PROFILES.items():
        print(f"== {dept} ({len(faculty)} faculty) ==")
        for slug, name, url in faculty:
            key = f"{dept}/{slug}"
            if key in db and (db[key].get("research") or db[key].get("books")):
                continue  # already populated
            html = fetch(url)
            if html is None:
                total_fail += 1
                continue
            parsed = parse_profile(html)
            parsed["name"] = name
            parsed["url"] = url
            db[key] = parsed
            total_ok += 1
            time.sleep(0.12)
        OUT.write_text(json.dumps(db, indent=2), encoding="utf-8")
        print(f"  ...checkpoint saved ({len(db)} entries, "
              f"{sum(1 for v in db.values() if v.get('research'))} have pubs)")

    print(f"\nDone. Fetched {total_ok}, failed {total_fail}, total {len(db)}")


if __name__ == "__main__":
    main()
