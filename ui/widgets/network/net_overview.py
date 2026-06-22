"""
CafePulse — Network Overview landing page (Phase 4)
Displays clean status metrics, resource usage gauges, and public ping checklists.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QProgressBar, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSlot
from ui.widgets.dash_card import DashCard


class NetOverview(QWidget):
    """
    Approachable landing panel for the Network Workspace.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ── Upper row: Identity Cards & Internet Check ────────────────────────
        top_row = QHBoxLayout()
        top_row.setSpacing(14)

        # Identity Card
        self.ident_card = QFrame()
        self.ident_card.setObjectName("DashCard")
        self.ident_card.setStyleSheet("background-color: #111625; border-left: 3px solid #06B6D4;")
        ident_layout = QVBoxLayout(self.ident_card)
        ident_layout.setContentsMargins(14, 12, 14, 12)
        
        self.ident_title = QLabel("ROUTER IDENTITY")
        self.ident_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        ident_layout.addWidget(self.ident_title)

        self.ident_val = QLabel("CafePulse_Router")
        self.ident_val.setStyleSheet("color: #E2E8F0; font-size: 18px; font-weight: 700;")
        ident_layout.addWidget(self.ident_val)

        self.ident_sub = QLabel("Model: hEX S | OS: RouterOS v7.12")
        self.ident_sub.setStyleSheet("color: #64748B; font-size: 11px;")
        ident_layout.addWidget(self.ident_sub)
        top_row.addWidget(self.ident_card)

        # Internet Status Checklist
        self.net_check_card = QFrame()
        self.net_check_card.setObjectName("DashCard")
        self.net_check_card.setStyleSheet("background-color: #111625; border-left: 3px solid #22C55E;")
        net_layout = QVBoxLayout(self.net_check_card)
        net_layout.setContentsMargins(14, 12, 14, 12)

        self.net_title = QLabel("INTERNET STATUS")
        self.net_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        net_layout.addWidget(self.net_title)

        self.net_val = QLabel("Online")
        self.net_val.setStyleSheet("color: #22C55E; font-size: 18px; font-weight: 700;")
        net_layout.addWidget(self.net_val)

        self.net_sub = QLabel("Gateway: 192.168.1.1 (Reachable)")
        self.net_sub.setStyleSheet("color: #64748B; font-size: 11px;")
        net_layout.addWidget(self.net_sub)
        top_row.addWidget(self.net_check_card)

        layout.addLayout(top_row)

        # ── Middle row: Resource Gauges (CPU, Memory, Uptime) ─────────────────
        res_container = QWidget()
        res_layout = QGridLayout(res_container)
        res_layout.setContentsMargins(0, 0, 0, 0)
        res_layout.setSpacing(12)

        # CPU Progress Card
        self.cpu_card = QFrame()
        self.cpu_card.setObjectName("DashCard")
        cpu_layout = QVBoxLayout(self.cpu_card)
        cpu_layout.setContentsMargins(14, 12, 14, 12)
        
        cpu_lbl = QLabel("CPU USAGE")
        cpu_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700;")
        cpu_layout.addWidget(cpu_lbl)

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setValue(12)
        self.cpu_bar.setStyleSheet(
            "QProgressBar { background: #1E293B; border-radius: 4px; text-align: center; color: white; font-weight: bold; }"
            "QProgressBar::chunk { background: #0284C7; border-radius: 4px; }"
        )
        self.cpu_bar.setFixedHeight(20)
        cpu_layout.addWidget(self.cpu_bar)
        res_layout.addWidget(self.cpu_card, 0, 0)

        # Memory Card
        self.ram_card = QFrame()
        self.ram_card.setObjectName("DashCard")
        ram_layout = QVBoxLayout(self.ram_card)
        ram_layout.setContentsMargins(14, 12, 14, 12)
        
        ram_lbl = QLabel("MEMORY USAGE")
        ram_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700;")
        ram_layout.addWidget(ram_lbl)

        self.ram_bar = QProgressBar()
        self.ram_bar.setValue(45)
        self.ram_bar.setStyleSheet(
            "QProgressBar { background: #1E293B; border-radius: 4px; text-align: center; color: white; font-weight: bold; }"
            "QProgressBar::chunk { background: #10B981; border-radius: 4px; }"
        )
        self.ram_bar.setFixedHeight(20)
        ram_layout.addWidget(self.ram_bar)
        res_layout.addWidget(self.ram_card, 0, 1)

        layout.addWidget(res_container)

        # ── Lower row: Dynamic DNA counters ──────────────────────────────────
        dna_container = QWidget()
        dna_layout = QHBoxLayout(dna_container)
        dna_layout.setContentsMargins(0, 0, 0, 0)
        dna_layout.setSpacing(12)

        self.card_devices = DashCard("Active Clients", "0", "connected devices", "#38BDF8")
        self.card_hotspot = DashCard("Hotspot Users", "0", "active sessions", "#A78BFA")
        self.card_uptime = DashCard("Router Uptime", "—", "up since boot", "#F59E0B")

        dna_layout.addWidget(self.card_devices)
        dna_layout.addWidget(self.card_hotspot)
        dna_layout.addWidget(self.card_uptime)
        layout.addWidget(dna_container)

        layout.addStretch()

    def update_stats(self, payload: dict) -> None:
        """Dynamically update dashboard cards from live ticks."""
        cpu = int(payload.get("cpu_load", payload.get("cpu", 12)))
        self.cpu_bar.setValue(cpu)
        
        # Format memory
        free = payload.get("free_memory", 128.0)
        total = payload.get("total_memory", 256.0)
        used_pct = int(((total - free) / total) * 100) if total > 0 else 45
        self.ram_bar.setValue(used_pct)

        # Uptime
        uptime = payload.get("uptime", "—")
        self.card_uptime.set_value(uptime)

        # Counters
        dev_cnt = payload.get("device_count", payload.get("active_hosts_count", 0))
        self.card_devices.set_value(str(dev_cnt))
        
        hs_cnt = payload.get("hotspot_active_count", 0)
        self.card_hotspot.set_value(str(hs_cnt))

        # Router Identity
        identity = payload.get("identity", "CafePulse_Router")
        self.ident_val.setText(identity)
        
        board = payload.get("board_name", "hEX S")
        version = payload.get("version", "v7.12")
        self.ident_sub.setText(f"Model: {board} | OS: RouterOS {version}")
