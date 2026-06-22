"""
CafePulse — Alerts Page
Shows recent alerts with type badges, message, and timestamp.
"""

import logging
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QColor

logger = logging.getLogger("cafepulse.ui.alerts")

def get_alert_colors(alert_type: str, theme: str) -> tuple[str, str, str]:
    # Returns (text_color, bg_color, border_color)
    if theme == "light":
        light_colors = {
            "reconnect":  ("#D97706", "#FEF3C7", "#FDE68A"), # Amber-600, Amber-100, Amber-200
            "bandwidth":  ("#DC2626", "#FEE2E2", "#FCA5A5"), # Red-600, Red-100, Red-300
            "new_device": ("#0284C7", "#E0F2FE", "#BAE6FD"), # Sky-600, Sky-100, Sky-300
            "congestion": ("#7C3AED", "#F3E8FF", "#E9D5FF"), # Violet-600, Violet-100, Violet-300
            "suspicious": ("#DC2626", "#FEE2E2", "#FCA5A5"),
            "test":       ("#059669", "#D1FAE5", "#A7F3D0"), # Emerald-600, Emerald-100, Emerald-300
        }
        return light_colors.get(alert_type, ("#475569", "#F1F5F9", "#CBD5E1"))
    else:
        dark_colors = {
            "reconnect":  ("#F59E0B", "#1A140A", "#F59E0B"),
            "bandwidth":  ("#EF4444", "#1A0A0A", "#EF4444"),
            "new_device": ("#38BDF8", "#0A1420", "#38BDF8"),
            "congestion": ("#A78BFA", "#120A1A", "#A78BFA"),
            "suspicious": ("#EF4444", "#1A0A0A", "#EF4444"),
            "test":       ("#22C55E", "#0A1A0A", "#22C55E"),
        }
        return dark_colors.get(alert_type, ("#94A3B8", "#161B27", "#94A3B8"))


class AlertItem(QFrame):
    """Single alert row with type badge + message + time."""

    def __init__(self, alert_type: str, message: str, timestamp: str, theme: str = "dark", parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setFixedHeight(62)

        self.alert_type = alert_type
        self.message = message
        self.timestamp = timestamp

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(14)

        # Type badge
        self.badge = QLabel(alert_type.upper())
        self.badge.setFixedWidth(90)
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.badge)

        # Message
        self.msg_lbl = QLabel(message)
        self.msg_lbl.setWordWrap(False)
        layout.addWidget(self.msg_lbl, stretch=1)

        # Timestamp
        self.ts = QLabel(timestamp)
        self.ts.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.ts)

        self.update_theme(theme)

    def update_theme(self, theme: str) -> None:
        accent, bg, border = get_alert_colors(self.alert_type, theme)
        self.badge.setStyleSheet(
            f"background-color:{bg}; color:{accent}; border:1px solid {border};"
            f"border-radius:5px; font-size:10px; font-weight:700; padding:3px 6px;"
        )
        if theme == "light":
            self.msg_lbl.setStyleSheet("color:#334155; font-size:12px;")
            self.ts.setStyleSheet("color:#64748B; font-size:11px;")
        else:
            self.msg_lbl.setStyleSheet("color:#CBD5E1; font-size:12px;")
            self.ts.setStyleSheet("color:#475569; font-size:11px;")


class AlertsPage(QWidget):
    """Full alerts page with scrollable list."""

    MAX_ALERTS = 80

    alerts_read = pyqtSignal()
    alerts_cleared = pyqtSignal()

    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._db = db
        self._app_state = app_state
        self._alert_items: list[AlertItem] = []
        self._build_ui()
        self._load_from_db()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        title = QLabel("Alerts")
        title.setObjectName("SectionHeader")
        hdr.addWidget(title)
        hdr.addStretch()

        self._count_lbl = QLabel("0 alerts")
        self._count_lbl.setStyleSheet("color:#F59E0B; font-size:12px; font-weight:600;")
        hdr.addWidget(self._count_lbl)

        clear_btn = QPushButton("Mark All Read")
        clear_btn.setFixedWidth(130)
        clear_btn.clicked.connect(self._mark_read)
        hdr.addWidget(clear_btn)

        delete_btn = QPushButton("Clear Alerts")
        delete_btn.setFixedWidth(110)
        delete_btn.clicked.connect(self._clear_alerts)
        hdr.addWidget(delete_btn)

        layout.addLayout(hdr)

        sub = QLabel("Network events and anomaly detections")
        sub.setObjectName("SectionSubtitle")
        layout.addWidget(sub)

        # Scroll area for alert items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        self._scroll_container = QWidget()
        scroll.setWidget(self._scroll_container)

        self._alerts_layout = QVBoxLayout(self._scroll_container)
        self._alerts_layout.setContentsMargins(0, 0, 0, 0)
        self._alerts_layout.setSpacing(8)
        self._alerts_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._empty_label = QLabel("No alerts yet — network looks clean ✓")
        self._empty_label.setStyleSheet("color:#475569; font-size:13px; padding:20px;")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._alerts_layout.addWidget(self._empty_label)

    # ─── Data ─────────────────────────────────────────────────────────────────

    def _load_from_db(self) -> None:
        try:
            rows = self._db.get_all_alerts(limit=self.MAX_ALERTS)
            for row in reversed(list(rows)):
                ts = row["created_at"][:19].replace("T", " ")
                self._prepend_alert(row["alert_type"], row["message"], ts)
        except Exception as exc:
            logger.error("Failed to load alerts from DB: %s", exc)

    @pyqtSlot(dict)
    def add_alert(self, payload: dict) -> None:
        """Called by DemoWorker signal when a new alert fires."""
        now = datetime.now().strftime("%H:%M:%S")
        self._prepend_alert(payload.get("type", "info"), payload.get("message", ""), now)

    def _prepend_alert(self, alert_type: str, message: str, timestamp: str) -> None:
        try:
            self._empty_label.setVisible(False)
        except RuntimeError:
            pass

        theme = self._app_state.current_theme if (self._app_state and hasattr(self._app_state, "current_theme")) else "dark"
        item = AlertItem(alert_type, message, timestamp, theme=theme)
        self._alerts_layout.insertWidget(0, item)
        self._alert_items.insert(0, item)

        # Prune old items
        while len(self._alert_items) > self.MAX_ALERTS:
            old = self._alert_items.pop()
            self._alerts_layout.removeWidget(old)
            old.deleteLater()

        self._count_lbl.setText(f"{len(self._alert_items)} alerts")

    def _mark_read(self) -> None:
        try:
            self._db.mark_alerts_read()
        except Exception:
            pass
        self._count_lbl.setText("0 unread")
        if self._app_state:
            self._app_state.set_alert_count(0)
        self.alerts_read.emit()

    def _clear_alerts(self) -> None:
        try:
            self._db.clear_all_alerts()
        except Exception:
            pass
        
        while self._alert_items:
            old = self._alert_items.pop()
            self._alerts_layout.removeWidget(old)
            old.deleteLater()
            
        try:
            self._empty_label.setVisible(True)
        except RuntimeError:
            pass
            
        self._count_lbl.setText("0 unread")
        if self._app_state:
            self._app_state.set_alert_count(0)
        self.alerts_cleared.emit()

    def update_theme(self, theme: str) -> None:
        """Propagates visual theme changes down to all child AlertItems and updates page alerts list labels."""
        if theme == "light":
            self._count_lbl.setStyleSheet("color:#D97706; font-size:12px; font-weight:600;")
            self._empty_label.setStyleSheet("color:#64748B; font-size:13px; padding:20px;")
        else:
            self._count_lbl.setStyleSheet("color:#F59E0B; font-size:12px; font-weight:600;")
            self._empty_label.setStyleSheet("color:#475569; font-size:13px; padding:20px;")

        for item in self._alert_items:
            item.update_theme(theme)
