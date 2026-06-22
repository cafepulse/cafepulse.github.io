import logging
from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from .connection_manager import ConnectionManager, ConnectionState

logger = logging.getLogger(__name__)

class PollingWorker(QThread):
    stats_updated = pyqtSignal(dict)
    connection_state_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, host, username, password, port=8728, use_ssl=False):
        super().__init__()
        self.manager = ConnectionManager(host, username, password, port, use_ssl)
        self._is_running = False
        
        self.fast_timer = None
        self.medium_timer = None
        self.slow_timer = None
        
    def run(self):
        self._is_running = True
        logger.info('PollingWorker thread started.')
        
        self.manager.start_connection()
        self.connection_state_changed.emit(self.manager.state)
        
        self.fast_timer = QTimer()
        self.fast_timer.timeout.connect(self._poll_fast_stats)
        self.fast_timer.start(2000)
        
        self.medium_timer = QTimer()
        self.medium_timer.timeout.connect(self._poll_medium_stats)
        self.medium_timer.start(10000)
        
        self.slow_timer = QTimer()
        self.slow_timer.timeout.connect(self._poll_slow_stats)
        self.slow_timer.start(30000)
        
        self.exec()
        
        self.manager.stop()
        logger.info('PollingWorker thread stopped cleanly.')

    def stop(self):
        self._is_running = False
        if self.fast_timer: self.fast_timer.stop()
        if self.medium_timer: self.medium_timer.stop()
        if self.slow_timer: self.slow_timer.stop()
        self.quit()
        self.wait()
        
    def _poll_fast_stats(self):
        if not self._is_running:
            return
            
        self.connection_state_changed.emit(self.manager.state)
            
        if self.manager.state != ConnectionState.CONNECTED:
            return
            
        api = self.manager.get_api()
        if not api:
            return
            
        try:
            data = {'type': 'fast', 'status': 'ok'}
            self.stats_updated.emit(data)
            self.manager.reset_timeout()
            
        except Exception as e:
            logger.warning(f'Fast polling error: {e}')
            self.manager.handle_timeout()
            self.error_occurred.emit(str(e))

    def _poll_medium_stats(self):
        if not self._is_running or self.manager.state != ConnectionState.CONNECTED:
            return
        
        api = self.manager.get_api()
        if not api: return
        
        try:
            data = {'type': 'medium', 'status': 'ok'}
            self.stats_updated.emit(data)
            self.manager.reset_timeout()
        except Exception as e:
            self.manager.handle_timeout()

    def _poll_slow_stats(self):
        if not self._is_running or self.manager.state != ConnectionState.CONNECTED:
            return
            
        api = self.manager.get_api()
        if not api: return
            
        try:
            data = {'type': 'slow', 'status': 'ok'}
            self.stats_updated.emit(data)
            self.manager.reset_timeout()
        except Exception as e:
            self.manager.handle_timeout()