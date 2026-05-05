"""Debug helper: fetch one profile page and dump the relevant text region
so we can craft a better Areas/Qualifications parser."""
import urllib.request, ssl, re, html as html_mod, sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://mlrit.ac.in/faculty/dr-d-b-k-kamesh/"

ctx = ssl.create_default_context()
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    html = r.read().decode("utf-8", errors="replace")


def strip_tags(html: str) -> str:
    html = re.sub(r"</(p|div|li|tr|h[1-6])>", "\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", "", html)
    text = html_mod.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text


text = strip_tags(html)

# Show 30 lines around any line that mentions "interest" or "areas"
lines = text.split("\n")
for i, line in enumerate(lines):
    if re.search(r"interest|areas?\s+of|specialization|qualif|research", line, re.I):
        for j in range(max(0, i - 1), min(len(lines), i + 4)):
            tag = ">>>" if j == i else "   "
            print(f"{tag} L{j:>4}: {lines[j].strip()[:200]}")
        print("---")
