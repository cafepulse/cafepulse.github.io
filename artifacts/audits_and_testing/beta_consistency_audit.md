# CafePulse Beta Tester Program Consistency Audit
This report compiles conflicts and discrepancies related to the limits, rules, and rewards of the CafePulse Beta Tester Program across all documents and website pages.

---

## 1. Official Beta Program Policy (Source of Truth)
To ensure close feedback loops and quality bug triage, the Beta Tester Program is governed by these official guidelines:
*   **Tester Cap**: Capped strictly at a maximum of **10 active Beta Testers**.
*   **Top Contributor Reward**: **5-Year Professional License** (unlocked for unearthing structural bugs like database lockups, multithreading crashes, or major guide/code contributions).
*   **Contributor Reward**: **1-Year Professional License** (unlocked for documenting and submitting at least **3 validated bugs** with full environment specifications).
*   **Participant Status**: Purely voluntary. Testers are strictly product stability validators and hold no commercial partnership, investment role, or equity.

---

## 2. Identified Beta Tester Program Conflicts

Below is the list of conflicts found in the workspace files regarding the Beta Tester Program:

| File Path | Conflict Area | Existing Text / Conflict | Official Policy Mapping | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **[beta_tester_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/beta_tester_program.md)** | Tester Capacity | Mentions no capacity limits for candidate enrollment. | Capped at **10 active testers** max. | **HIGH** |
| **[beta_tester_program.md](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/docs/business/beta_tester_program.md)** | Reward Terms | Line 34-35: "...report at least three confirmed bugs... receive Free 1-Year Pro License." (No Top Contributor tier). | Establish two-tiered system: **5-Year Professional License** for Top Contributors and **1-Year Professional License** for Contributors. | **HIGH** |
| **[beta.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/beta.html)** | Page Body Text (Tester Cap) | Grid card and description mention no capacity limits. | Add clear note that the program is limited to **10 active testers**. | **HIGH** |
| **[beta.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/beta.html)** | Page Body Text (Rewards) | Line 80-82: "Beta testers who document and submit at least three validated bugs... will receive Free 1-Year Pro License key." | Update text to display the two-tier reward structure (**5-Year Pro** for Top Contributors, **1-Year Pro** for Contributors). | **HIGH** |
| **[beta.html](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/website/beta.html)** | Terminology | References to "Pro License key" instead of "Professional License". | Standardize to **Professional License**. | **MEDIUM** |

---

## 3. Recommended Actions
1.  **Update website copy**: Modify `website/beta.html` (lines 78-85) to declare the 10 active tester cap and clearly layout the 5-Year and 1-Year Professional License rewards based on contribution levels.
2.  **Overwrite old business files**: Replace the content of `docs/business/beta_tester_program.md` with the finalized rules from `docs/beta_program_final.md` which contains correct limits and contribution grids.
3.  **Archive duplicate guidelines**: Archive `docs/beta_program_final.md` and `docs/beta_program_revision.md` from the root `docs/` folder once the business folder is updated to keep a single clean copy in `docs/business/`.
