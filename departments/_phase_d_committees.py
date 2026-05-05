"""
Phase D: add 'Committees' tab + sidebar items + panel to the 5 dept pages
that are missing it (aero, ece, eee, mech, freshman) so all 11 dept pages
share the same tab/sidebar structure as the CSE family.

Idempotent — re-running on a page that already has Committees is a no-op.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = ["aeronautical.html", "ece.html", "eee.html", "mechanical.html", "freshman.html"]

TAB_LINE = '    <a class="dept-tab" data-tab="achievements">Achievements</a>\n'
TAB_INSERT = TAB_LINE + '    <a class="dept-tab" data-tab="committees">Committees</a>\n'

SIDEBAR_INSERT = (
    '    <a class="ds-item" data-ds-tab="committees" data-ds-target="panel-committees"><span class="ds-item__dot"></span><span class="ds-item__label">DAC</span></a>\n'
    '    <a class="ds-item" data-ds-tab="committees" data-ds-target="panel-committees"><span class="ds-item__dot"></span><span class="ds-item__label">PAC</span></a>\n'
    '    <a class="ds-item" data-ds-tab="committees" data-ds-target="panel-committees"><span class="ds-item__dot"></span><span class="ds-item__label">Domain Experts</span></a>\n'
    '  </aside>\n'
)

# Panel HTML — generic across depts; download links point to the shared docx
# files in ../assets/ since dept-specific committee docs are not yet ingested.
PANEL_HTML = """
  <!-- == TAB: Committees == -->
  <div class="dept-panel" id="panel-committees">
    <h2 class="panel-heading">Departmental Committees</h2>
    <p>The department operates through several key committees that ensure quality education, curriculum relevance, and continuous improvement in line with NBA and autonomous regulations. These committees comprise senior faculty, industry experts, and academic leaders who guide the department's strategic direction.</p>

    <div class="panel-sub">Departmental Advisory Committee (DAC)</div>
    <div class="card" style="margin-bottom:20px;">
      <h3>DAC</h3>
      <p>The Departmental Advisory Committee advises on curriculum design, infrastructure development, and academic policies. It includes senior faculty, HOD, and external industry representatives who meet periodically to review and recommend improvements to the programme.</p>
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
      <p>The Course Expert Team comprises domain specialists from industry and academia who review and validate the curriculum content, ensuring alignment with current technology trends and industry requirements. They provide inputs on professional electives, lab experiments, and project topics.</p>
      <a href="assets/Domain experts formation-CSE.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; Domain Experts Formation Document</a>
    </div>

    <div class="panel-sub">Vision and Mission Process</div>
    <div class="card" style="margin-bottom:20px;">
      <h3>Vision and Mission Committee</h3>
      <p>This committee is responsible for defining, reviewing, and periodically updating the department's vision and mission statements in consultation with all stakeholders — faculty, students, alumni, parents, and industry partners. The process follows a structured methodology aligned with NBA requirements.</p>
      <a href="assets/1.1&1.1.2- Vision Mission Process.docx" download style="font-family:'Raleway',sans-serif;font-size:0.75rem;font-weight:700;color:#E85D1F;text-decoration:none;padding:6px 14px;border:1px solid rgba(232,93,31,0.3);border-radius:6px;display:inline-flex;align-items:center;gap:6px;margin-top:12px;">&#8595; Vision Mission Process Document</a>
    </div>
  </div>
"""

PANEL_CLOSE_MARKER = '  </div><!-- .dept-body__panels -->\n'


def patch(path: Path) -> str:
    text = path.read_text(encoding="utf-8")

    if 'data-tab="committees"' in text:
        return "skipped (already has Committees)"

    # 1. Tab
    if TAB_LINE not in text:
        return "FAIL: achievements tab line not found"
    text = text.replace(TAB_LINE, TAB_INSERT, 1)

    # 2. Sidebar (insert before the closing </aside>)
    sidebar_close = '  </aside>\n'
    if sidebar_close not in text:
        return "FAIL: sidebar closing </aside> not found"
    text = text.replace(sidebar_close, SIDEBAR_INSERT, 1)

    # 3. Panel (insert before the dept-body__panels close)
    if PANEL_CLOSE_MARKER not in text:
        return "FAIL: dept-body__panels close marker not found"
    text = text.replace(PANEL_CLOSE_MARKER, PANEL_HTML + "\n" + PANEL_CLOSE_MARKER, 1)

    path.write_text(text, encoding="utf-8")
    return "OK"


for name in TARGETS:
    p = HERE / name
    print(f"{name}: {patch(p)}")
