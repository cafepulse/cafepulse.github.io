# CafePulse Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0-alpha.1] - 2026-06-21

### Added
- **Linux Distribution Support:** Added GitHub Actions CI/CD configuration `.github/workflows/build-linux.yml` to automatically build Linux releases on Ubuntu runners.
- **Headless PyQt6/PyQtGraph Compilation:** Enabled PyInstaller compilation of PyQt6 apps in headless environments by configuring `QT_QPA_PLATFORM: offscreen` and installing `libxcb-cursor0` system dependency.
- **AppImage Build Integration:** Integrated `appimagetool` to package both `CafePulse_Free.AppImage` and `CafePulse_Professional.AppImage` dynamically.
- **Unified Release Assets:** Bundled portable ZIP archives alongside built AppImages into a unified `exports/` artifact distribution on success.
- **SHA-256 Download Integrity:** Added `generate_sha256.py` script and integrated it into both Windows local build (`build_installer.bat`) and Linux CI/CD (`build-linux.yml`) to automatically output `SHA256SUMS.txt`.

### Changed
- **Final Root Merge [D-015 / D-019]:** Eliminated the `Project/` folder and merged all Python application code (`core/`, `modes/`, `ui/`, `main.py`) directly into the root directory alongside website assets. This resolves AI confusion and locks the directory structure.
- **Website Downloads:** Updated download commands on `download.html` (and localized versions) to use optimized PowerShell scripts (`$ProgressPreference = 'SilentlyContinue'`) and Linux flags (`-O`).
- **Beta Tester Form:** Reverted custom FormSubmit integration and replaced it with a direct CTA to the official Google Form (`forms.gle/VPwQ3jRBySbCEvKX7`) to reduce technical debt and maintain ecosystem stability.
- **Founder Release:** Updated `founder.html` pricing to Rp 299.000 and explicitly changed CTAs to 'Coming Soon' to enforce the delayed launch requirement (D-020).


### Fixed
- **Terminal Flash (CREATE_NO_WINDOW):** Fixed the missing `subprocess.CREATE_NO_WINDOW` patch in `core/scanner/arp_scanner.py` that was lost during previous directory refactoring.
- **Zombie Process Issue:** Migrated thread lifecycle management away from `terminate()` and `wait()` inside workers, using a unified async `GracefulShutdownMonitor` in `main_window.py` to prevent frozen database locks and abandoned sockets.
- **Build Path Resolution:** Updated `build.py`, `build_installer.bat`, and `build-linux.yml` to correctly target the merged root directory instead of `Project/`.

## [1.0.0-RC1.2] - 2026-06-21

### Added
- **Subnet Detection Fallback Chain:** Implemented a robust 6-stage subnet fallback detection in `core/scanner/arp_scanner.py` and `modes/home_wifi/arp_scanner.py`, enabling offline network sweeps without relying on online DNS checks.

### Fixed
- **Home WiFi Scanner Device Count:** Resolved "Device Found = 0" bug during offline local sweeps.
- **CMD Window Flickers:** Hidden transient console flashes during network scans by configuring `STARTUPINFO` hidden flags on system command executions.
- **False Recovery Warnings:** Corrected state tracking for `.clean` and `.lock` files on PyQt6 application shutdown to prevent false recovery warnings.
- **PyInstaller Loader Conflict:** Resolved PyInstaller `pyimod02_importers` `AttributeError` by executing complete cache cleans (`build/` and `dist/` directory purges) prior to building.

## [1.0.0-RC1.1] - 2026-06-21

### Added
- **Project OS AI Framework:** Initialized standardized Project OS AI subfolders inside `artifacts/` (`bible/`, `roadmap/`, `sprint/`, `changelog/`, `decisions/`, `state/`, `sessions/`, `architecture/`) as the Single Source of Truth (SSOT).
- **Code Relation Map:** Created `CODE_RELATION_MAP.md` mapping file trees, module dependencies, database schema, high-risk/safe files, and entry points.

### Changed
- **Centralized Restructuring (Level 3 to Level 2):** Eliminated the nested Level 3 folder (`...\CafePulse\CafePulse\CafePulse\`), centralizing the PyQt6 app codebase into a top-level `Project/` folder.
- **Website Consolidation:** Merged root and Level 3 website pages into the centralized `website/` folder, including localized pages (`de/`, `es/`, `fr/`, `id/`, `ja/`, `zh/`) and JSON translations (`lang/`).
- **License Generator Relocation:** Moved license tools to a top-level `license_generator/` directory, adapting import paths and keys.
- **Output Redirection:** Updated PyInstaller zipping and Inno Setup installer scripts to compile and output setup binaries directly into `exports/`.
- **PDF Compiler Redirection:** Modified the 6 PDF compiler scripts to output compiled PDF documents directly into `artifacts/compiled_pdfs/` rather than polluting the `Project/` directory.

### Fixed
- **Private Key Path:** Moved the developer's private key (`private_key.pem`) to `Project/core/licensing/private_key.pem` to resolve a `FileNotFoundError` during cryptographic license signing.
- **Website i18n Scripts:** Restored deleted translations engine scripts (`js/i18n.js` and `js/checkout_tracker.js`) and relocated them to `website/js/`.

---

## [1.0.0-RC1] - 2026-06-21

### Added
- **Master Reference:** Created `docs/architecture/CAFEPULSE_MASTER_REFERENCE.md` as the absolute source of truth mapping repository nesting, file directories, and strict guidelines for AI agents to prevent directory pollution.
- **Professional Specifications:** Created `docs/specs/FEATURE_SPEC_PROFESSIONAL.md` defining features like MikroTik RouterOS API, IAM guest portals, PyQtGraph Radar diagrams, and ReportLab PDF voucher templates.
- **Documentation Compiler:** Added Section 11 (Master Reference), 12 (Professional Spec), and 13 (Changelog) to the central PDF documentation build process.

### Changed
- **Website Downloads:** Configured website download links on `download.html` to point directly to hosted setup files (`CafePulse_Free_Setup.exe` and `CafePulse_Free_Portable.zip`) within the website repository.

### Fixed
- **ARP Scanner Windows Flickering:** Applied `STARTUPINFO` flags with `wShowWindow = SW_HIDE` to prevent transient command prompt window spawns during periodic network scans.
- **Graceful Shutdown Flags:** Guaranteed writing of `CLEAN_FLAG` file inside `main.py` exit hooks, preventing false-positive recovery warnings on subsequent launches.

---

## [1.0.0-beta] - 2026-06-05

### Added
- **Core Architecture:** Fully isolated offline-first local Python / PyQt6 desktop architecture.
- **Data Persistence:** SQLite3 database configured with WAL mode for concurrency and crash-safe IO.
- **Hardware Locking:** Cryptographically signed Professional licensing mechanism tied to PC hardware (AppId).
- **APPDATA Routing:** Proper Windows Standard separation of read-only Program Files (via PyInstaller `sys._MEIPASS`) and writable `LOCALAPPDATA/CafePulse`.
- **Installer Ecosystem:** Dual-edition (Free & Professional) standalone Inno Setup compilers with clean Uninstaller prompts.
- **Network Observability:** Real-time RouterOS neighbor discovery (MNDP) and interface polling dashboards.
- **Security & Portability:** Standalone `.zip` releases built natively alongside `.exe` installers.

### Changed
- Re-architected all config files to seed from a read-only `settings_default.json` to prevent crashes on fresh installs.
- Removed legacy `tmp/` and hardcoded `C:/Users/...` paths from the entire codebase.

### Fixed
- QThread race condition crash during application shutdown via `CafePulseApplication` cleanup hooks.
- PyInstaller bundling failures by explicitly importing implicit PyQt6 and cryptography DLL dependencies via `CafePulse.spec`.
- Relative path lookup errors in `main.py` causing icons to missing after PyInstaller compilation.

### Removed
- Legacy SaaS code, telemetry, and external database tracking integrations (Strict Offline-First model).
