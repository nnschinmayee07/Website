# Architecture Diagram - React Hybrid Setup

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MLRIT Website                             │
│                  (Existing HTML/CSS/JS)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│   Navbar     │    │ Success Stories  │    │    Footer    │
│  (Vanilla)   │    │     (REACT)      │    │  (Vanilla)   │
└──────────────┘    └──────────────────┘    └──────────────┘
                             │
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
            ┌──────────────┐  ┌──────────────┐
            │  React App   │  │  Tailwind    │
            │   (Vite)     │  │     CSS      │
            └──────────────┘  └──────────────┘
```

---

## React App Structure

```
react-app/
│
├── src/
│   │
│   ├── components/
│   │   │
│   │   ├── ui/                    # Reusable UI Components
│   │   │   └── spotlight-card.tsx
│   │   │       ├── Mouse tracking
│   │   │       ├── Glow effect
│   │   │       └── Hover states
│   │   │
│   │   └── sections/              # Page Sections
│   │       └── SuccessStories.tsx
│   │           ├── Infinite scroll
│   │           ├── Story cards
│   │           └── Animations
│   │
│   ├── lib/                       # Utilities
│   │   └── utils.ts
│   │       └── cn() helper
│   │
│   ├── App.tsx                    # Main App
│   ├── main.tsx                   # Entry Point
│   ├── index.css                  # Global Styles
│   └── App.css                    # App Styles
│
├── dist/                          # Build Output
│   ├── index.html
│   └── assets/
│       ├── index-[hash].js
│       └── index-[hash].css
│
└── [config files]
```

---

## Component Hierarchy

```
App
 │
 └── SuccessStories
      │
      ├── Header
      │    ├── Title
      │    └── Description
      │
      └── Scrolling Container
           │
           ├── Left Fade Mask
           │
           ├── Right Fade Mask
           │
           └── Scrolling Track
                │
                └── Story Cards (x16, duplicated)
                     │
                     └── SpotlightCard
                          │
                          ├── Spotlight Effect Layer
                          │
                          └── Content
                               ├── Image
                               ├── Name
                               ├── Role
                               ├── Testimonial
                               └── Accent Line
```

---

## Data Flow

```
┌─────────────────┐
│  stories array  │
│   (8 items)     │
└────────┬────────┘
         │
         │ Duplicate
         ▼
┌─────────────────┐
│ duplicatedStories│
│   (16 items)    │
└────────┬────────┘
         │
         │ Map
         ▼
┌─────────────────┐
│  Story Cards    │
│  (rendered)     │
└────────┬────────┘
         │
         │ Wrap
         ▼
┌─────────────────┐
│ SpotlightCard   │
│  (with glow)    │
└─────────────────┘
```

---

## State Management

```
SuccessStories Component
│
├── isPaused: boolean
│    ├── false → Animation running
│    └── true  → Animation paused
│
└── Event Handlers
     ├── onMouseEnter → setIsPaused(true)
     └── onMouseLeave → setIsPaused(false)


SpotlightCard Component
│
├── isFocused: boolean
│    └── Keyboard focus state
│
├── position: { x: number, y: number }
│    └── Mouse coordinates
│
├── opacity: number
│    └── Spotlight visibility
│
└── Event Handlers
     ├── onMouseMove   → Update position
     ├── onMouseEnter  → Show spotlight
     ├── onMouseLeave  → Hide spotlight
     ├── onFocus       → Keyboard focus
     └── onBlur        → Keyboard blur
```

---

## Build Process

```
┌─────────────────┐
│  Source Files   │
│   (.tsx, .ts)   │
└────────┬────────┘
         │
         │ TypeScript Compiler
         ▼
┌─────────────────┐
│  JavaScript     │
│     (.js)       │
└────────┬────────┘
         │
         │ Vite Bundler
         ▼
┌─────────────────┐
│  Optimized      │
│    Bundle       │
└────────┬────────┘
         │
         │ Output
         ▼
┌─────────────────┐
│   dist/         │
│  ├── index.js   │
│  └── index.css  │
└─────────────────┘
```

---

## Deployment Flow

```
┌─────────────────┐
│  npm run build  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  dist/ folder   │
│   generated     │
└────────┬────────┘
         │
         │ Copy files
         ▼
┌─────────────────┐
│  Web server     │
│  (production)   │
└────────┬────────┘
         │
         │ Serve
         ▼
┌─────────────────┐
│  index.html     │
│  loads React    │
└────────┬────────┘
         │
         │ Render
         ▼
┌─────────────────┐
│ Success Stories │
│   (visible)     │
└─────────────────┘
```

---

## CSS Isolation

```
┌──────────────────────────────────────┐
│         Existing Site CSS            │
│  (navbar.css, hero.css, etc.)        │
└──────────────────────────────────────┘
                  │
                  │ No Conflict
                  │
┌──────────────────────────────────────┐
│      React App CSS (Scoped)          │
│  #react-success-stories { ... }      │
│                                      │
│  ┌────────────────────────────────┐ │
│  │    Tailwind Utilities          │ │
│  │  (scoped to container)         │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

---

## Animation System

```
Scrolling Track
│
├── Initial State
│    └── transform: translateX(0)
│
├── Animation
│    ├── Duration: 25s
│    ├── Timing: linear
│    ├── Iteration: infinite
│    └── Transform: translateX(-50%)
│
└── Hover State
     ├── animation: none
     └── Paused at current position
```

---

## Spotlight Effect

```
Mouse Position
     │
     ▼
┌─────────────────┐
│  Calculate      │
│  Relative Pos   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Update State   │
│  { x, y }       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Radial         │
│  Gradient       │
│  at (x, y)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Spotlight      │
│  Visible        │
└─────────────────┘
```

---

## Responsive Behavior

```
Desktop (>768px)
├── Cards: 320px width
├── Scroll: Horizontal
└── Layout: Single row

Mobile (<768px)
├── Cards: 280px width
├── Scroll: Horizontal (maintained)
└── Layout: Single row (no wrap)
```

---

## Performance Optimization

```
┌─────────────────┐
│  Code Splitting │
│                 │
│  ├── vendor.js  │ ← React, React DOM
│  └── app.js     │ ← Application code
└─────────────────┘

┌─────────────────┐
│  Tree Shaking   │
│                 │
│  Remove unused  │
│  code from      │
│  bundle         │
└─────────────────┘

┌─────────────────┐
│  Minification   │
│                 │
│  Compress JS    │
│  and CSS        │
└─────────────────┘

┌─────────────────┐
│  CSS Purging    │
│                 │
│  Remove unused  │
│  Tailwind       │
│  classes        │
└─────────────────┘
```

---

## Integration Points

```
Existing HTML
│
├── <head>
│    └── <link rel="stylesheet" href="react-app/dist/assets/index.css">
│
└── <body>
     │
     ├── ... existing sections ...
     │
     ├── <div id="react-success-stories"></div>  ← React mounts here
     │
     ├── ... more sections ...
     │
     └── <script src="react-app/dist/assets/index.js"></script>
```

---

## Future Migration Path

```
Phase 1: Success Stories (Current)
┌──────────────────────────────────┐
│  HTML Site                       │
│  ├── Navbar (vanilla)            │
│  ├── Hero (vanilla)              │
│  ├── Success Stories (REACT) ✓  │
│  ├── Events (vanilla)            │
│  └── Footer (vanilla)            │
└──────────────────────────────────┘

Phase 2: Add More Sections
┌──────────────────────────────────┐
│  HTML Site                       │
│  ├── Navbar (vanilla)            │
│  ├── Hero (vanilla)              │
│  ├── Success Stories (REACT) ✓  │
│  ├── Events (REACT) ✓           │
│  └── Footer (vanilla)            │
└──────────────────────────────────┘

Phase 3: Full Migration
┌──────────────────────────────────┐
│  React App                       │
│  ├── Navbar (REACT) ✓           │
│  ├── Hero (REACT) ✓             │
│  ├── Success Stories (REACT) ✓  │
│  ├── Events (REACT) ✓           │
│  └── Footer (REACT) ✓           │
└──────────────────────────────────┘
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────┐
│         User Interface              │
│  (Success Stories Component)        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Component Library              │
│  (SpotlightCard, utilities)         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Styling Layer               │
│  (Tailwind CSS, animations)         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         React Layer                 │
│  (Components, hooks, state)         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Build Tool Layer               │
│  (Vite, TypeScript, bundling)       │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Browser                     │
│  (DOM, JavaScript engine)           │
└─────────────────────────────────────┘
```

---

## Summary

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Isolated React environment
- ✅ No conflicts with existing code
- ✅ Scalable for future growth
- ✅ Maintainable structure
- ✅ Performance optimized

For implementation details, see the other documentation files.
