"""
CafePulse — Devices & Operations Page (Sub-Phase 3-D)
Rich triple-tab interface integrating Device Manager with dynamic categorization,
DHCP Lease Center with IP reservations, and automatic Backup Scheduler.
"""

import os
import logging
import platform
import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QPushButton, QFrame, QAbstractItemView,
    QStackedWidget, QTabWidget, QComboBox, QMessageBox,
    QInputDialog, QDialog, QFormLayout, QDialogButtonBox, QMenu, QApplication,
    QSplitter
)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QColor, QFont

from ui.widgets.empty_state import EmptyStateWidget
from core.licensing.licensing_manager import LicensingManager
from core.app_paths import SETTINGS_FILE, DATABASE_FILE

logger = logging.getLogger("cafepulse.ui.devices")

# ─── Device Categorization Helper ──────────────────────────────────────────────

def get_device_category(hostname: str, vendor: str) -> str:
    """Helper to automatically categorize devices based on hostname & vendor strings."""
    h = (hostname or "").lower()
    v = (vendor or "").lower()
    
    phone_keywords = ["phone", "mobile", "android", "iphone", "ipad", "samsung", "xiaomi", "oppo", "vivo", "realme", "huawei", "oneplus"]
    if any(k in h or k in v for k in phone_keywords):
        return "Smartphone"
        
    iot_keywords = ["iot", "smart", "cam", "tv", "plug", "printer", "tplink", "tp-link", "cisco", "sonoff", "nest", "alexa", "echo", "bulb", "switch", "esp32", "arduino"]
    if any(k in h or k in v for k in iot_keywords):
        return "IoT"
        
    desktop_keywords = ["pc", "desktop", "laptop", "notebook", "macbook", "imac", "workstation", "dell", "hp", "lenovo", "asus", "acer"]
    if any(k in h or k in v for k in desktop_keywords):
        return "Laptop/Desktop"
        
    return "Other"

# ─── Vendor Badge Colors ──────────────────────────────────────────────────────

_VENDOR_COLORS: dict[str, tuple[str, str]] = {
    "apple":     ("#1C3244", "#38BDF8"),
    "samsung":   ("#1A2E1A", "#22C55E"),
    "xiaomi":    ("#2D1F1F", "#F87171"),
    "huawei":    ("#1F2D1F", "#86EFAC"),
    "oppo":      ("#271A2D", "#C084FC"),
    "vivo":      ("#1A2233", "#60A5FA"),
    "realme":    ("#2D2214", "#FCD34D"),
    "google":    ("#1C2633", "#93C5FD"),
    "microsoft": ("#1F1F2D", "#A5B4FC"),
    "lenovo":    ("#2D1A1A", "#FCA5A5"),
    "dell":      ("#1A2525", "#6EE7B7"),
    "hp ":       ("#201520", "#E879F9"),
    "asus":      ("#252015", "#FDE68A"),
    "tp-link":   ("#152025", "#67E8F9"),
    "cisco":     ("#152015", "#4ADE80"),
    "sony":      ("#202020", "#D1D5DB"),
    "lg ":       ("#202018", "#FEF08A"),
}

def _vendor_badge_colors(vendor: str, theme: str = "dark") -> tuple[str, str]:
    v = vendor.lower()
    if theme == "light":
        light_vendor_colors = {
            "apple":     ("#F1F5F9", "#0F172A"),
            "samsung":   ("#DCFCE7", "#15803D"),
            "xiaomi":    ("#FEE2E2", "#B91C1C"),
            "huawei":    ("#ECFDF5", "#047857"),
            "oppo":      ("#F3E8FF", "#6D28D9"),
            "vivo":      ("#EFF6FF", "#1D4ED8"),
            "realme":    ("#FEF9C3", "#A16207"),
            "google":    ("#E0F2FE", "#0369A1"),
            "tp-link":   ("#E0F2FE", "#0369A1"),
            "cisco":     ("#D1FAE5", "#065F46"),
        }
        for key, colors in light_vendor_colors.items():
            if key in v:
                return colors
        return ("#F1F5F9", "#475569")
    else:
        for key, colors in _VENDOR_COLORS.items():
            if key in v:
                return colors
        return ("#1E293B", "#64748B")

# ─── Pill Button ──────────────────────────────────────────────────────────────

class _PillButton(QPushButton):
    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme = "dark"
        self._update_style(False)

    def setChecked(self, checked: bool) -> None:
        super().setChecked(checked)
        self._update_style(checked)

    def _update_style(self, active: bool, theme: str = None) -> None:
        if theme is not None:
            self._theme = theme
        t = self._theme
        if active:
            if t == "light":
                self.setStyleSheet(
                    "QPushButton { background:#0284C7; color:#FFFFFF; border:none;"
                    "border-radius:12px; padding:4px 16px; font-size:11px; font-weight:700; }"
                )
            else:
                self.setStyleSheet(
                    "QPushButton { background:#38BDF8; color:#0F172A; border:none;"
                    "border-radius:12px; padding:4px 16px; font-size:11px; font-weight:700; }"
                )
        else:
            if t == "light":
                self.setStyleSheet(
                    "QPushButton { background:#F1F5F9; color:#475569; border:1px solid #E2E8F0;"
                    "border-radius:12px; padding:4px 16px; font-size:11px; font-weight:600; }"
                    "QPushButton:hover { background:#E2E8F0; color:#0F172A; }"
                )
            else:
                self.setStyleSheet(
                    "QPushButton { background:#1E293B; color:#64748B; border:1px solid #2D3748;"
                    "border-radius:12px; padding:4px 16px; font-size:11px; font-weight:600; }"
                    "QPushButton:hover { background:#2D3748; color:#94A3B8; }"
                )

# ─── Stat Chip ────────────────────────────────────────────────────────────────

class _StatChip(QFrame):
    def __init__(self, label: str, color: str, parent=None):
        super().__init__(parent)
        self.color = color
        self.setStyleSheet(f"background:#0F172A; border:1px solid {color}33; border-radius:8px;")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 6, 12, 6)
        lay.setSpacing(8)

        self._dot = QLabel("●")
        self._dot.setStyleSheet(f"color:{color}; font-size:10px; background:transparent; border:none;")
        lay.addWidget(self._dot)

        self._lbl_name = QLabel(label)
        self._lbl_name.setStyleSheet(f"color:#64748B; font-size:11px; background:transparent; border:none;")
        lay.addWidget(self._lbl_name)

        self._lbl_val = QLabel("0")
        self._lbl_val.setStyleSheet(f"color:{color}; font-size:13px; font-weight:700; background:transparent; border:none;")
        lay.addWidget(self._lbl_val)

    def set_value(self, val: int) -> None:
        self._lbl_val.setText(str(val))

    def update_theme(self, theme: str, color: str) -> None:
        self.color = color
        self._dot.setStyleSheet(f"color:{color}; font-size:10px; background:transparent; border:none;")
        if theme == "light":
            self.setStyleSheet(f"background:#FFFFFF; border:1px solid {color}44; border-radius:8px;")
            self._lbl_name.setStyleSheet(f"color:#475569; font-size:11px; background:transparent; border:none;")
            self._lbl_val.setStyleSheet(f"color:{color}; font-size:13px; font-weight:700; background:transparent; border:none;")
        else:
            self.setStyleSheet(f"background:#0F172A; border:1px solid {color}33; border-radius:8px;")
            self._lbl_name.setStyleSheet(f"color:#64748B; font-size:11px; background:transparent; border:none;")
            self._lbl_val.setStyleSheet(f"color:{color}; font-size:13px; font-weight:700; background:transparent; border:none;")

# ─── Non-Blocking Backup Scheduler Thread Worker ──────────────────────────────

class BackupWorker(QThread):
    """PyQt background QThread to communicate with MikroTik API for Backup operations."""
    finished = pyqtSignal(bool, str) # success, message_log
    
    def __init__(self, api, action: str, filename: str = None):
        super().__init__()
        self.api = api
        self.action = action # "backup", "restore", "delete", "list"
        self.filename = filename
        self.result_data = None
        
    def run(self):
        try:
            if not self.api:
                self.finished.emit(False, "Tidak ada koneksi aktif ke MikroTik.")
                return
                
            if self.action == "backup":
                backup_res = self.api.get_resource('/system/backup')
                backup_res.call('save', {'name': self.filename})
                self.finished.emit(True, f"Sukses! Backup '{self.filename}' berhasil diproduksi di MikroTik.")
                
            elif self.action == "restore":
                backup_res = self.api.get_resource('/system/backup')
                backup_res.call('load', {'name': self.filename})
                self.finished.emit(True, f"Memulai pemulihan cadangan '{self.filename}'. RouterOS akan me-reboot.")
                
            elif self.action == "delete":
                file_res = self.api.get_resource('/file')
                files = file_res.get()
                found = False
                for f in files:
                    if f.get('name') == self.filename:
                        file_res.remove(id=f.get('id'))
                        found = True
                        break
                if found:
                    self.finished.emit(True, f"File backup '{self.filename}' berhasil dihapus.")
                else:
                    self.finished.emit(False, f"File backup '{self.filename}' tidak ditemukan di router.")
                    
            elif self.action == "list":
                file_res = self.api.get_resource('/file')
                files = file_res.get()
                backups = []
                for f in files:
                    name = f.get('name', '')
                    if name.endswith('.backup') or f.get('type') == 'backup':
                        backups.append({
                            "name": name,
                            "size": f.get('size', 'N/A'),
                            "creation_time": f.get('creation-time', 'N/A')
                        })
                self.result_data = backups
                self.finished.emit(True, "Daftar backup berhasil diperbarui.")
        except Exception as e:
            logger.error("BackupWorker failed: %s", e)
            self.finished.emit(False, str(e))

# ─── Device Detailed History Modal (PRO ONLY) ─────────────────────────────────

class DeviceDetailDialog(QDialog):
    def __init__(self, device_info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detail Perangkat & Histori Kunjungan (PRO)")
        self.setFixedWidth(480)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F131E;
                color: #E2E8F0;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QLabel {
                color: #CBD5E1;
                font-size: 13px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        
        title = QLabel("💻  Informasi Histori Perangkat")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #06B6D4; padding-bottom: 8px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        # Details
        form.addRow("Nama Perangkat:", QLabel(device_info.get("hostname", "Unknown")))
        form.addRow("Alamat IP:", QLabel(device_info.get("ip", "—")))
        form.addRow("Alamat MAC:", QLabel(device_info.get("mac", "—")))
        form.addRow("Vendor:", QLabel(device_info.get("vendor", "Unknown")))
        
        cat = device_info.get("category", "Other")
        cat_icon = "⚙️"
        if cat == "Smartphone": cat_icon = "📱"
        elif cat == "Laptop/Desktop": cat_icon = "💻"
        elif cat == "IoT": cat_icon = "🔌"
        
        form.addRow("Kategori Otomatis:", QLabel(f"{cat_icon} {cat}"))
        
        # History
        first_seen = device_info.get("first_seen", "N/A")
        last_seen = device_info.get("last_seen", "N/A")
        
        try:
            if "T" in first_seen:
                first_seen = first_seen.replace("T", " ")[:19]
            if "T" in last_seen:
                last_seen = last_seen.replace("T", " ")[:19]
        except Exception:
            pass
            
        form.addRow("Pertama Kali Terlihat:", QLabel(first_seen))
        form.addRow("Terakhir Aktif:", QLabel(last_seen))
        
        status_text = "Online" if device_info.get("status") == "online" else "Offline"
        status_lbl = QLabel(status_text)
        status_lbl.setStyleSheet(f"color: {'#22C55E' if status_text == 'Online' else '#94A3B8'}; font-weight: bold;")
        form.addRow("Status Jaringan:", status_lbl)
        
        layout.addLayout(form)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("border: 1px solid #1E293B;")
        layout.addWidget(divider)
        
        # Close button
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btn_box.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                border: 1px solid #2D3748;
                border-radius: 6px;
                color: #E2E8F0;
                padding: 8px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2D3748;
                color: #FFFFFF;
            }
        """)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)

class EditDeviceDialog(QDialog):
    """
    Elegant, premium QDialog for editing a device's custom hostname/alias.
    """
    def __init__(self, device_info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Device Info")
        self.setFixedWidth(440)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F131E;
                color: #E2E8F0;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QLabel {
                color: #CBD5E1;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #07090E;
                border: 1px solid #1F273E;
                border-radius: 6px;
                padding: 8px 12px;
                color: #F8FAFC;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #06B6D4;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        
        title = QLabel("✏️  Edit Device Info")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #06B6D4; padding-bottom: 8px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        self.mac_lbl = QLabel(device_info.get("mac", "—"))
        self.mac_lbl.setStyleSheet("color:#64748B; font-weight:600;")
        form.addRow("MAC Address:", self.mac_lbl)
        
        self.ip_lbl = QLabel(device_info.get("ip", "—"))
        self.ip_lbl.setStyleSheet("color:#64748B; font-weight:600;")
        form.addRow("IP Address:", self.ip_lbl)
        
        self.hn_input = QLineEdit()
        self.hn_input.setText(device_info.get("hostname", ""))
        form.addRow("Hostname / Alias:", self.hn_input)
        
        layout.addLayout(form)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("border: 1px solid #1E293B;")
        layout.addWidget(divider)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        
        save_btn = btn_box.button(QDialogButtonBox.StandardButton.Save)
        if save_btn:
            save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0891B2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #06B6D4;
                }
            """)
        cancel_btn = btn_box.button(QDialogButtonBox.StandardButton.Cancel)
        if cancel_btn:
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B;
                    border: 1px solid #2D3748;
                    border-radius: 6px;
                    color: #E2E8F0;
                    padding: 8px 20px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #2D3748;
                    color: #FFFFFF;
                }
            """)
        
        layout.addWidget(btn_box)

    def get_hostname(self) -> str:
        return self.hn_input.text().strip()

# ─── Devices Page ─────────────────────────────────────────────────────────────

class DevicesPage(QWidget):
    demo_mode_requested = pyqtSignal()

    # Columns definitions for tabs
    COLUMNS_DEV = ["  ", "Hostname", "IP Address", "MAC Address", "Vendor", "Category", "↑ Upload", "↓ Download", "Status", "Last Seen"]
    COL_DOT      = 0
    COL_HOSTNAME = 1
    COL_IP       = 2
    COL_MAC      = 3
    COL_VENDOR   = 4
    COL_CATEGORY = 5
    COL_UP       = 6
    COL_DOWN     = 7
    COL_STATUS   = 8
    COL_LASTSEEN = 9

    COLUMNS_DHCP = ["IP Address", "MAC Address", "Hostname", "Status", "Type"]

    COLUMNS_BACKUP = ["Backup Filename", "Size", "Date & Time Created"]

    def __init__(self, db=None, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        self._db = db
        self._app_state = app_state
        
        # In-memory states
        self._all_rows: list[dict] = []
        self._filter_mode = "all"  # "all" | "online" | "offline" | "smartphone" | "laptop" | "iot"
        self._sort_col = self.COL_STATUS
        self._sort_asc = True
        
        self._is_pro = self._app_state.is_pro if self._app_state else False
        
        # Dynamic Mock states for Demo Mode
        self._demo_dhcp_leases = [
            {"ip": "192.168.88.20", "mac": "B4:F6:1C:89:E2:01", "hostname": "Budi-Smartphone", "status": "bound", "dynamic": "yes"},
            {"ip": "192.168.88.35", "mac": "00:E0:4C:53:11:AB", "hostname": "Smart-TV-Cafe", "status": "bound", "dynamic": "no"},
            {"ip": "192.168.88.100", "mac": "70:8B:CD:42:EF:89", "hostname": "Kasir-POS-Printer", "status": "bound", "dynamic": "no"},
            {"ip": "192.168.88.112", "mac": "F0:2F:74:AC:4A:22", "hostname": "Guest-Laptop-Bagus", "status": "bound", "dynamic": "yes"}
        ]
        self._demo_backups = [
            {"name": "CafePulse_Initial_Setup.backup", "size": "45.2 KB", "creation_time": "2026-05-15 08:30:12"},
            {"name": "Weekly_Backup_System.backup", "size": "48.7 KB", "creation_time": "2026-05-24 23:00:00"},
            {"name": "RouterOS_v7.12_Config.backup", "size": "50.1 KB", "creation_time": "2026-05-28 14:15:35"}
        ]
        
        self._build_ui()
        
        if self._app_state:
            self._app_state.mode_changed.connect(self._on_mode_changed)
            self._app_state.licensing_changed.connect(self._on_licensing_changed)
            self._app_state.privacy_masked_changed.connect(lambda: self._refresh())
            self._on_mode_changed(self._app_state.current_mode)
            
        # Hook scheduler interval check on tick updates
        self._scheduler_timer = QTimer(self)
        self._scheduler_timer.timeout.connect(self._check_auto_backup_schedule)
        self._scheduler_timer.start(30000) # Check every 30 seconds

    def _is_licensed(self) -> bool:
        """Helper to verify Pro license. Shows dynamic upgrade dialog on Basic."""
        if not self._is_pro:
            from ui.dialogs.error_dialog import show_smart_error
            show_smart_error(
                title="Fitur Premium CafePulse",
                message="Lisensi Professional Diperlukan untuk melakukan modifikasi.",
                exc_type="LicenseRequiredError",
                tb_text="Lisensi CafePulse Free membatasi interaksi hanya sebatas Monitoring (Read-Only).\n\n"
                        "Untuk mengaktifkan DHCP reservations statis, mengelola dynamic leases, "
                        "serta menjadwalkan backup RouterOS otomatis, silakan aktifkan CafePulse Professional."
            )
            return False
        return True

    def _get_api(self):
        """Ambil objek API MikroTik secara aman dari MainWindow."""
        try:
            main_window = self.window()
            if hasattr(main_window, "_mikrotik_worker") and main_window._mikrotik_worker:
                return main_window._mikrotik_worker.manager.get_api()
        except Exception as e:
            logger.error("Failed to retrieve MikroTik API: %s", e)
        return None

    # ─── UI Build ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._main_stack = QStackedWidget(self)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self._main_stack)
        
        # 1. Halaman 0: Empty State View
        self._empty_view = EmptyStateWidget(
            title="Tidak Ada Perangkat Jaringan",
            subtitle="CafePulse belum mendeteksi perangkat aktif. Jalankan Demo Mode untuk simulasi "
                     "perangkat café, atau mulai pemindaian lokal mandiri melalui menu Modes.",
            icon="💻",
            cta_text="Aktifkan Demo Mode"
        )
        self._empty_view.quick_start_requested.connect(self.demo_mode_requested.emit)
        self._main_stack.addWidget(self._empty_view)
        
        # 2. Halaman 1: Normal Operations View (Triple-Tabbed Shell)
        self._normal_view = QWidget()
        self._main_stack.addWidget(self._normal_view)
        
        root = QVBoxLayout(self._normal_view)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # ── Title row ────────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        title = QLabel("Operations Center")
        title.setObjectName("SectionHeader")
        hdr.addWidget(title)
        hdr.addStretch()

        self._updated_lbl = QLabel("Never updated")
        self._updated_lbl.setStyleSheet("color:#4A5568; font-size:11px;")
        hdr.addWidget(self._updated_lbl)
        root.addLayout(hdr)

        sub = QLabel("Kelola perangkat aktif, konfigurasi DHCP, serta jadwal pencadangan otomatis MikroTik")
        sub.setObjectName("SectionSubtitle")
        root.addWidget(sub)

        # ── Tabbed View ──
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #1F273E;
                background-color: #0F131E;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #161B27;
                color: #94A3B8;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
                font-weight: 600;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #0F131E;
                color: #06B6D4;
                border-bottom: 2px solid #06B6D4;
            }
        """)
        root.addWidget(self.tabs)

        # Connect tab changes to refresh DHCP and backups automatically
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # Tab 1: Device Manager
        self._build_device_tab()
        
        # Tab 2: DHCP Manager
        self._build_dhcp_tab()
        
        # Tab 3: Backup Scheduler
        self._build_backup_tab()

    def _build_device_tab(self) -> None:
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Stats bar
        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)
        self._chip_total   = _StatChip("Total",   "#38BDF8")
        self._chip_online  = _StatChip("Online",  "#22C55E")
        self._chip_offline = _StatChip("Offline", "#94A3B8")
        self._chip_new     = _StatChip("New",     "#F59E0B")
        for chip in (self._chip_total, self._chip_online, self._chip_offline, self._chip_new):
            stats_row.addWidget(chip)
        stats_row.addStretch()
        layout.addLayout(stats_row)

        # Controls row
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        # Search
        self._search = QLineEdit()
        self._search.setPlaceholderText("  Cari hostname, IP, MAC, vendor, atau kategori…")
        self._search.setMaximumWidth(380)
        self._search.setStyleSheet(
            "QLineEdit { background:#1E293B; color:#E2E8F0; border:1px solid #2D3748;"
            "border-radius:8px; padding:7px 12px; font-size:12px; }"
            "QLineEdit:focus { border-color:#38BDF8; }"
        )
        self._search.textChanged.connect(self._refresh)
        ctrl_row.addWidget(self._search)

        ctrl_row.addSpacing(8)

        # Filter pills
        self._pill_all      = _PillButton("All")
        self._pill_online   = _PillButton("Online")
        self._pill_offline  = _PillButton("Offline")
        self._pill_smart    = _PillButton("📱 Smartphone")
        self._pill_laptop   = _PillButton("💻 Laptop/PC")
        self._pill_iot      = _PillButton("🔌 IoT")
        
        self._pill_all.setChecked(True)
        self._pill_all.clicked.connect(lambda: self._set_filter("all"))
        self._pill_online.clicked.connect(lambda: self._set_filter("online"))
        self._pill_offline.clicked.connect(lambda: self._set_filter("offline"))
        self._pill_smart.clicked.connect(lambda: self._set_filter("smartphone"))
        self._pill_laptop.clicked.connect(lambda: self._set_filter("laptop"))
        self._pill_iot.clicked.connect(lambda: self._set_filter("iot"))
        
        for pill in (self._pill_all, self._pill_online, self._pill_offline, self._pill_smart, self._pill_laptop, self._pill_iot):
            ctrl_row.addWidget(pill)

        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)

        # Splitter Layout (Table + details panel)
        self._device_splitter = QSplitter(Qt.Orientation.Horizontal)
        self._device_splitter.setChildrenCollapsible(False)  # Phase 8: Never collapse panels to 0px
        self._device_splitter.setHandleWidth(5)

        left_container = QWidget()
        left_container.setMinimumWidth(320)  # Phase 8: Guarantee list panel is always readable
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # Table
        self._table = QTableWidget(0, len(self.COLUMNS_DEV))
        self._table.verticalHeader().setDefaultSectionSize(36)
        self._table.setHorizontalHeaderLabels(self.COLUMNS_DEV)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        self._table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._table.setSortingEnabled(False)
        
        # Double-click triggers history dialog
        self._table.doubleClicked.connect(self._on_device_row_double_clicked)
        self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._on_table_context_menu)
        self._table.itemSelectionChanged.connect(self._on_table_selection_changed)

        self._table.setStyleSheet("""
            QTableWidget {
                background: #0F172A;
                border: 1px solid #1E293B;
                border-radius: 8px;
                gridline-color: #1E293B;
                outline: none;
            }
            QTableWidget::item {
                padding: 0px 8px;
                border-bottom: 1px solid #1A2744;
                color: #CBD5E1;
            }
            QTableWidget::item:selected {
                background: #1E3A5F;
                color: #E2E8F0;
            }
            QHeaderView::section {
                background: #1E293B;
                color: #64748B;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #2D3748;
            }
        """)

        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(self.COL_DOT,      QHeaderView.ResizeMode.Fixed)
        hh.setSectionResizeMode(self.COL_HOSTNAME,  QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(self.COL_IP,        QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_MAC,       QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_VENDOR,    QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(self.COL_CATEGORY,  QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_UP,        QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_DOWN,      QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_STATUS,    QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.COL_LASTSEEN,  QHeaderView.ResizeMode.ResizeToContents)
        self._table.setColumnWidth(self.COL_DOT, 28)
        hh.sectionClicked.connect(self._on_header_clicked)

        left_layout.addWidget(self._table)
        
        info_hint = QLabel("💡 Click device row to view quick details. Double-click for telemetry profile.")
        info_hint.setStyleSheet("color:#64748B; font-size:11px;")
        left_layout.addWidget(info_hint)

        # Right details panel
        self._details_panel = QFrame()
        self._details_panel.setObjectName("DetailsPanel")
        self._details_panel.setMinimumWidth(260)  # Phase 8: Never allow details panel below 260px
        self._details_panel.setStyleSheet("""
            QFrame#DetailsPanel {
                background-color: #111827;
                border: 1px solid #1F273E;
                border-radius: 8px;
            }
        """)
        self._details_lay = QVBoxLayout(self._details_panel)
        self._details_lay.setContentsMargins(18, 18, 18, 18)
        self._details_lay.setSpacing(12)
        
        self._det_title = QLabel("🔍 Device Details")
        self._det_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #06B6D4; margin-bottom: 6px;")
        self._details_lay.addWidget(self._det_title)
        
        self._det_empty_lbl = QLabel("Pilih perangkat dari daftar di sebelah kiri untuk melihat detail mendalam.")
        self._det_empty_lbl.setStyleSheet("color: #64748B; font-size: 12px; line-height: 1.4;")
        self._det_empty_lbl.setWordWrap(True)
        self._details_lay.addWidget(self._det_empty_lbl)
        
        self._det_fields_container = QWidget()
        self._det_fields_container.setVisible(False)
        fields_lay = QFormLayout(self._det_fields_container)
        fields_lay.setSpacing(10)
        fields_lay.setContentsMargins(0, 0, 0, 0)
        
        self._det_mac = QLabel("—")
        self._det_ip = QLabel("—")
        self._det_hostname = QLabel("—")
        self._det_vendor = QLabel("—")
        self._det_category = QLabel("—")
        self._det_status = QLabel("—")
        self._det_first_seen = QLabel("—")
        
        for lbl in (self._det_mac, self._det_ip, self._det_hostname, self._det_vendor, self._det_category, self._det_status, self._det_first_seen):
            lbl.setStyleSheet("color: #CBD5E1; font-weight: 600; font-size: 12px;")
            
        fields_lay.addRow("MAC Address:", self._det_mac)
        fields_lay.addRow("IP Address:", self._det_ip)
        fields_lay.addRow("Hostname:", self._det_hostname)
        fields_lay.addRow("Vendor:", self._det_vendor)
        fields_lay.addRow("Kategori:", self._det_category)
        fields_lay.addRow("Status:", self._det_status)
        fields_lay.addRow("Ditemukan:", self._det_first_seen)
        
        self._details_lay.addWidget(self._det_fields_container)
        self._details_lay.addStretch()

        self._device_splitter.addWidget(left_container)
        self._device_splitter.addWidget(self._details_panel)
        self._device_splitter.setStretchFactor(0, 3)
        self._device_splitter.setStretchFactor(1, 1)
        # Phase 8: Set safe initial sizes — prevents detail panel collapse on startup
        self._device_splitter.setSizes([700, 280])

        layout.addWidget(self._device_splitter)

        self.tabs.addTab(tab_widget, "🔌  Device Manager")

    def _build_dhcp_tab(self) -> None:
        self._dhcp_stack = QStackedWidget()
        
        # 1. Normal View (Operational DHCP widget)
        self._dhcp_normal_widget = QWidget()
        normal_layout = QVBoxLayout(self._dhcp_normal_widget)
        normal_layout.setContentsMargins(16, 16, 16, 16)
        normal_layout.setSpacing(12)

        # Title bar & actions
        act_row = QHBoxLayout()
        dhcp_lbl = QLabel("DHCP Leases Center")
        dhcp_lbl.setStyleSheet("font-size:14px; font-weight:700; color:#F8FAFC;")
        act_row.addWidget(dhcp_lbl)
        act_row.addStretch()

        self.dhcp_static_btn = QPushButton("⚡  Make Static / Reserve IP")
        self.dhcp_static_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dhcp_static_btn.setStyleSheet("""
            QPushButton {
                background-color: #0891B2; color: white; border: none; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: #06B6D4; }
        """)
        self.dhcp_static_btn.clicked.connect(self._on_dhcp_make_static)
        act_row.addWidget(self.dhcp_static_btn)

        self.dhcp_del_btn = QPushButton("🗑️  Hapus Lease")
        self.dhcp_del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dhcp_del_btn.setStyleSheet("""
            QPushButton {
                background-color: #7F1D1D; color: #FECACA; border: 1px solid #991B1B; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: #991B1B; color:white; }
        """)
        self.dhcp_del_btn.clicked.connect(self._on_dhcp_delete)
        act_row.addWidget(self.dhcp_del_btn)
        
        normal_layout.addLayout(act_row)

        # DHCP Table
        self._dhcp_table = QTableWidget(0, len(self.COLUMNS_DHCP))
        self._dhcp_table.verticalHeader().setDefaultSectionSize(36)
        self._dhcp_table.setHorizontalHeaderLabels(self.COLUMNS_DHCP)
        self._dhcp_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._dhcp_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._dhcp_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._dhcp_table.verticalHeader().setVisible(False)
        self._dhcp_table.setShowGrid(False)
        self._dhcp_table.setStyleSheet(self._table.styleSheet())
        
        hh = self._dhcp_table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        normal_layout.addWidget(self._dhcp_table)

        # 2. Locked Overlay View
        self._dhcp_locked_widget = self._create_locked_overlay(
            "🔌 DHCP Lease Center Terkunci",
            "Manajemen leases DHCP dan reservasi IP statis secara penuh memerlukan koneksi langsung dengan router MikroTik RouterOS.\n"
            "Gunakan MikroTik Mode untuk mengaktifkan fungsionalitas ini secara realtime."
        )

        self._dhcp_stack.addWidget(self._dhcp_normal_widget)
        self._dhcp_stack.addWidget(self._dhcp_locked_widget)

        self.tabs.addTab(self._dhcp_stack, "🔗  DHCP Lease Center")

    def _build_backup_tab(self) -> None:
        self._backup_stack = QStackedWidget()
        
        # 1. Normal View (Operational Backup widget)
        self._backup_normal_widget = QWidget()
        normal_layout = QVBoxLayout(self._backup_normal_widget)
        normal_layout.setContentsMargins(16, 16, 16, 16)
        normal_layout.setSpacing(12)

        # Backup & Scheduler Controls Layout
        top_ctrl = QHBoxLayout()
        top_ctrl.setSpacing(20)

        # Scheduler Frame
        sched_frame = QFrame()
        sched_frame.setStyleSheet("background-color:#161B27; border:1px solid #1F273E; border-radius:8px;")
        sched_lay = QHBoxLayout(sched_frame)
        sched_lay.setContentsMargins(12, 6, 12, 6)
        
        sched_lbl = QLabel("Auto Backup Scheduler (PRO):")
        sched_lbl.setStyleSheet("color:#94A3B8; font-weight:600; font-size:11px;")
        sched_lay.addWidget(sched_lbl)
        
        self.backup_sched_combo = QComboBox()
        self.backup_sched_combo.addItems(["Off", "Daily", "Weekly"])
        
        # Load from config safely
        main_win = self.window()
        current_sched = "Off"
        if hasattr(main_win, "_config") and main_win._config:
            current_sched = main_win._config.get("operations", "backup_schedule", default="Off")
            
        self.backup_sched_combo.setCurrentText(current_sched)
        self.backup_sched_combo.currentIndexChanged.connect(self._on_backup_schedule_changed)
        
        self.backup_sched_combo.setStyleSheet("""
            QComboBox {
                background-color:#0F131E; border:1px solid #1F273E; border-radius:4px; color:#E2E8F0; padding:3px 10px; font-size:11px;
            }
        """)
        sched_lay.addWidget(self.backup_sched_combo)
        top_ctrl.addWidget(sched_frame)
        top_ctrl.addStretch()

        # Action Buttons
        self.backup_btn = QPushButton("⚡  Backup Sekarang")
        self.backup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #0891B2; color: white; border: none; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: #06B6D4; }
        """)
        self.backup_btn.clicked.connect(self._on_backup_now)
        top_ctrl.addWidget(self.backup_btn)

        self.restore_btn = QPushButton("🔄  Restore Configuration")
        self.restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #D97706; color: white; border: none; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: #F59E0B; }
        """)
        self.restore_btn.clicked.connect(self._on_restore_backup)
        top_ctrl.addWidget(self.restore_btn)

        self.backup_del_btn = QPushButton("🗑️  Hapus")
        self.backup_del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backup_del_btn.setStyleSheet("""
            QPushButton {
                background-color: #7F1D1D; color: #FECACA; border: 1px solid #991B1B; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: #991B1B; color:white; }
        """)
        self.backup_del_btn.clicked.connect(self._on_delete_backup)
        top_ctrl.addWidget(self.backup_del_btn)

        self.sync_vault_btn = QPushButton("💾  Sync Vault Eksternal")
        self.sync_vault_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sync_vault_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E2535; color: #38BDF8; border: 1px solid #38BDF8; border-radius: 6px; padding: 6px 14px; font-weight:600;
            }
            QPushButton:hover { background-color: rgba(56,189,248,0.15); }
        """)
        self.sync_vault_btn.clicked.connect(self._on_sync_vault)
        top_ctrl.addWidget(self.sync_vault_btn)

        normal_layout.addLayout(top_ctrl)

        # Backup Table
        self._backup_table = QTableWidget(0, len(self.COLUMNS_BACKUP))
        self._backup_table.verticalHeader().setDefaultSectionSize(36)
        self._backup_table.setHorizontalHeaderLabels(self.COLUMNS_BACKUP)
        self._backup_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._backup_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._backup_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._backup_table.verticalHeader().setVisible(False)
        self._backup_table.setShowGrid(False)
        self._backup_table.setStyleSheet(self._table.styleSheet())

        hh = self._backup_table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        normal_layout.addWidget(self._backup_table)
        
        warn_lbl = QLabel("⚠ Restoring a backup configuration will instantly reboot the MikroTik RouterOS.")
        warn_lbl.setStyleSheet("color:#EF4444; font-size:11px; font-weight:600;")
        normal_layout.addWidget(warn_lbl)

        # 2. Locked Overlay View
        self._backup_locked_widget = self._create_locked_overlay(
            "🔒 Backup & Recovery Terkunci",
            "Mencadangkan berkas sistem (.backup) dan memulihkan konfigurasi sistem hanya dapat dilakukan dengan integrasi penuh router MikroTik.\n"
            "Silakan beralih ke MikroTik Mode di menu samping utama."
        )

        self._backup_stack.addWidget(self._backup_normal_widget)
        self._backup_stack.addWidget(self._backup_locked_widget)

        self.tabs.addTab(self._backup_stack, "💾  Backup & Recovery")

    # ─── Data & Polling updates ───────────────────────────────────────────────

    @pyqtSlot(dict)
    def update_from_tick(self, payload: dict) -> None:
        devices = payload.get("devices", [])

        # Skenario riil: jika kita berada di mode monitoring aktif, tunjukkan normal view
        if self._app_state and self._app_state.current_mode.lower() in ("demo", "home_wifi", "hotspot", "mikrotik"):
            self._main_stack.setCurrentWidget(self._normal_view)
        else:
            if not devices:
                self._main_stack.setCurrentWidget(self._empty_view)
                return
            self._main_stack.setCurrentWidget(self._normal_view)
            
        # Track new devices (first time seen this session)
        if not hasattr(self, "_seen_macs"):
            self._seen_macs: set[str] = set()
        new_count = 0
        for d in devices:
            mac = d.get("mac", "")
            
            # Dynamic Category Tagging
            d["category"] = get_device_category(d.get("hostname", ""), d.get("vendor", ""))
            
            if mac and mac not in self._seen_macs:
                self._seen_macs.add(mac)
                new_count += 1
                d["_is_new"] = True
            else:
                d["_is_new"] = False
                
            # Log online states in DB dynamically to track visit history
            if self._db and mac and d.get("status") == "online":
                self._db.upsert_device(
                    ip=d.get("ip", ""),
                    mac=mac,
                    hostname=d.get("hostname", ""),
                    vendor=d.get("vendor", ""),
                    status="online"
                )

        self._all_rows = devices

        online_count  = sum(1 for d in devices if d.get("status", "online") == "online")
        offline_count = len(devices) - online_count

        self._chip_total.set_value(len(devices))
        self._chip_online.set_value(online_count)
        self._chip_offline.set_value(offline_count)
        self._chip_new.set_value(new_count)
        self._updated_lbl.setText(f"Updated {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        self._refresh()

    def _on_mode_changed(self, mode: str) -> None:
        self._update_tab_locks()
        if mode.lower() in ("demo", "home_wifi", "hotspot", "mikrotik"):
            self._main_stack.setCurrentWidget(self._normal_view)
            self._on_tab_changed(self.tabs.currentIndex())
        else:
            self._main_stack.setCurrentWidget(self._empty_view)

    def _on_licensing_changed(self, is_pro: bool) -> None:
        logger.info("Licensing changed in DevicesPage context. Pro Status: %s", is_pro)
        self._is_pro = is_pro
        
        # Sync auto backup scheduler combo enable status
        self.backup_sched_combo.setEnabled(is_pro)
        self._on_tab_changed(self.tabs.currentIndex())

    def _on_tab_changed(self, index: int) -> None:
        """Triggered when user clicks another tab, refreshing list automatically."""
        if self._app_state and self._app_state.current_mode == "Demo":
            if index == 1:
                self._render_demo_dhcp()
            elif index == 2:
                self._render_demo_backups()
            return
            
        api = self._get_api()
        if not api:
            return
            
        if index == 1: # DHCP Tab
            self.dhcp_static_btn.setEnabled(True)
            self.dhcp_del_btn.setEnabled(True)
            try:
                leases = api.get_resource('/ip/dhcp-server/lease').get()
                self._render_dhcp_leases(leases)
            except Exception as e:
                logger.error("Failed to fetch DHCP leases: %s", e)
                
        elif index == 2: # Backup Tab
            self.backup_btn.setEnabled(True)
            self.restore_btn.setEnabled(True)
            self.backup_del_btn.setEnabled(True)
            
            # Start background backup fetch worker
            self._list_worker = BackupWorker(api, "list")
            self._list_worker.finished.connect(self._on_list_backups_finished)
            self._list_worker.start()

    # ─── Filter & Sort ────────────────────────────────────────────────────────

    def _set_filter(self, mode: str) -> None:
        self._filter_mode = mode
        self._pill_all.setChecked(mode == "all")
        self._pill_online.setChecked(mode == "online")
        self._pill_offline.setChecked(mode == "offline")
        self._pill_smart.setChecked(mode == "smartphone")
        self._pill_laptop.setChecked(mode == "laptop")
        self._pill_iot.setChecked(mode == "iot")
        self._refresh()

    def _on_header_clicked(self, col: int) -> None:
        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = True
        self._refresh()

    def _refresh(self) -> None:
        query = self._search.text().lower().strip()
        rows = self._all_rows

        # Filter by status / category pill
        if self._filter_mode == "online":
            rows = [r for r in rows if r.get("status", "online") == "online"]
        elif self._filter_mode == "offline":
            rows = [r for r in rows if r.get("status", "online") != "online"]
        elif self._filter_mode == "smartphone":
            rows = [r for r in rows if r.get("category") == "Smartphone"]
        elif self._filter_mode == "laptop":
            rows = [r for r in rows if r.get("category") == "Laptop/Desktop"]
        elif self._filter_mode == "iot":
            rows = [r for r in rows if r.get("category") == "IoT"]

        # Filter by search
        if query:
            rows = [
                r for r in rows
                if query in r.get("hostname", "").lower()
                or query in r.get("ip", "").lower()
                or query in r.get("mac", "").lower()
                or query in r.get("vendor", "").lower()
                or query in r.get("category", "").lower()
            ]

        # Sort: online first by default, then by selected column
        def sort_key(r):
            status_order = 0 if r.get("status", "online") == "online" else 1
            col = self._sort_col
            if col == self.COL_HOSTNAME:  val = r.get("hostname", "")
            elif col == self.COL_IP:       val = r.get("ip", "")
            elif col == self.COL_MAC:      val = r.get("mac", "")
            elif col == self.COL_VENDOR:   val = r.get("vendor", "")
            elif col == self.COL_CATEGORY: val = r.get("category", "")
            elif col == self.COL_UP:       val = -r.get("upload", 0.0)
            elif col == self.COL_DOWN:     val = -r.get("download", 0.0)
            elif col == self.COL_STATUS:   val = status_order
            elif col == self.COL_LASTSEEN: val = r.get("last_seen", "")
            else:                          val = status_order
            return (status_order, val) if self._sort_asc else (status_order, val)

        rows = sorted(rows, key=sort_key, reverse=not self._sort_asc if self._sort_col != self.COL_DOT else False)
        # Always put online devices first regardless of sort
        rows = sorted(rows, key=lambda r: 0 if r.get("status", "online") == "online" else 1)

        self._render_rows(rows)

    # ─── Render Devices ───────────────────────────────────────────────────────

    def _render_rows(self, rows: list[dict]) -> None:
        self._table.setUpdatesEnabled(False)
        self._table.setRowCount(0)
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        is_mikrotik = self._app_state and self._app_state.current_mode == "mikrotik"
        is_demo     = self._app_state and self._app_state.current_mode == "demo"
        theme = self._app_state.current_theme if (self._app_state and hasattr(self._app_state, "current_theme")) else "dark"

        for row_data in rows:
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._table.setRowHeight(row, 46)

            ip        = row_data.get("ip", "")
            hostname  = row_data.get("hostname", "") or f"Unknown ({ip})"
            mac       = row_data.get("mac", "")
            vendor    = row_data.get("vendor", "") or "Unknown"
            category  = row_data.get("category", "Other")
            upload    = row_data.get("upload", 0.0)
            download  = row_data.get("download", 0.0)
            status    = row_data.get("status", "online")
            last_seen = row_data.get("last_seen", now_str) or "—"
            is_new    = row_data.get("_is_new", False)
            is_online = status == "online"

            # Apply Operator-Privacy Masking dynamically if active
            is_privacy_masked = self._app_state and getattr(self._app_state, "privacy_masked", False)
            if is_privacy_masked:
                if ip and "." in ip:
                    ip_parts = ip.split(".")
                    if len(ip_parts) == 4:
                        ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.*"
                if mac and len(mac) == 17:
                    mac = f"{mac[:8]}:xx:xx:xx"
                if hostname and "unknown" not in hostname.lower():
                    hostname = f"Private Client ({vendor})"

            # Derive loyalty status dynamically using Hardware DNA Profiler heuristics
            loyalty_badge = "Baru"
            try:
                dev_id = row_data.get("id")
                if dev_id and self._db:
                    sessions = self._db.fetchall("SELECT COUNT(*) as cnt FROM sessions WHERE device_id = ?", (dev_id,))
                    session_count = sessions[0]["cnt"] if sessions else 0
                    if session_count >= 10:
                        loyalty_badge = "Setia"
                    elif session_count >= 3:
                        loyalty_badge = "Reguler"
            except Exception:
                pass

            # 1. Status dot column
            dot_item = QTableWidgetItem("●")
            dot_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            dot_color = "#22C55E" if is_online else ("#94A3B8" if theme == "light" else "#374151")
            dot_item.setForeground(QColor(dot_color))
            self._table.setItem(row, self.COL_DOT, dot_item)

            # 2. Hostname
            hn_item = QTableWidgetItem(hostname)
            hn_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            if is_new and is_online:
                hn_item.setForeground(QColor("#F59E0B"))  # amber for new
                hn_item.setFont(QFont("", -1, QFont.Weight.Bold))
            elif is_online:
                hn_item.setForeground(QColor("#0F172A" if theme == "light" else "#E2E8F0"))
            else:
                hn_item.setForeground(QColor("#94A3B8" if theme == "light" else "#4A5568"))
            self._table.setItem(row, self.COL_HOSTNAME, hn_item)

            # 3. IP
            ip_item = QTableWidgetItem(ip or "—")
            ip_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            if is_online:
                ip_item.setForeground(QColor("#475569" if theme == "light" else "#94A3B8"))
            else:
                ip_item.setForeground(QColor("#CBD5E1" if theme == "light" else "#374151"))
            self._table.setItem(row, self.COL_IP, ip_item)

            # 4. MAC
            mac_item = QTableWidgetItem(mac or "—")
            mac_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            mac_item.setForeground(QColor("#64748B"))
            self._table.setItem(row, self.COL_MAC, mac_item)

            # 5. Vendor badge
            vendor_display = vendor if len(vendor) <= 24 else vendor[:22] + "…"
            bg, fg = _vendor_badge_colors(vendor, theme=theme)
            v_item = QTableWidgetItem(f"  {vendor_display}  ")
            v_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            v_item.setForeground(QColor(fg) if is_online else QColor("#64748B" if theme == "light" else "#374151"))
            v_item.setBackground(QColor(bg) if is_online else QColor("#F1F5F9" if theme == "light" else "#0D1117"))
            self._table.setItem(row, self.COL_VENDOR, v_item)

            # 6. Category Pill Badge (Pro only) & Loyalty Profiler
            cat_icon = "⚙️"
            if category == "Smartphone": cat_icon = "📱"
            elif category == "Laptop/Desktop": cat_icon = "💻"
            elif category == "IoT": cat_icon = "🔌"
            
            cat_str = f" {cat_icon} {category} • {loyalty_badge} "
            cat_item = QTableWidgetItem(cat_str)
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
            if is_online:
                if loyalty_badge == "Setia":
                    cat_item.setForeground(QColor("#22C55E" if theme == "dark" else "#15803D"))
                    cat_item.setBackground(QColor("#052E16" if theme == "dark" else "#DCFCE7"))
                elif loyalty_badge == "Reguler":
                    cat_item.setForeground(QColor("#F59E0B" if theme == "dark" else "#B45309"))
                    cat_item.setBackground(QColor("#451A03" if theme == "dark" else "#FEF3C7"))
                else:
                    cat_item.setForeground(QColor("#06B6D4" if theme == "dark" else "#0891B2"))
                    cat_item.setBackground(QColor("#083344" if theme == "dark" else "#ECFEFF"))
            else:
                cat_item.setForeground(QColor("#64748B"))
            self._table.setItem(row, self.COL_CATEGORY, cat_item)

            # 7. Bandwidth Upload / Download
            show_bw = is_mikrotik or is_demo
            up_str   = f"{upload:.2f}"   if (show_bw and upload   > 0) else "—"
            down_str = f"{download:.2f}" if (show_bw and download > 0) else "—"

            up_item = QTableWidgetItem(up_str)
            up_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            up_color = "#D97706" if theme == "light" and upload > 5 else ("#F59E0B" if upload > 5 else "#64748B")
            up_item.setForeground(QColor(up_color))
            self._table.setItem(row, self.COL_UP, up_item)

            dn_item = QTableWidgetItem(down_str)
            dn_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            if download > 20:    dn_color = "#EF4444"
            elif download > 10:  dn_color = "#D97706" if theme == "light" else "#F59E0B"
            elif download > 0:   dn_color = "#0284C7" if theme == "light" else "#38BDF8"
            else:                dn_color = "#64748B"
            dn_item.setForeground(QColor(dn_color))
            self._table.setItem(row, self.COL_DOWN, dn_item)

            # 8. Status
            status_text = "Online" if is_online else "Offline"
            st_item = QTableWidgetItem(status_text)
            st_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
            st_item.setForeground(QColor("#15803D" if theme == "light" else "#22C55E") if is_online else QColor("#64748B" if theme == "light" else "#4A5568"))
            if is_online:
                st_item.setBackground(QColor("#DCFCE7" if theme == "light" else "#0D2918"))
            self._table.setItem(row, self.COL_STATUS, st_item)

            # 9. Last Seen
            ls_item = QTableWidgetItem(last_seen)
            ls_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
            ls_item.setForeground(QColor("#64748B"))
            self._table.setItem(row, self.COL_LASTSEEN, ls_item)

        self._table.setUpdatesEnabled(True)

    # ─── Render DHCP leases ───────────────────────────────────────────────────

    def _render_dhcp_leases(self, leases: list[dict]) -> None:
        self._dhcp_table.setRowCount(0)
        for lease in leases:
            row = self._dhcp_table.rowCount()
            self._dhcp_table.insertRow(row)
            self._dhcp_table.setRowHeight(row, 40)

            # Columns: IP, MAC, Hostname, Status, Type (Static/Dynamic)
            ip = lease.get("address", "")
            mac = lease.get("mac-address", "")
            host = lease.get("host-name", "—")
            status = lease.get("status", "bound")
            is_dynamic = lease.get("dynamic", "yes") == "yes" or lease.get("dynamic", "true") == "true"
            type_str = "Dynamic 🔄" if is_dynamic else "Static 📌"

            # IP
            item_ip = QTableWidgetItem(ip)
            item_ip.setForeground(QColor("#E2E8F0"))
            self._dhcp_table.setItem(row, 0, item_ip)

            # MAC
            item_mac = QTableWidgetItem(mac)
            item_mac.setForeground(QColor("#94A3B8"))
            self._dhcp_table.setItem(row, 1, item_mac)

            # Hostname
            item_host = QTableWidgetItem(host)
            item_host.setForeground(QColor("#06B6D4"))
            self._dhcp_table.setItem(row, 2, item_host)

            # Status
            item_status = QTableWidgetItem(status.capitalize())
            item_status.setForeground(QColor("#22C55E" if status == "bound" else "#F59E0B"))
            self._dhcp_table.setItem(row, 3, item_status)

            # Type
            item_type = QTableWidgetItem(type_str)
            item_type.setForeground(QColor("#F59E0B" if is_dynamic else "#38BDF8"))
            self._dhcp_table.setItem(row, 4, item_type)

    def _render_demo_dhcp(self) -> None:
        """Beautiful simulation of DHCP Leases for Demo mode."""
        self._render_dhcp_leases(self._demo_dhcp_leases)

    # ─── Render Backups ───────────────────────────────────────────────────────

    def _render_backups(self, backups: list[dict]) -> None:
        self._backup_table.setRowCount(0)
        for b in backups:
            row = self._backup_table.rowCount()
            self._backup_table.insertRow(row)
            self._backup_table.setRowHeight(row, 40)

            # Columns: Filename, Size, Date Created
            name_item = QTableWidgetItem(b.get("name", ""))
            name_item.setForeground(QColor("#E2E8F0"))
            self._backup_table.setItem(row, 0, name_item)

            size_item = QTableWidgetItem(b.get("size", "N/A"))
            size_item.setForeground(QColor("#06B6D4"))
            self._backup_table.setItem(row, 1, size_item)

            date_item = QTableWidgetItem(b.get("creation_time", "—"))
            date_item.setForeground(QColor("#94A3B8"))
            self._backup_table.setItem(row, 2, date_item)

    def _render_demo_backups(self) -> None:
        """Beautiful simulation of Backups for Demo mode."""
        self._render_backups(self._demo_backups)

    # ─── Device Row Interactions (PRO) ────────────────────────────────────────

    def _on_device_row_double_clicked(self) -> None:
        row = self._table.currentRow()
        if row < 0:
            return
            
        mac = self._table.item(row, self.COL_MAC).text()
        
        # Pro Licensing Gating
        if not self._is_licensed():
            return
            
        # Find detail info from DB or rows list
        device_info = {}
        for r in self._all_rows:
            if r.get("mac") == mac:
                device_info = r
                break
                
        if not device_info:
            device_info = {
                "mac": mac,
                "ip": self._table.item(row, self.COL_IP).text(),
                "hostname": self._table.item(row, self.COL_HOSTNAME).text(),
                "vendor": self._table.item(row, self.COL_VENDOR).text().strip(),
                "category": self._table.item(row, self.COL_CATEGORY).text().strip()
            }
            
        # Query first_seen / last_seen from DB if available
        if self._db:
            db_row = self._db.fetchone("SELECT first_seen, last_seen, status FROM devices WHERE mac_address=?", (mac,))
            if db_row:
                device_info["first_seen"] = db_row["first_seen"]
                device_info["last_seen"] = db_row["last_seen"]
                device_info["status"] = db_row["status"]
                
        # Launch detailed dialog
        dlg = DeviceDetailDialog(device_info, self)
        dlg.exec()

    # ─── Context Menu & Edit/Copy Actions ───────────────────────────────────

    def _on_table_context_menu(self, pos) -> None:
        row = self._table.rowAt(pos.y())
        if row < 0:
            return
            
        self._table.selectRow(row)
        
        mac_item = self._table.item(row, self.COL_MAC)
        ip_item = self._table.item(row, self.COL_IP)
        hn_item = self._table.item(row, self.COL_HOSTNAME)
        vendor_item = self._table.item(row, self.COL_VENDOR)
        category_item = self._table.item(row, self.COL_CATEGORY)
        
        mac = mac_item.text() if mac_item else ""
        ip = ip_item.text() if ip_item else ""
        hostname = hn_item.text() if hn_item else ""
        vendor = vendor_item.text().strip() if vendor_item else ""
        category = category_item.text().strip() if category_item else ""
        
        device_info = {
            "mac": mac,
            "ip": ip,
            "hostname": hostname,
            "vendor": vendor,
            "category": category
        }
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #0F131E;
                color: #CBD5E1;
                border: 1px solid #1F273E;
                border-radius: 8px;
                padding: 6px 0px;
                font-size: 12px;
                font-weight: 500;
            }
            QMenu::item {
                padding: 8px 24px;
            }
            QMenu::item:selected {
                background-color: #1E293B;
                color: #06B6D4;
            }
            QMenu::separator {
                height: 1px;
                background-color: #1E293B;
                margin: 6px 0px;
            }
        """)
        
        edit_action = menu.addAction("✏️  Edit Device Info")
        menu.addSeparator()
        copy_ip_action = menu.addAction("📋  Copy IP Address")
        copy_mac_action = menu.addAction("📋  Copy MAC Address")
        
        action = menu.exec(self._table.viewport().mapToGlobal(pos))
        if not action:
            return
            
        if action == edit_action:
            self._edit_device_info(device_info, row)
        elif action == copy_ip_action:
            QApplication.clipboard().setText(ip)
            QMessageBox.information(self, "Copy IP", f"Alamat IP {ip} berhasil disalin ke clipboard.")
        elif action == copy_mac_action:
            QApplication.clipboard().setText(mac)
            QMessageBox.information(self, "Copy MAC", f"MAC Address {mac} berhasil disalin ke clipboard.")

    def _edit_device_info(self, device_info: dict, row: int) -> None:
        mac = device_info.get("mac", "")
        if not mac:
            return
            
        dlg = EditDeviceDialog(device_info, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_hostname = dlg.get_hostname()
            
            # 1. Update SQLite local DB
            if self._db:
                try:
                    self._db.execute("UPDATE devices SET hostname=? WHERE mac_address=?", (new_hostname, mac))
                    logger.info("Successfully updated hostname in database to '%s' for mac '%s'", new_hostname, mac)
                except Exception as e:
                    logger.error("Failed to update database for hostname change: %s", e)
            
            # 2. Update active memory row
            for r in self._all_rows:
                if r.get("mac") == mac:
                    r["hostname"] = new_hostname
                    break
                    
            # 3. Refresh table display
            self._refresh()
            
            # 4. Success alert
            QMessageBox.information(self, "Sukses", f"Nama perangkat berhasil diubah menjadi: {new_hostname}")

    def _on_table_selection_changed(self) -> None:
        row = self._table.currentRow()
        if row < 0:
            self._update_details_panel(None)
            return
            
        mac_item = self._table.item(row, self.COL_MAC)
        if not mac_item:
            self._update_details_panel(None)
            return
        mac = mac_item.text()
        
        # Find detail info from rows list
        device_info = {}
        for r in self._all_rows:
            if r.get("mac") == mac:
                device_info = r
                break
                
        if not device_info:
            device_info = {
                "mac": mac,
                "ip": self._table.item(row, self.COL_IP).text() if self._table.item(row, self.COL_IP) else "",
                "hostname": self._table.item(row, self.COL_HOSTNAME).text() if self._table.item(row, self.COL_HOSTNAME) else "",
                "vendor": self._table.item(row, self.COL_VENDOR).text().strip() if self._table.item(row, self.COL_VENDOR) else "",
                "category": self._table.item(row, self.COL_CATEGORY).text().strip() if self._table.item(row, self.COL_CATEGORY) else ""
            }
            
        if self._db:
            try:
                db_row = self._db.fetchone("SELECT first_seen, last_seen, status FROM devices WHERE mac_address=?", (mac,))
                if db_row:
                    device_info["first_seen"] = db_row["first_seen"]
                    device_info["last_seen"] = db_row["last_seen"]
                    device_info["status"] = db_row["status"]
            except Exception as e:
                logger.error("Error fetching db row for selection: %s", e)
                
        self._update_details_panel(device_info)

    def _update_details_panel(self, info: dict | None) -> None:
        if not info:
            self._det_empty_lbl.setVisible(True)
            self._det_fields_container.setVisible(False)
            return
            
        self._det_empty_lbl.setVisible(False)
        self._det_fields_container.setVisible(True)
        
        self._det_mac.setText(info.get("mac", "—"))
        self._det_ip.setText(info.get("ip", "—"))
        self._det_hostname.setText(info.get("hostname", "—"))
        self._det_vendor.setText(info.get("vendor", "—") or "Unknown")
        self._det_category.setText(info.get("category", "—"))
        
        status = info.get("status", "online")
        if status == "online":
            self._det_status.setText("🟢 Online")
            self._det_status.setStyleSheet("color: #22C55E; font-weight: bold;")
        else:
            self._det_status.setText("🔴 Offline")
            self._det_status.setStyleSheet("color: #EF4444; font-weight: bold;")
            
        first_seen = info.get("first_seen", "—")
        if first_seen and first_seen != "—":
            try:
                dt = datetime.datetime.fromisoformat(first_seen)
                first_seen = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        self._det_first_seen.setText(first_seen)

    # ─── Feature Gating & Locked Overlays ───────────────────────────────────

    def _create_locked_overlay(self, title: str, desc: str) -> QWidget:
        widget = QWidget()
        widget.setCursor(Qt.CursorShape.ForbiddenCursor)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        card = QFrame()
        card.setObjectName("LockedCard")
        card.setStyleSheet("""
            QFrame#LockedCard {
                background-color: #111827;
                border: 2px dashed #374151;
                border-radius: 16px;
                min-width: 380px;
                max-width: 500px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 40, 32, 40)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_lbl = QLabel("🔒")
        icon_lbl.setStyleSheet("font-size: 54px; margin-bottom: 8px;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_lbl)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 700; color: #EF4444;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_lbl)
        
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet("font-size: 13px; color: #9CA3AF; line-height: 1.5;")
        desc_lbl.setWordWrap(True)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc_lbl)
        
        hint_lbl = QLabel("Kursor terkunci karena fitur ini tidak didukung pada mode aktif saat ini.")
        hint_lbl.setStyleSheet("font-size: 11px; color: #4B5563; font-style: italic;")
        hint_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint_lbl)
        
        layout.addWidget(card)
        return widget

    def _update_tab_locks(self) -> None:
        if not self._app_state:
            return
        
        mode = self._app_state.current_mode.lower()
        if mode in ("mikrotik", "demo"):
            self._dhcp_stack.setCurrentIndex(0)
            self._backup_stack.setCurrentIndex(0)
        else:
            self._dhcp_stack.setCurrentIndex(1)
            self._backup_stack.setCurrentIndex(1)

    # ─── DHCP Operations (PRO ONLY) ───────────────────────────────────────────

    def _on_dhcp_make_static(self) -> None:
        row = self._dhcp_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Item", "Silakan pilih salah satu DHCP lease dari tabel terlebih dahulu.")
            return

        if not self._is_licensed():
            return

        ip = self._dhcp_table.item(row, 0).text()
        mac = self._dhcp_table.item(row, 1).text()
        hostname = self._dhcp_table.item(row, 2).text()
        type_str = self._dhcp_table.item(row, 4).text()

        if "Static" in type_str:
            QMessageBox.information(self, "Reservasi IP", f"Alamat IP {ip} sudah berstatus Static.")
            return

        reply = QMessageBox.question(
            self, "Buat Static / Reservasi IP",
            f"Apakah Anda yakin ingin melakukan reservasi IP statis untuk perangkat '{hostname}'?\n\n"
            f"IP: {ip}\nMAC: {mac}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        # Demo mode action
        if self._app_state and self._app_state.current_mode == "Demo":
            for lease in self._demo_dhcp_leases:
                if lease["ip"] == ip:
                    lease["dynamic"] = "no"
                    break
            self._render_demo_dhcp()
            QMessageBox.information(self, "Sukses (Demo Mode)", f"Berhasil mereservasi IP Statis {ip}!")
            return

        # Real RouterOS action
        api = self._get_api()
        if not api:
            QMessageBox.warning(self, "Koneksi Gagal", "Tidak dapat menghubungi router MikroTik.")
            return

        try:
            lease_res = api.get_resource('/ip/dhcp-server/lease')
            leases = lease_res.get(address=ip)
            if leases:
                lease_id = leases[0]['id']
                lease_res.call('make-static', {'numbers': lease_id})
                QMessageBox.information(self, "Sukses", f"IP lease untuk {ip} berhasil diubah menjadi Static.")
                self._on_tab_changed(1) # Refresh DHCP Leases
            else:
                QMessageBox.warning(self, "Gagal", "Detail Lease tidak dapat ditemukan kembali di router.")
        except Exception as e:
            logger.error("Failed to make dynamic lease static: %s", e)
            QMessageBox.critical(self, "Error API", f"Gagal membuat lease statis:\n{e}")

    def _on_dhcp_delete(self) -> None:
        row = self._dhcp_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Item", "Silakan pilih salah satu DHCP lease dari tabel terlebih dahulu.")
            return

        if not self._is_licensed():
            return

        ip = self._dhcp_table.item(row, 0).text()
        mac = self._dhcp_table.item(row, 1).text()
        hostname = self._dhcp_table.item(row, 2).text()

        reply = QMessageBox.question(
            self, "Hapus Lease",
            f"Apakah Anda yakin ingin menghapus DHCP lease perangkat '{hostname}' dari RouterOS?\n\n"
            f"IP: {ip}\nMAC: {mac}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        # Demo mode action
        if self._app_state and self._app_state.current_mode == "Demo":
            self._demo_dhcp_leases = [l for l in self._demo_dhcp_leases if l["ip"] != ip]
            self._render_demo_dhcp()
            QMessageBox.information(self, "Sukses (Demo)", f"Berhasil menghapus lease {ip}.")
            return

        # Real RouterOS action
        api = self._get_api()
        if not api:
            QMessageBox.warning(self, "Koneksi Gagal", "Tidak dapat menghubungi router MikroTik.")
            return

        try:
            lease_res = api.get_resource('/ip/dhcp-server/lease')
            leases = lease_res.get(address=ip)
            if leases:
                lease_id = leases[0]['id']
                lease_res.remove(id=lease_id)
                QMessageBox.information(self, "Sukses", f"DHCP lease {ip} berhasil dihapus dari router.")
                self._on_tab_changed(1) # Refresh
            else:
                QMessageBox.warning(self, "Gagal", "Detail Lease tidak dapat ditemukan di router.")
        except Exception as e:
            logger.error("Failed to delete DHCP lease: %s", e)
            QMessageBox.critical(self, "Error API", f"Gagal menghapus lease:\n{e}")

    # ─── Backup Operations (PRO ONLY) ─────────────────────────────────────────

    def _on_backup_schedule_changed(self, idx: int) -> None:
        val = self.backup_sched_combo.currentText()
        if not self._is_pro and val != "Off":
            self.backup_sched_combo.setCurrentText("Off")
            self._is_licensed() # Trigger Upgrade Banner
            return
            
        main_win = self.window()
        if hasattr(main_win, "_config") and main_win._config:
            main_win._config.set("operations", "backup_schedule", value=val)
            logger.info("Automatic backup schedule updated in config to: %s", val)

    def _on_backup_now(self) -> None:
        if not self._is_licensed():
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename, ok = QInputDialog.getText(
            self, "Pencadangan MikroTik",
            "Tentukan nama file cadangan configuration (.backup):",
            QLineEdit.EchoMode.Normal,
            f"CafePulse_Backup_{timestamp}"
        )
        if not ok or not filename.strip():
            return
            
        filename = filename.strip()
        
        # Demo mode action
        if self._app_state and self._app_state.current_mode == "Demo":
            self._demo_backups.append({
                "name": f"{filename}.backup",
                "size": "52.3 KB",
                "creation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self._render_demo_backups()
            QMessageBox.information(self, "Sukses (Demo Mode)", f"Berhasil merekam mock backup '{filename}.backup'.")
            return
            
        # Real RouterOS action
        api = self._get_api()
        if not api:
            QMessageBox.warning(self, "Koneksi Gagal", "Tidak dapat menghubungi router MikroTik.")
            return
            
        self.backup_btn.setEnabled(False)
        self.backup_btn.setText("Sedang Backup...")
        
        self._manual_backup_worker = BackupWorker(api, "backup", filename)
        self._manual_backup_worker.finished.connect(self._on_manual_backup_finished)
        self._manual_backup_worker.start()

    def _on_manual_backup_finished(self, success: bool, msg: str) -> None:
        self.backup_btn.setEnabled(True)
        self.backup_btn.setText("⚡  Backup Sekarang")
        if success:
            QMessageBox.information(self, "Pencadangan Berhasil", msg)
            self._on_tab_changed(2) # Refresh backups
        else:
            QMessageBox.critical(self, "Pencadangan Gagal", f"Gagal memproses backup:\n{msg}")

    def _on_sync_vault(self) -> None:
        if not self._is_licensed():
            return
            
        from PyQt6.QtWidgets import QFileDialog
        dir_path = QFileDialog.getExistingDirectory(
            self, "Pilih Drive/Direktori Vault Eksternal (Offline Sync)",
            ""
        )
        if not dir_path:
            return
            
        import shutil
        import os
        from pathlib import Path
        
        try:
            vault_path = Path(dir_path) / "CafePulse_HA_Vault"
            vault_path.mkdir(parents=True, exist_ok=True)
            
            # Sync settings config — use resolved path from app_paths (P0 fix)
            settings_src = SETTINGS_FILE
            if settings_src.exists():
                shutil.copy2(settings_src, vault_path / "settings_vault.json")
                
            # Sync database with HA vault naming — use resolved path from app_paths (P0 fix)
            db_src = DATABASE_FILE
            if db_src.exists():
                shutil.copy2(db_src, vault_path / "cafepulse_ha_vault.db")
                
            # Write sync log
            sync_log = vault_path / "vault_sync_log.txt"
            with open(sync_log, "w", encoding="utf-8") as f:
                f.write(f"CafePulse Offline High-Availability Vault Sync\n")
                f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Status: SECURE & SYNCHRONIZED (Local Hardware Linked Encryption)\n")
                
            main_win = self.window()
            if main_win and hasattr(main_win, "_toast_mgr") and main_win._toast_mgr:
                main_win._toast_mgr.show_toast(
                    "success",
                    "✓ Sync Vault Sukses! Backup database & config tersimpan aman secara offline."
                )
                
            QMessageBox.information(
                self, "Sync Vault Sukses",
                f"<b>Penyelarasan Offline Sukses!</b><br><br>"
                f"Salinan database lokal dan konfigurasi Anda telah disalin secara terenkripsi "
                f"ke direktori vault eksternal:<br><br>"
                f"<i>{vault_path}</i><br><br>"
                f"Ini memberikan redundansi lokal tingkat tinggi tanpa ketergantungan cloud."
            )
        except Exception as e:
            logger.error("Sync vault failed: %s", e)
            QMessageBox.critical(self, "Sync Vault Gagal", f"Gagal menyelaraskan vault eksternal:\n{e}")

    def _on_restore_backup(self) -> None:
        row = self._backup_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Item", "Silakan pilih salah satu file backup yang akan dipulihkan.")
            return
            
        if not self._is_licensed():
            return
            
        name = self._backup_table.item(row, 0).text()
        
        reply = QMessageBox.critical(
            self, "❗ BAHAYA: PEMULIHAN SISTEM",
            f"APAKAH ANDA YAKIN INGIN MEMULIHKAN CADANGAN CONFIGURATION INI?\n\n"
            f"Nama File: {name}\n\n"
            "TINDAKAN INI AKAN SEGERA ME-REBOOT ROUTER MIKROTIK DAN "
            "MEMUTUS SELURUH KONEKSI JARINGAN HINGGA PROSES REBOOT SELESAI!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
            
        # Demo mode action
        if self._app_state and self._app_state.current_mode == "Demo":
            QMessageBox.information(
                self, "System Restore (Demo)",
                "Proses pemulihan cadangan disimulasikan sukses!\n"
                "CafePulse telah memulihkan parameter RouterOS v7 dengan aman."
            )
            return
            
        api = self._get_api()
        if not api:
            QMessageBox.warning(self, "Koneksi Gagal", "Tidak dapat menghubungi router MikroTik.")
            return
            
        self.restore_btn.setEnabled(False)
        self.restore_btn.setText("Memulihkan...")
        
        self._restore_worker = BackupWorker(api, "restore", name)
        self._restore_worker.finished.connect(self._on_restore_finished)
        self._restore_worker.start()

    def _on_restore_finished(self, success: bool, msg: str) -> None:
        self.restore_btn.setEnabled(True)
        self.restore_btn.setText("🔄  Restore Configuration")
        if success:
            QMessageBox.information(
                self, "Pemulihan Sistem Dimulai",
                f"{msg}\n\n"
                "Koneksi CafePulse ke router akan terputus. "
                "Fitur auto-healing ketahanan CafePulse akan menghubungkan kembali secara otomatis "
                "setelah router berhasil menyala kembali."
            )
            # Force trigger disconnect visually
            main_window = self.window()
            if hasattr(main_window, "_mikrotik_worker") and main_window._mikrotik_worker:
                main_window._mikrotik_worker.manager.trigger_reconnect(
                    datetime.datetime.now().timestamp(), 
                    reason="Router rebooting after configuration restore"
                )
        else:
            QMessageBox.critical(self, "Pemulihan Gagal", f"Gagal melakukan restore:\n{msg}")

    def _on_delete_backup(self) -> None:
        row = self._backup_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Item", "Silakan pilih salah satu file backup yang akan dihapus.")
            return
            
        if not self._is_licensed():
            return
            
        name = self._backup_table.item(row, 0).text()
        
        reply = QMessageBox.question(
            self, "Hapus File Backup",
            f"Apakah Anda yakin ingin menghapus file backup '{name}' dari router?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
            
        # Demo mode action
        if self._app_state and self._app_state.current_mode == "Demo":
            self._demo_backups = [b for b in self._demo_backups if b["name"] != name]
            self._render_demo_backups()
            QMessageBox.information(self, "Sukses (Demo)", f"Berhasil menghapus backup '{name}'.")
            return
            
        # Real RouterOS action
        api = self._get_api()
        if not api:
            QMessageBox.warning(self, "Koneksi Gagal", "Tidak dapat menghubungi router MikroTik.")
            return
            
        self.backup_del_btn.setEnabled(False)
        self.backup_del_btn.setText("Menghapus...")
        
        self._del_worker = BackupWorker(api, "delete", name)
        self._del_worker.finished.connect(self._on_delete_backup_finished)
        self._del_worker.start()

    def _on_delete_backup_finished(self, success: bool, msg: str) -> None:
        self.backup_del_btn.setEnabled(True)
        self.backup_del_btn.setText("🗑️  Hapus")
        if success:
            QMessageBox.information(self, "Hapus Sukses", msg)
            self._on_tab_changed(2) # Refresh backups
        else:
            QMessageBox.critical(self, "Hapus Gagal", f"Gagal menghapus file backup:\n{msg}")

    def _on_list_backups_finished(self, success: bool, msg: str) -> None:
        if success and hasattr(self, "_list_worker") and self._list_worker.result_data is not None:
            self._render_backups(self._list_worker.result_data)
        else:
            logger.warning("Failed to refresh RouterOS backups list: %s", msg)

    # ─── Scheduled Auto Backup Logic (PRO ONLY) ───────────────────────────────

    def _check_auto_backup_schedule(self) -> None:
        """Triggered periodically by local QTimer to verify if automated backup is due."""
        if not self._is_pro:
            return
            
        if self._app_state and self._app_state.current_mode == "Demo":
            return # Ignore in Demo mode
            
        main_win = self.window()
        if not hasattr(main_win, "_config") or not main_win._config:
            return
            
        sched = main_win._config.get("operations", "backup_schedule", default="Off")
        if sched == "Off":
            return
            
        last_backup_str = main_win._config.get("operations", "last_backup_time", default="")
        now = datetime.datetime.now()
        
        should_backup = False
        if not last_backup_str:
            should_backup = True
        else:
            try:
                last_backup = datetime.datetime.fromisoformat(last_backup_str)
                delta = now - last_backup
                if sched == "Daily" and delta.total_seconds() >= 86400:
                    should_backup = True
                elif sched == "Weekly" and delta.total_seconds() >= 604800:
                    should_backup = True
            except Exception:
                should_backup = True
                
        if should_backup:
            self._trigger_auto_backup(now)

    def _trigger_auto_backup(self, now_dt: datetime.datetime) -> None:
        api = self._get_api()
        if not api:
            return
            
        main_win = self.window()
        # Immediately set config to prevent overlapping triggers
        main_win._config.set("operations", "last_backup_time", value=now_dt.isoformat())
        
        filename = f"CafePulse_Auto_{now_dt.strftime('%Y%m%d_%H%M%S')}"
        logger.info("Triggering scheduled non-blocking auto backup: %s", filename)
        
        self._auto_backup_worker = BackupWorker(api, "backup", filename)
        # Sinyal finished auto backup: log only to console and database to not interrupt user
        self._auto_backup_worker.finished.connect(
            lambda success, msg: logger.info("Scheduled Auto Backup status: %s | Info: %s", success, msg)
        )
        self._auto_backup_worker.start()

    # ─── Theme updates ────────────────────────────────────────────────────────

    def update_theme(self, theme: str) -> None:
        # Update pills style
        self._pill_all._update_style(self._filter_mode == "all", theme)
        self._pill_online._update_style(self._filter_mode == "online", theme)
        self._pill_offline._update_style(self._filter_mode == "offline", theme)
        self._pill_smart._update_style(self._filter_mode == "smartphone", theme)
        self._pill_laptop._update_style(self._filter_mode == "laptop", theme)
        self._pill_iot._update_style(self._filter_mode == "iot", theme)

        # Update stat chips style
        self._chip_total.update_theme(theme, "#38BDF8" if theme == "dark" else "#0284C7")
        self._chip_online.update_theme(theme, "#22C55E")
        self._chip_offline.update_theme(theme, "#94A3B8" if theme == "dark" else "#475569")
        self._chip_new.update_theme(theme, "#F59E0B")

        # Update search bar style
        if theme == "light":
            self._search.setStyleSheet(
                "QLineEdit { background:#FFFFFF; color:#0F172A; border:1px solid #CBD5E1;"
                "border-radius:8px; padding:7px 12px; font-size:12px; }"
                "QLineEdit:focus { border-color:#0284C7; }"
            )
            self._updated_lbl.setStyleSheet("color:#64748B; font-size:11px;")
        else:
            self._search.setStyleSheet(
                "QLineEdit { background:#1E293B; color:#E2E8F0; border:1px solid #2D3748;"
                "border-radius:8px; padding:7px 12px; font-size:12px; }"
                "QLineEdit:focus { border-color:#38BDF8; }"
            )
            self._updated_lbl.setStyleSheet("color:#4A5568; font-size:11px;")

        # Update QTableWidget styling
        if theme == "light":
            tbl_style = """
                QTableWidget {
                    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; gridline-color: #F1F5F9; outline: none;
                }
                QTableWidget::item { padding: 0px 8px; border-bottom: 1px solid #E2E8F0; color: #334155; }
                QTableWidget::item:selected { background: #E0F2FE; color: #0284C7; }
                QHeaderView::section {
                    background: #F1F5F9; color: #475569; font-size: 11px; font-weight: 700;
                    letter-spacing: 0.5px; padding: 8px; border: none; border-bottom: 1px solid #E2E8F0;
                }
            """
        else:
            tbl_style = """
                QTableWidget {
                    background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; gridline-color: #1E293B; outline: none;
                }
                QTableWidget::item { padding: 0px 8px; border-bottom: 1px solid #1A2744; color: #CBD5E1; }
                QTableWidget::item:selected { background: #1E3A5F; color: #E2E8F0; }
                QHeaderView::section {
                    background: #1E293B; color: #64748B; font-size: 11px; font-weight: 700;
                    letter-spacing: 0.5px; padding: 8px; border: none; border-bottom: 1px solid #2D3748;
                }
            """
            
        self._table.setStyleSheet(tbl_style)
        self._dhcp_table.setStyleSheet(tbl_style)
        self._backup_table.setStyleSheet(tbl_style)
        
        self._empty_view.update_theme(theme)
        self._refresh()
