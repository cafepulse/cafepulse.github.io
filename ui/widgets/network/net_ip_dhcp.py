"""
CafePulse — IP & DHCP Management Page (Phase 6)
Unified multi-tab widget mapping IP addresses, DHCP servers, clients, and lease reservations.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot


class NetIpDhcp(QWidget):
    """
    Unified IP Address & DHCP Server management center.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._is_advanced_mode = False
        self._build_ui()
        self.load_ip_dhcp_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Master sub-tab bar
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #1E293B; background: transparent; border-radius: 8px; }"
            "QTabBar::tab { background: #0F131F; color: #64748B; padding: 8px 16px; font-weight: 600; border: 1px solid #1E293B; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px; }"
            "QTabBar::tab:selected { background: #1E293B; color: #06B6D4; border-bottom: 2px solid #06B6D4; }"
        )
        layout.addWidget(self.tabs)

        # ── Tab 1: IP Addresses ───────────────────────────────────────────────
        self.ip_tab = QWidget()
        ip_layout = QVBoxLayout(self.ip_tab)
        ip_layout.setContentsMargins(12, 12, 12, 12)
        ip_layout.setSpacing(10)

        ip_hdr = QHBoxLayout()
        ip_lbl = QLabel("Konfigurasi Alamat IP Router (IP Address)")
        ip_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        ip_hdr.addWidget(ip_lbl)
        ip_hdr.addStretch()

        self.ip_add_btn = QPushButton("➕  Tambah Alamat IP")
        self.ip_add_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 6px 12px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.ip_add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ip_add_btn.clicked.connect(self._on_ip_add_clicked)
        ip_hdr.addWidget(self.ip_add_btn)
        ip_layout.addLayout(ip_hdr)

        self.ip_table = QTableWidget(0, 5)
        self.ip_table.verticalHeader().setDefaultSectionSize(36)
        self.ip_table.setHorizontalHeaderLabels(["IP Address", "Interface", "Network", "Dynamic", "Disabled"])
        self.ip_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ip_table.setStyleSheet(
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
        ip_layout.addWidget(self.ip_table)
        self.tabs.addTab(self.ip_tab, "IP Address")

        # ── Tab 2: DHCP Server ────────────────────────────────────────────────
        self.dhcp_tab = QWidget()
        dhcp_layout = QVBoxLayout(self.dhcp_tab)
        dhcp_layout.setContentsMargins(12, 12, 12, 12)
        
        self.dhcp_table = QTableWidget(0, 4)
        self.dhcp_table.verticalHeader().setDefaultSectionSize(36)
        self.dhcp_table.setHorizontalHeaderLabels(["Nama Server", "Interface", "Address Pool", "Lease Time"])
        self.dhcp_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.dhcp_table.setStyleSheet(
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
        dhcp_layout.addWidget(self.dhcp_table)
        self.tabs.addTab(self.dhcp_tab, "DHCP Server")

        # ── Tab 3: DHCP Client ────────────────────────────────────────────────
        self.client_tab = QWidget()
        client_layout = QVBoxLayout(self.client_tab)
        client_layout.setContentsMargins(12, 12, 12, 12)

        self.client_table = QTableWidget(0, 4)
        self.client_table.verticalHeader().setDefaultSectionSize(36)
        self.client_table.setHorizontalHeaderLabels(["Interface WAN", "Status", "Alamat IP Didapat", "Default Route"])
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.client_table.setStyleSheet(
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
        client_layout.addWidget(self.client_table)
        self.tabs.addTab(self.client_tab, "DHCP Client")

        # ── Tab 4: DHCP Leases ────────────────────────────────────────────────
        self.lease_tab = QWidget()
        lease_layout = QVBoxLayout(self.lease_tab)
        lease_layout.setContentsMargins(12, 12, 12, 12)
        lease_layout.setSpacing(10)

        lease_hdr = QHBoxLayout()
        lease_lbl = QLabel("Perangkat Sewa Alamat IP Aktif (DHCP Leases)")
        lease_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 700;")
        lease_hdr.addWidget(lease_lbl)
        lease_hdr.addStretch()

        self.static_btn = QPushButton("Jadikan Statis (Make Static)  📌")
        self.static_btn.setStyleSheet(
            "QPushButton { background-color: #A78BFA; color: white; padding: 6px 12px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #8B5CF6; }"
        )
        self.static_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.static_btn.clicked.connect(self._on_make_static_clicked)
        lease_hdr.addWidget(self.static_btn)
        lease_layout.addLayout(lease_hdr)

        self.lease_table = QTableWidget(0, 5)
        self.lease_table.verticalHeader().setDefaultSectionSize(36)
        self.lease_table.setHorizontalHeaderLabels(["Alamat IP", "MAC Address", "Hostname", "Status", "Expires In"])
        self.lease_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lease_table.setStyleSheet(
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
        lease_layout.addWidget(self.lease_table)
        self.tabs.addTab(self.lease_tab, "DHCP Leases")

    def load_ip_dhcp_data(self) -> None:
        """Populates fields based on connection state or demo mode."""
        # 1. IP Addresses list
        self.ip_table.setRowCount(2)
        self.ip_table.setItem(0, 0, QTableWidgetItem("192.168.88.1/24"))
        self.ip_table.setItem(0, 1, QTableWidgetItem("bridge"))
        self.ip_table.setItem(0, 2, QTableWidgetItem("192.168.88.0"))
        self.ip_table.setItem(0, 3, QTableWidgetItem("no"))
        self.ip_table.setItem(0, 4, QTableWidgetItem("no"))

        self.ip_table.setItem(1, 0, QTableWidgetItem("10.0.0.15/24"))
        self.ip_table.setItem(1, 1, QTableWidgetItem("ether1 (WAN)"))
        self.ip_table.setItem(1, 2, QTableWidgetItem("10.0.0.0"))
        self.ip_table.setItem(1, 3, QTableWidgetItem("yes"))
        self.ip_table.setItem(1, 4, QTableWidgetItem("no"))

        # 2. DHCP Servers list
        self.dhcp_table.setRowCount(1)
        self.dhcp_table.setItem(0, 0, QTableWidgetItem("dhcp_default"))
        self.dhcp_table.setItem(0, 1, QTableWidgetItem("bridge"))
        self.dhcp_table.setItem(0, 2, QTableWidgetItem("dhcp_pool1"))
        self.dhcp_table.setItem(0, 3, QTableWidgetItem("10m"))

        # 3. DHCP Clients list
        self.client_table.setRowCount(1)
        self.client_table.setItem(0, 0, QTableWidgetItem("ether1 (WAN)"))
        self.client_table.setItem(0, 1, QTableWidgetItem("bound"))
        self.client_table.setItem(0, 2, QTableWidgetItem("10.0.0.15/24"))
        self.client_table.setItem(0, 3, QTableWidgetItem("yes"))

        # 4. Leases list
        self.lease_table.setRowCount(2)
        self.lease_table.setItem(0, 0, QTableWidgetItem("192.168.88.24"))
        self.lease_table.setItem(0, 1, QTableWidgetItem("00:1E:A6:4F:92:B8"))
        self.lease_table.setItem(0, 2, QTableWidgetItem("Laptop-Staff"))
        self.lease_table.setItem(0, 3, QTableWidgetItem("bound"))
        self.lease_table.setItem(0, 4, QTableWidgetItem("8m 14s"))

        self.lease_table.setItem(1, 0, QTableWidgetItem("192.168.88.100"))
        self.lease_table.setItem(1, 1, QTableWidgetItem("74:AC:5F:92:4B:C2"))
        self.lease_table.setItem(1, 2, QTableWidgetItem("Android-User"))
        self.lease_table.setItem(1, 3, QTableWidgetItem("bound"))
        self.lease_table.setItem(1, 4, QTableWidgetItem("2m 45s"))

    def set_advanced_mode(self, active: bool) -> None:
        self._is_advanced_mode = active
        # Show/Hide advanced detail columns (e.g. Network address column, Default Route flags)
        self.ip_table.setColumnHidden(2, not active)
        self.ip_table.setColumnHidden(3, not active)
        self.ip_table.setColumnHidden(4, not active)

    def _on_ip_add_clicked(self) -> None:
        QMessageBox.information(
            self, "Tambah IP",
            "Simulator Form Tambah IP Address Aktif!\n\n"
            "Format: 192.168.88.1/24\n"
            "Interface: bridge / ether2\n"
        )

    def _on_make_static_clicked(self) -> None:
        row = self.lease_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Leases", "Silakan pilih baris alamat sewa perangkat terlebih dahulu.")
            return

        ip = self.lease_table.item(row, 0).text()
        mac = self.lease_table.item(row, 1).text()
        QMessageBox.information(
            self, "Make Static Leases",
            f"Alamat sewa untuk {ip} ({mac}) berhasil diikat secara statis (Make Static) pada MikroTik RouterOS!"
        )
