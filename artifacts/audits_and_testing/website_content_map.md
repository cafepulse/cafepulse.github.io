# CafePulse Website V1: Content Map

This document defines the page-by-page sections and target copywriting to align with official product files.

---

## 1. Home Page (`index.html`)
- **Hero Section**: Strong visual headline outlining "Local-First MikroTik Operations Platform". Modern animated CTA for "Download Free" and "Explore Pro".
- **Product Pillar Grid**: Three-card grid outlining:
  1. *Local-First / Privacy-First*: SQLite local db (`cafepulse.db`), offline functionality.
  2. *MikroTik native*: High performance API observability.
  3. *Adaptive Interface*: Dual themes, responsive widgets.
- **Founders Banner**: Bold banner inviting users to join the limited 100-member Founder Program.
- **Latest Release Summary**: Static badge displaying the current stable release (`v1.0.0.0`) and quick download buttons.

---

## 2. Product Page (`product.html`)
- **Interactive Workspaces Walkthrough**: Detailed feature highlights matching the desktop app layouts:
  - *Workspace Business*: KPI metrics, hotspot analytics, user trends.
  - *Workspace Operations*: Hotspot dashboard, bulk voucher generation, device manager (ARP scanning, local OUI cache).
  - *Workspace Network*: DHCP lease tables, IP addresses, DNS cache, interfaces.
  - *Workspace Advanced*: Backup manager, scheduler, diagnostic ZIP export.

---

## 3. Pricing Page (`pricing.html`)
- **Primary Package Cards**:
  - *Free Edition*: Scan and neighbor discovery, basic monitoring (CPU, RAM, Uptime), basic UI alerts. Gratis selamanya.
  - *Professional Edition*: Rp499.000 one-time, 1 License = 1 PC. Full MikroTik API controls, Automated scheduled backups, PDF report exports, Smart AI insights, 5-Year Update Entitlement (functional after expiration).
- **Comparison Matrix Table**: Detailed side-by-side feature grid mirroring [editions_comparison.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/product/editions_comparison.md).

---

## 4. Founder Program Page (`founder.html`)
- **Founder's Vision Statement**: Commitment to offline-first, avoiding venture capital/cloud user tracking.
- **Membership Benefits**: 5-Year Update Entitlement (software remains fully active locally offline thereafter), exclusive badging in-app, Discord community seat, credits recognition.
- **Availability Limits**: Limited to the first **100 members**. Shows a dynamic/static progress indicator.
- **Price Details**: Rp499.000 one-time payment. Support inquiries directed to: `cafepulse.network@gmail.com`.

---

## 5. Beta Tester Program Page (`beta.html`)
- **Beta Objectives**: OS compatibility (Windows/Linux), RouterOS load verification, UI/UX feedback.
- **Release Channels**:
  - *Alpha Branch*: Experimental builds.
  - *Beta Branch*: Feature-complete release candidates.
- **Bug Reporting Guidelines**: Form outlining log retrieval instructions (`logs/crash/`) and required specs.
- **Incentives**: Two-tier rewards (5-Year Professional License for Top Contributors, 1-Year Professional License for Contributors who submit 3 validated bugs). Capped at 10 active Beta Testers.

---

## 6. Documentation Page (`documentation.html`)
- **Quick-Start Section**: Step-by-step instructions for running the application.
- **MikroTik RouterOS Configuration Guide**: Enabling API service:
  ```bash
  /ip service set api disabled=no port=8728
  ```
- **FAQ Section**: offline capabilities, database location, and security parameters.

---

## 7. Download Page (`download.html`)
- **Download Artifacts List**:
  - Windows Installer (`CafePulse_Setup.exe`)
  - Windows Portable (`CafePulse_Portable.zip`)
  - Linux AppImage (`CafePulse.AppImage`)
- **CLI Download Experience**: Documentation for terminal installation via `curl` and `winget`.
- **Release Feed**: Links pointing to GitHub Releases endpoints (no custom download backend).

---

## 8. About Page (`about.html`)
- **Company Vision & Philosophy**: Delivering powerful yet understandable network monitoring utilities.
- **Founder Spotlight**: High-definition image of founder Youbellkey ([founder_youbellkey.png](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/assets/branding/founder_youbellkey.png)) with short bio.
- **Technological Integrity**: Commitment to keeping database local.

---

## 9. Contact Page (`contact.html`)
- **Support Form**: General support, pricing issues, licensing bugs.
- **Contact Email**: Explicit display of temporary email **`cafepulse.network@gmail.com`**.
- **Support Terms**: Best Effort Support (no response SLA guarantees).
