"""
CafePulse — Network Connections Page (Phase 5)
Handles router discovery neighbors list, secure saved favorite credentials, and audit logs.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot


class NetConnections(QWidget):
    """
    Connections page managing neighboring router discoveries and secure saved routers.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_connections()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ── Neighbor Router Discovery ─────────────────────────────────────────
        discovery_card = QFrame()
        discovery_card.setObjectName("DashCard")
        discovery_layout = QVBoxLayout(discovery_card)
        discovery_layout.setContentsMargins(14, 12, 14, 12)
        discovery_layout.setSpacing(10)

        disc_title = QLabel("ROUTER NEIGHBOR DISCOVERY (MNDP)")
        disc_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        discovery_layout.addWidget(disc_title)

        self.disc_table = QTableWidget(0, 4)
        self.disc_table.verticalHeader().setDefaultSectionSize(36)
        self.disc_table.setHorizontalHeaderLabels(["Board Model", "IP Address", "MAC Address", "Identity"])
        self.disc_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.disc_table.setStyleSheet(
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
        self.disc_table.setFixedHeight(120)
        discovery_layout.addWidget(self.disc_table)
        layout.addWidget(discovery_card)

        # ── Saved Favorited Routers ───────────────────────────────────────────
        favorites_card = QFrame()
        favorites_card.setObjectName("DashCard")
        favorites_layout = QVBoxLayout(favorites_card)
        favorites_layout.setContentsMargins(14, 12, 14, 12)
        favorites_layout.setSpacing(10)

        fav_title = QLabel("PROFIL ROUTER YANG DISIMPAN (SECURE VAULT)")
        fav_title.setStyleSheet("color: #A78BFA; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        favorites_layout.addWidget(fav_title)

        self.fav_table = QTableWidget(0, 4)
        self.fav_table.verticalHeader().setDefaultSectionSize(36)
        self.fav_table.setHorizontalHeaderLabels(["Nama Profil", "Alamat IP", "Port", "Username"])
        self.fav_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fav_table.setStyleSheet(
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
        favorites_layout.addWidget(self.fav_table)

        # Action button
        action_row = QHBoxLayout()
        action_row.addStretch()
        self.connect_btn = QPushButton("Hubungkan Sekarang  ⚡")
        self.connect_btn.setObjectName("QuickScanButton")
        self.connect_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.connect_btn.clicked.connect(self._on_connect_clicked)
        action_row.addWidget(self.connect_btn)
        favorites_layout.addLayout(action_row)

        layout.addWidget(favorites_card)

        # ── Audit History Logs ────────────────────────────────────────────────
        log_card = QFrame()
        log_card.setObjectName("DashCard")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(14, 12, 14, 12)
        log_layout.setSpacing(6)

        log_title = QLabel("RIWAYAT KONEKSI SISTEM (AUDIT LOGS)")
        log_title.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        log_layout.addWidget(log_title)

        self.log_lbl = QLabel(
            "• Sesi " + ("Demo aktif" if self._app_state and self._app_state.current_mode == "demo" else "Siap") + ".\n"
            "• [Audit] Kredensial router dienkripsi dalam Secure Vault secara lokal.\n"
            "• [API] Hubungan port API standar 8728 siap digunakan."
        )
        self.log_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.6;")
        log_layout.addWidget(self.log_lbl)
        layout.addWidget(log_card)

        layout.addStretch()

    def load_connections(self) -> None:
        # Mock neighbor discovery data
        self.disc_table.setRowCount(1)
        self.disc_table.setItem(0, 0, QTableWidgetItem("hAP ac lite"))
        self.disc_table.setItem(0, 1, QTableWidgetItem("192.168.88.1"))
        self.disc_table.setItem(0, 2, QTableWidgetItem("B8:69:F4:A2:38:11"))
        self.disc_table.setItem(0, 3, QTableWidgetItem("CafePulse_Router"))

        # Load saved routers
        try:
            routers = self._db.get_all_routers()
            self.fav_table.setRowCount(len(routers))
            for i, r in enumerate(routers):
                self.fav_table.setItem(i, 0, QTableWidgetItem(r["name"]))
                self.fav_table.setItem(i, 1, QTableWidgetItem(r["host"]))
                self.fav_table.setItem(i, 2, QTableWidgetItem(str(r["port"])))
                self.fav_table.setItem(i, 3, QTableWidgetItem(r["username"]))
        except Exception:
            pass

    def _on_connect_clicked(self) -> None:
        # Trigger standard connection modal flow in parent window
        row = self.fav_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Router", "Silakan pilih salah satu router favorit pada tabel untuk dihubungkan.")
            return
        
        main_window = self.window()
        if hasattr(main_window, "_start_mikrotik_mode"):
            main_window._start_mikrotik_mode()
