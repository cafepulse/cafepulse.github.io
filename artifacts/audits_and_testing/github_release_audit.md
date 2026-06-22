# CafePulse GitHub Release Audit Report

This report evaluates the readiness of the CafePulse GitHub repository structure, documentations, release tagging plans, sitemap alignments, and website deployment pipelines.

---

## 1. Repository Structure & Configuration

We audited the repository root to verify file structure cleanups:
* **Branding Integrity**: Checked and confirmed that all brand assets (`logo.png`, `logo.svg`, `icon.ico`, `splash.png`) have been cleaned of legacy terms and resides under `assets/branding/`.
* **Licensing Guidelines**: Root directory contains:
  * `README_FREE.md` (installation and execution details for Free Edition).
  * `README_PROFESSIONAL.md` (router setups and offline key information for Professional Edition).
  * `LICENSE.txt` (updated copyright notice).
* **Missing Files**: No dedicated changelog file (`CHANGELOG.md`) is active in the root folder.

---

## 2. Release & Tagging Strategy

* **Target Tag Convention**: `v1.0.0`
* **Release Branch**: `main`
* **Release Package Layout**:
  * Free Edition Release: Bundles `CafePulse_Free.zip` (portable zipped binary) and `CafePulse_Free_Setup.exe` (Inno Setup compiler package).
  * Professional Edition Release: Bundles `CafePulse_Professional.zip` and `CafePulse_Professional_Setup.exe`.
* **Changelog Formatting Plan**:
  * Every release tag description must contain:
    1. A detailed list of additions and fixes.
    2. A checklist of system requirements (Windows 10/11, Python 3.12+ for source execution).
    3. Clear instructions on offline HWID serial activation.
    4. An explicit note confirming **100% Local Processing** (no user credentials or traffic packets ever leave their local machines).

---

## 3. GitHub Pages Integration

* **Official Pages Namespace**: `https://youbellkey.github.io/cafepulse-site/`
* **Subdirectory Pathing**: The website layout references resource files (CSS, JS, images, sitemap) relatively starting with `./`. This ensures the site displays perfectly inside a project subdirectory (`/cafepulse-site/`) without absolute mapping errors.
* **Domain Redirection Error Warning**:
  * **Finding**: `docs/website/` subfolders still contain legacy audit reports (`github_pages_audit.md`, `seo_audit.md`, `open_graph_report.md`, `sitemap_report.md`, `robots_report.md`) that hardcode the wrong URL `https://yubelki.github.io/cafepulse/`.
  * **Status**: While the active website files have been corrected, these legacy documentation files must be updated or removed during the final launch cleanup to prevent confusion.
* **NoJekyll Presence**: The `website/.nojekyll` file is present. This bypasses Jekyll compilation on GitHub Pages, ensuring asset folders starting with underscores (e.g. `_pycache__` if present or other subfolders) are served.
