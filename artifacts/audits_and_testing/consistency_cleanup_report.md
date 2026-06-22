# CafePulse Consistency Cleanup & Synchronization Report

**Revision:** 1.0  
**Date:** June 3, 2026  
**Final Status:** **CONSISTENT**

---

## 1. Daftar File yang Diperbaiki (List of Files Fixed)

| File Path | Description |
| :--- | :--- |
| **`LICENSE.txt`** | Updated copyright year to 2026, renamed Basic Edition and locked Pro limits. |
| **`assets/branding/version_info.txt`** | Updated copyright year to 2026. |
| **`docs/business/founder_program.md`** | Overwritten with the final policies. |
| **`docs/business/beta_tester_program.md`** | Overwritten with the final guidelines. |
| **`docs/business/community_advisor_program.md`**| Updated to remove Lifetime references and limit Pro license. |
| **`docs/business/pricing_structure.md`** | Removed Enterprise tier and updated pricing / activation parameters. |
| **`docs/business/support_policy.md`** | Removed Enterprise section and defined support as Best Effort. |
| **`docs/legal/eula.md`** | Standardized naming to Free Edition. |
| **`docs/legal/license_agreement.md`** | Enforced 1 PC limit, deleted Multi-Seat/Enterprise, and updated privacy terms. |
| **`docs/legal/refund_policy.md`** | Standardized naming to Free Edition. |
| **`docs/legal/terms_of_service.md`** | Updated support levels, renamed editions, and restricted activation limits. |
| **`docs/product/editions_comparison.md`** | Removed Enterprise column and updated grid specifications. |
| **`docs/website_content_map.md`** | Updated slots limits, pricing, and rewards details. |
| **`docs/founder_sales_funnel.md`** | Replaced Lifetime with 5-Year Update Entitlement. |
| **`docs/cafepulse_launch_checklist.md`** | Marked WEB-02 and WEB-03 tasks as complete. |
| **`README_FREE.md`** | Created with correct product terms (renamed from `README_BASIC.md`). |
| **`README_PROFESSIONAL.md`** | Created with correct product terms (renamed from `README_PRO.md`). |
| **`website/index.html`** | Corrected founder banner counter (100 spots) and updates entitlement (5-Year). |
| **`website/founder.html`** | Replaced Lifetime with 5-Year updates, set 100 slots, and added legal disclaimer. |
| **`website/beta.html`** | Capped testers at 10 active, updated two-tier rewards list. |
| **`website/pricing.html`** | Renamed Basic/Pro to Free Edition/Professional Edition and updated headers. |
| **`website/about.html`** | Translated "Visi & Filosofi" to "Vision & Philosophy" and "Visi" to "Vision". |
| **`ui/widgets/about_page.py`** | Programmatic padding cropper (+300% logo boost), updated avatar, renamed editions. |
| **`ui/widgets/sidebar.py`** | Programmatic padding cropper, correct aspect ratio scaling, renamed editions. |
| **`ui/widgets/license_page.py`** | Updated returning warning copy. |
| **`ui/widgets/devices_page.py`** | Updated Basic limit warning copy to Free Edition. |
| **`build.py`** | Updated distribution targets to Free/Professional and added Pillow square ico padding. |

---

## 2. Daftar Konflik yang Diselesaikan (List of Conflicts Resolved)

- **C-01 (Lifetime vs 5-Year Update Entitlement)**: Removed all promises of "Lifetime Updates" or "Lifetime License" from websites, founder guidelines, EULAs, and advisor terms. Replaced with a **5-Year Update Entitlement** with a clear explanation that the software remains fully functional offline locally after the entitlement expires.
- **C-02 (Founder Cap Discrepancy)**: Updated the maximum number of Founders from 250 to **100 spots** across all files (`founder.html`, `index.html`, etc.).
- **C-03 (USD Pricing Mismatch)**: Updated all main references to Professional Edition cost to **Rp499.000 (One-Time Purchase)**. USD pricing ($49) was moved to references/international estimates only.
- **C-04 (Unapproved Enterprise/MSP Tiers)**: Deleted all Enterprise/MSP columns, annual subscription prices ($199/yr), and multi-seat terms across all documents and website cards.
- **H-01 (Workstation Activation Limits)**: Changed concurrent activations from 2 devices to strictly **1 License = 1 PC** bound.
- **H-02 (Support SLAs vs Best Effort)**: Removed the 48-hour (Pro) and 8-hour (Enterprise) response guarantees, redefining support as **Best Effort Support** via email and Discord due to solo developer parameters.
- **H-03 (Beta Program Tester Cap & Rewards)**: Capped active beta testers at **10 active candidates**, and defined the official two-tier reward structure (5-Year Professional License for Top Contributors, 1-Year Professional License for Contributors).
- **H-04 (Community Advisor Program)**: Replaced "Complementary Lifetime Pro License" and partner status with voluntary help and a standard Professional license with 5-Year Update Entitlement.
- **M-01 (Indonesian Web Headings)**: Translated "Visi & Filosofi" to "Vision & Philosophy" and "Operations & Visi" to "Operations & Vision" on the About page.
- **M-02 (Icon Aspect Ratio)**: Fixed blurry desktop shortcut stretching by padding `icon.ico` to a standard 1:1 canvas.
- **M-03 (EULA Edition Naming)**: Replaced "Free/Basic" with "Free Edition" inside the EULA and Refund Policy.

---

## 3. Daftar Istilah yang Diganti (List of Terms Replaced)

- `Basic / Basic Edition` ➔ `Free Edition`
- `Pro / Pro Edition` ➔ `Professional Edition`
- `Lifetime updates` / `Lifetime license` ➔ `5-Year Update Entitlement`
- `250 spots` ➔ `100 spots`
- `$49 USD` (Main Pricing) ➔ `Rp499.000` (Main Pricing, with USD for reference)
- `$199 USD` Annual Subscription ➔ Removed
- `2 devices concurrent` ➔ `1 PC locked active activation`
- `Support SLA (48h/8h)` ➔ `Best Effort Support`
- `Visi & Filosofi` ➔ `Vision & Philosophy`

---

## 4. Daftar File & Aset yang Dibersihkan (List of Files & Assets Cleaned)

- **Misspelled File Deleted**: `assets/loago.png` (2.1 MB)
- **Duplicate Assets Deleted**:
  - `assets/branding/founder_photo.png` (1.9 MB)
  - `assets/branding/founder_photo_hd.png` (1.9 MB)
  - `website/assets/founder_photo.png` (1.9 MB)
  - `website/assets/founder_photo_hd.png` (1.9 MB)
- **Roadmap Draft Archived**: Moved `docs/architecture/full roadmap of cafepulse.md` to `docs/archive/full roadmap of cafepulse.md`.
- **Duplicate Final Policy Drafts Deleted**:
  - `docs/founder_program_final.md` and `docs/founder_program_revision.md`
  - `docs/beta_program_final.md` and `docs/beta_program_revision.md`

---

## 5. Ringkasan Sinkronisasi (Synchronization Summaries)

### 5.1 Website
All pages under `website/` (`index.html`, `pricing.html`, `founder.html`, `beta.html`, `about.html`) were synchronized with the official pricing cards, edition limitations, and legal guidelines. Disclaimers were added to explain the role of Founders as supporters, not partners/investors. Indonesian placeholders were translated to English.

### 5.2 Dokumentasi
All markdown files inside `docs/` and its subfolders were cleaned of deprecated terms (Enterprise/MSP editions, SLAs, USD models). Readme files were renamed to `README_FREE.md` and `README_PROFESSIONAL.md`.

### 5.3 Lisensi
The root `LICENSE.txt` and python licensing indicators were updated to reflect the workstation limit of exactly 1 PC, a 5-Year Update Entitlement, and a 2026 copyright year. Privacy policies and license agreements were updated to clarify that local machine checks use hardware hashes during activation without sending telemetry.

### 5.4 Branding
Programmatic margins cropping was added to `about_page.py` and `sidebar.py` to ensure the logo is rendered cleanly and scaled smoothly to standard size ratios (+300% visual boost). Desktop shortcuts were fixed by regenerating `icon.ico` into a square 1:1 format. Duplicate photos were deleted, leaving `founder_youbellkey.png` as the single portrait asset.

---

## 6. Status Akhir (Final Status)

**CONSISTENT**
The entire CafePulse ecosystem is now aligned to a single, unified source of truth and is fully prepared for the Founder Program rollout.
