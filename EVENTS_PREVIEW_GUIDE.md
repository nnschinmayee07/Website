# Events Section — Hover Preview Panel Implementation

## Overview
Added a refined hover-triggered video preview system that displays a small cinematic panel at the bottom-right corner of the Events section when hovering over thumbnail cards.

## Visual Design

### Panel Specifications
```
Position: Absolute (bottom-right corner)
Size: min(360px, 30vw) × auto (16:9 aspect)
Border Radius: 16px
Shadow: Multi-layer (depth + subtle glow)
Z-index: 10 (above content, below controls)
```

### Visual Effects
```css
Video Blur: 8px (visible but softened)
Brightness: 0.85 (slightly dimmed)
Scale: 1.1 (compensates for blur edge crop)
Overlay: Linear gradient (subtle darkening)
```

### States

#### Default (Hidden)
```
opacity: 0
transform: scale(0.95) translateY(8px)
pointer-events: none
```

#### Active (Visible)
```
opacity: 1
transform: scale(1) translateY(0)
transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1)
```

## Interaction Flow

### 1. Hover Enter (Thumbnail)
```
User hovers over thumbnail
  ↓
JS detects mouseenter event
  ↓
Load video source into preview panel
  ↓
Add 'is-previewing' class to thumbnail
  ↓
Add 'is-active' class to panel
  ↓
Panel fades in + scales up
  ↓
Video starts playing
  ↓
"PREVIEW" badge appears on thumbnail
```

### 2. Hover Switch (Different Thumbnail)
```
User moves to different thumbnail
  ↓
Remove 'is-previewing' from previous
  ↓
Switch video source (smooth transition)
  ↓
Add 'is-previewing' to new thumbnail
  ↓
Panel remains visible (no flicker)
```

### 3. Hover Exit
```
User leaves thumbnail area
  ↓
150ms delay (smooth UX)
  ↓
Remove 'is-active' from panel
  ↓
Panel fades out + scales down
  ↓
Video pauses
  ↓
Remove 'is-previewing' indicator
```

## Technical Implementation

### HTML Structure
```html
<section class="ev-section" id="events">
  <!-- Existing player system -->
  <div class="ev-player-wrap">...</div>
  
  <!-- NEW: Hover preview panel -->
  <div class="ev-preview-panel" id="evPreviewPanel">
    <video class="ev-preview-panel__video" id="evPreviewVid" 
           muted loop playsinline></video>
    <div class="ev-preview-panel__overlay"></div>
  </div>
</section>
```

### JavaScript Logic
```javascript
// Single reusable video element
const previewVideo = document.getElementById('evPreviewVid');

// Event mapping
const eventVideos = [
  'events/e1.mp4',
  'events/e2.mp4',
  'events/e3.mp4',
  'events/e4.mp4'
];

// Hover handlers
thumbnails.forEach((thumb, index) => {
  thumb.addEventListener('mouseenter', () => {
    showPreview(thumb, eventVideos[index]);
  });
  
  thumb.addEventListener('mouseleave', () => {
    hidePreview(); // Delayed 150ms
  });
});
```

### Performance Optimizations
1. **Single video element** — Reused for all previews
2. **Source switching** — Only loads if different
3. **Delayed fade-out** — Prevents flicker on quick hovers
4. **GPU acceleration** — Uses transform + opacity
5. **No layout shifts** — Absolute positioning

## Responsive Behavior

### Desktop (> 768px)
```
Position: bottom: 40px, right: 40px
Width: min(360px, 30vw)
Transform origin: bottom-right
```

### Mobile (≤ 768px)
```
Position: bottom: 20px, right: 50%
Width: 85vw
Transform: translateX(50%) + scale/opacity
Centered horizontally
```

## "Now Playing" Indicator

### Visual Design
```css
Content: 'PREVIEW'
Position: Top-right of thumbnail
Background: rgba(232,93,31,0.9) (orange)
Font: 0.5rem, 700 weight, 0.08em spacing
Padding: 3px 6px
Border-radius: 4px
```

### Behavior
- Appears when thumbnail is being previewed
- Removed when hover ends
- Only one active at a time

## Integration with Existing System

### Preserved Features
✓ Main Lionheart player (unchanged)
✓ Beam sweep animation
✓ Tagline transformation
✓ Play/pause controls
✓ Mute functionality
✓ Arrow navigation
✓ Touch swipe support
✓ Ambient background

### New Addition
✓ Hover preview panel (non-intrusive)

### No Conflicts
- Preview panel uses separate video element
- Different z-index layer
- No interference with main player
- Independent state management

## Browser Compatibility

### Required Features
- CSS `aspect-ratio` (modern browsers)
- CSS `filter: blur()` (all modern browsers)
- CSS `backdrop-filter` (optional enhancement)
- JavaScript `classList` API
- Video autoplay (muted)

### Fallback
- Older browsers: Panel won't show (graceful degradation)
- No JavaScript errors
- Main player continues to work

## Testing Checklist

### Visual
- [ ] Panel positioned correctly (bottom-right)
- [ ] Blur effect visible but not excessive
- [ ] Rounded corners render smoothly
- [ ] Shadow provides depth
- [ ] Overlay gradient subtle

### Interaction
- [ ] Hover triggers preview immediately
- [ ] Video loads and plays
- [ ] Switching thumbnails is smooth
- [ ] No flicker on quick hovers
- [ ] Fade-out delay feels natural

### Performance
- [ ] No layout shifts
- [ ] Smooth 60fps animations
- [ ] Video switching is instant
- [ ] No memory leaks

### Responsive
- [ ] Desktop: Bottom-right corner
- [ ] Mobile: Bottom-center
- [ ] Size adjusts appropriately
- [ ] Touch devices: No hover issues

### Integration
- [ ] Main player unaffected
- [ ] Thumbnails still clickable
- [ ] Navigation arrows work
- [ ] Mute button works
- [ ] No z-index conflicts

## Future Enhancements (Optional)

1. **Loading state** — Show spinner while video loads
2. **Keyboard navigation** — Arrow keys to switch previews
3. **Touch support** — Long-press to preview on mobile
4. **Analytics** — Track which events get previewed most
5. **Preloading** — Preload next video for instant switching
6. **Custom blur intensity** — User preference setting
7. **Picture-in-picture** — Detach preview panel

## Conclusion

The hover preview panel adds a refined, cinematic touch to the Events section without disrupting the existing sophisticated player system. It provides users with a quick visual preview of event videos while maintaining the premium, polished feel of the site.
