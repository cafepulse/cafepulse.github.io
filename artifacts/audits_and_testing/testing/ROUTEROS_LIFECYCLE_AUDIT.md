# ROUTEROS LIFECYCLE AUDIT

**File:** core/mikrotik/mikrotik_worker.py
**File:** core/mikrotik/router_client.py

### API Session Lifecycle
- **Connect:** Uses 
outeros_api.RouterOsApiPool. self.connection.set_timeout(3) is used to restrict socket timeouts.
- **Polling:** Calls pi.get_resource(...).get() synchronously inside the MikrotikWorker QThread loop.
- **Disconnect:** Handled by self.manager.stop() which calls self.connection.disconnect().

### Findings / Defects
1. **Unreachable Disconnect:** MikrotikWorker.stop() sets self._is_running = False and then calls self.wait(2000). It expects the thread loop to terminate and subsequently call self.manager.stop(). However, if the thread is currently blocked on an API call (e.g. pi.get_resource('/interface').get()) that hangs or takes a long time, the while condition is not re-evaluated in time.
2. **Zombie Sockets:** When wait(2000) times out, MainWindow._stop_all_workers forcefully 	erminate()s the QThread. The line self.manager.stop() is **never executed**.
3. **RouterOS Leak:** Because self.connection.disconnect() is never reached due to forced termination, the TCP socket is not cleanly closed via FIN packets. The MikroTik router retains an orphaned API session, and Windows leaves the socket handle dangling.
