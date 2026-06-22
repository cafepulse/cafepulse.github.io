"""
CafePulse — Bandwidth Monitor
Realtime host-level upload/download speed using psutil.
Lightweight, cross-platform, no admin privileges required.
"""

import logging
import time

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

logger = logging.getLogger("cafepulse.bandwidth")


def _format_speed(bytes_per_sec: float) -> str:
    """Format bytes/sec into human-readable string."""
    if bytes_per_sec >= 1_048_576:  # >= 1 MB/s
        return f"{bytes_per_sec / 1_048_576:.1f} MB/s"
    elif bytes_per_sec >= 1024:  # >= 1 KB/s
        return f"{bytes_per_sec / 1024:.0f} KB/s"
    else:
        return f"{bytes_per_sec:.0f} B/s"


class BandwidthMonitor(QObject):
    """
    Emits realtime upload/download speed every `interval_ms` milliseconds.
    Uses psutil.net_io_counters() delta computation.

    Signal payload:
        {
            "upload_speed":     float,  # bytes/sec
            "download_speed":   float,  # bytes/sec
            "upload_display":   str,    # e.g. "1.2 MB/s"
            "download_display": str,    # e.g. "5.4 MB/s"
            "upload_mbps":      float,  # Mbps
            "download_mbps":    float,  # Mbps
        }
    """

    speed_updated = pyqtSignal(dict)

    def __init__(self, interval_ms: int = 2000, parent=None):
        super().__init__(parent)
        self._interval_ms = interval_ms
        self._prev_sent = 0
        self._prev_recv = 0
        self._prev_time = 0.0
        self._timer: QTimer | None = None
        self._available = False

        try:
            import psutil
            self._psutil = psutil
            self._available = True
        except ImportError:
            logger.warning("psutil not installed — bandwidth monitoring disabled")

    def start(self) -> None:
        if not self._available:
            return
        # Take initial reading
        counters = self._psutil.net_io_counters()
        self._prev_sent = counters.bytes_sent
        self._prev_recv = counters.bytes_recv
        self._prev_time = time.monotonic()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(self._interval_ms)
        logger.info("BandwidthMonitor started — interval=%dms", self._interval_ms)

    def stop(self) -> None:
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _tick(self) -> None:
        try:
            counters = self._psutil.net_io_counters()
            now = time.monotonic()
            dt = now - self._prev_time
            if dt <= 0:
                return

            sent_delta = counters.bytes_sent - self._prev_sent
            recv_delta = counters.bytes_recv - self._prev_recv

            upload_speed = max(0, sent_delta / dt)
            download_speed = max(0, recv_delta / dt)

            self._prev_sent = counters.bytes_sent
            self._prev_recv = counters.bytes_recv
            self._prev_time = now

            self.speed_updated.emit({
                "upload_speed":     upload_speed,
                "download_speed":   download_speed,
                "upload_display":   _format_speed(upload_speed),
                "download_display": _format_speed(download_speed),
                "upload_mbps":      round(upload_speed * 8 / 1_000_000, 2),
                "download_mbps":    round(download_speed * 8 / 1_000_000, 2),
            })
        except Exception as exc:
            logger.debug("Bandwidth tick error: %s", exc)
