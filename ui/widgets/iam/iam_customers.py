"""
CafePulse — IAM Customers Sub-View
Lightweight, no-friction Customer Ledger mapping customer profiles to active access tokens.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QMessageBox, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSlot

class IamCustomers(QWidget):
    """
    Customer Ledger profile panel.
    """
    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_customers()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Split: Form (Left) + Grid Lists (Right)
        body = QHBoxLayout()
        body.setSpacing(16)

        # ── Left: Add Customer Form ──────────────────────────────────────────
        form_card = QFrame()
        form_card.setObjectName("DashCard")
        form_card.setFixedWidth(340)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 14, 16, 14)
        form_layout.setSpacing(12)

        form_title = QLabel("DAFTAR PELANGGAN BARU")
        form_title.setObjectName("DashCardTitle")
        form_layout.addWidget(form_title)

        inputs = QFormLayout()
        inputs.setSpacing(8)

        self.cust_name = QLineEdit()
        self.cust_name.setPlaceholderText("Nama lengkap pelanggan")
        self.cust_name.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Nama Pelanggan:", self.cust_name)

        self.cust_phone = QLineEdit()
        self.cust_phone.setPlaceholderText("Nomor telepon / WA")
        self.cust_phone.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("No. Telepon (WA):", self.cust_phone)

        self.cust_notes = QLineEdit()
        self.cust_notes.setPlaceholderText("Catatan (opsional)")
        self.cust_notes.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Catatan / Alamat:", self.cust_notes)

        self.cust_token = QLineEdit()
        self.cust_token.setPlaceholderText("Tempel token voucher aktif")
        self.cust_token.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Tautkan Token:", self.cust_token)

        form_layout.addLayout(inputs)

        # Submit
        self.submit_btn = QPushButton("Tambah Pelanggan  👤")
        self.submit_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self._on_submit_clicked)
        form_layout.addWidget(self.submit_btn)

        body.addWidget(form_card)

        # ── Right: Customers Card Grid List ──────────────────────────────────
        list_card = QFrame()
        list_card.setObjectName("DashCard")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(16, 14, 16, 14)
        list_layout.setSpacing(10)

        list_title = QLabel("BUKU PELANGGAN & STATUS AKTIF")
        list_title.setObjectName("DashCardTitle")
        list_layout.addWidget(list_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.grid_container = QWidget()
        self.grid_layout = QVBoxLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(10)
        self.grid_layout.addStretch()

        scroll.setWidget(self.grid_container)
        list_layout.addWidget(scroll)

        body.addWidget(list_card)
        layout.addLayout(body)

    def load_customers(self) -> None:
        # Clean current grid items
        while self.grid_layout.count() > 1:
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            customers = self._db.get_all_customers()
            for c in customers:
                card = QFrame()
                card.setStyleSheet("background-color: #07090D; border: 1px solid #1E293B; border-radius: 8px;")
                card_layout = QHBoxLayout(card)
                card_layout.setContentsMargins(14, 12, 14, 12)

                # Icon
                avatar = QLabel("👤")
                avatar.setStyleSheet("font-size: 22px;")
                card_layout.addWidget(avatar)

                # Left Info col
                info = QVBoxLayout()
                name = QLabel(f"<b>{c['name']}</b>")
                name.setStyleSheet("color: #E2E8F0; font-size: 13px;")
                info.addWidget(name)

                details = QLabel(f"Telp: {c['phone'] or '—'} | Catatan: {c['notes'] or '—'}")
                details.setStyleSheet("color: #64748B; font-size: 11px;")
                info.addWidget(details)
                card_layout.addLayout(info)

                card_layout.addStretch()

                # Right active token mapping display
                token_val = c["active_token"]
                token_lbl = QLabel(f"Token: {token_val}" if token_val else "Tanpa Token")
                token_lbl.setStyleSheet(
                    "background-color: #1E293B; color: #38BDF8; font-size: 10px; font-weight: 700; "
                    "padding: 4px 8px; border-radius: 4px; border: 1px solid #334155;" if token_val
                    else "background-color: #161B27; color: #475569; font-size: 10px; padding: 4px 8px; border-radius: 4px;"
                )
                card_layout.addWidget(token_lbl)

                # Delete btn
                del_btn = QPushButton("🗑️")
                del_btn.setFixedSize(28, 28)
                del_btn.setStyleSheet(
                    "QPushButton { background-color: #7F1D1D; color: white; border: none; border-radius: 4px; }"
                    "QPushButton:hover { background-color: #991B1B; }"
                )
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.clicked.connect(lambda checked, cid=c["id"]: self._on_delete_clicked(cid))
                card_layout.addWidget(del_btn)

                # Insert at top (above stretch)
                self.grid_layout.insertWidget(self.grid_layout.count() - 1, card)
        except Exception as e:
            logger.error("Failed to load customers: %s", e)

    def _on_submit_clicked(self) -> None:
        name = self.cust_name.text().strip()
        phone = self.cust_phone.text().strip()
        notes = self.cust_notes.text().strip()
        token = self.cust_token.text().strip()

        if not name:
            QMessageBox.warning(self, "Validasi Gagal", "Nama pelanggan wajib diisi.")
            return

        try:
            self._db.add_customer(name, phone, notes, token)
            self.cust_name.clear()
            self.cust_phone.clear()
            self.cust_notes.clear()
            self.cust_token.clear()
            self.load_customers()
        except Exception as e:
            logger.error("Failed to add customer: %s", e)
            QMessageBox.critical(self, "Gagal Menambahkan", f"Terjadi kesalahan:\n{e}")

    def _on_delete_clicked(self, cid: int) -> None:
        confirm = QMessageBox.question(
            self, "Hapus Pelanggan", "Apakah Anda yakin ingin menghapus data pelanggan ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self._db.delete_customer(cid)
                self.load_customers()
            except Exception as e:
                logger.error("Failed to delete customer: %s", e)
