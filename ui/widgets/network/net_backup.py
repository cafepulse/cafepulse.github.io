"""
CafePulse — Router Backup & Restore Page (Phase 17)
Enables binary backups generation, plain-text RSC script exports, and restore wizards.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class NetBackup(QWidget):
    """
    Backup & Restore Configuration panel.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_backups()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Split: Backups List (Left) + RSC Export (Right)
        body = QHBoxLayout()
        body.setSpacing(16)

        # Backups List (Left)
        list_card = QFrame()
        list_card.setObjectName("DashCard")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(14, 12, 14, 12)
        list_layout.setSpacing(10)

        list_title = QLabel("DAFTAR FILE BACKUP BINER (.BACKUP)")
        list_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        list_layout.addWidget(list_title)

        self.table = QTableWidget(0, 3)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setHorizontalHeaderLabels(["Filename", "Size (Bytes)", "Created Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        list_layout.addWidget(self.table)

        # Trigger actions
        act_row = QHBoxLayout()
        self.create_btn = QPushButton("Buat Backup Biner  💾")
        self.create_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.create_btn.clicked.connect(self._on_create_backup)
        act_row.addWidget(self.create_btn)
        
        self.restore_btn = QPushButton("Restore Terpilih  ⚡")
        self.restore_btn.setStyleSheet(
            "QPushButton { background-color: #A78BFA; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #8B5CF6; }"
        )
        self.restore_btn.clicked.connect(self._on_restore_clicked)
        act_row.addWidget(self.restore_btn)
        list_layout.addLayout(act_row)

        body.addWidget(list_card)

        # Plain RSC script block (Right)
        rsc_card = QFrame()
        rsc_card.setObjectName("DashCard")
        rsc_card.setFixedWidth(360)
        rsc_layout = QVBoxLayout(rsc_card)
        rsc_layout.setContentsMargins(14, 12, 14, 12)
        rsc_layout.setSpacing(10)

        rsc_title = QLabel("EKSPOR SKRIP TEKS MENTAH (.RSC)")
        rsc_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        rsc_layout.addWidget(rsc_title)

        self.rsc_viewer = QTextEdit()
        self.rsc_viewer.setReadOnly(True)
        self.rsc_viewer.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; color: #E2E8F0; font-family: monospace; font-size: 10px;"
        )
        self.rsc_viewer.setText(
            "# jun/01/2026 21:00:55 by CafePulse\n"
            "/ip address\n"
            "add address=192.168.88.1/24 interface=bridge\n"
            "/ip dns\n"
            "set servers=8.8.8.8,1.1.1.1\n"
            "/ip firewall filter\n"
            "add action=fasttrack-connection chain=forward"
        )
        rsc_layout.addWidget(self.rsc_viewer)

        self.export_btn = QPushButton("Salin Ekspor RSC  📋")
        self.export_btn.setStyleSheet(
            "QPushButton { background-color: #1E293B; color: #E2E8F0; padding: 8px; font-weight: 600; border-radius: 6px; border: 1px solid #334155; }"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.export_btn.clicked.connect(self._on_copy_rsc)
        rsc_layout.addWidget(self.export_btn)
        body.addWidget(rsc_card)

        layout.addLayout(body)

    def load_backups(self) -> None:
        self.table.setRowCount(2)
        
        self.table.setItem(0, 0, QTableWidgetItem("backup_auto_daily.backup"))
        self.table.setItem(0, 1, QTableWidgetItem("148201"))
        self.table.setItem(0, 2, QTableWidgetItem("2026-06-01 02:00:00"))

        self.table.setItem(1, 0, QTableWidgetItem("backup_before_refactor.backup"))
        self.table.setItem(1, 1, QTableWidgetItem("149112"))
        self.table.setItem(1, 2, QTableWidgetItem("2026-06-01 20:45:00"))

    def _on_create_backup(self) -> None:
        main_win = self.window()
        if hasattr(main_win, "_close_app"):
            main_win.is_backup_running = True
            QMessageBox.information(
                self, "Backup Simulasi Aktif", 
                "Simulasi Proses Backup latar belakang berhasil diaktifkan!\n\n"
                "Jika Anda menutup aplikasi sekarang, sistem akan mendeteksi proses ini dan memicu dialog LEVEL 3 (Background Task)."
            )
        else:
            QMessageBox.information(self, "Backup Sukses", "Berhasil membuat file backup biner baru pada flash penyimpanan MikroTik!")

    def _on_restore_clicked(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Backup", "Silakan pilih salah satu file backup biner pada tabel.")
            return

        filename = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self, "Konfirmasi Restore",
            f"Apakah Anda yakin ingin memulihkan (Restore) konfigurasi router dari file '{filename}'?\n\n"
            "Peringatan: Perangkat router MikroTik Anda akan restart secara otomatis setelah restore berhasil.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            main_win = self.window()
            if hasattr(main_win, "_close_app"):
                main_win.is_restore_running = True
                QMessageBox.information(
                    self, "Restore Kritis Simulasi Aktif", 
                    "Simulasi Operasi Kritis (Restore Router) diaktifkan!\n\n"
                    "Menutup aplikasi saat operasi kritis berjalan sangat berbahaya. "
                    "Jika Anda menutup aplikasi sekarang, sistem akan memicu dialog LEVEL 4 (Critical Operation)."
                )
            else:
                QMessageBox.information(self, "Restore Berhasil", "Mengirim instruksi restore. Router sedang melakukan reboot...")

    def _on_copy_rsc(self) -> None:
        self.rsc_viewer.selectAll()
        self.rsc_viewer.copy()
        QMessageBox.information(self, "Salin RSC", "Konfigurasi skrip teks RSC berhasil disalin ke clipboard Anda!")
