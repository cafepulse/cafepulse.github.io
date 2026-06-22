"""
CafePulse — Connection Resilience Manager
Mengontrol transisi state machine koneksi, mengelola socket timeouts,
dan mengorkestrasi pemulihan otomatis non-blocking menggunakan capped exponential backoff.
"""

import time
import random
import logging
from .router_client import RouterClient

logger = logging.getLogger("cafepulse.core.mikrotik.manager")

class ConnectionState:
    DISCONNECTED = 'DISCONNECTED'
    CONNECTING = 'CONNECTING'
    CONNECTED = 'CONNECTED'
    DEGRADED = 'DEGRADED'
    RECONNECTING = 'RECONNECTING'
    FAILED = 'FAILED'
    RECOVERED = 'RECOVERED'

class ConnectionManager:
    """
    Manajer Ketahanan Jaringan MikroTik yang non-blocking.
    Mengelola transisi state machine koneksi secara aman tanpa race-conditions.
    """
    
    def __init__(self, host, username, password, port=8728, use_ssl=False):
        self.client = RouterClient(host, username, password, port, use_ssl)
        self.state = ConnectionState.DISCONNECTED
        
        # Metrik & Parameter Reconnect
        self.retry_attempt = 0
        self.base_delay = 2.0  # delay awal (detik)
        self.max_delay = 30.0  # delay maksimal (detik)
        self.next_reconnect_time = 0.0
        
        # Penanganan Timeout
        self.timeout_threshold = 3
        self.timeout_count = 0
        
        # Metrik Stabilitas & Telemetri Premium untuk Debug Overlay
        self.reconnect_count = 0
        self.last_state_change = time.time()
        self.last_success_packet = 0.0
        
        self.last_exception = "None"
        self.last_reconnect_reason = "None"
        self.successful_api_commands = 0
        self.failed_api_commands = 0
        self.state_history = []
        self.api_auth_status = "PENDING"

    def set_state(self, new_state: str) -> None:
        """Mengubah status koneksi secara aman dan mencatat perubahan transisi."""
        if self.state != new_state:
            old_state = self.state
            self.state = new_state
            self.last_state_change = time.time()
            
            # Catat riwayat transisi status dengan timestamp
            timestamp_str = time.strftime("%H:%M:%S")
            self.state_history.append(f"[{timestamp_str}] {old_state} ➜ {new_state}")
            if len(self.state_history) > 8:
                self.state_history.pop(0)
                
            logger.info(f"[STATE MACHINE] Transisi: {old_state} ➜ {new_state} | State aktif: {new_state}")

    def start_connection(self) -> bool:
        """Memulai inisialisasi koneksi pertama kali."""
        logger.info(f"[CONNECTION] Memulai inisialisasi koneksi ke MikroTik Router ({self.client.host})...")
        self.set_state(ConnectionState.CONNECTING)
        self.retry_attempt = 0
        self.timeout_count = 0
        success = self._attempt_connect()
        if not success:
            logger.warning("[CONNECTION] Koneksi awal gagal. Memicu orkestrasi pemulihan otomatis (auto-reconnect).")
            self.trigger_reconnect(time.time(), reason="Initial connection failure")
        return success

    def _attempt_connect(self, is_recovery: bool = False) -> bool:
        """Melakukan percobaan socket connection secara aman."""
        try:
            logger.info(f"[CONNECTION] Mencoba membuka socket API ke {self.client.host}:{self.client.port}...")
            self.api_auth_status = "PENDING"
            self.client.connect()
            self.timeout_count = 0
            self.successful_api_commands += 1
            self.api_auth_status = "SUCCESS"
            
            logger.info(f"[CONNECTION] API Auth Success. Berhasil terhubung ke host {self.client.host}!")
            # Jika merupakan pemulihan, tandai recovered
            if is_recovery:
                self.set_state(ConnectionState.RECOVERED)
            else:
                self.set_state(ConnectionState.CONNECTED)
            return True
        except Exception as e:
            self.last_exception = str(e)
            self.failed_api_commands += 1
            self.api_auth_status = "FAILED"
            logger.error(f"[CONNECTION] Gagal melakukan koneksi ke router {self.client.host}: {e}")
            return False

    def trigger_reconnect(self, now: float, reason: str = "Unknown") -> None:
        """Memicu siklus reconnect non-blocking."""
        if self.state in (ConnectionState.RECONNECTING, ConnectionState.FAILED):
            return
            
        logger.warning(f"[RECONNECT] Koneksi lost! Memulai orkestrasi pemulihan otomatis (Attempt #{self.reconnect_count + 1}) | Reason: {reason}...")
        self.set_state(ConnectionState.RECONNECTING)
        self.client.disconnect()
        
        self.last_reconnect_reason = reason
        self.retry_attempt = 0
        self.reconnect_count += 1
        # Reconnect pertama langsung dipicu setelah base_delay (2s)
        self.next_reconnect_time = now + self.base_delay
        logger.info(f"[RECONNECT] Percobaan reconnect ke-{self.reconnect_count} dijadwalkan dalam {self.base_delay}s...")

    def handle_timeout(self, now: float) -> None:
        """Menangani insiden timeout polling."""
        self.timeout_count += 1
        logger.warning(f"[CONNECTION] Polling metrik gagal terkirim ({self.timeout_count}/{self.timeout_threshold})")
        
        if self.timeout_count >= self.timeout_threshold:
            logger.error("[CONNECTION] Batas timeout beruntun terlampaui. Memaksa orkestrasi reconnect.")
            self.trigger_reconnect(now, reason="Consecutive timeout threshold exceeded")
        else:
            self.set_state(ConnectionState.DEGRADED)

    def reset_timeout(self) -> None:
        """Mereset status timeout jika data berhasil diambil."""
        self.timeout_count = 0
        self.last_success_packet = time.time()
        logger.debug(f"[CONNECTION] Polling metrik sukses | Last packet timestamp: {self.last_success_packet}")
        if self.state in (ConnectionState.DEGRADED, ConnectionState.RECOVERED):
            logger.info("[CONNECTION] Pemulihan data stabil kembali ke CONNECTED.")
            self.set_state(ConnectionState.CONNECTED)

    def attempt_recovery_nonblocking(self, now: float) -> bool:
        """
        Mencoba melakukan pemulihan koneksi secara non-blocking jika waktunya tiba.
        Fungsi ini dipanggil secara berkala di dalam background loop utama.
        """
        if self.state not in (ConnectionState.RECONNECTING, ConnectionState.FAILED):
            return False
            
        if now < self.next_reconnect_time:
            return False
            
        self.retry_attempt += 1
        logger.info(f"[RECOVERY] Mencoba menghubungkan kembali (Percobaan ke-{self.retry_attempt})...")
        
        # Pindahkan state ke CONNECTING untuk visual
        self.set_state(ConnectionState.CONNECTING)
        
        if self._attempt_connect(is_recovery=True):
            logger.info(f"[RECOVERY] Berhasil pulih secara otomatis setelah {self.retry_attempt} percobaan!")
            self.retry_attempt = 0
            return True
        else:
            # Hitung delay exponential backoff baru dengan capped dan jitter acak ringan
            delay = min(self.max_delay, self.base_delay * (2 ** self.retry_attempt))
            jitter = random.uniform(-0.5, 0.5)
            total_delay = max(2.0, delay + jitter)
            
            self.next_reconnect_time = now + total_delay
            self.set_state(ConnectionState.RECONNECTING)
            logger.warning(f"[RECOVERY] Gagal. Percobaan berikutnya dijadwalkan dalam {total_delay:.2f}s...")
            return False

    def stop(self) -> None:
        """Menghentikan seluruh koneksi dan membersihkan soket."""
        self.set_state(ConnectionState.DISCONNECTED)
        self.client.disconnect()
        logger.info("[CONNECTION] Koneksi MikroTik berhasil dihentikan secara bersih.")

    def get_api(self):
        """Mengambil instansi API aktif hanya jika state tersambung."""
        if self.state in (ConnectionState.CONNECTED, ConnectionState.DEGRADED, ConnectionState.RECOVERED):
            return self.client.get_api()
        return None
