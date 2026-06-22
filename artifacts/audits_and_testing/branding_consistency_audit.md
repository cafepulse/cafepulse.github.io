# CafePulse Branding Consistency Audit
This report compiles visual design inconsistencies, asset mismatches, naming errors, and metadata discrepancies across all branding resources of CafePulse (logo, icon, website, about page, installer, and splash screen).

---

## 1. Inventory & Health Check of Branding Assets

A visual and structural audit of files under `assets/branding/` and the root `assets/` directories was conducted. Below are the findings:

*   **Typo File Name**: `assets/loago.png` (2.1 MB) is present at the root assets directory. It contains the standard logo but is misspelled ("loago.png") and is not referenced anywhere in the source code or website pages.
*   **Icon Ratio Violation (`icon.ico`)**: The file `assets/branding/icon.ico` is compiled at **256 x 171** pixels (a 3:2 aspect ratio). Standard Windows applications require square **1:1** multi-resolution icons (containing 16x16, 32x32, 48x48, 64x64, and 256x256 sub-buffers) to prevent stretching, distortion, or clipping on taskbars and shortcuts.
*   **Logo Canvas Padding Overhead**: `logo.png`, `logo_dark.png`, and `logo_light.png` are saved at **1536 x 1024** pixels. Most of this area consists of transparent or white padding space. In UI modules (e.g. `about_page.py`), when PyQt6 loads this asset, the logo appears extremely small because the layout compiles the outer canvas bounds rather than the actual symbol.
*   **Duplicate Founder Photos**: The files `founder_photo.png`, `founder_photo_hd.png`, and `founder_youbellkey.png` (each 1.9 MB) are exact binary duplicates of the same portrait. The official asset referenced in the phase 5 blueprint is `founder_youbellkey.png`.
*   **Copyright Year Mismatches**:
    *   Root `LICENSE.txt` lists: `Copyright (c) 2025 CafePulse`.
    *   `assets/branding/version_info.txt` lists: `StringStruct(u'LegalCopyright', u'Copyright (c) 2025 CafePulse')`.
    *   Official legal documents and Phase 5 about pages specify `2026` as the current active copyright year.
*   **Website Translation Inconsistency**:
    *   `website/about.html` uses Indonesian headers: **"Our Visi & Filosofi"** and title **"About CafePulse — Operations & Visi"** on an otherwise fully English webpage.

---

## 2. Desktop Application Sizing & Scale Issues

According to the **Branding Scale Revision Plan (Revision 3.0)**, CafePulse branding elements require a **300% visual scale boost** inside the desktop app layout coordinates:

1.  **Startup Splash Screen**:
    *   *Current*: Logo is scaled to `80x80` pixels. Slogan text is `11px`.
    *   *Target (+300%)*: Increase logo to `240x240` pixels, slogan to `14px`, and title to `36px` bold.
2.  **About Page Widget**:
    *   *Current*: Logo is scaled to `96x96` pixels. Title is `32px`.
    *   *Target (+300%)*: Scale logo to `288x288` pixels on a transparent background, slogan to `16px`.
3.  **Windows Installer (Inno Setup)**:
    *   *Current*: The installer is compiled using standard small assets.
    *   *Target*: Apply Inno Setup settings to crop `installer_sidebar.png` and `installer_banner.png` (originally `1536x1024`) to standard ratios (`499x312` and `79x29` respectively) without stretching them.

---

## 3. Recommended Actions
1.  **Clean Duplicate & Misspelled Files**: Delete `assets/loago.png` and duplicate photos `founder_photo.png` / `founder_photo_hd.png`. Keep only `assets/branding/founder_youbellkey.png`.
2.  **Re-Compile `icon.ico`**: Re-generate `icon.ico` using a standard square 1:1 multi-resolution canvas containing all required Windows sub-resolutions.
3.  **Update Copyright Years**: Update `LICENSE.txt` and `version_info.txt` to state `Copyright (c) 2026 CafePulse`.
4.  **Fix Website Slogans**: Replace "Our Visi & Filosofi" with **"Our Vision & Philosophy"** in `website/about.html`.
5.  **Boost UI Branding Scales**: Modify `ui/widgets/splash_screen.py` and `ui/widgets/about_page.py` to boost logo dimensions by 300%.
