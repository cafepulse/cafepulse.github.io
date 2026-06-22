# CafePulse — PHASE 8: Download Pipeline Audit
**Generated:** 2026-06-05

---

## CURRENT DOWNLOAD SITUATION

**Simple truth: No downloadable file exists anywhere publicly.**

| Platform | Installer File | GitHub Release | Status |
|---|---|---|---|
| Windows EXE | `CafePulse_Free_Setup.exe` | ❌ No release | 🔴 DOES NOT EXIST |
| Windows Portable | `CafePulse_Portable.zip` | ❌ No release | 🔴 DOES NOT EXIST |
| Linux AppImage | `CafePulse.AppImage` | ❌ No release | 🔴 DOES NOT EXIST |
| Professional EXE | `CafePulse_Professional_Setup.exe` | ❌ No release | 🔴 DOES NOT EXIST |

---

## DOWNLOAD BUTTON ANALYSIS

### `download.html` — All three download buttons:

```html
<a href="https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse_Setup.exe">
<a href="https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse_Portable.zip">
<a href="https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse.AppImage">
```

These URLs follow the GitHub Releases `/latest/download/` pattern, which is correct.  
They will work **automatically** once a GitHub Release named appropriately is published with those exact filenames.

**No code change needed on the website — only the GitHub Release needs to be created.**

---

## BROKEN COMMAND-LINE INSTRUCTIONS

### Windows:
```bash
winget install CafePulse
```
**Status:** 🔴 FAKE — CafePulse is not in the winget catalog. This command will fail.  
**Fix options:**
1. Remove this from the website entirely (simplest)
2. Replace with a direct download script:
   ```powershell
   Invoke-WebRequest -Uri "https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse_Free_Setup.exe" -OutFile "CafePulse_Free_Setup.exe"
   ```

### Linux:
```bash
curl -L -O https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse.AppImage && chmod +x CafePulse.AppImage
```
**Status:** 🔴 INVALID — Linux AppImage has never been created. No Linux build exists.  
**Fix:** Remove Linux download section entirely from V1. Linux support is not part of V1 release scope.

---

## EXACT ACTIONS REQUIRED BEFORE PUBLIC RELEASE

### Priority 1 — Build the Application
```
[ ] Fix CafePulse.spec — add datas=[], fix absolute paths
[ ] Fix main.py — resolve all paths relative to APPDATA / PROJECT_ROOT
[ ] Create config/settings_default.json (clean defaults)
[ ] Run: python build.py
[ ] Verify: dist/CafePulse/CafePulse.exe launches correctly
[ ] Verify: All assets (icon, splash, theme) load in packaged build
```

### Priority 2 — Build the Free Edition Installer
```
[ ] Create installer/free/CafePulse_Free_Setup.iss
[ ] Install Inno Setup 6 (https://jrsoftware.org/isinfo.php)
[ ] Run: ISCC installer/free/CafePulse_Free_Setup.iss
[ ] Verify: exports/CafePulse_Free_Setup.exe created
[ ] Test install on clean Windows 10/11 VM
[ ] Verify: App launches from Program Files after install
[ ] Verify: Settings saved to APPDATA correctly
[ ] Verify: Uninstaller works
```

### Priority 3 — Create GitHub Release
```
[ ] Create GitHub repository at https://github.com/cafepulse/CafePulse
  (or use existing youbellkey/CafePulse repo)
[ ] Create Release: v0.9-beta
[ ] Upload: CafePulse_Free_Setup.exe
[ ] Upload: CafePulse_Free_Portable.zip (optional)
[ ] Write release notes
[ ] Mark as: Pre-release (beta)
```

### Priority 4 — Fix Website
```
[ ] Remove "winget install CafePulse" from download.html
[ ] Remove Linux AppImage section from download.html (V1 = Windows only)
[ ] Update version metadata dynamically or set static v0.9-beta
[ ] Replace SHA-256 line with actual file hash once EXE is built
[ ] Add "v0.9 Beta — Windows Only" badge to download page
[ ] Update pricing.html "Buy Now" / "Get License" flows
```

### Priority 5 — Professional Edition (after Free is validated)
```
[ ] Create installer/professional/CafePulse_Pro_Setup.iss  
[ ] Build Professional installer
[ ] Upload to GitHub Release
[ ] Activate purchase workflow (manual email → license key delivery)
```

---

## DOWNLOAD PAGE TEMPORARY FIX (Before Installers Are Built)

Add a "Coming Soon" banner to `download.html` to prevent user confusion:

```html
<div style="background: #F59E0B20; border: 1px solid #F59E0B; border-radius: 8px; padding: 1rem; margin-bottom: 2rem; text-align: center;">
    <strong>🚧 V1 Release is in preparation.</strong> 
    Installers will be available upon public launch. 
    <a href="./founder.html">Join the Founder Program</a> to get early access.
</div>
```

---

## GITHUB REPOSITORY STATUS

The download URLs reference `github.com/cafepulse/CafePulse`. This repository must:
- Be public (for free downloads)
- Have GitHub Releases enabled
- Have the correct filenames in releases (exact match to `href` URLs in download.html)

---

## DOWNLOAD PIPELINE VERDICT

| Item | Status |
|---|---|
| Installer built | 🔴 NO |
| GitHub Release exists | 🔴 NO |
| Download buttons functional | 🔴 NO |
| `winget` command valid | 🔴 NO |
| Linux AppImage available | 🔴 NO (V1 Windows only) |
| Download page has pre-release warning | 🔴 NOT YET |

**No user can download anything. This is the #1 blocker for public release.**  
**Estimated actions to fix: ~10–15 hours of focused work (build + test + release).**

---

*End of Phase 8 — Download Pipeline Audit*
