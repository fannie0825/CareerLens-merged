# CareerLens Logo Usage Guide

## Logo Design: "Focus Aperture"

The CareerLens logo features a clean, modern camera aperture design that forms the shape of a "C", representing:
- **Clarity**: Clear focus on opportunities
- **Precision**: AI-powered targeting
- **Vision**: Seeing the right career path
- **Technology**: Modern, tech-forward aesthetic

The design consists of:
- An outer circle for depth and context
- Aperture blades forming a diamond/star shape in the center
- A C-shaped arc that completes the "C" letterform
- A center focus point representing precision and clarity

## Logo Variants

### 1. Full Logo (Icon + Text)
Use for headers, navigation bars, and primary branding.

```jsx
import Logo from './components/Logo';

<Logo variant="full" size="default" />
```

### 2. Icon Only
Use for favicons, app icons, and compact spaces.

```jsx
<Logo variant="icon" size="sm" />
```

### 3. Text Only
Use when the icon is displayed separately or for text-only contexts.

```jsx
<Logo variant="text" size="lg" />
```

## Size Options

- `sm`: Small (24px icon, 18px text)
- `default`: Default (32px icon, 20px text)
- `lg`: Large (48px icon, 24px text)
- `xl`: Extra Large (64px icon, 30px text)

## Usage Examples

### Header/Navigation
```jsx
<header className="bg-bg-sidebar text-white p-4">
  <Logo variant="full" size="default" className="text-white" />
</header>
```

### Sidebar
```jsx
<aside className="sidebar">
  <Logo variant="full" size="sm" className="mb-8" />
</aside>
```

### Favicon
Use `logo-icon.svg` (64x64px) for favicon:
```html
<link rel="icon" type="image/svg+xml" href="/logo-icon.svg" />
```

### Dark Mode
The logo automatically adapts to dark mode when using the component:
```jsx
<Logo variant="full" darkMode={isDarkMode} />
```

## SVG Files

### Standalone SVG Files
- `public/logo.svg` - Full logo (200x200px viewBox)
- `public/logo-dark.svg` - Dark mode variant
- `public/logo-icon.svg` - Icon only (64x64px)

### Direct SVG Usage
```jsx
<img src="/logo.svg" alt="CareerLens" className="w-32 h-32" />
```

### Using LogoAperture Component (Simplified)
```jsx
import { LogoAperture } from './components/LogoAperture';

// Simple usage
<LogoAperture className="w-8 h-8" />

// With dark mode
<LogoAperture className="w-8 h-8" darkMode={isDarkMode} />
```

## Color Specifications

### Light Mode
- Primary: `#3B82F6` (Accent Blue)
- Secondary: `#2563EB` (Dark Blue)
- Gradient: From `#3B82F6` to `#2563EB`

### Dark Mode
- Primary: `#60A5FA` (Light Blue)
- Secondary: `#3B82F6` (Accent Blue)
- Gradient: From `#60A5FA` to `#3B82F6`

## Best Practices

1. **Minimum Size**: Never scale the logo below 24px height
2. **Clear Space**: Maintain at least 1x the icon height as clear space around the logo
3. **Contrast**: Ensure sufficient contrast against backgrounds
4. **Consistency**: Use the same variant and size within a section
5. **Accessibility**: Always include alt text or aria-label

## Do's and Don'ts

✅ **Do:**
- Use the full logo in headers and navigation
- Use the icon for favicons and app icons
- Maintain aspect ratio when scaling
- Use appropriate size for context

❌ **Don't:**
- Stretch or distort the logo
- Change the colors (except for dark mode variants)
- Rotate the logo
- Place on busy backgrounds without sufficient contrast
- Use outdated or modified versions

## Integration with Tailwind

The logo component uses Tailwind classes from the design system:
- `text-text-heading` for text color
- `dark:text-dark-text-primary` for dark mode text
- Responsive sizing with Tailwind width/height utilities

## File Structure

```
/workspace
├── components/
│   ├── Logo.jsx          # React component (JavaScript)
│   ├── Logo.tsx          # React component (TypeScript)
│   └── LogoUsage.md      # This file
└── public/
    ├── logo.svg          # Full logo (light mode)
    ├── logo-dark.svg     # Full logo (dark mode)
    └── logo-icon.svg     # Icon only
```
