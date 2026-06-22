# CafePulse Founder Program Consistency Audit
This report compiles conflicts and discrepancies related to the limits, roles, legal boundaries, and definitions of the CafePulse Founder Program across all documents and website pages.

---

## 1. Official Founder Program Policy (Source of Truth)
To align with standard retail deployment and prevent legal liabilities, the Founder Program is governed by these official policies:
*   **Capacity Cap**: Strictly capped at a maximum of **100 Founder Users**.
*   **Legal Standing**: Founders are strictly customers. They are **NOT investors, NOT business partners, NOT shareholders, and NOT affiliates**. They hold zero equity, zero voting rights, and receive no commissions.
*   **Official Definitions**: Founders are strictly defined as:
    1.  **Early Adopters** (who support early local product development)
    2.  **Product Validators** (who help test software builds in real-world scenarios)
    3.  **Community Supporters** (who help seed community discussion and assist peers)

---

## 2. Identified Founder Program Conflicts

Below is the list of conflicts found in the workspace files regarding the Founder Program:

| File Path | Conflict Area | Existing Text / Conflict | Official Policy Mapping | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Membership Cap | Line 25: "The program is limited to the first **250 members**." | Capped at **100 members** max. | **CRITICAL** |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Role Definition | Line 3: Defines members as "...early adopters, solo developers, and network administrators..." | Should explicitly define roles as **Early Adopter, Product Validator, and Community Supporter**. | **HIGH** |
| **[founder_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/founder_program.md)** | Legal Boundaries | Lacks explicit clauses stating that founders are NOT investors, partners, shareholders, or affiliates. | Add legal disclaimers stating that membership grants zero equity, profit-sharing, or commercial partnership. | **HIGH** |
| **[website_content_map.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/website_content_map.md)** | Content Map Outline | Line 13 & 38: Mentions "limited 250-member Founder Program" and "first 250 members." | Update map references to **100 members**. | **MEDIUM** |
| **[index.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/index.html)** | Homepage Banner | Line 114: "...for only Rp499.000 (limited to the first **250 spots**)." | Update to **100 spots**. | **CRITICAL** |
| **[founder.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/founder.html)** | Page Body Text | Line 63: "The program is strictly limited to the first **250 memberships**." | Update copy to **100 memberships**. | **CRITICAL** |
| **[founder.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/founder.html)** | Legal Disclaimers | Lacks explicit disclaimers regarding what a Founder is not. | Add notice clarifying that founders are early adopters and not investors or business partners. | **HIGH** |

---

## 3. Recommended Actions
1.  **Sync counter limits**: Immediately edit `index.html` (line 114) and `founder.html` (line 63) to change the slot limit from **250** to **100**.
2.  **Overwrite old founder guidelines**: Replace the content of `docs/business/founder_program.md` with the finalized terms from `docs/founder_program_final.md` which contains correct cap definitions and legal boundary checks.
3.  **Correct website Content Maps**: Update `docs/website_content_map.md` to reference the 100-user cap instead of 250.
