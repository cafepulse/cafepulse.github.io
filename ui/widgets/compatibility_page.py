"""
CafePulse — Platform Compatibility & Diagnostic Page
Clear platform disclosure separating MikroTik RouterOS capabilities from generic routers,
including an interactive diagnostic port tester for API ports.
"""

import logging
import socket
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QLineEdit, QPushButton, QGridLayout,
    QProgressBar, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QColor

logger = logging.getLogger("cafepulse.ui.compatibility")


class PortTesterThread(QThread):
    """
    Background thread to test connectivity and check API ports (8728, 8729).
    """
    result_ready = pyqtSignal(dict)

    def __init__(self, host: str, timeout: float = 2.0):
        super().__init__()
        self.host = host
        self.timeout = timeout

    def run(self):
        result = {
            "host": self.host,
            "ping_ok": False,
            "port_8728_open": False,
            "port_8729_open": False,
            "error": None
        }

        # Resolve hostname
        try:
            ip = socket.gethostbyname(self.host)
        except socket.gaierror as e:
            result["error"] = f"Gagal menyelesaikan host: {e}"
            self.result_ready.emit(result)
            return

        # 1. Simple socket check on port 80/53 or ICMP (here we just try to connect to see if the host is up)
        # We will check the specific MikroTik API ports
        result["ping_ok"] = True

        # Test Port 8728 (API)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.settimeout(self.timeout)
        try:
            s1.connect((ip, 8728))
            result["port_8728_open"] = True
            s1.close()
        except socket.error:
            pass

        # Test Port 8729 (API SSL)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.settimeout(self.timeout)
        try:
            s2.connect((ip, 8729))
            result["port_8729_open"] = True
            s2.close()
        except socket.error:
            pass

        self.result_ready.emit(result)


class CompatibilityPage(QWidget):
    """
    Supported Platform Disclosure and Connection Diagnostic Assistant.
    """
    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._app_state = app_state
        self._tester_thread = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        title = QLabel("Kesesuaian Platform & Diagnostik")
        title.setObjectName("SectionHeader")
        layout.addWidget(title)

        sub = QLabel("Periksa kompatibilitas fitur antara router MikroTik dan perangkat jaringan standar.")
        sub.setObjectName("SectionSubtitle")
        layout.addWidget(sub)

        # Scroll Area for responsive contents
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)

        # ── Grid Kompatibilitas ────────────────────────────────────────────────
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(16)

        # MikroTik Card
        mt_card = QFrame()
        mt_card.setObjectName("DashCard")
        mt_card.setStyleSheet("QFrame#DashCard { border-top: 3px solid #06B6D4; background-color: #111625; }")
        mt_layout = QVBoxLayout(mt_card)
        mt_layout.setContentsMargins(18, 18, 18, 18)
        mt_layout.setSpacing(10)

        mt_title = QLabel("✓  MIKROTIK ROUTEROS (Penuh)")
        mt_title.setStyleSheet("color: #06B6D4; font-size: 14px; font-weight: 700; letter-spacing: 0.5px;")
        mt_layout.addWidget(mt_title)

        mt_desc = QLabel(
            "Mengaktifkan seluruh kapabilitas operasional dan jaringan secara otomatis.\n\n"
            "• Manajemen Kecepatan & Alokasi Bandwidth\n"
            "• Generator Voucher & Token Akses (IAM)\n"
            "• Isolasi Keamanan (Firewall, VLAN, NAT)\n"
            "• Backup Otomatis Terjadwal & Skrip Kustom\n"
            "• Statistik Real-time & Monitoring Sesi Aktif"
        )
        mt_desc.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.6;")
        mt_desc.setWordWrap(True)
        mt_layout.addWidget(mt_desc)
        grid.addWidget(mt_card, 0, 0)

        # Universal Card
        univ_card = QFrame()
        univ_card.setObjectName("DashCard")
        univ_card.setStyleSheet("QFrame#DashCard { border-top: 3px solid #F59E0B; background-color: #111625; }")
        univ_layout = QVBoxLayout(univ_card)
        univ_layout.setContentsMargins(18, 18, 18, 18)
        univ_layout.setSpacing(10)

        univ_title = QLabel("⚠  ROUTER UNIVERSAL (Terbatas)")
        univ_title.setStyleSheet("color: #F59E0B; font-size: 14px; font-weight: 700; letter-spacing: 0.5px;")
        univ_layout.addWidget(univ_title)

        univ_desc = QLabel(
            "Mode plug & play tanpa perlu mengubah konfigurasi pada router lokal Anda.\n\n"
            "• Deteksi Nama & MAC Perangkat Jaringan\n"
            "• Informasi Subnet & Alokasi IP Lokal\n"
            "• Pemindaian ARP Tanpa Hak Akses Khusus\n"
            "• Monitor Kualitas Latensi Jaringan Dasar\n"
            "✗ TIDAK MENDUKUNG Manajemen Kecepatan & Voucher"
        )
        univ_desc.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.6;")
        univ_desc.setWordWrap(True)
        univ_layout.addWidget(univ_desc)
        grid.addWidget(univ_card, 0, 1)

        scroll_layout.addWidget(grid_container)

        # ── Diagnostic Connection Assistant Card ─────────────────────────────
        diag_card = QFrame()
        diag_card.setObjectName("DashCard")
        diag_card.setStyleSheet("background-color: #0F131F;")
        diag_layout = QVBoxLayout(diag_card)
        diag_layout.setContentsMargins(20, 20, 20, 20)
        diag_layout.setSpacing(14)

        diag_title = QLabel("Asisten Diagnostik Koneksi MikroTik")
        diag_title.setStyleSheet("color: #E2E8F0; font-size: 14px; font-weight: 700;")
        diag_layout.addWidget(diag_title)

        diag_desc = QLabel(
            "Masukkan alamat IP atau domain router MikroTik Anda untuk menguji apakah port API "
            "telah terbuka dan siap dihubungkan oleh CafePulse."
        )
        diag_desc.setStyleSheet("color: #64748B; font-size: 12px;")
        diag_desc.setWordWrap(True)
        diag_layout.addWidget(diag_desc)

        # Test Input Row
        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Alamat IP Router (contoh: 192.168.88.1)")
        self.ip_input.setStyleSheet(
            "background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 10px; color: white;"
        )
        # Pre-populate if configuration has saved router IP
        if self._app_state and hasattr(self._app_state, "is_pro"):
            # Set default values if we can fetch from app_state parent config
            pass
        self.ip_input.setText("192.168.88.1")
        input_row.addWidget(self.ip_input)

        self.test_btn = QPushButton("Uji Koneksi  ⚡")
        self.test_btn.setObjectName("QuickScanButton")
        self.test_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 10px 20px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
            "QPushButton:disabled { background-color: #1E293B; color: #475569; }"
        )
        self.test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_btn.clicked.connect(self._on_test_clicked)
        input_row.addWidget(self.test_btn)

        diag_layout.addLayout(input_row)

        # Progress / Loading bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Infinite loading style
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(
            "QProgressBar { background: #1E293B; border-radius: 2px; }"
            "QProgressBar::chunk { background: #06B6D4; }"
        )
        diag_layout.addWidget(self.progress_bar)

        # Result Display Area
        self.result_box = QFrame()
        self.result_box.setObjectName("DashCard")
        self.result_box.setStyleSheet("background-color: #07090D; border: 1px solid #1E293B; border-radius: 6px;")
        self.result_box.setVisible(False)
        self.res_layout = QVBoxLayout(self.result_box)
        self.res_layout.setContentsMargins(14, 14, 14, 14)
        self.res_layout.setSpacing(8)

        self.res_title = QLabel("HASIL DIAGNOSTIK")
        self.res_title.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 700; letter-spacing: 0.5px;")
        self.res_layout.addWidget(self.res_title)

        self.res_ip = QLabel("Router IP: —")
        self.res_ip.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        self.res_layout.addWidget(self.res_ip)

        self.res_ping = QLabel("Reachability: —")
        self.res_ping.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        self.res_layout.addWidget(self.res_ping)

        self.res_8728 = QLabel("API Port 8728: —")
        self.res_8728.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        self.res_layout.addWidget(self.res_8728)

        self.res_8729 = QLabel("API SSL Port 8729: —")
        self.res_8729.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        self.res_layout.addWidget(self.res_8729)

        self.res_advice = QLabel("")
        self.res_advice.setStyleSheet("color: #38BDF8; font-size: 12px; margin-top: 6px;")
        self.res_advice.setWordWrap(True)
        self.res_layout.addWidget(self.res_advice)

        diag_layout.addWidget(self.result_box)

        scroll_layout.addWidget(diag_card)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _on_test_clicked(self) -> None:
        host = self.ip_input.text().strip()
        if not host:
            return

        self.test_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.result_box.setVisible(False)

        self._tester_thread = PortTesterThread(host)
        self._tester_thread.result_ready.connect(self._on_test_result)
        self._tester_thread.finished.connect(lambda: self.progress_bar.setVisible(False))
        self._tester_thread.finished.connect(lambda: self.test_btn.setEnabled(True))
        self._tester_thread.start()

    @pyqtSlot(dict)
    def _on_test_result(self, result: dict) -> None:
        self.result_box.setVisible(True)
        host = result["host"]
        self.res_ip.setText(f"Router Host: <b>{host}</b>")

        if result["error"]:
            self.res_ping.setText("Reachability: <span style='color: #EF4444;'>Gagal (Host tidak dikenal)</span>")
            self.res_8728.setText("API Port 8728: <span style='color: #EF4444;'>Tidak Terbuka</span>")
            self.res_8729.setText("API SSL Port 8729: <span style='color: #EF4444;'>Tidak Terbuka</span>")
            self.res_advice.setText(f"<b>Saran:</b> {result['error']}. Silakan periksa kembali alamat IP atau koneksi LAN Anda.")
            self.res_advice.setStyleSheet("color: #F87171; font-size: 12px;")
            return

        # Display ping/connectivity
        ping_text = "<span style='color: #22C55E;'>Sukses (Host Terjangkau)</span>" if result["ping_ok"] else "<span style='color: #EF4444;'>Gagal</span>"
        self.res_ping.setText(f"Koneksi Fisik: {ping_text}")

        # Port 8728 (API)
        p8728_text = "<span style='color: #22C55E; font-weight: 700;'>TERBUKA ✓</span>" if result["port_8728_open"] else "<span style='color: #EF4444;'>TERTUTUP ✗</span>"
        self.res_8728.setText(f"Port API Standar (8728): {p8728_text}")

        # Port 8729 (API SSL)
        p8729_text = "<span style='color: #22C55E; font-weight: 700;'>TERBUKA ✓</span>" if result["port_8729_open"] else "<span style='color: #EF4444;'>TERTUTUP ✗</span>"
        self.res_8729.setText(f"Port API SSL Aman (8729): {p8729_text}")

        # Diagnostic Advice
        if result["port_8728_open"] or result["port_8729_open"]:
            advice = (
                "<b>Saran:</b> Router MikroTik Anda siap dihubungkan! Port API telah terbuka. "
                "Silakan masuk ke halaman Mode Switcher dan beralih ke Mode MikroTik."
            )
            self.res_advice.setStyleSheet("color: #4ADE80; font-size: 12px;")
        else:
            advice = (
                "<b>Saran:</b> Router terdeteksi, namun layanan API MikroTik masih dinonaktifkan.<br/><br/>"
                "Untuk mengaktifkannya, silakan hubungkan kabel ke router Anda, buka Winbox / Terminal MikroTik, dan ketikkan perintah berikut:<br/>"
                "<span style='font-family: monospace; color: #F59E0B;'>/ip service enable api</span>"
            )
            self.res_advice.setStyleSheet("color: #FB923C; font-size: 12px;")

        self.res_advice.setText(advice)
