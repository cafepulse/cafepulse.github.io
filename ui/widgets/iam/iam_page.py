"""
CafePulse — IAM Master Coordinator (Internet Access Management)
Coordinative tab container wrapping all sub-views (Dashboard, Packages, Vouchers, Customers, Guests).
Acts as a seamless, backward-compatible drop-in wrapper.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QFrame, QTableWidget
)
from PyQt6.QtCore import Qt, pyqtSlot

# Import our modular sub-views
from ui.widgets.iam.iam_dashboard import IamDashboard
from ui.widgets.iam.iam_packages import IamPackages
from ui.widgets.iam.iam_vouchers import IamVouchers
from ui.widgets.iam.iam_customers import IamCustomers
from ui.widgets.iam.iam_guests import IamGuests

logger = logging.getLogger("cafepulse.ui.iam")


class IamPage(QWidget):
    """
    Main portal page for the Internet Access Management module.
    """
    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._db = db
        self._app_state = app_state
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Master Header Row
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        
        title = QLabel("Manajemen Akses Internet")
        title.setObjectName("SectionHeader")
        title_box.addWidget(title)

        sub = QLabel("Kelola paket kecepatan, voucher aktivasi, data pelanggan, dan akses tamu sekali klik.")
        sub.setObjectName("SectionSubtitle")
        title_box.addWidget(sub)
        header.addLayout(title_box)
        header.addStretch()
        layout.addLayout(header)

        # Tab Widget container
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #1E293B; background: transparent; border-radius: 8px; margin-top: -1px; }"
            "QTabBar::tab { background: #0F131F; color: #64748B; padding: 10px 20px; font-weight: 600; border: 1px solid #1E293B; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px; }"
            "QTabBar::tab:hover { background: #161B27; color: #E2E8F0; }"
            "QTabBar::tab:selected { background: #1E293B; color: #06B6D4; border-bottom: 2px solid #06B6D4; }"
        )

        # Instantiate sub-views
        self.view_dashboard = IamDashboard(self._db, self._app_state, self)
        self.view_packages = IamPackages(self._db, self._app_state, self)
        self.view_vouchers = IamVouchers(self._db, self._app_state, self)
        self.view_customers = IamCustomers(self._db, self._app_state, self)
        self.view_guests = IamGuests(self._db, self._app_state, self)

        # Connect package change triggers to voucher reloader
        self.view_packages.packages_changed.connect(self.view_vouchers.reload_packages_combo)

        # Add tabs
        self.tabs.addTab(self.view_dashboard, "Ringkasan")
        self.tabs.addTab(self.view_packages, "Paket Akses")
        self.tabs.addTab(self.view_vouchers, "Voucher")
        self.tabs.addTab(self.view_customers, "Pelanggan")
        self.tabs.addTab(self.view_guests, "WiFi Tamu")

        layout.addWidget(self.tabs)

        # ── Backward Compatibility Hooks ─────────────────────────────────────
        # Main Window references self.user_table inside the responsive system.
        # We bind it directly to the vouchers list table.
        self.user_table = self.view_vouchers.table

    # ── Master Delegators (backward-compatible methods called by MainWindow) ──

    def set_scanning(self, active: bool) -> None:
        """Sets scanning overlay/status."""
        logger.debug(f"IAM Page scanning state: {active}")
        # We can optionally disable tabs during active background scan
        self.tabs.setEnabled(not active)

    def update_from_scan(self, payload: dict) -> None:
        """Called during portable local hotspot scan."""
        # Update our active hosts in dashboard from sweep scan results
        devices = payload.get("devices", [])
        active_hosts = []
        for dev in devices:
            active_hosts.append({
                "user": dev.get("hostname") or dev.get("mac_address"),
                "address": dev.get("ip_address"),
                "mac-address": dev.get("mac_address"),
                "uptime": "Live Scan"
            })
        self.view_dashboard.update_active_sessions(active_hosts)

    def update_hotspot_info(self, info: dict) -> None:
        """Updates standard local sweep scan info."""
        pass

    def update_from_mikrotik_scan(self, payload: dict) -> None:
        """Called during active MikroTik router sweep scans."""
        # Reload active session listings
        active_hosts = payload.get("active_hosts", [])
        self.view_dashboard.update_active_sessions(active_hosts)
        
        # Reload SQLite state sync in background
        self.view_vouchers.reload_packages_combo()
        self.view_dashboard.update_kpis()
