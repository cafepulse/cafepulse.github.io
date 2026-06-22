"""
CafePulse — Firewall & NAT Configuration Page (Phase 13)
Implements quick security toggles in Basic View and extensive tabular lists in Advanced View.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QCheckBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QLineEdit, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSlot


class NetFirewall(QWidget):
    """
    Firewall administration center supporting dynamic Basic/Advanced viewpoints.
    """
    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self._db = db
        self._app_state = app_state
        self._is_advanced_mode = False
        self._build_ui()
        self.load_firewall_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Header Row (Title + View Toggle)
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Dinding Api & Keamanan (Firewall)")
        title.setStyleSheet("color: #E2E8F0; font-size: 14px; font-weight: 700;")
        title_box.addWidget(title)
        header.addLayout(title_box)
        header.addStretch()

        self.toggle_btn = QPushButton("Tampilan: Dasar  ⚙️")
        self.toggle_btn.setStyleSheet(
            "QPushButton { background-color: #1E293B; color: #E2E8F0; font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self._toggle_view)
        header.addWidget(self.toggle_btn)
        layout.addLayout(header)

        # Stacked Layout: 0 = Basic View, 1 = Advanced View
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self._build_basic_view()
        self._build_advanced_view()
        self.stack.setCurrentIndex(0)

    # ─── Basic View (Stack 0) ─────────────────────────────────────────────────

    def _build_basic_view(self) -> None:
        basic_widget = QWidget()
        basic_layout = QVBoxLayout(basic_widget)
        basic_layout.setContentsMargins(0, 0, 0, 0)
        basic_layout.setSpacing(14)

        # Toggles card
        toggles_card = QFrame()
        toggles_card.setObjectName("DashCard")
        toggles_layout = QVBoxLayout(toggles_card)
        toggles_layout.setContentsMargins(16, 14, 16, 14)
        toggles_layout.setSpacing(10)

        toggles_title = QLabel("PENGATURAN KEAMANAN DASAR (QUICK TOGGLES)")
        toggles_title.setStyleSheet("color: #F59E0B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        toggles_layout.addWidget(toggles_title)

        self.chk_ping = QCheckBox("Blokir Ping / ICMP dari Internet WAN (Mencegah Scan Eksternal)")
        self.chk_ping.setChecked(True)
        self.chk_ping.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        toggles_layout.addWidget(self.chk_ping)

        self.chk_fasttrack = QCheckBox("Aktifkan FastTrack Connection Tracking (Menghemat Beban CPU)")
        self.chk_fasttrack.setChecked(True)
        self.chk_fasttrack.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        toggles_layout.addWidget(self.chk_fasttrack)

        self.chk_win = QCheckBox("Blokir Port Berbahaya Windows Sharing (Ports 139, 445)")
        self.chk_win.setChecked(True)
        self.chk_win.setStyleSheet("color: #E2E8F0; font-size: 12px;")
        toggles_layout.addWidget(self.chk_win)

        self.apply_basic_btn = QPushButton("Terapkan Proteksi  ✓")
        self.apply_basic_btn.setStyleSheet(
            "QPushButton { background-color: #0284C7; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #0369A1; }"
        )
        self.apply_basic_btn.clicked.connect(self._on_apply_basic)
        toggles_layout.addWidget(self.apply_basic_btn)

        basic_layout.addWidget(toggles_card)

        # Port forwarding form
        pf_card = QFrame()
        pf_card.setObjectName("DashCard")
        pf_layout = QVBoxLayout(pf_card)
        pf_layout.setContentsMargins(16, 14, 16, 14)
        pf_layout.setSpacing(10)

        pf_title = QLabel("PORT FORWARDING SEDERHANA (NAT Dst-Nat)")
        pf_title.setStyleSheet("color: #06B6D4; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        pf_layout.addWidget(pf_title)

        inputs = QFormLayout()
        inputs.setSpacing(8)

        self.pub_port = QLineEdit()
        self.pub_port.setPlaceholderText("Port luar WAN (contoh: 8080)")
        self.pub_port.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Public Port WAN:", self.pub_port)

        self.priv_ip = QLineEdit()
        self.priv_ip.setPlaceholderText("IP perangkat lokal (contoh: 192.168.88.24)")
        self.priv_ip.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Private IP Lokal:", self.priv_ip)

        self.priv_port = QLineEdit()
        self.priv_port.setPlaceholderText("Port perangkat lokal (contoh: 80)")
        self.priv_port.setStyleSheet("background-color: #07090D; border: 1px solid #1F293D; border-radius: 6px; padding: 6px; color: white;")
        inputs.addRow("Private Port Lokal:", self.priv_port)

        pf_layout.addLayout(inputs)

        self.pf_btn = QPushButton("Buat Port Forward  ✓")
        self.pf_btn.setStyleSheet(
            "QPushButton { background-color: #0891B2; color: white; padding: 8px 16px; font-weight: 600; border-radius: 6px; }"
            "QPushButton:hover { background-color: #06B6D4; }"
        )
        self.pf_btn.clicked.connect(self._on_pf_add)
        pf_layout.addWidget(self.pf_btn)

        basic_layout.addWidget(pf_card)
        basic_layout.addStretch()

        self.stack.addWidget(basic_widget)

    # ─── Advanced View (Stack 1) ──────────────────────────────────────────────

    def _build_advanced_view(self) -> None:
        adv_widget = QWidget()
        adv_layout = QVBoxLayout(adv_widget)
        adv_layout.setContentsMargins(0, 0, 0, 0)
        adv_layout.setSpacing(12)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #1E293B; background: transparent; border-radius: 8px; }"
            "QTabBar::tab { background: #0F131F; color: #64748B; padding: 8px 16px; font-weight: 600; border: 1px solid #1E293B; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px; }"
            "QTabBar::tab:selected { background: #1E293B; color: #06B6D4; border-bottom: 2px solid #06B6D4; }"
        )
        adv_layout.addWidget(self.tabs)

        # Tab 1: Filter Rules
        self.filter_table = QTableWidget(0, 5)
        self.filter_table.verticalHeader().setDefaultSectionSize(36)
        self.filter_table.setHorizontalHeaderLabels(["Chain", "Protocol", "Dst Port", "Action", "Comment"])
        self.filter_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.filter_table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        self.tabs.addTab(self.filter_table, "Filter Rules")

        # Tab 2: NAT
        self.nat_table = QTableWidget(0, 5)
        self.nat_table.verticalHeader().setDefaultSectionSize(36)
        self.nat_table.setHorizontalHeaderLabels(["Chain", "Dst IP / Port", "Action", "To IP / Port", "Comment"])
        self.nat_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.nat_table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        self.tabs.addTab(self.nat_table, "NAT Rules")

        # Tab 3: Mangle
        self.mangle_table = QTableWidget(0, 5)
        self.mangle_table.verticalHeader().setDefaultSectionSize(36)
        self.mangle_table.setHorizontalHeaderLabels(["Chain", "Protocol", "Action", "Mark Name", "Comment"])
        self.mangle_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mangle_table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        self.tabs.addTab(self.mangle_table, "Mangle Rules")

        # Tab 4: Address Lists
        self.addr_table = QTableWidget(0, 3)
        self.addr_table.verticalHeader().setDefaultSectionSize(36)
        self.addr_table.setHorizontalHeaderLabels(["List Name", "IP Address", "Timeout"])
        self.addr_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.addr_table.setStyleSheet(
            "QTableWidget { background-color: transparent; gridline-color: #1E293B; color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget::item:selected { background-color: #1E3A5F; color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QTableWidget QLineEdit, QTableView QLineEdit { background-color: #0B0F19; border: 1px solid #38BDF8; border-radius: 4px; padding: 2px 6px; margin: 0px; color: #F8FAFC; selection-background-color: #1E3A5F; selection-color: #38BDF8; }"
            "QHeaderView::section { background-color: #0F131F; color: #94A3B8; padding: 6px; border: none; font-weight: 700; }"
        )
        self.tabs.addTab(self.addr_table, "Address Lists")

        self.stack.addWidget(adv_widget)

    def _toggle_view(self) -> None:
        self._is_advanced_mode = not self._is_advanced_mode
        if self._is_advanced_mode:
            self.toggle_btn.setText("Tampilan: Lanjutan  🛠️")
            self.toggle_btn.setStyleSheet(
                "QPushButton { background-color: #0F172A; color: #06B6D4; font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 6px; border: 1px solid #06B6D4; }"
            )
            self.stack.setCurrentIndex(1)
        else:
            self.toggle_btn.setText("Tampilan: Dasar  ⚙️")
            self.toggle_btn.setStyleSheet(
                "QPushButton { background-color: #1E293B; color: #E2E8F0; font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }"
            )
            self.stack.setCurrentIndex(0)

    def load_firewall_data(self) -> None:
        # Load Filters
        self.filter_table.setRowCount(2)
        self.filter_table.setItem(0, 0, QTableWidgetItem("input"))
        self.filter_table.setItem(0, 1, QTableWidgetItem("icmp"))
        self.filter_table.setItem(0, 2, QTableWidgetItem("any"))
        self.filter_table.setItem(0, 3, QTableWidgetItem("drop"))
        self.filter_table.setItem(0, 4, QTableWidgetItem("Blokir Ping"))

        self.filter_table.setItem(1, 0, QTableWidgetItem("forward"))
        self.filter_table.setItem(1, 1, QTableWidgetItem("tcp"))
        self.filter_table.setItem(1, 2, QTableWidgetItem("139,445"))
        self.filter_table.setItem(1, 3, QTableWidgetItem("drop"))
        self.filter_table.setItem(1, 4, QTableWidgetItem("Blokir Windows Share"))

        # Load NAT
        self.nat_table.setRowCount(1)
        self.nat_table.setItem(0, 0, QTableWidgetItem("dstnat"))
        self.nat_table.setItem(0, 1, QTableWidgetItem("TCP / 8080"))
        self.nat_table.setItem(0, 2, QTableWidgetItem("dst-nat"))
        self.nat_table.setItem(0, 3, QTableWidgetItem("192.168.88.24 / 80"))
        self.nat_table.setItem(0, 4, QTableWidgetItem("Web Server forwarding"))

        # Load Mangle
        self.mangle_table.setRowCount(1)
        self.mangle_table.setItem(0, 0, QTableWidgetItem("prerouting"))
        self.mangle_table.setItem(0, 1, QTableWidgetItem("tcp"))
        self.mangle_table.setItem(0, 2, QTableWidgetItem("mark-connection"))
        self.mangle_table.setItem(0, 3, QTableWidgetItem("conn_http"))
        self.mangle_table.setItem(0, 4, QTableWidgetItem("Tandai koneksi HTTP"))

        # Load Address list
        self.addr_table.setRowCount(1)
        self.addr_table.setItem(0, 0, QTableWidgetItem("blacklist_attackers"))
        self.addr_table.setItem(0, 1, QTableWidgetItem("203.0.113.5"))
        self.addr_table.setItem(0, 2, QTableWidgetItem("1d"))

    def _on_apply_basic(self) -> None:
        QMessageBox.information(self, "Terapkan Proteksi", "Pengaturan Dinding Api Dasar (Ping block & FastTrack) berhasil dipasang!")

    def _on_pf_add(self) -> None:
        pub = self.pub_port.text().strip()
        priv = self.priv_ip.text().strip()
        port = self.priv_port.text().strip()

        if not pub or not priv or not port:
            QMessageBox.warning(self, "Validasi Gagal", "Lengkapi seluruh isian formulir NAT.")
            return

        QMessageBox.information(
            self, "Port Forward Sukses",
            f"Aturan NAT berhasil dipasang: Akses luar port {pub} diteruskan ke IP lokal {priv}:{port}."
        )
        self.pub_port.clear()
        self.priv_ip.clear()
        self.priv_port.clear()
