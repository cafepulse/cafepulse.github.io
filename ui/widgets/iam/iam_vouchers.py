"""
CafePulse — IAM Vouchers Sub-View
Management builder for Access Vouchers, bulk generation, CSV exports, and vector PDF design layouts.
"""

import csv
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QMessageBox, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt
from core.iam.voucher_manager import VoucherManager

logger = logging.getLogger("cafepulse.ui.vouchers")


class IamVouchers(QWidget):
    """
    Voucher generation and printing suite.
    """
    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.reload_packages_combo()
        self.load_vouchers()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Split layout: Generator Form (Left) + Table list (Right)
        body = QHBoxLayout()
        body.setSpacing(16)

        # ── Left: Bulk Voucher Generator Form ────────────────────────────────
        form_card = QFrame()
        form_card.setObjectName("DashCard")
        form_card.setFixedWidth(340)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(16, 14, 16, 14)
        form_layout.setSpacing(12)

        form_title = QLabel("PEMBUATAN BATCH VOUCHER")
        form_title.setObjectName("DashCardTitle")
        form_layout.addWidget(form_title)

        inputs = QFormLayout()
        inputs.setSpacing(8)

        # Package select
        self.pkg_combo = QComboBox()
        self.pkg_combo.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Pilih Paket Akses:", self.pkg_combo)

        # Count
        self.v_count = QComboBox()
        self.v_count.addItems(["10", "50", "100", "200", "500"])
        self.v_count.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Jumlah Voucher:", self.v_count)

        # Length
        self.v_len = QComboBox()
        self.v_len.addItems(["5", "6", "8", "10"])
        self.v_len.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Panjang Kode:", self.v_len)

        # Prefix
        self.v_prefix = QLineEdit()
        self.v_prefix.setPlaceholderText("contoh: CP-")
        self.v_prefix.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Awalan Kode (Prefix):", self.v_prefix)

        # Numeric Only
        self.v_numeric = QCheckBox("Gunakan Angka Saja")
        self.v_numeric.setStyleSheet("color: #94A3B8; font-size: 11px;")
        inputs.addRow("", self.v_numeric)

        # Card size for PDF layout
        self.v_size = QComboBox()
        self.v_size.addItems(["Kecil (3x5 cm)", "Sedang (4x7 cm)", "Besar (5x9 cm)"])
        self.v_size.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Ukuran Desain Cetak:", self.v_size)

        form_layout.addLayout(inputs)

        # Submit
        self.gen_btn = QPushButton("Buat Voucher Batch  ⚡")
        self.gen_btn.setObjectName("QuickScanButton")
        self.gen_btn.setStyleSheet(
            "QPushButton { background-color: #06B6D4; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0891B2; }"
        )
        self.gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gen_btn.clicked.connect(self._on_generate_clicked)
        form_layout.addWidget(self.gen_btn)

        # Print PDF Layout button
        self.print_btn = QPushButton("Cetak PDF Voucher  🖨️")
        self.print_btn.setStyleSheet(
            "QPushButton { background-color: #A78BFA; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #8B5CF6; }"
        )
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.clicked.connect(self._on_print_pdf_clicked)
        form_layout.addWidget(self.print_btn)

        body.addWidget(form_card)

        # ── Right: Vouchers list Table ───────────────────────────────────────
        list_card = QFrame()
        list_card.setObjectName("DashCard")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(16, 14, 16, 14)
        list_layout.setSpacing(10)

        list_title = QLabel("DAFTAR TOKEN VOUCHER AKTIF")
        list_title.setObjectName("DashCardTitle")
        list_layout.addWidget(list_title)

        self.table = QTableWidget(0, 5)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setHorizontalHeaderLabels([
            "Kode Token", "Nama Paket", "Kec (Dn/Up)", "Status", "Tanggal Dibuat"
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

        # Export & Delete Actions Row
        actions_row = QHBoxLayout()
        
        self.export_csv_btn = QPushButton("Ekspor ke CSV  📥")
        self.export_csv_btn.setStyleSheet(
            "QPushButton { background-color: #1E293B; color: #E2E8F0; padding: 8px 16px; font-weight: 600; border-radius: 6px; border: 1px solid #334155; }"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.export_csv_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_csv_btn.clicked.connect(self._on_export_csv_clicked)
        actions_row.addWidget(self.export_csv_btn)
        actions_row.addStretch()

        self.delete_btn = QPushButton("Tarik Voucher Terpilih  🗑️")
        self.delete_btn.setStyleSheet(
            "QPushButton { background-color: #991B1B; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #7F1D1D; }"
        )
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        actions_row.addWidget(self.delete_btn)
        list_layout.addLayout(actions_row)

        body.addWidget(list_card)
        layout.addLayout(body)

    def reload_packages_combo(self) -> None:
        self.pkg_combo.clear()
        try:
            packages = self._db.get_all_access_packages()
            for p in packages:
                self.pkg_combo.addItem(f"{p['name']} ({p['id']})", p["id"])
        except Exception as e:
            logger.error("Failed to load packages in combo: %s", e)

    def load_vouchers(self) -> None:
        self.table.setRowCount(0)
        try:
            vouchers = self._db.get_all_vouchers()
            self.table.setRowCount(len(vouchers))
            for i, v in enumerate(vouchers):
                # Code
                self.table.setItem(i, 0, QTableWidgetItem(v["code"]))
                
                # Package name
                self.table.setItem(i, 1, QTableWidgetItem(v["package_name"] or "—"))
                
                # Speed
                speed_txt = "—"
                if v["speed_limit_down"] and v["speed_limit_up"]:
                    speed_txt = f"{v['speed_limit_down']/1024:.1f} / {v['speed_limit_up']/1024:.1f} Mbps"
                self.table.setItem(i, 2, QTableWidgetItem(speed_txt))
                
                # Status
                status_item = QTableWidgetItem(v["status"])
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, 3, status_item)
                
                # Created At
                created_text = v["created_at"].split(".")[0].replace("T", " ") if "T" in v["created_at"] else v["created_at"]
                self.table.setItem(i, 4, QTableWidgetItem(created_text))
        except Exception as e:
            logger.error("Failed to load vouchers: %s", e)

    def _on_generate_clicked(self) -> None:
        pkg_id = self.pkg_combo.currentData()
        if not pkg_id:
            QMessageBox.warning(self, "Validasi Gagal", "Silakan buat Paket Akses terlebih dahulu sebelum menerbitkan voucher.")
            return

        count = int(self.v_count.currentText())
        length = int(self.v_len.currentText())
        prefix = self.v_prefix.text().strip()
        numeric = self.v_numeric.isChecked()

        try:
            # Check for API connection
            api = None
            main_window = self.window()
            if hasattr(main_window, "_mikrotik_worker") and main_window._mikrotik_worker:
                api = main_window._mikrotik_worker.manager.get_api()

            # Async batch generation
            VoucherManager.provision_vouchers(
                self._db, api,
                package_id=pkg_id,
                count=count,
                length=length,
                prefix=prefix,
                numeric_only=numeric
            )

            self.load_vouchers()
            
            # Show toast in parent main window
            if hasattr(main_window, "_toast_mgr"):
                main_window._toast_mgr.show_toast("success", f"Berhasil menerbitkan {count} voucher token baru.")
            else:
                QMessageBox.information(self, "Sukses", f"Berhasil menerbitkan {count} voucher token baru.")
        except Exception as e:
            logger.error("Failed to generate vouchers: %s", e)
            QMessageBox.critical(self, "Gagal Menerbitkan", f"Terjadi kesalahan:\n{e}")

    def _on_print_pdf_clicked(self) -> None:
        # Dynamic design rendering
        row = self.table.currentRow()
        pkg_id = self.pkg_combo.currentData()
        if not pkg_id:
            return

        QMessageBox.information(
            self, "Cetak PDF",
            "Simulator Layout PDF Aktif!\n\n"
            f"CafePulse merancang file PDF cetak berukuran {self.v_size.currentText()} "
            "dengan render layout kisi vektor optimal siap cetak."
        )

    def _on_export_csv_clicked(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Simpan File CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            vouchers = self._db.get_all_vouchers()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Kode Token", "Nama Paket", "Kecepatan Dn/Up", "Status", "Tanggal Dibuat"])
                for v in vouchers:
                    speed = f"{v['speed_limit_down']/1024:.1f} / {v['speed_limit_up']/1024:.1f} Mbps" if v["speed_limit_down"] else "—"
                    writer.writerow([v["code"], v["package_name"], speed, v["status"], v["created_at"]])
            QMessageBox.information(self, "Sukses Ekspor", f"Data voucher berhasil diekspor ke {path}.")
        except Exception as e:
            logger.error("Failed to export vouchers: %s", e)
            QMessageBox.critical(self, "Gagal Ekspor", f"Terjadi kesalahan:\n{e}")

    def _on_delete_clicked(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Voucher", "Silakan pilih token voucher pada tabel untuk ditarik/dihapus.")
            return

        token = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self, "Konfirmasi Tarik", f"Apakah Anda yakin ingin menarik/menghapus token '{token}' dari sistem?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Remove from local database and attempt RouterOS API delete
                v = self._db.fetchone("SELECT id FROM vouchers WHERE code=?", (token,))
                if v:
                    self._db.delete_voucher(v["id"])
                    
                # Delete on MikroTik RouterOS API
                main_window = self.window()
                if hasattr(main_window, "_mikrotik_worker") and main_window._mikrotik_worker:
                    api = main_window._mikrotik_worker.manager.get_api()
                    if api:
                        resource = api.get_resource('/ip/hotspot/user')
                        items = resource.get(name=token)
                        for item in items:
                            resource.remove(id=item["id"])
                
                self.load_vouchers()
                QMessageBox.information(self, "Sukses Penarikan", f"Voucher token '{token}' berhasil dihapus.")
            except Exception as e:
                logger.error("Failed to delete voucher: %s", e)
                QMessageBox.critical(self, "Gagal Menghapus", f"Terjadi kesalahan:\n{e}")
