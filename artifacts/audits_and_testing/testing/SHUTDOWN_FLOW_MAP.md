# SHUTDOWN FLOW MAP

## 1. Application Exit Flow Sequence
1. User clicks close button.
2. MainWindow.closeEvent(event) is triggered.
3. Checks _is_shutting_down. If true, returns immediately.
4. Calls self._close_app(force_bypass_tray=False).
5. Evaluates smart conditions:
   - First-time close prompt.
   - Minimize to tray behavior.
   - Unsaved settings (unsaved).
   - Active Mikrotik connection (connected).
   - Active critical operations (g_tasks, critical_operations).
6. Based on response, calls self._finalize_and_exit().

## 2. Finalize and Exit Routine (_finalize_and_exit)
1. **[SHUTDOWN] Step 1:** Starts shutdown flag (_is_shutting_down = True).
2. **[SHUTDOWN] Step 2:** Saves session state (last_active_page).
3. **[SHUTDOWN] Step 3:** Stops workers (_stop_all_workers()).
4. **[SHUTDOWN] Step 4:** Commits and closes database (self._db.close()).
5. **[SHUTDOWN] Step 5:** Saves state (last_exit_time).
6. **[SHUTDOWN] Step 6:** Marks clean shutdown (CLEAN_FLAG.touch(), LOCK_FILE.unlink()).
7. **[SHUTDOWN] Step 7:** Flushes logs (logging.shutdown()).
8. **[SHUTDOWN] Step 8:** QCoreApplication.quit().

## Sequence Diagram

`mermaid
sequenceDiagram
    participant User
    participant MW as MainWindow
    participant Workers as QThread Workers
    participant DB as Database
    participant Core as QApplication

    User->>MW: Clicks Close
    MW->>MW: closeEvent()
    MW->>MW: _close_app()
    alt Minimized to Tray
        MW->>MW: hide()
    else Quit Approved
        MW->>MW: _finalize_and_exit()
        MW->>Workers: _stop_all_workers()
        Workers->>MW: wait(5000)
        alt Wait Timeout
            MW->>Workers: terminate()
            MW->>Workers: wait(1000)
        end
        MW->>DB: close()
        MW->>Core: quit()
    end
`
