"""
CafePulse — RouterOS System, Identity, Clock & Scripts Page (Phase 18)
Consolidates NTP, administrative Identity, live logs viewer, scripts list and schedules.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


class NetSystem(QWidget):
    """
    RouterOS utilities management center.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_system_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Split: Clock/NTP (Left) + Scheduler (Right)
        row1 = QHBoxLayout()
        row1.setSpacing(14)

        # NTP details
        ntp_card = QFrame()
        ntp_card.setObjectName("DashCard")
        ntp_layout = QVBoxLayout(ntp_card)
        ntp_layout.setContentsMargins(14, 12, 14, 12)
        ntp_layout.setSpacing(6)

        ntp_title = QLabel("SYSTEM CLOCK & NTP STATUS")
        ntp_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        ntp_layout.addWidget(ntp_title)

        self.clock_val = QLabel("Time: 21:00:55 | Date: jun/01/2026")
        self.clock_val.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 700;")
        ntp_layout.addWidget(self.clock_val)

        self.ntp_val = QLabel("NTP: enabled (Primary: 0.pool.ntp.org)")
        self.ntp_val.setStyleSheet("color: #64748B; font-size: 11px;")
        ntp_layout.addWidget(self.ntp_val)
        row1.addWidget(ntp_card)

        # Scheduler
        sch_card = QFrame()
        sch_card.setObjectName("DashCard")
        sch_layout = QVBoxLayout(sch_card)
        sch_layout.setContentsMargins(14, 12, 14, 12)
        sch_layout.setSpacing(6)

        sch_title = QLabel("ACTIVE ROUTEROS SCHEDULER TASKS")
        sch_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        sch_layout.addWidget(sch_title)

        self.sch_val = QLabel("Tasks: 1 active (Task: backup_script | Run: every 1d)")
        self.sch_val.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 700;")
        sch_layout.addWidget(self.sch_val)

        self.sch_sub = QLabel("Next Run: jun/02/2026 02:00:00")
        self.sch_sub.setStyleSheet("color: #64748B; font-size: 11px;")
        sch_layout.addWidget(self.sch_sub)
        row1.addWidget(sch_card)

        layout.addLayout(row1)

        # Logs Viewer
        logs_card = QFrame()
        logs_card.setObjectName("DashCard")
        logs_layout = QVBoxLayout(logs_card)
        logs_layout.setContentsMargins(14, 12, 14, 12)
        logs_layout.setSpacing(10)

        logs_title = QLabel("LIVE ROUTEROS SYSTEM LOG STREAM")
        logs_title.setStyleSheet("color: #EF4444; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        logs_layout.addWidget(logs_title)

        self.logs_table = QTableWidget(0, 3)
        self.logs_table.verticalHeader().setDefaultSectionSize(36)
        self.logs_table.setHorizontalHeaderLabels(["Timestamp", "Topics / Category", "Log Message"])
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.logs_table.setStyleSheet(
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
        logs_layout.addWidget(self.logs_table)
        layout.addWidget(logs_card)

    def load_system_data(self) -> None:
        self.logs_table.setRowCount(3)
        
        self.logs_table.setItem(0, 0, QTableWidgetItem("20:56:04"))
        self.logs_table.setItem(0, 1, QTableWidgetItem("system, info"))
        self.logs_table.setItem(0, 2, QTableWidgetItem("user admin logged in from 192.168.88.2 via api"))

        self.logs_table.setItem(1, 0, QTableWidgetItem("20:56:15"))
        self.logs_table.setItem(1, 1, QTableWidgetItem("hotspot, info, debug"))
        self.logs_table.setItem(1, 2, QTableWidgetItem("host 00:1E:A6:4F:92:B8 logged in (user: cp-8291)"))

        self.logs_table.setItem(2, 0, QTableWidgetItem("21:00:00"))
        self.logs_table.setItem(2, 1, QTableWidgetItem("script, info"))
        self.logs_table.setItem(2, 2, QTableWidgetItem("autobackup: database backup successful."))
