"""
CafePulse — Network Workspace Master Coordinator Page (Phase 3)
Coordinating 15 modular views into an elegant, side-tab dashboard layout.
Emulates the exact API mapping required by MainWindow.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot

# Import our 15 deconstructed views
from ui.widgets.network.net_overview import NetOverview
from ui.widgets.network.net_connections import NetConnections
from ui.widgets.network.net_ip_dhcp import NetIpDhcp
from ui.widgets.network.net_dns import NetDns
from ui.widgets.network.net_wifi import NetWifi
from ui.widgets.network.net_interfaces import NetInterfaces
from ui.widgets.network.net_traffic import NetTraffic
from ui.widgets.network.net_access_control import NetAccessControl
from ui.widgets.network.net_routing import NetRouting
from ui.widgets.network.net_firewall import NetFirewall
from ui.widgets.network.net_ppp import NetPpp
from ui.widgets.network.net_hotspot import NetHotspot
from ui.widgets.network.net_queue import NetQueue
from ui.widgets.network.net_backup import NetBackup
from ui.widgets.network.net_system import NetSystem

logger = logging.getLogger("cafepulse.ui.network")


class NetworkPage(QWidget):
    """
    Master coordinator wrapping all 15 refactored Network Workspace views.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._db = db
        self._app_state = app_state
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Row
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Network Workspace (MikroTik)")
        title.setObjectName("SectionHeader")
        title_box.addWidget(title)

        sub = QLabel("Infrastruktur, routing, firewall, ppp, hotspot dan QoS terintegrasi.")
        sub.setObjectName("SectionSubtitle")
        title_box.addWidget(sub)
        header.addLayout(title_box)
        header.addStretch()

        self.conn_state_lbl = QLabel("DISCONNECTED")
        self.conn_state_lbl.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 800; padding: 6px 12px; background-color: #1E1B1B; border-radius: 6px; border: 1px solid #7F1D1D;")
        header.addWidget(self.conn_state_lbl)
        layout.addLayout(header)

        # Tab Widget container (Vertical sub-tabs style or clean top-tab)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #1E293B; background: transparent; border-radius: 8px; }"
            "QTabBar::tab { background: #0F131F; color: #64748B; padding: 6px 12px; font-size: 11px; font-weight: 600; border: 1px solid #1E293B; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }"
            "QTabBar::tab:selected { background: #1E293B; color: #06B6D4; border-bottom: 2px solid #06B6D4; }"
        )
        layout.addWidget(self.tabs)

        # Instantiate our 15 sub-views
        self.view_overview = NetOverview(self._db, self._app_state, self)
        self.view_connections = NetConnections(self._db, self._app_state, self)
        self.view_ip_dhcp = NetIpDhcp(self._db, self._app_state, self)
        self.view_dns = NetDns(self._db, self._app_state, self)
        self.view_wifi = NetWifi(self._db, self._app_state, self)
        self.view_interfaces = NetInterfaces(self._db, self._app_state, self)
        self.view_traffic = NetTraffic(self._db, self._app_state, self)
        self.view_access = NetAccessControl(self._db, self._app_state, self)
        self.view_routing = NetRouting(self._db, self._app_state, self)
        self.view_firewall = NetFirewall(self._db, self._app_state, self)
        self.view_ppp = NetPpp(self._db, self._app_state, self)
        self.view_hotspot = NetHotspot(self._db, self._app_state, self)
        self.view_queue = NetQueue(self._db, self._app_state, self)
        self.view_backup = NetBackup(self._db, self._app_state, self)
        self.view_system = NetSystem(self._db, self._app_state, self)

        # Add tabs to selector
        self.tabs.addTab(self.view_overview, "Overview")
        self.tabs.addTab(self.view_connections, "Connections")
        self.tabs.addTab(self.view_ip_dhcp, "IP & DHCP")
        self.tabs.addTab(self.view_dns, "DNS")
        self.tabs.addTab(self.view_wifi, "WiFi")
        self.tabs.addTab(self.view_interfaces, "Interfaces")
        self.tabs.addTab(self.view_traffic, "Traffic")
        self.tabs.addTab(self.view_access, "Access Control")
        self.tabs.addTab(self.view_routing, "Routing")
        self.tabs.addTab(self.view_firewall, "Firewall")
        self.tabs.addTab(self.view_ppp, "PPP")
        self.tabs.addTab(self.view_hotspot, "Hotspot")
        self.tabs.addTab(self.view_queue, "Queue")
        self.tabs.addTab(self.view_backup, "Backup")
        self.tabs.addTab(self.view_system, "System")

        # ── Table Aliases for Responsive System ──────────────────────────────
        # Map attributes exactly as they are queried by MainWindow in register_table
        self._ip_table = self.view_ip_dhcp.ip_table
        self._dns_table = self.view_dns.static_table
        self._cache_table = self.view_dns.cache_table

    # ── MainWindow Delegators ─────────────────────────────────────────────────

    def update_connection_state(self, state: str) -> None:
        self.conn_state_lbl.setText(state)
        if state in ("CONNECTED", "RECOVERED"):
            self.conn_state_lbl.setStyleSheet("color: #22C55E; font-size: 13px; font-weight: 800; padding: 6px 12px; background-color: #16271A; border-radius: 6px; border: 1px solid #14532D;")
        else:
            self.conn_state_lbl.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 800; padding: 6px 12px; background-color: #1E1B1B; border-radius: 6px; border: 1px solid #7F1D1D;")

    def update_stats(self, payload: dict) -> None:
        """Called by MainWindow on live polling ticks."""
        # Update overview counters & gauges
        self.view_overview.update_stats(payload)

        # Update traffic monitoring curves
        self.view_traffic.update_ticks(payload)

        # Update live active hotspot lists
        active_hosts = payload.get("active_hosts", [])
        self.view_hotspot.sess_table.setRowCount(len(active_hosts))
        for i, host in enumerate(active_hosts):
            self.view_hotspot.sess_table.setItem(i, 0, QTableWidgetItem(host.get("user", "—")))
            self.view_hotspot.sess_table.setItem(i, 1, QTableWidgetItem(f"{host.get('address', '—')} / {host.get('mac-address', '—')}"))
            self.view_hotspot.sess_table.setItem(i, 2, QTableWidgetItem(host.get("uptime", "—")))
            self.view_hotspot.sess_table.setItem(i, 3, QTableWidgetItem(f"{host.get('bytes-in', 0)} B / {host.get('bytes-out', 0)} B"))

        # Synchronize wireless hardware capability indicator
        has_wireless = payload.get("has_wireless", False)
        self.view_wifi.set_hardware_present(has_wireless)
