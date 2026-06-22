# CafePulse Pricing Consistency Audit
This report compiles all instances of conflicting price figures, unapproved currencies, subscriptions, and obsolete product editions across the CafePulse codebase and documentation files.

---

## 1. Official Pricing Policy (Source of Truth)
To protect commercial integrity and match local payment integrations, pricing must adhere to these policies:
*   **Official Pricing**: **Rp499.000** (One-Time Purchase).
*   **Launch Promo**: **Rp399.000** (First 30 days only).
*   **Target Currency**: **Indonesian Rupiah (IDR)**. (USD conversion can be shown strictly as an approximate reference for international clients, but IDR is the base currency).
*   **Prohibited Items**: Any references to `USD`, `$49 USD`, `$99 USD`, `$199 USD`, `Subscription`, `SaaS`, `Monthly/Annual Fee`, `Enterprise Edition`, `MSP Edition`, `Lifetime Edition`.

---

## 2. Identified Pricing & Currency Conflicts

Below is the list of conflicts found in the workspace files regarding pricing and currency:

| File Path | Conflict Area | Existing Text / Conflict | Official Policy Mapping | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Currency & Price | Line 31: "- **Price:** $49 USD (One-time payment)" | Set price to **Rp499.000** (with USD reference if needed). | **CRITICAL** |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Currency & Price | Line 11: Professional pricing is listed as **$49 USD** (One-time, perpetual). | Replace with **Rp499.000** (One-Time). | **CRITICAL** |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Subscription & Enterprise | Line 11: Enterprise/MSP pricing is listed as **$199 USD** (Annual subscription). | Remove Enterprise/MSP tier column and annual fee entirely. | **CRITICAL** |
| **[long_term_business_review.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/long_term_business_review.md)** | Subscriptions | Line 41: "Sell high-value modules... on an annual subscription." | Speculative future proposal. Clarify that the current v1.0 releases strictly prohibit subscriptions. | **MEDIUM** |
| **[founder_sales_funnel.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/founder_sales_funnel.md)** | Currency Notes | Line 37: "Mismatch in currency (USD vs. IDR)..." | Set IDR as the official base price across all files. | **LOW** |
| **[founder.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/founder.html)** | Edition Terms | Line 71: "Access all current and future Pro/Enterprise features..." | No Enterprise Edition exists. Align text to "Professional Edition features." | **HIGH** |
| **[pricing.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/pricing.html)** | Page Subtitle | Line 52: "...No monthly subscriptions... Own your software licensing forever." | Good, but grid titles below use shorthands instead of full official names. | **LOW** |

---

## 3. Recommended Actions
1.  **Correct all pricing values**: Overwrite all outdated pricing figures of **$49 USD** with the official IDR pricing of **Rp499.000** (or **Rp399.000** with launch promo explanation).
2.  **Eliminate the Enterprise/MSP tier**: Remove the Enterprise/MSP columns in `pricing_structure.md` and related documents. Delete annual subscription billing details.
3.  **Sanitize website files**: Modify references to "Pro/Enterprise features" in `founder.html` to reference only the "Professional Edition".
