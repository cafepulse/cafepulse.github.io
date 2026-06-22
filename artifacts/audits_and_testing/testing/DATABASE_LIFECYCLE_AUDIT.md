# DATABASE LIFECYCLE AUDIT

**File:** core/database/db_manager.py

### Connection Lifecycle
- **Startup:** Uses check_same_thread=False to share a SINGLE sqlite3.Connection across all background QThreads (WiFiWorker, HotspotWorker, MikrotikWorker, etc.).
- **Journal Mode:** Uses PRAGMA journal_mode=WAL. This enables high concurrency but requires safe connection closing to merge the Write-Ahead Log.
- **Shutdown:** self._db.close() is called in main.py inside the inally block, and also logically requested by MainWindow._finalize_and_exit().

### Findings / Defects
1. **Thread Sharing Danger:** Sharing a single connection with check_same_thread=False is highly efficient, but requires strict thread coordination. 
2. **Zombie Locks:** Because _stop_all_workers() forcefully calls worker.terminate() when a timeout occurs, if a worker is terminated **while** it is executing a self._db.execute() command, the internal SQLite lock is abandoned.
3. **Close Failure:** When the Main Thread subsequently calls self._db.close(), it may hang indefinitely waiting for the abandoned lock to release, or fail to merge the .wal file, leading to the reported zombie background process.
