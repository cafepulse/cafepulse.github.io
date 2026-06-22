# CafePulse Website Consistency Recheck Audit
This report compiles content mismatches found between the static website pages and the official LEGAL, BUSINESS, PRODUCT, and COMMUNITY databases.

---

## 1. Summary of Website Content Conflicts

The static pages inside `website/` contain several outdated terms and counters that conflict with official policies:

| Web Page | Element / Line | Mismatch Content | Target Policy / Correct Text | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **`index.html`** | Line 114 (Founder banner) | "...Secure a **lifetime upgrade license**... for only Rp499.000 (limited to the first **250 spots**)." | Replace with **"5-Year Update Entitlement"** and cap at **100 spots**. | **CRITICAL** |
| **`founder.html`** | Line 52 & 71 (Benefits) | "lifetime feature access", "Lifetime license key: Access all current and **future Pro/Enterprise features** with zero subscription bills." | Replace with **"5-Year Update Entitlement"**. Remove references to the unapproved Enterprise Edition. | **CRITICAL** |
| **`founder.html`** | Line 63 (Description) | "...strictly limited to the first **250 memberships**." | Cap at **100 memberships** max. | **CRITICAL** |
| **`founder.html`** | General Copy | Lacks explicit statement clarifying that founders are early adopters, not business partners, affiliates, shareholders, or investors. | Add legal boundaries text block to align with `founder_program_final.md`. | **HIGH** |
| **`beta.html`** | Line 80-82 (Rewards) | "...submit at least three validated bugs... will receive Free **1-Year Pro License key**..." | Should show two-tier structure: **5-Year Professional License** for Top Contributors and **1-Year Professional License** for Contributors. | **HIGH** |
| **`beta.html`** | General Copy | Lacks capacity caps for enrollment. | Add note stating the program is capped at **10 active testers**. | **HIGH** |
| **`pricing.html`** | Pricing cards & Grid | Uses shorthands like "Basic (Free)", "Professional (Pro)", or "Basic Edition" / "Pro Edition". | Standardize naming to **Free Edition** and **Professional Edition**. | **MEDIUM** |
| **`about.html`** | Slogans (Line 6, 51) | Uses Indonesian words: "Our **Visi & Filosofi**" and "Operations & **Visi**". | Translate to English: **"Our Vision & Philosophy"** and **"Operations & Vision"**. | **MEDIUM** |

---

## 2. Inconsistencies vs. Legal Documents

The EULA and EULA-derived pages linked on the website footer must be kept identical to the local versions in `docs/legal/`:
1.  **Workstation Activation Limit**: The website pricing states "1 License = 1 PC", but older license agreements in the docs folder allowed up to 2 devices concurrently. The website is correct; the local `license_agreement.md` must be updated to match it.
2.  **Edition Naming**: The EULA (`eula.md`) uses the term "Free/Basic Edition". The website pricing card uses "Free Edition". The EULA must be aligned to "Free Edition".

---

## 3. Recommended Actions
1.  **Edit `index.html` & `founder.html`**:
    *   Change slot limits from **250** to **100**.
    *   Remove "Lifetime" references and insert the "5-Year Update Entitlement" parameters.
2.  **Edit `beta.html`**:
    *   Insert the 10-tester cap.
    *   Insert the two-tier reward structure (5-Year Professional License for Top Contributors and 1-Year Professional License for Contributors).
3.  **Edit `about.html`**:
    *   Standardize headings and titles to English ("Vision & Philosophy").
