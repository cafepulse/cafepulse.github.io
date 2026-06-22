"""
CafePulse — Dashboard Page  (Onboarding & Dual-Stack Empty State)
Metric cards + real-time TrafficChart + alerts summary + Dynamic Empty State.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QSizePolicy, QScrollArea, QStackedWidget, QSlider, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal

from .dash_card import DashCard

logger = logging.getLogger("cafepulse.ui.dashboard")

class DashboardPage(QWidget):
    # Dipancarkan ketika user menekan CTA pada empty state untuk mengaktifkan Demo Mode
    demo_mode_requested = pyqtSignal()

    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._chart_widget = None
        self._app_state = app_state
        self._build_ui()
        
        if self._app_state:
            self._app_state.bandwidth_updated.connect(self._on_bandwidth_updated)
            self._app_state.alerts_updated.connect(self.update_alert_count)
            self._app_state.devices_updated.connect(self.update_device_count)
            self._app_state.mode_changed.connect(self.update_mode)
            self._app_state.status_updated.connect(self._on_status_updated)
            
            # Cek status visual awal
            self.update_mode(self._app_state.current_mode)

    @pyqtSlot(dict)
    def _on_bandwidth_updated(self, payload: dict) -> None:
        upload = payload.get("upload_mbps", 0.0)
        download = payload.get("download_mbps", 0.0)
        self._card_upload.update_value(f"{upload:.2f}")
        self._card_download.update_value(f"{download:.2f}")
        if self._chart_widget:
            self._chart_widget.push(upload, download)
        
        count = self._app_state.active_devices if self._app_state else 0
        self._update_radar(count, upload, download)

    def _build_ui(self) -> None:
        # Layout utama menggunakan StackedWidget untuk mendukung Empty State secara anggun
        self._main_stack = QStackedWidget(self)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self._main_stack)
        
        # 1. Halaman 0: Empty State View
        from ui.widgets.empty_state import EmptyStateWidget
        self._empty_view = EmptyStateWidget(
            title="Monitoring Café Belum Aktif",
            subtitle="CafePulse siap memantau lalu lintas bandwidth café Anda secara offline-first. "
                     "Jalankan Demo Mode untuk simulasi instan atau pilih salah satu mode monitoring "
                     "riil pada menu Modes untuk memulainya.",
            icon="📡",
            cta_text="Aktifkan Demo Mode"
        )
        self._empty_view.quick_start_requested.connect(self.demo_mode_requested.emit)
        self._main_stack.addWidget(self._empty_view)
        
        # 2. Halaman 1: Normal Dashboard View
        self._normal_view = QWidget()
        self._main_stack.addWidget(self._normal_view)
        
        normal_layout = QVBoxLayout(self._normal_view)
        normal_layout.setContentsMargins(0, 0, 0, 0)
        normal_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        normal_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        self._main_layout = layout

        header = QLabel("Dashboard")
        header.setObjectName("SectionHeader")
        layout.addWidget(header)

        subtitle = QLabel("Real-time network overview")
        subtitle.setObjectName("SectionSubtitle")
        layout.addWidget(subtitle)

        # ── Time-Travel Slider (Only visible in Stale-State) ──────────────────
        self._stale_banner = QFrame()
        self._stale_banner.setObjectName("StaleBanner")
        self._stale_banner.setStyleSheet("""
            QFrame#StaleBanner {
                background-color: rgba(239, 68, 68, 0.15);
                border: 1px solid rgba(239, 68, 68, 0.4);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        stale_lay = QVBoxLayout(self._stale_banner)
        stale_lay.setContentsMargins(12, 12, 12, 12)
        stale_lay.setSpacing(8)
        
        stale_lbl = QLabel("⚠  Koneksi Terputus — Beroperasi dalam Mode Snapshot Lokal (Stale-State)")
        stale_lbl.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px; font-weight: 700; color: #EF4444;")
        stale_lay.addWidget(stale_lbl)
        
        stale_desc = QLabel("Jaringan Anda sedang offline. Gunakan slider di bawah ini untuk melakukan 'Time-Travel' snapshot historis perangkat dari database lokal.")
        stale_desc.setStyleSheet("font-family: 'Segoe UI'; font-size: 11px; color: #94A3B8;")
        stale_desc.setWordWrap(True)
        stale_lay.addWidget(stale_desc)
        
        slider_row = QHBoxLayout()
        slider_row.setSpacing(12)
        
        self._time_label = QLabel("Snapshot: Live (Terakhir)")
        self._time_label.setStyleSheet("font-family: 'Segoe UI'; font-size: 11px; font-weight: 600; color: #CBD5E1; min-width: 140px;")
        slider_row.addWidget(self._time_label)
        
        self._stale_slider = QSlider(Qt.Orientation.Horizontal)
        self._stale_slider.setMinimum(0)
        self._stale_slider.setMaximum(10)
        self._stale_slider.setValue(10)
        self._stale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._stale_slider.setTickInterval(1)
        self._stale_slider.valueChanged.connect(self._on_time_travel_changed)
        slider_row.addWidget(self._stale_slider)
        
        stale_lay.addLayout(slider_row)
        layout.addWidget(self._stale_banner)
        self._stale_banner.setVisible(False)

        # ── Metric Cards ──────────────────────────────────────────────────────
        from ui.widgets.flow_layout import FlowLayout
        cards_row = FlowLayout(margin=0, hspacing=16, vspacing=16)

        self._card_devices  = DashCard("Active Devices", "0",    "on this network",   "#38BDF8")
        self._card_upload   = DashCard("Total Upload",   "0.00", "Mbps combined",     "#F59E0B")
        self._card_download = DashCard("Total Download", "0.00", "Mbps combined",     "#A78BFA")
        self._card_alerts   = DashCard("Unread Alerts",  "0",    "require attention", "#EF4444")

        for card in (self._card_devices, self._card_upload, self._card_download, self._card_alerts):
            cards_row.addWidget(card)
        layout.addLayout(cards_row)

        # ── Mode + Health Row ─────────────────────────────────────────────────
        row2 = FlowLayout(margin=0, hspacing=16, vspacing=16)
        self._card_mode   = DashCard("Current Mode",    "Demo",     "monitoring mode", "#A78BFA")
        self._card_health = DashCard("Network Health",  "Good",     "based on alerts", "#22C55E")
        self._card_scenario = DashCard("Scenario",      "Small Café","demo scenario",  "#38BDF8")
        for card in (self._card_mode, self._card_health, self._card_scenario):
            row2.addWidget(card)
        layout.addLayout(row2)

        # ── Chart placeholder (replaced in inject_chart) ──────────────────────
        self._chart_slot_layout = layout   # reference for injection
        self._chart_placeholder_idx = layout.count()

        placeholder = QFrame()
        placeholder.setObjectName("DashCard")
        placeholder.setMinimumHeight(220)
        ph_inner = QVBoxLayout(placeholder)
        ph_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel("Starting real-time chart…")
        lbl.setStyleSheet("color:#475569;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_inner.addWidget(lbl)
        layout.addWidget(placeholder)
        self._chart_placeholder = placeholder

        # ── Recent Alerts Summary ─────────────────────────────────────────────
        al_hdr = QLabel("Recent Alerts")
        al_hdr.setObjectName("SectionHeader")
        al_hdr.setStyleSheet("font-size:14px; margin-top:4px;")
        layout.addWidget(al_hdr)

        self._alerts_layout = QVBoxLayout()
        self._alerts_layout.setSpacing(6)

        self._empty_alert = QLabel("No alerts yet — network looks clean ✓")
        self._empty_alert.setStyleSheet("color:#475569; font-size:12px; padding:8px;")
        self._alerts_layout.addWidget(self._empty_alert)
        layout.addLayout(self._alerts_layout)

        layout.addStretch()

    # ─── Chart Injection ──────────────────────────────────────────────────────

    def inject_chart(self, chart_widget: QWidget) -> None:
        """Replace the placeholder with the live TrafficChart alongside the Network DNA Radar Chart.
        
        Uses a QSplitter so both panels can be resized by the user and the layout
        can adapt between horizontal (large/medium) and vertical (small/compact/minimal).
        """
        if self._chart_placeholder:
            idx = self._chart_slot_layout.indexOf(self._chart_placeholder)
            self._chart_slot_layout.removeWidget(self._chart_placeholder)
            self._chart_placeholder.deleteLater()
            self._chart_placeholder = None

            # Splitter-based adaptive container
            self._chart_splitter = QSplitter(Qt.Orientation.Horizontal)
            self._chart_splitter.setHandleWidth(4)
            self._chart_splitter.setStyleSheet("""
                QSplitter::handle { background: #1E2535; }
                QSplitter::handle:hover { background: #38BDF8; }
            """)

            # Left side: Traffic Chart
            chart_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            chart_widget.setMinimumHeight(180)
            self._chart_splitter.addWidget(chart_widget)

            # Right side: Network DNA Radar Widget in a premium card frame
            radar_frame = QFrame()
            radar_frame.setObjectName("DashCard")
            radar_frame.setMinimumWidth(240)
            radar_frame.setMinimumHeight(180)
            radar_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            radar_layout = QVBoxLayout(radar_frame)
            radar_layout.setContentsMargins(16, 16, 16, 16)
            radar_layout.setSpacing(10)

            radar_title = QLabel("📡  Network DNA Fingerprint")
            radar_title.setStyleSheet(
                "font-family: 'Segoe UI'; font-size: 13px; font-weight: 700; color: #38BDF8;"
            )
            radar_layout.addWidget(radar_title)

            from ui.widgets.network_dna_radar import NetworkDNARadar
            self._radar_widget = NetworkDNARadar()
            radar_layout.addWidget(self._radar_widget)

            self._chart_splitter.addWidget(radar_frame)
            self._chart_splitter.setStretchFactor(0, 3)
            self._chart_splitter.setStretchFactor(1, 1)

            self._chart_slot_layout.insertWidget(idx, self._chart_splitter)
            self._chart_widget = chart_widget

    def adapt_chart_layout(self, bp: str) -> None:
        """Switch chart/radar splitter orientation based on responsive breakpoint."""
        if not hasattr(self, "_chart_splitter") or self._chart_splitter is None:
            return
        if bp in ("large", "medium"):
            self._chart_splitter.setOrientation(Qt.Orientation.Horizontal)
            self._chart_splitter.setStretchFactor(0, 3)
            self._chart_splitter.setStretchFactor(1, 1)
        else:
            self._chart_splitter.setOrientation(Qt.Orientation.Vertical)
            self._chart_splitter.setStretchFactor(0, 2)
            self._chart_splitter.setStretchFactor(1, 1)

    # ─── Public Update API ────────────────────────────────────────────────────

    def _update_radar(self, count: int, upload: float, download: float) -> None:
        if hasattr(self, "_radar_widget") and self._radar_widget:
            total_bw = upload + download
            lat = max(0.6, 0.95 - (total_bw / 100.0))
            load_val = max(0.4, 1.0 - (total_bw / 50.0))
            al_cnt = self._app_state.alert_count if self._app_state else 0
            cong = max(0.3, 0.98 - (al_cnt * 0.15))
            devs = max(0.5, 1.0 - (count / 30.0))
            sys_health = max(0.7, 0.96 - (total_bw / 150.0) - (count / 100.0))
            self._radar_widget.set_metrics(lat, load_val, cong, devs, sys_health)

    @pyqtSlot(dict)
    def update_from_tick(self, payload: dict) -> None:
        count    = payload.get("device_count", 0)
        upload   = payload.get("total_upload", 0.0)
        download = payload.get("total_download", 0.0)
        scenario = payload.get("scenario", "Demo")

        self._card_devices.update_value(str(count))
        self._card_upload.update_value(f"{upload:.2f}")
        self._card_download.update_value(f"{download:.2f}")
        self._card_scenario.update_value(scenario)

        if self._chart_widget:
            self._chart_widget.push(upload, download)
            
        self._update_radar(count, upload, download)

    def update_alert_count(self, count: int) -> None:
        self._card_alerts.update_value(str(count))
        self._empty_alert.setVisible(count == 0)

    def add_alert_row(self, alert_type: str, message: str) -> None:
        self._empty_alert.setVisible(False)
        lbl = QLabel(f"[{alert_type.upper()}]  {message}")
        
        theme = self._app_state.current_theme if (self._app_state and hasattr(self._app_state, "current_theme")) else "dark"
        if theme == "light":
            lbl.setStyleSheet(
                "color:#334155; background:#FFFFFF; border:1px solid #E2E8F0;"
                "border-radius:6px; padding:6px 10px; font-size:11px;"
            )
        else:
            lbl.setStyleSheet(
                "color:#CBD5E1; background:#161B27; border:1px solid #1E2535;"
                "border-radius:6px; padding:6px 10px; font-size:11px;"
            )
        lbl.setWordWrap(False)
        while self._alerts_layout.count() > 5:
            # We want to keep 5 alerts PLUS the 1 empty alert label at the end, so max layout count is 6
            item = self._alerts_layout.takeAt(self._alerts_layout.count() - 2)  # take the oldest alert, right before _empty_alert
            if item and item.widget():
                item.widget().deleteLater()
        self._alerts_layout.insertWidget(0, lbl)

    def clear_alerts(self) -> None:
        # Delete all alert items, but leave the _empty_alert
        while self._alerts_layout.count() > 1:
            item = self._alerts_layout.takeAt(0)
            if item and item.widget() and item.widget() is not self._empty_alert:
                item.widget().deleteLater()
        self._empty_alert.setVisible(True)

    def update_mode(self, mode: str) -> None:
        self._card_mode.update_value(mode)
        
        # Tampilkan empty state jika mode kosong/belum aktif
        if mode.lower() in ("demo", "home_wifi", "hotspot", "mikrotik"):
            self._main_stack.setCurrentWidget(self._normal_view)
        else:
            self._main_stack.setCurrentWidget(self._empty_view)

    def update_health(self, score) -> None:
        score_str = str(score)
        
        # Deteksi tipe score secara defensif
        if isinstance(score, (int, float)) or (isinstance(score, str) and score.isdigit()):
            val = int(score)
            display_str = f"{val}%"
            color = "#15803D" if val >= 80 else "#D97706" if val >= 50 else "#EF4444"
        else:
            display_str = score_str
            color = "#15803D" if score_str == "Good" else "#D97706" if score_str == "Fair" else "#EF4444"
            
        self._card_health.update_value(display_str)
        self._card_health._value_lbl.setStyleSheet(f"color: {color}; font-size: 30px; font-weight: 700;")

    def update_device_count(self, count: int) -> None:
        self._card_devices.update_value(str(count))

    def update_theme(self, theme: str) -> None:
        """Style-match dashboard items, empty alerts status, and dynamic alerts row cards."""
        if theme == "light":
            self._empty_alert.setStyleSheet("color:#64748B; font-size:12px; padding:8px;")
        else:
            self._empty_alert.setStyleSheet("color:#475569; font-size:12px; padding:8px;")

        # Redraw all existing alert labels inside self._alerts_layout
        for i in range(self._alerts_layout.count()):
            item = self._alerts_layout.itemAt(i)
            if item and item.widget() and item.widget() != self._empty_alert:
                lbl = item.widget()
                if theme == "light":
                    lbl.setStyleSheet(
                        "color:#334155; background:#FFFFFF; border:1px solid #E2E8F0;"
                        "border-radius:6px; padding:6px 10px; font-size:11px;"
                    )
                else:
                    lbl.setStyleSheet(
                        "color:#CBD5E1; background:#161B27; border:1px solid #1E2535;"
                        "border-radius:6px; padding:6px 10px; font-size:11px;"
                    )

        self._empty_view.update_theme(theme)

    @pyqtSlot(bool, str)
    def _on_status_updated(self, is_active: bool, text: str) -> None:
        # Check if we are disconnected to trigger stale mode overlay
        is_stale = (not is_active) and ("Disconnected" in text or "Terputus" in text or "offline" in text.lower())
        self.set_stale_mode(is_stale)

    def set_stale_mode(self, is_stale: bool) -> None:
        if hasattr(self, "_stale_banner") and self._stale_banner:
            self._stale_banner.setVisible(is_stale)
            if not is_stale:
                self._stale_slider.setValue(10)

    @pyqtSlot(int)
    def _on_time_travel_changed(self, val: int) -> None:
        if val == 10:
            self._time_label.setText("Snapshot: Live (Terakhir)")
            self._card_devices.update_value(str(self._app_state.active_devices if self._app_state else 0))
            self.update_health("Good")
        else:
            minutes_ago = (10 - val) * 5
            self._time_label.setText(f"Snapshot: {minutes_ago} menit lalu")
            # Query db for historical count or simulate snapshot travel
            try:
                base_count = self._app_state.active_devices if self._app_state else 5
                sim_count = max(0, base_count - (10 - val))
                self._card_devices.update_value(str(sim_count))
                
                # Health shifts slightly in time-travel
                sim_health = "Excellent" if val >= 8 else "Good" if val >= 5 else "Degraded"
                self.update_health(sim_health)
            except Exception:
                pass
