"""
CafePulse — Demo Worker (QThread)
Runs DemoEngine.tick() on a background thread.
Emits Qt signals safe for UI consumption from the main thread.
"""

import logging
from PyQt6.QtCore import QThread, pyqtSignal, QMutex

from modes.demo.demo_engine import DemoEngine

logger = logging.getLogger("cafepulse.demo.worker")


class DemoWorker(QThread):
    """
    Background QThread for Demo Mode data simulation.

    Signals (all emitted from worker thread — connect with Qt.ConnectionType.QueuedConnection):
        tick_data(dict)   — full tick payload from DemoEngine
        alert_fired(dict) — alert payload {type, message, device}
        error(str)        — error message if engine crashes
    """

    tick_data   = pyqtSignal(dict)
    alert_fired = pyqtSignal(dict)
    error       = pyqtSignal(str)
    heartbeat   = pyqtSignal(float)

    def __init__(self, db, scenario: str = "small_cafe", interval_ms: int = 2000, parent=None):
        super().__init__(parent)
        self._db          = db
        self._scenario    = scenario
        self._interval_ms = interval_ms
        self._running     = False
        self._mutex       = QMutex()
        self._engine: DemoEngine | None = None

    # ─── QThread Entry ────────────────────────────────────────────────────────

    def run(self) -> None:
        logger.info("DemoWorker started — scenario=%s interval=%dms",
                    self._scenario, self._interval_ms)
        try:
            self._engine = DemoEngine(self._db, self._scenario)
            self._engine.on_tick(lambda p: self.tick_data.emit(p))
            self._engine.on_alert(lambda p: self.alert_fired.emit(p))

            self._running = True
            while self._running:
                import time
                self.heartbeat.emit(time.time())
                self._engine.tick()
                self.msleep(self._interval_ms)

        except Exception as exc:
            logger.error("DemoWorker error: %s", exc, exc_info=True)
            self.error.emit(str(exc))
        finally:
            logger.info("DemoWorker stopped")

    # ─── Control ──────────────────────────────────────────────────────────────

    def stop(self) -> None:
        self._running = False
        self.wait(3000)  # max 3s wait

    def set_scenario(self, scenario_name: str) -> None:
        """Switch scenario at runtime (safe — engine handles it internally)."""
        self._scenario = scenario_name
        if self._engine:
            self._engine.change_scenario(scenario_name)

    def set_interval(self, ms: int) -> None:
        self._interval_ms = max(500, ms)
