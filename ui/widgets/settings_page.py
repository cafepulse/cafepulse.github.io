"""
CafePulse — Settings Page
Full settings UI backed by ConfigManager (config/settings.json).
All changes are persisted immediately to disk.
"""

import logging
import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QSpinBox, QCheckBox, QLineEdit, QComboBox,
    QScrollArea, QMessageBox, QGroupBox, QDialog,
    QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from ui.widgets.license_page import LicensePage

logger = logging.getLogger(__name__)


class SectionCard(QGroupBox):
    """Styled group box for a settings section."""
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
        self._form_rows = []  # List[ResponsiveFormRow]
        self.setStyleSheet("""
            QGroupBox {
                color: #E2E8F0;
                font-size: 13px;
                font-weight: 700;
                border: 1px solid #2D3748;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                background: #1A202C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #38BDF8;
            }
        """)
        self._inner = QVBoxLayout(self)
        self._inner.setContentsMargins(16, 16, 16, 16)
        self._inner.setSpacing(10)

    def add_row(self, label: str, widget: QWidget, hint: str = ""):
        from ui.widgets.responsive_form_row import ResponsiveFormRow
        row = ResponsiveFormRow(label, widget, hint)
        self._form_rows.append(row)
        self._inner.addWidget(row)

    def adapt_layout(self, bp: str) -> None:
        for row in self._form_rows:
            row.adapt_layout(bp)


    def update_theme(self, theme: str) -> None:
        """Style groupbox container and propagate to all form rows."""
        if theme == "light":
            self.setStyleSheet("""
                QGroupBox {
                    color: #0F172A;
                    font-size: 13px;
                    font-weight: 700;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 8px;
                    background: #FFFFFF;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 6px;
                    color: #0284C7;
                }
            """)
        else:
            self.setStyleSheet("""
                QGroupBox {
                    color: #E2E8F0;
                    font-size: 13px;
                    font-weight: 700;
                    border: 1px solid #2D3748;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 8px;
                    background: #1A202C;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 6px;
                    color: #38BDF8;
                }
            """)
        for row in self._form_rows:
            row.update_theme(theme)


_WIDGET_STYLE = """
    QSpinBox, QLineEdit, QComboBox {
        background: #2D3748;
        color: #E2E8F0;
        border: 1px solid #4A5568;
        border-radius: 5px;
        padding: 5px 8px;
        font-size: 12px;
        min-height: 28px;
    }
    QSpinBox:focus, QLineEdit:focus, QComboBox:focus {
        border-color: #38BDF8;
    }
    QCheckBox {
        color: #E2E8F0;
        font-size: 12px;
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 16px; height: 16px;
        border-radius: 3px;
        border: 1px solid #4A5568;
        background: #2D3748;
    }
    QCheckBox::indicator:checked {
        background: #38BDF8;
        border-color: #38BDF8;
    }
    QPushButton {
        background: #2D3748;
        color: #E2E8F0;
        border: 1px solid #4A5568;
        border-radius: 5px;
        padding: 6px 16px;
        font-size: 12px;
    }
    QPushButton:hover {
        background: #38BDF8;
        color: #0F172A;
        border-color: #38BDF8;
    }
    QPushButton#DangerButton {
        background: #2D1515;
        color: #FC8181;
        border-color: #742A2A;
    }
    QPushButton#DangerButton:hover {
        background: #FC8181;
        color: #1A202C;
        border-color: #FC8181;
    }
    QTabWidget::pane {
        border: 1px solid #2D3748;
        border-radius: 8px;
        background: #0F172A;
        padding: 18px;
    }
    QTabBar::tab {
        background: #1A202C;
        color: #94A3B8;
        border: 1px solid #2D3748;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 8px 18px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 4px;
    }
    QTabBar::tab:hover {
        background: #2D3748;
        color: #38BDF8;
    }
    QTabBar::tab:selected {
        background: #0F172A;
        color: #38BDF8;
        border-color: #38BDF8;
        border-bottom-color: #0F172A;
        font-weight: 700;
    }
"""


class SettingsPage(QWidget):
    """
    Full Settings page tabbed. Contains General and License tabs.
    Reads from and writes to ConfigManager.
    Emits settings_changed so the rest of the app can react.
    """
    settings_changed = pyqtSignal(str, object)  # (key_path, new_value)

    def __init__(self, config, db, app_state=None, parent=None):
        super().__init__(parent)
        self._config = config
        self._db = db
        self._app_state = app_state
        self._section_cards = []  # Track all SectionCards for adaptive breakpoint propagation
        self.setObjectName("ContentArea")
        self.setStyleSheet(_WIDGET_STYLE)
        self._build_ui()
        self._load_values()

    # ─── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Root Header
        title = QLabel("Settings")
        title.setObjectName("SectionHeader")
        root.addWidget(title)

        # Tab Widget
        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        # ── TAB 1: GENERAL SETTINGS ──
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(0, 12, 0, 0)
        general_layout.setSpacing(16)

        # Sub Header for general settings
        header = QHBoxLayout()
        sub = QLabel("Changes are saved automatically to config/settings.json")
        sub.setObjectName("SectionSubtitle")
        save_btn = QPushButton("Save All")
        save_btn.setFixedWidth(100)
        save_btn.setStyleSheet(
            "background:#38BDF8; color:#0F172A; border:none; border-radius:5px;"
            "padding:7px 16px; font-weight:700;"
        )
        save_btn.clicked.connect(self._save_all)
        header.addWidget(sub)
        header.addStretch()
        header.addWidget(save_btn)
        general_layout.addLayout(header)

        sub_lbl = QLabel("Changes are applied immediately. Restart may be required for window size changes.")
        sub_lbl.setStyleSheet("color:#4A5568; font-size:11px;")
        general_layout.addWidget(sub_lbl)

        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        inner.setMinimumWidth(450)
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(0, 0, 12, 0)
        inner_layout.setSpacing(16)

        # ── Network ────────────────────────────────────────────────────────────
        net_card = SectionCard("Network & Scanning")
        self._section_cards.append(net_card)

        self._spin_wifi_interval = QSpinBox()
        self._spin_wifi_interval.setRange(10, 300)
        self._spin_wifi_interval.setSuffix("  seconds")
        self._spin_wifi_interval.setFixedWidth(160)
        net_card.add_row("Home WiFi Scan Interval", self._spin_wifi_interval,
                         "How often to auto-scan for devices (10–300 s)")

        self._spin_hotspot_interval = QSpinBox()
        self._spin_hotspot_interval.setRange(5, 120)
        self._spin_hotspot_interval.setSuffix("  seconds")
        self._spin_hotspot_interval.setFixedWidth(160)
        net_card.add_row("Hotspot Scan Interval", self._spin_hotspot_interval,
                         "Refresh rate for hotspot client detection (5–120 s)")

        self._spin_scan_timeout = QSpinBox()
        self._spin_scan_timeout.setRange(1, 30)
        self._spin_scan_timeout.setSuffix("  seconds")
        self._spin_scan_timeout.setFixedWidth(160)
        net_card.add_row("Scan Timeout", self._spin_scan_timeout,
                         "Max wait per ping probe (1–30 s)")

        inner_layout.addWidget(net_card)

        # ── Database ───────────────────────────────────────────────────────────
        db_card = SectionCard("Database & Storage")
        self._section_cards.append(db_card)

        self._spin_cleanup_days = QSpinBox()
        self._spin_cleanup_days.setRange(1, 365)
        self._spin_cleanup_days.setSuffix("  days")
        self._spin_cleanup_days.setFixedWidth(160)
        db_card.add_row("Auto-cleanup Stale Devices", self._spin_cleanup_days,
                        "Remove devices not seen within this many days")

        cleanup_btn = QPushButton("Run Cleanup Now")
        cleanup_btn.setFixedWidth(160)
        cleanup_btn.clicked.connect(self._run_cleanup)
        db_card.add_row("Manual Cleanup", cleanup_btn)

        clear_btn = QPushButton("Clear All Devices")
        clear_btn.setObjectName("DangerButton")
        clear_btn.setFixedWidth(160)
        clear_btn.clicked.connect(self._clear_devices)
        db_card.add_row("Reset Device Database", clear_btn,
                        "Permanently deletes all stored devices, sessions, and logs")

        inner_layout.addWidget(db_card)

        # ── UI ─────────────────────────────────────────────────────────────────
        ui_card = SectionCard("User Interface")
        self._section_cards.append(ui_card)

        # Window Size row — these are STARTUP PREFERENCES only, not runtime locks.
        # The window remains freely resizable after launch; the responsive system handles reflow.
        win_size_row = QWidget()
        win_size_layout = QHBoxLayout(win_size_row)
        win_size_layout.setContentsMargins(0, 0, 0, 0)
        win_size_layout.setSpacing(8)

        self._spin_win_width = QSpinBox()
        self._spin_win_width.setRange(960, 3840)   # 960 = min usable responsive width
        self._spin_win_width.setSuffix("  W")
        self._spin_win_width.setMinimumWidth(90)
        self._spin_win_width.setMaximumWidth(130)

        self._spin_win_height = QSpinBox()
        self._spin_win_height.setRange(600, 2160)  # 600 = min usable responsive height
        self._spin_win_height.setSuffix("  H")
        self._spin_win_height.setMinimumWidth(90)
        self._spin_win_height.setMaximumWidth(130)

        self._btn_sync_winsize = QPushButton("📌  Pakai Saat Ini")
        self._btn_sync_winsize.setToolTip("Isi otomatis dengan ukuran window CafePulse saat ini")
        self._btn_sync_winsize.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_sync_winsize.setMinimumWidth(100)
        self._btn_sync_winsize.clicked.connect(self._sync_window_size)

        win_size_layout.addWidget(self._spin_win_width)
        win_size_layout.addWidget(QLabel("×"))
        win_size_layout.addWidget(self._spin_win_height)
        win_size_layout.addWidget(self._btn_sync_winsize)
        win_size_layout.addStretch()

        ui_card.add_row(
            "Startup Size (px)",
            win_size_row,
            "⚠ Preferensi startup saja — bukan kunci ukuran. Window tetap bisa di-resize bebas saat dipakai."
        )

        self._chk_animations = QCheckBox("Enable smooth animations and transitions")
        ui_card.add_row("Animations", self._chk_animations)

        self._combo_theme = QComboBox()
        self._combo_theme.addItems(["Dark Theme", "Light Theme"])
        self._combo_theme.setFixedWidth(160)
        ui_card.add_row("Visual Theme", self._combo_theme,
                        "Switch between Cyber-Dark and Premium Light Mode")

        inner_layout.addWidget(ui_card)

        # ── MikroTik Defaults ─────────────────────────────────────────────────
        mt_card = SectionCard("MikroTik Defaults")
        self._section_cards.append(mt_card)

        self._edit_mt_host = QLineEdit()
        self._edit_mt_host.setPlaceholderText("e.g. 192.168.88.1")
        self._edit_mt_host.setFixedWidth(220)
        mt_card.add_row("Default Router IP", self._edit_mt_host,
                        "Pre-filled in the MikroTik login dialog")

        self._spin_mt_port = QSpinBox()
        self._spin_mt_port.setRange(1, 65535)
        self._spin_mt_port.setFixedWidth(160)
        mt_card.add_row("API Port", self._spin_mt_port,
                        "Default is 8728 (8729 for SSL)")

        self._edit_mt_user = QLineEdit()
        self._edit_mt_user.setPlaceholderText("admin")
        self._edit_mt_user.setFixedWidth(220)
        mt_card.add_row("Default Username", self._edit_mt_user)

        self._chk_mt_save_session = QCheckBox("Simpan Sesi MikroTik secara Otomatis")
        mt_card.add_row("Simpan Sesi", self._chk_mt_save_session,
                        "Menyimpan kredensial sesi terakhir secara lokal untuk pemulihan otomatis")

        inner_layout.addWidget(mt_card)

        # ── Logging ────────────────────────────────────────────────────────────
        log_card = SectionCard("Logging")
        self._section_cards.append(log_card)

        self._combo_log_level = QComboBox()
        self._combo_log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self._combo_log_level.setFixedWidth(160)
        log_card.add_row("Log Level", self._combo_log_level,
                         "More verbose levels may slow down the app")

        inner_layout.addWidget(log_card)

        # ── Perilaku Penutupan (Closing Behavior) ──────────────────────────────
        close_card = SectionCard("Exit & Close Preferences")
        self._section_cards.append(close_card)
        
        self._combo_close_behavior = QComboBox()
        self._combo_close_behavior.addItems(["Smart Safe Close", "Exit Immediately", "Minimize to Tray"])
        self._combo_close_behavior.setFixedWidth(220)
        close_card.add_row("Closing Behavior", self._combo_close_behavior,
                           "Pilih perilaku aplikasi saat tombol X atau Alt+F4 ditekan.")
        inner_layout.addWidget(close_card)

        # ── Sistem Onboarding ──────────────────────────────────────────────────
        onb_card = SectionCard("Panduan & Onboarding")
        self._section_cards.append(onb_card)
        
        self.btn_reset_tutorials = QPushButton("Reset Panduan & Tutorial")
        self.btn_reset_tutorials.setFixedWidth(220)
        self.btn_reset_tutorials.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset_tutorials.clicked.connect(self._reset_tutorials_action)
        onb_card.add_row("Panduan Kontekstual", self.btn_reset_tutorials,
                         "Mengatur ulang penayangan seluruh bantuan visual kontekstual sekali-tayang")
                         
        inner_layout.addWidget(onb_card)

        inner_layout.addStretch()
        scroll.setWidget(inner)
        general_layout.addWidget(scroll)
        self.tabs.addTab(general_tab, "⚙️  General")

        # ── TAB 2: LICENSE MANAGEMENT ──
        self.license_page = LicensePage(app_state=self._app_state)
        # Forward license successfully changed signal
        self.license_page.license_changed.connect(lambda is_pro: self.settings_changed.emit("licensing", is_pro))
        self.tabs.addTab(self.license_page, "🔑  License")

    # ─── Responsive Layout Adaptation ────────────────────────────────────────

    def adapt_layout(self, bp: str) -> None:
        """Called by ResponsiveManager when breakpoint changes. Propagates to all form rows."""
        for card in self._section_cards:
            card.adapt_layout(bp)

    def _sync_window_size(self) -> None:
        """Reads the current MainWindow geometry and fills the startup-size spinboxes.
        
        This makes clear that the setting is a 'startup preference' not a lock:
        the user can resize freely, then optionally 'capture' the current size for next launch.
        """
        from PyQt6.QtWidgets import QApplication
        main_win = QApplication.activeWindow()
        # Walk up to find the top-level QMainWindow
        w = self.window()
        if w and w is not self:
            geo = w.size()
            new_w = max(960, min(3840, geo.width()))
            new_h = max(600, min(2160, geo.height()))
            self._spin_win_width.setValue(new_w)
            self._spin_win_height.setValue(new_h)
            try:
                from ui.widgets.toast_notification import ToastNotification
                ToastNotification.show_toast(
                    self,
                    f"📌  Ukuran startup diset ke {new_w} × {new_h} px (berlaku setelah restart)",
                    2500
                )
            except Exception:
                pass


    def has_unsaved_changes(self) -> bool:
        """Deterministically checks if the current widget values differ from persisted config."""
        try:
            if self._spin_wifi_interval.value() != int(self._config.get("network", "wifi_scan_interval_seconds", default=30)): return True
            if self._spin_hotspot_interval.value() != int(self._config.get("network", "hotspot_scan_interval_seconds", default=10)): return True
            if self._spin_scan_timeout.value() != int(self._config.get("network", "scan_timeout_seconds", default=5)): return True
            if self._spin_cleanup_days.value() != int(self._config.get("database", "auto_cleanup_days", default=30)): return True
            if self._spin_win_width.value() != int(self._config.get("ui", "window_width", default=1200)): return True
            if self._spin_win_height.value() != int(self._config.get("ui", "window_height", default=750)): return True
            if self._chk_animations.isChecked() != bool(self._config.get("ui", "animations_enabled", default=True)): return True
            
            theme_val = "light" if self._combo_theme.currentText() == "Light Theme" else "dark"
            if theme_val != self._config.get("ui", "theme", default="dark"): return True
            
            if self._edit_mt_host.text().strip() != self._config.get("mikrotik", "host", default=""): return True
            if self._spin_mt_port.value() != int(self._config.get("mikrotik", "port", default=8728)): return True
            if self._edit_mt_user.text().strip() != self._config.get("mikrotik", "username", default=""): return True
            if self._chk_mt_save_session.isChecked() != bool(self._config.get("mikrotik", "save_session", default=False)): return True
            
            if self._combo_log_level.currentText() != self._config.get("logging", "level", default="INFO"): return True

            close_behavior = self._config.get("general", "closing_behavior", default="smart_safe_close")
            behavior_map = {
                "smart_safe_close": "Smart Safe Close",
                "exit_immediately": "Exit Immediately",
                "minimize_to_tray": "Minimize to Tray"
            }
            if self._combo_close_behavior.currentText() != behavior_map.get(close_behavior, "Smart Safe Close"): return True
        except Exception:
            pass
        return False

    # ─── Load / Save ──────────────────────────────────────────────────────────

    def _load_values(self):
        """Read current config into widgets."""
        try:
            self._spin_wifi_interval.setValue(
                int(self._config.get("network", "wifi_scan_interval_seconds", default=30)))
            self._spin_hotspot_interval.setValue(
                int(self._config.get("network", "hotspot_scan_interval_seconds", default=10)))
            self._spin_scan_timeout.setValue(
                int(self._config.get("network", "scan_timeout_seconds", default=5)))

            self._spin_cleanup_days.setValue(
                int(self._config.get("database", "auto_cleanup_days", default=30)))

            self._spin_win_width.setValue(
                int(self._config.get("ui", "window_width", default=1200)))
            self._spin_win_height.setValue(
                int(self._config.get("ui", "window_height", default=750)))
            self._chk_animations.setChecked(
                bool(self._config.get("ui", "animations_enabled", default=True)))
            
            theme = self._config.get("ui", "theme", default="dark")
            idx = self._combo_theme.findText("Light Theme" if theme == "light" else "Dark Theme")
            if idx >= 0:
                self._combo_theme.setCurrentIndex(idx)

            self._edit_mt_host.setText(
                self._config.get("mikrotik", "host", default=""))
            self._spin_mt_port.setValue(
                int(self._config.get("mikrotik", "port", default=8728)))
            self._edit_mt_user.setText(
                self._config.get("mikrotik", "username", default=""))
            self._chk_mt_save_session.setChecked(
                bool(self._config.get("mikrotik", "save_session", default=False)))

            level = self._config.get("logging", "level", default="INFO")
            idx = self._combo_log_level.findText(level)
            if idx >= 0:
                self._combo_log_level.setCurrentIndex(idx)

            close_behavior = self._config.get("general", "closing_behavior", default="smart_safe_close")
            behavior_map = {
                "smart_safe_close": "Smart Safe Close",
                "exit_immediately": "Exit Immediately",
                "minimize_to_tray": "Minimize to Tray"
            }
            idx_close = self._combo_close_behavior.findText(behavior_map.get(close_behavior, "Smart Safe Close"))
            if idx_close >= 0:
                self._combo_close_behavior.setCurrentIndex(idx_close)
        except Exception as e:
            logger.error("Failed to load settings: %s", e)

    def _save_all(self):
        """Write all widget values to ConfigManager (auto-persists to JSON)."""
        try:
            self._config.set("network", "wifi_scan_interval_seconds",
                             value=self._spin_wifi_interval.value())
            self._config.set("network", "hotspot_scan_interval_seconds",
                             value=self._spin_hotspot_interval.value())
            self._config.set("network", "scan_timeout_seconds",
                             value=self._spin_scan_timeout.value())

            self._config.set("database", "auto_cleanup_days",
                             value=self._spin_cleanup_days.value())

            self._config.set("ui", "window_width",
                             value=self._spin_win_width.value())
            self._config.set("ui", "window_height",
                             value=self._spin_win_height.value())
            self._config.set("ui", "animations_enabled",
                             value=self._chk_animations.isChecked())
            
            theme_val = "light" if self._combo_theme.currentText() == "Light Theme" else "dark"
            self._config.set("ui", "theme", value=theme_val)

            self._config.set("mikrotik", "host",
                             value=self._edit_mt_host.text().strip())
            self._config.set("mikrotik", "port",
                             value=self._spin_mt_port.value())
            self._config.set("mikrotik", "username",
                             value=self._edit_mt_user.text().strip())
            self._config.set("mikrotik", "save_session",
                             value=self._chk_mt_save_session.isChecked())

            self._config.set("logging", "level",
                             value=self._combo_log_level.currentText())

            behavior_text = self._combo_close_behavior.currentText()
            behavior_val = "smart_safe_close"
            if behavior_text == "Exit Immediately":
                behavior_val = "exit_immediately"
            elif behavior_text == "Minimize to Tray":
                behavior_val = "minimize_to_tray"
            self._config.set("general", "closing_behavior", value=behavior_val)
            self.settings_changed.emit("general.closing_behavior", behavior_val)

            self.settings_changed.emit("all", None)
            logger.info("Settings saved by user.")
            self._ask_restart()
        except Exception as e:
            logger.error("Failed to save settings: %s", e)
            QMessageBox.warning(self, "Error", f"Failed to save settings:\n{e}")

    def _ask_restart(self) -> None:
        """Show a styled restart dialog after saving settings."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Settings Saved")
        dlg.setFixedWidth(420)
        dlg.setStyleSheet("""
            QDialog {
                background: #0F172A;
            }
            QLabel {
                color: #E2E8F0;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(16)

        # Icon + title row
        top_row = QHBoxLayout()
        icon_lbl = QLabel("✅")
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent;")
        top_row.addWidget(icon_lbl)
        top_row.addSpacing(10)
        title_col = QVBoxLayout()
        title_lbl = QLabel("Settings Saved")
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #E2E8F0;")
        sub_lbl = QLabel("All changes have been written to\nconfig/settings.json")
        sub_lbl.setStyleSheet("font-size: 11px; color: #64748B;")
        title_col.addWidget(title_lbl)
        title_col.addWidget(sub_lbl)
        top_row.addLayout(title_col)
        top_row.addStretch()
        layout.addLayout(top_row)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background: #1E293B; border: none; max-height: 1px;")
        layout.addWidget(div)

        # Info text
        info = QLabel(
            "Some changes (window size) require a restart to take effect.\n"
            "Other changes (scan interval, MikroTik, logging) are already active."
        )
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 11px; color: #94A3B8; background: transparent;")
        layout.addWidget(info)

        layout.addSpacing(8)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_later = QPushButton("Later")
        btn_later.setFixedSize(100, 34)
        btn_later.setStyleSheet(
            "QPushButton { background: #1E293B; color: #94A3B8; border: 1px solid #2D3748;"
            "border-radius: 6px; font-size: 12px; }"
            "QPushButton:hover { background: #2D3748; color: #E2E8F0; }"
        )
        btn_later.clicked.connect(dlg.reject)

        btn_restart = QPushButton("Restart Now")
        btn_restart.setFixedSize(120, 34)
        btn_restart.setStyleSheet(
            "QPushButton { background: #38BDF8; color: #0F172A; border: none;"
            "border-radius: 6px; font-size: 12px; font-weight: 700; }"
            "QPushButton:hover { background: #7DD3FC; }"
        )
        btn_restart.clicked.connect(lambda: self._do_restart(dlg))
        btn_restart.setDefault(True)

        btn_row.addWidget(btn_later)
        btn_row.addSpacing(8)
        btn_row.addWidget(btn_restart)
        layout.addLayout(btn_row)

        dlg.exec()

    def _do_restart(self, dlg: QDialog) -> None:
        """Close dialog and re-launch the application process."""
        dlg.accept()
        try:
            python = sys.executable
            args   = sys.argv
            logger.info("Restarting: %s %s", python, args)
            os.execv(python, [python] + args)
        except Exception as exc:
            logger.error("Restart failed: %s", exc)
            QMessageBox.warning(
                self, "Restart Failed",
                f"Could not restart automatically.\nPlease close and reopen CafePulse manually.\n\n{exc}"
            )

    # ─── Actions ──────────────────────────────────────────────────────────────

    def _run_cleanup(self):
        days = self._spin_cleanup_days.value()
        try:
            self._db.prune_stale_devices(days=days)
            QMessageBox.information(self, "Cleanup Complete",
                                    f"Removed devices not seen in the last {days} days.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cleanup failed:\n{e}")

    def _clear_devices(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "This will permanently delete ALL stored devices, sessions, and traffic logs.\n\n"
            "This action cannot be undone. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self._db.clear_all_devices()
                QMessageBox.information(self, "Done",
                                        "All device data has been cleared.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed:\n{e}")

    def _reset_tutorials_action(self):
        reply = QMessageBox.question(
            self, "Reset Panduan",
            "Apakah Anda yakin ingin mereset seluruh panduan awal dan bantuan tutorial di CafePulse?\n\n"
            "Semua layar sambutan dan visual tips kontekstual akan ditayangkan kembali.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from core.runtime.onboarding_manager import OnboardingManager
                mgr = OnboardingManager(self._config)
                mgr.reset_all_tutorials()
                QMessageBox.information(
                    self, "Reset Berhasil",
                    "Panduan & tutorial berhasil diatur ulang. Layar Onboarding akan kembali muncul pada startup berikutnya."
                )
            except Exception as e:
                QMessageBox.warning(self, "Gagal", f"Gagal mereset tutorial:\n{e}")
