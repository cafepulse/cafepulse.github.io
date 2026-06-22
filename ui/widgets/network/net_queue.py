"""
CafePulse — Queue & Bandwidth QoS Page (Phase 16)
Manages Simple Queues limits, visualizes Queue Trees, and handles bursted speeds.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt


class NetQueue(QWidget):
    """
    QoS Bandwidth Allocator (Simple Queue & Queue Tree).
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._is_advanced_mode = False
        self._build_ui()
        self.load_queues()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Simple queues card
        sq_card = QFrame()
        sq_card.setObjectName("DashCard")
        sq_layout = QVBoxLayout(sq_card)
        sq_layout.setContentsMargins(14, 12, 14, 12)
        sq_layout.setSpacing(10)

        sq_title = QLabel("TABEL SIMPLE QUEUE (BANDWIDTH LIMITS)")
        sq_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        sq_layout.addWidget(sq_title)

        self.table = QTableWidget(0, 4)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setHorizontalHeaderLabels(["Name / Target", "Max Limit Download", "Max Limit Upload", "Queued Bytes"])
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
        sq_layout.addWidget(self.table)
        layout.addWidget(sq_card)

        # Queue tree card
        tree_card = QFrame()
        tree_card.setObjectName("DashCard")
        tree_card.setStyleSheet("background-color: #111625; border-left: 3px solid #A78BFA;")
        tree_layout = QVBoxLayout(tree_card)
        tree_layout.setContentsMargins(14, 12, 14, 12)
        tree_layout.setSpacing(8)

        tree_title = QLabel("HIERARKI QUEUE TREE (QoS PRIORITISATION)")
        tree_title.setStyleSheet("color: #A78BFA; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        tree_layout.addWidget(tree_title)

        self.tree_lbl = QLabel(
            "<b>[ Global Bridge Parent ]</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;├──► <b>qos_traffic_priority_1 (VoIP / DNS)</b> (Limit: 2M | Priority: 1)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;├──► <b>qos_traffic_priority_2 (Web Browsing)</b> (Limit: 20M | Priority: 3)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;└──► <b>qos_traffic_priority_8 (P2P / Downloads)</b> (Limit: 5M | Priority: 8)"
        )
        self.tree_lbl.setStyleSheet("color: #E2E8F0; font-size: 11px; line-height: 1.5; font-family: Consolas, monospace;")
        tree_layout.addWidget(self.tree_lbl)
        layout.addWidget(tree_card)

        # Action button
        act_row = QHBoxLayout()
        act_row.addStretch()
        self.add_btn = QPushButton("Tambah Aturan Bandwidth  ➕")
        self.add_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.add_btn.clicked.connect(self._on_add_clicked)
        act_row.addWidget(self.add_btn)
        layout.addLayout(act_row)

        layout.addStretch()

    def load_queues(self) -> None:
        self.table.setRowCount(2)
        
        self.table.setItem(0, 0, QTableWidgetItem("queue_budi (192.168.88.24)"))
        self.table.setItem(0, 1, QTableWidgetItem("10 Mbps"))
        self.table.setItem(0, 2, QTableWidgetItem("5 Mbps"))
        self.table.setItem(0, 3, QTableWidgetItem("24.8 MB"))

        self.table.setItem(1, 0, QTableWidgetItem("hotspot_users_default"))
        self.table.setItem(1, 1, QTableWidgetItem("5 Mbps"))
        self.table.setItem(1, 2, QTableWidgetItem("2 Mbps"))
        self.table.setItem(1, 3, QTableWidgetItem("142.1 MB"))

    def set_advanced_mode(self, active: bool) -> None:
        self._is_advanced_mode = active

    def _on_add_clicked(self) -> None:
        QMessageBox.information(
            self, "Tambah Queue",
            "Simulator Form Tambah Simple Queue Aktif!\n\n"
            "CafePulse dapat membuat aturan limitasi bandwidth dinamis berdasarkan IP Tunggal, Interface, atau rentang subnet."
        )
