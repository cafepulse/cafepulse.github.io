"""
CafePulse — PPP Tunnels & Secrets Page (Phase 14)
Manages Secret credentials, active PPPoE/tunnels sessions, and profile limits.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


class NetPpp(QWidget):
    """
    PPP Point-to-Point tunneling panel.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_ppp_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Secrets card
        secrets_card = QFrame()
        secrets_card.setObjectName("DashCard")
        sec_layout = QVBoxLayout(secrets_card)
        sec_layout.setContentsMargins(14, 12, 14, 12)
        sec_layout.setSpacing(10)

        sec_title = QLabel("PPP SECRET USER ACCOUNTS")
        sec_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        sec_layout.addWidget(sec_title)

        self.secrets_table = QTableWidget(0, 4)
        self.secrets_table.verticalHeader().setDefaultSectionSize(36)
        self.secrets_table.setHorizontalHeaderLabels(["Username", "Password (Encr)", "Service Profile", "Local / Remote IP"])
        self.secrets_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.secrets_table.setStyleSheet(
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
        sec_layout.addWidget(self.secrets_table)
        layout.addWidget(secrets_card)

        # Active connections card
        conn_card = QFrame()
        conn_card.setObjectName("DashCard")
        conn_layout = QVBoxLayout(conn_card)
        conn_layout.setContentsMargins(14, 12, 14, 12)
        conn_layout.setSpacing(10)

        conn_title = QLabel("ACTIVE PPP CLIENT SESSIONS (LIVE CONNECTIONS)")
        conn_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        conn_layout.addWidget(conn_title)

        self.conn_table = QTableWidget(0, 5)
        self.conn_table.verticalHeader().setDefaultSectionSize(36)
        self.conn_table.setHorizontalHeaderLabels(["User / Client", "Service Protocol", "Caller ID (MAC/IP)", "Allocated IP", "Uptime"])
        self.conn_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.conn_table.setStyleSheet(
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
        conn_layout.addWidget(self.conn_table)
        layout.addWidget(conn_card)

        layout.addStretch()

    def load_ppp_data(self) -> None:
        # Load Secrets
        self.secrets_table.setRowCount(2)
        self.secrets_table.setItem(0, 0, QTableWidgetItem("pppoe_budi"))
        self.secrets_table.setItem(0, 1, QTableWidgetItem("••••••••"))
        self.secrets_table.setItem(0, 2, QTableWidgetItem("pppoe"))
        self.secrets_table.setItem(0, 3, QTableWidgetItem("10.10.10.1 / 10.10.10.24"))

        self.secrets_table.setItem(1, 0, QTableWidgetItem("vpn_office"))
        self.secrets_table.setItem(1, 1, QTableWidgetItem("••••••••"))
        self.secrets_table.setItem(1, 2, QTableWidgetItem("l2tp"))
        self.secrets_table.setItem(1, 3, QTableWidgetItem("172.16.0.1 / 172.16.0.50"))

        # Load Active
        self.conn_table.setRowCount(1)
        self.conn_table.setItem(0, 0, QTableWidgetItem("pppoe_budi"))
        self.conn_table.setItem(0, 1, QTableWidgetItem("pppoe"))
        self.conn_table.setItem(0, 2, QTableWidgetItem("00:1E:A6:4F:92:B8"))
        self.conn_table.setItem(0, 3, QTableWidgetItem("10.10.10.24"))
        self.conn_table.setItem(0, 4, QTableWidgetItem("2h 14m 5s"))
