"""
CafePulse — Config Manager
JSON-based configuration with safe read/write and validation.
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Any
from core.app_paths import SETTINGS_FILE as _DEFAULT_SETTINGS

logger = logging.getLogger("cafepulse.config")

# P0 Fix: Use resolved path from app_paths (works in both dev and packaged mode)
DEFAULT_CONFIG_PATH = _DEFAULT_SETTINGS


class ConfigManager:
    """
    Manages application configuration stored in a JSON file.
    Thread-safe for reading; writes should happen from main thread only.
    """

    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        self._path = Path(config_path)
        self._data: dict = {}
        self._load()

    # ─── Internal ─────────────────────────────────────────────────────────────

    def _load(self) -> None:
        """Load config from disk. Falls back to defaults on any error."""
        if not self._path.exists():
            logger.warning("Config file not found at %s — using defaults", self._path)
            self._data = {}
            return

        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                self._data = json.load(fh)
            logger.info("Config loaded from %s", self._path)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load config: %s — using defaults", exc)
            self._backup_corrupt()
            self._data = {}

    def _backup_corrupt(self) -> None:
        """Rename a corrupt config file so it is not lost."""
        backup = self._path.with_suffix(".json.bak")
        try:
            shutil.copy2(self._path, backup)
            logger.info("Corrupt config backed up to %s", backup)
        except OSError:
            pass

    # ─── Public API ───────────────────────────────────────────────────────────

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get a nested value using dot-path keys.
        Example: config.get("app", "version", default="0.0.0")
        """
        node = self._data
        for key in keys:
            if not isinstance(node, dict):
                return default
            node = node.get(key, None)
            if node is None:
                return default
        return node

    def set(self, *keys: str, value: Any) -> None:
        """Set a nested value and persist to disk."""
        if len(keys) == 0:
            return
        node = self._data
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        node[keys[-1]] = value
        self._save()

    def _save(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=4)
            logger.debug("Config saved to %s", self._path)
        except OSError as exc:
            logger.error("Failed to save config: %s", exc)

    def all(self) -> dict:
        """Return a shallow copy of the full config dict."""
        return dict(self._data)
