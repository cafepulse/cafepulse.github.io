# CafePulse Final Website Launch Checklist

This checklist tracks the readiness status of all website elements before publishing to production.

## Status Classifications
* **`READY`**: Fully implemented, verified, and aligned with CafePulse business rules.
* **`NEEDS REVIEW`**: Implemented, but requires final client confirmation or credentials mapping.
* **`NOT READY`**: Missing implementation.

---

## 1. Brand & Presentation
* [x] **Branding Assets**
  * *Status*: `READY`
  * *Details*: Official high-resolution assets (`logo.png`, `logo.svg`, `logo_dark.png`, `logo_light.png`) are stored in `website/assets/` and render correctly in headers and footers.
* [x] **Product Screenshots**
  * *Status*: `READY`
  * *Details*: All 24 professional screenshots captured by PyQt6 are placed in `website/assets/screenshots/` and successfully embedded within `product.html` cards.
* [x] **CSS Styles & Theme**
  * *Status*: `READY`
  * *Details*: Custom Cyber-Dark style sheet (`main.css`) loads cleanly with custom fonts and smooth animations.

---

## 2. Marketing & Pricing
* [x] **Pricing & Licensing**
  * *Status*: `READY`
  * *Details*: `pricing.html` contains the single commercial price of **Rp499.000** for **Professional Edition**. Formatted as **One-Time Purchase**, **1 License = 1 PC**, and **5-Year Update Entitlement** with perpetual functionality afterwards.
* [x] **Founder Program Specifications**
  * *Status*: `READY`
  * *Details*: `founder.html` aligns with strict business caps (max 100 slots, early supporters, no shares/ownership/investor status).
* [x] **Beta Program Specifications**
  * *Status*: `READY`
  * *Details*: `beta.html` maps rewards correctly (max 10 active testers, Top Contributor gets a Professional License with 5-year updates, Contributor gets a Professional License with 1-year updates).
* [x] **Community Advisors**
  * *Status*: `READY`
  * *Details*: Rules state that advisors are volunteers providing feedback with no ownership or partnership entitlements.

---

## 3. Legal & Documentation
* [x] **Technical Documentation**
  * *Status*: `READY`
  * *Details*: `documentation.html` has working guides for RouterOS adapter setups and troubleshooting.
* [x] **Legal Policies (EULA & ToS)**
  * *Status*: `READY`
  * *Details*: End-User License Agreement and Terms of Service documents are embedded inside the documentation page to protect IP.
* [ ] **Discord Invitation**
  * *Status*: `NEEDS REVIEW`
  * *Details*: The Discord button link is currently set to a template link (`https://discord.gg/cafepulse`). A live non-expiring custom link must be configured upon official Discord channel setup.
* [ ] **App Download & GitHub Releases**
  * *Status*: `NEEDS REVIEW`
  * *Details*: Links to application installers (`.exe`, `.tar.gz`) are pointing to the GitHub Releases placeholder (`https://github.com/cafepulse/CafePulse/releases`). Real binary paths must be mapped once the code repository releases are built.

---

## 4. Search Engine Optimization & Sharing
* [x] **SEO Meta Configuration**
  * *Status*: `READY`
  * *Details*: Unique titles and descriptions are configured for all 9 pages. Main keywords and canonical urls are mapped.
* [x] **Sitemap Generation**
  * *Status*: `READY`
  * *Details*: `website/sitemap.xml` maps all 9 pages with correct indexing weights.
* [x] **Robots Configuration**
  * *Status*: `READY`
  * *Details*: `website/robots.txt` points to the XML sitemap and permits crawling.
* [x] **Favicon Suite**
  * *Status*: `READY`
  * *Details*: Tab icons, apple touch icons, and Android PWA manifest (`site.webmanifest`) are fully integrated.
* [x] **Open Graph Metadata**
  * *Status*: `READY`
  * *Details*: Social crawler tags are configured on all pages, linking to `assets/og_preview.png`.
* [ ] **Analytics Readiness**
  * *Status*: `NEEDS REVIEW`
  * *Details*: The script tags for Google Analytics or other privacy-first logging utilities must be injected into the HTML heads when production analytics IDs are generated.

---

## 5. Technical Delivery & Layout
* [x] **GitHub Pages Paths**
  * *Status*: `READY`
  * *Details*: All assets load via relative pathing (`./`). Empty `.nojekyll` file successfully bypasses Jekyll parser.
* [x] **404 Routing**
  * *Status*: `READY`
  * *Details*: Custom themed `404.html` error page is created at root.
* [x] **Mobile Responsiveness**
  * *Status*: `READY`
  * *Details*: Grid layouts collapse on small viewports, and comparisons scroll smoothly inside `.table-container` containers.
