# HOTSPOT WORKER AUDIT

**File:** modes/hotspot/hotspot_worker.py
**File:** modes/hotspot/hotspot_scanner.py

### Worker Entry Point
HotspotWorker.run(): Enters a while self._running: loop. Inside the loop, it executes HotspotScanner.run_scan().

### Stop Routine
HotspotWorker.stop() sets self._running = False and immediately calls self.wait(5000).

### Findings
1. **Self.Wait Danger:** Calling self.wait(5000) inside stop() blocks the calling thread (the Main UI Thread) for up to 5 seconds. _stop_all_workers in MainWindow also calls worker.wait(5000).
2. **Scanner Blocking:** 
un_scan() uses subprocess.run (e.g. rp -a, ip neighbor). If subprocess.run hangs without a timeout, the QThread hangs permanently. Setting _running = False does NOT abort subprocess.run.
3. **Signal Cleanup:** No explicit cleanup of pyqtSignals.

