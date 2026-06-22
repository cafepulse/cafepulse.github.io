# CafePulse Website V1: Folder Structure

The layout structures are placed under the single `website/` directory inside the project codebase:

```
website/
├── index.html                   # Homepage & Product Pitch
├── product.html                 # Workspace & Feature Showcases
├── pricing.html                 # Basic vs Pro Comparison
├── founder.html                 # Founder Program Application page
├── beta.html                    # Beta Program & Bug Reporter page
├── documentation.html           # Setup Guide & RouterOS configuration
├── download.html                # GitHub Releases Download mappings
├── about.html                   # Mission & Founder Bio
├── contact.html                 # Support Form & Contact Email
│
├── css/
│   ├── main.css                 # Base theme properties, resets, styles, grids
│   └── responsive.css           # Screen-size overrides and overflow control
│
├── js/
│   └── main.js                  # Navigation handler, mock downloader, email validator
│
└── assets/
    ├── logo.svg                 # Scalable branding logo
    ├── logo_dark.png            # Dark-theme logo background wrapper
    ├── logo_light.png           # Light-theme logo background wrapper
    ├── icon.ico                 # Favicon
    ├── founder_youbellkey.png   # Founder biography image
    └── splash.png               # Hero background illustrations
```

---

## Folder Principles

1. **Self-Containment**: All styles, icons, and code run locally within this folder. No references to external CDN styles (like Bootstrap or Tailwind) to keep loading speeds maximum and dependencies zero.
2. **Relative Referencing**: Assets and hyperlinks are referenced as relative paths (e.g. `./css/main.css`, `./assets/logo.svg`, `./about.html`) to ensure compatibility with folder previews and path configurations under GitHub Pages subdirectories.
3. **No Build Step Required**: The files in this folder are directly readable by the web browser, eliminating compilation steps.
