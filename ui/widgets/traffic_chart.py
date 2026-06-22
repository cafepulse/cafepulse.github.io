"""
CafePulse — Real-Time Traffic Chart
PyQtGraph PlotWidget with rolling upload/download curves.
No matplotlib — pyqtgraph only (as spec requires).
"""

import logging

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor

logger = logging.getLogger("cafepulse.ui.chart")

# ─── PyQtGraph global config ──────────────────────────────────────────────────
pg.setConfigOptions(antialias=True, background="#161B27", foreground="#475569")

HISTORY_LEN = 60  # data points shown (60 × 2s = 2 minutes of history)


class TrafficChart(QWidget):
    """
    Real-time upload/download line chart.
    Call push(upload_mbps, download_mbps) to add a data point.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setMinimumHeight(220)

        self.MAX_POINTS = 300
        self._upload_buf   = [0.0] * self.MAX_POINTS
        self._download_buf = [0.0] * self.MAX_POINTS
        self._x = list(range(self.MAX_POINTS))

        self._build_ui()

    # ─── Build ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        # Header row
        header_row = QHBoxLayout()
        title = QLabel("REAL-TIME TRAFFIC")
        title.setObjectName("DashCardTitle")
        header_row.addWidget(title)

        header_row.addStretch()

        # Legend
        self._legend_dots = []
        self._legend_labels = []
        for label, color in [("↑ Upload", "#F59E0B"), ("↓ Download", "#38BDF8")]:
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 10px;")
            self._legend_dots.append(dot)
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #64748B; font-size: 11px;")
            self._legend_labels.append(lbl)
            header_row.addWidget(dot)
            header_row.addWidget(lbl)
            header_row.addSpacing(12)

        layout.addLayout(header_row)

        # PyQtGraph plot
        self._plot_widget = pg.PlotWidget()
        self._plot_widget.setBackground("#161B27")
        self._plot_widget.getPlotItem().hideAxis("bottom")
        self._plot_widget.getPlotItem().getAxis("left").setTextPen("#475569")
        self._plot_widget.getPlotItem().getAxis("left").setPen("#1E2535")
        self._plot_widget.showGrid(x=False, y=True, alpha=0.15)
        self._plot_widget.setMouseEnabled(x=False, y=False)
        self._plot_widget.setMenuEnabled(False)
        self._plot_widget.setLabel("left", "Mbps", color="#475569", size="10pt")
        self._plot_widget.getPlotItem().setContentsMargins(0, 0, 0, 0)
        self._plot_widget.setMinimumHeight(150)

        # Curves
        self._upload_curve = self._plot_widget.plot(
            self._x, list(self._upload_buf),
            pen=pg.mkPen(color="#F59E0B", width=2),
            fillLevel=0,
            brush=pg.mkBrush(QColor(245, 158, 11, 30)),
            name="Upload",
        )
        self._download_curve = self._plot_widget.plot(
            self._x, list(self._download_buf),
            pen=pg.mkPen(color="#38BDF8", width=2),
            fillLevel=0,
            brush=pg.mkBrush(QColor(56, 189, 248, 30)),
            name="Download",
        )

        layout.addWidget(self._plot_widget)

        # Stats row
        stats_row = QHBoxLayout()
        self._upload_label   = QLabel("↑  0.00 Mbps")
        self._download_label = QLabel("↓  0.00 Mbps")
        self._total_label    = QLabel("Total: 0.00 Mbps")

        for lbl, color in [
            (self._upload_label, "#F59E0B"),
            (self._download_label, "#38BDF8"),
            (self._total_label, "#94A3B8"),
        ]:
            lbl.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600;")
            stats_row.addWidget(lbl)
            stats_row.addSpacing(20)

        stats_row.addStretch()
        layout.addLayout(stats_row)

    def update_theme(self, theme: str) -> None:
        """Dynamically style the PyQtGraph plotting canvas and standard labels."""
        if theme == "light":
            bg_color = "#FFFFFF"
            axis_color = "#E2E8F0"
            text_color = "#475569"
            grid_alpha = 0.15
            up_color = "#D97706"  # Amber 600
            dn_color = "#0284C7"  # Sky 600
            up_brush = QColor(217, 119, 6, 20)
            dn_brush = QColor(2, 132, 199, 20)

            self._upload_label.setStyleSheet("color: #D97706; font-size: 12px; font-weight: 600;")
            self._download_label.setStyleSheet("color: #0284C7; font-size: 12px; font-weight: 600;")
            self._total_label.setStyleSheet("color: #475569; font-size: 12px; font-weight: 600;")
        else:
            bg_color = "#161B27"
            axis_color = "#1E2535"
            text_color = "#94A3B8"
            grid_alpha = 0.15
            up_color = "#F59E0B"
            dn_color = "#38BDF8"
            up_brush = QColor(245, 158, 11, 30)
            dn_brush = QColor(56, 189, 248, 30)

            self._upload_label.setStyleSheet("color: #F59E0B; font-size: 12px; font-weight: 600;")
            self._download_label.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: 600;")
            self._total_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")

        self._plot_widget.setBackground(bg_color)
        self._plot_widget.getPlotItem().getAxis("left").setTextPen(text_color)
        self._plot_widget.getPlotItem().getAxis("left").setPen(axis_color)
        self._plot_widget.showGrid(x=False, y=True, alpha=grid_alpha)
        self._plot_widget.setLabel("left", "Mbps", color=text_color, size="10pt")

        self._upload_curve.setPen(pg.mkPen(color=up_color, width=2))
        self._upload_curve.setBrush(pg.mkBrush(up_brush))
        self._download_curve.setPen(pg.mkPen(color=dn_color, width=2))
        self._download_curve.setBrush(pg.mkBrush(dn_brush))

        # Legenda adaptif
        self._legend_dots[0].setStyleSheet(f"color: {up_color}; font-size: 10px;")
        self._legend_dots[1].setStyleSheet(f"color: {dn_color}; font-size: 10px;")
        for lbl in self._legend_labels:
            lbl.setStyleSheet(f"color: {text_color}; font-size: 11px;")

    # ─── Data Ingestion ───────────────────────────────────────────────────────

    def push(self, upload_mbps: float, download_mbps: float) -> None:
        """Add one data point and refresh the chart. Call from main thread only."""
        self._upload_buf.append(upload_mbps)
        self._download_buf.append(download_mbps)

        # Enforce memory bounds via strict slicing
        self._upload_buf = self._upload_buf[-self.MAX_POINTS:]
        self._download_buf = self._download_buf[-self.MAX_POINTS:]

        y_up   = self._upload_buf
        y_down = self._download_buf

        self._upload_curve.setData(self._x, y_up)
        self._download_curve.setData(self._x, y_down)

        # Auto-scale Y with headroom
        max_val = max(max(y_up), max(y_down), 1.0)
        self._plot_widget.setYRange(0, max_val * 1.15, padding=0)

        # Update labels
        self._upload_label.setText(f"↑  {upload_mbps:.2f} Mbps")
        self._download_label.setText(f"↓  {download_mbps:.2f} Mbps")
        self._total_label.setText(f"Total: {upload_mbps + download_mbps:.2f} Mbps")

    def reset(self) -> None:
        """Resets chart buffers and clears all curves."""
        self._upload_buf = [0.0] * self.MAX_POINTS
        self._download_buf = [0.0] * self.MAX_POINTS
        self._upload_curve.setData(self._x, self._upload_buf)
        self._download_curve.setData(self._x, self._download_buf)
        self._plot_widget.setYRange(0, 1.0, padding=0)
        self._upload_label.setText("↑  0.00 Mbps")
        self._download_label.setText("↓  0.00 Mbps")
        self._total_label.setText("Total: 0.00 Mbps")
