# MAINWINDOW LIFECYCLE AUDIT

## General Audit
**File:** ui/windows/main_window.py

### Worker Initialization:
- _start_demo_mode: Init DemoWorker.
- _start_mikrotik_mode: Init MikrotikWorker.
- _start_hotspot_mode: Init HotspotWorker.
- _start_wifi_mode: Init WiFiWorker.

### Worker Destruction (_stop_all_workers):
The _stop_all_workers iterates over _demo_worker, _wifi_worker, _hotspot_worker, _mikrotik_worker.

### Answers to Critical Questions
**Are all workers explicitly stopped?**
YES. .stop() is explicitly called on each running worker.

**Are all workers waited for?**
YES. .wait(5000) is called to gracefully wait for up to 5 seconds.

**Are all workers disconnected?**
NO. There is NO explicit .disconnect() call for the signals attached to the workers.

### Risk Identified
If worker.stop() is ineffective, the 5-second wait times out, and the system forcefully calls worker.terminate(). Force terminating a QThread is highly dangerous in PyQt as it bypasses Python's inally blocks, leaving OS sockets, database locks, and external API handles open permanently.
