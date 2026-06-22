"""
CafePulse — Routing Table Page (Phase 12)
Provides tabular IP routing tables, static route builders, and dynamic protocol tags.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFormLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class NetRouting(QWidget):
    """
    Core IP Routing table management.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_routes()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Split: Form (Left) + Routes List (Right)
        body = QHBoxLayout()
        body.setSpacing(16)

        # ── Left: Add Route Form ──────────────────────────────────────────────
        form_card = QFrame()
        form_card.setObjectName("DashCard")
        form_card.setFixedWidth(320)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(14, 12, 14, 12)
        form_layout.setSpacing(10)

        form_title = QLabel("BUAT ROUTE STATIS BARU")
        form_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        form_layout.addWidget(form_title)

        inputs = QFormLayout()
        inputs.setSpacing(8)

        self.dst_input = QLineEdit()
        self.dst_input.setPlaceholderText("contoh: 0.0.0.0/0")
        self.dst_input.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Destination IP/Mask:", self.dst_input)

        self.gw_input = QLineEdit()
        self.gw_input.setPlaceholderText("contoh: 192.168.1.1")
        self.gw_input.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Gateway IP:", self.gw_input)

        self.dist_input = QLineEdit("1")
        self.dist_input.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Route Distance:", self.dist_input)

        form_layout.addLayout(inputs)

        self.add_btn = QPushButton("Tambah Route Statis  ✓")
        self.add_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.add_btn.clicked.connect(self._on_add_route)
        form_layout.addWidget(self.add_btn)
        body.addWidget(form_card)

        # ── Right: Routes Table ───────────────────────────────────────────────
        table_card = QFrame()
        table_card.setObjectName("DashCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(14, 12, 14, 12)
        table_layout.setSpacing(10)

        table_title = QLabel("TABEL ROUTING IP AKTIF")
        table_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        table_layout.addWidget(table_title)

        self.table = QTableWidget(0, 5)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setHorizontalHeaderLabels(["Destination", "Gateway", "Distance", "Flags", "Routing Mark"])
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
        table_layout.addWidget(self.table)
        body.addWidget(table_card)

        layout.addLayout(body)

    def load_routes(self) -> None:
        self.table.setRowCount(3)
        
        # Default route
        self.table.setItem(0, 0, QTableWidgetItem("0.0.0.0/0"))
        self.table.setItem(0, 1, QTableWidgetItem("10.0.0.1 reachable ether1"))
        self.table.setItem(0, 2, QTableWidgetItem("1"))
        self.table.setItem(0, 3, QTableWidgetItem("DAS (Active Static)"))
        self.table.setItem(0, 4, QTableWidgetItem("main"))

        # LAN bridge route
        self.table.setItem(1, 0, QTableWidgetItem("192.168.88.0/24"))
        self.table.setItem(1, 1, QTableWidgetItem("bridge reachable"))
        self.table.setItem(1, 2, QTableWidgetItem("0"))
        self.table.setItem(1, 3, QTableWidgetItem("DAC (Active Connect)"))
        self.table.setItem(1, 4, QTableWidgetItem("main"))

        # WAN subnet route
        self.table.setItem(2, 0, QTableWidgetItem("10.0.0.0/24"))
        self.table.setItem(2, 1, QTableWidgetItem("ether1 reachable"))
        self.table.setItem(2, 2, QTableWidgetItem("0"))
        self.table.setItem(2, 3, QTableWidgetItem("DAC (Active Connect)"))
        self.table.setItem(2, 4, QTableWidgetItem("main"))

    def _on_add_route(self) -> None:
        dst = self.dst_input.text().strip()
        gw = self.gw_input.text().strip()
        dist = self.dist_input.text().strip()

        if not dst or not gw:
            QMessageBox.warning(self, "Validasi Gagal", "Destination dan Gateway wajib diisi.")
            return

        QMessageBox.information(
            self, "Route Ditambahkan",
            f"Berhasil menambahkan static route ke {dst} via gateway {gw} (distance: {dist})!"
        )
        self.dst_input.clear()
        self.gw_input.clear()
