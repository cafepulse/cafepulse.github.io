"""
CafePulse — IAM Guest Access Sub-View
Quick, frictionless temporary visitor provisioning.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from core.iam.voucher_manager import VoucherManager


class IamGuests(QWidget):
    """
    Friction-free visitor provisioning panel.
    """
    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("DashCard")
        card.setStyleSheet("background-color: #0F131F;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        title = QLabel("WiFi Tamu Cepat (Guest Access)")
        title.setStyleSheet("color: #E2E8F0; font-size: 16px; font-weight: 700;")
        card_layout.addWidget(title)

        desc = QLabel(
            "Berikan akses internet sementara untuk tamu, rekan bisnis, atau pengunjung kantor Anda secara instan. "
            "Sistem akan menerbitkan kode token sekali pakai dengan batasan waktu aktif rendah secara otomatis tanpa biaya jual."
        )
        desc.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.5;")
        desc.setWordWrap(True)
        card_layout.addWidget(desc)

        # Config Row
        config_row = QHBoxLayout()
        config_row.setSpacing(14)

        duration_lbl = QLabel("Pilih Batas Waktu:")
        duration_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600;")
        config_row.addWidget(duration_lbl)

        self.guest_dur = QComboBox()
        self.guest_dur.addItems(["1 Jam (Gratis)", "3 Jam (Gratis)", "12 Jam (Gratis)", "1 Hari (Gratis)"])
        self.guest_dur.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 8px; color: white;")
        config_row.addWidget(self.guest_dur)
        config_row.addStretch()

        card_layout.addLayout(config_row)

        # Generate Button
        btn_layout = QHBoxLayout()
        self.gen_btn = QPushButton("Buat Akses Tamu  🔑")
        self.gen_btn.setObjectName("QuickScanButton")
        self.gen_btn.setStyleSheet(
            "QPushButton { background-color: #A78BFA; color: white; padding: 12px 24px; font-size: 13px; font-weight: 700; border-radius: 6px; }"
            "QPushButton:hover { background-color: #8B5CF6; }"
        )
        self.gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gen_btn.clicked.connect(self._on_generate_guest)
        btn_layout.addWidget(self.gen_btn)
        btn_layout.addStretch()
        card_layout.addLayout(btn_layout)

        # Result display
        self.result_box = QFrame()
        self.result_box.setStyleSheet("background-color: #07090D; border: 1px solid #334155; border-radius: 8px;")
        self.result_layout = QVBoxLayout(self.result_box)
        self.result_layout.setContentsMargins(16, 16, 16, 16)
        self.result_layout.setSpacing(8)
        self.result_box.setVisible(False)

        res_title = QLabel("TOKEN AKSES TAMU AKTIF")
        res_title.setStyleSheet("color: #22C55E; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        self.result_layout.addWidget(res_title)

        self.res_code = QLabel("Token: GUEST-XXXX")
        self.res_code.setStyleSheet("color: #E2E8F0; font-size: 18px; font-weight: 800;")
        self.result_layout.addWidget(self.res_code)

        self.res_limit = QLabel("Batasan: 1 Jam Gratis @ 2 Mbps")
        self.res_limit.setStyleSheet("color: #64748B; font-size: 12px;")
        self.result_layout.addWidget(self.res_limit)

        card_layout.addWidget(self.result_box)
        layout.addWidget(card)

        # Notice
        notice = QLabel("Hanya perlu dibagikan secara lisan atau ditulis pada papan tamu.")
        notice.setStyleSheet("color: #475569; font-size: 11px; font-style: italic;")
        layout.addWidget(notice)

        layout.addStretch()

    def _on_generate_guest(self) -> None:
        duration_text = self.guest_dur.currentText()
        
        # Determine duration in seconds
        duration_sec = 3600
        if "3 Jam" in duration_text: duration_sec = 3600 * 3
        elif "12 Jam" in duration_text: duration_sec = 3600 * 12
        elif "1 Hari" in duration_text: duration_sec = 86400

        try:
            # Check if our "guest" package exists in SQLite, if not auto-create it
            pkg = self._db.fetchone("SELECT id FROM access_packages WHERE id='guest_free'")
            if not pkg:
                self._db.add_access_package(
                    pkg_id="guest_free",
                    name="Tamu Gratis",
                    pkg_type="DURATION",
                    duration_sec=duration_sec,
                    quota_bytes=0,
                    speed_dn=2048, # 2 Mbps suggestion
                    speed_up=1024, # 1 Mbps suggestion
                    price=0.0
                )

            # Generate standard random code for guest
            api = None
            main_window = self.window()
            if hasattr(main_window, "_mikrotik_worker") and main_window._mikrotik_worker:
                api = main_window._mikrotik_worker.manager.get_api()

            codes = VoucherManager.provision_vouchers(
                self._db, api,
                package_id="guest_free",
                count=1,
                length=5,
                prefix="GUEST-",
                numeric_only=True
            )

            if codes:
                self.result_box.setVisible(True)
                self.res_code.setText(f"Token: <span style='color: #A78BFA; font-weight: 800;'>{codes[0]}</span>")
                self.res_limit.setText(f"Batasan: Aktif selama {duration_text} | Kecepatan suguhan: 2 Mbps")
                
                if hasattr(main_window, "_toast_mgr"):
                    main_window._toast_mgr.show_toast("success", f"Akses Tamu '{codes[0]}' berhasil diterbitkan.")
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal membuat akses tamu:\n{e}")
