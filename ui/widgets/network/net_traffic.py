"""
CafePulse — Traffic & Monitoring Page (Phase 10)
Provides real-time pyqtgraph curves, download/upload monitors, and read-only traffic loads.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
import pyqtgraph as pg
from ui.widgets.dash_card import DashCard


class NetTraffic(QWidget):
    """
    Dedicated, read-only Traffic Inspection and Monitoring Dashboard.
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

        # ── KPI Cards (Read Only) ─────────────────────────────────────────────
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(12)

        self.card_rx = DashCard("RX Traffic (Download)", "0.0 Mbps", "standard bandwidth", "#22C55E")
        self.card_tx = DashCard("TX Traffic (Upload)", "0.0 Mbps", "standard bandwidth", "#38BDF8")
        self.card_load = DashCard("Total Link Load", "Low", "utilization index", "#F59E0B")

        kpi_row.addWidget(self.card_rx)
        kpi_row.addWidget(self.card_tx)
        kpi_row.addWidget(self.card_load)
        layout.addLayout(kpi_row)

        # ── Real-time Traffic Graph ───────────────────────────────────────────
        graph_card = QFrame()
        graph_card.setObjectName("DashCard")
        graph_layout = QVBoxLayout(graph_card)
        graph_layout.setContentsMargins(12, 12, 12, 12)

        self.chart = pg.PlotWidget(title="Live Link Utilization Graph")
        self.chart.setBackground("#0F131E")
        self.chart.showGrid(x=True, y=True, alpha=0.15)
        self.chart.setLabel('left', 'Speed', units='Mbps')
        
        self.time_data = []
        self.rx_data = []
        self.tx_data = []
        self.rx_curve = self.chart.plot(pen=pg.mkPen(color='#22C55E', width=2), name="Download (RX)")
        self.tx_curve = self.chart.plot(pen=pg.mkPen(color='#38BDF8', width=2), name="Upload (TX)")
        
        graph_layout.addWidget(self.chart)
        layout.addWidget(graph_card, stretch=2)

        # ── Visual warning block ──────────────────────────────────────────────
        notice = QFrame()
        notice.setObjectName("DashCard")
        notice.setStyleSheet("QFrame#DashCard { border-left: 3px solid #06B6D4; background-color: #0F1420; }")
        notice_layout = QVBoxLayout(notice)
        notice_layout.setContentsMargins(12, 8, 12, 8)
        
        lbl = QLabel(
            "ℹ  Halaman ini bersifat <b>Read-Only (Hanya Baca)</b>. Anda tidak dapat melakukan "
            "perubahan konfigurasi port atau batas kecepatan di sini untuk mencegah gangguan jaringan."
        )
        lbl.setStyleSheet("color: #64748B; font-size: 11px;")
        notice_layout.addWidget(lbl)
        layout.addWidget(notice)

    def update_ticks(self, payload: dict) -> None:
        """Called dynamically from main window ticks to update live curves."""
        rx = float(payload.get("rx_speed_mbps", payload.get("download_mbps", 0.0)))
        tx = float(payload.get("tx_speed_mbps", payload.get("upload_mbps", 0.0)))

        self.card_rx.set_value(f"{rx:.1f} Mbps")
        self.card_tx.set_value(f"{tx:.1f} Mbps")

        total = rx + tx
        load = "Low" if total < 5.0 else ("Moderate" if total < 20.0 else "High (Saturated)")
        self.card_load.set_value(load)

        # Update Pyqtgraph curves
        self.time_data.append(len(self.time_data))
        self.rx_data.append(rx)
        self.tx_data.append(tx)

        if len(self.time_data) > 60:
            self.time_data.pop(0)
            self.rx_data.pop(0)
            self.tx_data.pop(0)

        self.rx_curve.setData(self.time_data, self.rx_data)
        self.tx_curve.setData(self.time_data, self.tx_data)
