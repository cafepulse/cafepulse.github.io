"""
CafePulse — Logging System
Centralized logging configuration with file rotation and console output.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path


# ─── Global logger instance ───────────────────────────────────────────────────
_initialized = False
_app_logger = None


def get_logger(name: str = "cafepulse") -> logging.Logger:
    """Return a named child logger under the root 'cafepulse' logger."""
    return logging.getLogger(name)


def setup_logging(
    log_dir: str | Path | None = None,
    level: str = "INFO",
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Initialize the CafePulse logging system.
    Safe to call multiple times — only initializes once.
    """
    global _initialized, _app_logger

    if _initialized:
        return _app_logger

    if log_dir is None:
        raise ValueError("log_dir must be provided to setup_logging")

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "cafepulse.log"

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Root 'cafepulse' logger
    logger = logging.getLogger("cafepulse")
    logger.setLevel(numeric_level)
    logger.propagate = False  # prevent double logging

    # ── Formatter ────────────────────────────────────────────────────────────
    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Rotating File Handler ────────────────────────────────────────────────
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
    except OSError as exc:
        print(f"[WARN] Cannot write log file at {log_file}: {exc}", file=sys.stderr)

    # ── Console Handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    _initialized = True
    _app_logger = logger
    logger.info("Logging system initialized — level=%s, file=%s", level, log_file)
    return logger
