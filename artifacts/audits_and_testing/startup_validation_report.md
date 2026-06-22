# CafePulse — PHASE 2: Application Startup Validation Report
**Generated:** 2026-06-05  
**Scope:** `main.py` startup sequence, all fallback paths, failure modes

---

## OVERVIEW

`main.py` is well-structured with a proper `StartupValidator` class, splash screen, global exception handler, safe mode window, and clean shutdown flags. The architecture is sound. However, several path-resolution issues create real-world failures when packaged and installed.

---

## STARTUP SEQUENCE (Actual Flow)

```
1. setup_logging()           ← Early bootstrap logger
2. sys.excepthook assigned   ← Global crash handler
3. QApplication created      ← Qt initialized
4. QIcon set from logo.png   ← Graceful fallback if missing
5. SplashScreen shown        ← From splash.png or logo.png fallback
6. StartupValidator.run()    ← Checks Python, dirs, config, deps, write
7. If validation fails       ← launch_safe_mode() shown
8. Clean shutdown flag check ← Recovery mode if unclean exit
9. Lock file created         ← config/.lock
10. ConfigManager loaded     ← config/settings.json
11. Logging reconfigured     ← with config values
12. DatabaseManager init     ← cafepulse.db
13. Theme applied            ← dark_theme or light_theme
14. MainWindow launched      ← Full UI
15. app.exec() loop          ← Main Qt event loop
16. db.close()               ← Database closed
17. Clean flag written       ← config/.clean
18. sys.exit(exit_code)      ← Process ends
```

---

## VALIDATION SCENARIO RESULTS

### Scenario 1: `settings.json` is missing

**What happens:**
- `_check_config()` detects the missing file → logs a WARNING but returns **no errors**.
- `is_first_run = True` → skips recovery mode dialog.
- `ConfigManager` loads with all defaults.
- App launches normally.

**Verdict:** ✅ HANDLED — graceful fallback to defaults.

---

### Scenario 2: `cafepulse.db` is missing

**What happens:**
- `DatabaseManager(db_path="cafepulse.db")` is called.
- `DatabaseManager` creates a new database file with `CREATE TABLE IF NOT EXISTS` statements.
- App launches with an empty, freshly initialized database.

**Verdict:** ✅ HANDLED — database auto-created on first launch.

**⚠️ Packaging Risk:** `db_path="cafepulse.db"` is relative. After PyInstaller packaging:
- If launched via shortcut from Desktop → DB created at `C:\Users\USER\Desktop\cafepulse.db`
- If launched from Start Menu → DB created at `C:\Program Files\CafePulse\cafepulse.db` (requires admin rights)
- If launched by double-clicking the EXE → DB created wherever the EXE is.

**This is a CRITICAL bug.** The database location will be non-deterministic. Users will see empty data on every session.

---

### Scenario 3: `logo.png` is missing

**What happens:**
- `logo_path = assets/branding/logo.png` — checked first.
- Falls back to `assets/logo.png`.
- If neither exists, `app.setWindowIcon()` is skipped silently.
- Splash screen: `splash.png` is checked → falls back to `logo.png` → falls back to `assets/logo.png`.
- If all are missing, `CafePulseSplashScreen(str(splash_path))` is called with a non-existent path.

**Potential Issue:** `CafePulseSplashScreen` behavior when passed a missing path is not verified here. If it raises an exception, the global exception handler catches it and shows a dialog, but the splash is never shown. App may still launch.

**Verdict:** ⚠️ PARTIAL — likely survives, but unverified behavior at the splash level.

---

### Scenario 4: `license.dat` is missing

**What happens:**
- `LicensingManager.check_license()` checks for `config/license.lic`.
- If missing: returns `False` → user treated as Free Edition.
- No crash, no error dialog.

**Verdict:** ✅ HANDLED — Free Edition mode activated silently.

---

### Scenario 5: Network unavailable

**What happens:**
- All network operations are done in background `QThread` workers.
- Missing network → workers return empty data or timeout.
- UI shows "No data" or empty state widgets.
- `StartupValidator` does NOT check network availability.

**Verdict:** ✅ HANDLED — Local-first design works correctly offline.

---

### Scenario 6: MikroTik unavailable

**What happens:**
- `MikrotikWorker` attempts connection, times out, emits error signal.
- Network page shows disconnected state.
- All other app features (Dashboard, Devices, Analytics) continue to function normally.

**Verdict:** ✅ HANDLED — MikroTik is optional, not required for app startup.

---

### Scenario 7: Python < 3.12

**What happens:**
- `_check_python_version()` returns an error string.
- `StartupValidator.run()` returns `ok=False`.
- `launch_safe_mode()` is shown with the version error.
- App exits with code 1.

**Verdict:** ✅ HANDLED — Safe mode correctly shown. *(Note: After PyInstaller packaging, Python is bundled — this check always passes in the packaged app.)*

---

### Scenario 8: Missing required dependency

**What happens:**
- `DependencyRegistry.check_all()` returns missing required packages.
- Each missing package adds an error message.
- `launch_safe_mode()` shows which packages are missing with install instructions.

**Verdict:** ✅ HANDLED — *(Note: After PyInstaller packaging, all deps are bundled — this check always passes.)*

---

### Scenario 9: `logs/` or `exports/` not writable

**What happens:**
- `_check_writable_dirs()` attempts to create a `.write_test` file.
- If `Program Files\CafePulse\logs` is not writable (UAC restriction), this returns an error.
- `launch_safe_mode()` is shown.

**Verdict:** ⚠️ RISK — After installation to `Program Files`, `logs/` and `exports/` are inside the install directory. Standard Windows UAC prevents writing there without elevation. This is a CRITICAL installer design flaw. These writable directories must be placed in `%APPDATA%\CafePulse\` instead.

---

### Scenario 10: Previous session crashed (no `.clean` flag)

**What happens:**
- `clean_flag.exists()` returns `False`.
- `is_first_run` is also `False`.
- A `QMessageBox` appears: "Recovered from an unexpected shutdown."
- No data recovery is actually performed beyond the message.

**Verdict:** ✅ ACCEPTABLE — Honest messaging. No false recovery claims.

---

## CRITICAL PATH PROBLEMS SUMMARY

| Problem | Impact | Fix Required |
|---|---|---|
| `cafepulse.db` path is relative | 🔴 CRITICAL | Use `%APPDATA%\CafePulse\` for DB path |
| `config/license.lic` path is relative | 🔴 CRITICAL | Use `%APPDATA%\CafePulse\` for license path |
| `logs/` and `exports/` inside install dir | 🔴 CRITICAL | Redirect to `%APPDATA%\CafePulse\` |
| `config/settings.json` inside install dir | 🔴 CRITICAL | Copy to `%APPDATA%\CafePulse\` on first run |
| Splash path fallback to non-existent | 🟡 MEDIUM | Add explicit check before passing to SplashScreen |

---

*End of Phase 2 — Startup Validation Report*
