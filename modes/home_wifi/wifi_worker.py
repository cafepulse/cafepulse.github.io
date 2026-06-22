"""
CafePulse — WiFi Worker (QThread)
Runs WiFiScanner on a background thread and emits Qt signals to the UI.
"""

import logging
from PyQt6.QtCore import QThread, pyqtSignal

from modes.home_wifi.wifi_scanner   import WiFiScanner, ScanResult
from core.analytics.analytics_engine import AnalyticsEngine

logger = logging.getLogger("cafepulse.homewifi.worker")


class WiFiWorker(QThread):
    """
    Background scanner for Home WiFi Mode.

    Signals:
        scan_result(dict)   — enriched scan result payload for UI
        alert_fired(dict)   — alert {type, message}
        scan_started()      — emitted at start of each scan cycle
        scan_finished()     — emitted at end of each scan cycle
        error(str)          — on unrecoverable failure
    """

    scan_result  = pyqtSignal(dict)
    alert_fired  = pyqtSignal(dict)
    scan_started  = pyqtSignal()
    scan_finished = pyqtSignal()
    error        = pyqtSignal(str)
    heartbeat    = pyqtSignal(float)

    def __init__(
        self,
        db,
        interval_ms:    int  = 30_000,   # 30s default for real scanning
        do_ping_sweep:  bool = True,
        subnet:         str  = None,
        parent=None,
    ):
        super().__init__(parent)
        self._db           = db
        self._interval_ms  = interval_ms
        self._do_ping_sweep = do_ping_sweep
        self._subnet       = subnet
        self._running      = False
        self._scan_now     = False
        self._scanner: WiFiScanner | None = None
        self._analytics    = AnalyticsEngine()

    def run(self) -> None:
        logger.info("WiFiWorker started — interval=%ds", self._interval_ms // 1000)
        try:
            from modes.home_wifi.vendor_lookup import VendorLookup
            import time
            vendor_lookup = VendorLookup()
            self._scanner = WiFiScanner(self._db, vendor_lookup)
            self._scanner.on_alert(lambda p: self.alert_fired.emit(p))
            self._scanner.on_heartbeat(lambda: self.heartbeat.emit(time.time()))

            self._running = True
            while self._running:
                import time
                self.heartbeat.emit(time.time())
                self.scan_started.emit()
                result: ScanResult = self._scanner.run_scan(
                    subnet=self._subnet,
                    do_ping_sweep=self._do_ping_sweep,
                )

                payload = {
                    "device_count": len(result.entries),
                    "devices":      result.entries,
                    "new_devices":  result.new_devices,
                    "missing":      result.missing,
                    "scan_duration": result.scan_duration,
                    "local_ip":     result.local_ip,
                    "subnet":       result.subnet,
                    "error":        result.error,
                    "total_upload":   0.0,
                    "total_download": 0.0,
                    "scenario":     "Home WiFi",
                }
                self.scan_result.emit(payload)
                
                # Generate AI Insights based on topology
                insights = self._analytics.generate_basic_insights(
                    active_users=len(result.entries),
                    new_devices_count=len(result.new_devices),
                    missing_devices_count=len(result.missing)
                )
                for ins in insights:
                    self.alert_fired.emit({"type": "insight", "message": ins})
                    
                self.scan_finished.emit()

                # Interruptible wait: check _scan_now every 500ms
                self._scan_now = False
                elapsed = 0
                while self._running and elapsed < self._interval_ms and not self._scan_now:
                    self.msleep(500)
                    elapsed += 500

        except Exception as exc:
            logger.error("WiFiWorker error: %s", exc, exc_info=True)
            self.error.emit(str(exc))
        finally:
            logger.info("WiFiWorker stopped")

    def stop(self) -> None:
        self._running = False

    def trigger_scan(self) -> None:
        """Request an immediate scan — breaks out of the wait loop."""
        self._scan_now = True

    def set_interval(self, ms: int) -> None:
        self._interval_ms = max(10_000, ms)

    def set_subnet(self, subnet: str) -> None:
        self._subnet = subnet

