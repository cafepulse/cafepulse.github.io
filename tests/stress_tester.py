"""
CafePulse - Advanced Memory & Performance Stress Tester
Runs a long-duration automated test (e.g. 48 hours) to detect:
- Memory Leaks (RAM usage over time)
- CPU Spikes
- UI Lag / Frozen Threads (Event loop delays)

Usage:
  pip install psutil matplotlib
  python tests/stress_tester.py --hours 48
"""

import sys
import time
import os
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import psutil
except ImportError:
    print("Error: 'psutil' is required for this stress test. Please run: pip install psutil")
    sys.exit(1)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class StressTester:
    def __init__(self, target_hours: float):
        self.target_hours = target_hours
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=target_hours)
        
        self.process = psutil.Process(os.getpid())
        self.report_data = []
        
        # UI Lag Tracking
        self.last_tick = time.time()
        self.max_lag_ms = 0
        self.lag_events = 0
        
        # Mode Switching
        self.modes = ["demo", "home_wifi", "demo", "hotspot"]
        self.mode_idx = 0
        
        # Setup App
        self.app = QApplication(sys.argv)
        
        test_db_path = "stress_test.db"
        if Path(test_db_path).exists():
            Path(test_db_path).unlink()
            
        from core.database.db_manager import DatabaseManager
        from core.utils.config_manager import ConfigManager
        from ui.windows.main_window import MainWindow
        
        self.db_path = test_db_path
        self.db = DatabaseManager(test_db_path)
        self.window = MainWindow(config=ConfigManager(), db=self.db)
        
        # Setup Timers
        self.lag_timer = QTimer()
        self.lag_timer.setInterval(100) # Check every 100ms
        self.lag_timer.timeout.connect(self._measure_lag)
        
        self.action_timer = QTimer()
        self.action_timer.setInterval(10000) # Switch mode every 10s
        self.action_timer.timeout.connect(self._perform_action)
        
        self.log_timer = QTimer()
        self.log_timer.setInterval(60000) # Log metrics every 60s
        self.log_timer.timeout.connect(self._log_metrics)
        
        # Check end condition
        self.end_timer = QTimer()
        self.end_timer.setInterval(10000)
        self.end_timer.timeout.connect(self._check_completion)

    def start(self):
        print(f"=== CafePulse Automated Stress Tester ===")
        print(f"Started at: {self.start_time}")
        print(f"Target End Time: {self.end_time} ({self.target_hours} hours)")
        print(f"Monitoring: RAM, CPU, UI Freeze, App Stability\n")
        
        self.window.show()
        
        self.last_tick = time.time()
        self.lag_timer.start()
        self.action_timer.start()
        self.log_timer.start()
        self.end_timer.start()
        
        self._log_metrics() # Initial log
        self._perform_action() # Initial action
        
        # Start Device Churn Chaos Timer
        self.chaos_timer = QTimer()
        self.chaos_timer.setInterval(2000) # Inject churn every 2 seconds
        self.chaos_timer.timeout.connect(self._inject_device_churn)
        self.chaos_timer.start()
        
        self.app.exec()

    def _inject_device_churn(self):
        """Simulate rapid connect/disconnect of devices to test race conditions."""
        if self.mode_idx % 2 == 0:
            mac = f"00:11:22:33:44:{random.randint(10, 99)}"
            self.db.upsert_device(ip=f"192.168.1.{random.randint(10,250)}", mac=mac, hostname=f"Chaos_Device_{random.randint(100,999)}", vendor="ChaosLabs")

    def _measure_lag(self):
        """Measure if the Qt Event loop was blocked."""
        current_time = time.time()
        delta_ms = (current_time - self.last_tick) * 1000
        self.last_tick = current_time
        
        # If delta is significantly larger than 100ms (e.g., > 300ms)
        if delta_ms > 300:
            freeze_duration = delta_ms - 100
            if freeze_duration > self.max_lag_ms:
                self.max_lag_ms = freeze_duration
            self.lag_events += 1
            print(f"[!] UI Freeze Detected: {freeze_duration:.0f} ms")

    def _perform_action(self):
        """Simulate user switching modes."""
        current_mode = self.modes[self.mode_idx % len(self.modes)]
        self.mode_idx += 1
        self.window._on_mode_changed(current_mode)

    def _log_metrics(self):
        """Capture RAM and CPU."""
        ram_mb = self.process.memory_info().rss / (1024 * 1024)
        cpu_percent = self.process.cpu_percent(interval=None) # Non-blocking
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "time": timestamp,
            "ram_mb": round(ram_mb, 2),
            "cpu_percent": round(cpu_percent, 1),
            "max_lag_ms_in_window": round(self.max_lag_ms, 0),
            "lag_events": self.lag_events
        }
        self.report_data.append(entry)
        
        print(f"[{timestamp}] RAM: {ram_mb:.2f} MB | CPU: {cpu_percent}% | Peak Freeze: {self.max_lag_ms:.0f}ms")
        
        # Reset window tracking for lag
        self.max_lag_ms = 0

    def _check_completion(self):
        if datetime.now() >= self.end_time:
            self._finish_test()

    def _finish_test(self):
        self.lag_timer.stop()
        self.action_timer.stop()
        self.log_timer.stop()
        self.end_timer.stop()
        if hasattr(self, 'chaos_timer'):
            self.chaos_timer.stop()
        
        print("\n=== Stress Test Completed ===")
        self._analyze_leak()
        self._generate_report()
        self._generate_graph()
        
        self.window.close()
        self.db.close()
        
        if Path(self.db_path).exists():
            try:
                Path(self.db_path).unlink()
            except:
                pass
                
        self.app.quit()

    def _generate_report(self):
        report_file = f"stress_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("Timestamp,RAM (MB),CPU (%),Peak UI Freeze (ms),Total Freeze Events\n")
                for r in self.report_data:
                    f.write(f"{r['time']},{r['ram_mb']},{r['cpu_percent']},{r['max_lag_ms_in_window']},{r['lag_events']}\n")
            
            print(f"✅ Full CSV report saved to: {report_file}")
        except Exception as e:
            print(f"Failed to write report: {e}")

    def _analyze_leak(self):
        """Analyze RAM trend for potential leaks."""
        if len(self.report_data) < 10:
            return
            
        initial_ram = self.report_data[0]['ram_mb']
        final_ram = self.report_data[-1]['ram_mb']
        growth = final_ram - initial_ram
        
        print("\n--- Leak Analysis ---")
        print(f"Initial RAM: {initial_ram} MB")
        print(f"Final RAM: {final_ram} MB")
        print(f"Net Growth: {growth:.2f} MB")
        
        if growth > 50.0:  # Arbitrary threshold: 50MB growth is suspicious
            print("⚠️ WARNING: Potential Memory Leak Detected! RAM grew significantly during the test.")
        else:
            print("✅ Memory appears stable.")

    def _generate_graph(self):
        """Generate a visual graph using matplotlib if available."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            
            times = [datetime.strptime(r['time'], "%Y-%m-%d %H:%M:%S") for r in self.report_data]
            ram = [r['ram_mb'] for r in self.report_data]
            cpu = [r['cpu_percent'] for r in self.report_data]
            
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            color = 'tab:red'
            ax1.set_xlabel('Time')
            ax1.set_ylabel('RAM (MB)', color=color)
            ax1.plot(times, ram, color=color, linewidth=2)
            ax1.tick_params(axis='y', labelcolor=color)
            
            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('CPU (%)', color=color)
            ax2.plot(times, cpu, color=color, alpha=0.5)
            ax2.tick_params(axis='y', labelcolor=color)
            
            fig.tight_layout()
            graph_file = f"stress_test_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(graph_file)
            print(f"📈 Graph visualization saved to: {graph_file}")
            
        except ImportError:
            print("Matplotlib not installed. Skipping graph generation. (pip install matplotlib)")
        except Exception as e:
            print(f"Failed to generate graph: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CafePulse Stress Tester")
    parser.add_argument("--hours", type=float, default=0.05, help="Number of hours to run the test (e.g., 48). Default is 0.05 (3 minutes) for quick test.")
    args = parser.parse_args()
    
    tester = StressTester(target_hours=args.hours)
    tester.start()
