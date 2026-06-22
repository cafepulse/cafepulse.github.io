"""
CafePulse — App State
A lightweight, deterministic runtime state manager.
All core UI pages subscribe to this object instead of directly to worker threads.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class AppState(QObject):
    """
    Central repository for global runtime state.
    """

    # Signals
    state_changed = pyqtSignal()          # Generic trigger for full refresh
    bandwidth_updated = pyqtSignal(dict)  # Real-time upload/download (dict with display strings & mbps)
    alerts_updated = pyqtSignal(int)      # New alert count
    mode_changed = pyqtSignal(str)        # e.g., 'Demo Mode', 'Home WiFi'
    devices_updated = pyqtSignal(int)     # Active device count
    status_updated = pyqtSignal(bool, str)# is_active, status_text
    theme_changed = pyqtSignal(str)       # Dynamic theme switching ('light' or 'dark')
    licensing_changed = pyqtSignal(bool)  # Premium status changed (is_pro: bool)
    privacy_masked_changed = pyqtSignal(bool) # Privacy masking state toggled

    def __init__(self, parent=None):
        super().__init__(parent)
        self.upload_mbps: float = 0.0
        self.download_mbps: float = 0.0
        self.active_devices: int = 0
        self.alert_count: int = 0
        self.current_theme: str = "dark"
        self.current_mode: str = "Demo"
        self.current_status: str = "Initializing..."
        self.is_scanning: bool = False
        self.privacy_masked: bool = False
        
        # Integrasi Lisensi Terpusat
        from core.licensing.licensing_manager import LicensingManager
        self.is_pro: bool = LicensingManager.check_license()

    def check_license_status(self) -> bool:
        """Kalkulasi status Pro secara terpusat dan kabarkan UI jika terjadi perubahan status."""
        from core.licensing.licensing_manager import LicensingManager
        pro_status = LicensingManager.check_license()
        if self.is_pro != pro_status:
            self.is_pro = pro_status
            self.licensing_changed.emit(pro_status)
        return pro_status

    def update_bandwidth(self, payload: dict) -> None:
        self.upload_mbps = payload.get("upload_mbps", 0.0)
        self.download_mbps = payload.get("download_mbps", 0.0)
        self.bandwidth_updated.emit(payload)

    def set_alert_count(self, count: int) -> None:
        if self.alert_count != count:
            self.alert_count = count
            self.alerts_updated.emit(count)

    def increment_alert(self) -> None:
        self.set_alert_count(self.alert_count + 1)

    def set_mode(self, mode: str) -> None:
        if self.current_mode != mode:
            self.current_mode = mode
            self.mode_changed.emit(mode)

    def set_device_count(self, count: int) -> None:
        if self.active_devices != count:
            self.active_devices = count
            self.devices_updated.emit(count)

    def set_status(self, is_active: bool, text: str) -> None:
        self.is_scanning = is_active
        self.current_status = text
        self.status_updated.emit(is_active, text)

    def set_theme(self, theme: str) -> None:
        if self.current_theme != theme:
            self.current_theme = theme
            self.theme_changed.emit(theme)
