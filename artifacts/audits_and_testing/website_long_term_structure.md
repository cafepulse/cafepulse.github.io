# CafePulse Website V1: Long-Term Directory Structure Plan

This document reviews the initial file layouts and provides structural recommendations for the growth phases of CafePulse.

---

## 1. Audited Directory Layout

Currently, the V1 site occupies a flat `website/` directory inside the project codebase:

```
website/
├── [HTML Templates]
├── assets/
├── css/
└── js/
```

This is simple and ideal for V1 launch on GitHub Pages. However, as documentation grows, marketing assets expand, and releases accumulate, a flat folder layout will become difficult to navigate.

---

## 2. Long-Term Directory Architecture Proposal

For CafePulse V2, we recommend migrating the website source files to a structured subfolder tree within the existing codebase:

```
website/
├── index.html                   # Master Landing page
├── 404.html                     # Custom 404 error redirect
├── robots.txt                   # Crawler indexing instructions
├── sitemap.xml                  # SEO path dictionary
│
├── branding/                    # Vector logos and color profiles
│   ├── logo.svg
│   ├── logo_light.png
│   └── logo_dark.png
│
├── assets/                      # Shared static page graphics
│   ├── icon.ico
│   └── splash.png
│
├── screenshots/                 # Application screenshots
│   ├── scr_dashboard.png
│   └── scr_device_manager.png
│
├── docs/                        # Static HTML documentation
│   ├── index.html               # Main guides index
│   ├── installation.html
│   └── routeros_setup.html
│
├── legal/                       # Static compiled legal policy files
│   ├── eula.html
│   ├── privacy_policy.html
│   ├── terms_of_service.html
│   └── refund_policy.html
│
├── releases/                    # Binary download archives details
│   └── index.html               # Releases changelog history
│
├── community/                   # Community program rules
│   ├── founder.html             # Founder application guides
│   └── beta.html                # Tester registration pages
│
├── css/                         # Modular styling system
│   ├── base.css                 # Color tokens, reset, typography
│   ├── layout.css               # Header, footers, grids
│   ├── modules.css              # Cards, buttons, tables
│   └── templates/               # Page specific styling overrides
│
└── js/                          # Interactive logic files
    ├── main.js                  # Global scripts switcher
    ├── download_fetcher.js      # GitHub Release integrations
    └── docs_renderer.js         # Dynamic local searches index
```

---

## 3. Migration Advantages

1. **Clean Segregation of Concerns**: Separates commercial landing layouts (Home, About, Pricing) from heavy reference materials (Documentation, Legal, Release logs).
2. **Modular Styling**: Splitting CSS into base, layout, and modular files prevents a single large stylesheet from becoming unmaintainable.
3. **Improved Path Security**: Restricting legal/policy files to a dedicated `legal/` subfolder makes permissions and access policies easier to configure.
