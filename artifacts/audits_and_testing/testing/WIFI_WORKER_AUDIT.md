# WIFI WORKER AUDIT

**File:** modes/home_wifi/wifi_worker.py
**File:** modes/home_wifi/arp_scanner.py

### Worker Entry Point
WiFiWorker.run(): Enters a while self._running: loop. It calls WiFiScanner.run_scan(do_ping_sweep=self._do_ping_sweep).

### Stop Routine
WiFiWorker.stop() sets self._running = False and immediately calls self.wait(5000).

### Findings
1. **Self.Wait Danger:** Calling self.wait(5000) inside stop() blocks the Main UI Thread.
2. **Scanner Blocking:** 
un_scan() uses ThreadPoolExecutor and subprocess.run (e.g. rp -a, ping). These calls are synchronous inside the ThreadPoolExecutor. If any subprocess.run blocks, the thread pool blocks. Setting _running = False does not terminate the ThreadPool or the subprocesses immediately.
3. **Signal Cleanup:** No explicit cleanup of pyqtSignals.

