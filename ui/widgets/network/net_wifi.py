"""
CafePulse — WiFi & Wireless Configuration Page (Phase 8)
Supports SSIDs, security profiles, Access Point parameters, and dynamic hardware check fallbacks.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit, QComboBox,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot


class NetWifi(QWidget):
    """
    WiFi control panel with dynamic "Not Available" placeholder fallback.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._has_wireless_hardware = False # Default simulation fallback
        self._build_ui()

    def _build_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(14)

        # ── Standard Setup Layout (Only active if hardware exists) ─────────────
        self.setup_widget = QWidget()
        setup_layout = QVBoxLayout(self.setup_widget)
        setup_layout.setContentsMargins(0, 0, 0, 0)
        setup_layout.setSpacing(14)

        wifi_card = QFrame()
        wifi_card.setObjectName("DashCard")
        wifi_layout = QVBoxLayout(wifi_card)
        wifi_layout.setContentsMargins(16, 14, 16, 14)
        wifi_layout.setSpacing(12)

        wifi_title = QLabel("WiFi ACCESS POINT CONFIGURATION")
        wifi_title.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 700;")
        wifi_layout.addWidget(wifi_title)

        # SSID name input
        ssid_row = QHBoxLayout()
        ssid_lbl = QLabel("SSID Jaringan WiFi:")
        ssid_lbl.setFixedWidth(160)
        ssid_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        ssid_row.addWidget(ssid_lbl)

        self.ssid_input = QLineEdit("CafePulse_Hotspot")
        self.ssid_input.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 8px; color: white;"
        )
        ssid_row.addWidget(self.ssid_input)
        wifi_layout.addLayout(ssid_row)

        # Security mode
        sec_row = QHBoxLayout()
        sec_lbl = QLabel("Protokol Keamanan:")
        sec_lbl.setFixedWidth(160)
        sec_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        sec_row.addWidget(sec_lbl)

        self.sec_combo = QComboBox()
        self.sec_combo.addItems(["Open (Tanpa Sandi)", "WPA2-PSK (Personal)", "WPA3-SAE (Aman)"])
        self.sec_combo.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 8px; color: white;"
        )
        sec_row.addWidget(self.sec_combo)
        wifi_layout.addLayout(sec_row)

        # Password
        pwd_row = QHBoxLayout()
        pwd_lbl = QLabel("Sandi WPA/WPA2:")
        pwd_lbl.setFixedWidth(160)
        pwd_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        pwd_row.addWidget(pwd_lbl)

        self.pwd_input = QLineEdit("12345678")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 8px; color: white;"
        )
        pwd_row.addWidget(self.pwd_input)
        wifi_layout.addLayout(pwd_row)

        # Actions
        act_row = QHBoxLayout()
        act_row.addStretch()
        self.save_btn = QPushButton("Terapkan Konfigurasi WiFi  ✓")
        self.save_btn.setObjectName("QuickScanButton")
        self.save_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.save_btn.clicked.connect(self._on_save_wifi)
        act_row.addWidget(self.save_btn)
        wifi_layout.addLayout(act_row)

        setup_layout.addWidget(wifi_card)
        setup_layout.addStretch()
        self.main_layout.addWidget(self.setup_widget)

        # ── Fallback Placeholder (Only active if hardware DOES NOT exist) ─────
        self.fallback_widget = QFrame()
        self.fallback_widget.setObjectName("DashCard")
        self.fallback_widget.setStyleSheet("QFrame#DashCard { border-left: 3px solid #F59E0B; background-color: #1E1B18; }")
        fallback_layout = QVBoxLayout(self.fallback_widget)
        fallback_layout.setContentsMargins(24, 24, 24, 24)
        fallback_layout.setSpacing(12)

        lock_icon = QLabel("📶")
        lock_icon.setStyleSheet("font-size: 32px; text-align: center;")
        lock_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fallback_layout.addWidget(lock_icon)

        fallback_title = QLabel("WiFi & Wireless Interface Tidak Tersedia")
        fallback_title.setStyleSheet("color: #F59E0B; font-size: 15px; font-weight: 700;")
        fallback_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fallback_layout.addWidget(fallback_title)

        fallback_text = QLabel(
            "Perangkat router MikroTik yang terhubung saat ini tidak mendeteksi adanya chip nirkabel Wi-Fi fisik "
            "(misalnya MikroTik CCR, Cloud Hosted Router virtual, atau generic x86 PC router).\n\n"
            "Jika Anda menggunakan AP eksternal (seperti UniFi atau Ruijie), kelola jaringan nirkabel secara langsung "
            "melalui kontroler AP tersebut. CafePulse akan mengelola alokasi IP & bandwidth-nya secara universal."
        )
        fallback_text.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.6;")
        fallback_text.setWordWrap(True)
        fallback_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fallback_layout.addWidget(fallback_text)

        self.main_layout.addWidget(self.fallback_widget)

        # Apply visibility initially
        self.set_hardware_present(self._has_wireless_hardware)

    def set_hardware_present(self, present: bool) -> None:
        self._has_wireless_hardware = present
        self.setup_widget.setVisible(present)
        self.fallback_widget.setVisible(not present)

    def update_from_mikrotik(self, payload: dict) -> None:
        # Check if connected router has wireless support
        has_wireless = payload.get("has_wireless", False)
        self.set_hardware_present(has_wireless)

    def _on_save_wifi(self) -> None:
        ssid = self.ssid_input.text()
        QMessageBox.information(self, "WiFi Disimpan", f"SSID Jaringan diset ke: {ssid}")
