import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFrame,
    QScrollArea, QCheckBox, QSizePolicy, QWidget
)
from PyQt6.QtCore import Qt, pyqtSlot
from ui.widgets.password_field import PasswordField
from core.mikrotik.router_discovery import RouterDiscoveryWorker, RouterDiscoveryResult, RouterDiagnosticsWorker
from core.security.credential_store import CredentialStore
from core.mikrotik.router_client import RouterClient

logger = logging.getLogger("cafepulse.ui.login_dialog")

_DIALOG_STYLE = """
QDialog {
    background-color: #0B0F19;
}
QLabel {
    font-family: 'Segoe UI', -apple-system, sans-serif;
    color: #94A3B8;
    font-size: 11px;
    font-weight: 600;
}
QLineEdit {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 6px;
    color: #F9FAFB;
    padding: 8px 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    min-height: 24px;
}
QLineEdit:focus {
    border: 1px solid #38BDF8;
}
QPushButton {
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 6px;
    color: #F3F4F6;
    padding: 8px 16px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
    font-size: 12px;
    min-height: 22px;
}
QPushButton:hover {
    background-color: #374151;
    border-color: #38BDF8;
    color: #38BDF8;
}
QPushButton#PrimaryBtn {
    background-color: #38BDF8;
    color: #0B0F19;
    border: none;
}
QPushButton#PrimaryBtn:hover {
    background-color: #7DD3FC;
    color: #0B0F19;
}
QPushButton#DangerBtn {
    background-color: #2D1515;
    color: #FC8181;
    border: 1px solid #742A2A;
}
QPushButton#DangerBtn:hover {
    background-color: #E53E3E;
    color: white;
}
QFrame#Divider {
    background: #1F2937;
    border: none;
    max-height: 1px;
    min-height: 1px;
}
QScrollArea {
    background: transparent;
    border: none;
}
"""

class RouterCard(QFrame):
    """Interactive card representing a discovered or saved router."""
    def __init__(self, name: str, ip: str, version: str, status: str, latency: float, is_saved: bool = False, parent=None):
        super().__init__(parent)
        self.name = name
        self.ip = ip
        self.version = version
        self.status = status
        self.latency = latency
        self.is_saved = is_saved
        self.setObjectName("RouterCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Style status badge colors
        status_colors = {
            "Ready": ("#10B981", "rgba(16, 185, 129, 0.15)", "rgba(16, 185, 129, 0.3)"),
            "API Disabled": ("#EF4444", "rgba(239, 68, 68, 0.15)", "rgba(239, 68, 68, 0.3)"),
            "Unknown": ("#3B82F6", "rgba(59, 130, 246, 0.15)", "rgba(59, 130, 246, 0.3)"),
            "Unreachable": ("#64748B", "rgba(100, 116, 139, 0.15)", "rgba(100, 116, 139, 0.3)")
        }
        color, bg, border = status_colors.get(status, status_colors["Unknown"])

        self.setStyleSheet(f"""
            QFrame#RouterCard {{
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 8px;
                padding: 10px;
            }}
            QFrame#RouterCard:hover {{
                border-color: #38BDF8;
                background-color: #1F2937;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)
        
        # Details
        v_col = QVBoxLayout()
        v_col.setSpacing(3)
        
        name_row = QHBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #F9FAFB; background: transparent;")
        name_row.addWidget(name_lbl)
        
        if is_saved:
            saved_badge = QLabel("⭐ SAVED")
            saved_badge.setStyleSheet("font-size: 9px; font-weight: 800; color: #FBBF24; background-color: rgba(251, 191, 36, 0.15); border: 1px solid rgba(251, 191, 36, 0.3); padding: 1px 4px; border-radius: 3px;")
            name_row.addWidget(saved_badge)
            
        name_row.addStretch()
        v_col.addLayout(name_row)
        
        sub_lbl = QLabel(f"{ip} • ROS v{version}")
        sub_lbl.setStyleSheet("font-size: 11px; color: #6B7280; background: transparent;")
        v_col.addWidget(sub_lbl)
        
        layout.addLayout(v_col)
        layout.addStretch()
        
        # Latency + Status Badge
        badge_col = QVBoxLayout()
        badge_col.setSpacing(4)
        badge_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        status_lbl = QLabel(status.upper())
        status_lbl.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {color}; background-color: {bg}; border: 1px solid {border}; padding: 2px 6px; border-radius: 4px;")
        
        lat_lbl = QLabel(f"⚡ {latency} ms" if latency > 0 else "⚡ -- ms")
        lat_lbl.setStyleSheet("font-size: 10px; color: #9CA3AF; background: transparent;")
        
        badge_col.addWidget(status_lbl)
        badge_col.addWidget(lat_lbl)
        layout.addLayout(badge_col)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Propagate custom signal or execute direct trigger
        parent_dialog = self.window()
        if hasattr(parent_dialog, "_on_router_selected"):
            parent_dialog._on_router_selected(self)


class DiagnosticCard(QFrame):
    """
    A beautifully designed diagnostic report widget shown when no routers are found.
    Allows user to run interactive network diagnostics, connect manually, or retry scanning.
    """
    def __init__(self, parent_dialog, parent=None):
        super().__init__(parent)
        self.parent_dialog = parent_dialog
        self.setObjectName("DiagnosticCard")
        
        self.setStyleSheet("""
            QFrame#DiagnosticCard {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 8px;
                padding: 14px;
            }
            QLabel#DiagTitle {
                font-size: 11px;
                font-weight: 800;
                color: #FBBF24;
                letter-spacing: 0.5px;
                background: transparent;
            }
            QLabel#DiagBody {
                font-size: 11px;
                color: #9CA3AF;
                line-height: 14px;
                background: transparent;
            }
            QLabel#Checklbl {
                font-size: 11px;
                color: #D1D5DB;
                background: transparent;
            }
            QFrame#SolutionBox {
                background-color: #1F2937;
                border-radius: 6px;
                padding: 8px;
            }
            QLabel#SolutionTitle {
                font-size: 10px;
                font-weight: 800;
                color: #38BDF8;
                background: transparent;
            }
            QLabel#SolutionText {
                font-size: 11px;
                color: #E5E7EB;
                line-height: 14px;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        title_lbl = QLabel("🔍 DIAGNOSIS HAMBATAN JARINGAN")
        title_lbl.setObjectName("DiagTitle")
        layout.addWidget(title_lbl)

        # Body text
        body_lbl = QLabel("Tidak ada router MikroTik yang terdeteksi secara otomatis. Jaringan Anda mungkin memblokir proses discovery.")
        body_lbl.setObjectName("DiagBody")
        body_lbl.setWordWrap(True)
        layout.addWidget(body_lbl)

        # Checklist layout
        self.checks_layout = QVBoxLayout()
        self.checks_layout.setSpacing(6)
        
        self.check_gw = QLabel("⚪ Koneksi Gateway: Belum diuji")
        self.check_gw.setObjectName("Checklbl")
        
        self.check_iso = QLabel("⚪ AP / Client Isolation: Belum diuji")
        self.check_iso.setObjectName("Checklbl")
        
        self.check_portal = QLabel("⚪ Captive Portal / Hotspot: Belum diuji")
        self.check_portal.setObjectName("Checklbl")
        
        self.check_api = QLabel("⚪ Port API MikroTik (8728/8729): Belum diuji")
        self.check_api.setObjectName("Checklbl")
        
        self.checks_layout.addWidget(self.check_gw)
        self.checks_layout.addWidget(self.check_iso)
        self.checks_layout.addWidget(self.check_portal)
        self.checks_layout.addWidget(self.check_api)
        layout.addLayout(self.checks_layout)

        # Solution box
        self.sol_box = QFrame()
        self.sol_box.setObjectName("SolutionBox")
        sol_layout = QVBoxLayout(self.sol_box)
        sol_layout.setContentsMargins(8, 8, 8, 8)
        sol_layout.setSpacing(4)
        
        sol_title = QLabel("REKOMENDASI SOLUSI")
        sol_title.setObjectName("SolutionTitle")
        sol_layout.addWidget(sol_title)
        
        self.sol_text = QLabel("Silakan klik 'Uji Diagnosis' untuk menganalisis hambatan pada jaringan Wi-Fi/LAN Anda saat ini.")
        self.sol_text.setObjectName("SolutionText")
        self.sol_text.setWordWrap(True)
        sol_layout.addWidget(self.sol_text)
        
        layout.addWidget(self.sol_box)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        
        self.btn_diag = QPushButton("Uji Diagnosis")
        self.btn_diag.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_diag.setStyleSheet("QPushButton { background-color: #1E3A8A; color: #93C5FD; border-color: #2563EB; } QPushButton:hover { background-color: #2563EB; color: white; }")
        self.btn_diag.clicked.connect(self._run_diagnostics)
        
        self.btn_manual = QPushButton("Tambah Manual")
        self.btn_manual.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manual.clicked.connect(self.parent_dialog._on_manual_mode)
        
        self.btn_retry = QPushButton("Scan Ulang")
        self.btn_retry.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_retry.setStyleSheet("QPushButton { background-color: #0369A1; color: white; border: none; } QPushButton:hover { background-color: #0284C7; }")
        self.btn_retry.clicked.connect(self.parent_dialog._start_scan)

        btn_row.addWidget(self.btn_diag)
        btn_row.addWidget(self.btn_manual)
        btn_row.addWidget(self.btn_retry)
        layout.addLayout(btn_row)

    def _run_diagnostics(self):
        self.btn_diag.setEnabled(False)
        self.btn_diag.setText("Mendiagnosis...")
        self.parent_dialog.status_label.setText("Menjalankan diagnosis sistem...")
        
        self.check_gw.setText("⏳ Koneksi Gateway: Memeriksa...")
        self.check_iso.setText("⏳ AP / Client Isolation: Memeriksa...")
        self.check_portal.setText("⏳ Captive Portal / Hotspot: Memeriksa...")
        self.check_api.setText("⏳ Port API MikroTik (8728/8729): Memeriksa...")
        
        self.diag_worker = RouterDiagnosticsWorker(self)
        self.diag_worker.progress_updated.connect(self._on_diag_progress)
        self.diag_worker.finished.connect(self._on_diag_finished)
        self.diag_worker.start()

    def _on_diag_progress(self, msg):
        self.parent_dialog.status_label.setText(msg)

    def _on_diag_finished(self, report):
        self.btn_diag.setEnabled(True)
        self.btn_diag.setText("Uji Diagnosis")
        self.parent_dialog.status_label.setText("Diagnosis jaringan selesai.")
        
        # Update checklist labels with beautiful results
        # 1. Gateway
        if report["gateway_reachable"]:
            self.check_gw.setText("🟢 Koneksi Gateway: Terhubung (" + report["gateway_ip"] + ")")
        else:
            self.check_gw.setText("🔴 Koneksi Gateway: Terputus (" + report["gateway_ip"] + ")")
            
        # 2. Isolation
        if report["client_isolation"]:
            self.check_iso.setText("🟡 AP / Client Isolation: AKTIF (Klien diisolasi)")
        else:
            self.check_iso.setText("🟢 AP / Client Isolation: Tidak Aktif (Discovery diizinkan)")
            
        # 3. Portal
        if report["captive_portal"]:
            self.check_portal.setText("🟡 Captive Portal: Terdeteksi (Dicegat di browser)")
        else:
            self.check_portal.setText("🟢 Captive Portal: Bersih (Akses langsung)")
            
        # 4. API
        if report["api_enabled"]:
            self.check_api.setText("🟢 Port API MikroTik: Terbuka (Siap terhubung)")
        elif report["gateway_reachable"]:
            self.check_api.setText("🔴 Port API MikroTik: Tertutup (Layanan API router mati)")
        else:
            self.check_api.setText("⚪ Port API MikroTik: Tidak Terdeteksi")
            
        # Update solution box text
        self.sol_text.setText(report["solution"])


class MikrotikLoginDialog(QDialog):
    """
    Stunning, split-panel MikroTik Connection & Discovery Center.
    - Left side: Discovered and Saved router profiles.
    - Right side: Login credentials form + connection profiles generator.
    """
    def __init__(self, db=None, config=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.selected_ip = None
        self.selected_port = 8728
        self.selected_use_ssl = False
        
        self.setWindowTitle("Workspace Connection — CafePulse")
        self.setMinimumSize(640, 420)
        self.resize(820, 520)
        self.setSizeGripEnabled(True)
        self.setStyleSheet(_DIALOG_STYLE)
        
        self._build_ui()
        self._load_saved_profiles()
        
        # Auto-trigger scan on startup for seamless instant discovery
        self._start_scan()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(24)

        # ─── LEFT PANEL: DISCOVERY & PROFILES ─────────────────────────────────
        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)
        
        disc_title = QLabel("DETECTOR & PROFIL")
        disc_title.setStyleSheet("font-size: 10px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        left_layout.addWidget(disc_title)
        
        # Scrollable area for discovered router list
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 8, 0)
        self.scroll_layout.setSpacing(8)
        self.scroll_layout.addStretch()  # Initial stretch
        self.scroll.setWidget(self.scroll_widget)
        left_layout.addWidget(self.scroll)
        
        # Scan Progress Text
        self.progress_lbl = QLabel("")
        self.progress_lbl.setStyleSheet("color: #38BDF8; font-size: 11px; font-style: italic; background: transparent;")
        left_layout.addWidget(self.progress_lbl)
        
        # Left side buttons
        left_btn_row = QHBoxLayout()
        left_btn_row.setSpacing(8)
        
        self.btn_scan = QPushButton("Scan Jaringan")
        self.btn_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_scan.clicked.connect(self._start_scan)
        
        self.btn_manual = QPushButton("Tambah Manual")
        self.btn_manual.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manual.clicked.connect(self._on_manual_mode)
        
        left_btn_row.addWidget(self.btn_scan)
        left_btn_row.addWidget(self.btn_manual)
        left_btn_row.addStretch()
        left_layout.addLayout(left_btn_row)
        
        main_layout.addLayout(left_layout, stretch=4)

        # ─── MIDDLE DIVIDER ───────────────────────────────────────────────────
        mid_div = QFrame()
        mid_div.setFrameShape(QFrame.Shape.VLine)
        mid_div.setStyleSheet("background-color: #1F2937; max-width: 1px;")
        main_layout.addWidget(mid_div)

        # ─── RIGHT PANEL: CONNECTION FORM ─────────────────────────────────────
        right_layout = QVBoxLayout()
        right_layout.setSpacing(14)
        
        conn_title = QLabel("WORKSPACE LOGIN")
        conn_title.setStyleSheet("font-size: 10px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        right_layout.addWidget(conn_title)

        # Selection Header
        self.sel_header = QLabel("Pilih router dari daftar atau gunakan mode manual")
        self.sel_header.setWordWrap(True)
        self.sel_header.setStyleSheet("font-size: 13px; font-weight: 700; color: #F9FAFB; min-height: 36px;")
        right_layout.addWidget(self.sel_header)

        # Divider
        div1 = QFrame()
        div1.setObjectName("Divider")
        right_layout.addWidget(div1)

        # Form Layout fields
        self.ip_container = QWidget()
        ip_vbox = QVBoxLayout(self.ip_container)
        ip_vbox.setContentsMargins(0, 0, 0, 0)
        ip_vbox.setSpacing(4)
        ip_vbox.addWidget(QLabel("ROUTER IP ADDRESS"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 192.168.88.1")
        ip_vbox.addWidget(self.ip_input)
        right_layout.addWidget(self.ip_container)
        self.ip_container.setVisible(False)  # Hidden by default, unlocked by "Tambah Manual"

        # Read-only selector details
        self.read_only_details = QLabel("")
        self.read_only_details.setStyleSheet("color: #9CA3AF; font-size: 11px; line-height: 14px;")
        right_layout.addWidget(self.read_only_details)

        # Username
        user_vbox = QVBoxLayout()
        user_vbox.setSpacing(4)
        user_vbox.addWidget(QLabel("USERNAME"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("admin")
        user_vbox.addWidget(self.user_input)
        right_layout.addLayout(user_vbox)

        # Password
        pass_vbox = QVBoxLayout()
        pass_vbox.setSpacing(4)
        pass_vbox.addWidget(QLabel("PASSWORD"))
        self.pass_input = PasswordField()
        self.pass_input.setPlaceholderText("Sandi RouterOS")
        pass_vbox.addWidget(self.pass_input)
        right_layout.addLayout(pass_vbox)

        # Checkbox & Name profile for saving connection
        self.profile_vbox = QVBoxLayout()
        self.profile_vbox.setSpacing(6)
        self.chk_save = QCheckBox("Simpan sebagai Profil Favorit")
        self.chk_save.setStyleSheet("QCheckBox { color: #94A3B8; font-size: 11px; font-weight: bold; }")
        self.chk_save.toggled.connect(self._on_save_toggled)
        self.profile_vbox.addWidget(self.chk_save)
        
        self.profile_name_container = QWidget()
        name_vbox = QVBoxLayout(self.profile_name_container)
        name_vbox.setContentsMargins(0, 0, 0, 0)
        name_vbox.setSpacing(4)
        self.profile_name_input = QLineEdit()
        self.profile_name_input.setPlaceholderText("Nama Profil (e.g. Kafe Utama)")
        name_vbox.addWidget(self.profile_name_input)
        self.profile_vbox.addWidget(self.profile_name_container)
        self.profile_name_container.setVisible(False)
        
        right_layout.addLayout(self.profile_vbox)

        # Status output
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: normal;")
        right_layout.addWidget(self.status_label)
        
        right_layout.addStretch()

        # Connect button actions
        self.btn_connect = QPushButton("Sambungkan Jaringan")
        self.btn_connect.setObjectName("PrimaryBtn")
        self.btn_connect.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_connect.setDefault(True)
        self.btn_connect.clicked.connect(self._on_connect_clicked)
        right_layout.addWidget(self.btn_connect)
        
        main_layout.addLayout(right_layout, stretch=3)

        # Wired keys
        self.ip_input.returnPressed.connect(self._on_connect_clicked)
        self.user_input.returnPressed.connect(self._on_connect_clicked)
        self.pass_input.returnPressed.connect(self._on_connect_clicked)
        self.profile_name_input.returnPressed.connect(self._on_connect_clicked)

    def _load_saved_profiles(self):
        """Fetches saved connection profiles from database and renders them."""
        self.saved_profiles = []
        if not self.db:
            return

        try:
            self.saved_profiles = self.db.get_all_routers()
        except Exception as e:
            logger.error("Failed to load saved profiles: %s", e)

    def _render_router_list(self, discovered_list: list[RouterDiscoveryResult] = None):
        """Clears list layout and rebuilds with saved profiles and auto-discovered ones."""
        # Clear scrollable layout safely
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 1. Render Saved Profiles first (Reconnect candidates)
        if self.saved_profiles:
            for p in self.saved_profiles:
                try:
                    # Saved password decrypt to test check
                    pwd_dec = CredentialStore.decrypt(p["password"])
                    card = RouterCard(
                        name=p["name"],
                        ip=p["host"],
                        version="Saved Profile",
                        status="Ready",
                        latency=0,
                        is_saved=True,
                        parent=self.scroll_widget
                    )
                    # Bind saved credentials data to card properties
                    card.username = p["username"]
                    card.password = pwd_dec
                    card.port = p["port"]
                    card.use_ssl = bool(p["use_ssl"])
                    self.scroll_layout.addWidget(card)
                except Exception as e:
                    logger.error("Failed to render saved profile card: %s", e)

        # 2. Render Discovered Router candidates
        if discovered_list:
            # Prevent showing duplicate IP of saved profiles if they are already rendered
            rendered_ips = {p["host"] for p in self.saved_profiles} if self.saved_profiles else set()
            for r in discovered_list:
                if r.ip_address in rendered_ips:
                    continue
                card = RouterCard(
                    name=r.identity,
                    ip=r.ip_address,
                    version=r.routeros_version,
                    status=r.status,
                    latency=r.response_time,
                    is_saved=False,
                    parent=self.scroll_widget
                )
                card.username = "admin"
                card.password = ""
                card.port = 8728 if r.api_available else 8729
                card.use_ssl = not r.api_available and r.api_ssl_available
                self.scroll_layout.addWidget(card)

        # Placeholder if empty
        if self.scroll_layout.count() == 0:
            diag_card = DiagnosticCard(self, self.scroll_widget)
            self.scroll_layout.addWidget(diag_card)

        self.scroll_layout.addStretch()

    def _start_scan(self):
        """Spawns non-blocking discovery QThread."""
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("Memindai...")
        self.progress_lbl.setText("Menginisialisasi detektor subnet...")
        
        self.worker = RouterDiscoveryWorker(self)
        self.worker.progress_updated.connect(self._on_scan_progress)
        self.worker.finished.connect(self._on_scan_finished)
        self.worker.start()

    @pyqtSlot(str)
    def _on_scan_progress(self, progress_msg: str):
        self.progress_lbl.setText(progress_msg)

    @pyqtSlot(list)
    def _on_scan_finished(self, results: list):
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("Scan Jaringan")
        self.progress_lbl.setText(f"Selesai. Menemukan {len(results)} perangkat.")
        self._render_router_list(discovered_list=results)

    def _on_router_selected(self, card: RouterCard):
        """Triggered when user clicks a router card in the left list."""
        self.selected_ip = card.ip
        self.selected_port = getattr(card, "port", 8728)
        self.selected_use_ssl = getattr(card, "use_ssl", False)
        
        self.ip_container.setVisible(False)
        self.sel_header.setText(f"✓ {card.name}")
        self.sel_header.setStyleSheet("font-size: 15px; font-weight: bold; color: #10B981;")
        
        det_str = f"IP Address: {card.ip}\nStatus API: {card.status}\nUpdate Entitlement: Lifetime Pro Support"
        if card.is_saved:
            det_str += "\nKredensial tersimpan berhasil dimuat."
        self.read_only_details.setText(det_str)
        
        # Auto fill username and password from card
        self.user_input.setText(getattr(card, "username", "admin"))
        self.pass_input.setText(getattr(card, "password", ""))

    def _on_manual_mode(self):
        """Unlocks standard text-field connection mode."""
        self.selected_ip = None
        self.ip_container.setVisible(True)
        self.ip_input.setText("")
        self.sel_header.setText("Manual Router Entry")
        self.sel_header.setStyleSheet("font-size: 15px; font-weight: bold; color: #38BDF8;")
        self.read_only_details.setText("Masukkan IP Address router secara manual untuk terhubung langsung.")
        self.user_input.setText("admin")
        self.pass_input.setText("")

    def _on_save_toggled(self, checked: bool):
        self.profile_name_container.setVisible(checked)
        if checked:
            self.profile_name_input.setText(self.sel_header.text().replace("✓ ", "").strip() if self.selected_ip else "Cafe Utama")

    def _on_connect_clicked(self):
        """Validates credentials and closes dialog with accepted code."""
        ip = self.selected_ip if self.selected_ip else self.ip_input.text().strip()
        user = self.user_input.text().strip()
        pwd = self.pass_input.text()
        
        if not ip:
            QMessageBox.warning(self, "Validasi Gagal", "IP Address router tidak boleh kosong!")
            return
        if not user:
            QMessageBox.warning(self, "Validasi Gagal", "Username login tidak boleh kosong!")
            return

        self.status_label.setText("Menghubungkan & verifikasi kredensial...")
        
        # Fast synchronous credentials validation via RouterClient
        try:
            client = RouterClient(ip, user, pwd, port=self.selected_port, use_ssl=self.selected_use_ssl)
            success, err_msg = client.validate_credentials()
            if success:
                self.accept()
            else:
                self.status_label.setText("Gagal.")
                QMessageBox.critical(self, "Koneksi Gagal", f"Tidak dapat terhubung ke MikroTik:\n{err_msg}")
        except Exception as e:
            self.status_label.setText("Gagal.")
            QMessageBox.critical(self, "Koneksi Gagal", f"Terjadi kesalahan koneksi:\n{e}")

    def get_credentials(self) -> dict:
        ip = self.selected_ip if self.selected_ip else self.ip_input.text().strip()
        return {
            "ip": ip,
            "username": self.user_input.text().strip(),
            "password": self.pass_input.text(),
            "port": self.selected_port,
            "use_ssl": self.selected_use_ssl,
            "save_profile": self.chk_save.isChecked(),
            "profile_name": self.profile_name_input.text().strip()
        }
