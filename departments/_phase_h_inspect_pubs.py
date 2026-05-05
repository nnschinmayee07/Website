"""Phase H — inspect a faculty profile page's publication HTML structure
so we can write a robust parser. Pulls the raw HTML and dumps the table
structure around publication-y headers."""
import urllib.request, ssl, re, sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://mlrit.ac.in/faculty/dr-d-b-k-kamesh/"

ctx = ssl.create_default_context()
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    html = r.read().decode("utf-8", errors="replace")

# Find publication-y headers and dump 30 lines after
markers = [
    r"Journal\s+Publications", r"Conference\s+Publications",
    r"Books?\s+(?:Published|Authored)", r"Patents", r"Awards",
    r"Publications", r"Research\s+Publications",
]
for marker in markers:
    for m in re.finditer(marker, html, re.I):
        start = m.start()
        # Skip matches inside meta tags
        prev = html[max(0, start - 200):start]
        if "<meta" in prev[-200:]:
            continue
        snippet = html[start:start + 1200]
        # Compress whitespace for readability
        snippet = re.sub(r"\s+", " ", snippet)[:800]
        print(f"--- '{m.group()}' at pos {start} ---")
        print(snippet.encode("ascii", errors="replace").decode("ascii"))
        print()
        break  # one per marker
