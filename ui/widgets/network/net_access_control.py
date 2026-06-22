"""
CafePulse — Access Control Page (Phase 11)
Manages administrative users, group permissions, and active router service ports.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt


class NetAccessControl(QWidget):
    """
    Access Control administration panel.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_users()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ── Upper section: System Users ───────────────────────────────────────
        users_card = QFrame()
        users_card.setObjectName("DashCard")
        users_layout = QVBoxLayout(users_card)
        users_layout.setContentsMargins(14, 12, 14, 12)
        users_layout.setSpacing(10)

        users_title = QLabel("ROUTER ADMINISTRATIVE USERS & GROUPS")
        users_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        users_layout.addWidget(users_title)

        self.users_table = QTableWidget(0, 4)
        self.users_table.verticalHeader().setDefaultSectionSize(36)
        self.users_table.setHorizontalHeaderLabels(["Username", "Group (Role)", "Allowed Address Subnet", "Last Login"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setStyleSheet(
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
        users_layout.addWidget(self.users_table)
        layout.addWidget(users_card)

        # ── Lower section: Service ports & Access Rules ───────────────────────
        ports_card = QFrame()
        ports_card.setObjectName("DashCard")
        ports_layout = QVBoxLayout(ports_card)
        ports_layout.setContentsMargins(14, 12, 14, 12)
        ports_layout.setSpacing(10)

        ports_title = QLabel("ROUTER SERVICE PORTS STATUS")
        ports_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        ports_layout.addWidget(ports_title)

        self.ports_table = QTableWidget(0, 4)
        self.ports_table.verticalHeader().setDefaultSectionSize(36)
        self.ports_table.setHorizontalHeaderLabels(["Service Name", "Port Number", "SSL Enabled", "Status"])
        self.ports_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ports_table.setStyleSheet(
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
        self.ports_table.setFixedHeight(120)
        ports_layout.addWidget(self.ports_table)
        layout.addWidget(ports_card)

        layout.addStretch()

    def load_users(self) -> None:
        # Load administrative users
        self.users_table.setRowCount(2)
        self.users_table.setItem(0, 0, QTableWidgetItem("admin"))
        self.users_table.setItem(0, 1, QTableWidgetItem("full"))
        self.users_table.setItem(0, 2, QTableWidgetItem("192.168.88.0/24"))
        self.users_table.setItem(0, 3, QTableWidgetItem("2026-06-01 20:30:14"))

        self.users_table.setItem(1, 0, QTableWidgetItem("cafepulse_api"))
        self.users_table.setItem(1, 1, QTableWidgetItem("write"))
        self.users_table.setItem(1, 2, QTableWidgetItem("192.168.88.2"))
        self.users_table.setItem(1, 3, QTableWidgetItem("2026-06-01 20:56:04"))

        # Load ports status
        self.ports_table.setRowCount(3)
        self.ports_table.setItem(0, 0, QTableWidgetItem("api"))
        self.ports_table.setItem(0, 1, QTableWidgetItem("8728"))
        self.ports_table.setItem(0, 2, QTableWidgetItem("no"))
        self.ports_table.setItem(0, 3, QTableWidgetItem("enabled"))

        self.ports_table.setItem(1, 0, QTableWidgetItem("api-ssl"))
        self.ports_table.setItem(1, 1, QTableWidgetItem("8729"))
        self.ports_table.setItem(1, 2, QTableWidgetItem("yes"))
        self.ports_table.setItem(1, 3, QTableWidgetItem("disabled"))

        self.ports_table.setItem(2, 0, QTableWidgetItem("winbox"))
        self.ports_table.setItem(2, 1, QTableWidgetItem("8291"))
        self.ports_table.setItem(2, 2, QTableWidgetItem("no"))
        self.ports_table.setItem(2, 3, QTableWidgetItem("enabled"))
