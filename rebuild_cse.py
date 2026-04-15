import re

# Read existing data from CSE
with open('c:/mlr/homepage/departments/cse.html', encoding='utf-8') as f:
    old = f.read()

# Extract faculty lane HTML
m = re.search(r'(<div class="faculty-lane">.*?</div>\s*</section>)', old, re.DOTALL)
faculty_html = m.group(1) if m else '<div class="faculty-lane">No faculty data</div>'
# Strip the </section> at the end
faculty_html = re.sub(r'\s*</section>\s*$', '', faculty_html)

# Extract publications HTML (just the cards)
m = re.search(r'(<div class="pub-filters".*?</div>\s*</section>)', old, re.DOTALL)
pubs_html = m.group(1) if m else ''
pubs_html = re.sub(r'\s*</section>\s*$', '', pubs_html)

# Extract achievements HTML (just the cards)
m = re.search(r'(<div class="achieve-grid">.*?</div>\s*</section>)', old, re.DOTALL)
achieve_html = m.group(1) if m else ''
achieve_html = re.sub(r'\s*</section>\s*$', '', achieve_html)

# Extract internship HTML
m = re.search(r'(<div class="intern-stats">.*?<p class="intern-note">.*?</p>)', old, re.DOTALL)
intern_html = m.group(1) if m else ''

# Extract JS data blocks
programs_js = open('c:/mlr/cse_programs.js').read()
subjects_js = open('c:/mlr/cse_subjects.js').read()
urls_js = open('c:/mlr/cse_urls.js').read()

# Build new file
html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CSE Department — MLRIT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&family=Raleway:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/navbar.css" />
  <link rel="stylesheet" href="../css/main.css" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', sans-serif; background: #F4F1EA; color: #3A3A3A; line-height: 1.7; }

    /* ── Department Hero ── */
    .dept-hero {
      background: linear-gradient(135deg, #0D3320, #18453B);
      padding: 60px 48px 28px;
      position: relative; overflow: hidden;
    }
    .dept-hero::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 70% 30%, rgba(232,93,31,0.12), transparent 60%); }
    .dept-hero__eyebrow { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 8px; position: relative; z-index: 1; }
    .dept-hero__title { font-family: 'Playfair Display', serif; font-size: clamp(1.6rem, 3vw, 2.6rem); font-weight: 700; color: #fff; position: relative; z-index: 1; }

    /* ── Tab Navigation ── */
    .dept-tabs {
      background: #0B0F1A;
      display: flex; gap: 0; overflow-x: auto;
      border-bottom: 3px solid #18453B;
      position: sticky; top: 0; z-index: 40;
    }
    .dept-tabs::-webkit-scrollbar { height: 0; }
    .dept-tab {
      font-family: 'Raleway', sans-serif; font-size: 0.78rem; font-weight: 700;
      color: rgba(255,255,255,0.5); text-decoration: none;
      padding: 14px 24px; white-space: nowrap; cursor: pointer;
      border-bottom: 3px solid transparent; margin-bottom: -3px;
      transition: color 0.25s, border-color 0.25s;
    }
    .dept-tab:hover { color: rgba(255,255,255,0.8); }
    .dept-tab.is-active { color: #fff; border-bottom-color: #E85D1F; }

    /* ── Tab Panels ── */
    .dept-panel { display: none; padding: 48px; max-width: 1100px; margin: 0 auto; }
    .dept-panel.is-active { display: block; animation: fadeIn 0.35s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

    .panel-heading {
      font-family: 'Playfair Display', serif; font-size: clamp(1.6rem, 2.5vw, 2.2rem);
      font-weight: 700; color: #0B0F1A; margin-bottom: 28px; line-height: 1.2;
    }
    .panel-heading::after { content: ''; display: block; width: 48px; height: 3px; background: #E85D1F; margin-top: 12px; border-radius: 2px; }

    .panel-sub { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 800; color: #18453B; text-transform: uppercase; letter-spacing: 0.1em; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 2px solid rgba(24,69,59,0.12); }

    p { font-size: 0.95rem; color: #3A3A3A; max-width: 780px; margin-bottom: 14px; line-height: 1.8; }

    /* ── Cards ── */
    .card { background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    .card h3 { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.15rem; color: #0B0F1A; margin-bottom: 10px; }
    .card p { font-size: 0.9rem; color: #3A3A3A; line-height: 1.7; }

    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    .three-col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .card--accent { border-top: 3px solid #18453B; }

    .peo-num { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: #18453B; margin-bottom: 10px; }

    /* ── OBE Section ── */
    .obe-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 20px; }
    .obe-col h4 { font-family: 'Raleway', sans-serif; font-size: 0.82rem; font-weight: 800; color: #18453B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
    .obe-list { list-style: none; padding: 0; }
    .obe-list li { font-size: 0.88rem; color: #444; padding: 8px 0; border-bottom: 1px solid rgba(0,0,0,0.05); padding-left: 16px; position: relative; }
    .obe-list li::before { content: ''; position: absolute; left: 0; top: 14px; width: 6px; height: 6px; border-radius: 50%; background: #E85D1F; }

    /* ── Course Catalog ── */
    .catalog-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }
    .catalog-item { background: #fff; border-radius: 10px; padding: 16px 20px; box-shadow: 0 1px 8px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; border-left: 3px solid #18453B; }
    .catalog-item:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    .catalog-item__icon { font-size: 1.2rem; }
    .catalog-item__text { font-family: 'Raleway', sans-serif; font-size: 0.82rem; font-weight: 700; color: #0B0F1A; }
    .catalog-item__sub { font-size: 0.68rem; color: #888; font-weight: 500; display: block; margin-top: 2px; }

    /* ── Syllabus ── */
    .syllabus-pdfs { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; }
    .syllabus-pdfs a { font-family: 'Raleway', sans-serif; font-size: 0.75rem; font-weight: 700; color: #18453B; text-decoration: none; padding: 8px 16px; border-radius: 8px; background: rgba(24,69,59,0.08); transition: all 0.2s; display: inline-flex; align-items: center; gap: 6px; }
    .syllabus-pdfs a:hover { background: #18453B; color: #fff; }
    .syllabus-pdfs a::before { content: '\\2913'; font-size: 0.9rem; }

    .pill-row { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .pill { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.06em; padding: 10px 22px; border-radius: 24px; border: 2px solid rgba(24,69,59,0.25); background: transparent; color: #3A3A3A; cursor: pointer; transition: all 0.25s; }
    .pill:hover { border-color: #E85D1F; color: #E85D1F; }
    .pill.is-active { background: #18453B; border-color: #18453B; color: #fff; }
    .subject-list { max-width: 700px; opacity: 0; transform: translateY(10px); transition: opacity 0.35s, transform 0.35s; }
    .subject-list.is-visible { opacity: 1; transform: translateY(0); }
    .subject-row { display: flex; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(0,0,0,0.06); gap: 16px; cursor: pointer; }
    .subject-row:last-child { border-bottom: none; }
    .subject-num { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.72rem; color: #18453B; width: 28px; flex-shrink: 0; }
    .subject-name { flex: 1; font-size: 0.92rem; color: #3A3A3A; }
    .subject-pdf { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 4px 12px; border: 1px solid rgba(232,93,31,0.3); border-radius: 6px; white-space: nowrap; transition: all 0.2s; }
    .subject-pdf:hover { background: #E85D1F; color: #fff; }
    .subject-units { max-height: 0; overflow: hidden; transition: max-height 0.4s; padding: 0 0 0 44px; }
    .subject-row.is-expanded + .subject-units { max-height: 300px; }
    .subject-units ol { list-style: none; padding: 8px 0 12px; counter-reset: unit; }
    .subject-units li { font-size: 0.82rem; color: #555; padding: 4px 0; counter-increment: unit; }
    .subject-units li::before { content: 'Unit ' counter(unit) ': '; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.7rem; color: #18453B; }
    .subject-toggle { font-size: 0.7rem; color: #888; margin-left: 8px; transition: transform 0.3s; display: inline-block; }
    .subject-row.is-expanded .subject-toggle { transform: rotate(90deg); color: #E85D1F; }

    /* ── Faculty Memory Lane ── */
    .faculty-lane { display: flex; gap: 28px; overflow-x: auto; padding: 20px 0 32px; scroll-behavior: smooth; -webkit-overflow-scrolling: touch; }
    .faculty-lane::-webkit-scrollbar { height: 6px; }
    .faculty-lane::-webkit-scrollbar-track { background: rgba(0,0,0,0.04); border-radius: 3px; }
    .faculty-lane::-webkit-scrollbar-thumb { background: rgba(24,69,59,0.2); border-radius: 3px; }
    .faculty-item { flex-shrink: 0; width: 120px; text-align: center; position: relative; cursor: pointer; }
    .faculty-item__photo { width: 90px; height: 90px; border-radius: 50%; margin: 0 auto 10px; background: linear-gradient(135deg, #2A2F40, #3A4050); overflow: hidden; border: 3px solid transparent; transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s; display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.3); font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 1.1rem; }
    .faculty-item__photo img { width: 100%; height: 100%; object-fit: cover; }
    .faculty-item:hover .faculty-item__photo { border-color: #E85D1F; transform: scale(1.08); box-shadow: 0 4px 20px rgba(232,93,31,0.25); }
    .faculty-item__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.72rem; color: #0B0F1A; line-height: 1.3; margin-bottom: 2px; }
    .faculty-item__role { font-family: 'Raleway', sans-serif; font-size: 0.62rem; color: #888; font-weight: 600; letter-spacing: 0.04em; }
    .faculty-popup { display: none; position: absolute; bottom: calc(100% + 12px); left: 50%; transform: translateX(-50%); width: 300px; background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); padding: 20px; z-index: 50; text-align: left; border-top: 3px solid #18453B; }
    .faculty-popup::after { content: ''; position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%); width: 16px; height: 8px; background: #fff; clip-path: polygon(0 0, 100% 0, 50% 100%); }
    .faculty-item:hover .faculty-popup { display: block; animation: popIn 0.25s ease; }
    @keyframes popIn { from { opacity: 0; transform: translateX(-50%) translateY(6px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
    .faculty-popup__name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1rem; color: #0B0F1A; margin-bottom: 4px; }
    .faculty-popup__role { font-size: 0.72rem; color: #E85D1F; font-weight: 600; margin-bottom: 10px; }
    .faculty-popup__detail { font-size: 0.78rem; color: #555; margin-bottom: 4px; line-height: 1.4; }
    .faculty-popup__detail strong { color: #18453B; font-weight: 700; }
    .faculty-popup__tag { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 0.62rem; font-weight: 700; color: #18453B; background: rgba(24,69,59,0.08); padding: 2px 8px; border-radius: 4px; margin: 2px 2px 0 0; }
    .faculty-popup__papers { margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.06); }
    .faculty-popup__papers-title { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.68rem; color: #18453B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
    .faculty-popup__paper { font-size: 0.72rem; color: #555; line-height: 1.4; margin-bottom: 4px; padding-left: 10px; border-left: 2px solid rgba(232,93,31,0.3); }

    /* ── Achievements ── */
    .achieve-grid { display: grid; grid-template-columns: 1fr; gap: 16px; max-width: 700px; }
    .achieve-card { border-left: 3px solid #E85D1F; cursor: pointer; }
    .achieve-card h4 { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 6px; }
    .achieve-card p { font-size: 0.88rem; color: #555; margin-bottom: 0; max-height: 0; overflow: hidden; transition: max-height 0.4s, margin 0.4s; }
    .achieve-card.is-expanded p { max-height: 200px; margin-bottom: 8px; }
    .achieve-toggle { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 6px; display: inline-block; }

    /* ── Publications ── */
    .pub-filters { display: flex; gap: 8px; margin-bottom: 28px; flex-wrap: wrap; }
    .pub-filter { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.75rem; letter-spacing: 0.06em; padding: 7px 18px; border-radius: 20px; border: 2px solid rgba(24,69,59,0.25); background: transparent; color: #3A3A3A; cursor: pointer; transition: all 0.25s; }
    .pub-filter:hover { border-color: #E85D1F; color: #E85D1F; }
    .pub-filter.is-active { background: #18453B; border-color: #18453B; color: #fff; }
    .pub-list { display: flex; flex-direction: column; gap: 16px; max-width: 780px; position: relative; }
    .pub-card { background: #fff; border-radius: 12px; padding: 24px 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-left: 3px solid #18453B; display: flex; align-items: flex-start; gap: 20px; transition: opacity 0.35s, transform 0.35s; }
    .pub-card.is-hidden { opacity: 0; transform: scale(0.95); position: absolute; pointer-events: none; }
    .pub-card__body { flex: 1; }
    .pub-card__title { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 6px; line-height: 1.4; }
    .pub-card__authors { font-size: 0.82rem; color: #888; margin-bottom: 4px; }
    .pub-card__journal { font-size: 0.82rem; color: #E85D1F; font-style: italic; }
    .pub-card__year { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.68rem; letter-spacing: 0.1em; color: #fff; background: #18453B; padding: 4px 10px; border-radius: 10px; flex-shrink: 0; align-self: flex-start; margin-top: 2px; }
    .pub-tag { display: inline-block; margin-top: 8px; font-family: 'Raleway', sans-serif; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #18453B; background: rgba(24,69,59,0.08); padding: 3px 10px; border-radius: 4px; }

    /* ── Internships ── */
    .intern-stats { display: flex; gap: 20px; margin-bottom: 36px; flex-wrap: wrap; }
    .stat-card { background: #fff; border-radius: 12px; padding: 24px 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center; flex: 1; min-width: 140px; }
    .stat-card__num { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.8rem; color: #18453B; line-height: 1; margin-bottom: 6px; }
    .stat-card__label { font-family: 'Raleway', sans-serif; font-weight: 600; font-size: 0.75rem; color: #888; letter-spacing: 0.06em; text-transform: uppercase; }
    .intern-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px; }
    .intern-card { perspective: 600px; background: none; box-shadow: none; border: none; padding: 0; height: 100px; }
    .intern-card__inner { position: relative; width: 100%; height: 100%; transition: transform 0.5s; transform-style: preserve-3d; }
    .intern-card:hover .intern-card__inner { transform: rotateY(180deg); }
    .intern-card__front, .intern-card__back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    .intern-card__front { background: #fff; }
    .intern-card__back { background: #18453B; transform: rotateY(180deg); color: #fff; }
    .intern-card__back-num { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.4rem; margin-bottom: 4px; }
    .intern-card__back-label { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.7; }
    .intern-card__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 4px; }
    .intern-card__type { font-size: 0.75rem; color: #888; font-weight: 500; }
    .intern-note { font-size: 0.88rem; color: #666; font-style: italic; max-width: 700px; }

    @media (max-width: 768px) {
      .dept-panel { padding: 32px 20px; }
      .two-col, .three-col, .obe-grid, .catalog-grid { grid-template-columns: 1fr; }
      .faculty-lane { gap: 16px; }
      .faculty-popup { width: 260px; }
    }
  </style>
</head>
<body>

  <!-- Main Header -->
  <header class="site-header">
    <div class="masthead">
      <div class="container masthead__inner">
        <a href="../index.html" class="masthead__logo" aria-label="MLRIT Home">
          <img src="../mlrit-logo-transparent.png" alt="MLRIT Logo" />
        </a>
        <div class="masthead__tagline">
          <span>Marri Laxman Reddy Institute of Technology</span>
        </div>
        <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      </div>
    </div>
  </header>

  <!-- Department Hero -->
  <div class="dept-hero">
    <div class="dept-hero__eyebrow">B.Tech &middot; Computer Science &amp; Engineering</div>
    <div class="dept-hero__title">Department of Computer Science &amp; Engineering</div>
  </div>

  <!-- Tab Navigation -->
  <nav class="dept-tabs" id="deptTabs">
    <a class="dept-tab is-active" data-tab="overview">Overview</a>
    <a class="dept-tab" data-tab="objectives">Objectives &amp; OBE</a>
    <a class="dept-tab" data-tab="faculty">Faculty Profiles</a>
    <a class="dept-tab" data-tab="academics">Academics &amp; Syllabus</a>
    <a class="dept-tab" data-tab="achievements">Achievements &amp; Research</a>
  </nav>

  <!-- ══════════════════════════════════════ -->
  <!-- TAB 1: Overview (Overview + Vision & Mission) -->
  <!-- ══════════════════════════════════════ -->
  <div class="dept-panel is-active" id="panel-overview">
    <h2 class="panel-heading">About the Department</h2>
    <p>The B.Tech program in Computer Science and Engineering was started in 2005 with an intake of 60, increased to 120 in 2007, 180 in 2012, 240 in 2013, and 840 in 2024. An additional 10% seats are under the lateral entry scheme. The department also offers M.Tech in CSE from 2011.</p>
    <p>The B.Tech (CSE) program has been accredited by the National Board of Accreditation (NBA) since 2008. The department has 12 well-equipped laboratories with 400+ computers, and industry MOUs with Boeing, Cyient, Tata Technologies, EPAM Systems, and Virtusa.</p>

    <div class="panel-sub">Vision &amp; Mission</div>
    <div class="two-col">
      <div class="card card--accent">
        <h3>Vision</h3>
        <p>Promote Innovation-centric education to produce globally competent graduates in Computer Science and Engineering education and research capable of building a strong and developed nation.</p>
      </div>
      <div class="card card--accent">
        <h3>Mission</h3>
        <p>Strengthen the department interaction with Multi National Companies to enhance graduate technological advancement skills and research capabilities.</p>
      </div>
    </div>
  </div>

  <!-- ══════════════════════════════════════ -->
  <!-- TAB 2: Objectives & OBE -->
  <!-- ══════════════════════════════════════ -->
  <div class="dept-panel" id="panel-objectives">
    <h2 class="panel-heading">Programme Educational Objectives</h2>
    <div class="three-col">
      <div class="card card--accent" style="text-align:center;">
        <div class="peo-num">PEO 1</div>
        <p>Graduates will have a globally competent professional career in the software industry.</p>
      </div>
      <div class="card card--accent" style="text-align:center;">
        <div class="peo-num">PEO 2</div>
        <p>Graduates will pursue higher education and research.</p>
      </div>
      <div class="card card--accent" style="text-align:center;">
        <div class="peo-num">PEO 3</div>
        <p>Graduates will have entrepreneur skills to solve societal problems.</p>
      </div>
    </div>

    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col">
        <h4>B.Tech</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>
      <div class="obe-col">
        <h4>M.Tech</h4>
        <ul class="obe-list">
          <li>Educational Objectives &amp; Outcomes</li>
          <li>OBE Process Manual</li>
          <li>Course Outcomes Description Booklets</li>
          <li>Course Outcomes (COs) Attainment</li>
          <li>Program Outcomes (POs) Attainment</li>
        </ul>
      </div>
    </div>

    <div class="panel-sub">Handbook</div>
    <div class="card" style="max-width:500px;">
      <h3>CSE Department Handbook</h3>
      <p>Computer Science and Engineering — Academic Year 2025–26</p>
    </div>
  </div>

  <!-- ══════════════════════════════════════ -->
  <!-- TAB 3: Faculty Profiles -->
  <!-- ══════════════════════════════════════ -->
  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Scroll to explore 64 faculty members. Hover for research details, click for full profile.</p>
''' + '    ' + faculty_html + '''
  </div>

  <!-- ══════════════════════════════════════ -->
  <!-- TAB 4: Academics & Syllabus -->
  <!-- ══════════════════════════════════════ -->
  <div class="dept-panel" id="panel-academics">
    <h2 class="panel-heading">Academics &amp; Syllabus</h2>

    <div class="panel-sub">Course Catalog</div>
    <div class="catalog-grid">
      <a href="https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_CSE-Syllabus.pdf" target="_blank" class="catalog-item">
        <span class="catalog-item__icon">📄</span>
        <div><span class="catalog-item__text">B.Tech Course Catalog — R25</span><span class="catalog-item__sub">Latest regulation (2025 batch onwards)</span></div>
      </a>
      <a href="https://mlrit.ac.in/curriculum/cse-r22-ug-syllabus/" target="_blank" class="catalog-item">
        <span class="catalog-item__icon">📄</span>
        <div><span class="catalog-item__text">B.Tech Course Catalog — R22</span><span class="catalog-item__sub">2022 regulation</span></div>
      </a>
      <a href="https://mlrit.ac.in/curriculum/cse-mlr20-ug-syllabus/" target="_blank" class="catalog-item">
        <span class="catalog-item__icon">📄</span>
        <div><span class="catalog-item__text">B.Tech Course Catalog — MLR20</span><span class="catalog-item__sub">2020 regulation</span></div>
      </a>
      <a href="https://mlrit.ac.in/curriculum/cse-m-tech-r22-syllabus/" target="_blank" class="catalog-item">
        <span class="catalog-item__icon">📄</span>
        <div><span class="catalog-item__text">M.Tech Course Catalog — R22</span><span class="catalog-item__sub">Postgraduate regulation</span></div>
      </a>
      <a href="https://mlrit.ac.in/curriculum/cse-m-tech-mlr20-syllabus/" target="_blank" class="catalog-item">
        <span class="catalog-item__icon">📄</span>
        <div><span class="catalog-item__text">M.Tech Course Catalog — MLR20</span><span class="catalog-item__sub">Postgraduate regulation</span></div>
      </a>
    </div>

    <div class="panel-sub">Semester-wise Syllabus Explorer</div>
    <p style="font-style:italic; color:#666; margin-bottom:20px;">Select programme, year and semester to browse subjects. Click a subject to see unit-wise topics.</p>

    <div class="pill-row" id="progPills">
      <button class="pill is-active" data-prog="btech">B.Tech</button>
      <button class="pill" data-prog="mtech">M.Tech</button>
    </div>
    <div class="pill-row" id="yearPills"></div>
    <div class="pill-row" id="semPills" style="display:none;"></div>
    <div class="subject-list" id="subjectList"></div>
  </div>

  <!-- ══════════════════════════════════════ -->
  <!-- TAB 5: Achievements & Research -->
  <!-- ══════════════════════════════════════ -->
  <div class="dept-panel" id="panel-achievements">
    <h2 class="panel-heading">Achievements</h2>
    ''' + achieve_html + '''

    <div class="panel-sub">Publications</div>
    ''' + pubs_html + '''

    <div class="panel-sub">Internships &amp; Placements</div>
    ''' + intern_html + '''
  </div>

  <!-- ══════════════════════════════════════ -->
  <!-- JavaScript -->
  <!-- ══════════════════════════════════════ -->
  <script>
    // ── Tab switching ──
    (function () {
      var tabs = document.querySelectorAll('.dept-tab');
      var panels = document.querySelectorAll('.dept-panel');

      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          tabs.forEach(function (t) { t.classList.remove('is-active'); });
          panels.forEach(function (p) { p.classList.remove('is-active'); });
          tab.classList.add('is-active');
          var panel = document.getElementById('panel-' + tab.getAttribute('data-tab'));
          if (panel) panel.classList.add('is-active');
        });
      });

      // Handle hash on load
      var hash = window.location.hash.replace('#', '');
      if (hash) {
        var target = document.querySelector('[data-tab="' + hash + '"]');
        if (target) target.click();
      }
    })();

    // ── Syllabus selector ──
    (function () {
      ''' + programs_js + '''
      ''' + urls_js + '''
      ''' + subjects_js + '''
      var progPills = document.getElementById('progPills');
      var yearPills = document.getElementById('yearPills');
      var semPillsRow = document.getElementById('semPills');
      var subjectList = document.getElementById('subjectList');
      var currentProg = 'btech';
      var selectedYear = null;

      function buildYearPills() {
        var curriculum = programs[currentProg];
        var years = Object.keys(curriculum);
        yearPills.innerHTML = '';
        years.forEach(function (y) {
          var pill = document.createElement('button');
          pill.className = 'pill';
          pill.setAttribute('data-year', y);
          pill.textContent = 'Year ' + y;
          yearPills.appendChild(pill);
        });
        semPillsRow.innerHTML = '';
        semPillsRow.style.display = 'none';
        subjectList.classList.remove('is-visible');
        subjectList.innerHTML = '';
        selectedYear = null;
      }

      buildYearPills();

      if (window.location.hash === '#mtech') {
        var mtechBtn = progPills.querySelector('[data-prog="mtech"]');
        if (mtechBtn) mtechBtn.click();
      }

      progPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill');
        if (!btn) return;
        currentProg = btn.getAttribute('data-prog');
        progPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active');
        buildYearPills();
      });

      yearPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill');
        if (!btn) return;
        var year = parseInt(btn.getAttribute('data-year'));
        selectedYear = year;
        yearPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active');
        var sems = Object.keys(programs[currentProg][year]);
        semPillsRow.innerHTML = '';
        sems.forEach(function (sem) {
          var pill = document.createElement('button');
          pill.className = 'pill';
          pill.setAttribute('data-sem', sem);
          pill.textContent = 'Sem ' + sem;
          semPillsRow.appendChild(pill);
        });
        semPillsRow.style.display = 'flex';
        subjectList.classList.remove('is-visible');
        subjectList.innerHTML = '';
      });

      semPillsRow.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill');
        if (!btn || !selectedYear) return;
        var sem = parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active');
        var subjects = programs[currentProg][selectedYear][sem];
        if (!subjects) return;
        var html = '';
        subjects.forEach(function (name, i) {
          var units = subjectDetails[name];
          var unitsHtml = '';
          if (units && units.length) {
            unitsHtml = '<div class="subject-units"><ol>';
            units.forEach(function (u) { unitsHtml += '<li>' + u + '</li>'; });
            unitsHtml += '</ol></div>';
          }
          html += '<div class="subject-row" onclick="this.classList.toggle(\\'is-expanded\\')"><span class="subject-num">' + (i + 1) + '.</span><span class="subject-name">' + name + '</span><span class="subject-toggle">&#9654;</span><a href="' + syllabusUrls[currentProg] + '" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">PDF</a></div>' + unitsHtml;
        });
        subjectList.innerHTML = html;
        subjectList.classList.remove('is-visible');
        void subjectList.offsetWidth;
        subjectList.classList.add('is-visible');
      });
    })();

    // ── Publication filter ──
    (function () {
      var filters = document.getElementById('pubFilters');
      var cards = document.querySelectorAll('.pub-card');
      if (!filters || !cards.length) return;
      filters.addEventListener('click', function (e) {
        var btn = e.target.closest('.pub-filter');
        if (!btn) return;
        var year = btn.getAttribute('data-year');
        filters.querySelectorAll('.pub-filter').forEach(function (f) { f.classList.remove('is-active'); });
        btn.classList.add('is-active');
        cards.forEach(function (card) {
          var match = (year === 'all' || card.getAttribute('data-pub-year') === year);
          if (match) { card.classList.remove('is-hidden'); card.style.display = 'flex'; }
          else { card.classList.add('is-hidden'); setTimeout(function () { if (card.classList.contains('is-hidden')) card.style.display = 'none'; }, 350); }
        });
      });
    })();

    // ── Achievement toggle ──
    (function () {
      document.querySelectorAll('[data-achieve]').forEach(function (card) {
        var toggle = card.querySelector('.achieve-toggle');
        card.addEventListener('click', function () {
          var expanded = card.classList.toggle('is-expanded');
          if (toggle) toggle.textContent = expanded ? 'Read Less' : 'Read More';
        });
      });
    })();

    // ── Faculty profile click ──
    (function () {
      document.querySelectorAll('.faculty-item').forEach(function (item) {
        item.addEventListener('click', function () {
          var popup = item.querySelector('.faculty-popup');
          if (!popup) return;
          var name = popup.querySelector('.faculty-popup__name');
          var role = popup.querySelector('.faculty-popup__role');
          var qual = popup.querySelector('.faculty-popup__detail');
          var photo = item.querySelector('.faculty-item__photo img');
          var tags = popup.querySelectorAll('.faculty-popup__tag');
          var n = name ? name.textContent : '';
          var r = role ? role.textContent : '';
          var q = qual ? qual.textContent.replace('Qualification: ', '') : '';
          var p = photo ? photo.getAttribute('src') : '';
          var areas = [];
          tags.forEach(function(t) { areas.push(t.textContent); });
          var id = n.toLowerCase().replace(/Dr\\.|Mr\\.|Mrs\\.|Ms\\.|Prof\\./g, '').trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
          window.location.href = 'faculty-profile.html?name=' + encodeURIComponent(n) + '&role=' + encodeURIComponent(r) + '&qual=' + encodeURIComponent(q) + '&photo=' + encodeURIComponent(p) + '&areas=' + encodeURIComponent(areas.join(',')) + '#' + id;
        });
      });
    })();
  </script>

</body>
</html>'''

# Fix escaped quotes in onclick
html = html.replace("\\\\'is-expanded\\\\'", "'is-expanded'")

with open('c:/mlr/homepage/departments/cse.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'CSE rebuilt: {len(html)} bytes')
