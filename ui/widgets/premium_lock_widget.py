import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from core.licensing.licensing_manager import LicensingManager

logger = logging.getLogger("cafepulse.ui.premium_lock")

class PremiumLockWidget(QWidget):
    """
    Elegant, premium, and cyber-clean overlay widget used to gate PRO features.
    Provides local offline license activation out-of-the-box.
    """
    
    activation_success = pyqtSignal()

    def __init__(self, feature_name: str, parent_app_state=None, parent=None):
        super().__init__(parent)
        self.feature_name = feature_name
        self.app_state = parent_app_state
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #0B0E14;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Card container for professional look
        card = QFrame()
        card.setObjectName("PremiumCard")
        card.setFixedWidth(560)
        card.setStyleSheet("""
            QFrame#PremiumCard {
                background-color: #0F131E;
                border: 1px solid #1F273E;
                border-radius: 16px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)

        # Glowing cyan lock icon
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setText("🔒")
        icon_label.setStyleSheet("font-size: 54px; color: #06B6D4; background: transparent;")
        card_layout.addWidget(icon_label)

        # Feature Gated Info
        title_label = QLabel(f"Buka Fitur: {self.feature_name}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #F8FAFC;
            background: transparent;
        """)
        card_layout.addWidget(title_label)

        desc_label = QLabel(
            "Fitur ini eksklusif untuk edisi **CafePulse Professional**.\n"
            "Dapatkan kendali penuh, monitoring realtime, visualisasi topologi, "
            "dan otomatisasi canggih dengan mengaktifkan lisensi Anda."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("""
            font-size: 13px;
            color: #94A3B8;
            line-height: 1.5;
            background: transparent;
        """)
        card_layout.addWidget(desc_label)

        # Premium Benefits List
        benefits_frame = QFrame()
        benefits_frame.setStyleSheet("background: transparent; border: none;")
        benefits_layout = QVBoxLayout(benefits_frame)
        benefits_layout.setSpacing(8)
        benefits_layout.setContentsMargins(20, 0, 20, 0)

        benefits = [
            "✔  Multi Router Monitoring & Management",
            "✔  Batch Voucher Generator (Cetak PDF)",
            "✔  Kesehatan Jaringan & Estimasi Kemacetan",
            "✔  Otomatisasi Script & Scheduler MikroTik",
            "✔  Pembaruan Gratis Selama 5 Tahun & Local-First"
        ]

        for b in benefits:
            blabel = QLabel(b)
            blabel.setStyleSheet("font-size: 12px; color: #38BDF8; font-weight: 600;")
            benefits_layout.addWidget(blabel)

        card_layout.addWidget(benefits_frame)

        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("border: 1px solid #1E293B; background: transparent;")
        card_layout.addWidget(divider)

        # Activation Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        form_title = QLabel("Aktivasi Lisensi Lokal (Offline-Friendly)")
        form_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #E2E8F0; background: transparent;")
        form_layout.addWidget(form_title)

        # Owner Name Input
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Nama Pemilik (Contoh: Budi Jaringan)")
        self.owner_input.setStyleSheet("""
            QLineEdit {
                background-color: #07090E;
                border: 1px solid #1F273E;
                border-radius: 8px;
                padding: 10px 14px;
                color: #F8FAFC;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #06B6D4;
            }
        """)
        form_layout.addWidget(self.owner_input)

        # License Key Input
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Masukkan Lisensi Key Pro Anda")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: #07090E;
                border: 1px solid #1F273E;
                border-radius: 8px;
                padding: 10px 14px;
                color: #F8FAFC;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #06B6D4;
            }
        """)
        form_layout.addWidget(self.key_input)

        # Error notification label
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("font-size: 12px; color: #EF4444; background: transparent; font-weight: 600;")
        form_layout.addWidget(self.error_label)

        # Activate Button
        self.activate_btn = QPushButton("Aktifkan Lisensi Premium")
        self.activate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.activate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0284C7);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                padding: 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0EA5E9);
            }
            QPushButton:pressed {
                background: #0369A1;
            }
        """)
        self.activate_btn.clicked.connect(self._on_activate)
        form_layout.addWidget(self.activate_btn)

        card_layout.addLayout(form_layout)
        main_layout.addWidget(card)

    def _on_activate(self) -> None:
        owner = self.owner_input.text().strip()
        key = self.key_input.text().strip()

        if not owner:
            self.error_label.setText("⚠ Harap masukkan nama pemilik lisensi.")
            return

        if not key:
            self.error_label.setText("⚠ Harap masukkan lisensi key.")
            return

        # Simple verification simulation for commercial feel:
        # Key must be at least 8 characters
        if len(key) < 8:
            self.error_label.setText("⚠ Format Lisensi Key salah atau tidak valid.")
            return

        self.error_label.setText("")
        self.activate_btn.setEnabled(False)
        self.activate_btn.setText("Memverifikasi Kunci Mesin...")

        # Perform local activation
        success = LicensingManager.activate_license(raw_key=key, owner_name=owner)

        if success:
            logger.info("License verified in UI overlay, notifying app_state.")
            if self.app_state:
                # Recalculate status and emit global licensing_changed signal
                self.app_state.check_license_status()
            
            self.activation_success.emit()
        else:
            self.activate_btn.setEnabled(True)
            self.activate_btn.setText("Aktifkan Lisensi Premium")
            self.error_label.setText("⚠ Gagal mengaktifkan lisensi pada mesin ini.")
