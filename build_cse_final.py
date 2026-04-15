#!/usr/bin/env python3
"""Build the final CSE department page with all 5 requested features."""

import re

# ═══ Load data ═══
faculty = []
for line in open('c:/mlr/cse_faculty_data.txt', encoding='utf-8'):
    parts = line.strip().split('|')
    if len(parts) == 3:
        faculty.append(parts)

programs_js = open('c:/mlr/cse_programs.js', encoding='utf-8').read()
subjects_js = open('c:/mlr/cse_subjects.js', encoding='utf-8').read()
urls_js = open('c:/mlr/cse_urls.js', encoding='utf-8').read()
pubs_html = open('c:/mlr/cse_pubs.txt', encoding='utf-8').read()
intern_html = open('c:/mlr/cse_intern.txt', encoding='utf-8').read()
achieve_html = open('c:/mlr/cse_achieve.txt', encoding='utf-8').read()

# ═══ Build faculty cards (rectangular flip) ═══
def get_initials(name):
    parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Prof.','').strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else parts[0][:2].upper()

# Faculty specializations (for back of card)
specs = {
    'Dr. Ajmeera Kiran': 'Deep Learning, ML, IoT',
    'Dr. K. Srinivas Rao': 'IoT, Embedded Systems',
    'Dr. N. Sirisha': 'Big Data, Network Security',
    'Dr. A. Balaram': 'Software Engg, Cloud',
    'Dr. V. Thrimurthulu': 'Data Mining, Big Data',
    'Dr. K. Venkata Subbaiah': 'Network Security',
    'Dr. Kandrakunta Chinnaiah': 'ML, Computer Vision',
    'Dr. J. Mahalakshmi': 'NLP, Deep Learning',
    'Dr. G. John Samuel Babu': 'Cloud Computing, IoT',
    'Dr. K. Gagan Kumar': 'AI, Reinforcement Learning',
    'Allam Sangeetha': 'Cloud, Data Science',
}

faculty_cards = []
for photo, name, role in faculty:
    ini = get_initials(name)
    spec = specs.get(name, 'Computer Science')
    # Sanitize for data-author
    author_id = name.replace('Dr. ', '').replace('Mr. ', '').replace('Mrs. ', '').replace('Ms. ', '').replace('Prof. ', '').strip()
    faculty_cards.append(f'''          <div class="fcard" data-author="{author_id}">
            <div class="fcard__inner">
              <div class="fcard__front">
                <img src="{photo}" alt="{name}" onerror="this.style.display='none';this.parentElement.querySelector('.fcard__ini').style.display='flex'" />
                <div class="fcard__ini" style="display:none">{ini}</div>
                <div class="fcard__overlay">
                  <div class="fcard__name">{name}</div>
                  <div class="fcard__role">{role}</div>
                </div>
              </div>
              <div class="fcard__back">
                <div class="fcard__back-name">{name}</div>
                <div class="fcard__back-role">{role}</div>
                <div class="fcard__back-spec">{spec}</div>
                <a href="faculty-profile.html?name={name.replace(' ','%20')}&role={role.replace(' ','%20').replace(',','%2C')}&photo={photo}" class="fcard__back-btn">View Publications</a>
              </div>
            </div>
          </div>''')

faculty_html = '\n'.join(faculty_cards)

# ═══ Add data-author to pub cards ═══
# Map author names to pub cards
pubs_with_authors = pubs_html
# The pub cards already have author divs, we need to add data-author to the pub-card div
# Pattern: <div class="pub-card" data-pub-year="2024">
# We need to extract the authors text and add it
author_patterns = [
    ('Dr. K. Srinivas Rao', 'K. Srinivas Rao'),
    ('Dr. N. Sirisha', 'N. Sirisha'),
    ('Dr. Ajmeera Kiran', 'Ajmeera Kiran'),
    ('Allam Sangeetha', 'Allam Sangeetha'),
]

# Add data-author attributes based on author content
for full, short in author_patterns:
    pubs_with_authors = pubs_with_authors.replace(
        f'<div class="pub-card__authors">{short}',
        f'<div class="pub-card__authors" data-faculty-author="{full}">{short}'
    )
    pubs_with_authors = pubs_with_authors.replace(
        f'<div class="pub-card__authors">{full}',
        f'<div class="pub-card__authors" data-faculty-author="{full}">{full}'
    )

# ═══ Quick-access sidebar items ═══
sidebar_items = [
    ('OV', 'Overview', 'overview'),
    ('OB', 'Objectives', 'objectives'),
    ('FA', 'Faculty', 'faculty'),
    ('AC', 'Academics', 'academics'),
    ('AH', 'Achievements', 'achievements'),
]

sidebar_html = '\n'.join([
    f'    <a class="qbar__btn" data-qtab="{tab}" title="{label}"><span class="qbar__abbr">{abbr}</span><span class="qbar__label">{label}</span></a>'
    for abbr, label, tab in sidebar_items
])

# ═══ Build the page ═══
page = r'''<!DOCTYPE html>
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

    /* ── Dept Nav ── */
    .dept-nav { background: #0B0F1A; display: flex; align-items: stretch; padding: 0 16px; border-bottom: 1px solid rgba(255,255,255,0.06); }
    .dept-nav__link { display: flex; align-items: center; padding: 0 20px; height: 44px; font-family: 'Raleway', sans-serif; font-size: 0.78rem; font-weight: 600; color: rgba(255,255,255,0.5); text-decoration: none; position: relative; transition: color 0.2s, background 0.2s; }
    .dept-nav__link:hover { color: rgba(255,255,255,0.85); background: rgba(232,93,31,0.08); }
    .dept-nav__link:active { background: rgba(232,93,31,0.18); }
    .dept-nav__link::after { content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%) scaleX(0); width: 70%; height: 2px; background: linear-gradient(90deg, transparent, #E85D1F, transparent); transition: transform 0.25s; }
    .dept-nav__link:hover::after, .dept-nav__link:active::after { transform: translateX(-50%) scaleX(1); }
    .dept-nav__link--active { color: #E85D1F; }
    .dept-nav__link--active::after { transform: translateX(-50%) scaleX(1); background: #E85D1F; }
    .dept-nav__link--dept { color: #fff; font-weight: 700; margin-left: auto; }
    .dept-nav__sep { width: 1px; height: 20px; background: rgba(255,255,255,0.1); align-self: center; margin: 0 4px; }

    /* ── Hero ── */
    .dept-hero { background: linear-gradient(135deg, #0D3320, #18453B); padding: 60px 48px 28px; position: relative; overflow: hidden; }
    .dept-hero::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 70% 30%, rgba(232,93,31,0.12), transparent 60%); }
    .dept-hero__eyebrow { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 8px; position: relative; z-index: 1; }
    .dept-hero__title { font-family: 'Playfair Display', serif; font-size: clamp(1.6rem, 3vw, 2.6rem); font-weight: 700; color: #fff; position: relative; z-index: 1; }

    /* ── Tabs ── */
    .dept-tabs { background: #0B0F1A; display: flex; gap: 0; overflow-x: auto; border-bottom: 3px solid #18453B; position: sticky; top: 0; z-index: 40; }
    .dept-tabs::-webkit-scrollbar { height: 0; }
    .dept-tab { font-family: 'Raleway', sans-serif; font-size: 0.78rem; font-weight: 700; color: rgba(255,255,255,0.5); text-decoration: none; padding: 14px 24px; white-space: nowrap; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -3px; transition: color 0.25s, border-color 0.25s, background 0.25s; }
    .dept-tab:hover { color: rgba(255,255,255,0.8); background: rgba(232,93,31,0.08); }
    .dept-tab.is-active { color: #fff; border-bottom-color: #E85D1F; background: rgba(232,93,31,0.06); }
    .dept-tab:active { background: rgba(232,93,31,0.18); }

    /* ── Panels ── */
    .dept-panel { display: none; padding: 48px; max-width: 1100px; margin: 0 auto; }
    .dept-panel.is-active { display: block; animation: fadeIn 0.35s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

    .panel-heading { font-family: 'Playfair Display', serif; font-size: clamp(1.6rem, 2.5vw, 2.2rem); font-weight: 700; color: #0B0F1A; margin-bottom: 28px; line-height: 1.2; }
    .panel-heading::after { content: ''; display: block; width: 48px; height: 3px; background: #E85D1F; margin-top: 12px; border-radius: 2px; }
    .panel-sub { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 800; color: #18453B; text-transform: uppercase; letter-spacing: 0.1em; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 2px solid rgba(24,69,59,0.12); }
    p { font-size: 0.95rem; color: #3A3A3A; max-width: 780px; margin-bottom: 14px; line-height: 1.8; }

    /* ── Cards ── */
    .card { background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    .card h3 { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.15rem; color: #0B0F1A; margin-bottom: 10px; }
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    .three-col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .card--accent { border-top: 3px solid #18453B; }
    .peo-num { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: #18453B; margin-bottom: 10px; }

    /* ── HOD Message ── */
    .hod-msg { display: flex; gap: 28px; align-items: flex-start; background: #fff; border-radius: 16px; padding: 32px; box-shadow: 0 2px 16px rgba(0,0,0,0.06); margin-bottom: 36px; border-left: 4px solid #18453B; }
    .hod-msg__photo { width: 100px; height: 100px; border-radius: 50%; overflow: hidden; flex-shrink: 0; border: 3px solid #18453B; }
    .hod-msg__photo img { width: 100%; height: 100%; object-fit: cover; }
    .hod-msg__label { font-family: 'Raleway', sans-serif; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: #E85D1F; margin-bottom: 8px; }
    .hod-msg__text { font-size: 0.92rem; color: #444; line-height: 1.8; font-style: italic; max-width: none; }
    .hod-msg__name { font-family: 'Raleway', sans-serif; font-size: 0.82rem; font-weight: 700; color: #18453B; margin-top: 12px; }

    /* ── Accordion ── */
    .sub-accordion { margin-bottom: 16px; border-radius: 10px; overflow: hidden; background: #fff; box-shadow: 0 1px 8px rgba(0,0,0,0.05); }
    .sub-accordion__header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; font-family: 'Raleway', sans-serif; font-size: 0.88rem; font-weight: 700; color: #0B0F1A; border-left: 3px solid #18453B; transition: background 0.2s; }
    .sub-accordion__header:hover { background: rgba(24,69,59,0.04); }
    .sub-accordion__chevron { font-size: 0.7rem; color: #888; transition: transform 0.3s; }
    .sub-accordion.is-open .sub-accordion__chevron { transform: rotate(180deg); color: #E85D1F; }
    .sub-accordion__body { max-height: 0; overflow: hidden; transition: max-height 0.4s; }
    .sub-accordion.is-open .sub-accordion__body { max-height: 2000px; }
    .sub-accordion__content { padding: 0 20px 20px; }
    .lab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
    .lab-card { background: #f9f8f5; border-radius: 8px; padding: 16px 18px; border-left: 3px solid #18453B; }
    .lab-card__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.85rem; color: #0B0F1A; margin-bottom: 4px; }
    .lab-card__desc { font-size: 0.78rem; color: #666; }

    /* ── OBE ── */
    .obe-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 20px; }
    .obe-col h4 { font-family: 'Raleway', sans-serif; font-size: 0.82rem; font-weight: 800; color: #18453B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
    .obe-list { list-style: none; padding: 0; }
    .obe-list li { font-size: 0.88rem; color: #444; padding: 8px 0 8px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); position: relative; }
    .obe-list li::before { content: ''; position: absolute; left: 0; top: 14px; width: 6px; height: 6px; border-radius: 50%; background: #E85D1F; }
    .obe-list-numbered p { font-size: 0.88rem; color: #444; line-height: 1.6; margin-bottom: 10px; max-width: none; }
    .obe-list-numbered p strong { color: #18453B; font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.78rem; }

    /* ── Catalog ── */
    .catalog-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }
    .catalog-item { background: #fff; border-radius: 10px; padding: 16px 20px; box-shadow: 0 1px 8px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; border-left: 3px solid #18453B; }
    .catalog-item:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    .catalog-item__text { font-family: 'Raleway', sans-serif; font-size: 0.82rem; font-weight: 700; color: #0B0F1A; }
    .catalog-item__sub { font-size: 0.68rem; color: #888; display: block; margin-top: 2px; }

    /* ── Syllabus ── */
    .pill-row { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .pill { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.82rem; padding: 10px 22px; border-radius: 24px; border: 2px solid rgba(24,69,59,0.25); background: transparent; color: #3A3A3A; cursor: pointer; transition: all 0.25s; }
    .pill:hover { border-color: #E85D1F; color: #E85D1F; }
    .pill.is-active { background: #18453B; border-color: #18453B; color: #fff; }
    .subject-list { max-width: 700px; opacity: 0; transform: translateY(10px); transition: opacity 0.35s, transform 0.35s; }
    .subject-list.is-visible { opacity: 1; transform: translateY(0); }
    .subject-row { display: flex; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(0,0,0,0.06); gap: 16px; cursor: pointer; }
    .subject-num { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.72rem; color: #18453B; width: 28px; }
    .subject-name { flex: 1; font-size: 0.92rem; color: #3A3A3A; }
    .subject-pdf { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 4px 12px; border: 1px solid rgba(232,93,31,0.3); border-radius: 6px; transition: all 0.2s; }
    .subject-pdf:hover { background: #E85D1F; color: #fff; }
    .subject-units { max-height: 0; overflow: hidden; transition: max-height 0.4s; padding: 0 0 0 44px; }
    .subject-row.is-expanded + .subject-units { max-height: 300px; }
    .subject-units ol { list-style: none; padding: 8px 0 12px; counter-reset: unit; }
    .subject-units li { font-size: 0.82rem; color: #555; padding: 4px 0; counter-increment: unit; }
    .subject-units li::before { content: 'Unit ' counter(unit) ': '; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.7rem; color: #18453B; }
    .subject-toggle { font-size: 0.7rem; color: #888; margin-left: 8px; transition: transform 0.3s; display: inline-block; }
    .subject-row.is-expanded .subject-toggle { transform: rotate(90deg); color: #E85D1F; }

    /* ══ FEATURE 1: Quick-access sidebar ══ */
    .qbar {
      position: fixed; right: 0; top: 50%; transform: translateY(-50%);
      width: 48px; background: #0B0F1A; border-radius: 8px 0 0 8px;
      display: flex; flex-direction: column; z-index: 50;
      box-shadow: -2px 0 12px rgba(0,0,0,0.15);
    }
    .qbar__btn {
      display: flex; align-items: center; justify-content: flex-end;
      padding: 10px 12px; cursor: pointer; text-decoration: none;
      border-left: 3px solid transparent;
      transition: border-color 0.2s, background 0.2s; overflow: hidden;
      width: 48px; transition: width 0.3s ease;
    }
    .qbar__btn:hover { width: 160px; background: rgba(232,93,31,0.08); }
    .qbar__btn.is-active { border-left-color: #E85D1F; }
    .qbar__abbr {
      font-family: 'Raleway', sans-serif; font-size: 0.62rem; font-weight: 800;
      color: rgba(255,255,255,0.5); letter-spacing: 0.06em;
      flex-shrink: 0; width: 24px; text-align: center;
    }
    .qbar__btn.is-active .qbar__abbr { color: #E85D1F; }
    .qbar__label {
      font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600;
      color: rgba(255,255,255,0.7); white-space: nowrap; margin-right: 8px;
      opacity: 0; transition: opacity 0.2s;
    }
    .qbar__btn:hover .qbar__label { opacity: 1; }

    /* ══ FEATURE 3: Faculty flip cards ══ */
    .fcard-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
    .fcard { width: 100%; height: 280px; perspective: 800px; cursor: pointer; }
    .fcard__inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s ease; transform-style: preserve-3d; }
    .fcard:hover .fcard__inner { transform: rotateY(180deg); }
    .fcard__front, .fcard__back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 10px; overflow: hidden; }
    .fcard__front { background: linear-gradient(135deg, #2A2F40, #3A4050); }
    .fcard__front img { width: 100%; height: 100%; object-fit: cover; object-position: top; }
    .fcard__ini { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 2rem; color: rgba(255,255,255,0.3); }
    .fcard__overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); }
    .fcard__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.82rem; color: #fff; }
    .fcard__role { font-size: 0.68rem; color: rgba(255,255,255,0.6); }
    .fcard__back { background: #0B0F1A; transform: rotateY(180deg); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; text-align: center; }
    .fcard__back-name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1rem; color: #fff; margin-bottom: 4px; }
    .fcard__back-role { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin-bottom: 12px; }
    .fcard__back-spec { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 600; color: #E85D1F; margin-bottom: 20px; letter-spacing: 0.04em; }
    .fcard__back-btn { font-family: 'Raleway', sans-serif; font-size: 0.72rem; font-weight: 700; color: #E85D1F; text-decoration: none; padding: 8px 20px; border: 1px solid #E85D1F; border-radius: 6px; transition: all 0.2s; }
    .fcard__back-btn:hover { background: #E85D1F; color: #fff; }

    /* ══ FEATURE 4: Pub filter by faculty ══ */
    .pub-card { transition: opacity 0.4s ease; }
    .pub-card.is-dimmed { opacity: 0.2; }

    /* ── Achievements ── */
    .achieve-grid { display: grid; grid-template-columns: 1fr; gap: 16px; max-width: 700px; }
    .achieve-card { border-left: 3px solid #E85D1F; cursor: pointer; }
    .achieve-card h4 { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 6px; }
    .achieve-card p { font-size: 0.88rem; color: #555; margin-bottom: 0; max-height: 0; overflow: hidden; transition: max-height 0.4s; }
    .achieve-card.is-expanded p { max-height: 200px; margin-bottom: 8px; }
    .achieve-toggle { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 700; color: #E85D1F; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 6px; display: inline-block; }

    /* ── Publications ── */
    .pub-filters { display: flex; gap: 8px; margin-bottom: 28px; flex-wrap: wrap; }
    .pub-filter { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.75rem; padding: 7px 18px; border-radius: 20px; border: 2px solid rgba(24,69,59,0.25); background: transparent; color: #3A3A3A; cursor: pointer; transition: all 0.25s; }
    .pub-filter:hover { border-color: #E85D1F; color: #E85D1F; }
    .pub-filter.is-active { background: #18453B; border-color: #18453B; color: #fff; }
    .pub-list { display: flex; flex-direction: column; gap: 16px; max-width: 780px; }
    .pub-card { background: #fff; border-radius: 12px; padding: 24px 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-left: 3px solid #18453B; display: flex; align-items: flex-start; gap: 20px; }
    .pub-card__body { flex: 1; }
    .pub-card__title { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 6px; line-height: 1.4; }
    .pub-card__authors { font-size: 0.82rem; color: #888; margin-bottom: 4px; }
    .pub-card__journal { font-size: 0.82rem; color: #E85D1F; font-style: italic; }
    .pub-card__year { font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 0.68rem; color: #fff; background: #18453B; padding: 4px 10px; border-radius: 10px; flex-shrink: 0; }
    .pub-tag { display: inline-block; margin-top: 8px; font-family: 'Raleway', sans-serif; font-size: 0.68rem; font-weight: 700; color: #18453B; background: rgba(24,69,59,0.08); padding: 3px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.08em; }

    /* ── Internships ── */
    .intern-stats { display: flex; gap: 20px; margin-bottom: 36px; flex-wrap: wrap; }
    .stat-card { background: #fff; border-radius: 12px; padding: 24px 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center; flex: 1; min-width: 140px; }
    .stat-card__num { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.8rem; color: #18453B; line-height: 1; margin-bottom: 6px; }
    .stat-card__label { font-family: 'Raleway', sans-serif; font-weight: 600; font-size: 0.75rem; color: #888; letter-spacing: 0.06em; text-transform: uppercase; }
    .intern-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px; }
    .intern-card { perspective: 600px; background: none; height: 100px; }
    .intern-card__inner { position: relative; width: 100%; height: 100%; transition: transform 0.5s; transform-style: preserve-3d; }
    .intern-card:hover .intern-card__inner { transform: rotateY(180deg); }
    .intern-card__front, .intern-card__back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    .intern-card__front { background: #fff; }
    .intern-card__back { background: #18453B; transform: rotateY(180deg); color: #fff; }
    .intern-card__back-num { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.4rem; margin-bottom: 4px; }
    .intern-card__back-label { font-family: 'Raleway', sans-serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.7; }
    .intern-card__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.95rem; color: #0B0F1A; margin-bottom: 4px; }
    .intern-card__type { font-size: 0.75rem; color: #888; }
    .intern-note { font-size: 0.88rem; color: #666; font-style: italic; max-width: 700px; }

    /* ── Honour / Achievement list ── */
    .honour-table { width: 100%; max-width: 700px; border-collapse: collapse; }
    .honour-table th { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; text-align: left; padding: 12px 16px; border-bottom: 2px solid rgba(0,0,0,0.08); }
    .honour-table td { font-size: 0.88rem; color: #333; padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.05); }
    .achieve-list { list-style: none; padding: 0; max-width: 700px; }
    .achieve-list li { position: relative; padding: 10px 0 10px 20px; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 0.88rem; color: #444; }
    .achieve-list li::before { content: ''; position: absolute; left: 0; top: 16px; width: 8px; height: 8px; border-radius: 50%; background: #E85D1F; }

    /* ── Placement stats ── */
    .placement-stats { display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0; }
    .placement-stat { background: #fff; border-radius: 10px; padding: 20px 28px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; flex: 1; min-width: 130px; border-top: 3px solid #E85D1F; }
    .placement-stat__num { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.6rem; color: #E85D1F; }
    .placement-stat__label { font-size: 0.72rem; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }

    @media (max-width: 768px) {
      .dept-panel { padding: 32px 20px; }
      .two-col, .three-col, .obe-grid, .catalog-grid, .lab-grid { grid-template-columns: 1fr; }
      .hod-msg { flex-direction: column; align-items: center; text-align: center; }
      .qbar { display: none; }
      .fcard-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
      .fcard { height: 240px; }
    }
  </style>
</head>
<body>

  <header class="site-header">
    <div class="masthead">
      <div class="container masthead__inner">
        <a href="../index.html" class="masthead__logo" aria-label="MLRIT Home"><img src="../mlrit-logo-transparent.png" alt="MLRIT Logo" /></a>
        <div class="masthead__tagline"><span>Marri Laxman Reddy Institute of Technology</span></div>
        <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      </div>
    </div>
  </header>

  <nav class="dept-nav">
    <a href="../index.html" class="dept-nav__link">Home</a>
    <span class="dept-nav__sep"></span>
    <a href="ug.html" class="dept-nav__link dept-nav__link--active">Undergraduate</a>
    <a href="pg.html" class="dept-nav__link">Postgraduate</a>
    <span class="dept-nav__sep"></span>
    <span class="dept-nav__link dept-nav__link--dept">CSE Department</span>
  </nav>

  <div class="dept-hero">
    <div class="dept-hero__eyebrow">B.Tech — Computer Science and Engineering</div>
    <div class="dept-hero__title">Department of Computer Science and Engineering</div>
  </div>

  <nav class="dept-tabs" id="deptTabs">
    <a class="dept-tab is-active" data-tab="overview">Overview</a>
    <a class="dept-tab" data-tab="objectives">Objectives</a>
    <a class="dept-tab" data-tab="faculty">Faculty Profiles</a>
    <a class="dept-tab" data-tab="academics">Academics</a>
    <a class="dept-tab" data-tab="achievements">Achievements</a>
  </nav>

  <!-- ══ FEATURE 1: Quick-access sidebar ══ -->
  <div class="qbar" id="qbar">
''' + sidebar_html + r'''
  </div>

  <!-- ═══ TAB 1: Overview ═══ -->
  <div class="dept-panel is-active" id="panel-overview">
    <h2 class="panel-heading">About the Department</h2>

    <div class="hod-msg">
      <div class="hod-msg__photo"><img src="images/cse/ajmeera-kiran.jpg" alt="Dr. Ajmeera Kiran" /></div>
      <div class="hod-msg__content">
        <div class="hod-msg__label">From the HOD's Desk</div>
        <p class="hod-msg__text">"Our department is committed to providing world-class education blending strong theoretical foundations with hands-on experience in cutting-edge technologies. With 64 dedicated faculty, 12 advanced laboratories, and industry partnerships with Boeing, Cyient, and EPAM Systems, we prepare students to excel in the ever-evolving technology landscape."</p>
        <div class="hod-msg__name">— Dr. Ajmeera Kiran, HOD</div>
      </div>
    </div>

    <p>The B.Tech program in Computer Science and Engineering was started in 2005 with an intake of 60, increased to 120 in 2007, 180 in 2012, 240 in 2013, and 840 in 2024. An additional 10% seats are under the lateral entry scheme. The department also offers M.Tech in CSE from 2011.</p>
    <p>The B.Tech (CSE) program has been accredited by the National Board of Accreditation (NBA) since 2008. The department has 12 well-equipped laboratories with 400+ computers, and industry MOUs with Boeing, Cyient, Tata Technologies, EPAM Systems, and Virtusa.</p>

    <div class="panel-sub">Vision and Mission</div>
    <div class="two-col">
      <div class="card card--accent"><h3>Vision</h3><p>Promote Innovation-centric education to produce globally competent graduates in Computer Science and Engineering education and research capable of building a strong and developed nation.</p></div>
      <div class="card card--accent"><h3>Mission</h3><p>Strengthen the department interaction with Multi National Companies to enhance graduate technological advancement skills and research capabilities.</p></div>
    </div>

    <div class="panel-sub">Innovative Teaching Methodology</div>
    <p>The department follows an active learning pedagogy integrating project-based learning, flipped classrooms, and industry-mentored hackathons. Regular guest lectures from professionals at Google, Microsoft, Qualcomm, and ISRO complement the curriculum. Students participate in coding boot camps, open-source contributions, and inter-college technical competitions to build practical skills beyond the classroom.</p>

    <div style="margin-top:32px;">
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">History of the Department <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>The Department of Computer Science and Engineering was established in 2005 with an initial intake of 60 students. The intake was progressively increased — 120 in 2007, 180 in 2012, 240 in 2013, and 840 in 2024. An additional 10% seats are available under the lateral entry scheme. The M.Tech programme in CSE commenced in 2011 with an intake of 6.</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">NBA Accreditation <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content"><p>The B.Tech (CSE) program has been accredited by the National Board of Accreditation (NBA) since 2008, demonstrating sustained quality in engineering education. The department consistently meets NBA's outcome-based education criteria.</p></div></div>
      </div>
      <div class="sub-accordion" onclick="this.classList.toggle('is-open')">
        <div class="sub-accordion__header">Academic Laboratories (12 Labs) <span class="sub-accordion__chevron">&#9660;</span></div>
        <div class="sub-accordion__body"><div class="sub-accordion__content">
          <div class="lab-grid">
            <div class="lab-card"><div class="lab-card__name">Case Tools and Web Technologies Lab</div><div class="lab-card__desc">69 systems — Software design tools, web development</div></div>
            <div class="lab-card"><div class="lab-card__name">Data Structures and Web Services Lab</div><div class="lab-card__desc">30 systems — M.Tech data structures and web services</div></div>
            <div class="lab-card"><div class="lab-card__name">Cryptography and Network Security Lab</div><div class="lab-card__desc">30 systems — Encryption, network protection</div></div>
            <div class="lab-card"><div class="lab-card__name">Mobile Application Development Lab</div><div class="lab-card__desc">36 systems — Android Studio, Flutter</div></div>
            <div class="lab-card"><div class="lab-card__name">Operating Systems Lab</div><div class="lab-card__desc">60 systems — OS concepts, Linux</div></div>
            <div class="lab-card"><div class="lab-card__name">Java Programming Lab</div><div class="lab-card__desc">60 systems — JDK, enterprise Java</div></div>
            <div class="lab-card"><div class="lab-card__name">Cloud Computing Lab</div><div class="lab-card__desc">30 systems — AWS, virtualization</div></div>
            <div class="lab-card"><div class="lab-card__name">Linux Programming Lab</div><div class="lab-card__desc">30 systems — System programming</div></div>
            <div class="lab-card"><div class="lab-card__name">Project Work Lab</div><div class="lab-card__desc">60 systems — Final year projects</div></div>
            <div class="lab-card"><div class="lab-card__name">Object Oriented Programming Lab</div><div class="lab-card__desc">36 systems — C++, OOP</div></div>
            <div class="lab-card"><div class="lab-card__name">Data Mining and Warehousing Lab</div><div class="lab-card__desc">30 systems — Informatica, Weka</div></div>
            <div class="lab-card"><div class="lab-card__name">Database Management Systems Lab</div><div class="lab-card__desc">36 systems — SQL, Oracle</div></div>
          </div>
        </div></div>
      </div>
    </div>
  </div>

  <!-- ═══ TAB 2: Objectives ═══ -->
  <div class="dept-panel" id="panel-objectives">
    <h2 class="panel-heading">Programme Educational Objectives</h2>
    <div class="three-col">
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 1</div><p>Graduates will have a globally competent professional career in the software industry.</p></div>
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 2</div><p>Graduates will pursue higher education and research.</p></div>
      <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 3</div><p>Graduates will have entrepreneur skills to solve societal problems.</p></div>
    </div>

    <div class="panel-sub">Programme Outcomes (POs)</div>
    <div class="obe-list-numbered" style="max-width:780px;">
      <p><strong>PO1:</strong> Apply knowledge of mathematics, science, engineering fundamentals to solve complex engineering problems.</p>
      <p><strong>PO2:</strong> Identify, formulate, review research literature, and analyze complex engineering problems.</p>
      <p><strong>PO3:</strong> Design solutions considering public health, safety, cultural, societal, and environmental factors.</p>
      <p><strong>PO4:</strong> Conduct investigations using research methods, experimental design, data analysis, and synthesis.</p>
      <p><strong>PO5:</strong> Create, select, and apply appropriate techniques, resources, and modern engineering and IT tools.</p>
      <p><strong>PO6:</strong> Assess societal, health, safety, legal, and cultural implications relevant to professional practice.</p>
      <p><strong>PO7:</strong> Demonstrate awareness of engineering solutions' impact on society and environment.</p>
      <p><strong>PO8:</strong> Apply ethical principles and commit to professional ethics and norms of engineering practice.</p>
      <p><strong>PO9:</strong> Function effectively as individual, team member, or leader in diverse environments.</p>
      <p><strong>PO10:</strong> Communicate complex engineering activities effectively through reports and presentations.</p>
      <p><strong>PO11:</strong> Demonstrate knowledge of engineering and management principles.</p>
      <p><strong>PO12:</strong> Recognize and pursue continuous, independent learning amid technological change.</p>
    </div>

    <div class="panel-sub">Programme Specific Outcomes (PSOs)</div>
    <p><strong>PSO1:</strong> Master software system structures and development methodologies to tackle contemporary computing challenges.</p>
    <p><strong>PSO2:</strong> Develop intelligent and autonomous systems to cater societal needs in health care, e-commerce, banking, agriculture, and cyber security.</p>

    <div class="panel-sub">Outcome Based Education (OBE)</div>
    <div class="obe-grid">
      <div class="obe-col"><h4>B.Tech</h4><ul class="obe-list"><li>Educational Objectives and Outcomes</li><li>OBE Process Manual</li><li>Course Outcomes Description Booklets</li><li>Course Outcomes (COs) Attainment</li><li>Program Outcomes (POs) Attainment</li></ul></div>
      <div class="obe-col"><h4>M.Tech</h4><ul class="obe-list"><li>Educational Objectives and Outcomes</li><li>OBE Process Manual</li><li>Course Outcomes Description Booklets</li><li>Course Outcomes (COs) Attainment</li><li>Program Outcomes (POs) Attainment</li></ul></div>
    </div>

    <div class="panel-sub">OBE Portal</div>
    <div class="card" style="max-width:500px;"><h3>OBE Assessment System</h3><p>Access the Outcome Based Education portal for CO/PO attainment data and assessment tools.</p><a href="http://103.15.62.235/ioncudos_mlrit_tier1/" target="_blank" style="font-family:Raleway;font-size:0.78rem;font-weight:700;color:#E85D1F;text-decoration:none;">Open OBE Portal &rarr;</a></div>

    <div class="panel-sub">Handbook</div>
    <div class="card" style="max-width:500px;"><h3>CSE Department Handbook</h3><p>Computer Science and Engineering — Academic Year 2025-26</p></div>
  </div>

  <!-- ═══ TAB 3: Faculty (FEATURE 3: Flip cards) ═══ -->
  <div class="dept-panel" id="panel-faculty">
    <h2 class="panel-heading">Faculty Profiles</h2>
    <p>Hover to flip a card. Click "View Publications" for the full research profile.</p>
    <div class="fcard-grid">
''' + faculty_html + r'''
    </div>
  </div>

  <!-- ═══ TAB 4: Academics ═══ -->
  <div class="dept-panel" id="panel-academics">
    <h2 class="panel-heading">Academics</h2>

    <div class="panel-sub">Course Catalog</div>
    <div class="catalog-grid">
      <a href="https://files.mlrit.ac.in/uploads/R25%20Syllabus/R25_CSE-Syllabus.pdf" target="_blank" class="catalog-item"><div><span class="catalog-item__text">B.Tech Course Catalog — R25</span><span class="catalog-item__sub">Latest regulation (2025 batch)</span></div></a>
      <a href="https://mlrit.ac.in/curriculum/cse-r22-ug-syllabus/" target="_blank" class="catalog-item"><div><span class="catalog-item__text">B.Tech Course Catalog — R22</span><span class="catalog-item__sub">2022 regulation</span></div></a>
      <a href="https://mlrit.ac.in/curriculum/cse-mlr20-ug-syllabus/" target="_blank" class="catalog-item"><div><span class="catalog-item__text">B.Tech Course Catalog — MLR20</span><span class="catalog-item__sub">2020 regulation</span></div></a>
      <a href="https://mlrit.ac.in/curriculum/cse-m-tech-r22-syllabus/" target="_blank" class="catalog-item"><div><span class="catalog-item__text">M.Tech Course Catalog — R22</span><span class="catalog-item__sub">Postgraduate</span></div></a>
      <a href="https://mlrit.ac.in/curriculum/cse-m-tech-mlr20-syllabus/" target="_blank" class="catalog-item"><div><span class="catalog-item__text">M.Tech Course Catalog — MLR20</span><span class="catalog-item__sub">Postgraduate</span></div></a>
    </div>

    <div class="panel-sub">SWAYAM / NPTEL Integration</div>
    <p>The department integrates SWAYAM NPTEL courses into the curriculum. Students can earn credits by completing SWAYAM courses relevant to their programme. The department has been recognised as an NPTEL Discipline Star with 140+ certifications in a single semester.</p>

    <div class="panel-sub">Semester-wise Syllabus Explorer</div>
    <p style="font-style:italic;color:#666;">Select programme, year and semester to browse subjects. Click a subject to see unit-wise topics.</p>
    <div class="pill-row" id="progPills"><button class="pill is-active" data-prog="btech">B.Tech</button><button class="pill" data-prog="mtech">M.Tech</button></div>
    <div class="pill-row" id="yearPills"></div>
    <div class="pill-row" id="semPills" style="display:none;"></div>
    <div class="subject-list" id="subjectList"></div>
  </div>

  <!-- ═══ TAB 5: Achievements ═══ -->
  <div class="dept-panel" id="panel-achievements">
    <h2 class="panel-heading">Achievements</h2>
    ''' + achieve_html + r'''

    <div class="panel-sub">Placements</div>
    <div class="placement-stats">
      <div class="placement-stat"><div class="placement-stat__num">98%</div><div class="placement-stat__label">Placement Rate</div></div>
      <div class="placement-stat"><div class="placement-stat__num">42 LPA</div><div class="placement-stat__label">Highest Package</div></div>
      <div class="placement-stat"><div class="placement-stat__num">312</div><div class="placement-stat__label">Students Placed (2024)</div></div>
      <div class="placement-stat"><div class="placement-stat__num">55+</div><div class="placement-stat__label">Recruiters</div></div>
    </div>
    <p>Top recruiters include Microsoft, Amazon, TCS, Infosys, Capgemini, Wipro, Cognizant, and Accenture.</p>

    <div class="panel-sub">Roll of Honour</div>
    <table class="honour-table">
      <thead><tr><th>Year</th><th>Name</th><th>Achievement</th><th>Score</th></tr></thead>
      <tbody>
        <tr><td>2013</td><td>Sheekha Singh</td><td>University Topper</td><td>86%</td></tr>
        <tr><td>2015</td><td>V. Bhavana</td><td>University Rank Holder</td><td>84%</td></tr>
        <tr><td>2011</td><td>Pankaj Agarwal</td><td>University Rank Holder</td><td>84%</td></tr>
        <tr><td>2012</td><td>S. Geetha Veera Lakshmi</td><td>Department Topper</td><td>81%</td></tr>
        <tr><td>2016</td><td>Hari Priya D S</td><td>Department Topper</td><td>80.82%</td></tr>
        <tr><td>2018</td><td>Nallagari Sravani</td><td>Department Topper</td><td>79.12%</td></tr>
      </tbody>
    </table>

    <div class="panel-sub">Student Achievements</div>
    <ul class="achieve-list">
      <li>Smart India Hackathon — National Finalists (Team CodeCraft, 2024)</li>
      <li>140+ NPTEL certifications in a single semester — NPTEL Discipline Star</li>
      <li>IEEE Student Branch — Engineering Project Expo with 15+ college participation</li>
      <li>CSI Student Chapter — Annual workshops, coding competitions, tech talks</li>
      <li>Amazon ML Summer School — 8 students selected (2024)</li>
    </ul>

    <div class="panel-sub">Publications</div>
    ''' + pubs_with_authors + r'''

    <div class="panel-sub">Internships and Placements</div>
    ''' + intern_html + r'''
  </div>

  <!-- ═══ JavaScript ═══ -->
  <script>
    // Tab switching
    (function () {
      var tabs = document.querySelectorAll('.dept-tab');
      var panels = document.querySelectorAll('.dept-panel');
      var qbtns = document.querySelectorAll('.qbar__btn');

      function switchTab(tabId) {
        tabs.forEach(function (t) { t.classList.remove('is-active'); });
        panels.forEach(function (p) { p.classList.remove('is-active'); });
        qbtns.forEach(function (q) { q.classList.remove('is-active'); });

        var tab = document.querySelector('[data-tab="' + tabId + '"]');
        var panel = document.getElementById('panel-' + tabId);
        var qbtn = document.querySelector('[data-qtab="' + tabId + '"]');
        if (tab) tab.classList.add('is-active');
        if (panel) panel.classList.add('is-active');
        if (qbtn) qbtn.classList.add('is-active');
      }

      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () { switchTab(tab.getAttribute('data-tab')); });
      });

      // Quick-access sidebar
      qbtns.forEach(function (btn) {
        btn.addEventListener('click', function () { switchTab(btn.getAttribute('data-qtab')); });
      });

      // Mark first qbar button active
      var firstQ = document.querySelector('.qbar__btn');
      if (firstQ) firstQ.classList.add('is-active');

      // Hash
      var hash = window.location.hash.replace('#', '');
      if (hash) switchTab(hash);
    })();

    // Syllabus
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
        var c = programs[currentProg]; var years = Object.keys(c);
        yearPills.innerHTML = '';
        years.forEach(function (y) { var p = document.createElement('button'); p.className = 'pill'; p.setAttribute('data-year', y); p.textContent = 'Year ' + y; yearPills.appendChild(p); });
        semPillsRow.innerHTML = ''; semPillsRow.style.display = 'none';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = ''; selectedYear = null;
      }
      buildYearPills();

      if (window.location.hash === '#mtech') { var m = progPills.querySelector('[data-prog="mtech"]'); if (m) m.click(); }

      progPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn) return;
        currentProg = btn.getAttribute('data-prog');
        progPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active'); buildYearPills();
      });

      yearPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn) return;
        var year = parseInt(btn.getAttribute('data-year')); selectedYear = year;
        yearPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); }); btn.classList.add('is-active');
        var sems = Object.keys(programs[currentProg][year]);
        semPillsRow.innerHTML = '';
        sems.forEach(function (s) { var p = document.createElement('button'); p.className = 'pill'; p.setAttribute('data-sem', s); p.textContent = 'Sem ' + s; semPillsRow.appendChild(p); });
        semPillsRow.style.display = 'flex'; subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
      });

      semPillsRow.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn || !selectedYear) return;
        var sem = parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); }); btn.classList.add('is-active');
        var subjects = programs[currentProg][selectedYear][sem]; if (!subjects) return;
        var html = '';
        subjects.forEach(function (name, i) {
          var units = subjectDetails[name]; var uh = '';
          if (units && units.length) { uh = '<div class="subject-units"><ol>'; units.forEach(function (u) { uh += '<li>' + u + '</li>'; }); uh += '</ol></div>'; }
          html += '<div class="subject-row" onclick="this.classList.toggle(\'is-expanded\')"><span class="subject-num">' + (i+1) + '.</span><span class="subject-name">' + name + '</span><span class="subject-toggle">&#9654;</span><a href="' + syllabusUrls[currentProg] + '" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">PDF</a></div>' + uh;
        });
        subjectList.innerHTML = html; subjectList.classList.remove('is-visible'); void subjectList.offsetWidth; subjectList.classList.add('is-visible');
      });
    })();

    // Publication filter
    (function () {
      var filters = document.getElementById('pubFilters');
      var cards = document.querySelectorAll('.pub-card');
      if (!filters || !cards.length) return;
      filters.addEventListener('click', function (e) {
        var btn = e.target.closest('.pub-filter'); if (!btn) return;
        var year = btn.getAttribute('data-year');
        filters.querySelectorAll('.pub-filter').forEach(function (f) { f.classList.remove('is-active'); }); btn.classList.add('is-active');
        cards.forEach(function (card) {
          var match = (year === 'all' || card.getAttribute('data-pub-year') === year);
          if (match) { card.classList.remove('is-hidden'); card.style.display = 'flex'; }
          else { card.classList.add('is-hidden'); setTimeout(function () { if (card.classList.contains('is-hidden')) card.style.display = 'none'; }, 350); }
        });
      });
    })();

    // Achievement toggle
    (function () {
      document.querySelectorAll('[data-achieve]').forEach(function (card) {
        var toggle = card.querySelector('.achieve-toggle');
        card.addEventListener('click', function () {
          var expanded = card.classList.toggle('is-expanded');
          if (toggle) toggle.textContent = expanded ? 'Read Less' : 'Read More';
        });
      });
    })();

    // FEATURE 4: Faculty hover → filter publications
    (function () {
      var fcards = document.querySelectorAll('.fcard');
      var pubCards = document.querySelectorAll('.pub-card');

      fcards.forEach(function (fcard) {
        var authorName = fcard.getAttribute('data-author');

        fcard.addEventListener('mouseenter', function () {
          var hasMatch = false;
          pubCards.forEach(function (pub) {
            var authorsDiv = pub.querySelector('.pub-card__authors');
            if (authorsDiv && authorsDiv.textContent.indexOf(authorName) !== -1) {
              pub.classList.remove('is-dimmed');
              hasMatch = true;
            } else {
              pub.classList.add('is-dimmed');
            }
          });
          // If no match, don't dim anything
          if (!hasMatch) pubCards.forEach(function (p) { p.classList.remove('is-dimmed'); });
        });

        fcard.addEventListener('mouseleave', function () {
          pubCards.forEach(function (pub) { pub.classList.remove('is-dimmed'); });
        });
      });
    })();
  </script>

</body>
</html>'''

with open('c:/mlr/homepage/departments/cse.html', 'w', encoding='utf-8') as f:
    f.write(page)

print(f'CSE rebuilt: {len(page)} bytes, {page.count(chr(10))} lines')
