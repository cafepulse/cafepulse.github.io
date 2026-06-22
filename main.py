"""
CafePulse — Application Entry Point
Startup validation → logging → config → database → UI launch
"""

import sys
import os
import traceback
import logging
from pathlib import Path

# ─── Ensure project root is on path ───────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ─── Central path resolver (must be imported first) ───────────────────────────
from core.app_paths import (
    INSTALL_DIR, USER_DATA_DIR,
    LOGS_DIR, CRASH_LOGS_DIR, EXPORTS_DIR,
    CONFIG_DIR, SETTINGS_FILE, LICENSE_FILE,
    CLEAN_FLAG, LOCK_FILE, DATABASE_FILE,
    LOGO_PATH, SPLASH_PATH, ICON_ICO_PATH, ICON_PNG_PATH,
    ensure_user_dirs, seed_settings_if_missing,
)

# ─── Early logging (before config) ───────────────────────────────────────────
from core.logging_system import setup_logging
_bootstrap_logger = setup_logging(log_dir=LOGS_DIR, level="INFO")
logger = logging.getLogger("cafepulse.main")


# ─── Global Exception Handler ─────────────────────────────────────────────────

def _global_exception_handler(exc_type, exc_value, exc_tb):
    """Catch any unhandled exception, log it to crash folder, show smart dialog, never silently crash."""
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.critical("Unhandled exception:\n%s", tb_text)
    
    # 1. Write crash log
    try:
        from datetime import datetime
        CRASH_LOGS_DIR.mkdir(parents=True, exist_ok=True)
        crash_file = CRASH_LOGS_DIR / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(crash_file, "w", encoding="utf-8") as f:
            import platform
            f.write(f"CafePulse Crash Log\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write(f"OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"{'-'*40}\n")
            f.write(tb_text)
    except Exception:
        pass

    # 2. Show Smart Qt dialog if app is running
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.dialogs.error_dialog import show_smart_error
        app = QApplication.instance()
        if app:
            show_smart_error(
                title="Aplikasi Berhenti (Crash)",
                message=str(exc_value),
                exc_type=exc_type.__name__,
                tb_text=tb_text
            )
    except Exception:
        pass

sys.excepthook = _global_exception_handler


# ─── Startup Validator ────────────────────────────────────────────────────────

class StartupValidator:
    """
    Validates the environment before launching the UI.
    Returns (ok: bool, errors: list[str])
    """

    def run(self, splash=None) -> tuple[bool, list[str]]:
        import time
        errors: list[str] = []

        if splash:
            splash.set_status("Memeriksa versi Python...", 15)
            time.sleep(0.15)
        errors += self._check_python_version()

        if splash:
            splash.set_status("Mempersiapkan direktori pengguna...", 30)
            time.sleep(0.15)
        errors += ensure_user_dirs()

        if splash:
            splash.set_status("Menyiapkan konfigurasi awal...", 45)
            time.sleep(0.15)
        seed_settings_if_missing()

        if splash:
            splash.set_status("Memuat berkas konfigurasi...", 55)
            time.sleep(0.15)
        # Config existence is not an error — defaults used if missing

        if splash:
            splash.set_status("Memeriksa pustaka dependensi...", 75)
            time.sleep(0.15)
        errors += self._check_dependencies()

        if splash:
            splash.set_status("Menguji hak akses menulis...", 90)
            time.sleep(0.15)
        errors += self._check_writable_dirs()

        ok = len(errors) == 0
        if ok:
            logger.info("Startup validation passed ✓")
        else:
            for err in errors:
                logger.error("Startup validation: %s", err)
        return ok, errors

    def _check_python_version(self) -> list[str]:
        if sys.version_info < (3, 12):
            return [f"Python 3.12+ required, got {sys.version}"]
        return []

    def _check_dependencies(self) -> list[str]:
        errs = []
        try:
            from core.runtime.dependency_registry import DependencyRegistry
            missing_required, missing_optional = DependencyRegistry.check_all()
            for dep in missing_required:
                errs.append(
                    f"Pustaka Inti '{dep.pypi_name}' ({dep.import_name}) tidak terinstall. "
                    f"Solusi: {dep.install_command}"
                )
            for dep in missing_optional:
                logger.info(
                    "Pustaka Opsional '%s' tidak ditemukan. Fitur ini akan dimatikan secara anggun "
                    "jika diakses. Solusi: %s",
                    dep.pypi_name, dep.install_command,
                )
        except Exception as exc:
            errs.append(f"Gagal melakukan audit dependensi: {exc}")
        return errs

    def _check_writable_dirs(self) -> list[str]:
        errs = []
        for directory in [LOGS_DIR, EXPORTS_DIR]:
            test_file = directory / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except OSError as exc:
                errs.append(f"Directory '{directory}' is not writable: {exc}")
        return errs


# ─── Safe Mode Window ─────────────────────────────────────────────────────────

def launch_safe_mode(errors: list[str]) -> None:
    """Minimal recovery window shown when startup validation fails."""
    from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
    from PyQt6.QtCore import Qt

    app = QApplication.instance() or QApplication(sys.argv)

    dlg = QDialog()
    dlg.setWindowTitle("CafePulse — Safe Mode")
    dlg.resize(520, 360)
    dlg.setStyleSheet("background:#0F1117; color:#E2E8F0; font-family:'Segoe UI',sans-serif;")

    layout = QVBoxLayout(dlg)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    title = QLabel("⚠  CafePulse could not start normally")
    title.setStyleSheet("font-size:16px; font-weight:700; color:#F59E0B;")
    layout.addWidget(title)

    detail = QLabel("The following issues were detected:")
    detail.setStyleSheet("color:#94A3B8;")
    layout.addWidget(detail)

    err_box = QTextEdit()
    err_box.setReadOnly(True)
    err_box.setStyleSheet(
        "background:#161B27; border:1px solid #1E2535; border-radius:8px; color:#EF4444; padding:8px;"
    )
    err_box.setText("\n".join(f"• {e}" for e in errors))
    layout.addWidget(err_box)

    close_btn = QPushButton("Close")
    close_btn.setStyleSheet(
        "background:#EF4444; color:white; border:none; border-radius:8px; padding:10px 20px; font-weight:600;"
    )
    close_btn.clicked.connect(dlg.accept)
    layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

    dlg.exec()
    sys.exit(1)


# ─── Main Application Launch ──────────────────────────────────────────────────

def main() -> None:
    logger.info("=== CafePulse starting ===")
    logger.info("Install dir:   %s", INSTALL_DIR)
    logger.info("User data dir: %s", USER_DATA_DIR)

    # ─── Pre-evaluate is_first_run before any files/folders are created/seeded ───
    is_first_run = not SETTINGS_FILE.exists()

    # ─── Set AppUserModelID for Windows Taskbar Icon ───
    if sys.platform == "win32":
        try:
            import ctypes
            myappid = "cafepulse.network.operations.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as exc:
            logger.warning("Could not set AppUserModelID: %s", exc)

    # ── Initialize Qt Application ──
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from PyQt6.QtCore import Qt
    import time

    app = QApplication(sys.argv)
    app.setApplicationName("CafePulse")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CafePulse")

    # Set window icon — favor native multi-resolution ICO for clean taskbar/title rendering
    icon_path = ICON_ICO_PATH if ICON_ICO_PATH.exists() else (
        ICON_PNG_PATH if ICON_PNG_PATH.exists() else LOGO_PATH
    )
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # ── Initialize and Show Splash Screen ──
    from ui.widgets.splash_screen import CafePulseSplashScreen
    splash_path = SPLASH_PATH if SPLASH_PATH.exists() else (
        LOGO_PATH if LOGO_PATH.exists() else None
    )
    splash = CafePulseSplashScreen(str(splash_path) if splash_path else "")
    splash.show()

    # ── Validate environment with splash updates ──
    validator = StartupValidator()
    ok, errors = validator.run(splash)

    if ok:
        splash.set_status("Inisialisasi selesai!", 100)
        time.sleep(0.3)
        splash.close()
    else:
        splash.close()
        launch_safe_mode(errors)
        return

    # ── Clean Shutdown flag check ──────────────────────────────────────────────
    # Unclean shutdown is defined as LOCK_FILE exists AND CLEAN_FLAG is missing.
    is_unclean_shutdown = LOCK_FILE.exists() and not CLEAN_FLAG.exists()

    if CLEAN_FLAG.exists():
        logger.info("Clean Shutdown flag found. Normal boot.")
        try:
            CLEAN_FLAG.unlink()
        except OSError:
            pass

    if is_unclean_shutdown and not is_first_run:
        logger.warning("LOCK_FILE exists and CLEAN_FLAG not found! Running recovery mode.")
        try:
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setWindowTitle("CafePulse — System Recovery")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Recovered from an unexpected shutdown.")
            msg.setDetailedText(
                "CafePulse was not closed properly during the last session.\n\n"
                "The database integrity check and configuration recovery will run "
                "automatically to ensure system stability."
            )
            msg.exec()
        except Exception:
            pass
    elif not is_unclean_shutdown:
        logger.info("Normal startup sequence. Skipping recovery mode.")
    else:
        logger.info("First-time CafePulse launch. Skipping recovery mode.")

    # Touch lock file to mark active session
    try:
        LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOCK_FILE.touch(exist_ok=True)
    except OSError as exc:
        logger.warning("Could not write lock file: %s", exc)

    # ── Load config ───────────────────────────────────────────────────────────
    from core.utils.config_manager import ConfigManager
    config = ConfigManager(SETTINGS_FILE)

    # Re-setup logging with config values (now that config is loaded)
    log_level  = config.get("logging", "level", default="INFO")
    max_bytes  = config.get("logging", "max_file_bytes", default=5242880)
    backup_cnt = config.get("logging", "backup_count", default=3)
    setup_logging(LOGS_DIR, level=log_level, max_bytes=int(max_bytes), backup_count=int(backup_cnt))

    # ── Initialize database ───────────────────────────────────────────────────
    from core.database.db_manager import DatabaseManager
    db = DatabaseManager(db_path=DATABASE_FILE)
    cleanup_days = config.get("database", "auto_cleanup_days", default=30)
    db.cleanup_old_logs(days=int(cleanup_days))
    db.prune_stale_devices(days=int(cleanup_days))

    # ── Apply theme ───────────────────────────────────────────────────────────
    theme = config.get("ui", "theme", default="dark")
    if theme == "light":
        from ui.themes.light_theme import LIGHT_STYLESHEET
        app.setStyleSheet(LIGHT_STYLESHEET)
    else:
        from ui.themes.dark_theme import DARK_STYLESHEET
        app.setStyleSheet(DARK_STYLESHEET)

    # ── Launch main window ────────────────────────────────────────────────────
    from ui.windows.main_window import MainWindow
    window = MainWindow(config=config, db=db)
    window.show()

    logger.info("CafePulse UI launched")

    exit_code = 0
    try:
        exit_code = app.exec()
    finally:
        # ── Cleanup — always runs, even on unexpected exit ──────────────────────
        try:
            db.close()
        except Exception:
            pass
        try:
            CLEAN_FLAG.parent.mkdir(parents=True, exist_ok=True)
            CLEAN_FLAG.touch(exist_ok=True)
            if LOCK_FILE.exists():
                LOCK_FILE.unlink()
        except Exception:
            pass

    logger.info("=== CafePulse exited (code %d) ===", exit_code)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
