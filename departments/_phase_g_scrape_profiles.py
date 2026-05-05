"""
Phase G - scrape research areas + publication counts from each faculty's
mlrit.ac.in profile page, save to faculty_profiles.json.

Approach: each profile page (https://mlrit.ac.in/faculty/<wp-slug>/) has a
predictable structure with:
  - "Areas of Interest" / "Research Interests" section
  - Journal/Conference/Book/Patent counts/lists

We fetch the HTML, strip tags, then pattern-match the relevant lines.
"""
from pathlib import Path
import urllib.request
import ssl
import re
import json
import time
import html as html_mod

HERE = Path(__file__).resolve().parent
OUT = HERE / "faculty_profiles.json"

# (our_slug, archive_name, profile_url) — built from the archive-page WebFetches
# Note: our_slug matches the slug used in the dept HTML's fcard image paths.

PROFILES = {
    "csit": [
        ("d-b-k-kamesh",       "Dr. D.B.K. Kamesh",        "https://mlrit.ac.in/faculty/dr-d-b-k-kamesh/"),
        ("p-nishitha",         "Ms .P.Nishitha",           "https://mlrit.ac.in/faculty/p-nishitha-2/"),
        ("d-rajeshwari",       "D.Rajeshwari",             "https://mlrit.ac.in/faculty/d-rajeshwari/"),
        ("a-nirisha",          "A.Nirisha",                "https://mlrit.ac.in/faculty/a-nirisha/"),
        ("p-poojasree",        "P. Poojasree",             "https://mlrit.ac.in/faculty/p-poojasree/"),
        ("rajkumar-bhookya",   "Rajkumar Bhookya",         "https://mlrit.ac.in/faculty/rajkumar-bhookya/"),
        ("devolla-manogna",    "Devolla Manogna",          "https://mlrit.ac.in/faculty/devolla-manogna/"),
        ("s-anudeep",          "S. Anudeep",               "https://mlrit.ac.in/faculty/sadula-anudeep/"),
        ("banothu-seva",       "Banothu Seva",             "https://mlrit.ac.in/faculty/banothu-seva/"),
        ("madhavi-banala",     "Ms.Madhavi Banala",        "https://mlrit.ac.in/faculty/b-madhavi/"),
        ("n-thulasi-chithra",  "N. Thulasi Chithra",       "https://mlrit.ac.in/faculty/n-thulasi-chitra/"),
        ("v-srikanth",         "V. Srikanth",              "https://mlrit.ac.in/faculty/v-srikanth/"),
        ("t-gandhi",           "T. Gandhi",                "https://mlrit.ac.in/faculty/t-gandhi/"),
        ("t-mounika",          "Mrs T. Mounika",           "https://mlrit.ac.in/faculty/mrs-t-mounika/"),
        ("s-parvathi",         "Mrs S.Parvathi",           "https://mlrit.ac.in/faculty/mrs-s-parvathi/"),
        ("n-sandhya",          "N. Sandhya",               "https://mlrit.ac.in/faculty/mrs-n-sandhya-rani/"),
        ("m-srividya",         "Mrs M.Srividya",           "https://mlrit.ac.in/faculty/mrs-m-srividya/"),
        ("d-neelima-priyadarshini", "Ms D.Neelima Priyadarshini", "https://mlrit.ac.in/faculty/mrs-d-neelima/"),
        ("n-vijayasri",        "Ms N.Vijayasri",           "https://mlrit.ac.in/faculty/mrs-ch-vijayasri/"),
        ("s-navya",            "S. Navya",                 "https://mlrit.ac.in/faculty/soleti-navya/"),
    ],
    "it": [
        ("n-v-raja-sekhar-reddy", "Dr.N V Raja Sekhar Reddy", "https://mlrit.ac.in/faculty/dr-n-v-rajasekhar-reddy/"),
        ("dhilli-rao-gorja",   "Dr. Dhilli Rao Gorja",     "https://mlrit.ac.in/faculty/dr-dhilli-rao-gorja/"),
        ("vemuri-nitin",       "Vemuri Nitin",             "https://mlrit.ac.in/faculty/vemuri-nitin/"),
        ("shruthi-patel",      "Mrs Shruthi Patel",        "https://mlrit.ac.in/faculty/mrs-shruti-patil/"),
        ("d-sandeep",          "Mr D. Sandeep",            "https://mlrit.ac.in/faculty/d-sandeep/"),
        ("j-adilakshmi",       "J Adilakshmi",             "https://mlrit.ac.in/faculty/j-adilakshmi/"),
        ("bhasker-boddu",      "Bhasker Boddu",            "https://mlrit.ac.in/faculty/bhasker-boddu/"),
        ("p-laxmaiah",         "P laxmaiah",               "https://mlrit.ac.in/faculty/p-laxmaiah/"),
        ("b-varija",           "B Varija",                 "https://mlrit.ac.in/faculty/b-varija/"),
        ("b-sushma",           "Ms B. Sushma",             "https://mlrit.ac.in/faculty/b-sushma/"),
        ("g-sathyanarayan",    "G Sathyanarayan",          "https://mlrit.ac.in/faculty/g-sathyanarayan/"),
        ("mohd-anwar-ali",     "Mr.Mohd Anwar Ali",        "https://mlrit.ac.in/faculty/mohd-anwar-ali/"),
        ("m-harshini",         "M Harshini",               "https://mlrit.ac.in/faculty/m-harshini/"),
        ("mopur-vijaya-bhaskar-reddy", "Dr. Mopur Vijaya Bhaskar Reddy", "https://mlrit.ac.in/faculty/dr-mopur-vijaya-bhaskar-reddy/"),
    ],
    "aiml": [
        ("kashi-sai-prasad",        "Dr. Kashi Sai Prasad",          "https://mlrit.ac.in/faculty/kashi-sai-prasad/"),
        ("k-varada-rajkumar",       "Dr. K. Varada Rajkumar",        "https://mlrit.ac.in/faculty/dr-k-varada-rajkumar/"),
        ("penubaka-kiran-kumar-reddy", "Dr. Penubaka Kiran Kumar Reddy", "https://mlrit.ac.in/faculty/penubaka-kiran-kumar-reddy/"),
        ("vs-pavan-kumar",          "VS Pavan Kumar",                "https://mlrit.ac.in/faculty/vs-pavan-kumar/"),
        ("bidinamcherla-ammanni",   "Bidinamcherla Ammanni",         "https://mlrit.ac.in/faculty/bidinamcherla-ammanni/"),
        ("sivakrishna-kondaveeti",  "Dr. Sivakrishna Kondaveeti",    "https://mlrit.ac.in/faculty/dr-sivakrishna-kondaveeti/"),
        ("g-sowmya",                "G. Sowmya",                     "https://mlrit.ac.in/faculty/g-sowmya/"),
        ("singanamala-priyanka",    "Singanamala Priyanka",          "https://mlrit.ac.in/faculty/s-priyanka/"),
        ("pasupuleti-pavani",       "Pasupuleti Pavani",             "https://mlrit.ac.in/faculty/pasupuleti-pavani/"),
        ("remedi-sravani",          "Remedi Sravani",                "https://mlrit.ac.in/faculty/remedi-sravani/"),
        ("lakshmi-saritha",         "Lakshmi Saritha",               "https://mlrit.ac.in/faculty/lakshmi-saritha/"),
        ("komari-biksheswara-rao",  "Komari BiksheswaraRao",         "https://mlrit.ac.in/faculty/komari-biksheswararao/"),
        ("e-raghavender",           "E Raghavender",                 "https://mlrit.ac.in/faculty/e-raghavender/"),
        ("seedarla-sandhya-rani",   "Seedarla Sandhya Rani",         "https://mlrit.ac.in/faculty/seedarla-sandhya-rani/"),
        ("shaik-gouse-pasha",       "Shaik Gouse Pasha",             "https://mlrit.ac.in/faculty/shaik-gouse-pasha/"),
        ("m-lakshmi-saranya",       "M Lakshmi Saranya",             "https://mlrit.ac.in/faculty/m-lakshmi-saranya/"),
        ("pottapinjara-babu",       "Pottapinjara Babu",             "https://mlrit.ac.in/faculty/pottapinjara-babu/"),
        ("b-mamatha",               "B.Mamatha",                     "https://mlrit.ac.in/faculty/b-mamatha/"),
        ("t-aswani",                "T Aswani",                      "https://mlrit.ac.in/faculty/t-aswani/"),
        ("ravi-gangadharolla",      "Ravi Gangadharolla",            "https://mlrit.ac.in/faculty/ravi-gangadharolla/"),
        ("pacha-swathi",            "Pacha Swathi",                  "https://mlrit.ac.in/faculty/pacha-swathi/"),
        ("t-nagini",                "T Nagini",                      "https://mlrit.ac.in/faculty/t-nagini/"),
        ("h-ramanjineyulu",         "H Ramanjineyulu",               "https://mlrit.ac.in/faculty/harijana-ramanjineyulu/"),
        ("talari-meena",            "Talari Meena",                  "https://mlrit.ac.in/faculty/talari-meena/"),
        ("nemala-jayasri",          "Nemala Jayasri",                "https://mlrit.ac.in/faculty/nemala-jayasri/"),
        ("gunda-aishwarya",         "Gunda Aishwarya",               "https://mlrit.ac.in/faculty/gunda-aishwarya/"),
        ("p-lokesh-kumar",          "P Lokesh Kumar",                "https://mlrit.ac.in/faculty/p-lokesh-kumar/"),
        ("j-teja",                  "J. Teja",                       "https://mlrit.ac.in/faculty/mr-j-teja/"),
        ("k-anusha",                "Mrs. K. Anusha",                "https://mlrit.ac.in/faculty/mrs-k-anusha/"),
        ("r-akhilesh-reddy",        "Mr.R Akhilesh Reddy",           "https://mlrit.ac.in/faculty/mr-r-akhilesh-reddy/"),
        ("p-sai-kumar",             "P Sai Kumar",                   "https://mlrit.ac.in/faculty/p-sai-kumar/"),
        ("damala-obulesu",          "Damala Obulesu",                "https://mlrit.ac.in/faculty/damala-obulesu/"),
        ("bhaskar-mekala",          "Bhaskar Mekala",                "https://mlrit.ac.in/faculty/bhaskar-mekala/"),
        ("masigari-nagalakshmi",    "Masigari Nagalakshmi",          "https://mlrit.ac.in/faculty/masigiri-nagalakshmi/"),
        ("y-naveen",                "Y. Naveen",                     "https://mlrit.ac.in/faculty/y-naveen/"),
        ("kallam-hemanthi",         "Kallam Hemanthi",               "https://mlrit.ac.in/faculty/kallam-hemanthi/"),
        ("vijay-keerthika",         "Vijay Keerthika",               "https://mlrit.ac.in/faculty/vijay-keerthika/"),
        ("g-umamaheswari",          "G. Umamaheswari",               "https://mlrit.ac.in/faculty/g-umamaheswari/"),
        ("k-jyothsna-reddy",        "K. Jyothsna Reddy",             "https://mlrit.ac.in/faculty/k-jyothsna-reddy/"),
    ],
    "cse-cs": [
        ("p-subhashini",         "Dr. P. Subhashini",        "https://mlrit.ac.in/faculty/dr-p-subhashini/"),
        ("atluri-srujan",        "Mr. Atluri Srujan",        "https://mlrit.ac.in/faculty/mr-atluri-srujan/"),
        ("manisha-kandukuri",    "Manisha Kandukuri",        "https://mlrit.ac.in/faculty/manisha-kandukuri/"),
        ("juttu-suresh",         "Juttu Suresh",             "https://mlrit.ac.in/faculty/juttu-suresh/"),
        ("k-shiva-krishna",      "K.Shiva Krishna",          "https://mlrit.ac.in/faculty/k-shiva-krishna/"),
        ("bochu-sandhya",        "Bochu Sandhya",            "https://mlrit.ac.in/faculty/mrs-kannuri-sandhya/"),
        ("swathi-dendi",         "Mrs. Swathi Dendi",        "https://mlrit.ac.in/faculty/mrs-swathi-dendi/"),
        ("y-anjali-satyavati",   "Mrs. Y Anjali Satyavati",  "https://mlrit.ac.in/faculty/mrs-y-anjali-satyavati/"),
        ("irfan-bagawan",        "Irfan Bagawan",            "https://mlrit.ac.in/faculty/mr-irfan-bagawan/"),
        ("kiran-kumar-reddy-a",  "Kiran Kumar Reddy.A",      "https://mlrit.ac.in/faculty/mr-a-kiran-kumar-reddy/"),
        ("mukku-bhavana",        "Ms. Mukku Bhavana",        "https://mlrit.ac.in/faculty/ms-mukku-bhavana/"),
        ("bolagani-balaji",      "Bolagani Balaji",          "https://mlrit.ac.in/faculty/mr-bolagani-balaji/"),
        ("d-tejaswini",          "Ms. D. Tejaswini",         "https://mlrit.ac.in/faculty/ms-d-tejaswini/"),
        ("ch-sharonu-pushpa",    "Mrs. Ch. Sharonu Pushpa",  "https://mlrit.ac.in/faculty/mrs-ch-sharonu-pushpa/"),
        ("g-umamaheswari",       "G. Umamaheswari",          "https://mlrit.ac.in/faculty/g-uma-maheshwari/"),
    ],
    "cse-ds": [
        ("d-b-k-kamesh",            "Dr. D.B.K. Kamesh",         "https://mlrit.ac.in/faculty/dr-d-b-k-kamesh/"),
        ("p-subhashini",            "Dr. P. Subhashini",         "https://mlrit.ac.in/faculty/dr-p-subhashini/"),
        ("damalla-jyothi",          "Dr. Damalla Jyothi",        "https://mlrit.ac.in/faculty/d-jyothi/"),
        ("veerasekhar-reddy",       "Dr. Veerasekhar reddy",     "https://mlrit.ac.in/faculty/b-veerasekhar-reddy/"),
        ("tahneyath-ahmed",         "Tahneyath Ahmed",           "https://mlrit.ac.in/faculty/tahneyath-ahmed/"),
        ("k-rani",                  "K. Rani",                   "https://mlrit.ac.in/faculty/mrs-kommula-rani/"),
        ("manasaraj",               "Manasaraj",                 "https://mlrit.ac.in/faculty/p-manasaraj/"),
        ("s-shakina",               "S. Shakina",                "https://mlrit.ac.in/faculty/shakina-samuel-mark/"),
        ("sravanthi-anumasula",     "Sravanthi Anumasula",       "https://mlrit.ac.in/faculty/d-sravanthi/"),
        ("d-srivalli",              "D.SRIVALLI",                "https://mlrit.ac.in/faculty/d-srivalli/"),
        ("d-gayathri",              "D.GAYATHRI",                "https://mlrit.ac.in/faculty/d-gayathri/"),
        ("n-baby-rani",             "N.BABY RANI",               "https://mlrit.ac.in/faculty/n-baby-rani/"),
        ("dasari-amulya",           "Dasari Amulya",             "https://mlrit.ac.in/faculty/dasari-amulya/"),
        ("v-divya",                 "V. DIVYA",                  "https://mlrit.ac.in/faculty/v-divya/"),
        ("p-nishitha",              "Ms .P.Nishitha",            "https://mlrit.ac.in/faculty/p-nishitha-2/"),
        ("a-nirisha",               "A.Nirisha",                 "https://mlrit.ac.in/faculty/a-nirisha/"),
        ("s-anudeep",               "S. Anudeep",                "https://mlrit.ac.in/faculty/sadula-anudeep/"),
        ("madhavi-banala",          "Ms.Madhavi Banala",         "https://mlrit.ac.in/faculty/b-madhavi/"),
        ("pallavi-mechineni",       "Mrs. Pallavi Mechineni",    "https://mlrit.ac.in/faculty/mrs-pallavi-mechineni/"),
        ("bochu-sandhya",           "Bochu Sandhya",             "https://mlrit.ac.in/faculty/mrs-kannuri-sandhya/"),
        ("swathi-dendi",            "Mrs. Swathi Dendi",         "https://mlrit.ac.in/faculty/mrs-swathi-dendi/"),
        ("banoth-rajeshwari",       "Mrs. Banoth Rajeshwari",    "https://mlrit.ac.in/faculty/mrs-banoth-rajeshwari/"),
        ("irfan-bagawan",           "Irfan Bagawan",             "https://mlrit.ac.in/faculty/mr-irfan-bagawan/"),
        ("kiran-kumar-reddy-a",     "Kiran Kumar Reddy.A",       "https://mlrit.ac.in/faculty/mr-a-kiran-kumar-reddy/"),
        ("bolagani-balaji",         "Bolagani Balaji",           "https://mlrit.ac.in/faculty/mr-bolagani-balaji/"),
        ("malothu-sindhuja",        "Malothu Sindhuja",          "https://mlrit.ac.in/faculty/mrs-malothu-sindhuja/"),
        ("hasina-nasrin",           "Hasina Nasrin",             "https://mlrit.ac.in/faculty/hasina-nasrin/"),
        ("k-alankruthi",            "Ms. K.Alankruthi",          "https://mlrit.ac.in/faculty/ms-k-alankruthi/"),
        ("b-ravali-reddy",          "Mrs. B.Ravali Reddy",       "https://mlrit.ac.in/faculty/mrs-b-ravali-reddy/"),
        ("mathipogu-ashok-babu",    "Mathipogu Ashok Babu",      "https://mlrit.ac.in/faculty/mr-m-ashok-babu/"),
        ("k-srinija",               "Mrs. K.Srinija",            "https://mlrit.ac.in/faculty/mrs-k-srinija/"),
        ("bhukya-balakrishna",      "Bhukya Balakrishna",        "https://mlrit.ac.in/faculty/bhukya-balakrishna/"),
        ("jangam-nagaraju",         "Jangam Nagaraju",           "https://mlrit.ac.in/faculty/mr-j-nagaraju/"),
        ("mary-navyatha-govindu",   "Mary Navyatha Govindu",     "https://mlrit.ac.in/faculty/mrs-navyatha-ravi/"),
        ("n-thulasi-chithra",       "N. Thulasi Chithra",        "https://mlrit.ac.in/faculty/n-thulasi-chitra/"),
        ("s-parvathi",              "Mrs S.Parvathi",            "https://mlrit.ac.in/faculty/mrs-s-parvathi/"),
        ("n-sandhya",               "N. Sandhya",                "https://mlrit.ac.in/faculty/mrs-n-sandhya-rani/"),
        ("m-srividya",              "Mrs M.Srividya",            "https://mlrit.ac.in/faculty/mrs-m-srividya/"),
        ("d-neelima-priyadarshini", "Ms D.Neelima Priyadarshini","https://mlrit.ac.in/faculty/mrs-d-neelima/"),
        ("n-vijayasri",             "Ms N.Vijayasri",            "https://mlrit.ac.in/faculty/mrs-ch-vijayasri/"),
        ("rowsonara-begum",         "Rowsonara Begum",           "https://mlrit.ac.in/faculty/rowsonara-begum/"),
        ("mohd-anwar-ali",          "Mr.Mohd Anwar Ali",         "https://mlrit.ac.in/faculty/mohd-anwar-ali/"),
        ("b-sushma",                "Ms B. Sushma",              "https://mlrit.ac.in/faculty/b-sushma/"),
        ("d-sandeep",               "Mr D. Sandeep",             "https://mlrit.ac.in/faculty/d-sandeep/"),
        ("s-navya",                 "S. Navya",                  "https://mlrit.ac.in/faculty/soleti-navya/"),
    ],
}

# ── Parsing helpers ─────────────────────────────────────────────────────────


def strip_tags(html: str) -> str:
    """Remove HTML tags and decode entities, preserving line structure."""
    # Replace block tags with newlines so we get sensible line breaks
    html = re.sub(r"</(p|div|li|tr|h[1-6])>", "\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", "", html)
    text = html_mod.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text


# Strict label patterns — labels must appear as a standalone heading-like line.
# Each pattern matches the label followed by a value on the SAME line or NEXT line.
AREAS_LABEL_RE = re.compile(
    r"^[ \t]*(?:areas?\s+of\s+(?:specialization|specialisation|interest|research)|"
    r"research\s+interests?|areas?\s+of\s+expertise|domain\s+of\s+expertise)\s*[:\-]?\s*\n+\s*(.+?)\s*\n",
    re.I | re.M,
)

# Same-line variant ("Areas of Interest: foo, bar")
AREAS_INLINE_RE = re.compile(
    r"^[ \t]*(?:areas?\s+of\s+(?:specialization|specialisation|interest|research)|"
    r"research\s+interests?|areas?\s+of\s+expertise|domain\s+of\s+expertise)\s*[:\-]\s*(.+?)\s*$",
    re.I | re.M,
)

QUAL_LABEL_RE = re.compile(
    r"^[ \t]*(?:qualifications?|qualification\s+details?|highest\s+qualification|education(?:al\s+qualifications?)?)\s*[:\-]?\s*\n+\s*(.+?)\s*\n",
    re.I | re.M,
)

# Counts must be near a "publications" / "research output" context — strict
# label-on-own-line pattern, value on next line.
COUNT_RE = re.compile(
    r"^[ \t]*(journals?|conferences?|books?|patents?|awards?)\s*[:\-]?\s*\n+\s*(\d{1,4})\s*\n",
    re.I | re.M,
)

# Department names that aren't useful as "research areas"
DEPT_NOISE = {
    "cse", "ece", "eee", "it", "csit", "ds", "cs", "aiml", "aero", "mech", "mba",
    "computer science", "electronics", "civil", "mathematics", "physics", "english",
    "mechanical", "n/a", "na", "none", "-", "—",
}


def parse_profile(html: str) -> dict:
    text = strip_tags(html)
    out = {"areas": [], "qual": "", "counts": {}}

    # --- areas / research interests (label on own line, value on next line OR inline)
    raw = None
    m = AREAS_LABEL_RE.search(text)
    if m:
        raw = m.group(1)
    else:
        m2 = AREAS_INLINE_RE.search(text)
        if m2:
            raw = m2.group(1)
    if raw:
        raw = raw.strip().rstrip(".").strip()
        # Split on commas / semicolons / "and" / multiple spaces
        parts = re.split(r"\s*[,;]\s*|\s+and\s+", raw)
        parts = [p.strip(" .;:-–—") for p in parts if p]
        # Drop very short or noise tokens
        parts = [p for p in parts if len(p) >= 3 and p.lower() not in DEPT_NOISE]
        out["areas"] = parts[:6]  # cap to keep cards readable

    # --- qualification
    m = QUAL_LABEL_RE.search(text)
    if m:
        q = m.group(1).strip().rstrip(".")
        # Filter sentence-fragment captures — must look like a degree
        if re.search(r"\b(Ph\.?D|M\.?Tech|M\.?E\b|B\.?Tech|B\.?E\b|M\.?Sc|B\.?Sc|MBA|MCA|BCA)\b", q, re.I):
            out["qual"] = q[:200]

    # --- numeric counts of pubs/books/etc (strict, label on own line)
    for label, n in COUNT_RE.findall(text):
        key = label.lower().rstrip("s")
        out["counts"][key] = max(int(n), out["counts"].get(key, 0))

    return out


# ── Fetcher ─────────────────────────────────────────────────────────────────

ssl_ctx = ssl.create_default_context()


def fetch(url: str, retries: int = 1) -> str | None:
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(0.4)
    print(f"  FAIL fetching {url}: {last}")
    return None


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
        for slug, archive_name, url in faculty:
            key = f"{dept}/{slug}"
            if key in db and db[key].get("areas"):
                # already scraped successfully — skip
                continue
            html = fetch(url)
            if html is None:
                total_fail += 1
                continue
            parsed = parse_profile(html)
            parsed["name"] = archive_name
            parsed["url"] = url
            db[key] = parsed
            total_ok += 1
            # be polite — small delay
            time.sleep(0.15)

        # checkpoint after each dept
        OUT.write_text(json.dumps(db, indent=2), encoding="utf-8")
        print(f"  ...checkpoint saved ({len(db)} entries)")

    print(f"\nDone. Fetched {total_ok}, failed {total_fail}, total in db {len(db)}")


def main_subset(only: list[str] | None = None):
    """Run main but only for the depts in `only`."""
    global PROFILES
    if only:
        PROFILES = {k: v for k, v in PROFILES.items() if k in only}
    main()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main_subset(sys.argv[1].split(","))
    else:
        main()
