# CafePulse Document Duplication Audit
This report compiles all instances of identical content, overlapping files, and redundant assets, providing clear operational recommendations (**Keep, Merge, Archive, or Delete**).

---

## 1. Inventory of Redundancy & Duplications

We identified several duplicate documentation files and binary assets during the audit:

| Item Name / Path | Duplicate / Overlapping File | Nature of Duplication / Overlap | Recommended Action | Justification |
| :--- | :--- | :--- | :--- | :--- |
| **`docs/business/founder_program.md`** | `docs/founder_program_final.md` & `docs/founder_program_revision.md` | Contains outdated draft terms ($49, 250 spots, lifetime) while the `final` and `revision` files in the root docs directory contain the correct approved parameters (100 spots, Rp499.000). | **Merge & Delete** | Merge `founder_program_final.md` into `docs/business/founder_program.md` (overwriting the old draft), then delete `founder_program_final.md` and `founder_program_revision.md` from the root `docs/` directory. |
| **`docs/business/beta_tester_program.md`** | `docs/beta_program_final.md` & `docs/beta_program_revision.md` | Contains outdated tester rewards and no tester cap. The `final` and `revision` files in the root docs directory contain the correct cap (10 active) and reward tiers. | **Merge & Delete** | Merge `beta_program_final.md` into `docs/business/beta_tester_program.md` (overwriting the old draft), then delete `beta_program_final.md` and `beta_program_revision.md` from the root `docs/` directory. |
| **`assets/loago.png`** | `assets/branding/logo.png` | Misspelled name ("loago.png") containing the logo symbol. It is not referenced anywhere. | **Delete** | Eliminate to clean the root assets folder and save 2.1 MB of space. |
| **`assets/branding/founder_photo.png`** & **`founder_photo_hd.png`** | `assets/branding/founder_youbellkey.png` | Exact binary duplicates of the founder's portrait avatar image (1.9 MB each). | **Delete** | Keep only the official `founder_youbellkey.png` used by the About Page and website layout plans. Delete the other two duplicates to free 3.8 MB of disk space. |
| **`docs/architecture/full roadmap of cafepulse.md`** | `docs/MASTER_PRODUCT_RELEASE_ROADMAP.md` | Older, unstructured roadmap. `MASTER_PRODUCT_RELEASE_ROADMAP.md` is the officially locked release roadmap. | **Archive** | Archive the older file to prevent confusion, and keep the locked `MASTER_PRODUCT_RELEASE_ROADMAP.md` as the single source of truth. |
| **`docs/phase5/business_consistency_audit.md`** | New master consistency reports | Contains older business consistency notes that are fully integrated into the new master reports. | **Archive** | Move `business_consistency_audit.md` to an archive folder after developer approval of the new master reports. |

---

## 2. Action Plan for Clean-Up
Once developer approval is obtained:
1.  **Founder Program Merge**: Copy the text from `docs/founder_program_final.md` and overwrite `docs/business/founder_program.md`. Remove `docs/founder_program_final.md` and `docs/founder_program_revision.md`.
2.  **Beta Tester Program Merge**: Copy the text from `docs/beta_program_final.md` and overwrite `docs/business/beta_tester_program.md`. Remove `docs/beta_program_final.md` and `docs/beta_program_revision.md`.
3.  **Binary Asset Cleanup**: Delete `assets/loago.png`, `assets/branding/founder_photo.png`, and `assets/branding/founder_photo_hd.png` from the filesystem.
4.  **Roadmap Archiving**: Move `docs/architecture/full roadmap of cafepulse.md` to a `/docs/archive/` folder.
