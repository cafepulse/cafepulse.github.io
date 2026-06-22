import logging
import time
import datetime
from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from core.mikrotik.connection_manager import ConnectionManager, ConnectionState
from core.database.batch_writer import BatchWriter
from core.analytics.analytics_engine import AnalyticsEngine

logger = logging.getLogger(__name__)

class MikrotikWorker(QThread):
    scan_result = pyqtSignal(dict)
    tick_data = pyqtSignal(dict)
    alert_fired = pyqtSignal(dict)
    error = pyqtSignal(str)
    heartbeat = pyqtSignal(float)
    
    connection_state_changed = pyqtSignal(str)
    
    def __init__(self, db, host, username, password, port=8728, use_ssl=False):
        super().__init__()
        self.db = db
        self.manager = ConnectionManager(host, username, password, port, use_ssl)
        self._is_running = False
        self._wan_interface = "ether1"
        self._force_slow_scan = False

        self._last_rx = 0
        self._last_tx = 0
        self._last_time = 0
        self._tick_count = 0
        self._active_users = 0
        
        self.router_device_id = self.db.upsert_device(ip=host, mac=f"router:{host}", hostname="MikroTik Router", vendor="MikroTik")
        
        self.writer = BatchWriter(
            db_manager=self.db, 
            table_name='traffic_logs', 
            columns=['device_id', 'upload_speed', 'download_speed', 'timestamp'],
            max_buffer=50
        )
        self.analytics = AnalyticsEngine(max_bandwidth_mbps=100, max_users=100)
        
        # Telemetri Observabilitas Premium
        self.last_fast_poll = 0.0
        self.last_slow_poll = 0.0
        self.monitor_status = "N/A"

    def run(self):
        self._is_running = True
        logger.info('MikrotikWorker background thread started.')
        
        self.manager.start_connection()
        self.connection_state_changed.emit(self.manager.state)
        
        self.last_fast_poll = 0.0
        self.last_slow_poll = 0.0
        last_loop_time = time.time()
        
        while self._is_running:
            now = time.time()
            
            # Deteksi Laptop Suspend / Resume (Sleep)
            # Jika selang loop melebihi 5 detik padahal jeda aslinya 100ms, 
            # berarti komputer baru saja terbangun dari sleep.
            if now - last_loop_time > 5.0:
                logger.warning(f"[SUSPEND-RESUME] Laptop baru saja terbangun! Selisih waktu terdeteksi: {now - last_loop_time:.2f}s. Mereset koneksi secara bersih...")
                self.manager.trigger_reconnect(now, reason="Laptop wake from suspend")
                self.connection_state_changed.emit(self.manager.state)
                
            last_loop_time = now
            
            current_state = self.manager.state
            
            # Siklus Pemulihan Koneksi Otomatis Non-Blocking jika terputus
            if current_state in (ConnectionState.RECONNECTING, ConnectionState.FAILED):
                old_state = current_state
                self.manager.attempt_recovery_nonblocking(now)
                if self.manager.state != old_state:
                    self.connection_state_changed.emit(self.manager.state)
                    
            elif current_state in (ConnectionState.CONNECTED, ConnectionState.DEGRADED, ConnectionState.RECOVERED):
                # Eksekusi Slow Scan paksa (dipicu dari UI secara thread-safe)
                if self._force_slow_scan:
                    self._force_slow_scan = False
                    self._poll_slow_stats(now)
                    self.last_slow_poll = time.time()
                
                # Polling Fast Stats setiap 2 detik
                if now - self.last_fast_poll >= 2.0:
                    self._poll_fast_stats(now)
                    self.last_fast_poll = time.time()
                    
                # Polling Slow Stats setiap 10 detik
                if now - self.last_slow_poll >= 10.0:
                    self._poll_slow_stats(now)
                    self.last_slow_poll = time.time()
            
            # Emit detak jantung (heartbeat) thread
            self.heartbeat.emit(now)
            
            # Tidur ringan agar konsumsi CPU tetap rendah (100ms)
            self.msleep(100)
            
        self.manager.stop()
        self.connection_state_changed.emit(self.manager.state)
        logger.info('MikrotikWorker thread stopped cleanly.')

    def stop(self):
        self._is_running = False
        
        if hasattr(self, 'writer') and self.writer:
            self.writer.shutdown()

    def trigger_scan(self):
        if self._is_running:
            self._force_slow_scan = True

    def _poll_fast_stats(self, now):
        if not self._is_running:
            return
            
        self.heartbeat.emit(time.time())
        
        if self.manager.state not in (ConnectionState.CONNECTED, ConnectionState.DEGRADED, ConnectionState.RECOVERED):
            return
            
        api = self.manager.get_api()
        if not api:
            return
            
        try:
            # Deteksi nama interface secara dinamis (defensive coding)
            try:
                interfaces_res = api.get_resource('/interface').get()
                self.manager.successful_api_commands += 1
                available_interfaces = [i.get('name') for i in interfaces_res if i.get('name')]
                if self._wan_interface not in available_interfaces and available_interfaces:
                    old_interface = self._wan_interface
                    self._wan_interface = available_interfaces[0]
                    logger.info(f"[POLLING] Interface {old_interface} tidak ditemukan. Otomatis mengalihkan ke: {self._wan_interface}")
            except Exception as e:
                self.manager.failed_api_commands += 1
                self.manager.last_exception = f"Interface dynamic detection error: {str(e)}"
                logger.warning(f"[POLLING] Gagal melacak nama interface secara dinamis: {e}")
                
            # Get interface traffic
            # Note: monitor-traffic blocks or runs continuously in CLI, but in API we can use once=True
            try:
                res = api.get_resource('/interface').call('monitor-traffic', {'interface': self._wan_interface, 'once': ''})
                self.manager.successful_api_commands += 1
                self.monitor_status = "OK"
            except Exception as e:
                self.manager.failed_api_commands += 1
                self.monitor_status = "ERROR"
                self.manager.last_exception = f"monitor-traffic command failed: {str(e)}"
                raise
                
            rx_bps = 0
            tx_bps = 0
            if res:
                rx_bps = int(res[0].get('rx-bits-per-second', 0))
                tx_bps = int(res[0].get('tx-bits-per-second', 0))
                
            rx_mbps = rx_bps / 1_000_000
            tx_mbps = tx_bps / 1_000_000
            
            self._tick_count += 1
            
            total_mbps = rx_mbps + tx_mbps
            self.analytics.update_bandwidth_trend(total_mbps)
            health = self.analytics.calculate_health_score(total_mbps, self._active_users)
            congestion_level, _ = self.analytics.estimate_congestion(total_mbps, self._active_users)
            insights = self.analytics.generate_insights(health, congestion_level, self._active_users)
            
            now_date = datetime.datetime.now().isoformat()
            self.writer.add((self.router_device_id, tx_mbps, rx_mbps, now_date))
            
            tick_payload = {
                "tick": self._tick_count,
                "upload_mbps": tx_mbps,
                "download_mbps": rx_mbps,
                "rx_mbps": rx_mbps,
                "tx_mbps": tx_mbps,
                "health": health,
                "congestion": congestion_level,
                "insights": insights
            }
            self.tick_data.emit(tick_payload)
            self.manager.reset_timeout()
            self.connection_state_changed.emit(self.manager.state)
            
        except Exception as e:
            logger.warning(f'Fast polling error: {e}')
            self.manager.handle_timeout(now)
            self.connection_state_changed.emit(self.manager.state)

    def _poll_slow_stats(self, now):
        if not self._is_running or self.manager.state not in (ConnectionState.CONNECTED, ConnectionState.DEGRADED, ConnectionState.RECOVERED):
            return
            
        api = self.manager.get_api()
        if not api: return
            
        try:
            # Poll DHCP Leases for active devices
            leases = api.get_resource('/ip/dhcp-server/lease').get()
            self.manager.successful_api_commands += 1
            active_count = 0
            devices = []
            for lease in leases:
                if lease.get('status') == 'bound':
                    active_count += 1
                    ip = lease.get('address', '')
                    mac = lease.get('mac-address', '')
                    hostname = lease.get('host-name', 'Unknown Device')
                    devices.append({
                        "ip": ip,
                        "mac": mac,
                        "hostname": hostname,
                        "vendor": "Unknown",
                        "status": "online",
                        "bandwidth": "0.0 Mbps"
                    })
            
            self._active_users = active_count

            # Ambil data Hotspot MikroTik secara defensif (mencegah crash jika fitur hotspot tidak aktif di router)
            hotspot_users = []
            hotspot_active = []
            hotspot_profiles = []
            hotspot_servers = []
            
            try:
                hotspot_users = api.get_resource('/ip/hotspot/user').get()
                self.manager.successful_api_commands += 1
            except Exception as ex:
                self.manager.failed_api_commands += 1
                logger.warning(f"Gagal mengambil data user hotspot MikroTik: {ex}")
                
            try:
                hotspot_active = api.get_resource('/ip/hotspot/active').get()
                self.manager.successful_api_commands += 1
            except Exception as ex:
                self.manager.failed_api_commands += 1
                logger.warning(f"Gagal mengambil data user aktif hotspot MikroTik: {ex}")
                
            try:
                hotspot_profiles = api.get_resource('/ip/hotspot/user/profile').get()
                self.manager.successful_api_commands += 1
            except Exception as ex:
                self.manager.failed_api_commands += 1
                logger.warning(f"Gagal mengambil profil hotspot MikroTik: {ex}")

            try:
                hotspot_servers = api.get_resource('/ip/hotspot').get()
                self.manager.successful_api_commands += 1
            except Exception as ex:
                self.manager.failed_api_commands += 1
                logger.warning(f"Gagal mengambil server hotspot MikroTik: {ex}")

            scan_payload = {
                "device_count": active_count,
                "devices": devices,
                "users": active_count,
                "hotspot_users": hotspot_users,
                "hotspot_active": hotspot_active,
                "hotspot_profiles": hotspot_profiles,
                "hotspot_servers": hotspot_servers
            }
            self.scan_result.emit(scan_payload)
            self.manager.reset_timeout()
            self.connection_state_changed.emit(self.manager.state)
        except Exception as e:
            self.manager.failed_api_commands += 1
            self.manager.last_exception = f"Slow poll DHCP leases error: {str(e)}"
            logger.warning(f'Slow polling error: {e}')
            self.manager.handle_timeout(now)
            self.connection_state_changed.emit(self.manager.state)
