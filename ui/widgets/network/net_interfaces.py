"""
CafePulse — Interfaces & Visual Topology Page (Phase 9)
Tabular listings for Ethernet, Bridges, VLANs, and custom horizontal schematic topologies.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame
)
from PyQt6.QtCore import Qt


class NetInterfaces(QWidget):
    """
    Interface Management workspace panel.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()
        self.load_interface_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # ── Upper section: Visual Topology Schematic ─────────────────────────
        topo_card = QFrame()
        topo_card.setObjectName("DashCard")
        topo_card.setStyleSheet("background-color: #111625; border-top: 3px solid #06B6D4;")
        topo_layout = QVBoxLayout(topo_card)
        topo_layout.setContentsMargins(16, 14, 16, 14)
        topo_layout.setSpacing(10)

        topo_title = QLabel("SKEMATIS TOPOLOGI INTERFACE SEDERHANA")
        topo_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        topo_layout.addWidget(topo_title)

        # Visual layout represented as a beautiful structured card tree
        self.topo_lbl = QLabel(
            "<b>[ Jaringan Internet / WAN (ether1) ]</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>"
            "<b>[ Router MikroTik ]</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► <b>bridge_local</b> ──► <i>ether2, ether3, ether4 (Ports LAN)</i><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──► <b>VLAN 10 (Staff)</b> (bridge_local)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──► <b>VLAN 20 (Guest)</b> (bridge_local)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──► <b>ether5 (Isolated LAN)</b> (Unbridged)"
        )
        self.topo_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; line-height: 1.6; font-family: Consolas, monospace;")
        topo_layout.addWidget(self.topo_lbl)
        layout.addWidget(topo_card)

        # ── Lower section: Tab lists ─────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #1E293B; background: transparent; border-radius: 8px; }"
            "QTabBar::tab { background: #0F131F; color: #64748B; padding: 6px 12px; font-weight: 600; border: 1px solid #1E293B; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px; }"
            "QTabBar::tab:selected { background: #1E293B; color: #06B6D4; border-bottom: 2px solid #06B6D4; }"
        )
        layout.addWidget(self.tabs)

        # Ethernet
        self.eth_tab = QTableWidget(0, 4)
        self.eth_tab.verticalHeader().setDefaultSectionSize(36)
        self.eth_tab.setHorizontalHeaderLabels(["Name", "Type", "Actual MTU", "Mac Address"])
        self.eth_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.eth_tab.setStyleSheet(
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
        self.tabs.addTab(self.eth_tab, "Ethernet")

        # Bridges
        self.br_tab = QTableWidget(0, 3)
        self.br_tab.verticalHeader().setDefaultSectionSize(36)
        self.br_tab.setHorizontalHeaderLabels(["Name", "Protocol Mode", "Fast Forward"])
        self.br_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.br_tab.setStyleSheet(
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
        self.tabs.addTab(self.br_tab, "Bridges")

        # VLANs
        self.vlan_tab = QTableWidget(0, 3)
        self.vlan_tab.verticalHeader().setDefaultSectionSize(36)
        self.vlan_tab.setHorizontalHeaderLabels(["Name", "VLAN ID", "Interface"])
        self.vlan_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vlan_tab.setStyleSheet(
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
        self.tabs.addTab(self.vlan_tab, "VLAN")

    def load_interface_data(self) -> None:
        # Load Ethernet
        self.eth_tab.setRowCount(5)
        for i in range(5):
            name = f"ether{i+1}"
            if i == 0:
                name += " (WAN)"
            self.eth_tab.setItem(i, 0, QTableWidgetItem(name))
            self.eth_tab.setItem(i, 1, QTableWidgetItem("ether"))
            self.eth_tab.setItem(i, 2, QTableWidgetItem("1500"))
            self.eth_tab.setItem(i, 3, QTableWidgetItem(f"00:1E:A6:4F:92:B{i+1}"))

        # Load Bridges
        self.br_tab.setRowCount(1)
        self.br_tab.setItem(0, 0, QTableWidgetItem("bridge_local"))
        self.br_tab.setItem(0, 1, QTableWidgetItem("none"))
        self.br_tab.setItem(0, 2, QTableWidgetItem("yes"))

        # Load VLANs
        self.vlan_tab.setRowCount(2)
        self.vlan_tab.setItem(0, 0, QTableWidgetItem("VLAN 10 (Staff)"))
        self.vlan_tab.setItem(0, 1, QTableWidgetItem("10"))
        self.vlan_tab.setItem(0, 2, QTableWidgetItem("bridge_local"))

        self.vlan_tab.setItem(1, 0, QTableWidgetItem("VLAN 20 (Guest)"))
        self.vlan_tab.setItem(1, 1, QTableWidgetItem("20"))
        self.vlan_tab.setItem(1, 2, QTableWidgetItem("bridge_local"))
