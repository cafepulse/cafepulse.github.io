# CafePulse Website V1: GitHub Pages Deployment Plan

This document details hosting setup, subdirectory access rules, and GitHub Releases downloads integration.

---

## 1. GitHub Pages Hosting Setup

Since CafePulse is hosted in a repository on GitHub, we can leverage GitHub Pages for free static hosting.

### Configuration Methods
1. **Source Option: GitHub Actions (Recommended)**:
   Configure a workflow (`.github/workflows/deploy-website.yml`) that triggers on push to the `main` branch, extracts the `website/` directory, and deploys it to the `gh-pages` branch.
2. **Source Option: Deploy from Branch**:
   Configure GitHub Pages under Repository Settings -> Pages to build from the `main` branch, pointing specifically to the `/docs` folder. *Note: If we use this option, we would symlink or build into `/docs`, but the Actions method is cleaner as it keeps the workspace root organized.*

---

## 2. Directory & Path Resolving Rules

When deployed on GitHub Pages, the base URL is typically:
`https://<username>.github.io/CafePulse/`

To prevent assets from failing to load (404s):
- **JANGAN** use absolute root paths (e.g. `/css/main.css`, `/assets/logo.svg`).
- **SELALU** use relative paths (e.g. `./css/main.css`, `./assets/logo.svg`).
- Hyperlinks between pages must also be relative (e.g. `./product.html` instead of `/product.html`).

---

## 3. GitHub Releases Download Integration

Instead of coding a complex custom installer backend:
- The website uses direct links to the official repository releases:
  - Latest Release page: `https://github.com/<username>/CafePulse/releases/latest`
  - Direct Installer link format: `https://github.com/<username>/CafePulse/releases/latest/download/CafePulse_Setup.exe`
- **Dynamic JavaScript Fetch**:
  On the `download.html` page, Vanilla JS fetches from the public GitHub Releases API:
  `https://api.github.com/repos/<username>/CafePulse/releases/latest`
  It parses the JSON response to display the latest release tag (e.g. `v1.0.0.0`), binary sizes, publish date, and updates the download links in real-time.
  If the API call fails or is rate-limited, the page falls back to static hardcoded links.
