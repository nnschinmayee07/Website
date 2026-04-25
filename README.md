# MLRIT — Educational Portal Prototype

Homepage redesign prototype for Marri Laxman Reddy Institute of Technology and Management.

## Stack
Plain HTML · CSS · Vanilla JS — no frameworks, no build step.

## Structure
```
index.html          # Main page
css/
  navbar.css        # Masthead + main nav with hover dropdowns
  hero.css          # Full-viewport video hero with crossfade
  main.css          # Global tokens + all page sections
  rankings.css      # Rankings & accreditations (legacy, merged into main)
  photo-section.css # PRD v1.0 structured photo grid
  events-disc.css   # Events disc / camera preview section
js/
  navbar.js         # Keyboard accessibility for nav
nirf/               # Accreditation SVG logos
hero1_hq.mp4        # Hero video 1 (not tracked in git)
hero2_hq.mp4        # Hero video 2 (not tracked in git)
mlrit-logo.png      # MLRIT logo
```

## Running locally
Open `index.html` directly in a browser — no server needed.

## Video assets
Hero videos are excluded from git due to size.  
Place `hero1_hq.mp4` and `hero2_hq.mp4` in the root after cloning.
