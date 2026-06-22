# CafePulse — PHASE 5: Installer Readiness Audit
**Generated:** 2026-06-05

---

## CURRENT STATE

Two build mechanisms exist:
1. `build.py` — Python script that runs PyInstaller + creates ZIP packages
2. `CafePulse.spec` — PyInstaller spec file  
3. `assets/branding/setup_script.iss` — Inno Setup script (stub, single edition)
4. `build_installer.bat` — Windows batch script (unreviewed)

---

## PYINSTALLER CONFIGURATION AUDIT

### `CafePulse.spec` — CRITICAL ISSUES

```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],              # ← EMPTY — CRITICAL
    hiddenimports=['routeros_api'],
    ...
)
```

| Issue | Severity | Impact |
|---|---|---|
| `datas=[]` — no assets included | 🔴 CRITICAL | Packaged app has no icons, no themes, no splash. Crashes or shows broken UI. |
| `pathex=[]` — no project root | 🟡 MEDIUM | Relies on working directory. May fail in some build environments. |
| Only `routeros_api` in hiddenimports | 🟠 HIGH | `mac_vendor_lookup` uses data files. `pyqtgraph` may need hidden imports. Missing imports → runtime ImportError. |
| Absolute paths in `version` and `icon` | 🔴 CRITICAL | `C:\Users\USER\...` paths → build fails on any other machine. |
| `console=False` (windowed) | ✅ CORRECT | Silent console window is correct for desktop app. |
| `onedir` mode (via COLLECT) | ✅ CORRECT | Onedir is correct for Inno Setup packaging. |

---

## REQUIRED `datas` ENTRIES

The following must be added to `CafePulse.spec` for a working packaged app:

```python
datas=[
    ('assets/branding/*.png',    'assets/branding'),
    ('assets/branding/*.svg',    'assets/branding'),
    ('assets/branding/*.ico',    'assets/branding'),
    ('assets/screenshots/*.png', 'assets/screenshots'),
    ('config/settings.json',     'config'),        # ← Use a clean default, not dev settings
    ('ui/themes/*.py',           'ui/themes'),     # Ensure theme modules bundle correctly
],
```

Additionally, `mac_vendor_lookup` ships with a vendor database file that must be included:
```python
# Find mac_vendor_lookup data location:
import mac_vendor_lookup, os
print(os.path.dirname(mac_vendor_lookup.__file__))  # → bundle this directory
```

---

## PATH RESOLUTION AFTER PACKAGING

### The Core Problem

When PyInstaller bundles an application:
- The EXE runs from a temp directory (`_MEIXXXXXX`) or the install directory
- `Path(__file__).resolve().parent` correctly points to the bundle root
- BUT relative paths like `Path("config/settings.json")` resolve relative to the **current working directory** (CWD), not the bundle root

`main.py` sets `PROJECT_ROOT = Path(__file__).resolve().parent` ✅ but then uses:
```python
ConfigManager(Path("config/settings.json"))   # ← RELATIVE — BROKEN
DatabaseManager(db_path="cafepulse.db")       # ← RELATIVE — BROKEN
setup_logging(log_dir="logs", ...)            # ← RELATIVE — BROKEN
Path("config/.clean")                         # ← RELATIVE — BROKEN
```

**All relative paths must be replaced with absolute paths using `PROJECT_ROOT` or `APPDATA`.**

---

## WRITABLE vs READ-ONLY DIRECTORIES

### After Inno Setup install to `C:\Program Files\CafePulse\`:

| Directory | Writable? | Fix |
|---|---|---|
| `C:\Program Files\CafePulse\` (root) | ❌ NO (UAC) | Read-only install dir |
| `C:\Program Files\CafePulse\config\` | ❌ NO (UAC) | Move to APPDATA |
| `C:\Program Files\CafePulse\logs\` | ❌ NO (UAC) | Move to APPDATA |
| `C:\Program Files\CafePulse\exports\` | ❌ NO (UAC) | Move to APPDATA |
| `C:\Users\USER\AppData\Roaming\CafePulse\` | ✅ YES | Target location |

### Required path architecture for packaged app:

```
INSTALL_DIR = C:\Program Files\CafePulse\        ← Read-only (binaries, assets)
APPDATA_DIR = %APPDATA%\CafePulse\               ← Writable (user data)
  ├── config/
  │   └── settings.json
  │   └── license.lic
  │   └── .clean
  │   └── .lock
  ├── logs/
  │   └── cafepulse.log
  │   └── crash/
  └── exports/
      └── cafepulse.db
```

---

## CAN APP RUN AFTER PACKAGING?

**Current answer: NO.**

Blockers:
1. `datas=[]` — zero assets bundled → missing icons, splash, themes
2. Relative paths → files created in wrong location
3. `config/` and `logs/` in Program Files → UAC write failure
4. Absolute developer paths in `.spec` → build fails on other machines

**With the fixes listed above, the app WOULD run after packaging.**

---

## CAN IT RUN FROM `C:\Program Files\CafePulse\`?

**With current code: NO.**  
**With path fixes applied: YES.**

The architecture is correct — the problem is exclusively path routing.

---

## `build.py` ASSESSMENT

`build.py` is well-structured:
- Calls PyInstaller programmatically ✅
- Falls back to auto-generating icon.ico from logo.png ✅
- Creates separate Free and Professional distributions ✅
- Copies assets and config into the dist folder ✅

**However:**
- It copies `config/settings.json` as-is (including developer session data like `"edition": "basic"`, `"onboarding.completed": true`, etc.)
- A clean default `config/settings_default.json` should be created and used instead.
- `build.py` does not copy `database/` (correct — DB should not be pre-populated)

---

## INNO SETUP SCRIPT ASSESSMENT

`assets/branding/setup_script.iss`:
- Generic, single-edition script
- `AppURL` points to `cafepulse.com` (wrong)
- No `LicenseFile` section
- No `WelcomeImage` / `HeaderImage` (installer_banner.png and installer_sidebar.png exist in assets but are unused)
- No separate Free/Professional scripts
- No `[Registry]` section (some apps use this to store APPDATA paths)
- No `[Dirs]` section creating APPDATA directories

**This script must be completely rewritten for production.**

---

## INSTALLER READINESS VERDICT

| Check | Result |
|---|---|
| PyInstaller spec includes assets | 🔴 NO |
| Relative paths resolved for packaging | 🔴 NO |
| Writable dirs outside Program Files | 🔴 NO |
| Spec file machine-agnostic | 🔴 NO |
| mac_vendor_lookup data bundled | 🟠 UNVERIFIED |
| Inno Setup script production-ready | 🔴 NO |
| Free vs Professional separation | 🔴 NO |
| Build from clean machine possible | 🔴 NO |

**Overall Installer Readiness: NOT READY. 5 critical fixes required before any installer can be compiled.**

---

*End of Phase 5 — Installer Readiness Audit*
