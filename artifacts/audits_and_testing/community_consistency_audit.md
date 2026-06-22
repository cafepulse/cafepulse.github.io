# CafePulse Community Consistency Audit
This report compiles all contradictions, discrepancies, and limit mismatches found in community programs (Discord, Founder Program, Beta Tester Program, and Community Advisor Program).

---

## 1. Summary of Community Program Alignments

| Program | Element / Location | Outdated Mismatch | Official Policy (Source of Truth) | Risk / Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Founder Program** | `founder_program.md` | Limited to first **250 members**. | Limited to first **100 members**. | **CRITICAL** |
| **Founder Program** | `founder.html` | Limited to first **250 members**. | Limited to first **100 members**. | **CRITICAL** |
| **Founder Program** | `founder_program.md` | Offers **Lifetime License** to all Pro/Enterprise features. | Offers Professional License with **5-Year Update Entitlement**. No Enterprise tier. | **CRITICAL** |
| **Beta Program** | `beta_tester_program.md` | Unlimited enrollment. | Strict cap of **10 active Beta Testers**. | **HIGH** |
| **Beta Program** | `beta_tester_program.md` | Offers a single reward tier of **1-Year Pro License**. | Two-tier reward system: **5-Year Pro** for Top Contributors and **1-Year Pro** for Contributors. | **HIGH** |
| **Beta Program** | `beta.html` | Unlimited enrollment. Offers only a 1-Year Pro license. | Capped at 10 active testers. Offers 5-Year and 1-Year rewards. | **HIGH** |
| **Community Advisor** | `community_advisor_program.md` | Offers a **"Complementary Lifetime Pro License"** and "quarterly roundtables" with developers. | Purely voluntary role. Reward is standard Professional License (**5-Year Update Entitlement**). The term "Lifetime" is banned. | **HIGH** |
| **Discord Server** | `discord_architecture.md` | Good alignment. Defines the Founder role for 100 members and Beta Tester role for 10 testers. | Matches the final target guidelines. | **LOW** |

---

## 2. Program-Specific Inconsistencies

### 2.1 The Founder Program
*   **Conflict**: The early business drafts (`founder_program.md` and website maps) assumed a limit of 250 spots and lifetime updates.
*   **Resolution**: The official cap is **100 users** with a **5-Year Update Entitlement**. The website must be immediately edited to prevent the public from assuming they can buy 250 lifetime licenses.

### 2.2 The Beta Tester Program
*   **Conflict**: The old guidelines (`beta_tester_program.md` and `beta.html` submit page) offered a 1-Year Pro license for reporting 3 bugs, with no candidate cap.
*   **Resolution**: Cap candidates at **10 active testers** to allow the developer to manage bug triages effectively. Incentivize high-level contributions by offering a **5-Year Pro license to Top Contributors** (structural crashes, memory leak unearthing) and a **1-Year Pro license to standard Contributors** (submitting 3 validated bugs).

### 2.3 The Community Advisor Program
*   **Conflict**: The draft guidelines (`community_advisor_program.md`) offered advisors a "Complementary Lifetime Pro License" and implied a partner/shareholder status with quarterly roundtables.
*   **Resolution**: Define advisors strictly as voluntary product guides. Change the reward to a standard Professional License containing a **5-Year Update Entitlement** (not Lifetime).

---

## 3. Recommended Actions
1.  **Sync Web Copy**: Edit `founder.html` and `beta.html` to update membership slot counts and reward tiers.
2.  **Overwrite old drafts**: Replace outdated `.md` files under `docs/business/` (`founder_program.md`, `beta_tester_program.md`, and `community_advisor_program.md`) with the correct, validated parameters to establish a single source of truth.
