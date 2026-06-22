"""
CafePulse — Central Path Resolver
===================================
Single source of truth for all filesystem paths used by CafePulse.

ARCHITECTURE:
  INSTALL_DIR  — Where the application binary and read-only assets live.
                 Dev: project root (source checkout)
                 Packaged: C:\\Program Files\\CafePulse\\

  USER_DATA_DIR — Where all writable user data lives.
                  Dev: project root (for ease of development)
                  Packaged: %LOCALAPPDATA%\\CafePulse\\
                  (LOCALAPPDATA is per-user, writable, no UAC required)

This module must be imported before any other CafePulse module
that touches the filesystem.
"""

import os
import sys
from pathlib import Path


def _is_packaged() -> bool:
    """Detect whether we are running inside a PyInstaller bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def _resolve_install_dir() -> Path:
    """
    Returns the directory where read-only application assets are stored.
    - Packaged (PyInstaller 6+): sys._MEIPASS → the _internal/ folder
      (This is where PyInstaller places all bundled datas files)
    - Dev: project root (directory containing this file → go up two levels)
    """
    if _is_packaged():
        # sys._MEIPASS is the _internal/ temp/onedir folder with all bundled assets
        return Path(sys._MEIPASS)
    # Dev: this file is at core/app_paths.py — go up two levels to project root
    return Path(__file__).resolve().parent.parent


def _resolve_user_data_dir() -> Path:
    """
    Returns the writable user-data directory.
    - Packaged (Windows): %LOCALAPPDATA%\\CafePulse\\
    - Dev: project root (mirrors production layout for easy debugging)
    """
    if _is_packaged():
        local_app_data = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA", "")
        if local_app_data:
            return Path(local_app_data) / "CafePulse"
        # Fallback: home directory if LOCALAPPDATA not set (non-Windows)
        return Path.home() / ".cafepulse"
    # Development: use project root so devs don't need to hunt for files
    return Path(__file__).resolve().parent.parent


# ─── Resolved base directories ────────────────────────────────────────────────

INSTALL_DIR: Path = _resolve_install_dir()
USER_DATA_DIR: Path = _resolve_user_data_dir()


# ─── Read-only asset paths (inside INSTALL_DIR) ───────────────────────────────

ASSETS_DIR: Path = INSTALL_DIR / "assets"
BRANDING_DIR: Path = INSTALL_DIR / "assets" / "branding"

LOGO_PATH: Path = BRANDING_DIR / "logo.png"
SPLASH_PATH: Path = BRANDING_DIR / "splash.png"
ICON_ICO_PATH: Path = BRANDING_DIR / "icon.ico"
ICON_PNG_PATH: Path = BRANDING_DIR / "icon.png"


# ─── Writable user-data paths (inside USER_DATA_DIR) ─────────────────────────

CONFIG_DIR: Path = USER_DATA_DIR / "config"
LOGS_DIR: Path = USER_DATA_DIR / "logs"
CRASH_LOGS_DIR: Path = USER_DATA_DIR / "logs" / "crash"
EXPORTS_DIR: Path = USER_DATA_DIR / "exports"

SETTINGS_FILE: Path = CONFIG_DIR / "settings.json"
LICENSE_FILE: Path = CONFIG_DIR / "license.lic"
CLEAN_FLAG: Path = CONFIG_DIR / ".clean"
LOCK_FILE: Path = CONFIG_DIR / ".lock"
DATABASE_FILE: Path = USER_DATA_DIR / "cafepulse.db"


# ─── Default settings source (read-only, shipped with the app) ────────────────

DEFAULT_SETTINGS_FILE: Path = INSTALL_DIR / "config" / "settings_default.json"


def ensure_user_dirs() -> list[str]:
    """
    Create all required writable directories.
    Returns a list of error strings for any directory that could not be created.
    """
    errors: list[str] = []
    for directory in [CONFIG_DIR, LOGS_DIR, CRASH_LOGS_DIR, EXPORTS_DIR]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            errors.append(f"Cannot create directory '{directory}': {exc}")
    return errors


def seed_settings_if_missing() -> None:
    """
    On first launch, copy the bundled default settings into the user data dir.
    Does nothing if settings already exist.
    """
    if SETTINGS_FILE.exists():
        return
    if DEFAULT_SETTINGS_FILE.exists():
        import shutil
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(DEFAULT_SETTINGS_FILE, SETTINGS_FILE)
        except OSError:
            pass  # config_manager will create defaults from scratch if needed
