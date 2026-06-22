# -*- mode: python ; coding: utf-8 -*-
"""
CafePulse — PyInstaller Build Specification
============================================
Generates a onedir Windows build with all required assets.

Usage:
    pyinstaller CafePulse.spec --noconfirm

Output:
    dist/CafePulse/CafePulse.exe   (and supporting files)
"""

import sys
from pathlib import Path

# ─── Project root is the directory containing this spec file ──────────────────
SPEC_DIR = Path(SPECPATH)  # PyInstaller provides SPECPATH automatically

# ─── Asset paths (relative to project root) ───────────────────────────────────
BRANDING_DIR = SPEC_DIR / "assets" / "branding"
SCREENSHOTS_DIR = SPEC_DIR / "assets" / "screenshots"
CONFIG_DIR = SPEC_DIR / "config"

ICON_PATH = str(BRANDING_DIR / "icon.ico")
VERSION_INFO_PATH = str(BRANDING_DIR / "version_info.txt")

# ─── Data files to bundle (source, destination inside the bundle) ─────────────
#   Format: (source_path_or_glob, destination_dir_relative_to_bundle_root)
added_files = [
    # Branding assets
    (str(BRANDING_DIR / "logo.png"),             "assets/branding"),
    (str(BRANDING_DIR / "logo.svg"),             "assets/branding"),
    (str(BRANDING_DIR / "logo_dark.png"),        "assets/branding"),
    (str(BRANDING_DIR / "logo_light.png"),       "assets/branding"),
    (str(BRANDING_DIR / "splash.png"),           "assets/branding"),
    (str(BRANDING_DIR / "icon.ico"),             "assets/branding"),
    (str(BRANDING_DIR / "icon.png"),             "assets/branding"),
    (str(BRANDING_DIR / "installer_banner.png"), "assets/branding"),
    (str(BRANDING_DIR / "installer_sidebar.png"),"assets/branding"),
    (str(BRANDING_DIR / "founder_youbellkey.png"),"assets/branding"),
    # App screenshots (used by the About/Product info pages in the UI)
    (str(SCREENSHOTS_DIR / "dashboard.png"),              "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "network_discovery.png"),      "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "network_monitoring.png"),     "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "product_network.png"),        "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "product_operations.png"),     "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "product_business.png"),       "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "settings_license.png"),       "assets/screenshots"),
    (str(SCREENSHOTS_DIR / "settings_about.png"),         "assets/screenshots"),
    # Default config (seed for first-time launch via app_paths.seed_settings_if_missing)
    (str(CONFIG_DIR / "settings_default.json"), "config"),
]

# Filter out any entries where the source file does not exist
# (guards against optional assets missing during CI builds)
valid_files = [(src, dst) for src, dst in added_files if Path(src).exists()]

# ─── Analysis ─────────────────────────────────────────────────────────────────
from PyInstaller.utils.hooks import collect_all

np_datas, np_binaries, np_hidden = collect_all('numpy')
pqg_datas, pqg_binaries, pqg_hidden = collect_all('pyqtgraph')

a = Analysis(
    [str(SPEC_DIR / "main.py")],
    pathex=[str(SPEC_DIR)],
    binaries=np_binaries + pqg_binaries,
    datas=valid_files + np_datas + pqg_datas,
    hiddenimports=[
        "routeros_api",
        "mac_vendor_lookup",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "PyQt6.QtNetwork",
        "cryptography",
        "cryptography.fernet",
        "psutil",
    ] + np_hidden + pqg_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy packages we don't use
        "tkinter",
        "matplotlib",
        "scipy",
        "notebook",
        "IPython",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CafePulse",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Version info and icon — use relative-style via SPEC_DIR (portable across machines)
    version=VERSION_INFO_PATH if Path(VERSION_INFO_PATH).exists() else None,
    icon=ICON_PATH if Path(ICON_PATH).exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="CafePulse",
)
