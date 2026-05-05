# MLRIT Search Bar — Implementation Guide

This folder is a **complete, ready-to-use copy** of the MLRIT website with the search bar fully integrated. Every file here reflects the final state of the project.

---

## Folder Structure

```
imple/
├── index.html                        ← Homepage (search integrated)
├── chronicles.html                   ← All chronicles listing page
├── search-results.html               ← Full search results page (Enter key)
│
├── css/
│   ├── navbar.css                    ← Existing navbar styles
│   ├── main.css                      ← Existing main styles
│   ├── search-integration.css        ← NEW: masthead sticky + header-right layout
│   └── chronicles-section.css        ← NEW: homepage chronicles section styles
│
├── js/                               ← All existing JS files
│
├── modules/
│   └── search/
│       ├── index.js                  ← Search system init + chronicles loader
│       ├── styles/
│       │   └── search.css            ← Search panel styles (green gradient)
│       ├── components/
│       │   ├── SearchOverlay.js      ← Slide-out panel DOM
│       │   ├── SearchInput.js        ← Input row + Enter key handler
│       │   ├── FAQList.js            ← Common searches shown when idle
│       │   └── SearchResultsPreview.js ← Live results (Pages + News sections)
│       ├── utils/
│       │   └── searchEngine.js       ← Static search engine (no API needed)
│       └── data/
│           ├── searchData.js         ← NEW: static page index (all site pages)
│           └── chroniclesData.js     ← NEW: 30 MLRIT chronicles (2024-2026)
│
├── departments/                      ← All department HTML pages (search integrated)
│   ├── cse.html
│   ├── ece.html
│   ├── eee.html
│   ├── aeronautical.html
│   ├── mechanical.html
│   ├── aiml.html
│   ├── cse-cs.html
│   ├── cse-ds.html
│   ├── freshman.html
│   ├── mba.html
│   ├── ug.html
│   ├── pg.html
│   └── faculty-profile.html
│
├── placements/
│   ├── placements.html               ← Placements page (search integrated)
│   ├── placements.css
│   └── placements.js
│
├── assets/                           ← Videos, logos
├── nirf/                             ← Accreditation SVG logos
├── mlrit-logo-transparent.png
└── mlrit-logo.png
```

---

## What Was Implemented

### 1. Search Icon in Header
Every page has a search icon (🔍) next to the EAPCET button in the top-right corner.

**HTML changes per page:**
```html
<!-- Add top-header class to masthead -->
<div class="masthead top-header">
  <div class="container masthead__inner">
    <a href="/" class="masthead__logo">...</a>
    <div class="masthead__tagline">...</div>

    <!-- Wrap EAPCET + search icon together -->
    <div class="header-right">
      <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      <!-- Search icon injected here automatically by SearchSystem.init() -->
    </div>
  </div>
</div>
```

**CSS links to add in `<head>`:**
```html
<link rel="stylesheet" href="css/search-integration.css" />
<link rel="stylesheet" href="modules/search/styles/search.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
```

**Scripts to add before `</body>` (root pages):**
```html
<script src="modules/search/data/searchData.js?v=2"></script>
<script src="modules/search/data/chroniclesData.js?v=2"></script>
<script src="modules/search/utils/searchEngine.js?v=2"></script>
<script src="modules/search/components/SearchOverlay.js?v=2"></script>
<script src="modules/search/components/SearchInput.js?v=2"></script>
<script src="modules/search/components/FAQList.js?v=2"></script>
<script src="modules/search/components/SearchResultsPreview.js?v=2"></script>
<script src="modules/search/index.js?v=2"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
    if (window.SearchSystem) {
        window.SearchSystem.init({
            basePath:   '',      // '' for root pages
            apiBase:    '',
            debounceMs: 300,
            faqItems:   []
        });
    }
});
</script>
```

**For department/placements pages (one level deep), use `../` prefix:**
```html
<script src="../modules/search/data/searchData.js?v=2"></script>
<!-- ... same pattern with ../ prefix ... -->
<script>
window.SearchSystem.init({ basePath: '../', ... });
</script>
```

---

### 2. Search Panel Behavior
- Opens as a **full-height slide-out panel** from the right (`height: 100vh`, `position: fixed`)
- Shows **Common Searches** (FAQ) when idle
- Shows **Pages** + **News & Chronicles** sections as you type
- Press **Enter** → navigates to `search-results.html?q=...`
- Click **"View all results"** → same search results page

---

### 3. Static Search (No Backend Needed)
The search works entirely client-side using two data files:

**`modules/search/data/searchData.js`** — indexes all site pages:
- All department pages (CSE, ECE, EEE, Aeronautical, Mechanical, AIML, etc.)
- Placements, UG/PG programs, MBA, Freshman
- Homepage sections

**`modules/search/data/chroniclesData.js`** — 30 MLRIT chronicles (2024-2026):
- Placements (Microsoft 51 LPA, Cognizant, Infosys, etc.)
- Sports (Championships, Football, Sports Quota)
- Events (ZIGNASA 2K25 Hackathon, NSS)
- Rankings (NIRF, Times Survey, ARIIA)
- Faculty achievements, Accreditations, Research

To add more chronicles, append to the `CHRONICLES_DATA` array in `chroniclesData.js`.

---

### 4. Search Results Page (`search-results.html`)
Full-page results with:
- **3 tabs**: All / Pages / News & Chronicles
- **Keyword highlighting** in results
- **Back button** to return to previous page
- Search icon in header to search again

---

### 5. Chronicles Section on Homepage
The homepage has a **"MLRIT Chronicles"** section showing the 6 most recent chronicles as cards before the footer. Each card links to `chronicles.html`.

CSS: `css/chronicles-section.css`

---

### 6. Chronicles Page (`chronicles.html`)
Standalone page listing all 30 chronicles with:
- Filter by category dropdown
- Live search filter
- Date-sorted (newest first)

---

## Color Scheme (Matches MLRIT Navbar)
- **Primary green**: `#1F6B24`
- **Accent orange**: `#E85D1F`
- Search panel header: `linear-gradient(135deg, #1a5c1e 0%, #1F6B24 60%, #2a8030 100%)`

---

## How to Run Locally
```bash
# From the imple/ folder
python -m http.server 8000
# Open: http://localhost:8000
```

---

## Files Changed vs Original
| File | Change |
|------|--------|
| `modules/search/styles/search.css` | Panel is `position: fixed`, `height: 100vh` |
| `modules/search/utils/searchEngine.js` | Uses static data instead of API calls |
| `modules/search/components/SearchResultsPreview.js` | Removed "unavailable" notices |
| `modules/search/index.js` | Submit navigates to `search-results.html` |
| `css/search-integration.css` | Masthead sticky, header-right layout |
| All HTML pages | Added `top-header` class, `header-right` div, CSS + JS links |
