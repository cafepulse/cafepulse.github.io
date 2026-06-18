"""
CafePulse — Network Health & Diagnostics Engine (Sub-Phase 4-A)
Provides non-blocking ping monitors, packet loss tracking, and advanced health score calculation.
"""

import os
import time
import logging
import platform
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger("cafepulse.analytics.health")

class PingMonitorWorker(QThread):
    """
    Non-blocking background thread to perform continuous ping monitoring.
    Calculates exact latency and packet loss to target hosts.
    """
    ping_updated = pyqtSignal(dict) # {"host": str, "latency_ms": float, "packet_loss_pct": float}
    
    def __init__(self, target_host: str = "8.8.8.8", interval_seconds: int = 5):
        super().__init__()
        self.target_host = target_host
        self.interval_seconds = interval_seconds
        self._is_running = False
        
    def run(self):
        self._is_running = True
        logger.info("PingMonitorWorker started for target host: %s", self.target_host)
        
        history = []
        max_history = 10
        
        while self._is_running:
            success, latency = self._ping(self.target_host)
            
            # Record in window history
            history.append(1.0 if success else 0.0)
            if len(history) > max_history:
                history.pop(0)
                
            # Compute packet loss percentage
            lost_count = history.count(0.0)
            packet_loss = (lost_count / len(history)) * 100.0
            
            payload = {
                "host": self.target_host,
                "latency_ms": latency if success else -1.0,
                "packet_loss_pct": packet_loss
            }
            self.ping_updated.emit(payload)
            
            # Wait for next check safely
            for _ in range(self.interval_seconds):
                if not self._is_running:
                    break
                time.sleep(1)
                
    def stop(self):
        self._is_running = False
        
    def _ping(self, host: str) -> tuple[bool, float]:
        """Perform native OS ping call and returns (success: bool, latency_ms: float)."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Timeout param: -w in milliseconds for Windows, -W in seconds for Linux/Darwin
        timeout_param = ['-w', '1000'] if platform.system().lower() == 'windows' else ['-W', '1']
        
        cmd = ['ping', param, '1'] + timeout_param + [host]
        
        try:
            start_time = time.time()
            
            # Run without showing window on Windows
            kwargs = {}
            if platform.system().lower() == 'windows':
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                **kwargs
            )
            stdout, stderr = proc.communicate(timeout=1.5)
            duration = (time.time() - start_time) * 1000.0 # ms
            
            if proc.returncode == 0:
                # Successfully pinged, extract latency if possible
                latency = self._parse_latency(stdout.decode('utf-8', errors='ignore'), duration)
                return True, latency
            return False, 0.0
        except subprocess.TimeoutExpired:
            return False, 0.0
        except Exception as e:
            logger.debug("Ping execution failed: %s", e)
            return False, 0.0
            
    def _parse_latency(self, output: str, fallback_duration: float) -> float:
        """Parse ping stdout to find exact latency round trip."""
        import re
        try:
            # Look for expressions like: time=29ms, time<1ms, waktu=5ms, average = 12ms, etc.
            # Handles different languages and sub-millisecond latencies (<1ms) robustly.
            match = re.search(r'[=<]\s*(\d+(?:\.\d+)?)\s*ms', output.lower())
            if match:
                return float(match.group(1))
        except Exception as e:
            logger.debug("Failed to parse ping latency: %s", e)
        return fallback_duration



class HealthEngine:
    """
    Advanced Network Health Score Calculator.
    Aggregates latency, packet loss, bandwidth utilisation, and connection states.
    """
    
    @classmethod
    def calculate_health(cls, latency_ms: float, packet_loss_pct: float, 
                         bw_utilization_pct: float, error_count: int = 0) -> tuple[int, str]:
        """
        Calculates health score (0-100) and returns (score, status_label).
        """
        score = 100
        
        # 1. Latency impact
        if latency_ms < 0: # Connection lost
            return 0, "CRITICAL (No Connection)"
            
        if latency_ms > 150:
            score -= 20
        elif latency_ms > 80:
            score -= 10
        elif latency_ms > 40:
            score -= 5
            
        # 2. Packet Loss impact (Very severe)
        if packet_loss_pct > 20:
            score -= 50
        elif packet_loss_pct > 10:
            score -= 30
        elif packet_loss_pct > 5:
            score -= 15
        elif packet_loss_pct > 0:
            score -= 5
            
        # 3. Bandwidth Congestion impact
        if bw_utilization_pct > 90:
            score -= 15
        elif bw_utilization_pct > 75:
            score -= 10
        elif bw_utilization_pct > 50:
            score -= 5
            
        # 4. Error rates impact
        score -= min(error_count * 4, 25)
        
        # Clamp between 0 and 100
        score = max(0, min(100, int(score)))
        
        # Determine status label
        if score >= 90:
            return score, "EXCELLENT"
        elif score >= 75:
            return score, "GOOD"
        elif score >= 50:
            return score, "DEGRADED"
        elif score >= 30:
            return score, "POOR"
        else:
            return score, "CRITICAL"
