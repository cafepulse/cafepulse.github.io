"""
CafePulse — Top Bar Widget
Displays current mode, network status, device count, and quick-scan button.
"""

import logging
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal

logger = logging.getLogger("cafepulse.ui.topbar")


class TopBar(QWidget):
    """
    Horizontal bar fixed at top of content area.
    Signals: scan_requested(), exit_demo_requested()
    """

    hamburger_clicked = pyqtSignal()
    scan_requested = pyqtSignal()
    exit_demo_requested = pyqtSignal()

    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.setFixedHeight(52)
        self._app_state = app_state
        self._build_ui()
        
        if self._app_state:
            self._app_state.mode_changed.connect(self.set_mode)
            self._app_state.devices_updated.connect(self.set_device_count)
            self._app_state.status_updated.connect(self.set_status)
            self._app_state.bandwidth_updated.connect(self._on_bandwidth_updated)
            self._app_state.privacy_masked_changed.connect(self.update_privacy_button_state)

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        # Collapsible Hamburger button for Responsive layouts
        self._hamburger_btn = QPushButton("☰")
        self._hamburger_btn.setObjectName("HamburgerButton")
        self._hamburger_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._hamburger_btn.setStyleSheet("""
            QPushButton#HamburgerButton {
                background: transparent;
                color: #CBD5E1;
                border: none;
                font-size: 18px;
                font-weight: bold;
                padding: 4px 8px;
                min-width: 32px;
                max-width: 32px;
            }
            QPushButton#HamburgerButton:hover {
                color: #06B6D4;
                background-color: rgba(30, 41, 59, 0.5);
                border-radius: 4px;
            }
        """)
        self._hamburger_btn.setVisible(False)
        self._hamburger_btn.clicked.connect(self.hamburger_clicked.emit)
        layout.addWidget(self._hamburger_btn)

        # Mode pill layout
        mode_layout = QHBoxLayout()
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(8)

        self._mode_label = QLabel("DEMO MODE")
        self._mode_label.setObjectName("TopBarModeLabel")
        mode_layout.addWidget(self._mode_label)

        # Subtle premium exit button for Demo Mode
        self._exit_demo_btn = QPushButton("Exit Demo")
        self._exit_demo_btn.setObjectName("ExitDemoButton")
        self._exit_demo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._exit_demo_btn.setStyleSheet("""
            QPushButton#ExitDemoButton {
                background-color: rgba(239, 68, 68, 0.12);
                color: #EF4444;
                border: 1px solid rgba(239, 68, 68, 0.35);
                border-radius: 6px;
                padding: 3px 10px;
                font-size: 10px;
                font-weight: 700;
                min-height: 18px;
            }
            QPushButton#ExitDemoButton:hover {
                background-color: #EF4444;
                color: white;
                border-color: #EF4444;
            }
        """)
        self._exit_demo_btn.setVisible(False)
        self._exit_demo_btn.clicked.connect(self.exit_demo_requested.emit)
        mode_layout.addWidget(self._exit_demo_btn)

        layout.addLayout(mode_layout)

        layout.addStretch()

        # Status dot + label
        self._status_dot = QLabel("●")
        self._status_dot.setObjectName("TopBarStatusDot")
        self._status_dot.setStyleSheet("color: #22C55E; font-size: 10px;")
        layout.addWidget(self._status_dot)

        self._status_label = QLabel("Network OK")
        self._status_label.setObjectName("TopBarStatusLabel")
        layout.addWidget(self._status_label)

        layout.addSpacing(20)

        # Device count
        device_icon = QLabel("⬡")
        device_icon.setStyleSheet("color: #38BDF8; font-size: 14px;")
        layout.addWidget(device_icon)

        self._device_count = QLabel("0 devices")
        self._device_count.setObjectName("TopBarDeviceCount")
        layout.addWidget(self._device_count)

        layout.addSpacing(16)

        # Live bandwidth
        up_icon = QLabel("↑")
        up_icon.setStyleSheet("color: #F59E0B; font-size: 12px; font-weight: 700;")
        layout.addWidget(up_icon)
        self._upload_speed = QLabel("0 B/s")
        self._upload_speed.setStyleSheet(
            "color: #F59E0B; font-size: 11px; font-weight: 600;"
        )
        layout.addWidget(self._upload_speed)

        layout.addSpacing(4)

        dn_icon = QLabel("↓")
        dn_icon.setStyleSheet("color: #A78BFA; font-size: 12px; font-weight: 700;")
        layout.addWidget(dn_icon)
        self._download_speed = QLabel("0 B/s")
        self._download_speed.setStyleSheet(
            "color: #A78BFA; font-size: 11px; font-weight: 600;"
        )
        layout.addWidget(self._download_speed)

        layout.addSpacing(16)

        # Privacy toggle button
        self._privacy_btn = QPushButton("👁  Unmasked")
        self._privacy_btn.setObjectName("PrivacyButton")
        self._privacy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._privacy_btn.clicked.connect(self._toggle_privacy)
        layout.addWidget(self._privacy_btn)

        # Quick scan button
        self._scan_btn = QPushButton("⟳  Quick Scan")
        self._scan_btn.setObjectName("QuickScanButton")
        self._scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scan_btn.clicked.connect(self.scan_requested.emit)
        layout.addWidget(self._scan_btn)

    # ─── External Updates ─────────────────────────────────────────────────────

    def set_mode(self, mode_name: str) -> None:
        self._mode_label.setText(mode_name.upper())
        is_demo = "DEMO" in mode_name.upper()
        self._exit_demo_btn.setVisible(is_demo)

    def set_status(self, ok: bool, label: str = "") -> None:
        if ok:
            self._status_dot.setStyleSheet("color: #22C55E; font-size: 10px;")
            self._status_label.setText(label or "Network OK")
        else:
            self._status_dot.setStyleSheet("color: #EF4444; font-size: 10px;")
            self._status_label.setText(label or "Disconnected")

    def set_device_count(self, count: int) -> None:
        self._device_count.setText(f"{count} device{'s' if count != 1 else ''}")

    def set_scanning(self, scanning: bool) -> None:
        self._scan_btn.setEnabled(not scanning)
        self._scan_btn.setText("⟳  Scanning…" if scanning else "⟳  Quick Scan")

    def set_bandwidth(self, upload_str: str, download_str: str) -> None:
        self._upload_speed.setText(upload_str)
        self._download_speed.setText(download_str)

    from PyQt6.QtCore import pyqtSlot

    @pyqtSlot(dict)
    def _on_bandwidth_updated(self, payload: dict) -> None:
        self.set_bandwidth(payload.get("upload_display", "0 B/s"), payload.get("download_display", "0 B/s"))

    def _toggle_privacy(self) -> None:
        if not self._app_state:
            return
        is_masked = not self._app_state.privacy_masked
        self._app_state.privacy_masked = is_masked
        self._app_state.privacy_masked_changed.emit(is_masked)
        
        main_win = self.window()
        if main_win and hasattr(main_win, "_toast_mgr") and main_win._toast_mgr:
            status_str = "AKTIF (Data Sensitif Sensor)" if is_masked else "NONAKTIF (Data Terbuka)"
            main_win._toast_mgr.show_toast(
                "success" if is_masked else "info",
                f"Privacy Masking {status_str}"
            )

    @pyqtSlot(bool)
    def update_privacy_button_state(self, is_masked: bool) -> None:
        if is_masked:
            self._privacy_btn.setText("🕶  Masked")
            self._privacy_btn.setStyleSheet("""
                QPushButton#PrivacyButton {
                    background-color: rgba(245, 158, 11, 0.15);
                    color: #F59E0B;
                    border: 1px solid rgba(245, 158, 11, 0.5);
                    border-radius: 6px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: 700;
                    min-height: 24px;
                }
                QPushButton#PrivacyButton:hover {
                    background-color: rgba(245, 158, 11, 0.25);
                }
            """)
        else:
            self._privacy_btn.setText("👁  Unmasked")
            self._privacy_btn.setStyleSheet("""
                QPushButton#PrivacyButton {
                    background-color: rgba(56, 189, 248, 0.12);
                    color: #38BDF8;
                    border: 1px solid rgba(56, 189, 248, 0.35);
                    border-radius: 6px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: 600;
                    min-height: 24px;
                }
                QPushButton#PrivacyButton:hover {
                    background-color: rgba(56, 189, 248, 0.25);
                }
            """)

    def set_hamburger_visible(self, visible: bool) -> None:
        self._hamburger_btn.setVisible(visible)
