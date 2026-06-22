# CafePulse Website V1: Navigation Map

This document outlines page transitions, routing, and access to legal documents.

---

## 1. Routing Model

Since V1 is hosted on GitHub Pages, the site operates using static path routing:
- Root URL: `https://<username>.github.io/CafePulse/website/index.html` (or simply `index.html`)
- All pages are stored in the root folder, allowing flat routing paths:
  - Homepage: `./index.html`
  - Product: `./product.html`
  - Pricing: `./pricing.html`
  - Founder: `./founder.html`
  - Beta: `./beta.html`
  - Documentation: `./documentation.html`
  - Download: `./download.html`
  - About: `./about.html`
  - Contact: `./contact.html`

---

## 2. Navigation Header & Responsive Drawer

All pages share a consistent navbar structure at the top:
- **Logo Area**: Official `logo.svg` wrapped with a home link.
- **Desktop Navigation Links**:
  - `Product`
  - `Pricing`
  - `Founder`
  - `Beta`
  - `Docs`
  - `Download`
  - `About`
  - `Contact`
- **Mobile Menu Trigger**: A hamburger menu icon (`bars` style) which triggers an overlay drawer listing all links.

---

## 3. Navigation Footer

The page footer includes:
- **Main Section Links**: Home, Product, Pricing, Founder Program, Beta Program, Documentation, Download.
- **Single Source of Truth (Legal Documents)**:
  - Privacy Policy (`./documentation.html?doc=privacy_policy`)
  - Terms of Service (`./documentation.html?doc=terms_of_service`)
  - EULA (`./documentation.html?doc=eula`)
  - Refund Policy (`./documentation.html?doc=refund_policy`)
  - Trademark Notes (`./documentation.html?doc=trademark_notes`)

---

## 4. Single Source of Truth Loader (Markdown Fetching)

To respect the core instruction—**JANGAN menduplikasi branding, legal, pricing, licensing, documentation, atau business policy**—the documentation and legal pages will not hardcode copy. Instead:
1. When a user clicks a legal link or documentation link, they are routed to `documentation.html` with a query parameter (e.g., `?doc=privacy_policy` or `?doc=pricing_structure`).
2. The Vanilla JS engine fetches the raw markdown file directly from the project's source docs folder:
   - For legal: `../docs/legal/[filename].md`
   - For business/pricing: `../docs/business/[filename].md`
   - For product/manuals: `../docs/product/[filename].md`
3. A lightweight JavaScript markdown parser reads the file contents and renders it inside `documentation.html` dynamically.
4. This ensures that any update to the desktop application's docs folder immediately reflects on the live website without redeploying code.
