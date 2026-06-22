import logging
import sqlite3
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QPushButton, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
import pyqtgraph as pg

from ui.widgets.empty_state import EmptyStateWidget

logger = logging.getLogger(__name__)

class StatCard(QFrame):
    def __init__(self, title, initial_value, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #161B27; border: 1px solid #1E2535; border-radius: 8px; padding: 12px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(200)
        self.setMinimumHeight(80)
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: bold; font-family: 'Segoe UI';")
        
        self.val_label = QLabel(str(initial_value))
        self.val_label.setStyleSheet("color: #F8FAFC; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.val_label)

    def set_value(self, value):
        self.val_label.setText(str(value))

    def update_theme(self, theme: str) -> None:
        if theme == "light":
            self.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;")
            self.title_label.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold; font-family: 'Segoe UI';")
            self.val_label.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")
        else:
            self.setStyleSheet("background-color: #161B27; border: 1px solid #1E2535; border-radius: 8px; padding: 12px;")
            self.title_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: bold; font-family: 'Segoe UI';")
            self.val_label.setStyleSheet("color: #F8FAFC; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")


class AnalyticsPage(QWidget):
    demo_mode_requested = pyqtSignal()

    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self.db = db
        self._app_state = app_state
        self._build_ui()
        
        if self._app_state:
            self._app_state.mode_changed.connect(self.update_view)
            # Hubungkan juga ke state update umum dan update data realtime
            self._app_state.state_changed.connect(lambda: self.update_view(self._app_state.current_mode))
            self._app_state.bandwidth_updated.connect(lambda payload: self.load_data())
            self.update_view(self._app_state.current_mode)

    def _build_ui(self):
        # Layout utama menggunakan StackedWidget untuk mendukung Empty State
        self._main_stack = QStackedWidget(self)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self._main_stack)
        
        # 1. Halaman 0: Empty State View
        self._empty_view = EmptyStateWidget(
            title="Belum Ada Riwayat Analitik",
            subtitle="Halaman analitik menyajikan tren lalu lintas bandwidth dari database lokal. "
                     "Lakukan pemantauan riil di menu Modes atau aktifkan Demo Mode untuk melihat grafik histografis simulasi café.",
            icon="📊",
            cta_text="Aktifkan Demo Mode"
        )
        self._empty_view.quick_start_requested.connect(self.demo_mode_requested.emit)
        self._main_stack.addWidget(self._empty_view)
        
        # 2. Halaman 1: Normal Analytics View
        self._normal_view = QWidget()
        self._main_stack.addWidget(self._normal_view)
        
        layout = QVBoxLayout(self._normal_view)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Header
        header_layout = QHBoxLayout()
        self.title_lbl = QLabel("Traffic Analytics")
        self.title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #F8FAFC; font-family: 'Segoe UI';")
        
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E2535; 
                border: 1px solid #2D3748;
                color: #F1F5F9; 
                padding: 6px 16px; 
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2D3748;
                border-color: #3B82F6;
            }
        """)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.load_data)

        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        layout.addLayout(header_layout)

        # Cards — using FlowLayout for adaptive wrapping across all breakpoints
        from ui.widgets.flow_layout import FlowLayout
        cards_flow = FlowLayout(margin=0, hspacing=12, vspacing=12)
        self.card_total_devices = StatCard("Total Unique Devices", "0")
        self.card_total_sessions = StatCard("Total Sessions", "0")
        self.card_avg_duration = StatCard("Avg Session Duration", "0 min")
        
        cards_flow.addWidget(self.card_total_devices)
        cards_flow.addWidget(self.card_total_sessions)
        cards_flow.addWidget(self.card_avg_duration)
        layout.addLayout(cards_flow)

        # Chart
        self.chart = pg.PlotWidget(title="Historical Traffic (Last 24 Hours)")
        self.chart.setBackground("#161B27")
        self.chart.showGrid(x=True, y=True, alpha=0.3)
        self.chart.setLabel('left', 'Mbps')
        
        self.rx_curve = self.chart.plot(pen=pg.mkPen(color='#10B981', width=2), name="Download")
        self.tx_curve = self.chart.plot(pen=pg.mkPen(color='#3B82F6', width=2), name="Upload")
        
        layout.addWidget(self.chart, stretch=1)

        # AI Insights Panel
        self._insight_frame = QFrame()
        self._insight_frame.setObjectName("DashCard")
        self._insight_frame.setStyleSheet("""
            QFrame#DashCard {
                background-color: #161B27;
                border: 1px solid #1E2535;
                border-radius: 8px;
                padding: 14px;
            }
        """)
        ins_layout = QVBoxLayout(self._insight_frame)
        ins_layout.setContentsMargins(14, 14, 14, 14)
        ins_layout.setSpacing(8)
        
        ins_header = QLabel("🤖  AI-Powered Local Business Insights")
        ins_header.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px; font-weight: 700; color: #F59E0B;")
        ins_layout.addWidget(ins_header)
        
        self._insights_container = QVBoxLayout()
        self._insights_container.setSpacing(6)
        ins_layout.addLayout(self._insights_container)
        
        layout.addWidget(self._insight_frame)
        
        # Load initial data
        self.load_data()

    def update_view(self, mode: str):
        # Tampilkan normal view jika mode adalah salah satu mode monitoring aktif
        if mode.lower() in ("demo", "home_wifi", "hotspot", "mikrotik"):
            self._main_stack.setCurrentWidget(self._normal_view)
            self.load_data()
        else:
            self._main_stack.setCurrentWidget(self._empty_view)

    def load_data(self):
        if not self.db or not self.db._conn:
            return
            
        try:
            cursor = self.db._conn.cursor()
            
            # Total unique devices
            cursor.execute("SELECT COUNT(id) FROM devices")
            row = cursor.fetchone()
            if row:
                self.card_total_devices.set_value(row[0])

            # Total sessions
            cursor.execute("SELECT COUNT(id) FROM sessions")
            row = cursor.fetchone()
            if row:
                self.card_total_sessions.set_value(row[0])

            # Average session duration (in minutes) for closed sessions
            cursor.execute("SELECT session_start, session_end FROM sessions WHERE session_end IS NOT NULL")
            sessions = cursor.fetchall()
            
            total_minutes = 0
            count = 0
            for start_str, end_str in sessions:
                try:
                    fmt = "%Y-%m-%d %H:%M:%S"
                    start = datetime.strptime(start_str[:19], fmt)
                    end = datetime.strptime(end_str[:19], fmt)
                    diff = (end - start).total_seconds() / 60
                    if diff >= 0:
                        total_minutes += diff
                        count += 1
                except ValueError:
                    continue
                    
            if count > 0:
                self.card_avg_duration.set_value(f"{int(total_minutes / count)} min")
            else:
                self.card_avg_duration.set_value("N/A")
                
            # Traffic logs (chronological)
            cursor.execute("SELECT timestamp, upload_speed, download_speed FROM traffic_logs ORDER BY timestamp DESC LIMIT 100")
            rows = cursor.fetchall()
            rows.reverse() # chronological
            
            if rows:
                rx_data = [r[2] for r in rows]
                tx_data = [r[1] for r in rows]
                time_data = list(range(len(rows)))
                self.rx_curve.setData(time_data, rx_data)
                self.tx_curve.setData(time_data, tx_data)
            else:
                self.rx_curve.setData([])
                self.tx_curve.setData([])

            # RENDER INSIGHTS
            self._render_ai_insights()

        except sqlite3.Error as e:
            logger.error(f"Failed to load analytics: {e}")

    def _render_ai_insights(self) -> None:
        if not hasattr(self, "_insights_container") or not self._insights_container:
            return
            
        # Clear container
        while self._insights_container.count() > 0:
            item = self._insights_container.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
                
        insights = []
        try:
            cursor = self.db._conn.cursor()
            
            # 1. Peak Hour analysis
            cursor.execute("SELECT strftime('%H', session_start) as hr, COUNT(*) as cnt FROM sessions GROUP BY hr ORDER BY cnt DESC LIMIT 1")
            row = cursor.fetchone()
            if row and row[0]:
                hr = int(row[0])
                insights.append(f"💡 <b>Puncak Kunjungan Kafe:</b> Pelanggan paling aktif terlihat pada pukul {hr:02d}:00 - {(hr+1)%24:02d}:00. Disarankan untuk memprioritaskan bandwidth kasir pada jam ini.")
            else:
                insights.append("💡 <b>Puncak Kunjungan Kafe:</b> Jam sibuk akan terdeteksi setelah lebih banyak data sesi terkumpul.")

            # 2. Frequent Reconnection analysis
            cursor.execute("SELECT device_id, COUNT(*) as cnt FROM sessions GROUP BY device_id HAVING cnt >= 5")
            frequent_users = cursor.fetchall()
            if frequent_users:
                insights.append(f"⚠️ <b>Anomali Sinyal:</b> Ada {len(frequent_users)} perangkat terputus-nyambung (>5 sesi). Ini dapat mengindikasikan sinyal WiFi lemah di beberapa titik kafe Anda.")
            else:
                insights.append("✓ <b>Stabilitas Sinyal:</b> Jaringan sangat stabil. Tidak ada perangkat yang mengalami putus-nyambung berlebihan hari ini.")

            # 3. Retensi Pelanggan Setia (BI Insight)
            cursor.execute("SELECT device_id, COUNT(*) as cnt FROM sessions GROUP BY device_id HAVING cnt >= 10")
            loyal_users = cursor.fetchall()
            if loyal_users:
                insights.append(f"⭐ <b>Loyalitas Pengunjung:</b> Ada {len(loyal_users)} pelanggan setia berkunjung >10 kali. Pertimbangkan memberikan voucher khusus untuk meningkatkan retensi!")
            else:
                insights.append("⭐ <b>Loyalitas Pengunjung:</b> Data loyalitas pelanggan akan terakumulasi seiring waktu pemakaian.")

            # 4. Keamanan
            cursor.execute("SELECT COUNT(*) FROM devices WHERE first_seen >= date('now')")
            new_today = cursor.fetchone()
            if new_today and new_today[0] > 0:
                insights.append(f"🔒 <b>Keamanan Jaringan:</b> Terdeteksi {new_today[0]} perangkat baru hari ini. Selalu awasi alert perangkat baru untuk mencegah penyusup.")

        except Exception as e:
            logger.error("AI Insight computation failed: %s", e)
            insights = ["💡 Mengumpulkan data lalu lintas jaringan untuk menghasilkan analisis bisnis lokal..."]

        theme = self._app_state.current_theme if (self._app_state and hasattr(self._app_state, "current_theme")) else "dark"
        for ins in insights:
            lbl = QLabel(ins)
            lbl.setStyleSheet(f"""
                font-family: 'Segoe UI';
                font-size: 11px;
                color: {"#334155" if theme == "light" else "#CBD5E1"};
                background-color: {"#F8FAFC" if theme == "light" else "#1E2535"};
                border-radius: 6px;
                padding: 10px 14px;
                border-left: 4px solid #F59E0B;
            """)
            lbl.setWordWrap(True)
            self._insights_container.addWidget(lbl)

    def update_theme(self, theme: str) -> None:
        """Dynamically style the PyQtGraph plotting canvas, cards, empty state, and refresh button."""
        if theme == "light":
            bg_color = "#FFFFFF"
            axis_color = "#E2E8F0"
            text_color = "#475569"
            grid_alpha = 0.15
            rx_color = "#059669"  # Emerald 600
            tx_color = "#0284C7"  # Sky 600

            self.title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #0F172A; font-family: 'Segoe UI';")
            self.refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F1F5F9; 
                    border: 1px solid #CBD5E1;
                    color: #334155; 
                    padding: 6px 16px; 
                    border-radius: 6px;
                    font-family: 'Segoe UI';
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #0284C7;
                    color: #0F172A;
                }
            """)
        else:
            bg_color = "#161B27"
            axis_color = "#1E2535"
            text_color = "#94A3B8"
            grid_alpha = 0.3
            rx_color = "#10B981"
            tx_color = "#3B82F6"

            self.title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #F8FAFC; font-family: 'Segoe UI';")
            self.refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E2535; 
                    border: 1px solid #2D3748;
                    color: #F1F5F9; 
                    padding: 6px 16px; 
                    border-radius: 6px;
                    font-family: 'Segoe UI';
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2D3748;
                    border-color: #3B82F6;
                }
            """)

        self.chart.setBackground(bg_color)
        self.chart.getPlotItem().getAxis("left").setTextPen(text_color)
        self.chart.getPlotItem().getAxis("left").setPen(axis_color)
        self.chart.getPlotItem().getAxis("bottom").setTextPen(text_color)
        self.chart.getPlotItem().getAxis("bottom").setPen(axis_color)
        self.chart.showGrid(x=True, y=True, alpha=grid_alpha)

        self.rx_curve.setPen(pg.mkPen(color=rx_color, width=2))
        self.tx_curve.setPen(pg.mkPen(color=tx_color, width=2))

        # Propagate to empty state & stat cards
        self._empty_view.update_theme(theme)
        self.card_total_devices.update_theme(theme)
        self.card_total_sessions.update_theme(theme)
        self.card_avg_duration.update_theme(theme)
        
        if hasattr(self, "_insight_frame") and self._insight_frame:
            if theme == "light":
                self._insight_frame.setStyleSheet("""
                    QFrame#DashCard {
                        background-color: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 8px;
                        padding: 14px;
                    }
                """)
            else:
                self._insight_frame.setStyleSheet("""
                    QFrame#DashCard {
                        background-color: #161B27;
                        border: 1px solid #1E2535;
                        border-radius: 8px;
                        padding: 14px;
                    }
                """)
            self._render_ai_insights()
