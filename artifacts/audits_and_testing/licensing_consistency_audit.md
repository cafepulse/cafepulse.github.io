# CafePulse Licensing Consistency Audit
This report compiles conflicts and mismatches in the licensing terms, activations, update windows, support tiers, and refunds across the CafePulse documentation and website.

---

## 1. Official Licensing Policy (Source of Truth)
To protect the product lifecycle and match the developer's solo capacity, all materials must reflect these official rules:
*   **Product Editions**: Free Edition and Professional Edition only.
*   **Professional Price**: Rp499.000 (One-Time Purchase).
*   **Seat Limit**: 1 License = 1 PC active activation. No Multi-Seat or concurrent devices.
*   **Activation Methods**: Online Activation and Offline Activation (via request file/file exchange) are both supported.
*   **Updates Entitlement**: 5-Year Update Entitlement. The core software remains fully functional locally after this window expires.
*   **Support SLA**: Best Effort Support only. No time-bound SLA guarantees.
*   **Prohibited Terms**: `Subscription`, `SaaS`, `Monthly Fee`, `Annual Fee`, `Lifetime Updates`, `Lifetime License`, `Enterprise/MSP Edition`.

---

## 2. Licensing Policy Conflicts Inventory

Below is a detailed list of all documents containing licensing terms that conflict with the official source of truth.

| File Path | Component / Section | Existing Text / Conflict | Official Policy Mapping | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Section 2 (Founder Benefits) | "Lifetime License: Access to all current and future Pro/Enterprise features... forever." | 5-Year Update Entitlement. Core software remains functional locally thereafter. No Enterprise features exist. | **CRITICAL** |
| **[community_advisor_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/community_advisor_program.md)** | Section 3 (Advisor Privileges) | "Complementary Lifetime Pro License: Free, unrestricted lifetime access to CafePulse Pro." | Professional Edition License (5-Year Update Entitlement). The term "Lifetime" is prohibited. | **CRITICAL** |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Section 1 (Pricing Tiers) | Columns for "Enterprise / MSP Edition" and pricing "$199 USD (Annual subscription)". | Only Free and Professional Editions. No subscriptions or Enterprise/MSP tiers allowed. | **CRITICAL** |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Section 2 (Pro Terms) | "One key allows active activation on up to two devices owned by the licensed user..." | 1 License = 1 PC active activation strictly. | **HIGH** |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Section 1 (Pricing Grid) | Professional Edition Support: "Email Support (48h SLA)". Enterprise: "Priority Chat (8h SLA)". | Best Effort Support only. No SLA time guarantees. | **HIGH** |
| **[support_policy.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/support_policy.md)** | Section 1 (Support SLAs) | Details time-bound SLAs: 48h response for Pro Edition and 8h response for Enterprise/MSP Edition. | Best Effort Support only due to solo developer limitations. | **HIGH** |
| **[support_policy.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/support_policy.md)** | Section 1 & 2 | References to "Enterprise / MSP Edition". | Remove all references to Enterprise/MSP tiers. | **CRITICAL** |
| **[license_agreement.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/license_agreement.md)** | Section 1.1 (Single-User) | Grants rights on "up to two (2) devices concurrently". | 1 License = 1 PC active activation strictly. | **HIGH** |
| **[license_agreement.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/license_agreement.md)** | Section 1.2 & 1.3 | "Multi-Seat / Team License" and "Enterprise & MSP License" descriptions. | Only Free and Professional Editions exist. No team or bulk licenses. | **CRITICAL** |
| **[refund_policy.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/refund_policy.md)** | Section 2 | "The license key will be blacklisted on our validation servers." | Must clarify that both Online and Offline activation blacklists apply (offline licenses will be invalidated upon next contact or in local update files). | **MEDIUM** |
| **[terms_of_service.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/terms_of_service.md)** | Section 4 | References support SLAs by edition tiers. | Change to Best Effort Support. | **HIGH** |
| **[editions_comparison.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/product/editions_comparison.md)** | Grid Column 4 | "Enterprise / MSP Edition" column. | Eliminate Enterprise/MSP tier column entirely. | **CRITICAL** |
| **[editions_comparison.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/product/editions_comparison.md)** | Row 28 & 29 | "Multi-device activations: Up to 2 devices" and "Updates and support: Premium Support". | Align to "1 License = 1 PC" and "Best Effort Support (5-Year Update Entitlement)". | **HIGH** |
| **[index.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/index.html)** | Line 114 | "Secure a lifetime upgrade license..." | Replace with "5-Year Update Entitlement (software remains functional thereafter)". | **CRITICAL** |
| **[founder.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/founder.html)** | Line 52 & 71 | "lifetime feature access", "Lifetime license key: Access all current and future Pro/Enterprise features". | Replace with "5-Year Update Entitlement". Delete "Enterprise" reference. | **CRITICAL** |
| **[pricing.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/pricing.html)** | Pricing comparison table | Grid uses shorthands "Basic (Free)" and "Professional (Pro)" instead of "Free Edition" and "Professional Edition". | Rename categories to official edition terms. | **MEDIUM** |
| **[terms_of_service.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/terms_of_service.md)** | Section 2.2 | "Commercial licenses are restricted based on the tier purchased..." | Replace with "Commercial license keys are restricted to exactly 1 PC activation." | **HIGH** |

---

## 3. Recommended Actions
1.  **Remove "Lifetime"**: Replace all occurrences of "Lifetime Updates/License/Membership" on the website (`index.html`, `founder.html`) and draft guidelines (`founder_program.md`, `community_advisor_program.md`) with the official **"5-Year Update Entitlement"**, explicitly stating that the core application remains fully active offline afterwards.
2.  **Delete "Enterprise / MSP"**: Delete column grids, lists, and sections referencing an Enterprise or MSP edition in `pricing_structure.md`, `support_policy.md`, `license_agreement.md`, and `editions_comparison.md`.
3.  **Enforce 1 License = 1 PC**: Update EULA, EULA-derived pages, and `license_agreement.md` to state that a single license key grants activation rights on exactly 1 PC. Remove the "2-device concurrent" rule.
4.  **Enforce Best Effort Support**: Align `support_policy.md`, `terms_of_service.md`, and website copy to remove 8h/48h response SLAs, setting support strictly to "Best Effort Support".
