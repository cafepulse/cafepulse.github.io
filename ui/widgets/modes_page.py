"""
CafePulse — Modes Page  (Phase 3 — Home WiFi enabled)
Mode switcher: Demo scenarios + Home WiFi + placeholders.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QButtonGroup, QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal

from modes.demo.demo_engine import SCENARIOS

logger = logging.getLogger("cafepulse.ui.modes")

# ─── Mode IDs ─────────────────────────────────────────────────────────────────
MODE_DEMO      = "demo"
MODE_HOME_WIFI = "home_wifi"
MODE_HOTSPOT   = "hotspot"
MODE_MIKROTIK  = "mikrotik"


class ModeButton(QPushButton):
    """Top-level mode selector button."""

    def __init__(self, mode_id: str, label: str, badge: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("NavButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(56)
        self._mode_id = mode_id

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)

        name_lbl = QLabel(label)
        name_lbl.setStyleSheet("font-size:13px; font-weight:600; color:#E2E8F0;")
        layout.addWidget(name_lbl)
        layout.addStretch()

        if badge:
            badge_lbl = QLabel(badge)
            badge_lbl.setStyleSheet(
                "color:#38BDF8; background:#0F2030; border:1px solid #38BDF8;"
                "border-radius:4px; font-size:10px; padding:1px 6px; font-weight:700;"
            )
            layout.addWidget(badge_lbl)

    @property
    def mode_id(self) -> str:
        return self._mode_id


class ScenarioCard(QFrame):
    """Clickable demo scenario card."""
    selected = pyqtSignal(str)

    def __init__(self, key: str, scenario, parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(80)
        self._key = key

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        name_lbl = QLabel(scenario.display_name)
        name_lbl.setStyleSheet("font-size:14px; font-weight:700; color:#E2E8F0;")
        layout.addWidget(name_lbl)

        info_lbl = QLabel(
            f"{scenario.device_count[0]}–{scenario.device_count[1]} devices  "
            f"↓ up to {scenario.download_range[1]:.0f} Mbps"
        )
        info_lbl.setStyleSheet("font-size:11px; color:#64748B;")
        layout.addWidget(info_lbl)

    def mousePressEvent(self, event) -> None:
        self.selected.emit(self._key)
        super().mousePressEvent(event)

    def set_active(self, active: bool) -> None:
        if active:
            self.setStyleSheet(
                "QFrame#DashCard { border: 1px solid #38BDF8; background:#0F2030; }"
            )
        else:
            self.setStyleSheet("")


class ModesPage(QWidget):
    """
    Full mode selector page.
    Signals:
        mode_changed(mode_id: str)
        scenario_changed(scenario_key: str)
    """

    mode_changed     = pyqtSignal(str)
    scenario_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._active_mode     = MODE_DEMO
        self._active_scenario = "small_cafe"
        self._scenario_cards: dict[str, ScenarioCard] = {}
        self._mode_buttons:   dict[str, ModeButton]   = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title = QLabel("Monitoring Modes")
        title.setObjectName("SectionHeader")
        layout.addWidget(title)

        sub = QLabel("Choose how CafePulse monitors your network")
        sub.setObjectName("SectionSubtitle")
        layout.addWidget(sub)

        # ── Mode Buttons Row ──────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_group = QButtonGroup(self)
        btn_group.setExclusive(True)

        modes = [
            (MODE_DEMO,      "⬡  Demo Mode",       "OFFLINE"),
            (MODE_HOME_WIFI, "⬡  Home WiFi",        "FREE"),
            (MODE_HOTSPOT,   "⬡  Hotspot",          "FREE"),
            (MODE_MIKROTIK,  "⬡  MikroTik ★",      "PROFESSIONAL"),
        ]

        for mode_id, label, badge in modes:
            btn = ModeButton(mode_id, label, badge)
            btn_group.addButton(btn)
            self._mode_buttons[mode_id] = btn
            btn.clicked.connect(lambda chk, mid=mode_id: self._on_mode_clicked(mid))
            btn_row.addWidget(btn)

        self._mode_buttons[MODE_DEMO].setChecked(True)
        layout.addLayout(btn_row)

        # ── Mode Detail Area (stacked) ────────────────────────────────────────
        self._detail_stack = QStackedWidget()
        layout.addWidget(self._detail_stack)

        # Demo sub-panel
        self._detail_stack.addWidget(self._build_demo_panel())
        # Home WiFi sub-panel
        self._detail_stack.addWidget(self._build_home_wifi_panel())
        # Hotspot sub-panel
        self._detail_stack.addWidget(self._build_hotspot_panel())
        # MikroTik panel
        self._detail_stack.addWidget(self._build_mikrotik_panel())

        layout.addStretch()

    # ─── Sub-Panels ───────────────────────────────────────────────────────────

    def _build_demo_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        lbl = QLabel("SELECT SCENARIO")
        lbl.setStyleSheet(
            "color:#38BDF8; font-size:11px; font-weight:700; letter-spacing:1px;"
        )
        layout.addWidget(lbl)

        grid = QHBoxLayout()
        grid.setSpacing(12)

        for key, scenario in SCENARIOS.items():
            card = ScenarioCard(key, scenario)
            card.selected.connect(self._on_scenario_selected)
            self._scenario_cards[key] = card
            grid.addWidget(card)

        layout.addLayout(grid)
        default_card = self._scenario_cards.get("small_cafe")
        if default_card:
            default_card.set_active(True)
        return panel

    def _build_home_wifi_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        info = QFrame()
        info.setObjectName("DashCard")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(16, 12, 16, 12)
        info_layout.setSpacing(6)

        title = QLabel("Home WiFi Mode — Plug & Play Discovery")
        title.setStyleSheet("color:#E2E8F0; font-size:13px; font-weight:700;")
        info_layout.addWidget(title)

        desc = QLabel(
            "Discovers all devices on your local network using ARP + ping sweep.\n"
            "No router configuration required.\n\n"
            "⚠  Cannot measure per-device bandwidth without router integration.\n"
            "   Scan interval: 30 seconds (auto) or manual trigger."
        )
        desc.setStyleSheet("color:#94A3B8; font-size:12px;")
        desc.setWordWrap(True)
        info_layout.addWidget(desc)

        activate_btn = QPushButton("Activate Home WiFi Mode")
        activate_btn.setObjectName("QuickScanButton")
        activate_btn.setFixedWidth(220)
        activate_btn.clicked.connect(lambda: self.mode_changed.emit(MODE_HOME_WIFI))
        info_layout.addWidget(activate_btn)

        layout.addWidget(info)
        return panel

    def _build_hotspot_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        info = QFrame()
        info.setObjectName("DashCard")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(16, 12, 16, 12)
        info_layout.setSpacing(8)

        title = QLabel("Hotspot Mode — Auto-Detected, Fast Refresh")
        title.setStyleSheet("color:#E2E8F0; font-size:13px; font-weight:700;")
        info_layout.addWidget(title)

        for line, color in [
            ("🤖  Android Hotspot — 192.168.43.x detected automatically", "#22C55E"),
            ("📱  iPhone Hotspot  — 172.20.10.x detected automatically",  "#38BDF8"),
            ("⏱  Scan interval: 10 seconds (fast refresh)",               "#94A3B8"),
            ("📋  Session tracking: join/leave events logged to DB",       "#94A3B8"),
        ]:
            lbl = QLabel(line)
            lbl.setStyleSheet(f"color:{color}; font-size:12px;")
            info_layout.addWidget(lbl)

        activate_btn = QPushButton("Activate Hotspot Mode")
        activate_btn.setObjectName("QuickScanButton")
        activate_btn.setFixedWidth(220)
        activate_btn.clicked.connect(lambda: self.mode_changed.emit("hotspot"))
        info_layout.addWidget(activate_btn)
        layout.addWidget(info)
        return panel

    def _build_placeholder_panel(self, title: str, desc: str) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("DashCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)

        t = QLabel(title)
        t.setStyleSheet("color:#E2E8F0; font-size:14px; font-weight:700;")
        card_layout.addWidget(t)

        d = QLabel(desc)
        d.setStyleSheet("color:#64748B; font-size:12px;")
        d.setWordWrap(True)
        card_layout.addWidget(d)

        layout.addWidget(card)
        return panel

    def _build_mikrotik_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        info = QFrame()
        info.setObjectName("DashCard")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(16, 12, 16, 12)
        info_layout.setSpacing(8)

        title = QLabel("MikroTik Mode — Professional")
        title.setStyleSheet("color:#E2E8F0; font-size:13px; font-weight:700;")
        info_layout.addWidget(title)

        desc = QLabel(
            "Full RouterOS integration with real-time bandwidth, queue monitoring,\n"
            "and AI-assisted insights."
        )
        desc.setStyleSheet("color:#94A3B8; font-size:12px;")
        desc.setWordWrap(True)
        info_layout.addWidget(desc)

        activate_btn = QPushButton("Activate MikroTik Mode")
        activate_btn.setObjectName("QuickScanButton")
        activate_btn.setFixedWidth(220)
        activate_btn.clicked.connect(lambda: self.mode_changed.emit(MODE_MIKROTIK))
        info_layout.addWidget(activate_btn)

        layout.addWidget(info)
        return panel

    # ─── Slots ────────────────────────────────────────────────────────────────

    def _on_mode_clicked(self, mode_id: str) -> None:
        self._active_mode = mode_id
        idx = list(self._mode_buttons.keys()).index(mode_id)
        self._detail_stack.setCurrentIndex(idx)
        if mode_id == MODE_DEMO:
            self.mode_changed.emit(MODE_DEMO)

    def _on_scenario_selected(self, key: str) -> None:
        for k, card in self._scenario_cards.items():
            card.set_active(k == key)
        self._active_scenario = key
        self.scenario_changed.emit(key)

    # ─── External API ─────────────────────────────────────────────────────────

    def set_active_scenario(self, key: str) -> None:
        self._on_scenario_selected(key)

    def _sync_ui_to_mode(self, mode_id: str) -> None:
        """Update button check state and detail panel WITHOUT emitting mode_changed.
        Called externally when the mode is already active and we just need the
        Modes page to reflect the current state visually."""
        self._active_mode = mode_id
        btn = self._mode_buttons.get(mode_id)
        if btn:
            btn.setChecked(True)
        keys = list(self._mode_buttons.keys())
        if mode_id in keys:
            self._detail_stack.setCurrentIndex(keys.index(mode_id))

    def set_active_mode(self, mode_id: str) -> None:
        self._sync_ui_to_mode(mode_id)
