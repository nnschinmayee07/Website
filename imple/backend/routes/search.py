"""
Search routes — intelligent query classifier + keyword search across site content.

Query types returned:
  navigate  → { type, url }
  answer    → { type, title, content }
  results   → { type, results: [{title, url, snippet}], corrected?, original? }
"""
import re
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone
from utils.decorators import admin_required

search_bp = Blueprint("search", __name__)

# ── Static navigation map ─────────────────────────────────────────────────
NAVIGATION_MAP = {
    # Departments
    "cse":                      "pages/computer-science-engineering.html",
    "computer science":         "pages/computer-science-engineering.html",
    "computer science engineering": "pages/computer-science-engineering.html",
    "ece":                      "pages/ece.html",
    "electronics":              "pages/ece.html",
    "electronics communication": "pages/ece.html",
    "eee":                      "pages/eee.html",
    "electrical":               "pages/eee.html",
    "mechanical":               "pages/mechanical-engineering.html",
    "mech":                     "pages/mechanical-engineering.html",
    "aeronautical":             "pages/aeronautical-engineering.html",
    "aero":                     "pages/aeronautical-engineering.html",
    "it":                       "pages/it.html",
    "information technology":   "pages/it.html",
    "mba":                      "pages/mba.html",
    "business administration":  "pages/mba.html",
    "cse aiml":                 "pages/cse-aiml.html",
    "aiml":                     "pages/cse-aiml.html",
    "ai ml":                    "pages/cse-aiml.html",
    "artificial intelligence":  "pages/cse-aiml.html",
    "cse ds":                   "pages/cse-ds.html",
    "data science":             "pages/cse-ds.html",
    "cse cs":                   "pages/cse-cs.html",
    "cyber security":           "pages/cse-cs.html",
    "cybersecurity":            "pages/cse-cs.html",
    "csit":                     "pages/csit.html",
    "ai ds":                    "pages/ai-ds.html",
    "csbs":                     "pages/csbs.html",
    "civil":                    "pages/civil.html",
    "freshman":                 "pages/freshman.html",
    # Pages
    "about":                    "pages/about-us.html",
    "about us":                 "pages/about-us.html",
    "admission":                "pages/admissions.html",
    "placements":               "pages/placements.html",
    "placement":                "pages/placements.html",
    "departments":              "pages/departments.html",
    "department":               "pages/departments.html",
    "all departments":          "pages/departments.html",
    "contact":                  "pages/contact.html",
    "contact us":               "pages/contact.html",
    "campus life":              "pages/campus-life.html",
    "campus":                   "pages/campus-life.html",
    "sports":                   "pages/sports.html",
    "events":                   "pages/events.html",
    "research":                 "pages/research.html",
    "iqac":                     "pages/iqac.html",
    "examinations":             "pages/examinations.html",
    "exams":                    "pages/examinations.html",
    "scholarships":             "pages/scholarships.html",
    "scholarship":              "pages/scholarships.html",
    "careers":                  "pages/careers.html",
    "innovation":               "pages/innovation-cell.html",
    "innovation cell":          "pages/innovation-cell.html",
    "virtual tour":             "pages/virtual-tour.html",
    "nirf":                     "pages/nirf-ranked-institution.html",
    "aicte":                    "pages/aicte-approvals.html",
    "aqar":                     "pages/aqar.html",
    "naac":                     "https://naac.mlrit.ac.in/",
    "nba":                      "pages/dcp.html",
    "dcp":                      "pages/dcp.html",
    "blog":                     "pages/blog.html",
    "news":                     "pages/news.html",
    "circulars":                "pages/circulars.html",
    "annual reports":           "pages/annual-reports.html",
    "financial statements":     "pages/financial-statements.html",
    "mandatory disclosures":    "pages/mandatory-disclosures.html",
}

# ── Typo correction ───────────────────────────────────────────────────────

TYPO_DICT = {
    "csee": "cse", "csse": "cse",
    "ecee": "ece", "eece": "ece",
    "eeee": "eee",
    "admissons": "admissions", "admision": "admissions",
    "admisssions": "admissions", "addmissions": "admissions",
    "placments": "placements", "placemants": "placements",
    "placeements": "placements", "placemets": "placements",
    "scholrships": "scholarships", "scholarhips": "scholarships",
    "scolarships": "scholarships",
    "examinatons": "examinations",
    "mechnical": "mechanical", "mechanicl": "mechanical",
    "aeronuatical": "aeronautical", "aeronatical": "aeronautical",
    "reserach": "research", "reasearch": "research",
    "inovation": "innovation", "innovaton": "innovation",
    "hostle": "hostel", "hostl": "hostel",
    "campas": "campus", "campu": "campus",
    "contect": "contact", "contcat": "contact",
    "carees": "careers", "carers": "careers",
    "sporst": "sports", "spors": "sports",
    "placment": "placements",
    "addmision": "admissions",
}

KNOWN_TERMS = [
    "cse", "ece", "eee", "mechanical", "aeronautical", "it", "mba", "aiml",
    "csit", "csbs", "civil", "freshman", "admissions", "placements", "about",
    "contact", "campus", "sports", "events", "research", "iqac", "examinations",
    "scholarships", "careers", "innovation", "hostel", "fees", "nirf", "aicte",
    "naac", "aqar", "circulars", "news", "blog", "virtual tour", "data science",
    "cyber security", "artificial intelligence",
]


def _levenshtein(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            dp[j] = prev[j - 1] if a[i-1] == b[j-1] else 1 + min(prev[j], dp[j-1], prev[j-1])
    return dp[n]


def _correct_typo(raw: str):
    """Return (corrected_query, was_fixed: bool)."""
    q = raw.strip().lower()
    if not q or len(q) < 3:
        return q, False

    # 1. Dictionary lookup
    if q in TYPO_DICT:
        return TYPO_DICT[q], True

    # 2. Levenshtein (only for short single-word queries)
    if len(q) <= 15 and " " not in q:
        best, best_dist = None, 999
        threshold = 1 if len(q) <= 5 else 2
        for term in KNOWN_TERMS:
            if abs(len(term) - len(q)) > 3:
                continue
            d = _levenshtein(q, term)
            if d <= threshold and d < best_dist:
                best_dist = d
                best = term
        if best and best != q:
            return best, True

    return q, False


# ── Static knowledge base (always available, no DB needed) ────────────────
STATIC_KNOWLEDGE = [
    {
        "title": "About MLRIT",
        "url": "pages/about-us.html",
        "keywords": ["about", "mlrit", "history", "established", "autonomous", "jntuh", "kmr", "trust"],
        "content": "MLR Institute of Technology (MLRIT) is located at Dundigal, Hyderabad, Telangana. "
                   "Established in 2005 by the KMR Education Trust headed by Mr. Marri Laxman Reddy. "
                   "Affiliated with JNTUH and granted Autonomous status by UGC in 2015. "
                   "Offers 11 UG and 5 PG courses with NAAC accreditation."
    },
    {
        "title": "Departments at MLRIT",
        "url": "pages/departments.html",
        "keywords": ["departments", "department", "all departments", "branches", "courses offered",
                     "programs", "engineering departments", "what departments"],
        "content": "MLRIT offers 12 departments: CSE, CSE AI&ML, CSE Data Science, CSE Cyber Security, "
                   "CSIT, IT, ECE, EEE, Mechanical Engineering, Aeronautical Engineering, Freshman, and MBA. "
                   "Total annual intake of 1800+ students across UG and PG programs."
    },
    {
        "title": "Admissions",
        "url": "pages/admissions.html",
        "keywords": ["admissions", "admission", "eapcet", "fee", "eligibility", "apply", "enroll", "intake", "mlid"],
        "content": "MLRIT admissions are through EAPCET (MLID code). Eligibility: 10+2 with Physics, Chemistry, Maths. "
                   "Fee structure varies by branch. Lateral entry available for diploma holders. "
                   "Contact admissions office: 1800 572 4363 (Toll Free)."
    },
    {
        "title": "Placements",
        "url": "pages/placements.html",
        "keywords": ["placements", "placement", "recruiters", "package", "salary", "companies", "jobs", "campus", "cognizant", "infosys", "tcs"],
        "content": "MLRIT has excellent placement record. Top recruiters: Cognizant (180 students), Infosys (179), "
                   "Tech Mahindra (64), HCL Tech (30), UST (19), GlobalLogic, Amazon, Virtusa. "
                   "Highest package: 12 LPA. Average package: 4.5 LPA. Training & Placement cell is active."
    },
    {
        "title": "CSE Department",
        "url": "pages/computer-science-engineering.html",
        "keywords": ["cse", "computer science", "engineering", "programming", "software", "coding"],
        "content": "Computer Science and Engineering department at MLRIT offers B.Tech CSE with 180 seats. "
                   "Specializations available in AI&ML, Data Science, Cyber Security. "
                   "State-of-the-art labs, experienced faculty, and strong industry connections."
    },
    {
        "title": "ECE Department",
        "url": "pages/ece.html",
        "keywords": ["ece", "electronics", "communication", "vlsi", "embedded", "signal"],
        "content": "Electronics and Communication Engineering department offers B.Tech ECE with 120 seats. "
                   "Focus areas: VLSI, Embedded Systems, Signal Processing, Communication Systems. "
                   "Well-equipped labs and active research programs."
    },
    {
        "title": "EEE Department",
        "url": "pages/eee.html",
        "keywords": ["eee", "electrical", "electronics", "power", "machines"],
        "content": "Electrical and Electronics Engineering department offers B.Tech EEE with 60 seats. "
                   "Covers power systems, electrical machines, control systems, and renewable energy."
    },
    {
        "title": "Mechanical Engineering",
        "url": "pages/mechanical-engineering.html",
        "keywords": ["mechanical", "mech", "manufacturing", "design", "thermal", "cad", "cam"],
        "content": "Mechanical Engineering department offers B.Tech with 60 seats. "
                   "Covers manufacturing, design, thermal engineering, CAD/CAM, and robotics."
    },
    {
        "title": "Aeronautical Engineering",
        "url": "pages/aeronautical-engineering.html",
        "keywords": ["aeronautical", "aero", "aerospace", "aviation", "aircraft", "flight"],
        "content": "Aeronautical Engineering department offers B.Tech with 60 seats. "
                   "Covers aerodynamics, aircraft structures, propulsion, and avionics."
    },
    {
        "title": "IT Department",
        "url": "pages/it.html",
        "keywords": ["it", "information technology", "networking", "web", "database"],
        "content": "Information Technology department offers B.Tech IT with 60 seats. "
                   "Covers networking, web technologies, database management, and cloud computing."
    },
    {
        "title": "MBA",
        "url": "pages/mba.html",
        "keywords": ["mba", "business", "management", "finance", "marketing", "hr"],
        "content": "Master of Business Administration (MBA) program with 60 seats. "
                   "Specializations in Finance, Marketing, HR, and Operations Management."
    },
    {
        "title": "CSE AI & ML",
        "url": "pages/cse-aiml.html",
        "keywords": ["aiml", "ai ml", "artificial intelligence", "machine learning", "deep learning", "cse aiml"],
        "content": "CSE with specialization in Artificial Intelligence and Machine Learning. "
                   "Covers neural networks, deep learning, NLP, computer vision, and data analytics."
    },
    {
        "title": "CSE Data Science",
        "url": "pages/cse-ds.html",
        "keywords": ["data science", "cse ds", "analytics", "big data", "python", "statistics"],
        "content": "CSE with specialization in Data Science. "
                   "Covers statistical analysis, big data, Python, R, machine learning, and data visualization."
    },
    {
        "title": "CSE Cyber Security",
        "url": "pages/cse-cs.html",
        "keywords": ["cyber security", "cybersecurity", "cse cs", "ethical hacking", "network security", "cryptography"],
        "content": "CSE with specialization in Cyber Security. "
                   "Covers ethical hacking, network security, cryptography, and digital forensics."
    },
    {
        "title": "CSIT Department",
        "url": "pages/csit.html",
        "keywords": ["csit", "computer science information technology"],
        "content": "Computer Science and Information Technology (CSIT) department. "
                   "Combines CS fundamentals with IT applications and networking."
    },
    {
        "title": "Campus Life",
        "url": "pages/campus-life.html",
        "keywords": ["campus", "hostel", "canteen", "library", "facilities", "clubs", "activities"],
        "content": "MLRIT campus spans 15 acres with modern facilities. "
                   "Hostel accommodation available for boys and girls. "
                   "Library with 50,000+ books, digital resources, and e-journals. "
                   "Active student clubs: coding, robotics, cultural, sports."
    },
    {
        "title": "Sports",
        "url": "pages/sports.html",
        "keywords": ["sports", "cricket", "football", "basketball", "athletics", "gym", "fitness"],
        "content": "MLRIT has excellent sports facilities including cricket ground, football field, "
                   "basketball court, volleyball court, and a modern gymnasium. "
                   "Students participate in inter-college and national level competitions."
    },
    {
        "title": "Research",
        "url": "pages/research.html",
        "keywords": ["research", "publications", "projects", "phd", "innovation", "patents"],
        "content": "MLRIT has active research programs with funded projects from DST, AICTE, and industry. "
                   "Faculty publications in reputed journals. PhD programs available. "
                   "Research centers in AI, IoT, and renewable energy."
    },
    {
        "title": "IQAC",
        "url": "pages/iqac.html",
        "keywords": ["iqac", "quality", "accreditation", "naac", "nba", "assessment"],
        "content": "Internal Quality Assurance Cell (IQAC) ensures quality standards. "
                   "MLRIT is NAAC accredited and NBA certified for multiple programs. "
                   "Regular academic audits and quality improvement initiatives."
    },
    {
        "title": "Examinations",
        "url": "pages/examinations.html",
        "keywords": ["examinations", "exams", "timetable", "results", "grading", "cbcs", "schedule"],
        "content": "MLRIT follows JNTUH examination pattern with autonomous modifications. "
                   "CBCS grading system. Mid-term and end-term examinations. "
                   "Results published on university portal. Supplementary exams available."
    },
    {
        "title": "Scholarships",
        "url": "pages/scholarships.html",
        "keywords": ["scholarships", "scholarship", "fee waiver", "financial aid", "merit", "ebc", "sc", "st", "bc"],
        "content": "Various scholarships available: Government scholarships (SC/ST/BC/EBC), "
                   "Merit scholarships, Sports scholarships, and Management scholarships. "
                   "Apply through official scholarship portals. Contact accounts office for details."
    },
    {
        "title": "Innovation Cell",
        "url": "pages/innovation-cell.html",
        "keywords": ["innovation", "startup", "entrepreneurship", "incubation", "hackathon", "ideathon"],
        "content": "MLRIT Innovation Cell promotes entrepreneurship and startup culture. "
                   "Incubation center, hackathons, ideathons, and industry mentorship programs. "
                   "Students have launched successful startups through this initiative."
    },
    {
        "title": "Contact Us",
        "url": "pages/contact.html",
        "keywords": ["contact", "address", "phone", "email", "location", "directions", "map"],
        "content": "MLRIT Address: Dundigal V, Survey No. 444, Dundigal, Gandi Maisama, "
                   "Medchal Malkajgiri, Telangana – 500 043. "
                   "Phone: +91 96522 26061. Toll Free: 1800 572 4363. "
                   "Email: info@mlrinstitutions.ac.in"
    },
    {
        "title": "Careers at MLRIT",
        "url": "pages/careers.html",
        "keywords": ["careers", "jobs", "faculty", "staff", "recruitment", "openings", "apply"],
        "content": "MLRIT regularly recruits qualified faculty and staff. "
                   "Open positions in teaching, research, and administrative roles. "
                   "Send CV to hr@mlrinstitutions.ac.in."
    },
    {
        "title": "Events",
        "url": "pages/events.html",
        "keywords": ["events", "fest", "techfest", "cultural", "seminar", "workshop", "conference"],
        "content": "MLRIT hosts various events including technical fests, cultural programs, "
                   "seminars, workshops, and national conferences throughout the academic year."
    },
    {
        "title": "NIRF Ranking",
        "url": "pages/nirf-ranked-institution.html",
        "keywords": ["nirf", "ranking", "rank", "national institutional ranking"],
        "content": "MLRIT is ranked by NIRF (National Institutional Ranking Framework). "
                   "Consistent improvement in rankings over the years."
    },
    {
        "title": "AICTE Approvals",
        "url": "pages/aicte-approvals.html",
        "keywords": ["aicte", "approval", "accreditation", "recognition", "ugc"],
        "content": "MLRIT is approved by AICTE (All India Council for Technical Education). "
                   "All programs are duly approved and recognized."
    },
    {
        "title": "Virtual Tour",
        "url": "pages/virtual-tour.html",
        "keywords": ["virtual tour", "tour", "360", "campus view", "online tour"],
        "content": "Take a virtual 360-degree tour of the MLRIT campus from anywhere in the world."
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────
def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _score(query_words: list, item: dict) -> int:
    """Return a relevance score for a search item."""
    score = 0
    title_lower = item["title"].lower()
    content_lower = item.get("content", "").lower()
    keywords = [k.lower() for k in item.get("keywords", [])]

    for word in query_words:
        if word in keywords:
            score += 10
        if word in title_lower:
            score += 6
        if word in content_lower:
            score += 2

    # Bonus: full query phrase match
    full_q = " ".join(query_words)
    if full_q in title_lower:
        score += 15
    if full_q in keywords:
        score += 20
    if full_q in content_lower:
        score += 5

    return score


def _snippet(content: str, query_words: list, max_len: int = 160) -> str:
    """Return a short snippet with the first matching sentence."""
    sentences = re.split(r"[.!?]", content)
    for sentence in sentences:
        s_lower = sentence.lower()
        if any(w in s_lower for w in query_words):
            snippet = sentence.strip()
            return snippet[:max_len] + ("…" if len(snippet) > max_len else "")
    return content[:max_len] + ("…" if len(content) > max_len else "")


def _get_db_items(db):
    """Fetch searchable items from MongoDB (content posts + search index)."""
    items = []
    if db is None:
        return items
    try:
        # Content posts
        for doc in db.content.find({}, {"title": 1, "description": 1, "category": 1}):
            items.append({
                "title": doc.get("title", ""),
                "url": "index.html",
                "keywords": [doc.get("category", "")],
                "content": doc.get("description", ""),
            })
        # Admin-defined search index entries
        for doc in db.search_index.find({}):
            items.append({
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "keywords": doc.get("keywords", []),
                "content": doc.get("content", ""),
            })
    except Exception:
        pass
    return items


# ══════════════════════════════════════════════════════════════════════════
# MAIN SEARCH ENDPOINT
# ══════════════════════════════════════════════════════════════════════════

@search_bp.route("/search", methods=["GET"])
def search():
    raw_query = (request.args.get("q") or "").strip()
    if not raw_query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # ── 0. Typo correction ────────────────────────────────────────────────
    corrected_query, was_fixed = _correct_typo(raw_query)
    query = _normalize(corrected_query)
    query_words = query.split()

    # Build base response extras
    correction_meta = {}
    if was_fixed and corrected_query.lower() != raw_query.lower():
        correction_meta = {"corrected": corrected_query, "original": raw_query}

    # ── 1. Navigation check (exact / near-exact match) ────────────────────
    if query in NAVIGATION_MAP:
        return jsonify({"type": "navigate", "url": NAVIGATION_MAP[query], **correction_meta}), 200

    for nav_key, nav_url in NAVIGATION_MAP.items():
        if query == nav_key or (len(query_words) == 1 and query_words[0] == nav_key):
            return jsonify({"type": "navigate", "url": nav_url, **correction_meta}), 200

    for nav_key, nav_url in sorted(NAVIGATION_MAP.items(), key=lambda x: -len(x[0])):
        if query == nav_key and len(nav_key) >= 3:
            return jsonify({"type": "navigate", "url": nav_url, **correction_meta}), 200

    # ── 2. Build combined search corpus ──────────────────────────────────
    db = current_app.db
    all_items = STATIC_KNOWLEDGE + _get_db_items(db)

    # ── 3. Score all items ────────────────────────────────────────────────
    scored = []
    for item in all_items:
        s = _score(query_words, item)
        if s > 0:
            scored.append((s, item))
    scored.sort(key=lambda x: -x[0])

    # ── 4. High-confidence single answer ─────────────────────────────────
    INFO_TRIGGERS = ["fee", "fees", "hostel", "salary", "package", "eligibility",
                     "address", "phone", "email", "contact", "details", "about",
                     "what is", "tell me", "explain", "how", "when", "where"]
    is_info_query = any(t in query for t in INFO_TRIGGERS)

    if is_info_query and scored and scored[0][0] >= 20:
        best = scored[0][1]
        return jsonify({
            "type": "answer",
            "title": best["title"],
            "content": best["content"],
            "url": best["url"],
            "query": corrected_query,
            **correction_meta,
        }), 200

    # ── 5. Return ranked results ──────────────────────────────────────────
    if scored:
        results = []
        seen_urls = set()
        for _, item in scored[:10]:
            url = item["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            results.append({
                "title": item["title"],
                "url": url,
                "snippet": _snippet(item.get("content", ""), query_words),
            })
        return jsonify({
            "type": "results",
            "query": corrected_query,
            "results": results,
            **correction_meta,
        }), 200

    # ── 6. No results ─────────────────────────────────────────────────────
    return jsonify({
        "type": "results",
        "query": corrected_query,
        "results": [],
        **correction_meta,
    }), 200


# ══════════════════════════════════════════════════════════════════════════
# AUTOCOMPLETE ENDPOINT
# ══════════════════════════════════════════════════════════════════════════

@search_bp.route("/search/suggest", methods=["GET"])
def suggest():
    raw = (request.args.get("q") or "").strip().lower()
    if len(raw) < 2:
        return jsonify({"suggestions": []}), 200

    suggestions = set()

    # From navigation map keys
    for key in NAVIGATION_MAP:
        if raw in key:
            suggestions.add(key.title())
        if len(suggestions) >= 8:
            break

    # From static knowledge titles
    for item in STATIC_KNOWLEDGE:
        title = item["title"]
        if raw in title.lower():
            suggestions.add(title)
        if len(suggestions) >= 8:
            break

    return jsonify({"suggestions": sorted(suggestions)[:8]}), 200


# ══════════════════════════════════════════════════════════════════════════
# ADMIN: SEARCH INDEX MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════

@search_bp.route("/api/search-index", methods=["GET"])
@admin_required
def get_search_index():
    db = current_app.db
    if db is None:
        return jsonify({"items": []}), 200
    from bson import ObjectId
    docs = []
    for d in db.search_index.find().sort("createdAt", -1):
        d["id"] = str(d.pop("_id"))
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
        docs.append(d)
    return jsonify({"items": docs}), 200


@search_bp.route("/api/search-index", methods=["POST"])
@admin_required
def add_search_item():
    db = current_app.db
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    body = request.get_json(silent=True) or {}
    title    = (body.get("title") or "").strip()
    url      = (body.get("url") or "").strip()
    content  = (body.get("content") or "").strip()
    keywords = body.get("keywords", [])

    if not title or not url:
        return jsonify({"error": "title and url are required"}), 400

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    doc = {
        "title":     title,
        "url":       url,
        "content":   content,
        "keywords":  keywords,
        "createdAt": datetime.now(timezone.utc),
    }
    result = db.search_index.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    doc["createdAt"] = doc["createdAt"].isoformat()
    return jsonify({"item": doc}), 201


@search_bp.route("/api/search-index/<item_id>", methods=["PUT"])
@admin_required
def update_search_item(item_id):
    db = current_app.db
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    from bson import ObjectId
    try:
        oid = ObjectId(item_id)
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

    body = request.get_json(silent=True) or {}
    keywords = body.get("keywords", None)
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    updates = {}
    for field in ("title", "url", "content"):
        if body.get(field) is not None:
            updates[field] = body[field]
    if keywords is not None:
        updates["keywords"] = keywords
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400

    updates["updatedAt"] = datetime.now(timezone.utc)
    db.search_index.update_one({"_id": oid}, {"$set": updates})
    return jsonify({"message": "Updated"}), 200


@search_bp.route("/api/search-index/<item_id>", methods=["DELETE"])
@admin_required
def delete_search_item(item_id):
    db = current_app.db
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    from bson import ObjectId
    try:
        oid = ObjectId(item_id)
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

    db.search_index.delete_one({"_id": oid})
    return jsonify({"message": "Deleted"}), 200
