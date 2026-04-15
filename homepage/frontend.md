# MLRIT Educational Portal — Frontend Documentation

## Project Overview

- **Project:** MLRIT Educational Portal landing page
- **Stack:** Pure HTML, CSS, JavaScript (vanilla) — no frameworks
- **Approach:** Performance-first
- **Focus:** Landing page with structured sections and custom components

---

## Navigation Structure

### About
- Programs
  - UG only
  - PG only
  - No PhD
- Why MLRIT

### Academics
- Resources
  - ERP
  - LMS
  - Edmit – Course Registration
  - Exam Portal

### Admissions
- Undergraduate only
- No PhD
- No PG
- No Admit Options

### Campus
- Student Life
  - Clubs & Societies
  - Events
  - No Cultural Fest

---

## Page Sections

1. Navbar
2. Hero Section
3. About Section
4. Events Section
5. Photo Section
6. Placements / Stats

---

## Section Details

### Navbar
- Dropdown navigation
- Keyboard accessible

### Hero Section
- Single video (current)
- Future: dual video system
- Includes text and CTA

### About Section
- Institution overview
- Programs (moved from Academics)
- Why MLRIT (replaces duplicate Campus Life)

### Events Section
- Orbital reel for selecting events
- Projector system projecting video
- Screen displaying event content

**Backend data required:**
- `title`
- `video_url`
- `thumbnail`
- `description`

### Photo Section
- Grid-based layout
- All tiles are clickable
- Desktop: hover interaction
- Mobile: double-tap interaction

**Backend data required:**
- `image_url`
- `category`
- `headline`
- `link`

### Placements / Stats
- Currently static
- Can be made dynamic later

---

## Interaction Logic

- **Navbar:** Dropdown with keyboard accessibility
- **Events:** Interactive reel + video projection on screen
- **Photo Section:**
  - Desktop: hover to reveal caption
  - Mobile: double-tap to reveal, second tap navigates

---

## Backend Data Requirements

### Events
| Field | Type |
|-------|------|
| title | string |
| video_url | string |
| thumbnail | string |
| description | string |

### Photos
| Field | Type |
|-------|------|
| image_url | string |
| category | string |
| headline | string |
| link | string |

### Hero
| Field | Type |
|-------|------|
| video_url | string |

### Navigation
| Field | Type |
|-------|------|
| labels | string |
| links | string |

---

## Future Scope

- Migration to React / Next.js
- API-driven content
- Asset optimization
- Dynamic content loading
