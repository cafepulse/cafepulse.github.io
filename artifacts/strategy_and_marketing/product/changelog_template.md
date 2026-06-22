# Changelog — CafePulse

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [[Unreleased]]
[Drafting area for future changes not yet published]

### Added
- 
### Changed
- 
### Deprecated
- 
### Removed
- 
### Fixed
- 
### Security
- 

---

## [1.0.0] — 2026-06-02

### Added
- Integrated a premium PyQt6 Splash Screen during startup sequence.
- Added automatic multi-resolution `icon.ico` generation from `logo.png` inside `build.py` using Pillow.
- Created `version_info.txt` to inject file description, version, and copyright details into compiled Windows binary headers.
- Created Inno Setup installer script template `setup_script.iss` and automated builder helper `build_installer.bat`.
- Added high-resolution logo widget display in `AboutPage` layout.

### Changed
- Refactored `main.py` entry point to initialize `QApplication` early so the splash screen can display immediately before validator execution.
- Configured build output structures for Basic and Pro zipped distributions in `build.py`.

### Fixed
- Resolved PyInstaller compile warning related to missing Win32 icon resources.
- Optimized exception handler dialog to close splash screen cleanly before raising the recovery panel.
