"""
CafePulse — IAM Dashboard Sub-View
Displays KPIs (Total Vouchers, Active Sessions, Total Packages) and real-time active hosts list.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor


class IamDashCard(QFrame):
    """Modern HSL KPI card for IAM dashboard."""
    def __init__(self, title: str, val: str, border_color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setStyleSheet(f"QFrame#DashCard {{ border-left: 3px solid {border_color}; background-color: #111625; }}")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        
        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;")
        layout.addWidget(self.title_lbl)
        
        self.val_lbl = QLabel(val)
        self.val_lbl.setStyleSheet("color: #E2E8F0; font-size: 20px; font-weight: 700;")
        layout.addWidget(self.val_lbl)

    def set_value(self, v: str) -> None:
        self.val_lbl.setText(v)


class IamDashboard(QWidget):
    """
    Landing sub-view of the IAM Module.
    """
    def __init__(self, db, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ── KPI Cards Grid ────────────────────────────────────────────────────
        kpi_container = QWidget()
        kpi_layout = QGridLayout(kpi_container)
        kpi_layout.setContentsMargins(0, 0, 0, 0)
        kpi_layout.setSpacing(12)

        self.card_active = IamDashCard("Sesi Aktif (Live)", "0 online", "#22C55E")
        self.card_vouchers = IamDashCard("Total Voucher Terbit", "0 token", "#06B6D4")
        self.card_packages = IamDashCard("Total Paket Akses", "0 paket", "#A78BFA")

        kpi_layout.addWidget(self.card_active, 0, 0)
        kpi_layout.addWidget(self.card_vouchers, 0, 1)
        kpi_layout.addWidget(self.card_packages, 0, 2)
        layout.addWidget(kpi_container)

        # ── Active Sessions Section ───────────────────────────────────────────
        sess_frame = QFrame()
        sess_frame.setObjectName("DashCard")
        sess_layout = QVBoxLayout(sess_frame)
        sess_layout.setContentsMargins(16, 14, 16, 14)
        sess_layout.setSpacing(10)

        sess_title = QLabel("Daftar Sesi Pengguna Aktif")
        sess_title.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 700;")
        sess_layout.addWidget(sess_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.sess_list_container = QWidget()
        self.sess_list_layout = QVBoxLayout(self.sess_list_container)
        self.sess_list_layout.setContentsMargins(0, 0, 0, 0)
        self.sess_list_layout.setSpacing(8)
        
        self.no_sess_lbl = QLabel("Tidak ada sesi aktif terdeteksi. Hubungkan MikroTik atau jalankan demo.")
        self.no_sess_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-style: italic; padding: 10px;")
        self.sess_list_layout.addWidget(self.no_sess_lbl)
        self.sess_list_layout.addStretch()

        scroll.setWidget(self.sess_list_container)
        sess_layout.addWidget(scroll)
        layout.addWidget(sess_frame)

        self.update_kpis()

    def update_kpis(self) -> None:
        """Fetch general stats from SQLite to update KPIs."""
        try:
            v_cnt = self._db.fetchone("SELECT COUNT(*) as cnt FROM vouchers")["cnt"]
            p_cnt = self._db.fetchone("SELECT COUNT(*) as cnt FROM access_packages")["cnt"]
            self.card_vouchers.set_value(f"{v_cnt} token")
            self.card_packages.set_value(f"{p_cnt} paket")
        except Exception:
            pass

    def update_active_sessions(self, active_hosts: list[dict]) -> None:
        """Dynamically repopulates the active sessions list."""
        # Clean previous items
        while self.sess_list_layout.count() > 0:
            item = self.sess_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not active_hosts:
            self.sess_list_layout.addWidget(self.no_sess_lbl)
            self.sess_list_layout.addStretch()
            self.card_active.set_value("0 online")
            return

        self.card_active.set_value(f"{len(active_hosts)} online")

        for host in active_hosts:
            row = QFrame()
            row.setStyleSheet("background-color: #07090D; border: 1px solid #1E293B; border-radius: 6px;")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 8, 12, 8)

            icon = QLabel("👤")
            icon.setStyleSheet("font-size: 16px;")
            row_layout.addWidget(icon)

            info = QVBoxLayout()
            name = QLabel(f"<b>{host.get('user', 'Unknown')}</b>")
            name.setStyleSheet("color: #E2E8F0; font-size: 12px;")
            info.addWidget(name)

            ip_mac = QLabel(f"IP: {host.get('address', '—')} | MAC: {host.get('mac-address', '—')}")
            ip_mac.setStyleSheet("color: #64748B; font-size: 10px;")
            info.addWidget(ip_mac)
            row_layout.addLayout(info)
            row_layout.addStretch()

            uptime = QLabel(host.get("uptime", "—"))
            uptime.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 600;")
            row_layout.addWidget(uptime)

            self.sess_list_layout.addWidget(row)

        self.sess_list_layout.addStretch()
        self.update_kpis()
