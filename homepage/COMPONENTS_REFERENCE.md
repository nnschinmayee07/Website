# Components Reference

## SpotlightCard Component

### Location
`src/components/ui/spotlight-card.tsx`

### Purpose
Creates a card with a mouse-tracking spotlight/glow effect.

### Props
```typescript
interface SpotlightCardProps {
  children: React.ReactNode;      // Card content
  className?: string;              // Additional CSS classes
  spotlightColor?: string;         // Spotlight color (default: orange)
  customSize?: boolean;            // Allow custom sizing (default: false)
}
```

### Usage
```tsx
<SpotlightCard
  customSize
  spotlightColor="rgba(232, 93, 31, 0.2)"
  className="h-full"
>
  <div>Your content here</div>
</SpotlightCard>
```

### Features
- Mouse-tracking spotlight effect
- Smooth opacity transitions
- Focus/blur support
- Customizable spotlight color
- Flexible sizing

---

## SuccessStories Component

### Location
`src/components/sections/SuccessStories.tsx`

### Purpose
Displays an infinite horizontal scrolling section of success stories with glow effects.

### Props
None (self-contained)

### Data Structure
```typescript
interface Story {
  id: number;
  name: string;
  role: string;
  testimonial: string;
  image: string;
  color: 'orange' | 'green';
}
```

### Features
- Infinite horizontal scroll
- Seamless loop (no visible break)
- Pause on hover
- Alternating orange/green colors
- Responsive design
- Edge fade masks

### Customization

#### Add Stories
```typescript
const stories: Story[] = [
  {
    id: 9,
    name: 'New Person',
    role: 'Department · Company',
    testimonial: 'Your quote here',
    image: 'https://images.unsplash.com/...',
    color: 'orange',
  },
];
```

#### Change Animation Speed
```typescript
style={{
  animation: isPaused ? 'none' : 'scroll-left 30s linear infinite',
}}
```

#### Adjust Card Width
```tsx
<div className="flex-shrink-0 w-96"> {/* Change w-80 to w-96 */}
```

---

## Utility Functions

### Location
`src/lib/utils.ts`

### cn() Function
Combines class names with proper merging.

```typescript
import { cn } from '@/lib/utils';

// Usage
<div className={cn(
  'base-class',
  condition && 'conditional-class',
  'another-class'
)} />
```

---

## Styling System

### Tailwind Classes
All components use Tailwind CSS utility classes.

### Brand Colors
```typescript
// In tailwind.config.js
mlrit: {
  orange: '#E85D1F',
  green: '#18453B',
}

// Usage
className="text-mlrit-orange bg-mlrit-green"
```

### Animations
```typescript
// In tailwind.config.js
keyframes: {
  "scroll-left": {
    "0%": { transform: "translateX(0)" },
    "100%": { transform: "translateX(-50%)" },
  },
}

// Usage
className="animate-scroll-left"
```

---

## Component Hierarchy

```
App
└── SuccessStories
    ├── Header (title + description)
    ├── Scrolling Container
    │   ├── Left Fade Mask
    │   ├── Right Fade Mask
    │   └── Scrolling Track
    │       └── Story Cards (duplicated)
    │           └── SpotlightCard
    │               ├── Image
    │               ├── Name
    │               ├── Role
    │               ├── Testimonial
    │               └── Accent Line
```

---

## State Management

### SuccessStories State
```typescript
const [isPaused, setIsPaused] = useState(false);
```

Controls animation pause/resume on hover.

### SpotlightCard State
```typescript
const [isFocused, setIsFocused] = useState(false);
const [position, setPosition] = useState({ x: 0, y: 0 });
const [opacity, setOpacity] = useState(0);
```

Manages spotlight effect and mouse tracking.

---

## Event Handlers

### SuccessStories
```typescript
onMouseEnter={() => setIsPaused(true)}   // Pause scroll
onMouseLeave={() => setIsPaused(false)}  // Resume scroll
```

### SpotlightCard
```typescript
onMouseMove={handleMouseMove}      // Track mouse position
onMouseEnter={handleMouseEnter}    // Show spotlight
onMouseLeave={handleMouseLeave}    // Hide spotlight
onFocus={handleFocus}              // Keyboard focus
onBlur={handleBlur}                // Keyboard blur
```

---

## Responsive Behavior

### Breakpoints
```typescript
// Tailwind breakpoints
sm: '640px'   // Small devices
md: '768px'   // Medium devices
lg: '1024px'  // Large devices
xl: '1280px'  // Extra large
2xl: '1400px' // 2X large
```

### Responsive Classes
```tsx
className="text-4xl md:text-5xl"  // Larger text on medium+
className="w-80"                   // Fixed width (responsive via container)
```

---

## Performance Considerations

### Optimizations
1. **CSS Animations** - GPU-accelerated transforms
2. **Duplicated Data** - Seamless infinite scroll
3. **Conditional Rendering** - Minimal re-renders
4. **Lazy Loading** - Images load on demand

### Best Practices
- Use `transform` instead of `left/right`
- Use `opacity` instead of `display`
- Avoid layout thrashing
- Minimize state updates

---

## Accessibility

### Keyboard Support
- SpotlightCard responds to focus/blur
- Proper ARIA labels (add as needed)

### Screen Readers
- Semantic HTML structure
- Alt text on images
- Descriptive text content

### Improvements Needed
- Add ARIA labels to cards
- Add keyboard navigation for scroll
- Add skip links
- Test with screen readers

---

## Browser Support

### Minimum Requirements
- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES2020 support
- CSS Grid support
- CSS Animations support

### Fallbacks
- Graceful degradation for older browsers
- No JavaScript fallback (static content)

---

## Testing

### Manual Testing
1. Hover over cards → spotlight appears
2. Move mouse → spotlight follows
3. Hover over track → scroll pauses
4. Move away → scroll resumes
5. Resize window → responsive layout

### Automated Testing (Future)
- Unit tests for components
- Integration tests for interactions
- E2E tests for user flows

---

## Extending Components

### Add New Section
```typescript
// src/components/sections/NewSection.tsx
export const NewSection = () => {
  return (
    <section className="...">
      {/* Your content */}
    </section>
  );
};

// App.tsx
import { NewSection } from './components/sections/NewSection';

function App() {
  return (
    <>
      <SuccessStories />
      <NewSection />
    </>
  );
}
```

### Create New UI Component
```typescript
// src/components/ui/new-component.tsx
import { cn } from '@/lib/utils';

interface NewComponentProps {
  // Props here
}

export const NewComponent: React.FC<NewComponentProps> = (props) => {
  return (
    <div className={cn('base-classes', props.className)}>
      {/* Component content */}
    </div>
  );
};
```

---

## Common Patterns

### Conditional Classes
```tsx
className={cn(
  'base-class',
  isActive && 'active-class',
  variant === 'primary' ? 'primary-class' : 'secondary-class'
)}
```

### Dynamic Styles
```tsx
style={{
  background: `radial-gradient(...)`,
  transform: `translateX(${position}px)`,
}}
```

### Event Handling
```tsx
const handleClick = (e: React.MouseEvent) => {
  e.preventDefault();
  // Handle click
};

<button onClick={handleClick}>Click</button>
```

---

## Troubleshooting

### Spotlight Not Working
- Check mouse event handlers
- Verify position state updates
- Check opacity transitions

### Scroll Not Smooth
- Verify animation keyframes
- Check for layout shifts
- Ensure GPU acceleration

### Cards Not Displaying
- Check data array
- Verify image URLs
- Check CSS classes

---

## Future Enhancements

### Potential Features
- [ ] Lazy load images
- [ ] Add loading states
- [ ] Implement virtual scrolling
- [ ] Add touch gestures
- [ ] Keyboard navigation
- [ ] Accessibility improvements
- [ ] Animation controls
- [ ] Theme switching
- [ ] Dark/light mode
- [ ] RTL support

---

## Resources

### Documentation
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Docs](https://vitejs.dev)

### Tools
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [ES7+ React Snippets](https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets)
- [TypeScript Error Translator](https://ts-error-translator.vercel.app/)

---

## Summary

This reference covers all components, utilities, and patterns used in the React Success Stories section. Use it as a guide for customization, extension, and troubleshooting.

For implementation details, see `REACT_IMPLEMENTATION_GUIDE.md`.
For quick setup, see `QUICK_START.md`.
