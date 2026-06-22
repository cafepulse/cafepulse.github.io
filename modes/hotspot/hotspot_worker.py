"""
CafePulse — Hotspot Worker (QThread)
Fast-refresh background scanner for Hotspot Mode (default 10s).
"""

import logging
from PyQt6.QtCore import QThread, pyqtSignal

from modes.home_wifi.vendor_lookup  import VendorLookup
from modes.hotspot.hotspot_scanner  import HotspotScanner, HotspotScanResult
from core.analytics.analytics_engine import AnalyticsEngine

logger = logging.getLogger("cafepulse.hotspot.worker")


class HotspotWorker(QThread):
    """
    Signals:
        scan_result(dict)    — full scan payload for UI consumption
        alert_fired(dict)    — {type, message}
        scan_started()
        scan_finished()
        hotspot_detected(dict) — hotspot info on first detection
        error(str)
    """

    scan_result       = pyqtSignal(dict)
    alert_fired       = pyqtSignal(dict)
    scan_started      = pyqtSignal()
    scan_finished     = pyqtSignal()
    hotspot_detected  = pyqtSignal(dict)
    error             = pyqtSignal(str)
    heartbeat         = pyqtSignal(float)

    def __init__(
        self,
        db,
        interval_ms:  int            = 10_000,  # 10s default — hotspot nets are small
        subnet:       str | None     = None,
        parent=None,
    ):
        super().__init__(parent)
        self._db          = db
        self._interval_ms = interval_ms
        self._subnet      = subnet
        self._running     = False
        self._scan_now    = False
        self._scanner:    HotspotScanner | None = None
        self._first_scan  = True
        self._analytics   = AnalyticsEngine()

    def run(self) -> None:
        logger.info("HotspotWorker started — interval=%ds", self._interval_ms // 1000)
        try:
            import time
            vendor = VendorLookup()
            self._scanner = HotspotScanner(self._db, vendor)
            self._scanner.on_alert(lambda p: self.alert_fired.emit(p))
            self._scanner.on_heartbeat(lambda: self.heartbeat.emit(time.time()))

            self._running = True
            while self._running:
                import time
                self.heartbeat.emit(time.time())
                self.scan_started.emit()

                result: HotspotScanResult = self._scanner.run_scan(
                    subnet=self._subnet,
                )

                # Emit hotspot info on first successful detection
                if self._first_scan and result.hotspot_info:
                    self.hotspot_detected.emit({
                        "detected":     result.hotspot_info.detected,
                        "type":         result.hotspot_info.hotspot_type,
                        "display_name": result.hotspot_info.display_name,
                        "local_ip":     result.hotspot_info.local_ip,
                        "subnet":       result.hotspot_info.subnet,
                        "gateway":      result.hotspot_info.gateway,
                    })
                    self._first_scan = False

                # Get full device list from DB to preserve offline history
                all_db_devices = [dict(d) for d in self._db.get_all_devices()]
                active_macs = {sess.get("mac", "").lower() for sess in result.active_sessions}
                
                # Map online/offline status based on active_sessions
                for d in all_db_devices:
                    if d.get("mac", "").lower() in active_macs:
                        d["status"] = "online"
                    else:
                        d["status"] = "offline"

                payload = {
                    "device_count":   len(result.active_sessions),
                    "devices":        all_db_devices,
                    "joined":         result.joined,
                    "left":           result.left,
                    "active_sessions": result.active_sessions,
                    "scan_duration":  result.scan_duration,
                    "last_scan_time": result.last_scan_time,
                    "hotspot_type":   result.hotspot_info.hotspot_type if result.hotspot_info else "",
                    "display_name":   result.hotspot_info.display_name if result.hotspot_info else "",
                    "local_ip":       result.hotspot_info.local_ip if result.hotspot_info else "",
                    "subnet":         result.hotspot_info.subnet if result.hotspot_info else "",
                    "total_upload":   0.0,
                    "total_download": 0.0,
                    "error":          result.error,
                    "scenario":       "Hotspot",
                }
                self.scan_result.emit(payload)
                
                # Generate AI Insights based on topology
                insights = self._analytics.generate_basic_insights(
                    active_users=len(result.active_sessions),
                    new_devices_count=len(result.joined),
                    missing_devices_count=len(result.left)
                )
                for ins in insights:
                    self.alert_fired.emit({"type": "insight", "message": ins})
                    
                self.scan_finished.emit()
                
                slept = 0
                while slept < self._interval_ms and self._running and not self._scan_now:
                    self.msleep(500)
                    slept += 500
                self._scan_now = False

        except Exception as exc:
            logger.error("HotspotWorker error: %s", exc, exc_info=True)
            self.error.emit(str(exc))
        finally:
            if self._scanner:
                self._scanner.shutdown()
            logger.info("HotspotWorker stopped")

    def stop(self) -> None:
        self._running = False

    def set_interval(self, ms: int) -> None:
        self._interval_ms = max(5_000, ms)

    def set_subnet(self, subnet: str) -> None:
        self._subnet = subnet
        if self._scanner:
            self._scanner._hotspot_info = None  # force re-detect

    def trigger_scan(self) -> None:
        self._scan_now = True
