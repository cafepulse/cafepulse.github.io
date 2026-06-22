"""
CafePulse — Main Window  (Phase 4 — Demo / Home WiFi / Hotspot switching)
"""

import logging
import time
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QMessageBox, QSystemTrayIcon, QMenu, QMenuBar,
    QDialog, QRadioButton, QButtonGroup, QProgressBar, QFrame,
    QLabel, QPushButton, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QIcon, QAction

from core.utils.version import __version__
from core.runtime.app_state import AppState
from core.bandwidth_monitor import BandwidthMonitor
from ui.widgets.toast_notification import ToastManager
from core.app_paths import CLEAN_FLAG, LOCK_FILE, LOGO_PATH

logger = logging.getLogger("cafepulse.ui.mainwindow")

MODE_DEMO      = "demo"
MODE_HOME_WIFI = "home_wifi"
MODE_HOTSPOT   = "hotspot"
MODE_MIKROTIK  = "mikrotik"


class FirstTimeCloseDialog(QDialog):
    """
    Stunning, professional onboarding prompt shown when the user first closes the app.
    Allows choosing between Exit Cleanly or Minimize to Tray with 'Remember my choice'.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exit Preference — CafePulse")
        self.setFixedWidth(440)
        self.setStyleSheet("""
            QDialog {
                background-color: #0B0F19;
            }
            QLabel {
                font-family: 'Segoe UI', -apple-system, sans-serif;
                color: #94A3B8;
                font-size: 11px;
                font-weight: 600;
            }
            QRadioButton {
                color: #F3F4F6;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                spacing: 8px;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 16px; height: 16px;
                border-radius: 8px;
                border: 1px solid #4A5568;
                background: #111827;
            }
            QRadioButton::indicator:checked {
                background: #38BDF8;
                border-color: #38BDF8;
            }
            QCheckBox {
                color: #94A3B8;
                font-size: 11px;
                font-weight: bold;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 14px; height: 14px;
                border-radius: 3px;
                border: 1px solid #4A5568;
                background: #111827;
            }
            QCheckBox::indicator:checked {
                background: #38BDF8;
                border-color: #38BDF8;
            }
            QPushButton {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 6px;
                color: #F3F4F6;
                padding: 8px 16px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 12px;
                min-height: 22px;
            }
            QPushButton:hover {
                background-color: #374151;
                border-color: #38BDF8;
                color: #38BDF8;
            }
            QPushButton#PrimaryBtn {
                background-color: #38BDF8;
                color: #0B0F19;
                border: none;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #7DD3FC;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Row
        hdr = QHBoxLayout()
        icon_lbl = QLabel("🚪")
        icon_lbl.setStyleSheet("font-size: 32px; background: transparent;")
        hdr.addWidget(icon_lbl)
        hdr.addSpacing(8)
        
        title_vbox = QVBoxLayout()
        title_lbl = QLabel("PILIH PERILAKU PENUTUPAN")
        title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #38BDF8; letter-spacing: 0.5px;")
        sub_lbl = QLabel("Tentukan tindakan sistem saat Anda menekan tombol tutup [X].")
        sub_lbl.setStyleSheet("font-size: 11px; color: #64748B;")
        title_vbox.addWidget(title_lbl)
        title_vbox.addWidget(sub_lbl)
        hdr.addLayout(title_vbox)
        hdr.addStretch()
        layout.addLayout(hdr)

        # Divider
        div = QFrame()
        div.setStyleSheet("background-color: #1F2937; max-height: 1px; min-height: 1px; border: none;")
        layout.addWidget(div)

        # Choices Box
        choices_vbox = QVBoxLayout()
        choices_vbox.setSpacing(12)
        
        self.rad_exit = QRadioButton("Keluar dari aplikasi (Smart Safe Close)")
        self.rad_exit.setChecked(True)
        self.rad_tray = QRadioButton("Minimalkan ke System Tray (Tetap aktif di latar)")
        
        self.grp = QButtonGroup(self)
        self.grp.addButton(self.rad_exit)
        self.grp.addButton(self.rad_tray)
        
        choices_vbox.addWidget(self.rad_exit)
        choices_vbox.addWidget(self.rad_tray)
        layout.addLayout(choices_vbox)

        # Remind me check
        self.chk_remember = QCheckBox("Ingat pilihan saya (Bisa diubah kapan saja di Settings)")
        self.chk_remember.setChecked(True)
        layout.addWidget(self.chk_remember)

        layout.addSpacing(8)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_cancel = QPushButton("Batal")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton("Lanjutkan")
        self.btn_ok.setObjectName("PrimaryBtn")
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ok.clicked.connect(self.accept)
        
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_ok)
        layout.addLayout(btn_row)

    def get_choice(self) -> tuple[str, bool]:
        """Returns (choice, remember_choice)"""
        choice = "smart_safe_close" if self.rad_exit.isChecked() else "minimize_to_tray"
        return choice, self.chk_remember.isChecked()


class GracefulShutdownMonitor:
    """
    Monitors and drives the graceful shutdown sequence.
    Tracks each step with progress feedback via callbacks.
    Steps: Stop Scan (0→33%) → Commit DB (33→66%) → Save Config (66→90%) → Exit (90→100%)
    """
    def __init__(self, main_window, progress_callback, done_callback):
        self._mw = main_window
        self._progress_cb = progress_callback   # fn(int: 0-100, str: label)
        self._done_cb = done_callback            # fn() called when fully done
        self._step = 0
        self._elapsed_ms = 0
        self._timeout_ms = 12000                # 12 second hard timeout
        self._poll_interval = 300

        self._timer = QTimer()
        self._timer.setInterval(self._poll_interval)
        self._timer.timeout.connect(self._poll)

    def start(self):
        # Step 0: request workers to stop
        self._progress_cb(5, "Menghentikan proses scanning jaringan...")
        logger.info("[SHUTDOWN] Step 1: Requesting all workers to stop")
        try:
            for attr in ("_demo_worker", "_wifi_worker", "_hotspot_worker", "_mikrotik_worker"):
                worker = getattr(self._mw, attr, None)
                if worker and worker.isRunning():
                    worker.stop()
        except Exception as e:
            logger.error("[SHUTDOWN] Error requesting stop for workers: %s", e)
        self._step = 1
        self._timer.start()

    def _poll(self):
        self._elapsed_ms += self._poll_interval

        if self._step == 1:
            # Check if all workers have stopped
            all_stopped = True
            for attr in ("_demo_worker", "_wifi_worker", "_hotspot_worker", "_mikrotik_worker"):
                worker = getattr(self._mw, attr, None)
                if worker and worker.isRunning():
                    all_stopped = False
                    break
            pct = min(5 + int((self._elapsed_ms / 3000) * 28), 33)  # ramp 5→33% over 3s
            self._progress_cb(pct, "Menghentikan proses scanning jaringan...")
            if all_stopped or self._elapsed_ms >= 3500:
                # Force-terminate any remaining workers
                for attr in ("_demo_worker", "_wifi_worker", "_hotspot_worker", "_mikrotik_worker"):
                    worker = getattr(self._mw, attr, None)
                    if worker and worker.isRunning():
                        logger.warning("[SHUTDOWN] Worker %s did not stop gracefully. Force terminating in monitor.", attr)
                        worker.terminate()
                        worker.wait(500)
                    setattr(self._mw, attr, None)
                self._step = 2
                self._progress_cb(35, "Menyimpan dan menutup database...")
                logger.info("[SHUTDOWN] Step 1 complete: Workers Stopped")

        elif self._step == 2:
            # Commit database
            try:
                if hasattr(self._mw, "_db") and self._mw._db:
                    self._mw._db.close()
                logger.info("[SHUTDOWN] Step 2 complete: Database Closed")
            except Exception as e:
                logger.error("[SHUTDOWN] Step 2 error closing database: %s", e)
            self._step = 3
            self._progress_cb(66, "Menyimpan sesi dan konfigurasi...")

        elif self._step == 3:
            # Save session & config
            try:
                if hasattr(self._mw, "_config") and self._mw._config:
                    import time as _time
                    current_page = getattr(self._mw, "_current_page_id", "dashboard")
                    self._mw._config.set("general", "last_active_page", value=current_page)
                    self._mw._config.set("general", "last_exit_time", value=_time.strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("[SHUTDOWN] Step 3 complete: Session & Config Saved")
            except Exception as e:
                logger.error("[SHUTDOWN] Step 3 error saving config: %s", e)
            self._step = 4
            self._progress_cb(85, "Membersihkan file kunci dan log...")

        elif self._step == 4:
            # Mark clean shutdown
            try:
                CLEAN_FLAG.parent.mkdir(parents=True, exist_ok=True)
                CLEAN_FLAG.touch(exist_ok=True)
                LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
                if LOCK_FILE.exists():
                    LOCK_FILE.unlink()
                logger.info("[SHUTDOWN] Step 4 complete: CLEAN_FLAG created, LOCK_FILE deleted")
            except Exception as e:
                logger.error("[SHUTDOWN] Step 4 error unlinking lock: %s", e)
            self._step = 5
            self._progress_cb(100, "Aplikasi berhasil ditutup dengan aman. ✅")
            self._timer.stop()
            # Small delay so user sees 100% before exit
            QTimer.singleShot(600, self._done_cb)
            return

        # Hard timeout fallback
        if self._elapsed_ms >= self._timeout_ms and self._step < 5:
            self._timer.stop()
            self._progress_cb(100, "Timeout — menutup paksa secara aman.")
            QTimer.singleShot(400, self._done_cb)


class SafeCloseDialog(QDialog):
    """
    A unified, gorgeous contextual Dialog for managing Level 1 to Level 4 close actions.
    Consistently styled with CafePulse cyber-dark theme.
    Level 3: Dialog stays open during graceful shutdown, shows live progress.
    """
    def __init__(self, level: int, description: str, router_ip: str = "", parent=None):
        super().__init__(parent)
        self.level = level
        self.setWindowTitle("Konfirmasi Penutupan — CafePulse")
        self.setFixedWidth(460)
        self.selected_action = "cancel"
        self._monitor = None

        self.setStyleSheet("""
            QDialog {
                background-color: #0B0F19;
            }
            QLabel {
                font-family: 'Segoe UI', -apple-system, sans-serif;
                color: #94A3B8;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 6px;
                color: #F3F4F6;
                padding: 10px 16px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 12px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #374151;
                border-color: #38BDF8;
                color: #38BDF8;
            }
            QPushButton:disabled {
                background-color: #111827;
                color: #4B5563;
                border-color: #1F2937;
            }
            QPushButton#PrimaryBtn {
                background-color: #38BDF8;
                color: #0B0F19;
                border: none;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #7DD3FC;
            }
            QPushButton#PrimaryBtn:disabled {
                background-color: #1E3A4A;
                color: #4B5563;
            }
            QPushButton#DangerBtn {
                background-color: #2D1515;
                color: #FC8181;
                border: 1px solid #742A2A;
            }
            QPushButton#DangerBtn:hover {
                background-color: #E53E3E;
                color: white;
            }
            QProgressBar {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 6px;
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 10px;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6D28D9, stop:1 #38BDF8
                );
                border-radius: 5px;
            }
        """)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(16)

        # 1. Header (Icon + Title)
        hdr = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setStyleSheet("font-size: 36px; background: transparent;")

        title_vbox = QVBoxLayout()
        self.title_lbl = QLabel()
        self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; letter-spacing: 0.5px;")

        self.sub_lbl = QLabel()
        self.sub_lbl.setStyleSheet("font-size: 11px; color: #64748B;")

        title_vbox.addWidget(self.title_lbl)
        title_vbox.addWidget(self.sub_lbl)
        hdr.addLayout(title_vbox)
        hdr.addStretch()
        self._layout.addLayout(hdr)

        # Level-specific setup
        if level == 1:
            icon_lbl.setText("💾")
            self.title_lbl.setText("PERUBAHAN BELUM DISIMPAN")
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #FBBF24; letter-spacing: 0.5px;")
            self.sub_lbl.setText("Terdapat konfigurasi atau pengaturan aplikasi yang diubah.")
        elif level == 2:
            icon_lbl.setText("🔌")
            self.title_lbl.setText("KONEKSI ROUTER AKTIF")
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #38BDF8; letter-spacing: 0.5px;")
            self.sub_lbl.setText("Sistem mendeteksi koneksi aktif ke MikroTik Router.")
        elif level == 3:
            icon_lbl.setText("⏳")
            self.title_lbl.setText("PROSES BACKUP / SCAN BERJALAN")
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #A78BFA; letter-spacing: 0.5px;")
            self.sub_lbl.setText("Terdapat background task yang sedang beroperasi.")
        elif level == 4:
            icon_lbl.setText("⚠️")
            self.title_lbl.setText("OPERASI SANGAT KRITIS SEDANG BERJALAN")
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #EF4444; letter-spacing: 0.5px;")
            self.sub_lbl.setText("PERINGATAN: Berisiko tinggi merusak konfigurasi router!")

        hdr.insertWidget(0, icon_lbl)

        # Divider
        div = QFrame()
        div.setStyleSheet("background-color: #1F2937; max-height: 1px; min-height: 1px; border: none;")
        self._layout.addWidget(div)

        # Description text
        desc_lbl = QLabel(description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 12px; color: #E5E7EB; line-height: 16px; background: transparent;")
        self._layout.addWidget(desc_lbl)

        # Progress bar (shown for level 3 and 4)
        if level in (3, 4):
            self.pbar = QProgressBar()
            self.pbar.setRange(0, 100)
            self.pbar.setValue(0)
            self.pbar.setFormat("%p%")
            self.pbar.setFixedHeight(20)
            self._layout.addWidget(self.pbar)

            self.pbar_status = QLabel("Menunggu keputusan Anda...")
            self.pbar_status.setStyleSheet(
                "font-size: 10px; color: #94A3B8; font-style: italic; background: transparent;"
            )
            self._layout.addWidget(self.pbar_status)

        self._layout.addSpacing(10)

        # Buttons row
        self._btn_row = QHBoxLayout()
        self._btn_row.setSpacing(8)
        self._all_buttons = []

        if level == 1:
            btn_save = QPushButton("Simpan dan Keluar")
            btn_save.setObjectName("PrimaryBtn")
            btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_save.clicked.connect(lambda: self._set_action("save_exit"))

            btn_discard = QPushButton("Keluar Tanpa Menyimpan")
            btn_discard.setObjectName("DangerBtn")
            btn_discard.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_discard.clicked.connect(lambda: self._set_action("discard_exit"))

            btn_cancel = QPushButton("Batal")
            btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cancel.clicked.connect(lambda: self._set_action("cancel"))

            self._btn_row.addWidget(btn_cancel)
            self._btn_row.addStretch()
            self._btn_row.addWidget(btn_discard)
            self._btn_row.addWidget(btn_save)
            self._all_buttons = [btn_save, btn_discard, btn_cancel]

        elif level == 2:
            btn_disc = QPushButton("Disconnect & Keluar")
            btn_disc.setObjectName("DangerBtn")
            btn_disc.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_disc.clicked.connect(lambda: self._set_action("exit"))

            btn_tray = QPushButton("Tetap Jalan di Tray")
            btn_tray.setObjectName("PrimaryBtn")
            btn_tray.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_tray.clicked.connect(lambda: self._set_action("tray"))

            btn_cancel = QPushButton("Batal")
            btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cancel.clicked.connect(lambda: self._set_action("cancel"))

            self._btn_row.addWidget(btn_cancel)
            self._btn_row.addStretch()
            self._btn_row.addWidget(btn_disc)
            self._btn_row.addWidget(btn_tray)
            self._all_buttons = [btn_disc, btn_tray, btn_cancel]

        elif level == 3:
            self._btn_wait = QPushButton("⏳  Tunggu Selesai")
            self._btn_wait.setObjectName("PrimaryBtn")
            self._btn_wait.setCursor(Qt.CursorShape.PointingHandCursor)
            self._btn_wait.clicked.connect(self._start_graceful_wait)

            self._btn_force = QPushButton("Keluar Paksa")
            self._btn_force.setObjectName("DangerBtn")
            self._btn_force.setCursor(Qt.CursorShape.PointingHandCursor)
            self._btn_force.clicked.connect(lambda: self._set_action("force"))

            self._btn_tray = QPushButton("Minimalkan ke Tray")
            self._btn_tray.setCursor(Qt.CursorShape.PointingHandCursor)
            self._btn_tray.clicked.connect(lambda: self._set_action("tray"))

            self._btn_row.addWidget(self._btn_tray)
            self._btn_row.addStretch()
            self._btn_row.addWidget(self._btn_force)
            self._btn_row.addWidget(self._btn_wait)
            self._all_buttons = [self._btn_wait, self._btn_force, self._btn_tray]

        elif level == 4:
            btn_wait = QPushButton("Tunggu (Disarankan)")
            btn_wait.setObjectName("PrimaryBtn")
            btn_wait.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_wait.clicked.connect(self._start_graceful_wait)

            btn_force = QPushButton("Keluar Paksa (Berisiko)")
            btn_force.setObjectName("DangerBtn")
            btn_force.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_force.clicked.connect(lambda: self._set_action("force"))

            btn_cancel = QPushButton("Batal")
            btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cancel.clicked.connect(lambda: self._set_action("cancel"))

            self._btn_row.addWidget(btn_cancel)
            self._btn_row.addStretch()
            self._btn_row.addWidget(btn_force)
            self._btn_row.addWidget(btn_wait)
            self._all_buttons = [btn_wait, btn_force, btn_cancel]

        self._layout.addLayout(self._btn_row)

    def _start_graceful_wait(self):
        """Starts graceful shutdown monitoring — dialog stays open, progress updates live."""
        # Disable all buttons so user can't interrupt
        for btn in self._all_buttons:
            btn.setEnabled(False)

        # Update title to show we're in shutdown mode
        self.title_lbl.setText("🔄  MENUTUP APLIKASI DENGAN AMAN...")
        self.title_lbl.setStyleSheet(
            "font-size: 14px; font-weight: 800; color: #38BDF8; letter-spacing: 0.5px;"
        )
        self.sub_lbl.setText("Harap tunggu — proses sedang dihentikan secara cerdas.")

        # Prevent the X button from closing the dialog during shutdown
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.show()  # re-apply flag

        # Start the monitor
        self._monitor = GracefulShutdownMonitor(
            main_window=self.parent(),
            progress_callback=self._on_progress,
            done_callback=self._on_shutdown_done
        )
        self._monitor.start()

    def _on_progress(self, pct: int, label: str):
        """Called by GracefulShutdownMonitor to update the progress bar."""
        if hasattr(self, "pbar"):
            self.pbar.setValue(pct)
        if hasattr(self, "pbar_status"):
            self.pbar_status.setText(label)

    def _on_shutdown_done(self):
        """Called when all shutdown steps are complete — exit the app."""
        self.selected_action = "wait_done"
        self.accept()  # closes the dialog

    def _set_action(self, act: str):
        self.selected_action = act
        if act in ("cancel", "tray"):
            self.reject()
        else:
            self.accept()

from core.runtime.app_state import AppState
from core.bandwidth_monitor import BandwidthMonitor
from ui.widgets.toast_notification import ToastManager

logger = logging.getLogger("cafepulse.ui.mainwindow")

MODE_DEMO      = "demo"
MODE_HOME_WIFI = "home_wifi"
MODE_HOTSPOT   = "hotspot"
MODE_MIKROTIK  = "mikrotik"


class MainWindow(QMainWindow):
    def __init__(self, config, db, parent=None):
        super().__init__(parent)
        self._config          = config
        self._db              = db
        self._demo_worker     = None
        self._wifi_worker     = None
        self._hotspot_worker  = None
        self._current_mode    = MODE_DEMO
        self._alert_count     = 0

        # Simulated Task states for Safe Close testing
        self.is_backup_running = False
        self.is_restore_running = False
        self.is_update_running = False
        self.is_config_pushing = False

        self._app_state = AppState(self)
        self._bandwidth = BandwidthMonitor(interval_ms=2000, parent=self)
        self._bandwidth.speed_updated.connect(self._app_state.update_bandwidth)
        self._bandwidth.start()

        self._setup_window()
        self._build_ui()
        self._connect_signals()
        
        # System Tray Integration
        self._init_tray_icon()

        # Connect aboutToQuit signal to ensure clean shutdown sequence always runs
        from PyQt6.QtCore import QCoreApplication
        app_inst = QCoreApplication.instance()
        if app_inst:
            app_inst.aboutToQuit.connect(self._finalize_and_exit)
            # Connect commitDataRequest for OS shutdown session tracking
            from PyQt6.QtGui import QGuiApplication
            app_gui = QGuiApplication.instance()
            if app_gui:
                app_gui.commitDataRequest.connect(self._on_commit_data_request)

        # Watchdog System
        self._last_heartbeat = time.time()
        self._watchdog_timer = QTimer(self)
        self._watchdog_timer.setInterval(5000)
        self._watchdog_timer.timeout.connect(self._check_watchdog)
        self._watchdog_timer.start()
        
        self._initialize_onboarding_and_start()
        
        # Initialize Responsive System
        from core.runtime.responsive_manager import ResponsiveManager
        self._responsive_mgr = ResponsiveManager(self, self)
        
        # Hook signals
        self._top_bar.hamburger_clicked.connect(self._toggle_responsive_drawer)
        self._sidebar.page_changed.connect(self._on_sidebar_page_changed)
        
        # Centralized Responsive Layout Registrations
        # 1. Devices Table
        dev_col_map = {
            "large": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "medium": [0, 1, 2, 3, 4, 6, 7, 8],     # Hide Category and Last Seen
            "small": [0, 1, 2, 6, 7, 8],           # Hide MAC, Vendor, Category, Last Seen
            "compact": [0, 1, 2, 8],               # Hide MAC, Vendor, Category, Upload, Download, Last Seen
            "minimal": [0, 1, 2, 8]
        }
        self._responsive_mgr.register_table(self._devices_page._table, dev_col_map)
        
        # 2. DHCP Table
        dhcp_col_map = {
            "large": [0, 1, 2, 3, 4],
            "medium": [0, 1, 2, 3, 4],
            "small": [0, 2, 3],                    # Hide MAC and Type
            "compact": [0, 2, 3],
            "minimal": [0, 2, 3]
        }
        self._responsive_mgr.register_table(self._devices_page._dhcp_table, dhcp_col_map)
        
        # 3. Backup Table
        backup_col_map = {
            "large": [0, 1, 2],
            "medium": [0, 1, 2],
            "small": [0, 1],                       # Hide Creation Date & Time
            "compact": [0, 1],
            "minimal": [0, 1]
        }
        self._responsive_mgr.register_table(self._devices_page._backup_table, backup_col_map)
        
        # 4. Device Details Splitter
        self._responsive_mgr.register_splitter(self._devices_page._device_splitter, ["small", "compact", "minimal"])
        
        # 5. MikroTik Observability IP Table
        ip_col_map = {
            "large": [0, 1, 2, 3, 4],
            "medium": [0, 1, 2],       # Hide Dynamic and Disabled
            "small": [0, 2],           # Hide Network, Dynamic, Disabled
            "compact": [0, 2],
            "minimal": [0]             # Hide Network, Interface, Dynamic, Disabled
        }
        self._responsive_mgr.register_table(self._mikrotik_dashboard._ip_table, ip_col_map)
        
        # 6. MikroTik Observability DNS Table
        dns_col_map = {
            "large": [0, 1, 2],
            "medium": [0, 1],          # Hide TTL
            "small": [0, 1],
            "compact": [0],            # Hide Address, TTL
            "minimal": [0]
        }
        self._responsive_mgr.register_table(self._mikrotik_dashboard._dns_table, dns_col_map)
        
        # 7. MikroTik Observability Cache Table
        cache_col_map = {
            "large": [0, 1, 2, 3],
            "medium": [0, 1, 3],       # Hide TTL
            "small": [0, 3],           # Hide Type, TTL
            "compact": [0],            # Hide Type, TTL, Data
            "minimal": [0]
        }
        self._responsive_mgr.register_table(self._mikrotik_dashboard._cache_table, cache_col_map)
        
        # 8. Hotspot Users Table
        hotspot_col_map = {
            "large": [0, 1, 2, 3, 4, 5, 6],
            "medium": [1, 3, 4, 6],    # Hide checkbox, Password, Catatan/Owner
            "small": [1, 3, 6],       # Hide checkbox, Password, Time Limit, Catatan/Owner
            "compact": [1, 6],         # Hide checkbox, Password, Profile, Time Limit, Catatan/Owner
            "minimal": [1, 6]
        }
        self._responsive_mgr.register_table(self._hotspot_page.user_table, hotspot_col_map)
        
        # Trigger initial resize detection
        self._responsive_mgr.handle_resize(self.width(), self.height())

        # Phase 5: Connect breakpoint changes to SettingsPage form adaptation
        self._responsive_mgr.breakpoint_changed.connect(self._settings_page.adapt_layout)

        # Phase 7: Connect breakpoint changes to Dashboard chart/radar layout
        self._responsive_mgr.breakpoint_changed.connect(self._dashboard_page.adapt_chart_layout)

        logger.info("MainWindow (Phase 4) initialized")

    # ─── Window ───────────────────────────────────────────────────────────────

    def _setup_window(self) -> None:
        self.setWindowTitle(f"CafePulse v{__version__} — Network Monitor")
        try:
            width = int(self._config.get("ui.window_width", 1440) or 1440)
        except (ValueError, TypeError):
            width = 1440
            
        try:
            height = int(self._config.get("ui.window_height", 900) or 900)
        except (ValueError, TypeError):
            height = 900
            
        self.resize(width, height)
        # Phase 5 fix: Use a smaller minimum so the window can be used at 1366x768.
        # The responsive system handles layout reflow — we do NOT lock the window size.
        self.setMinimumSize(960, 600)

    # ─── UI Build ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        from ui.widgets.sidebar          import Sidebar
        from ui.widgets.top_bar          import TopBar
        from ui.widgets.dashboard_page   import DashboardPage
        from ui.widgets.devices_page     import DevicesPage
        from ui.widgets.alerts_page import AlertsPage
        from ui.widgets.modes_page import ModesPage
        from ui.widgets.home_wifi_page import HomeWifiPage
        from ui.widgets.hotspot_page import HotspotPage
        from ui.widgets.mikrotik_dashboard import MikrotikDashboard
        from ui.widgets.about_page import AboutPage
        from ui.widgets.traffic_chart import TrafficChart

        # Create and Style File -> Exit Menu Bar
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #0B0F19;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: bold;
                border-bottom: 1px solid #1F2937;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #1E293B;
                color: #38BDF8;
            }
            QMenu {
                background-color: #0B0F19;
                border: 1px solid #1F2937;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: bold;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #38BDF8;
                color: #0B0F19;
            }
        """)
        file_menu = menubar.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self._exit_immediately_menu)
        file_menu.addAction(exit_action)

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._top_bar = TopBar(app_state=self._app_state)
        self._top_bar.set_mode("Demo Mode")
        root_layout.addWidget(self._top_bar)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        self._body_widget = body
        self._body_layout = body_layout

        self._sidebar = Sidebar(app_state=self._app_state)
        body_layout.addWidget(self._sidebar)

        self._stack = QStackedWidget()
        body_layout.addWidget(self._stack)
        
        # Scrim overlay for drawer mode
        self._drawer_scrim = QWidget(self)
        self._drawer_scrim.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self._drawer_scrim.setVisible(False)
        self._drawer_scrim.mousePressEvent = lambda event: self._toggle_responsive_drawer(force_state=False)

        self._dashboard_page  = DashboardPage(app_state=self._app_state)
        self._devices_page    = DevicesPage(self._db, app_state=self._app_state)
        self._alerts_page     = AlertsPage(self._db, app_state=self._app_state)
        self._modes_page      = ModesPage()
        self._home_wifi_page  = HomeWifiPage(app_state=self._app_state)
        self._hotspot_page    = HotspotPage(self._db, app_state=self._app_state)
        self._mikrotik_dashboard = MikrotikDashboard(self._db, app_state=self._app_state)

        from ui.widgets.compatibility_page import CompatibilityPage
        self._compatibility_page = CompatibilityPage(app_state=self._app_state)

        from ui.widgets.analytics_page import AnalyticsPage
        self._analytics_page = AnalyticsPage(self._db, app_state=self._app_state)

        from ui.widgets.settings_page import SettingsPage
        self._settings_page = SettingsPage(self._config, self._db, app_state=self._app_state)

        # Inisialisasi Locked Widgets untuk Edisi Premium (PRO)
        from ui.widgets.premium_lock_widget import PremiumLockWidget
        self._analytics_lock = PremiumLockWidget("Analytics & BI", self._app_state, self)
        self._mikrotik_lock = PremiumLockWidget("MikroTik Dashboard", self._app_state, self)

        self._pages: dict[str, QWidget] = {
            "dashboard":       self._dashboard_page,
            "devices":         self._devices_page,
            "analytics":       self._analytics_page,
            "alerts":          self._alerts_page,
            "modes":           self._modes_page,
            "settings":        self._settings_page,
            "about":           AboutPage(),
            "compatibility":   self._compatibility_page,
            "home_wifi_detail": self._home_wifi_page,
            "hotspot_detail":  self._hotspot_page,
            "mikrotik_detail": self._mikrotik_dashboard,
            "analytics_locked": self._analytics_lock,
            "mikrotik_locked":  self._mikrotik_lock,
        }

        # Hubungkan sinyal aktivasi lisensi sukses untuk membuka akses modul secara realtime
        self._analytics_lock.activation_success.connect(lambda: self._on_license_activated("analytics"))
        self._mikrotik_lock.activation_success.connect(lambda: self._on_license_activated("mikrotik_detail"))

        for widget in self._pages.values():
            self._stack.addWidget(widget)

        root_layout.addWidget(body)

        self._chart = TrafficChart()
        self._dashboard_page.inject_chart(self._chart)

        # Toast notifications overlay
        self._toast_mgr = ToastManager(self)
        
        # Developer Debug Overlay (collapsible floating widget)
        from ui.widgets.dev_debug_overlay import DevDebugOverlay
        self._dev_overlay = DevDebugOverlay(self, root)
        self._dev_overlay.setVisible(False)

    # ─── Signal Wiring ────────────────────────────────────────────────────────

    def _connect_signals(self) -> None:
        self._sidebar.page_changed.connect(self._on_page_changed)
        self._top_bar.scan_requested.connect(self._on_scan_requested)
        self._top_bar.exit_demo_requested.connect(self._exit_demo_mode)
        self._modes_page.mode_changed.connect(self._on_mode_changed)
        self._modes_page.scenario_changed.connect(self._on_scenario_changed)
        self._home_wifi_page.scan_requested.connect(self._on_manual_scan)
        self._settings_page.settings_changed.connect(self._on_settings_changed)
        
        # Connect demo mode CTA signals
        self._dashboard_page.demo_mode_requested.connect(self._start_demo_mode)
        self._analytics_page.demo_mode_requested.connect(self._start_demo_mode)
        self._devices_page.demo_mode_requested.connect(self._start_demo_mode)
        
        # Connect alert sync signals
        self._alerts_page.alerts_read.connect(self._on_alerts_cleared)
        self._alerts_page.alerts_cleared.connect(self._on_alerts_cleared)

    # ─── Worker Lifecycle ─────────────────────────────────────────────────────

    def _stop_all_workers(self) -> None:
        import time
        from PyQt6.QtWidgets import QApplication
        
        # 1. Signal all workers to stop simultaneously
        active_workers = []
        for attr in ("_demo_worker", "_wifi_worker", "_hotspot_worker", "_mikrotik_worker"):
            worker = getattr(self, attr, None)
            if worker and worker.isRunning():
                logger.info("[SHUTDOWN] Signaling stop to worker: %s", attr)
                worker.stop()  # Should now be non-blocking
                active_workers.append((attr, worker))
                
        # 2. Wait for all to stop collectively, keeping UI alive and processing events
        if active_workers:
            logger.info("[SHUTDOWN] Waiting for %d workers to exit gracefully (up to 5s)...", len(active_workers))
            start_time = time.time()
            while time.time() - start_time < 5.0:
                all_stopped = True
                for _, w in active_workers:
                    if w.isRunning():
                        all_stopped = False
                        break
                if all_stopped:
                    logger.info("[SHUTDOWN] All workers stopped cleanly.")
                    break
                QApplication.processEvents()
                time.sleep(0.1)
                
            # 3. Handle any workers that refused to stop (NO TERMINATE)
            for attr, w in active_workers:
                if w.isRunning():
                    logger.warning("[SHUTDOWN] Worker %s is still running after timeout! "
                                   "Abandoning gracefully without terminate to prevent DB/Socket corruption.", attr)
                setattr(self, attr, None)

    # ─── Demo Mode ────────────────────────────────────────────────────────────

    def _start_demo_mode(self) -> None:
        self._stop_all_workers()
        from modes.demo.demo_worker import DemoWorker
        interval = int(self._config.get("network", "polling_interval_seconds", default=2)) * 1000
        self._demo_worker = DemoWorker(self._db, "small_cafe", interval_ms=interval)
        self._demo_worker.tick_data.connect(self._on_tick)
        self._demo_worker.alert_fired.connect(self._on_alert)
        self._demo_worker.error.connect(self._on_worker_error)
        self._demo_worker.heartbeat.connect(self._on_heartbeat)
        self._demo_worker.start()
        self._last_heartbeat = time.time()
        self._current_mode = MODE_DEMO
        self._app_state.set_mode("demo")
        self._alert_count  = 0
        self._app_state.set_alert_count(0)
        self._sidebar.set_mode_label("Demo Mode")
        self._top_bar.set_mode("Demo Mode")
        self._top_bar.set_status(True, "Demo Running")
        self._app_state.set_status(True, "Demo Running")

    def _exit_demo_mode(self) -> None:
        """Menonaktifkan Demo Mode secara bersih dan mengembalikan workspace ke keadaan kosong."""
        logger.info("Exiting Demo Mode and transitioning to empty state")
        self._stop_all_workers()
        
        # Bersihkan seluruh data buatan/dummy dari database
        self._db.clear_all_devices()
        
        # Reset charts & dashboards
        if hasattr(self, "_chart") and self._chart:
            self._chart.reset()
            
        self._dashboard_page.clear_alerts()
        self._dashboard_page.update_alert_count(0)
        self._sidebar.set_alert_count(0)
        
        # Reset ke status empty professional state
        self._current_mode = "empty"
        self._app_state.set_mode("empty")
        self._app_state.set_status(False, "Belum Dikonfigurasi")
        self._sidebar.set_mode_label("Belum Aktif")
        self._top_bar.set_mode("CafePulse Jaringan")
        self._top_bar.set_status(False, "Jaringan Kosong")
        self._top_bar.set_device_count(0)
        
        # Sinkronisasi visual kosong pada seluruh halaman
        self._dashboard_page.update_mode("empty")
        self._analytics_page.update_view("empty")
        self._devices_page._on_mode_changed("empty")
        
        self._toast_mgr.show_toast("info", "Demo Mode dinonaktifkan. Workspace kembali ke keadaan kosong.")

    # ─── Home WiFi Mode ───────────────────────────────────────────────────────

    def _start_home_wifi_mode(self) -> None:
        # Clear demo-generated fake devices so they don't pollute real scan
        if self._current_mode == MODE_DEMO:
            self._db.clear_all_devices()
        self._stop_all_workers()
        from modes.home_wifi.wifi_worker import WiFiWorker
        self._wifi_worker = WiFiWorker(self._db, interval_ms=30_000, do_ping_sweep=True)
        self._wifi_worker.scan_result.connect(self._on_scan_result)
        self._wifi_worker.scan_started.connect(lambda: self._top_bar.set_scanning(True))
        self._wifi_worker.scan_started.connect(lambda: self._home_wifi_page.set_scanning(True))
        self._wifi_worker.scan_finished.connect(lambda: self._top_bar.set_scanning(False))
        self._wifi_worker.scan_finished.connect(lambda: self._home_wifi_page.set_scanning(False))
        self._wifi_worker.alert_fired.connect(self._on_alert)
        self._wifi_worker.error.connect(self._on_worker_error)
        self._wifi_worker.heartbeat.connect(self._on_heartbeat)
        self._wifi_worker.start()
        self._last_heartbeat = time.time()
        self._current_mode = MODE_HOME_WIFI
        self._app_state.set_mode("home_wifi")
        self._alert_count  = 0
        self._app_state.set_alert_count(0)
        self._sidebar.set_mode_label("Home WiFi")
        self._top_bar.set_mode("Home WiFi Mode")
        self._top_bar.set_status(True, "Scanning…")
        self._app_state.set_status(True, "Scanning…")
        self._stack.setCurrentWidget(self._pages["home_wifi_detail"])
        # Keep ModesPage button in sync
        self._modes_page.set_active_mode(MODE_HOME_WIFI)

    # ─── Hotspot Mode ─────────────────────────────────────────────────────────

    def _start_hotspot_mode(self) -> None:
        # Clear demo-generated fake devices so they don't pollute real scan
        if self._current_mode == MODE_DEMO:
            self._db.clear_all_devices()
        self._stop_all_workers()
        from modes.hotspot.hotspot_worker import HotspotWorker
        self._hotspot_worker = HotspotWorker(self._db, interval_ms=10_000)
        self._hotspot_worker.scan_result.connect(self._on_hotspot_result)
        self._hotspot_worker.hotspot_detected.connect(self._on_hotspot_detected)
        self._hotspot_worker.scan_started.connect(lambda: self._top_bar.set_scanning(True))
        self._hotspot_worker.scan_started.connect(lambda: self._hotspot_page.set_scanning(True))
        self._hotspot_worker.scan_finished.connect(lambda: self._top_bar.set_scanning(False))
        self._hotspot_worker.scan_finished.connect(lambda: self._hotspot_page.set_scanning(False))
        self._hotspot_worker.alert_fired.connect(self._on_alert)
        self._hotspot_worker.error.connect(self._on_worker_error)
        self._hotspot_worker.heartbeat.connect(self._on_heartbeat)
        self._hotspot_worker.start()
        self._last_heartbeat = time.time()
        self._current_mode = MODE_HOTSPOT
        self._app_state.set_mode("hotspot")
        self._alert_count  = 0
        self._app_state.set_alert_count(0)
        self._sidebar.set_mode_label("Hotspot")
        self._top_bar.set_mode("Hotspot Mode")
        self._top_bar.set_status(True, "Detecting hotspot…")
        self._app_state.set_status(True, "Detecting hotspot…")
        self._stack.setCurrentWidget(self._pages["hotspot_detail"])
        # Keep ModesPage button in sync
        self._modes_page.set_active_mode(MODE_HOTSPOT)

    # ─── MikroTik Mode ────────────────────────────────────────────────────────

    def _start_mikrotik_mode(self) -> None:
        # Cek dependensi secara dinamis dari registry sebelum mengimpor worker
        from core.runtime.dependency_registry import DependencyRegistry
        if not DependencyRegistry.is_available("routeros_api"):
            logger.error("Gagal memulai MikroTik Mode: Pustaka 'routeros_api' tidak terinstall.")
            from ui.dialogs.error_dialog import show_smart_error
            show_smart_error(
                title="Pustaka Tambahan Diperlukan",
                message="Modul 'routeros_api' tidak ditemukan di environment Python.",
                exc_type="ModuleNotFoundError",
                tb_text="ModuleNotFoundError: No module named 'routeros_api'\n\nHarap install modul ini dengan menjalankan:\npip install routeros-api==0.21.0"
            )
            # Kembalikan pilihan mode di UI ke mode yang sedang aktif
            self._modes_page.set_active_mode(self._current_mode)
            return

        # Cek apakah fitur Simpan Sesi aktif dan ada kredensial yang valid tersimpan
        from core.security.credential_store import CredentialStore
        save_session = bool(self._config.get("mikrotik", "save_session", default=False))
        saved_host = self._config.get("mikrotik", "host", default="")
        saved_port = int(self._config.get("mikrotik", "port", default=8728))
        saved_user = self._config.get("mikrotik", "username", default="")
        
        # Dekripsi password secara aman
        saved_pwd = CredentialStore.decrypt(self._config.get("mikrotik", "password", default=""))

        ip = None
        user = None
        pwd = None
        port = saved_port

        if save_session and saved_host and saved_user and saved_pwd:
            logger.info("Persistent session recovery aktif. Bypass login dialog.")
            ip = saved_host
            user = saved_user
            pwd = saved_pwd
        else:
            from ui.dialogs.mikrotik_login_dialog import MikrotikLoginDialog
            dlg = MikrotikLoginDialog(db=self._db, config=self._config, parent=self)
            # Isi default host & username jika tersedia di config
            if saved_host:
                dlg.ip_input.setText(saved_host)
            if saved_user:
                dlg.user_input.setText(saved_user)
                
            if dlg.exec():
                creds = dlg.get_credentials()
                ip = creds.get('ip')
                user = creds.get('username')
                pwd = creds.get('password')
                port = creds.get('port', 8728)
                use_ssl = creds.get('use_ssl', False)
                
                # Simpan ke config jika checkbox/fitur simpan sesi aktif (enkripsi password router)
                if save_session:
                    self._config.set("mikrotik", "host", value=ip)
                    self._config.set("mikrotik", "username", value=user)
                    self._config.set("mikrotik", "password", value=CredentialStore.encrypt(pwd))
                    self._config.set("mikrotik", "port", value=port)
                    self._config.set("mikrotik", "use_ssl", value=use_ssl)

                # Simpan profil favorit jika dicentang di UI dialog
                if creds.get('save_profile') and creds.get('profile_name'):
                    try:
                        self._db.add_router(
                            name=creds.get('profile_name'),
                            host=ip,
                            port=port,
                            username=user,
                            password_encrypted=CredentialStore.encrypt(pwd),
                            use_ssl=use_ssl
                        )
                        logger.info("Saved connection profile to database: %s", creds.get('profile_name'))
                    except Exception as e:
                        logger.error("Failed to save connection profile to DB: %s", e)
            else:
                self._modes_page.set_active_mode(self._current_mode)
                return

        self._stop_all_workers()
        try:
            from modes.mikrotik.mikrotik_worker import MikrotikWorker
            self._mikrotik_worker = MikrotikWorker(self._db, host=ip, username=user, password=pwd, port=port)
        except Exception as e:
            logger.error("Gagal memuat modul MikroTik Worker: %s", e)
            import traceback
            tb_text = traceback.format_exc()
            from ui.dialogs.error_dialog import show_smart_error
            show_smart_error(
                title="Gagal Memuat Modul MikroTik",
                message=str(e),
                exc_type=type(e).__name__,
                tb_text=tb_text
            )
            if save_session and saved_host:
                logger.warning("Kegagalan sesi persisten terdeteksi. Reset password.")
                self._config.set("mikrotik", "password", value="")
            self._modes_page.set_active_mode(self._current_mode)
            return
            
        self._mikrotik_worker.connection_state_changed.connect(self._on_mikrotik_state_changed)
        self._mikrotik_worker.tick_data.connect(self._on_mikrotik_tick)
        self._mikrotik_worker.scan_result.connect(self._on_mikrotik_scan)
        self._mikrotik_worker.error.connect(self._on_worker_error)
        self._mikrotik_worker.heartbeat.connect(self._on_heartbeat)
        self._mikrotik_worker.start()
        self._last_heartbeat = time.time()
        
        self._current_mode = MODE_MIKROTIK
        self._app_state.set_mode("mikrotik")
        self._alert_count = 0
        self._app_state.set_alert_count(0)
        self._sidebar.set_mode_label("MikroTik")
        self._top_bar.set_mode(f"MikroTik Mode — {ip}")
        self._top_bar.set_status(True, "Connecting to router…")
        self._app_state.set_status(True, "Connecting to router…")
        self._stack.setCurrentWidget(self._pages["mikrotik_detail"])

    @pyqtSlot(str)
    def _on_mikrotik_state_changed(self, state: str) -> None:
        """Menangani transisi status koneksi dari state machine MikroTik."""
        # Perbarui widget status chip di dashboard
        self._mikrotik_dashboard.update_connection_state(state)
        
        # Peta status text
        status_map = {
            "CONNECTED": "Online",
            "RECOVERED": "Koneksi Pulih",
            "CONNECTING": "Menghubungkan...",
            "RECONNECTING": "Koneksi Terputus - Reconnecting...",
            "DEGRADED": "Koneksi Menurun",
            "FAILED": "Koneksi Gagal",
            "DISCONNECTED": "Offline"
        }
        status_text = status_map.get(state, state)
        
        is_ok = state in ("CONNECTED", "RECOVERED")
        self._top_bar.set_status(is_ok, status_text)
        self._app_state.set_status(is_ok, status_text)
        
        # Trigger Toast visual premium dan tambahkan riwayat log/alert sistem
        if state == "RECONNECTING":
            self._toast_mgr.show_toast("warning", "Koneksi terputus! Mencoba pemulihan otomatis...")
            self._on_alert({"type": "warning", "message": "Koneksi MikroTik terputus. Memulai reconnect otomatis."})
        elif state == "RECOVERED":
            self._toast_mgr.show_toast("success", "Koneksi MikroTik pulih secara otomatis!")
            self._on_alert({"type": "reconnect", "message": "Koneksi MikroTik berhasil dipulihkan secara otomatis."})
        elif state == "FAILED":
            self._toast_mgr.show_toast("error", "Gagal menghubungkan kembali ke MikroTik.")
            self._on_alert({"type": "error", "message": "Upaya reconnect gagal. Sistem akan terus mencoba."})

    # ─── Slots ────────────────────────────────────────────────────────────────

    @pyqtSlot(str)
    def _on_page_changed(self, page_id: str) -> None:
        self._current_page_id = page_id
        target_page = page_id
        
        # Pengecekan Lisensi Dinamis untuk Fitur Pro (Analytics & MikroTik Dashboard)
        is_pro = self._app_state.is_pro
        if page_id == "analytics" and not is_pro:
            target_page = "analytics_locked"
        elif page_id == "mikrotik_detail" and not is_pro:
            target_page = "mikrotik_locked"
            
        if target_page in self._pages:
            self._stack.setCurrentWidget(self._pages[target_page])
            
        # When returning to the Modes page, sync its active button to current mode
        if page_id == "modes":
            self._modes_page.set_active_mode(self._current_mode)
            
        # Pemicu Contextual Guided Tutorial secara dinamis
        self._trigger_contextual_tutorial(page_id)

    def _on_license_activated(self, original_page_id: str) -> None:
        """Dipanggil ketika aktivasi lisensi offline lokal berhasil."""
        self._toast_mgr.show_toast("success", "Lisensi CafePulse Professional Berhasil Diaktifkan!")
        
        # Jalankan pengecekan status lisensi global agar AppState dan Sidebar langsung memicu pembaruan realtime
        self._app_state.check_license_status()
        
        # Pindahkan navigasi ke halaman asli secara instan
        self._on_page_changed(original_page_id)
        # Perbarui juga sidebar secara aktif
        self._sidebar.set_active_page(original_page_id)

    @pyqtSlot()
    def _on_scan_requested(self) -> None:
        self._top_bar.set_scanning(True)
        self._app_state.set_status(True, "Scanning…")
        
        if self._current_mode == MODE_HOME_WIFI and self._wifi_worker:
            self._wifi_worker.trigger_scan()
        elif self._current_mode == MODE_HOTSPOT and self._hotspot_worker:
            self._hotspot_worker.trigger_scan()
        else:
            QTimer.singleShot(800, lambda: self._top_bar.set_scanning(False))
            QTimer.singleShot(800, lambda: self._app_state.set_status(False, "Idle"))

    @pyqtSlot(str)
    def _on_manual_scan(self, subnet: str) -> None:
        if self._wifi_worker:
            self._home_wifi_page.set_scanning(True)
            self._wifi_worker.trigger_scan()

    @pyqtSlot(str)
    def _on_mode_changed(self, mode_id: str) -> None:
        logger.info("Mode → %s", mode_id)
        if mode_id == MODE_DEMO:
            self._start_demo_mode()
        elif mode_id == MODE_HOME_WIFI:
            self._start_home_wifi_mode()
        elif mode_id == MODE_HOTSPOT:
            self._start_hotspot_mode()
        elif mode_id == MODE_MIKROTIK:
            self._start_mikrotik_mode()

    @pyqtSlot(str)
    def _on_scenario_changed(self, key: str) -> None:
        if self._demo_worker:
            self._demo_worker.set_scenario(key)
        from modes.demo.demo_engine import SCENARIOS
        sc = SCENARIOS.get(key)
        if sc:
            self._sidebar.set_mode_label(f"Demo: {sc.display_name}")
            self._top_bar.set_mode(f"Demo — {sc.display_name}")
        self._alert_count = 0

    # ─── Demo tick ────────────────────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_tick(self, payload: dict) -> None:
        if self._current_mode != MODE_DEMO:
            return
        count = payload.get("device_count", 0)
        self._app_state.set_device_count(count)
        self._dashboard_page.update_from_tick(payload)
        self._dashboard_page.update_mode("Demo")
        alert_rate = self._alert_count / max(payload.get("tick", 1), 1)
        health = "Good" if alert_rate < 0.05 else ("Fair" if alert_rate < 0.15 else "Poor")
        self._dashboard_page.update_health(health)
        self._devices_page.update_from_tick(payload)
        self._top_bar.set_device_count(count)

    # ─── WiFi scan result ─────────────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_scan_result(self, payload: dict) -> None:
        if self._current_mode != MODE_HOME_WIFI:
            return
        count = payload.get("device_count", 0)
        self._app_state.set_device_count(count)
        self._dashboard_page.update_from_tick(payload)
        self._dashboard_page.update_mode("Home WiFi")
        self._dashboard_page.update_health("Good")
        self._devices_page.update_from_tick(payload)
        self._home_wifi_page.update_from_scan(payload)
        self._top_bar.set_device_count(count)
        self._top_bar.set_status(True, f"{count} devices found")
        self._app_state.set_status(True, f"{count} devices found")

    # ─── Hotspot scan result ──────────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_hotspot_result(self, payload: dict) -> None:
        if self._current_mode != MODE_HOTSPOT:
            return
        count = payload.get("device_count", 0)
        self._app_state.set_device_count(count)
        self._dashboard_page.update_from_tick(payload)
        self._dashboard_page.update_mode("Hotspot")
        self._dashboard_page.update_health("Good")
        self._devices_page.update_from_tick(payload)
        self._hotspot_page.update_from_scan(payload)
        self._top_bar.set_device_count(count)

        joined = payload.get("joined", [])
        left   = payload.get("left", [])
        mode_label = payload.get("display_name", "Hotspot")
        self._sidebar.set_mode_label(mode_label)

        status = f"{count} connected"
        if joined:
            status += f"  +{len(joined)}"
        if left:
            status += f"  -{len(left)}"
        self._top_bar.set_status(True, status)

    @pyqtSlot(dict)
    def _on_hotspot_detected(self, info: dict) -> None:
        if self._current_mode != MODE_HOTSPOT:
            return
        display = info.get("display_name", "Hotspot")
        self._sidebar.set_mode_label(display)
        self._top_bar.set_mode(f"{display}")
        self._top_bar.set_status(True, f"Connected — {info.get('subnet', '')}")
        self._hotspot_page.update_hotspot_info(info)

    # ─── MikroTik slots ───────────────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_mikrotik_tick(self, payload: dict) -> None:
        if self._current_mode != MODE_MIKROTIK:
            return
        self._mikrotik_dashboard.update_stats(payload)
        self._app_state.update_bandwidth(payload)
        
        # Penyelarasan Dashboard utama dengan data real-time MikroTik
        ip = self._config.get("mikrotik", "host", default="CHR")
        dash_payload = {
            "device_count": self._app_state.active_devices,
            "total_upload": payload.get("upload_mbps", 0.0),
            "total_download": payload.get("download_mbps", 0.0),
            "scenario": f"CHR: {ip}"
        }
        self._dashboard_page.update_from_tick(dash_payload)
        self._dashboard_page.update_health(payload.get("health", "Good"))

    @pyqtSlot(dict)
    def _on_mikrotik_scan(self, payload: dict) -> None:
        if self._current_mode != MODE_MIKROTIK:
            return
        count = payload.get("device_count", 0)
        self._app_state.set_device_count(count)
        self._mikrotik_dashboard.update_stats(payload)
        self._devices_page.update_from_tick(payload)
        self._hotspot_page.update_from_mikrotik_scan(payload)
        self._top_bar.set_device_count(count)

    # ─── Common alert ─────────────────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_alert(self, payload: dict) -> None:
        alert_type = payload.get("type", "info")
        message    = payload.get("message", "")
        self._alert_count += 1
        self._app_state.set_alert_count(self._alert_count)
        self._dashboard_page.update_alert_count(self._alert_count)
        self._dashboard_page.add_alert_row(alert_type, message)
        self._alerts_page.add_alert(payload)
        self._sidebar.set_alert_count(self._alert_count)
        # Show toast for actionable alerts only (suppress noisy periodic ones)
        if alert_type in ("new_device", "suspicious", "offline", "reconnect", "error", "warning"):
            self._toast_mgr.show_toast(alert_type, message)

    @pyqtSlot()
    def _on_alerts_cleared(self) -> None:
        self._alert_count = 0
        self._app_state.set_alert_count(0)
        self._dashboard_page.clear_alerts()
        self._dashboard_page.update_alert_count(0)
        self._sidebar.set_alert_count(0)

    @pyqtSlot(str)
    def _on_worker_error(self, msg: str) -> None:
        logger.error("Worker error: %s", msg)
        self._top_bar.set_status(False, "Error")
        QMessageBox.warning(self, "CafePulse Error", f"An error occurred:\n{msg}")

    # ─── Watchdog System ──────────────────────────────────────────────────────

    @pyqtSlot(float)
    def _on_heartbeat(self, timestamp: float) -> None:
        self._last_heartbeat = timestamp

    @pyqtSlot()
    def _check_watchdog(self) -> None:
        """Monitor if the current worker has hung and automatically restart it."""
        now = time.time()
        # Real-network scanning modes (home_wifi, hotspot, mikrotik) take longer. Give them a 60s threshold.
        threshold = 60.0 if self._current_mode in (MODE_HOME_WIFI, MODE_HOTSPOT, MODE_MIKROTIK) else 15.0
        if (now - self._last_heartbeat) > threshold:
            active_worker = None
            if self._current_mode == MODE_DEMO and self._demo_worker: active_worker = self._demo_worker
            elif self._current_mode == MODE_HOME_WIFI and self._wifi_worker: active_worker = self._wifi_worker
            elif self._current_mode == MODE_HOTSPOT and self._hotspot_worker: active_worker = self._hotspot_worker
            elif self._current_mode == MODE_MIKROTIK and self._mikrotik_worker: active_worker = self._mikrotik_worker
            
            if active_worker and active_worker.isRunning():
                logger.critical("WATCHDOG: Worker hung detected in mode %s! Auto-restarting...", self._current_mode)
                self._toast_mgr.show_toast("error", f"Watchdog Auto-Recovery Triggered in {self._current_mode}")
                
                # Force terminate (since normal stop might block)
                try:
                    active_worker.terminate()
                    active_worker.wait(1000)
                except Exception:
                    pass
                    
                # Reset heartbeat and restart
                self._last_heartbeat = time.time()
                self._on_mode_changed(self._current_mode)

    @pyqtSlot(str, object)
    def _on_settings_changed(self, key: str, value) -> None:
        """Apply relevant settings immediately without restart."""
        if key == "licensing":
            self._app_state.check_license_status()
            logger.info("Realtime License state changed, Pro status: %s", value)
        if self._wifi_worker and self._wifi_worker.isRunning():
            interval_s = int(self._config.get("network", "wifi_scan_interval_seconds", default=30))
            self._wifi_worker.set_interval(interval_s * 1000)
            logger.info("WiFi scan interval updated live: %ds", interval_s)
            
        # Dinamis switch tema visual (Light / Dark) realtime
        theme = self._config.get("ui", "theme", default="dark")
        from PyQt6.QtWidgets import QApplication
        if theme == "light":
            from ui.themes.light_theme import LIGHT_STYLESHEET
            QApplication.instance().setStyleSheet(LIGHT_STYLESHEET)
            logger.info("Premium Light Theme applied dynamically.")
        else:
            from ui.themes.dark_theme import DARK_STYLESHEET
            QApplication.instance().setStyleSheet(DARK_STYLESHEET)
            logger.info("Cyber-Dark Theme applied dynamically.")

    # ─── Onboarding & Tutorial Engine ──────────────────────────────────────────

    def _initialize_onboarding_and_start(self) -> None:
        from core.runtime.onboarding_manager import OnboardingManager
        self._onboarding_mgr = OnboardingManager(self._config)
        
        if self._onboarding_mgr.is_first_launch():
            logger.info("First launch detected — delaying wizard popup")
            # Tunda wizard popup sesaat setelah UI utama tampil agar responsif
            QTimer.singleShot(600, self._show_onboarding_wizard)
            
            # Default ke Empty State
            self._current_mode = "empty"
            self._app_state.set_mode("empty")
            self._app_state.set_status(False, "Belum Dikonfigurasi")
            self._sidebar.set_mode_label("Belum Aktif")
            self._top_bar.set_mode("CafePulse Jaringan")
            self._top_bar.set_status(False, "Jaringan Kosong")
            self._dashboard_page.update_mode("empty")
            self._analytics_page.update_view("empty")
            self._devices_page._on_mode_changed("empty")
        else:
            logger.info("Normal launch — loading default Demo Mode")
            self._start_demo_mode()

    def _show_onboarding_wizard(self) -> None:
        from ui.dialogs.onboarding_wizard import OnboardingWizard
        wizard = OnboardingWizard(self)
        wizard.onboarding_finished.connect(self._on_onboarding_finished)
        wizard.exec()

    def _on_onboarding_finished(self, use_demo: bool) -> None:
        self._onboarding_mgr.mark_onboarding_completed()
        if use_demo:
            self._start_demo_mode()
            self._toast_mgr.show_toast("success", "Demo Mode berhasil diaktifkan!")
        else:
            self._current_mode = "empty"
            self._app_state.set_mode("empty")
            self._sidebar.set_mode_label("Belum Aktif")
            self._top_bar.set_mode("CafePulse Jaringan")
            self._top_bar.set_status(False, "Jaringan Kosong")
            self._dashboard_page.update_mode("empty")
            self._analytics_page.update_view("empty")
            self._devices_page._on_mode_changed("empty")
            self._toast_mgr.show_toast("info", "Onboarding selesai. Pilih mode di sidebar untuk memulai.")

    def _trigger_contextual_tutorial(self, page_id: str) -> None:
        if not hasattr(self, "_onboarding_mgr") or not self._onboarding_mgr:
            return
            
        # Pengecekan status: jika onboarding wizard utama sedang aktif, tunda contextual tutorial
        if self._onboarding_mgr.is_first_launch():
            return
            
        from core.runtime.tutorial_registry import TUTORIALS
        reg_id = page_id
        
        if reg_id in TUTORIALS and not self._onboarding_mgr.has_seen_tutorial(reg_id):
            info = TUTORIALS[reg_id]
            from ui.widgets.contextual_guide import ContextualGuideCard
            
            target_widget = self._pages.get(page_id)
            if target_widget:
                card = ContextualGuideCard(info["title"], info["description"], target_widget)
                card.dismissed.connect(lambda: self._onboarding_mgr.mark_tutorial_seen(reg_id))
                
                # Tampilkan mengambang di pojok kanan bawah setelah jeda singkat
                QTimer.singleShot(400, lambda: card.show_floating(target_widget))

    # ─── Close ────────────────────────────────────────────────────────────────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._toast_mgr._reposition()
        if hasattr(self, "_dev_overlay") and self._dev_overlay:
            self._dev_overlay._reposition()
        if hasattr(self, "_responsive_mgr") and self._responsive_mgr:
            self._responsive_mgr.handle_resize(self.width(), self.height())
        # Auto-save window geometry debounced (500ms) so next launch opens at last-used size.
        if not hasattr(self, "_resize_save_timer"):
            from PyQt6.QtCore import QTimer
            self._resize_save_timer = QTimer(self)
            self._resize_save_timer.setSingleShot(True)
            self._resize_save_timer.timeout.connect(self._persist_window_size)
        self._resize_save_timer.start(500)

    def _persist_window_size(self) -> None:
        """Quietly save current window size to config after resize (debounced)."""
        try:
            self._config.set("ui", "window_width", value=self.width())
            self._config.set("ui", "window_height", value=self.height())
        except Exception:
            pass  # Non-critical — don't disrupt the user

    # ─── Drawer overlay transitions ──────────────────────────────────────────

    def _apply_responsive_state(self, bp: str) -> None:
        is_drawer_mode = bp in ("compact", "minimal", "small")
        self._top_bar.set_hamburger_visible(is_drawer_mode)
        
        if not hasattr(self, "_drawer_open"):
            self._drawer_open = False
            
        if is_drawer_mode:
            self._drawer_open = False
            if self._drawer_scrim:
                self._drawer_scrim.setVisible(False)
                
            self._sidebar.setParent(self)
            self._sidebar.set_compact(False)
            self._sidebar.setGeometry(-240, 52, 240, self.height() - 52)
            self._sidebar.hide()
        else:
            if self._drawer_scrim:
                self._drawer_scrim.setVisible(False)
                
            self._sidebar.setParent(self._body_widget)
            self._body_layout.insertWidget(0, self._sidebar)
            self._sidebar.show()
            
            if bp == "medium":
                self._sidebar.set_compact(True)
            else:
                self._sidebar.set_compact(False)
                
    def _reposition_responsive_drawer(self, width: int, height: int, bp: str) -> None:
        is_drawer_mode = bp in ("compact", "minimal", "small")
        if is_drawer_mode:
            self._drawer_scrim.setGeometry(0, 52, width, height - 52)
            if getattr(self, "_drawer_open", False):
                self._sidebar.setGeometry(0, 52, 240, height - 52)
                self._sidebar.raise_()
            else:
                self._sidebar.setGeometry(-240, 52, 240, height - 52)
        else:
            self._drawer_scrim.setVisible(False)

    def _toggle_responsive_drawer(self, force_state=None) -> None:
        if not hasattr(self, "_drawer_open"):
            self._drawer_open = False
            
        next_state = force_state if force_state is not None else (not self._drawer_open)
        if next_state == self._drawer_open:
            return
            
        self._drawer_open = next_state
        
        self._drawer_scrim.setVisible(next_state)
        if next_state:
            self._drawer_scrim.raise_()
            self._sidebar.show()
            self._sidebar.raise_()
            
        from PyQt6.QtCore import QPropertyAnimation, QRect
        self._drawer_anim = QPropertyAnimation(self._sidebar, b"geometry")
        self._drawer_anim.setDuration(250)
        
        start_rect = QRect(-240, 52, 240, self.height() - 52)
        end_rect = QRect(0, 52, 240, self.height() - 52)
        
        if next_state:
            self._drawer_anim.setStartValue(start_rect)
            self._drawer_anim.setEndValue(end_rect)
        else:
            self._drawer_anim.setStartValue(end_rect)
            self._drawer_anim.setStartValue(start_rect)
            self._drawer_anim.finished.connect(lambda: self._sidebar.setVisible(False) if not self._drawer_open else None)
            
        self._drawer_anim.start()

    def _on_sidebar_page_changed(self, page_id: str) -> None:
        if getattr(self, "_drawer_open", False):
            self._toggle_responsive_drawer(force_state=False)

    def keyPressEvent(self, event) -> None:
        # Toggle Developer Debug Overlay via Ctrl+Shift+D
        if event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier) and event.key() == Qt.Key.Key_D:
            self._toggle_dev_overlay()
            event.accept()
        else:
            super().keyPressEvent(event)

    def _toggle_dev_overlay(self) -> None:
        if hasattr(self, "_dev_overlay") and self._dev_overlay:
            is_visible = not self._dev_overlay.isVisible()
            self._dev_overlay.setVisible(is_visible)
            if is_visible:
                self._dev_overlay.raise_()
                self._dev_overlay._reposition()
                self._toast_mgr.show_toast("success", "Dev Debug Overlay Diaktifkan | Tekan Ctrl+Shift+D untuk menutup")
            else:
                self._toast_mgr.show_toast("info", "Dev Debug Overlay Dinonaktifkan")

    def _init_tray_icon(self) -> None:
        """Initializes system tray integration with premium menus."""
        from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
        from PyQt6.QtGui import QIcon, QAction
        
        self._tray_icon = QSystemTrayIcon(self)
        
        # Use LOGO_PATH from app_paths (P1 fix — resolved correctly in packaged mode)
        icon_path = str(LOGO_PATH)
        if not os.path.exists(icon_path):
            icon_path = str(LOGO_PATH.parent.parent / "logo.png")
            
        if os.path.exists(icon_path):
            self._tray_icon.setIcon(QIcon(icon_path))
        else:
            from PyQt6.QtWidgets import QStyle
            self._tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
            
        # Context Menu styling
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #0B0F19;
                border: 1px solid #1F2937;
                color: #E2E8F0;
                font-size: 11px;
                font-weight: bold;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #38BDF8;
                color: #0B0F19;
            }
        """)
        
        act_open = QAction("Open CafePulse  📱", self)
        act_open.triggered.connect(self.show_and_raise)
        
        act_reconnect = QAction("Reconnect Router  🔌", self)
        act_reconnect.triggered.connect(self._reconnect_router_tray)
        
        act_license = QAction("Check License  🔑", self)
        act_license.triggered.connect(self._check_license_tray)
        
        act_settings = QAction("Settings  ⚙️", self)
        act_settings.triggered.connect(self._open_settings_tray)
        
        act_exit = QAction("Exit CafePulse  🚪", self)
        act_exit.triggered.connect(self._exit_immediately_tray)
        
        menu.addAction(act_open)
        menu.addSeparator()
        menu.addAction(act_reconnect)
        menu.addAction(act_license)
        menu.addAction(act_settings)
        menu.addSeparator()
        menu.addAction(act_exit)
        
        self._tray_icon.setContextMenu(menu)
        self._tray_icon.activated.connect(self._on_tray_activated)
        self._tray_icon.show()

    def show_and_raise(self) -> None:
        self.show()
        self.raise_()
        self.activateWindow()

    def _reconnect_router_tray(self) -> None:
        self.show_and_raise()
        self._on_page_changed("modes")
        self._sidebar.set_active_page("modes")
        self._start_mikrotik_mode()

    def _check_license_tray(self) -> None:
        self.show_and_raise()
        self._on_page_changed("settings")
        self._sidebar.set_active_page("settings")
        if hasattr(self, "_settings_page") and self._settings_page:
            self._settings_page.tabs.setCurrentIndex(1) # Index 1 is License Tab

    def _open_settings_tray(self) -> None:
        self.show_and_raise()
        self._on_page_changed("settings")
        self._sidebar.set_active_page("settings")
        if hasattr(self, "_settings_page") and self._settings_page:
            self._settings_page.tabs.setCurrentIndex(0) # Index 0 is General Tab

    def _exit_immediately_menu(self) -> None:
        """File -> Exit path. Bypasses tray, runs 14-item safety checklist."""
        self._close_app(force_bypass_tray=True)

    def _exit_immediately_tray(self) -> None:
        """Forces exit sequence using safe close analyzer, bypassing minimize to tray."""
        self._close_app(force_bypass_tray=True)

    def _on_tray_activated(self, reason) -> None:
        from PyQt6.QtWidgets import QSystemTrayIcon
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_and_raise()

    def _on_commit_data_request(self, manager) -> None:
        logger.info("[SHUTDOWN] OS Session Shutdown detected via commitDataRequest")
        self._finalize_and_exit()

    def closeEvent(self, event) -> None:
        if getattr(self, "_is_shutting_down", False):
            event.accept()
            return
        event.ignore()
        self._close_app(force_bypass_tray=False)

    def _close_app(self, force_bypass_tray: bool = False) -> None:
        """Intelligent Safe Close execution sequence."""
        logger.info("Safe Close Triggered")
        
        # 1. Fetch close behavior preferences
        close_behavior = self._config.get("general", "closing_behavior", default="smart_safe_close")
        is_first_time = self._config.get("general", "first_time_close", default=True)

        # 2. First-time close prompt behavior
        if is_first_time and not force_bypass_tray:
            dlg = FirstTimeCloseDialog(self)
            if dlg.exec():
                choice, remember = dlg.get_choice()
                if remember:
                    self._config.set("general", "first_time_close", value=False)
                    self._config.set("general", "closing_behavior", value=choice)
                close_behavior = choice
            else:
                logger.info("Safe Close Cancelled")
                return

        # 3. Handle 'Minimize to Tray' behavior if not bypassed
        if close_behavior == "minimize_to_tray" and not force_bypass_tray:
            logger.info("Minimizing to system tray.")
            self.hide()
            if hasattr(self, "_tray_icon") and self._tray_icon.isVisible():
                self._tray_icon.showMessage(
                    "CafePulse",
                    "Aplikasi tetap berjalan di System Tray latar belakang.",
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
            return

        # 4. Perform dynamic condition evaluation (Checklist Engine)
        unsaved = False
        if hasattr(self, "_settings_page") and self._settings_page:
            unsaved = self._settings_page.has_unsaved_changes()

        connected = False
        router_ip = self._config.get("mikrotik", "host", default="CHR")
        if self._current_mode == MODE_MIKROTIK and self._mikrotik_worker and self._mikrotik_worker.isRunning():
            connected = True

        # Detect active processes
        bg_tasks = []
        critical_operations = []

        if getattr(self, "is_backup_running", False):
            bg_tasks.append("Backup Router")
        if getattr(self, "is_restore_running", False):
            critical_operations.append("Restore Router")
        if getattr(self, "is_update_running", False):
            critical_operations.append("Firmware Update")
        if getattr(self, "is_config_pushing", False):
            critical_operations.append("Config Push")
        
        # Check active scans
        if self._app_state.is_scanning:
            bg_tasks.append("Running network scan / discovery")

        # 5. Smart level categorization
        level = 0
        desc = ""

        if critical_operations:
            level = 4
            desc = f"Operasi kritis '{', '.join(critical_operations)}' sedang berjalan di latar belakang. " \
                   f"Menutup paksa CafePulse saat ini berisiko tinggi merusak sistem router MikroTik atau menyebabkan kegagalan konfigurasi permanen."
        elif bg_tasks:
            level = 3
            desc = f"Proses '{', '.join(bg_tasks)}' masih berjalan aktif. " \
                   f"Menutup aplikasi saat ini akan membatalkan atau merusak file proses yang sedang diproduksi."
        elif connected:
            level = 2
            desc = f"Koneksi aktif ke MikroTik ({router_ip}) masih terjalin. " \
                   f"Apa yang ingin Anda lakukan?"
        elif unsaved:
            level = 1
            desc = f"Beberapa perubahan pengaturan CafePulse belum disimpan ke settings.json. " \
                   f"Apakah Anda ingin menyimpan perubahan tersebut terlebih dahulu?"

        # 6. Execute level categorization action
        if level == 0 or close_behavior == "exit_immediately":
            self._finalize_and_exit()
            return

        # Show Safe Close Dialog
        dlg = SafeCloseDialog(level, desc, router_ip, self)
        if dlg.exec():
            act = dlg.selected_action
            if act == "save_exit":
                if hasattr(self, "_settings_page") and self._settings_page:
                    self._settings_page._save_all()
                self._finalize_and_exit()
            elif act == "discard_exit" or act == "exit" or act == "force":
                self._finalize_and_exit()
            elif act == "wait_done":
                # GracefulShutdownMonitor already handled DB/config save.
                # Just mark clean shutdown and exit.
                from PyQt6.QtCore import QCoreApplication
                QCoreApplication.quit()
            elif act == "tray":
                logger.info("Minimizing to system tray from safe close dialog.")
                self.hide()
                if hasattr(self, "_tray_icon") and self._tray_icon.isVisible():
                    self._tray_icon.showMessage(
                        "CafePulse",
                        "Aplikasi berjalan di system tray.",
                        QSystemTrayIcon.MessageIcon.Information,
                        2000
                    )
            else:
                logger.info("Safe Close Cancelled")
        else:
            logger.info("Safe Close Cancelled")

    def _finalize_and_exit(self) -> None:
        """Performs database, logs, and worker safety checkpoints before exiting."""
        if getattr(self, "_is_shutting_down", False):
            return
        self._is_shutting_down = True
        
        # 1. Shutdown Started
        logger.info("[SHUTDOWN] Step 1: Shutdown Started")
        
        # 2. Save Session
        try:
            if hasattr(self, "_config") and self._config:
                current_page = getattr(self, "_current_page_id", "dashboard")
                self._config.set("general", "last_active_page", value=current_page)
            logger.info("[SHUTDOWN] Step 2 complete: Session Saved")
        except Exception as e:
            logger.error("[SHUTDOWN] Step 2 failed: Failed to save session: %s", e)

        # 3. Stop Workers
        try:
            self._stop_all_workers()
            logger.info("[SHUTDOWN] Step 3 complete: Workers Stopped")
        except Exception as e:
            logger.error("[SHUTDOWN] Step 3 failed: Failed to stop workers: %s", e)

        # 4. Commit Database
        try:
            if hasattr(self, "_db") and self._db:
                self._db.close()
            logger.info("[SHUTDOWN] Step 4 complete: Database Committed")
        except Exception as e:
            logger.error("[SHUTDOWN] Step 4 failed: Failed to commit database: %s", e)

        # 5. Save State
        try:
            if hasattr(self, "_config") and self._config:
                self._config.set("general", "last_exit_time", value=time.strftime("%Y-%m-%d %H:%M:%S"))
            logger.info("[SHUTDOWN] Step 5 complete: Save State")
        except Exception as e:
            logger.error("[SHUTDOWN] Step 5 failed: Failed to save state: %s", e)

        # 6. Mark Clean Shutdown — use CLEAN_FLAG & LOCK_FILE from app_paths (P0 fix)
        try:
            CLEAN_FLAG.parent.mkdir(parents=True, exist_ok=True)
            CLEAN_FLAG.touch(exist_ok=True)
            
            # Remove legacy lock file
            if LOCK_FILE.exists():
                try:
                    LOCK_FILE.unlink()
                except OSError:
                    pass
            logger.info("[SHUTDOWN] Step 6 complete: Clean Shutdown Completed")
        except Exception as e:
            logger.error("[SHUTDOWN] Step 6 failed: Failed to mark clean shutdown: %s", e)

        # 7. Flush Logs
        try:
            import logging
            logging.shutdown()
        except Exception:
            pass

        # 8. Exit Application
        from PyQt6.QtCore import QCoreApplication
        QCoreApplication.quit()
