"""Phase E verification: check that every fcard <img src="images/<dept>/X.jpg">
in the 5 dept HTMLs has a matching file on disk, and report orphans."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
IMG = HERE / "images"
DEPTS = ["csit", "it", "aiml", "cse-cs", "cse-ds"]

PAGES = {
    "csit": "csit.html",
    "it": "it.html",
    "aiml": "aiml.html",
    "cse-cs": "cse-cs.html",
    "cse-ds": "cse-ds.html",
}

for dept in DEPTS:
    page = HERE / PAGES[dept]
    text = page.read_text(encoding="utf-8")
    refs = re.findall(rf'images/{re.escape(dept)}/([a-z0-9-]+)\.jpg', text)
    refs = sorted(set(refs))
    on_disk = sorted({p.stem for p in (IMG / dept).glob("*.jpg")})

    missing = [r for r in refs if r not in on_disk]   # in HTML but no file
    orphan  = [d for d in on_disk if d not in refs]   # file but no HTML reference
    print(f"== {dept}: {len(refs)} refs in HTML, {len(on_disk)} files on disk")
    if missing:
        print(f"   MISSING (no file): {missing}")
    if orphan:
        print(f"   ORPHAN (no HTML ref): {orphan}")
    if not missing and not orphan:
        print("   OK - all matched")
