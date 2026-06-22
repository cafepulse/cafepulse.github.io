# CafePulse GitHub Pages Deployment Guide

This guide describes the configuration and procedures required to deploy the CafePulse website to GitHub Pages successfully. 

## 1. Directory Structure Readiness

The website files reside in the `website/` directory. To deploy, this directory must serve as the root of your GitHub Pages publication.

```
website/
├── .nojekyll             # Bypasses Jekyll build processing
├── 404.html              # Custom professional error page
├── index.html            # Main Landing Page
├── product.html          # Product & Workspace Details
├── pricing.html          # Standard Pricing Matrix
├── founder.html          # Founder Program Sign-up
├── beta.html             # Beta Tester Application
├── documentation.html    # Documentation & EULA/TOS
├── download.html         # Installer Downloads
├── about.html            # Brand Philosophy & About Us
├── contact.html          # Contact Sales & Support
├── robots.txt            # Search Engine Crawl Rules
├── sitemap.xml           # XML Sitemap
├── site.webmanifest      # PWA App Manifest
├── css/                  # Styling files
├── js/                   # Javascript files
└── assets/               # Brand assets & screenshots
```

---

## 2. GitHub Pages Deployment Methods

You can deploy the CafePulse website using either of the following two standard workflows:

### Method A: Deploying from a Branch (GitHub Settings)
1. Push the contents of the `website/` directory to a branch (e.g., `gh-pages` or `main`).
   * *Note: If your repository only contains the website, the root of the branch will be the website files. If it's a monorepo containing application code as well, use Method B (GitHub Actions) or keep the website in a dedicated branch.*
2. Navigate to your GitHub repository: **Settings** -> **Pages**.
3. Under **Build and deployment**, select **Deploy from a branch** as the Source.
4. Choose the target branch (e.g., `main` or `gh-pages`) and path (e.g., `/` root).
5. Click **Save**.

### Method B: GitHub Actions CI/CD (Recommended for Monorepos)
To deploy the `website/` subdirectory automatically whenever you push to the `main` branch, create a GitHub Actions workflow file:

`.github/workflows/deploy-pages.yml`
```yaml
name: Deploy Website to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'website/**'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './website'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 3. Important Deployment Settings

### A. Jekyll Bypass (`.nojekyll`)
GitHub Pages runs a static site builder called Jekyll by default. Since CafePulse uses custom directory structures and doesn't require Jekyll processing, we have included an empty `.nojekyll` file in the root of `website/`. This is critical because:
* It skips Jekyll compile processes, reducing deploy time to under a minute.
* It ensures files/folders that might start with underscores or contain custom assets are served directly without being ignored by Jekyll.

### B. Custom Domain Setup
When CafePulse is ready to move from `https://yubelki.github.io/cafepulse/` to `https://cafepulse.com/`:
1. In your domain provider (e.g., Namecheap, GoDaddy), configure DNS records:
   * Create `A` records pointing to GitHub Pages IP addresses:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   * Create a `CNAME` record for `www` pointing to `yubelki.github.io`.
2. Go to **Settings** -> **Pages** in the GitHub repository.
3. Under **Custom domain**, enter your domain (e.g., `cafepulse.com` or `www.cafepulse.com`) and click **Save**.
4. Check **Enforce HTTPS** to secure the connection with an SSL certificate provided by Let's Encrypt.
5. In your website root, GitHub will automatically create a `CNAME` file containing the domain.

---

## 4. Verification Checklists

### Path Verification
To verify that the site works on both subdirectory deployment and custom root domains:
- [x] Check that all stylesheet, script, and image references start with `./` (relative path) and never with a raw leading slash `/`.
- [x] Test the site locally by double-clicking HTML files or running a local server (`npm run dev` or Python `http.server`).
- [x] Verify that internal navigation links use relative routing (e.g., `./pricing.html` instead of `/pricing.html`).

### 404 Routing Verification
* Since GitHub Pages serves `404.html` on any route mismatch, typing `https://yubelki.github.io/cafepulse/nonexistent-page` should trigger our custom themed `404.html` page. This retains branding consistency and helps redirect users back to the dashboard.
