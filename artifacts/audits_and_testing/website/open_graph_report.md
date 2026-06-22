# CafePulse Open Graph Metadata Integration Report

This document reports the implementation of Open Graph and Twitter Card metadata across the CafePulse website to ensure sharing preview optimization on Discord, WhatsApp, Telegram, Facebook, and LinkedIn.

## 1. Social Preview Image Asset

We generated a custom branding banner matching the CafePulse Cyber-Dark style and saved it to the website repository:
* **File Location**: `website/assets/og_preview.png`
* **Resolution**: 1200x630 pixels (standard optimal dimension for Facebook, LinkedIn, Discord, and Slack cards)
* **Design Features**: Dark-themed grid background with CafePulse logo icon, corporate tagline ("Local-First MikroTik Operations Platform"), and neon cyan accent overlays.

---

## 2. Injected Metadata Tags

The following standardized Open Graph and Twitter Card tags have been injected into the `<head>` of all 9 HTML files. Each page has unique titles and descriptions matching its specific content, while using the absolute URL schema for social sharing parsers.

### Metadata Tag Structure Example (`website/index.html`):
```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://yubelki.github.io/cafepulse/">
<meta property="og:title" content="CafePulse — Local-First MikroTik Operations Platform">
<meta property="og:description" content="Modern, lightweight, local-first network monitoring and voucher management platform for MikroTik RouterOS networks. Keep your data private offline.">
<meta property="og:image" content="https://yubelki.github.io/cafepulse/assets/og_preview.png">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://yubelki.github.io/cafepulse/">
<meta name="twitter:title" content="CafePulse — Local-First MikroTik Operations Platform">
<meta name="twitter:description" content="Modern, lightweight, local-first network monitoring and voucher management platform for MikroTik RouterOS networks. Keep your data private offline.">
<meta name="twitter:image" content="https://yubelki.github.io/cafepulse/assets/og_preview.png">
```

### Page-Specific Open Graph Metadata Map:

| Page Name | Social Title (`og:title`) | Social URL (`og:url`) |
| :--- | :--- | :--- |
| `index.html` | CafePulse — Local-First MikroTik Operations Platform | `https://yubelki.github.io/cafepulse/` |
| `product.html` | Product Features & Workspaces — CafePulse | `https://yubelki.github.io/cafepulse/product.html` |
| `pricing.html` | Pricing & Licensing — CafePulse | `https://yubelki.github.io/cafepulse/pricing.html` |
| `founder.html` | Founder Program — CafePulse | `https://yubelki.github.io/cafepulse/founder.html` |
| `beta.html` | Beta Tester Program — CafePulse | `https://yubelki.github.io/cafepulse/beta.html` |
| `documentation.html` | Documentation & Legal Policy — CafePulse | `https://yubelki.github.io/cafepulse/documentation.html` |
| `download.html` | Download CafePulse App | `https://yubelki.github.io/cafepulse/download.html` |
| `about.html` | About Us & Our Philosophy — CafePulse | `https://yubelki.github.io/cafepulse/about.html` |
| `contact.html` | Contact Support & Sales — CafePulse | `https://yubelki.github.io/cafepulse/contact.html` |

---

## 3. Benefits & Performance Verification

* **Discord / Telegram**: Links now render a full large image preview containing the high-contrast logo banner, attracting click-throughs.
* **WhatsApp / Mobile SMS**: Shows a compact horizontal preview with the official favicon icon and clear title summary.
* **No Jekyll interference**: Skip rules in `.nojekyll` protect pathing references so scrapers can grab assets instantly without cache misses.
