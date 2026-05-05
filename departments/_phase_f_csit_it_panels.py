"""
Phase F - clean residual CSE-Cyber-Security content from csit.html and it.html.

Replaces:
  1. Cyber-security-themed Achievements panel
     - csit.html: replaced with a clean "data pending" placeholder
     - it.html:   replaced with the achievements actually published on
                  https://mlrit.ac.in/it/
  2. Cyber-security-themed Committees panel (with fabricated DAC/PAC names)
     - both pages get a clean generic committees panel matching the one used
       for aero/ece/eee/mech/freshman in Phase D.
  3. The "Cyber Security Department Handbook" reference inside the Objectives
     tab (Handbook subsection).
  4. The "B.Tech CSE (Cyber Security) programme progressively builds..."
     paragraph at the top of the Academics tab.
  5. Updates the partial-data banner at the top of the Overview to reflect
     what's still pending (publications, syllabus subject details, full
     achievements list).

Idempotent: identifying anchors are removed by the first replacement so
re-running on a clean page is a no-op.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent

# ─── new Achievements panel (CSIT — placeholder) ─────────────────────────────
CSIT_ACHIEVEMENTS_PANEL = """      <!-- ═══ TAB 5: Achievements ═══ -->
      <div class="dept-panel" id="panel-achievements">
        <h2 class="panel-heading">Achievements</h2>

        <div id="achieve-section" class="achieve-grid">
          <div class="card achieve-card" data-achieve>
            <h4>Department-level achievements pending</h4>
            <p>The CSIT department's public landing page on mlrit.ac.in does not currently expose a structured list of student or faculty achievements. Once the department publishes that data, this section will be updated with real awards, certifications, hackathon results, and Roll of Honour entries.</p>
          </div>
        </div>

        <div class="panel-sub" id="honour-section">Roll of Honour</div>
        <p>Top performers and university rank holders from the CSIT department will be listed here as the department publishes results.</p>

        <div class="panel-sub" id="placement-section">Placement Highlights</div>
        <p>Placement statistics for CSIT will be added here in coordination with the Training and Placement Cell.</p>

        <div class="panel-sub" id="intern-section">Internships</div>
        <p>Internship outcomes for CSIT students will be added here as data becomes available.</p>

        <div class="panel-sub" id="pub-section">Faculty Publications</div>
        <p>Faculty publications will be ingested from the individual faculty profile pages on mlrit.ac.in in a future pass.</p>
      </div>
"""

# ─── new Achievements panel (IT — real scraped data) ─────────────────────────
IT_ACHIEVEMENTS_PANEL = """      <!-- ═══ TAB 5: Achievements ═══ -->
      <div class="dept-panel" id="panel-achievements">
        <h2 class="panel-heading">Achievements</h2>

        <div id="achieve-section" class="achieve-grid">
          <div class="card achieve-card" data-achieve>
            <h4>Queen of Neural Hack — Virtusa Coding Competition</h4>
            <p>Ms. CHNV Punya Keerthi (IV B.Tech IT) excelled in the "Neural Hack" coding competition organised by Virtusa, winning the title "The Queen of Neural Hack".</p>
          </div>
          <div class="card achieve-card" data-achieve>
            <h4>Developer Student Clubs — Community Lead</h4>
            <p>Ms. Sreemukhi (III B.Tech IT) was appointed as the community lead for Developer Student Clubs at MLRIT — Google's developer-community programme for university students.</p>
          </div>
          <div class="card achieve-card" data-achieve>
            <h4>UpGrad Internship Selection</h4>
            <p>Ms. Uma Naveena (III B.Tech IT) was selected for the UpGrad Internship Programme.</p>
          </div>
          <div class="card achieve-card" data-achieve>
            <h4>Maa Saraswathi Award 2020 — Faculty Recognition</h4>
            <p>Mrs. IVS Haritha and Mrs. G. Anitha (Asst. Professors) were both conferred the Maa Saraswathi Award 2020 for their contributions to teaching and student mentorship.</p>
          </div>
          <div class="card achieve-card" data-achieve>
            <h4>Faculty PhD Completions — 2020</h4>
            <p>Mrs. K. Neeraja (Assoc. Professor) received her PhD from JNTUH in 2020 and Mr. Vikram Raju (Assoc. Professor) received his PhD from Manipal University in 2020.</p>
          </div>
          <div class="card achieve-card" data-achieve>
            <h4>Coursera Certifications — Department-Wide</h4>
            <p>All faculty members of the IT department have been certified on multiple Coursera courses across software engineering, data, networks, and cloud — sustaining a culture of continuous learning.</p>
          </div>
        </div>

        <div class="panel-sub" id="honour-section">Roll of Honour</div>
        <p>Top performers and university rank holders from the IT department will be listed here as the department publishes annual results.</p>

        <div class="panel-sub" id="placement-section">Placement Highlights</div>
        <p>Placement statistics for IT will be added here in coordination with the Training and Placement Cell.</p>

        <div class="panel-sub" id="intern-section">Internships</div>
        <ul class="achieve-list">
          <li>Ms. Uma Naveena (III B.Tech IT) — selected for the UpGrad Internship Programme.</li>
          <li>Aggregate internship outcomes for the IT department will be added as data becomes available.</li>
        </ul>

        <div class="panel-sub" id="pub-section">Faculty Publications</div>
        <p>Faculty publications will be ingested from the individual faculty profile pages on mlrit.ac.in in a future pass.</p>
      </div>
"""

# ─── new Committees panel (shared, generic) ───────────────────────────────────
GENERIC_COMMITTEES_PANEL = """      <!-- ═══ TAB 6: Committees ═══ -->
      <div class="dept-panel" id="panel-committees">
        <h2 class="panel-heading">Departmental Committees</h2>
        <p>The department operates through several key committees that ensure quality education, curriculum relevance, and continuous improvement in line with NBA and autonomous regulations. These committees comprise senior faculty, industry experts, and academic leaders who guide the department's strategic direction.</p>

        <div class="panel-sub">Departmental Advisory Committee (DAC)</div>
        <div class="card" style="margin-bottom:20px;">
          <h3>DAC</h3>
          <p>The Departmental Advisory Committee advises on curriculum design, infrastructure development, and academic policies. It includes senior faculty, the HOD, and external industry representatives who meet periodically to review and recommend improvements to the programme.</p>
          <a href="assets/DAC formation.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; DAC Formation Document</a>
        </div>

        <div class="panel-sub">Programme Assessment Committee (PAC)</div>
        <div class="card" style="margin-bottom:20px;">
          <h3>PAC</h3>
          <p>The Programme Assessment and Quality Improvement Committee monitors course outcomes, programme outcomes, and attainment levels. It drives the OBE process, reviews CO-PO mapping, and recommends corrective actions to improve educational quality.</p>
          <a href="assets/PAC Member formation.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; PAC Member Formation Document</a>
        </div>

        <div class="panel-sub">Course Expert Team</div>
        <div class="card" style="margin-bottom:20px;">
          <h3>Domain Experts</h3>
          <p>The Course Expert Team comprises domain specialists from industry and academia who review and validate the curriculum content, ensuring alignment with current technology trends and industry requirements.</p>
          <a href="assets/Domain experts formation-CSE.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; Domain Experts Formation Document</a>
        </div>

        <div class="panel-sub">Vision and Mission Process</div>
        <div class="card" style="margin-bottom:20px;">
          <h3>Vision and Mission Committee</h3>
          <p>This committee is responsible for defining, reviewing, and periodically updating the department's vision and mission statements in consultation with all stakeholders &mdash; faculty, students, alumni, parents, and industry partners.</p>
          <a href="assets/1.1&1.1.2- Vision Mission Process.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; Vision Mission Process Document</a>
        </div>
      </div>
"""

# ─── replacement helpers ─────────────────────────────────────────────────────

ACHIEVEMENTS_RE = re.compile(
    r'      <!-- ═══ TAB 5: Achievements ═══ -->\n'
    r'      <div class="dept-panel" id="panel-achievements">.*?\n'
    r'      </div>\n',
    re.DOTALL,
)

COMMITTEES_RE = re.compile(
    r'      <!-- ═══ TAB 6: Committees ═══ -->\n'
    r'      <div class="dept-panel" id="panel-committees">.*?\n'
    r'      </div>\n',
    re.DOTALL,
)

# Handbook subsection cleanup (small, contained — direct text replace)
CSE_CS_HANDBOOK_HEADING = "<h3>Cyber Security Department Handbook</h3>"
CSE_CS_HANDBOOK_DESC = "<p>Department of CSE (Cyber Security) — Academic Year 2025-26</p>"

# Academics-tab introductory paragraph (cyber-security-themed)
CSE_CS_ACADEMICS_INTRO = (
    "<p>The four-year B.Tech CSE (Cyber Security) programme progressively builds students "
    "from foundational mathematics, networking, and programming through to advanced topics in "
    "penetration testing, incident response, cloud security, and threat intelligence — aligned with "
    "EC-Council, NIST, and NASSCOM competency frameworks.</p>"
)

# Updated partial-data banner used in Phase B
OLD_PARTIAL_BANNER = (
    '<div style="background:#F1F8E9;border:1px solid #AED581;border-left:4px solid #1F6B24;'
    'padding:12px 16px;border-radius:8px;margin:0 0 20px;font-size:0.84rem;color:#33691E;">'
    'Overview, vision/mission, PEOs and HOD details have been ingested from mlrit.ac.in. '
    'Faculty profiles, lab list, and achievements are pending Phase&nbsp;C.'
    '</div>'
)

NEW_PARTIAL_BANNER = (
    '<div style="background:#F1F8E9;border:1px solid #AED581;border-left:4px solid #1F6B24;'
    'padding:12px 16px;border-radius:8px;margin:0 0 20px;font-size:0.84rem;color:#33691E;">'
    'Overview, vision/mission, PEOs, HOD details, and the full faculty roster (with photos) have been '
    'ingested from mlrit.ac.in. Lab inventory, publications, and the syllabus subject details are still '
    'pending — they will be added once the source data is available.'
    '</div>'
)

# Per-dept config -------------------------------------------------------------
DEPTS = {
    "csit.html": dict(
        achievements_panel=CSIT_ACHIEVEMENTS_PANEL,
        academics_intro_replacement=(
            "<p>The four-year B.Tech CSIT programme progressively builds students from foundational "
            "mathematics and programming through to applied IT topics including software engineering, "
            "databases, web technologies, networks, and cloud — combining the rigour of Computer Science "
            "with the breadth of Information Technology.</p>"
        ),
        handbook_h3="<h3>CSIT Department Handbook</h3>",
        handbook_p=(
            "<p>Department of Computer Science and Information Technology &mdash; Academic Year 2025-26</p>"
        ),
    ),
    "it.html": dict(
        achievements_panel=IT_ACHIEVEMENTS_PANEL,
        academics_intro_replacement=(
            "<p>The four-year B.Tech Information Technology programme progressively builds students from "
            "foundational mathematics and programming through to applied IT topics including software "
            "engineering, databases, networks, web technologies, and emerging stacks — preparing graduates "
            "for diverse software-engineering roles in industry.</p>"
        ),
        handbook_h3="<h3>IT Department Handbook</h3>",
        handbook_p=(
            "<p>Department of Information Technology &mdash; Academic Year 2025-26</p>"
        ),
    ),
}


def patch(name: str, cfg: dict) -> None:
    p = HERE / name
    text = p.read_text(encoding="utf-8")
    actions = []

    # 1. Achievements panel
    new_text, n = ACHIEVEMENTS_RE.subn(cfg["achievements_panel"], text, count=1)
    if n:
        actions.append("achievements")
    text = new_text

    # 2. Committees panel
    new_text, n = COMMITTEES_RE.subn(GENERIC_COMMITTEES_PANEL, text, count=1)
    if n:
        actions.append("committees")
    text = new_text

    # 3. Handbook subsection text
    if CSE_CS_HANDBOOK_HEADING in text:
        text = text.replace(CSE_CS_HANDBOOK_HEADING, cfg["handbook_h3"], 1)
        actions.append("handbook-h3")
    if CSE_CS_HANDBOOK_DESC in text:
        text = text.replace(CSE_CS_HANDBOOK_DESC, cfg["handbook_p"], 1)
        actions.append("handbook-p")

    # 4. Academics-tab intro paragraph
    if CSE_CS_ACADEMICS_INTRO in text:
        text = text.replace(CSE_CS_ACADEMICS_INTRO, cfg["academics_intro_replacement"], 1)
        actions.append("academics-intro")

    # 5. Partial banner refresh
    if OLD_PARTIAL_BANNER in text:
        text = text.replace(OLD_PARTIAL_BANNER, NEW_PARTIAL_BANNER, 1)
        actions.append("banner")

    p.write_text(text, encoding="utf-8")
    print(f"{name}: {', '.join(actions) if actions else '(no changes)'}")


for fname, cfg in DEPTS.items():
    patch(fname, cfg)
