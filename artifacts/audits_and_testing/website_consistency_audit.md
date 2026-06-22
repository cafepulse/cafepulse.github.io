# CafePulse Product Website Maturity Audit: Consistency Report

This report evaluates content, branding, licensing, pricing, and program alignment inconsistencies across the CafePulse V1 website pages and assets.

---

## 1. Audit Findings & Discrepancies

### 1.1 Pricing & Currency Conflicts
- **Finding**: Historically, files like `pricing_structure.md` and `founder_program.md` listed pricing as **$49 USD**. However, `MASTER_PRODUCT_RELEASE_ROADMAP.md` and the user requirements establish the target price as **Rp499.000 (One-Time Purchase)**.
- **Risk**: Displaying USD prices on some pages (e.g. for the Founder Program) and IDR prices on others will confuse Indonesian target consumers and dilute commercial credibility.
- **Recommendation**: Standardize all currency notation across all website copy to IDR (**Rp499.000**). If targeting international operators, explicitly set up separate geo-pricing tables later instead of mixing notations.
- **Priority**: **HIGH**

### 1.2 Licensing Activation Limits
- **Finding**: In older legal EULA templates and licensing guidelines, reference is made to a **2-device limit (diagnostic laptop + workstation)**. In contrast, the current commercial guidelines enforce a strict **1 License = 1 PC** policy.
- **Risk**: Legal disputes or support load spikes from users attempting to activate their license key on a second device.
- **Recommendation**: Clean all legal files (`eula.md`, `license_agreement.md`) and the website pricing card copywriting to explicitly mention: *"1 License key is restricted to 1 PC active activation"*.
- **Priority**: **HIGH**

### 1.3 Terminology Rules (Founder & Beta Support)
- **Finding**: Initial content referenced "Lifetime License", "Lifetime Membership", or "Lifetime Updates" for the Founder Program. 
- **Risk**: Legally binding commitments to provide infinite updates are highly risky, as operating system frameworks (PyQt6/Qt, Windows, RouterOS API) change over long horizons.
- **Recommendation**: Replace all "Lifetime" references with **"5-Year Update Entitlement"**, stating clearly: *"Software remains fully functional locally after the entitlement update window expires."*
- **Priority**: **CRITICAL**

### 1.4 Branding & Theme Variables Alignment
- **Finding**: The desktop app uses a curated, cyber-dark palette (`#0F1117`, `#161B27`, `#1E2535`, `#38BDF8`). The website matches this, but does not offer a theme switcher (Light Theme), whereas the desktop application provides a built-in light theme.
- **Risk**: Inconsistent onboarding experience if light-theme users visit the website and cannot preview or see matching branding.
- **Recommendation**: Build support for a CSS class-based light mode override mapping the PyQt theme variables in a future phase.
- **Priority**: **MEDIUM**

---

## 2. Risk & Priority Matrix

| Identifier | Conflict Description | Risk Level | Priority | Action Item |
| :--- | :--- | :--- | :--- | :--- |
| **CON-01** | "Lifetime Updates" vs 5-Year Entitlement | **CRITICAL** | **Immediate** | Clean website and founder copy |
| **CON-02** | $49 USD vs Rp499.000 pricing mismatch | **HIGH** | **Immediate** | Apply IDR rates globally |
| **CON-03** | 2-Device activation vs 1 PC rule | **HIGH** | **Immediate** | Sync EULA and website copy |
| **CON-04** | Form submission vs Direct Gmail | **MEDIUM** | **Deferred** | Simplify contact system |
