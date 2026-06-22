# CafePulse: Complete Product Launch Checklist

This checklist tracks the status, priority, ownership, and dependencies of all components for the CafePulse V1 public launch.

---

## 1. Product & Licensing Readiness

| Task ID | Component / Task | Status | Priority | Owner | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PRD-01** | Stress Test (24/72 Hours stability run) | `[ ] Pending` | **HIGH** | Developer | Core Engine stability |
| **PRD-02** | Secure Vault local credential encryption | `[ ] Pending` | **HIGH** | Developer | SQLite database schema |
| **LIC-01** | Offline Activation file validation logic | `[ ] Pending` | **HIGH** | Developer | Key generation algorithm |
| **LIC-02** | 1 License = 1 PC activation constraint check | `[ ] Pending` | **HIGH** | Developer | LIC-01 |

---

## 2. Website & Documentation Readiness

| Task ID | Component / Task | Status | Priority | Owner | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WEB-01** | Reorder navbar list on all 9 pages | `[ ] Pending` | **HIGH** | Web Dev | V1 HTML templates |
| **WEB-02** | Apply Rp499.000 currency globally | `[x] Complete` | **HIGH** | Web Dev | WEB-01 |
| **WEB-03** | Replace "Lifetime" with "5-Year Update Entitlement" | `[x] Complete` | **HIGH** | Web Dev | WEB-02 |
| **WEB-04** | Anonymized application screenshot assets | `[ ] Pending` | **MEDIUM**| Designer | PRD-01 (UI visual check) |
| **DOC-01** | Python build script (`build_docs.py`) | `[ ] Pending` | **HIGH** | Web Dev | GFM markdown documents |
| **DOC-02** | Compile static HTML legal policy files | `[ ] Pending` | **HIGH** | Web Dev | DOC-01 |

---

## 3. Business & Community Setup

| Task ID | Component / Task | Status | Priority | Owner | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BUS-01** | Setup invoicing email template (Rp499.000) | `[ ] Pending` | **MEDIUM**| Developer | Payment gateway links |
| **BUS-02** | Google Form for active Beta registrations | `[ ] Pending` | **MEDIUM**| Developer | Form mapping |
| **COM-01** | Initialize Discord Server categories & roles | `[ ] Pending` | **HIGH** | Developer | Server configuration |
| **COM-02** | Open GitHub Issues template structure | `[ ] Pending` | **HIGH** | Developer | Repository permissions |

---

## 4. Release & Deployment

| Task ID | Component / Task | Status | Priority | Owner | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEP-01** | Create sitemap.xml & robots.txt | `[ ] Pending` | **MEDIUM**| Web Dev | WEB-01 |
| **DEP-02** | Custom 404 page redirect template | `[ ] Pending` | **MEDIUM**| Web Dev | WEB-01 |
| **DEP-03** | GitHub Actions Pages deploy workflow | `[ ] Pending` | **HIGH** | Web Dev | Repository secrets config |
| **REL-01** | Upload Windows Native Setup to GitHub Releases | `[ ] Pending` | **HIGH** | Developer | LIC-02 (Compiler output) |
