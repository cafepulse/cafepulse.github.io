# ROOT CAUSE ANALYSIS

**Issue ID:** TD-002 (Shutdown Zombie Process & Thread Lifecycle Hang)

### Evidence
Our audit across main_window.py, mikrotik_worker.py, wifi_worker.py, hotspot_worker.py, and health_engine.py reveals a cascade of threading design flaws.
1. **Double-Blocking the Main Thread:** In worker.stop(), the Main Thread calls self.wait(2000) or self.wait(5000). MainWindow._stop_all_workers then calls worker.wait(5000) again. The UI thread is blocked heavily, making the app appear frozen during shutdown.
2. **Blocking Operations Ignoring Shutdown:** The QThread worker 
un() loops perform synchronous, blocking I/O:
   - subprocess.run (Ping/ARP without reliable timeouts or cancellation tokens)
   - ThreadPoolExecutor (Blocks until all spawned futures complete)
   - 
outeros_api.get_resource().get() (Synchronous socket read)
   Setting self._is_running = False does not interrupt these blocking operations.
3. **Forced Termination (QThread.terminate) Leak:** Because the workers do not exit within the timeout period, MainWindow._stop_all_workers invokes worker.terminate(). 
4. **The Ultimate Zombie Cause:** QThread.terminate() forcefully kills the OS thread immediately. 
   - inally blocks are bypassed.
   - SQLite DB connections (PRAGMA journal_mode=WAL) opened with check_same_thread=False are abandoned, leaving .wal locks held.
   - RouterClient.disconnect() is never executed, leaving TCP socket handles open in the OS.
   - subprocess.Popen processes (e.g., in health_engine.py catching TimeoutExpired without calling .kill()) remain orphaned.
   Because these underlying handles and locks are never returned to the OS, Python cannot fully exit the process even after QCoreApplication.quit() and sys.exit(), leaving a zombie background process.

### Affected Files
- ui/windows/main_window.py
- modes/mikrotik/mikrotik_worker.py
- modes/home_wifi/wifi_worker.py
- modes/hotspot/hotspot_worker.py
- core/analytics/health_engine.py

### Reproduction Steps
1. Open CafePulse and connect to a MikroTik router (or start a WiFi scan).
2. While a scan or polling operation is active, click the Close button.
3. The UI will freeze for ~5-10 seconds as wait() blocks the Main Thread.
4. The log will show Worker did not stop gracefully. Force terminating..
5. The UI disappears, but Task Manager reveals CafePulse.exe (or Python) is still running in the background.

### Severity
**CRITICAL (P0)** — Leaves permanent zombie processes, memory leaks, abandoned OS sockets, and risks SQLite database corruption.

### Confidence Level
100%

### Recommended Fix
1. Remove all internal self.wait() calls from worker.stop() methods.
2. Remove worker.terminate() from _stop_all_workers(). 
3. Introduce cancellation tokens or interrupt timeouts to all blocking subprocesses and APIs.
4. Ensure inally blocks explicitly release database and network handles.
5. In health_engine.py, explicitly call proc.kill() on subprocess.TimeoutExpired.
