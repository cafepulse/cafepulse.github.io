"""
CafePulse — Personal Network Discovery Page (Formerly Home WiFi Monitor)
Provides plug & play local ARP network scanning with clear platform limitation notices
and a dynamic Basic vs. Advanced view selector.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

logger = logging.getLogger("cafepulse.ui.personalnetwork")


class InfoRow(QWidget):
    """Key: Value display row with clean HSL styling."""
    def __init__(self, key: str, value: str = "—", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        key_lbl = QLabel(key)
        key_lbl.setFixedWidth(180)
        key_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500;")
        layout.addWidget(key_lbl)
        self._val_lbl = QLabel(value)
        self._val_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 600;")
        layout.addWidget(self._val_lbl)
        layout.addStretch()

    def set_value(self, v: str) -> None:
        self._val_lbl.setText(v)


class PersonalNetworkPage(QWidget):
    """
    Personal Network Discovery mode information and control panel.
    Incorporates Basic/Advanced toggle modes.
    """
    scan_requested = pyqtSignal(str)

    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._app_state = app_state
        self._last_payload = None
        self._is_advanced_mode = False
        self._build_ui()
        if self._app_state:
            self._app_state.privacy_masked_changed.connect(self._on_privacy_changed)

    def _on_privacy_changed(self, masked: bool) -> None:
        if self._last_payload:
            self._refresh_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Row (Title + Universal Badge + View Toggle)
        header_row = QHBoxLayout()
        header_title_layout = QVBoxLayout()
        title = QLabel("Deteksi Jaringan Pribadi")
        title.setObjectName("SectionHeader")
        header_title_layout.addWidget(title)

        sub = QLabel("Pemindaian perangkat LAN lokal — plug & play, tanpa perlu konfigurasi router.")
        sub.setObjectName("SectionSubtitle")
        header_title_layout.addWidget(sub)
        header_row.addLayout(header_title_layout)
        header_row.addStretch()

        # Universal Mode Badge
        badge = QLabel("Universal Mode")
        badge.setStyleSheet(
            "background-color: #1E293B; color: #38BDF8; font-size: 10px; font-weight: 700; "
            "padding: 6px 12px; border-radius: 12px; border: 1px solid #334155; margin-right: 10px;"
        )
        badge.setToolTip("Dapat digunakan pada jaringan apapun tanpa ketergantungan pada router MikroTik.")
        header_row.addWidget(badge)

        # Basic / Advanced View Toggle
        self.toggle_view_btn = QPushButton("Tampilan: Dasar  ⚙️")
        self.toggle_view_btn.setStyleSheet(
            "QPushButton { background-color: #1E293B; color: #E2E8F0; font-size: 11px; font-weight: 600; "
            "padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.toggle_view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_view_btn.clicked.connect(self._toggle_advanced_view)
        header_row.addWidget(self.toggle_view_btn)

        layout.addLayout(header_row)

        # ── Info Card (Always Visible) ────────────────────────────────────────
        info_card = QFrame()
        info_card.setObjectName("DashCard")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(18, 16, 18, 16)
        info_layout.setSpacing(8)

        card_title = QLabel("INFORMASI DETEKSI JARINGAN")
        card_title.setObjectName("DashCardTitle")
        info_layout.addWidget(card_title)

        self._row_local_ip  = InfoRow("IP Komputer Anda (Local IP)")
        self._row_subnet    = InfoRow("Subnet yang Dideteksi")
        self._row_devices   = InfoRow("Perangkat Ditemukan",    "0")
        self._row_last_scan = InfoRow("Pemindaian Terakhir",    "—")
        self._row_duration  = InfoRow("Durasi Pemindaian",      "—")
        self._row_new       = InfoRow("Perangkat Baru Terdeteksi", "0")

        for row in (self._row_local_ip, self._row_subnet,
                    self._row_devices, self._row_last_scan, self._row_duration, self._row_new):
            info_layout.addWidget(row)

        layout.addWidget(info_card)

        # ── Advanced Settings Card (Only shown in Advanced Mode) ──────────────
        self.adv_settings_card = QFrame()
        self.adv_settings_card.setObjectName("DashCard")
        self.adv_settings_card.setStyleSheet("background-color: #111625; border-left: 3px solid #06B6D4;")
        adv_layout = QVBoxLayout(self.adv_settings_card)
        adv_layout.setContentsMargins(18, 16, 18, 16)
        adv_layout.setSpacing(10)

        adv_title = QLabel("PENGATURAN PEMINDAIAN LANJUTAN (ADVANCED)")
        adv_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        adv_layout.addWidget(adv_title)

        # Subnet Override Input
        subnet_row = QHBoxLayout()
        subnet_lbl = QLabel("Override Subnet:")
        subnet_lbl.setFixedWidth(180)
        subnet_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        subnet_row.addWidget(subnet_lbl)

        self._subnet_input = QLineEdit()
        self._subnet_input.setPlaceholderText("Deteksi Otomatis (contoh: 192.168.1.0/24)")
        self._subnet_input.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;"
        )
        subnet_row.addWidget(self._subnet_input)
        adv_layout.addLayout(subnet_row)

        # Interface Select (Simulation or Dynamic Interface binding)
        interface_row = QHBoxLayout()
        interface_lbl = QLabel("Pilih Interface Fisik:")
        interface_lbl.setFixedWidth(180)
        interface_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
        interface_row.addWidget(interface_lbl)

        self.interface_combo = QComboBox()
        self.interface_combo.addItems(["Auto-detect", "Ethernet (LAN)", "Wi-Fi (Wireless Adapter)"])
        self.interface_combo.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;"
        )
        interface_row.addWidget(self.interface_combo)
        adv_layout.addLayout(interface_row)

        # Ping settings
        ping_row = QHBoxLayout()
        self.ping_sweep_chk = QCheckBox("Lakukan Ping Sweep (Lebih Akurat, Lebih Lambat)")
        self.ping_sweep_chk.setChecked(True)
        self.ping_sweep_chk.setStyleSheet("color: #94A3B8; font-size: 11px;")
        ping_row.addWidget(self.ping_sweep_chk)
        adv_layout.addLayout(ping_row)

        layout.addWidget(self.adv_settings_card)
        self.adv_settings_card.setVisible(False) # Default hidden

        # ── Control & Action Area ─────────────────────────────────────────────
        action_row = QHBoxLayout()
        self._scan_btn = QPushButton("⟳  Mulai Pindai Jaringan")
        self._scan_btn.setObjectName("QuickScanButton")
        self._scan_btn.setFixedWidth(220)
        self._scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scan_btn.clicked.connect(self._on_scan_clicked)
        action_row.addWidget(self._scan_btn)
        action_row.addStretch()
        layout.addLayout(action_row)

        # ── Limitation Notice (Styled using Warm HSL Warning Palette) ─────────
        notice = QFrame()
        notice.setObjectName("DashCard")
        notice.setStyleSheet(
            "QFrame#DashCard { border-left: 3px solid #F59E0B; background-color: #1A130C; }"
        )
        notice_layout = QVBoxLayout(notice)
        notice_layout.setContentsMargins(18, 14, 18, 14)
        notice_layout.setSpacing(6)

        notice_title = QLabel("⚠  Batasan Deteksi Mandiri (Universal Mode)")
        notice_title.setStyleSheet("color: #F59E0B; font-size: 13px; font-weight: 700;")
        notice_layout.addWidget(notice_title)

        notice_text = QLabel(
            "Modul ini memindai jaringan menggunakan protokol ARP standar lokal Anda. "
            "Aplikasi tidak memiliki kendali langsung untuk membatasi kecepatan, menetapkan kuota data, "
            "atau memutus koneksi pelanggan secara otomatis tanpa adanya router MikroTik yang terintegrasi.\n\n"
            "Untuk kontrol bandwidth dan manajemen voucher penuh, silakan beralih ke Mode MikroTik di menu Switcher."
        )
        notice_text.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.5;")
        notice_text.setWordWrap(True)
        notice_layout.addWidget(notice_text)

        layout.addWidget(notice)

        # ── Status Bar ────────────────────────────────────────────────────────
        self._status_label = QLabel("Siap — Klik 'Mulai Pindai Jaringan' untuk mendeteksi perangkat lokal")
        self._status_label.setStyleSheet("color: #64748B; font-size: 11px; padding-top: 4px;")
        layout.addWidget(self._status_label)

        layout.addStretch()

    def _toggle_advanced_view(self) -> None:
        self._is_advanced_mode = not self._is_advanced_mode
        self.adv_settings_card.setVisible(self._is_advanced_mode)
        if self._is_advanced_mode:
            self.toggle_view_btn.setText("Tampilan: Lanjutan  🛠️")
            self.toggle_view_btn.setStyleSheet(
                "QPushButton { background-color: #0F172A; color: #06B6D4; font-size: 11px; font-weight: 600; "
                "padding: 6px 12px; border-radius: 6px; border: 1px solid #06B6D4; }"
            )
        else:
            self.toggle_view_btn.setText("Tampilan: Dasar  ⚙️")
            self.toggle_view_btn.setStyleSheet(
                "QPushButton { background-color: #1E293B; color: #E2E8F0; font-size: 11px; font-weight: 600; "
                "padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }"
            )

    # ─── Slots ────────────────────────────────────────────────────────────────

    def _on_scan_clicked(self) -> None:
        subnet = self._subnet_input.text().strip() or None
        self.scan_requested.emit(subnet or "")
        self.set_scanning(True)

    @pyqtSlot(dict)
    def update_from_scan(self, payload: dict) -> None:
        self._last_payload = payload
        self._refresh_ui()
        self.set_scanning(False)

    def _refresh_ui(self) -> None:
        if not self._last_payload:
            return
        payload = self._last_payload
        local_ip = payload.get("local_ip", "—")
        subnet = payload.get("subnet", "—")

        # Apply operator-privacy masking if active
        is_privacy_masked = self._app_state and getattr(self._app_state, "privacy_masked", False)
        if is_privacy_masked:
            if local_ip and "." in local_ip:
                ip_parts = local_ip.split(".")
                if len(ip_parts) == 4:
                    local_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.*"
            if subnet and "." in subnet:
                sub_parts = subnet.split(".")
                if len(sub_parts) >= 3:
                    subnet = f"{sub_parts[0]}.{sub_parts[1]}.{sub_parts[2]}.0/*"

        self._row_local_ip.set_value(local_ip)
        self._row_subnet.set_value(subnet)
        self._row_devices.set_value(str(payload.get("device_count", 0)))
        duration = payload.get("scan_duration", 0)
        self._row_last_scan.set_value(payload.get("last_scan_time", "—"))
        self._row_duration.set_value(f"{duration:.1f} detik")
        self._row_new.set_value(str(len(payload.get("new_devices", []))))

        err = payload.get("error")
        if err:
            self._status_label.setText(f"⚠  Gagal melakukan scan: {err}")
            self._status_label.setStyleSheet("color: #EF4444; font-size: 11px;")
        else:
            self._status_label.setText(
                f"✓  Scan jaringan berhasil — {payload.get('device_count', 0)} perangkat ditemukan"
            )
            self._status_label.setStyleSheet("color: #22C55E; font-size: 11px;")

    def set_scanning(self, active: bool) -> None:
        self._scan_btn.setEnabled(not active)
        self._scan_btn.setText("⟳  Memindai Jaringan…" if active else "⟳  Mulai Pindai Jaringan")
        if active:
            self._status_label.setText("Memindai perangkat... proses ini memakan waktu sekitar 15-30 detik.")
            self._status_label.setStyleSheet("color: #38BDF8; font-size: 11px;")
