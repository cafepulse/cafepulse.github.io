# SUBPROCESS AUDIT

We audited all usages of subprocess.Popen and subprocess.run.

### subprocess.Popen (in core/analytics/health_engine.py)
- **Usage:** Background ping monitoring.
- **Timeout:** Explicitly uses stdout, stderr = proc.communicate(timeout=1.5).
- **Finding / Defect:** When TimeoutExpired is caught, the code 
eturn False, 0.0 is executed, but **proc.kill() is NEVER called**. This leaves zombie ping.exe processes running indefinitely in the background!

### subprocess.run (in 
outer_discovery.py, rp_scanner.py, wifi_scanner.py)
- **Usage:** Used for executing rp -a, ip route, and ping commands.
- **Timeout:** Some use 	imeout=2 or 	imeout=1.5. Some rp -a calls do not specify a timeout at all!
- **Finding / Defect:** Since subprocess.run is a blocking call, any missing timeout or system hang on these shell commands will permanently freeze the worker QThread. Because QThread.stop() waits 5 seconds before calling .terminate(), the thread is forcefully killed, but the underlying rp.exe or ping.exe handle might remain open or zombie-fied.

