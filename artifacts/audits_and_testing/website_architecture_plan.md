# CafePulse Website V1: Architecture Plan

This document outlines the foundation architecture of the CafePulse official product website.

---

## 1. Technical Stack

To keep the website lightweight, free, secure, and extremely easy to maintain, it is built with zero build steps or heavy framework runtime dependencies:

- **Structure**: Semantic HTML5.
- **Styling**: Vanilla CSS3 using custom properties (CSS variables) for theme mapping.
- **Interactivity**: Vanilla ES6 JavaScript (zero dependencies).
- **Hosting**: GitHub Pages (Static hosting).

---

## 2. Responsive Layout System

The website must render beautifully on all device factors:
- **Mobile** (320px - 480px)
- **Tablet** (481px - 768px)
- **Laptop** (769px - 1024px)
- **Desktop / Ultra-wide** (1025px and up)

### Grid and Flow Guidelines
- **Box-Sizing**: Globally set to `border-box` to prevent sizing issues.
- **Fluid Layouts**: Flexbox and CSS Grid are used exclusively instead of absolute positioning.
- **No Overflow Policy**: 
  - Main containers use relative padding (e.g., `padding: 2rem 5%`).
  - Images utilize `max-width: 100%; height: auto;`.
  - Horizontal scrolling is suppressed at the document level:
    ```css
    html, body {
        overflow-x: hidden;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    ```

---

## 3. Cyber-Clean Dark Design System

The visual language directly reflects the PyQt6 desktop app's "Cyber-Clean Dark Edition" palette:

```css
:root {
    /* Base Palette */
    --bg-primary: #0F1117;
    --bg-secondary: #161B27;
    --bg-tertiary: #1E2535;
    --border-color: #1E2535;
    
    /* Accents */
    --accent-blue: #38BDF8;
    --accent-blue-dark: #0EA5E9;
    --accent-glow: rgba(56, 189, 248, 0.15);
    
    /* System States */
    --color-success: #22C55E;
    --color-warning: #F59E0B;
    --color-danger: #EF4444;
    
    /* Text */
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #475569;
    
    /* Fonts */
    --font-sans: "Inter", "Segoe UI", system-ui, sans-serif;
    
    /* Transitions */
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 4. Performance & Access Optimization

1. **Local Asset Paths**: All links use relative paths (e.g., `./about.html`) so they work seamlessly under both local folders and GitHub Pages subdirectories (`/CafePulse/website/`).
2. **Minimal Styling Overhead**: Custom modular stylesheets split base setup (`main.css`) from viewport overrides (`responsive.css`).
3. **No Database Dependencies**: Dynamic features (such as searching documentation) are handled locally in Vanilla JS using predefined JSON indexes.
