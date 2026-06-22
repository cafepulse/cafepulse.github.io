"""
CafePulse — DNS Management Page (Phase 7)
Configures upstream DNS servers, local static overrides, and DNS cache viewers.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot


class NetDns(QWidget):
    """
    Dedicated DNS configuration dashboard.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._is_advanced_mode = False
        self._build_ui()
        self.load_dns_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # ── Upper section: Upstream config & Flush ────────────────────────────
        top_row = QHBoxLayout()
        top_row.setSpacing(14)

        # Upstream Servers Card
        up_card = QFrame()
        up_card.setObjectName("DashCard")
        up_layout = QVBoxLayout(up_card)
        up_layout.setContentsMargins(14, 12, 14, 12)
        up_layout.setSpacing(8)

        up_lbl = QLabel("DNS UPSTREAM SERVERS")
        up_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        up_layout.addWidget(up_lbl)

        srv_row = QHBoxLayout()
        self.dns_input = QLineEdit("8.8.8.8, 1.1.1.1")
        self.dns_input.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;"
        )
        srv_row.addWidget(self.dns_input)

        self.dns_save_btn = QPushButton("Simpan")
        self.dns_save_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 6px 12px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.dns_save_btn.clicked.connect(self._on_dns_save)
        srv_row.addWidget(self.dns_save_btn)
        up_layout.addLayout(srv_row)
        top_row.addWidget(up_card)

        # Flush DNS Card
        flush_card = QFrame()
        flush_card.setObjectName("DashCard")
        flush_layout = QVBoxLayout(flush_card)
        flush_layout.setContentsMargins(14, 12, 14, 12)

        flush_lbl = QLabel("TINDAKAN CEPAT (QUICK ACTIONS)")
        flush_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        flush_layout.addWidget(flush_lbl)

        self.flush_btn = QPushButton("Flush DNS Cache  ⚡")
        self.flush_btn.setStyleSheet(
            "QPushButton { background-color: #7F1D1D; color: #FECACA; border: 1px solid #991B1B; padding: 8px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #991B1B; color: white; }"
        )
        self.flush_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.flush_btn.clicked.connect(self._on_dns_flush)
        flush_layout.addWidget(self.flush_btn)
        top_row.addWidget(flush_card)

        layout.addLayout(top_row)

        # ── Lower section: Static entries & Cache list ────────────────────────
        body_row = QHBoxLayout()
        body_row.setSpacing(14)

        # Static DNS (Left)
        static_card = QFrame()
        static_card.setObjectName("DashCard")
        static_layout = QVBoxLayout(static_card)
        static_layout.setContentsMargins(14, 12, 14, 12)
        static_layout.setSpacing(10)

        static_title = QLabel("STATIC DNS RESOLUTION OVERRIDES")
        static_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        static_layout.addWidget(static_title)

        self.static_table = QTableWidget(0, 3)
        self.static_table.verticalHeader().setDefaultSectionSize(36)
        self.static_table.setHorizontalHeaderLabels(["Name / Host", "IP Address", "TTL"])
        self.static_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.static_table.setStyleSheet(
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
        static_layout.addWidget(self.static_table)
        body_row.addWidget(static_card)

        # Cache DNS List (Right)
        cache_card = QFrame()
        cache_card.setObjectName("DashCard")
        cache_layout = QVBoxLayout(cache_card)
        cache_layout.setContentsMargins(14, 12, 14, 12)
        cache_layout.setSpacing(10)

        cache_title = QLabel("ACTIVE DNS QUERY CACHE LIST")
        cache_title.setStyleSheet("color: #A78BFA; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        cache_layout.addWidget(cache_title)

        self.cache_table = QTableWidget(0, 3)
        self.cache_table.verticalHeader().setDefaultSectionSize(36)
        self.cache_table.setHorizontalHeaderLabels(["Cached Name", "Type", "IP / Data"])
        self.cache_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cache_table.setStyleSheet(
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
        cache_layout.addWidget(self.cache_table)
        body_row.addWidget(cache_card)

        layout.addLayout(body_row)

    def load_dns_data(self) -> None:
        # Load Static
        self.static_table.setRowCount(2)
        self.static_table.setItem(0, 0, QTableWidgetItem("router.lan"))
        self.static_table.setItem(0, 1, QTableWidgetItem("192.168.88.1"))
        self.static_table.setItem(0, 2, QTableWidgetItem("1d"))

        self.static_table.setItem(1, 0, QTableWidgetItem("cafepulse.local"))
        self.static_table.setItem(1, 1, QTableWidgetItem("192.168.88.1"))
        self.static_table.setItem(1, 2, QTableWidgetItem("10m"))

        # Load Cache
        self.cache_table.setRowCount(3)
        self.cache_table.setItem(0, 0, QTableWidgetItem("google.com"))
        self.cache_table.setItem(0, 1, QTableWidgetItem("A"))
        self.cache_table.setItem(0, 2, QTableWidgetItem("142.251.12.100"))

        self.cache_table.setItem(1, 0, QTableWidgetItem("github.com"))
        self.cache_table.setItem(1, 1, QTableWidgetItem("A"))
        self.cache_table.setItem(1, 2, QTableWidgetItem("140.82.113.3"))

        self.cache_table.setItem(2, 0, QTableWidgetItem("dns.google"))
        self.cache_table.setItem(2, 1, QTableWidgetItem("A"))
        self.cache_table.setItem(2, 2, QTableWidgetItem("8.8.8.8"))

    def set_advanced_mode(self, active: bool) -> None:
        self._is_advanced_mode = active

    def _on_dns_save(self) -> None:
        servers = self.dns_input.text()
        QMessageBox.information(self, "Simpan DNS", f"Upstream DNS Server diset ke: {servers}")

    def _on_dns_flush(self) -> None:
        QMessageBox.information(self, "Flush DNS", "Berhasil membersihkan cache DNS router (Flush DNS Cache)!")
