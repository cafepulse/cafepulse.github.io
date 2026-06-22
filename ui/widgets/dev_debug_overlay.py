"""
CafePulse — Developer Observability & Debug Overlay
A lightweight, transparent glassmorphism panel displaying real-time metrics
of connection state, worker thread lifecycles, and polling queues.
"""

import time
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
from PyQt6.QtCore import Qt, QTimer

logger = logging.getLogger("cafepulse.ui.devoverlay")


class DevDebugOverlay(QFrame):
    """
    Premium real-time observability panel overlay.
    Triggered with Ctrl+Shift+D. PyQt6 native and 100% non-blocking.
    """
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setObjectName("DevDebugOverlay")
        
        # Sci-Fi glassmorphism theme styling matching CafePulse cyber dark theme
        self.setStyleSheet("""
            QFrame#DevDebugOverlay {
                background-color: rgba(15, 23, 42, 0.96);
                border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 12px;
            }
            QLabel {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                color: #94A3B8;
                border: none;
                background: transparent;
            }
            QLabel#DebugTitle {
                font-size: 13px;
                font-weight: bold;
                color: #38BDF8;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#SectionHeader {
                font-size: 10px;
                font-weight: bold;
                color: #38BDF8;
                margin-top: 6px;
                margin-bottom: 2px;
                border-bottom: 1px solid rgba(56, 189, 248, 0.15);
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#MetricName {
                color: #64748B;
                font-weight: bold;
            }
            QLabel#MetricValue {
                color: #F8FAFC;
            }
            QFrame#TerminalContainer {
                background-color: rgba(2, 6, 23, 0.85);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 6px;
            }
            QLabel#HistoryTerminal {
                color: #38BDF8;
                font-family: 'Consolas', monospace;
                font-size: 9px;
            }
        """)
        
        self.setFixedWidth(340)
        self.setFixedHeight(540)
        
        self._build_ui()
        
        # Observer update timer (updates every 500ms)
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(500)
        self.update_timer.timeout.connect(self.refresh_metrics)
        self.update_timer.start()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)
        
        # Header title
        title = QLabel("💻 CafePulse Dev Observability")
        title.setObjectName("DebugTitle")
        layout.addWidget(title)
        
        self.metrics = {}
        
        # Group 1: Core System
        g1_hdr = QLabel("SYSTEM & LIFECYCLE")
        g1_hdr.setObjectName("SectionHeader")
        layout.addWidget(g1_hdr)
        
        self._add_row(layout, "Active Mode", "mode")
        self._add_row(layout, "Worker Thread Status", "worker_status")
        self._add_row(layout, "Watchdog Latency (UI)", "watchdog")
        self._add_row(layout, "Active Worker Threads", "active_workers")
        
        # Group 2: MikroTik Connection Details
        g2_hdr = QLabel("MIKROTIK METRICS & STATE")
        g2_hdr.setObjectName("SectionHeader")
        layout.addWidget(g2_hdr)
        
        self._add_row(layout, "Selected WAN Interface", "selected_interface")
        self._add_row(layout, "Connection State", "state")
        self._add_row(layout, "API Auth Status", "api_auth")
        self._add_row(layout, "Interface Monitor Status", "interface_monitor")
        self._add_row(layout, "Successful API Commands", "success_cmds")
        self._add_row(layout, "Failed API Commands", "failed_cmds")
        self._add_row(layout, "Fast Poll Schedule", "fast_poll_timer")
        self._add_row(layout, "Watchdog QTimer", "watchdog_qtimer")
        self._add_row(layout, "Tick Count / Polling", "ticks")
        self._add_row(layout, "Auto-Reconnects Count", "reconnects")
        
        # Group 3: Diagnostics
        g3_hdr = QLabel("DIAGNOSTICS & TELEMETRY")
        g3_hdr.setObjectName("SectionHeader")
        layout.addWidget(g3_hdr)
        
        self._add_row(layout, "Last Reconnect Reason", "reconnect_reason")
        self._add_row(layout, "Last Pipeline Error", "last_exception")
        
        # Group 4: Transition Terminal
        g4_hdr = QLabel("STATE TRANSITION HISTORY")
        g4_hdr.setObjectName("SectionHeader")
        layout.addWidget(g4_hdr)
        
        term_frame = QFrame()
        term_frame.setObjectName("TerminalContainer")
        term_layout = QVBoxLayout(term_frame)
        term_layout.setContentsMargins(8, 8, 8, 8)
        
        self.terminal = QLabel("No transitions logged.")
        self.terminal.setObjectName("HistoryTerminal")
        self.terminal.setWordWrap(True)
        self.terminal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        term_layout.addWidget(self.terminal)
        layout.addWidget(term_frame)
        
        layout.addStretch()

    def _add_row(self, parent_layout: QVBoxLayout, display_name: str, key: str) -> None:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_name = QLabel(display_name)
        lbl_name.setObjectName("MetricName")
        
        lbl_val = QLabel("-")
        lbl_val.setObjectName("MetricValue")
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        row_layout.addWidget(lbl_name)
        row_layout.addWidget(lbl_val)
        parent_layout.addWidget(row)
        
        self.metrics[key] = lbl_val

    def refresh_metrics(self) -> None:
        """Queries and refreshes connection metrics synchronously from QThreads."""
        mw = self.main_window
        now = time.time()
        
        # Mode
        self.metrics["mode"].setText(mw._current_mode.upper())
        
        # Determine active background worker
        worker = None
        if mw._current_mode == "demo" and mw._demo_worker:
            worker = mw._demo_worker
        elif mw._current_mode == "home_wifi" and mw._wifi_worker:
            worker = mw._wifi_worker
        elif mw._current_mode == "hotspot" and mw._hotspot_worker:
            worker = mw._hotspot_worker
        elif mw._current_mode == "mikrotik" and mw._mikrotik_worker:
            worker = mw._mikrotik_worker
            
        # Worker Status
        if worker and worker.isRunning():
            self.metrics["worker_status"].setText("ALIVE")
            self.metrics["worker_status"].setStyleSheet("color: #22C55E; font-weight: bold;")
        else:
            self.metrics["worker_status"].setText("DEAD")
            self.metrics["worker_status"].setStyleSheet("color: #EF4444; font-weight: bold;")
            
        # Count total running threads
        active_count = 0
        for attr in ("_demo_worker", "_wifi_worker", "_hotspot_worker", "_mikrotik_worker"):
            w = getattr(mw, attr, None)
            if w and w.isRunning():
                active_count += 1
        self.metrics["active_workers"].setText(str(active_count))
        
        # Watchdog Latency (heartbeat interval check)
        wd_age = now - mw._last_heartbeat
        self.metrics["watchdog"].setText(f"{wd_age:.1f}s ago")
        if wd_age > 15.0:
            self.metrics["watchdog"].setStyleSheet("color: #EF4444; font-weight: bold;")
        else:
            self.metrics["watchdog"].setStyleSheet("color: #22C55E;")
            
        # Watchdog QTimer remainingTime()
        rem_wd = mw._watchdog_timer.remainingTime()
        if mw._watchdog_timer.isActive() and rem_wd >= 0:
            self.metrics["watchdog_qtimer"].setText(f"ACTIVE ({rem_wd / 1000.0:.1f}s rem)")
            self.metrics["watchdog_qtimer"].setStyleSheet("color: #22C55E;")
        else:
            self.metrics["watchdog_qtimer"].setText("INACTIVE")
            self.metrics["watchdog_qtimer"].setStyleSheet("color: #EF4444;")

        # Specific MikroTik State values
        if mw._current_mode == "mikrotik" and mw._mikrotik_worker:
            mt_w = mw._mikrotik_worker
            manager = mt_w.manager
            
            # Selected interface
            self.metrics["selected_interface"].setText(str(mt_w._wan_interface))
            self.metrics["selected_interface"].setStyleSheet("color: #F59E0B; font-weight: bold;")
            
            # API Auth status
            auth_status = str(manager.api_auth_status)
            self.metrics["api_auth"].setText(auth_status)
            if auth_status == "SUCCESS":
                self.metrics["api_auth"].setStyleSheet("color: #22C55E; font-weight: bold;")
            elif auth_status == "FAILED":
                self.metrics["api_auth"].setStyleSheet("color: #EF4444; font-weight: bold;")
            else:
                self.metrics["api_auth"].setStyleSheet("color: #38BDF8; font-weight: bold;")
                
            # Interface monitor status
            mon_status = str(mt_w.monitor_status)
            self.metrics["interface_monitor"].setText(mon_status)
            if mon_status == "OK":
                self.metrics["interface_monitor"].setStyleSheet("color: #22C55E; font-weight: bold;")
            elif mon_status == "ERROR":
                self.metrics["interface_monitor"].setStyleSheet("color: #EF4444; font-weight: bold;")
            else:
                self.metrics["interface_monitor"].setStyleSheet("color: #64748B;")
                
            # API Command metrics
            self.metrics["success_cmds"].setText(str(manager.successful_api_commands))
            self.metrics["failed_cmds"].setText(str(manager.failed_api_commands))
            
            # Remaining time till next fast poll
            time_since_fast = now - mt_w.last_fast_poll
            next_fast_in = max(0.0, 2.0 - time_since_fast)
            polling_active = manager.state in ("CONNECTED", "DEGRADED", "RECOVERED")
            if polling_active and mt_w.last_fast_poll > 0:
                self.metrics["fast_poll_timer"].setText(f"ACTIVE ({next_fast_in:.1f}s)")
                self.metrics["fast_poll_timer"].setStyleSheet("color: #22C55E;")
            else:
                self.metrics["fast_poll_timer"].setText("PAUSED")
                self.metrics["fast_poll_timer"].setStyleSheet("color: #EF4444;")
            
            # State machine state
            state = manager.state
            self.metrics["state"].setText(state)
            state_colors = {
                "CONNECTED": "#22C55E",
                "RECOVERED": "#10B981",
                "CONNECTING": "#38BDF8",
                "RECONNECTING": "#F59E0B",
                "DEGRADED": "#EAB308",
                "FAILED": "#EF4444"
            }
            self.metrics["state"].setStyleSheet(f"color: {state_colors.get(state, '#94A3B8')}; font-weight: bold;")
            
            # Tick count
            self.metrics["ticks"].setText(f"{mt_w._tick_count} (Active: {polling_active})")
            
            # Reconnect count
            self.metrics["reconnects"].setText(str(manager.reconnect_count))
            
            # Diagnostics exceptions & reasons
            reconnect_reason = manager.last_reconnect_reason
            if len(reconnect_reason) > 26:
                reconnect_reason = reconnect_reason[:23] + "..."
            self.metrics["reconnect_reason"].setText(reconnect_reason)
            self.metrics["reconnect_reason"].setToolTip(manager.last_reconnect_reason)
            
            last_err = manager.last_exception
            if len(last_err) > 26:
                last_err = last_err[:23] + "..."
            self.metrics["last_exception"].setText(last_err)
            self.metrics["last_exception"].setToolTip(manager.last_exception)
            if manager.last_exception != "None":
                self.metrics["last_exception"].setStyleSheet("color: #EF4444;")
            else:
                self.metrics["last_exception"].setStyleSheet("color: #94A3B8;")
                
            # History log terminal
            if manager.state_history:
                # Show last 5 transitions
                log_lines = manager.state_history[-5:]
                self.terminal.setText("\n".join(log_lines))
            else:
                self.terminal.setText("No transitions logged.")
                
        else:
            self.metrics["selected_interface"].setText("N/A")
            self.metrics["state"].setText("N/A")
            self.metrics["api_auth"].setText("N/A")
            self.metrics["interface_monitor"].setText("N/A")
            self.metrics["success_cmds"].setText("0")
            self.metrics["failed_cmds"].setText("0")
            self.metrics["fast_poll_timer"].setText("INACTIVE")
            self.metrics["ticks"].setText("0 (Active: FALSE)")
            self.metrics["reconnects"].setText("0")
            self.metrics["reconnect_reason"].setText("None")
            self.metrics["last_exception"].setText("None")
            self.metrics["selected_interface"].setStyleSheet("color: #64748B;")
            self.metrics["state"].setStyleSheet("color: #64748B;")
            self.metrics["api_auth"].setStyleSheet("color: #64748B;")
            self.metrics["interface_monitor"].setStyleSheet("color: #64748B;")
            self.metrics["fast_poll_timer"].setStyleSheet("color: #64748B;")
            self.metrics["last_exception"].setStyleSheet("color: #94A3B8;")
            self.terminal.setText("No active MikroTik connection.")
            
    def show_floating(self, parent_widget: QWidget) -> None:
        """Mounts and positions the debug panel on top of the parent window."""
        self.setParent(parent_widget)
        self.show()
        self.raise_()
        self._reposition()
        
    def _reposition(self) -> None:
        if self.parentWidget():
            p_size = self.parentWidget().size()
            # Align top-right with 20px padding
            self.move(p_size.width() - self.width() - 20, 20)
            
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._reposition()
