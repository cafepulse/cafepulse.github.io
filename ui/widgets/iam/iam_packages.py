"""
CafePulse — IAM Access Packages Sub-View
Management builder for Access Packages (Duration/Quota/Hybrid) with dynamic SQLite persistence.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from core.iam.package_engine import PackageEngine


class IamPackages(QWidget):
    """
    Access Package builder panel.
    """
    packages_changed = pyqtSignal()

    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_packages()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Split layout: Form (Left) + Table list (Right)
        body = QHBoxLayout()
        body.setSpacing(16)

        # ── Left: Package Builder Form ────────────────────────────────────────
        form_card = QFrame()
        form_card.setObjectName("DashCard")
        form_card.setFixedWidth(340)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 14, 16, 14)
        form_layout.setSpacing(12)

        form_title = QLabel("BUAT PAKET AKSES BARU")
        form_title.setObjectName("DashCardTitle")
        form_layout.addWidget(form_title)

        inputs = QFormLayout()
        inputs.setSpacing(8)

        # ID
        self.pkg_id = QLineEdit()
        self.pkg_id.setPlaceholderText("contoh: pkt_harian_2g")
        self.pkg_id.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("ID Profile (Technical):", self.pkg_id)

        # Name
        self.pkg_name = QLineEdit()
        self.pkg_name.setPlaceholderText("contoh: Paket Harian 2GB")
        self.pkg_name.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Nama Paket (User):", self.pkg_name)

        # Type
        self.pkg_type = QComboBox()
        self.pkg_type.addItems(["DURATION", "QUOTA", "HYBRID"])
        self.pkg_type.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Tipe Batasan:", self.pkg_type)

        # Duration
        self.pkg_dur_val = QLineEdit("24")
        self.pkg_dur_val.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        self.pkg_dur_unit = QComboBox()
        self.pkg_dur_unit.addItems(["Jam (h)", "Hari (d)", "Minggu (w)"])
        self.pkg_dur_unit.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        
        dur_row = QHBoxLayout()
        dur_row.addWidget(self.pkg_dur_val)
        dur_row.addWidget(self.pkg_dur_unit)
        inputs.addRow("Masa Aktif:", dur_row)

        # Quota GB
        self.pkg_quota = QLineEdit("2")
        self.pkg_quota.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Kuota Data (GB):", self.pkg_quota)

        # Speed Down
        self.pkg_speed_dn = QLineEdit("5")
        self.pkg_speed_dn.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Kec. Download (Mbps):", self.pkg_speed_dn)

        # Speed Up
        self.pkg_speed_up = QLineEdit("2")
        self.pkg_speed_up.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Kec. Upload (Mbps):", self.pkg_speed_up)

        # Price
        self.pkg_price = QLineEdit("5000")
        self.pkg_price.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Harga Jual (Rp):", self.pkg_price)

        form_layout.addLayout(inputs)

        # Submit
        self.submit_btn = QPushButton("Simpan Paket  ✓")
        self.submit_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self._on_submit_clicked)
        form_layout.addWidget(self.submit_btn)

        body.addWidget(form_card)

        # ── Right: Packages List Table ────────────────────────────────────────
        list_card = QFrame()
        list_card.setObjectName("DashCard")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(16, 14, 16, 14)
        list_layout.setSpacing(10)

        list_title = QLabel("DAFTAR PAKET AKTIF")
        list_title.setObjectName("DashCardTitle")
        list_layout.addWidget(list_title)

        self.table = QTableWidget(0, 7)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setHorizontalHeaderLabels([
            "ID Profile", "Nama Paket", "Tipe", "Masa Aktif", "Kuota", "Kec (Dn/Up)", "Harga"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        list_layout.addWidget(self.table)

        # Delete Action Row
        del_row = QHBoxLayout()
        del_row.addStretch()
        
        self.delete_btn = QPushButton("Hapus Paket Terpilih  🗑️")
        self.delete_btn.setStyleSheet(
            "QPushButton { background-color: #991B1B; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #7F1D1D; }"
        )
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        del_row.addWidget(self.delete_btn)
        list_layout.addLayout(del_row)

        body.addWidget(list_card)
        layout.addLayout(body)

    def load_packages(self) -> None:
        self.table.setRowCount(0)
        try:
            packages = self._db.get_all_access_packages()
            self.table.setRowCount(len(packages))
            for i, p in enumerate(packages):
                # ID Profile
                self.table.setItem(i, 0, QTableWidgetItem(p["id"]))
                
                # Name
                self.table.setItem(i, 1, QTableWidgetItem(p["name"]))
                
                # Type Badge (Styled)
                t_badge = QTableWidgetItem(p["package_type"])
                t_badge.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, 2, t_badge)
                
                # Duration
                dur_text = "Unlimited"
                if p["duration_seconds"] > 0:
                    dur_hours = p["duration_seconds"] / 3600
                    if dur_hours % 24 == 0:
                        dur_text = f"{int(dur_hours / 24)} Hari"
                    else:
                        dur_text = f"{int(dur_hours)} Jam"
                self.table.setItem(i, 3, QTableWidgetItem(dur_text))
                
                # Quota
                quota_text = "Unlimited"
                if p["quota_bytes"] > 0:
                    quota_gb = p["quota_bytes"] / (1024 * 1024 * 1024)
                    quota_text = f"{quota_gb:.1f} GB"
                self.table.setItem(i, 4, QTableWidgetItem(quota_text))
                
                # Speed
                speed_text = f"{p['speed_limit_down']/1024:.1f} / {p['speed_limit_up']/1024:.1f} Mbps"
                self.table.setItem(i, 5, QTableWidgetItem(speed_text))
                
                # Price
                price_text = f"Rp {p['price']:,.0f}"
                self.table.setItem(i, 6, QTableWidgetItem(price_text))
        except Exception as e:
            logger.error("Failed to load packages: %s", e)

    def _on_submit_clicked(self) -> None:
        pkg_id = self.pkg_id.text().strip()
        name = self.pkg_name.text().strip()
        pkg_type = self.pkg_type.currentText()
        
        if not pkg_id or not name:
            QMessageBox.warning(self, "Validasi Gagal", "ID Profile dan Nama Paket wajib diisi.")
            return

        try:
            # Parse Duration
            duration_val = float(self.pkg_dur_val.text().strip() or 0)
            duration_unit_map = {
                "Jam (h)": "h",
                "Hari (d)": "d",
                "Minggu (w)": "w"
            }
            unit = duration_unit_map.get(self.pkg_dur_unit.currentText(), "h")
            duration_sec = PackageEngine.duration_to_seconds(int(duration_val), unit) if pkg_type in ("DURATION", "HYBRID") else 0

            # Parse Quota GB
            quota_val = float(self.pkg_quota.text().strip() or 0)
            quota_bytes = PackageEngine.quota_to_bytes(quota_val) if pkg_type in ("QUOTA", "HYBRID") else 0

            # Parse Speeds
            speed_dn = PackageEngine.speed_to_kbps(float(self.pkg_speed_dn.text().strip() or 0))
            speed_up = PackageEngine.speed_to_kbps(float(self.pkg_speed_up.text().strip() or 0))

            # Parse Price
            price = float(self.pkg_price.text().strip() or 0)

            # Insert into database
            self._db.add_access_package(pkg_id, name, pkg_type, duration_sec, quota_bytes, speed_dn, speed_up, price)
            
            # Clear Inputs
            self.pkg_id.clear()
            self.pkg_name.clear()
            
            self.load_packages()
            self.packages_changed.emit()
            
            QMessageBox.information(self, "Sukses", f"Paket '{name}' berhasil disimpan.")
        except Exception as e:
            logger.error("Failed to save package: %s", e)
            QMessageBox.critical(self, "Gagal Menyimpan", f"Terjadi kesalahan:\n{e}")

    def _on_delete_clicked(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Paket", "Silakan pilih baris paket yang ingin dihapus.")
            return

        pkg_id = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self, "Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus paket ID '{pkg_id}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self._db.delete_access_package(pkg_id)
                self.load_packages()
                self.packages_changed.emit()
            except Exception as e:
                logger.error("Failed to delete package: %s", e)
                QMessageBox.critical(self, "Gagal Menghapus", f"Terjadi kesalahan:\n{e}")
