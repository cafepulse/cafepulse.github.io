# Root Folder Cleanup Proposal

## 1. Current State Assessment
The CafePulse root directory contains 33 subdirectories and 35 files. This violates standard modern application structure and makes navigation difficult. However, the project is currently operating under a strict "Flat-Root Directory Lock" established during Sprint 7.5 to prevent pathing breaks in PyInstaller and relative imports.

**Core Issues Identified:**
- Mixed concerns: Website files (`index.html`, `css/`, `js/`), Python source code (`core/`, `modes/`), configuration files, and build artifacts (`build/`, `dist/`, `exports/`) all share the same root level.
- Path Dependencies: The application currently uses `Path(__file__).resolve().parent` and relies heavily on exact relative path resolution in `build.py` and PyInstaller (`CafePulse.spec`).

## 2. Proposed Restructuring Architecture
To clean up the root folder without breaking existing decisions, the project should be segmented into three distinct functional areas:

```text
CafePulse/
├── src/                # Python Application Source Code
│   ├── core/
│   ├── modes/
│   ├── ui/
│   ├── main.py
│   └── database/
├── website/            # GitHub Pages Documentation & Landing Site
│   ├── css/
│   ├── js/
│   ├── assets/
│   ├── docs/
│   └── *.html
├── scripts/            # Build & Maintenance Tools
│   ├── build.py
│   ├── generate_sha256.py
│   ├── build_installer.bat
│   └── ...
├── build_env/          # Ignored Build Artifacts (dist, build, exports)
├── artifacts/          # AI Context and Documentation
├── installer/          # Inno Setup Configurations
├── tests/              # Test Suites
├── CafePulse.spec      # PyInstaller Configuration
└── README.md
```

## 3. Implementation Plan & Safe Execution Strategy
To avoid conflicting with the "Flat-Root Directory Lock" decision, the cleanup must be performed in isolated, verified phases:

**Phase 1: CI/CD & Build Pipeline Refactoring**
- Update `.github/workflows` to map to the new `website/` directory if GitHub Pages uses it.
- Modify `build.py` and `build_installer.bat` to recognize `src/` and output properly without breaking `sys._MEIPASS` pathing in PyInstaller.
- Update `CafePulse.spec` to bundle from `src/`.

**Phase 2: Source Code Path Updates**
- Modify all internal path resolution logic (e.g., loading databases, configurations, assets) to handle the new directory depth.
- **Critical Risk:** `core/utils/` and `modes/` heavily rely on absolute parent traversing. This will require widespread replacement of `Path(__file__).parent.parent` mapping.

**Phase 3: GitHub Pages Redirection**
- If the repository root is serving GitHub pages, moving `.html` files to `website/` will break the site unless GitHub Pages is reconfigured to serve from the `/website` directory (requires a GitHub settings change, not just a repo change).

## 4. Recommendation
**Do NOT proceed with the cleanup at this exact moment.**
We are currently in Sprint 8 (Website Release Readiness). Executing this massive directory shift now will destabilize the PyInstaller build, the AppImage creation pipeline, and the live GitHub Pages website right before the Founder/Beta release.

**Action Item:** Schedule the Root Folder Cleanup as the primary objective for **Sprint 9 (Architecture Refactoring Phase)** after the Beta successfully launches and stability is confirmed.
