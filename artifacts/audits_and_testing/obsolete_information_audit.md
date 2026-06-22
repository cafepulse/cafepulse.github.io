# CafePulse Obsolete Information Audit
This report compiles all outdated policies, obsolete pricing figures, and abandoned licensing models that must be removed from the CafePulse project files.

---

## 1. Inventory of Obsolete Policies & Terms

Below is the list of outdated references that are present in the current documentation drafts and static website HTML files:

| File Path | Component / Section | Obsolete Information Found | Correct Current Policy | Risk / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Membership limits & Price | Capped at **250 slots** at a price of **$49 USD**. | Cap at **100 slots** at **Rp499.000**. | Public confusion and conversion rate loss on launch. |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Section 2 (Benefits) | Offers a **"Lifetime License"** to Pro/Enterprise features. | **5-Year Update Entitlement** to Professional features. Banish "Lifetime" terms. | High legal liability for perpetual compatibility patches. |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Pricing Grid | Lists Pro Edition at **$49 USD** (One-time, perpetual) and lists the **Enterprise / MSP Edition** at **$199 USD** (Annual subscription). | Pro Edition is **Rp499.000** (One-Time). No Enterprise/MSP edition or subscriptions. | Complex pricing matrix; conflicts with solo developer model. |
| **[pricing_structure.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/pricing_structure.md)** | Seat limits | One Pro license allows activation on **2 devices**. | **1 License = 1 PC** strictly. | Spikes in support volume and license sharing. |
| **[support_policy.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/support_policy.md)** | Support channels & SLAs | Details a **48-hour email SLA** for Pro and an **8-hour priority SLA** for Enterprise. | **Best Effort Support** only. No SLA time guarantees. Remove Enterprise tier support. | Unrealistic SLAs for a solo developer. |
| **[community_advisor_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/community_advisor_program.md)** | Privileges | Offers a **"Complementary Lifetime Pro License"**. | Professional License with a **5-Year Update Entitlement**. | Lifetime liability risk. |
| **[license_agreement.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/legal/license_agreement.md)** | Section 1 | Multi-Seat, Team, and Enterprise/MSP licenses. Runs on up to 2 devices. | Only Free and Professional Editions exist. 1 License = 1 PC. | Legal contract mismatch vs actual software behavior. |
| **[editions_comparison.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/product/editions_comparison.md)** | Grid columns | Enterprise/MSP columns. Multi-device activations. Premium Support. | Remove Enterprise/MSP. Set to 1 PC. Best Effort Support. | Marketing inconsistency. |
| **[index.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/index.html)** | Line 114 | Offers a **"lifetime upgrade license"** and **250 spots** cap. | Change to **"5-Year Update Entitlement"** and cap at **100 spots**. | Misleading public ads and legal risks. |
| **[founder.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/founder.html)** | Line 63 & 71 | Capped at **250 memberships**. Offers a **"lifetime license"** and Pro/Enterprise features. | Cap at **100 memberships**. 5-Year Update Entitlement. No Enterprise features. | Misleading public ads and legal risks. |
| **[beta.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/beta.html)** | Line 80-82 | Offers a general **1-Year Pro license** with no tester cap. | Cap at **10 active testers**. Reward is **5-Year Pro** for Top Contributors and **1-Year Pro** for Contributors. | Misleading public ads. |
| **`assets/loago.png`** | File listing | Typo file. | Should be deleted. | Unused asset footprint. |
| **`founder_photo.png`** & **`founder_photo_hd.png`** | File listing | Redundant duplicate images. | Should be deleted. | Unused asset footprint. |

---

## 2. Recommended Strategy for Obsolescence Removal
All obsolete pricing models, USD currency bases, lifetime update windows, and non-existent product editions must be cleaned from the workspace code and docs in the execution phase. This involves:
1.  **Strict Term Filtering**: Use search/replace queries to clean all files of `Lifetime`, `Enterprise Edition`, `MSP Edition`, and `Subscription` terms.
2.  **Updating Website HTML Pages**: Align the copy of `index.html`, `founder.html`, and `beta.html` to reflect correct counters (100 spots, 10 testers) and official IDR currency (**Rp499.000**).
3.  **Correcting Legal and Product Comparators**: Align `eula.md`, `license_agreement.md`, and `editions_comparison.md` to reflect a single workstation activation rule (1 License = 1 PC).
