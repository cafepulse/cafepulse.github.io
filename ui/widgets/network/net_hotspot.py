"""
CafePulse — Hotspot Server Configuration Page (Phase 15)
Focuses strictly on Hotspot servers, user profiles, active sessions, and login pages.
Strictly decoupled from commercial Voucher Management (which lives under IAM in Operations).
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class NetHotspot(QWidget):
    """
    MikroTik Hotspot Server operational configurations.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_hotspot_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Servers and profiles
        row1 = QHBoxLayout()
        row1.setSpacing(14)

        # Servers Card
        srv_card = QFrame()
        srv_card.setObjectName("DashCard")
        srv_layout = QVBoxLayout(srv_card)
        srv_layout.setContentsMargins(14, 12, 14, 12)
        srv_layout.setSpacing(10)

        srv_title = QLabel("HOTSPOT SERVERS LIST")
        srv_title.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        srv_layout.addWidget(srv_title)

        self.srv_table = QTableWidget(0, 3)
        self.srv_table.verticalHeader().setDefaultSectionSize(36)
        self.srv_table.setHorizontalHeaderLabels(["Name", "Interface WAN/LAN", "Address Pool"])
        self.srv_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.srv_table.setStyleSheet(
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
        srv_layout.addWidget(self.srv_table)
        row1.addWidget(srv_card)

        # Profiles Card
        prof_card = QFrame()
        prof_card.setObjectName("DashCard")
        prof_layout = QVBoxLayout(prof_card)
        prof_layout.setContentsMargins(14, 12, 14, 12)
        prof_layout.setSpacing(10)

        prof_title = QLabel("HOTSPOT USER PROFILES LIMITS")
        prof_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        prof_layout.addWidget(prof_title)

        self.prof_table = QTableWidget(0, 3)
        self.prof_table.verticalHeader().setDefaultSectionSize(36)
        self.prof_table.setHorizontalHeaderLabels(["Profile Name", "Rate Limit (Dn/Up)", "Idle Timeout"])
        self.prof_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prof_table.setStyleSheet(
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
        prof_layout.addWidget(self.prof_table)
        row1.addWidget(prof_card)

        layout.addLayout(row1)

        # Active Hotspot Users / Sessions
        sess_card = QFrame()
        sess_card.setObjectName("DashCard")
        sess_layout = QVBoxLayout(sess_card)
        sess_layout.setContentsMargins(14, 12, 14, 12)
        sess_layout.setSpacing(10)

        sess_title = QLabel("LIVE ACTIVE HOTSPOT SESSIONS (READ ONLY)")
        sess_title.setStyleSheet("color: #A78BFA; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        sess_layout.addWidget(sess_title)

        self.sess_table = QTableWidget(0, 4)
        self.sess_table.verticalHeader().setDefaultSectionSize(36)
        self.sess_table.setHorizontalHeaderLabels(["User", "IP / MAC Address", "Uptime", "Bytes In/Out"])
        self.sess_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sess_table.setStyleSheet(
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
        sess_layout.addWidget(self.sess_table)
        layout.addWidget(sess_card)

        # Action layout
        act_row = QHBoxLayout()
        self.html_btn = QPushButton("Kustomisasi Halaman Login (HTML)  🎨")
        self.html_btn.setStyleSheet(
            "QPushButton { background-color: #1E293B; color: #E2E8F0; padding: 8px 16px; font-weight: 600; border-radius: 6px; border: 1px solid #334155; }"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.html_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.html_btn.clicked.connect(self._on_html_clicked)
        act_row.addWidget(self.html_btn)
        act_row.addStretch()
        layout.addLayout(act_row)

    def load_hotspot_data(self) -> None:
        # Load Servers
        self.srv_table.setRowCount(1)
        self.srv_table.setItem(0, 0, QTableWidgetItem("hotspot1"))
        self.srv_table.setItem(0, 1, QTableWidgetItem("bridge_local"))
        self.srv_table.setItem(0, 2, QTableWidgetItem("hs_pool_1"))

        # Load Profiles
        self.prof_table.setRowCount(2)
        self.prof_table.setItem(0, 0, QTableWidgetItem("default"))
        self.prof_table.setItem(0, 1, QTableWidgetItem("Unlimited"))
        self.prof_table.setItem(0, 2, QTableWidgetItem("5m"))

        self.prof_table.setItem(1, 0, QTableWidgetItem("pkt_harian_2g"))
        self.prof_table.setItem(1, 1, QTableWidgetItem("5120k/2048k"))
        self.prof_table.setItem(1, 2, QTableWidgetItem("10m"))

        # Load Sessions
        self.sess_table.setRowCount(1)
        self.sess_table.setItem(0, 0, QTableWidgetItem("cp-8291"))
        self.sess_table.setItem(0, 1, QTableWidgetItem("192.168.88.24 / 00:1E:A6:4F:92:B8"))
        self.sess_table.setItem(0, 2, QTableWidgetItem("1h 14m"))
        self.sess_table.setItem(0, 3, QTableWidgetItem("14.2 MB / 8.5 MB"))

    def _on_html_clicked(self) -> None:
        QMessageBox.information(
            self, "Halaman Login",
            "Simulator Kustomisasi Login Page Aktif!\n\n"
            "CafePulse dapat memodifikasi logo, teks sambutan, dan mengunggah template HTML terkompresi langsung ke direktori flash/hotspot MikroTik Anda."
        )
