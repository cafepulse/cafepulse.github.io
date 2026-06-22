# THREAD INVENTORY

| Name | Location | Creation Point | Stop Method | Cleanup Method | Risk Level |
|---|---|---|---|---|---|
| DemoWorker | modes/demo/demo_worker.py | UI Init | .stop() | None | LOW |
| PingMonitorWorker | core/analytics/health_engine.py | Network Monitor | .stop() / .wait() | None | MEDIUM |
| PollingWorker | core/mikrotik/polling_worker.py | Connection Success | .stop() | None | MEDIUM |
| RouterDiscoveryWorker | core/mikrotik/router_discovery.py | UI Click | .stop() | None | LOW |
| RouterDiagnosticsWorker | core/mikrotik/router_discovery.py | UI Click | .stop() | None | LOW |
| WiFiWorker | modes/home_wifi/wifi_worker.py | UI Init | .stop() | None | HIGH |
| HotspotWorker | modes/hotspot/hotspot_worker.py | UI Init | .stop() | None | HIGH |
| MikrotikWorker | modes/mikrotik/mikrotik_worker.py | UI Init | .stop() | None | HIGH |
| PortTesterThread | ui/widgets/compatibility_page.py | UI Click | .stop() | None | LOW |
| BackupWorker | ui/widgets/devices_page.py | Scheduled/Click | .stop() | None | MEDIUM |
| QTimer (Multiple) | main_window.py, polling_worker.py, etc | App Lifecycle | .stop() | None | MEDIUM |
| 	hreading.Thread | rp_scanner.py, 
outer_discovery.py | Ad-hoc network scan | Daemon Thread | Garbage Collection | LOW |
| ThreadPoolExecutor | Scanner Modules | Ad-hoc bulk scan | Context Manager (with) | .shutdown() via context | LOW |
| subprocess.run | Scanner / Discovery | Ad-hoc commands | Blocks thread | None | LOW |
| subprocess.Popen | health_engine.py | Background ping | .kill() / .terminate() | Wait for exit | MEDIUM |
