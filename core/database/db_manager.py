"""
CafePulse — Database Manager
SQLite-based data layer with schema validation, auto-creation, and corruption recovery.
"""

import logging
import shutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger("cafepulse.database")

SCHEMA_VERSION = 1


# ─── SQL Definitions ──────────────────────────────────────────────────────────

DDL_META = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

DDL_DEVICES = """
CREATE TABLE IF NOT EXISTS devices (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address  TEXT NOT NULL,
    mac_address TEXT UNIQUE NOT NULL,
    hostname    TEXT DEFAULT '',
    vendor      TEXT DEFAULT '',
    first_seen  TEXT NOT NULL,
    last_seen   TEXT NOT NULL,
    status      TEXT DEFAULT 'online'
);
"""

DDL_SESSIONS = """
CREATE TABLE IF NOT EXISTS sessions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id      INTEGER NOT NULL,
    session_start  TEXT NOT NULL,
    session_end    TEXT,
    mode           TEXT DEFAULT 'unknown',
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);
"""

DDL_TRAFFIC_LOGS = """
CREATE TABLE IF NOT EXISTS traffic_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id       INTEGER NOT NULL,
    upload_speed    REAL DEFAULT 0.0,
    download_speed  REAL DEFAULT 0.0,
    timestamp       TEXT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);
"""

DDL_ALERTS = """
CREATE TABLE IF NOT EXISTS alerts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type  TEXT NOT NULL,
    device_id   INTEGER,
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    is_read     INTEGER DEFAULT 0,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE SET NULL
);
"""

DDL_SETTINGS = """
CREATE TABLE IF NOT EXISTS settings (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    key   TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL
);
"""

DDL_ROUTERS = """
CREATE TABLE IF NOT EXISTS routers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    host        TEXT NOT NULL,
    port        INTEGER DEFAULT 8728,
    username    TEXT NOT NULL,
    password    TEXT NOT NULL,
    use_ssl     INTEGER DEFAULT 0,
    is_favorite INTEGER DEFAULT 0,
    group_name  TEXT DEFAULT 'General',
    tags        TEXT DEFAULT '',
    created_at  TEXT NOT NULL
);
"""

DDL_ACCESS_PACKAGES = """
CREATE TABLE IF NOT EXISTS access_packages (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    package_type TEXT NOT NULL,
    duration_seconds INTEGER DEFAULT 0,
    quota_bytes INTEGER DEFAULT 0,
    speed_limit_down INTEGER DEFAULT 0,
    speed_limit_up INTEGER DEFAULT 0,
    price REAL DEFAULT 0.0,
    created_at TEXT NOT NULL
);
"""

DDL_CUSTOMERS = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    notes TEXT,
    active_token TEXT,
    created_at TEXT NOT NULL
);
"""

DDL_VOUCHERS = """
CREATE TABLE IF NOT EXISTS vouchers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    package_id TEXT NOT NULL,
    status TEXT DEFAULT 'Active',
    used_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (package_id) REFERENCES access_packages(id) ON DELETE CASCADE
);
"""

ALL_DDL = [
    DDL_META, DDL_ROUTERS, DDL_DEVICES, DDL_SESSIONS, 
    DDL_TRAFFIC_LOGS, DDL_ALERTS, DDL_SETTINGS,
    DDL_ACCESS_PACKAGES, DDL_CUSTOMERS, DDL_VOUCHERS
]



# ─── DatabaseManager ──────────────────────────────────────────────────────────

class DatabaseManager:
    """
    Manages the SQLite database lifecycle.
    - Auto-creates tables on first run
    - Validates schema version
    - Handles corruption with backup and re-init
    - Provides safe query helpers
    """

    def __init__(self, db_path: str | Path | None = None):
        if db_path is None:
            raise ValueError("db_path must be provided to DatabaseManager")
        self._path = Path(db_path)
        self._conn: sqlite3.Connection | None = None
        self._connect()

    # ─── Connection ───────────────────────────────────────────────────────────

    def _connect(self) -> None:
        """Open connection and initialize schema."""
        try:
            self._conn = sqlite3.connect(
                str(self._path),
                check_same_thread=False,
                timeout=10,
            )
            self._conn.row_factory = sqlite3.Row
            
            # Check DB integrity to catch silent corruption early
            cursor = self._conn.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result and result[0].lower() != "ok":
                raise sqlite3.DatabaseError(f"Integrity check failed: {result[0]}")
                
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._initialize_schema()
            logger.info("Database connected: %s", self._path)
        except sqlite3.DatabaseError as exc:
            logger.error("Database connection failed or corrupt: %s", exc)
            self._handle_corruption()

    def _initialize_schema(self) -> None:
        """Create all tables and set schema version if needed."""
        cursor = self._conn.cursor()
        for ddl in ALL_DDL:
            cursor.execute(ddl)
        self._conn.commit()
        self._set_meta("schema_version", str(SCHEMA_VERSION))
        self._set_meta("created_at", datetime.now().isoformat())
        logger.debug("Schema initialized (version %s)", SCHEMA_VERSION)

    def _handle_corruption(self) -> None:
        """Backup corrupt DB and re-create a fresh one."""
        if self._path.exists():
            backup = self._path.with_suffix(".db.bak")
            try:
                shutil.copy2(self._path, backup)
                logger.warning("Corrupt DB backed up to %s", backup)
                self._path.unlink()
            except OSError as exc:
                logger.error("Could not backup corrupt DB: %s", exc)
        logger.info("Re-creating fresh database...")
        self._connect()

    def reconnect(self) -> bool:
        """Attempt to reconnect to the database."""
        try:
            if self._conn:
                self._conn.close()
        except Exception:
            pass
        try:
            self._connect()
            return True
        except Exception as exc:
            logger.error("Reconnect failed: %s", exc)
            return False

    def close(self) -> None:
        """Safely close the database connection."""
        if self._conn:
            try:
                self._conn.close()
                logger.info("Database connection closed")
            except Exception:
                pass
            self._conn = None

    def get_connection(self) -> sqlite3.Connection:
        """Mengembalikan objek koneksi database SQLite aktif secara aman."""
        if not self._conn:
            self._connect()
        return self._conn

    # ─── Meta ─────────────────────────────────────────────────────────────────

    def _set_meta(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT INTO meta(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        self._conn.commit()

    def get_meta(self, key: str) -> str | None:
        row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None

    # ─── Generic Query Helpers ────────────────────────────────────────────────

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a write statement (INSERT, UPDATE, DELETE)."""
        cursor = self._conn.execute(sql, params)
        self._conn.commit()
        return cursor

    def fetchall(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        return self._conn.execute(sql, params).fetchall()

    def fetchone(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        return self._conn.execute(sql, params).fetchone()

    # ─── Devices ──────────────────────────────────────────────────────────────

    def upsert_device(self, ip: str, mac: str, hostname: str = "", vendor: str = "", status: str = "online") -> int:
        now = datetime.now().isoformat()
        existing = self.fetchone("SELECT id FROM devices WHERE mac_address=?", (mac,))
        if existing:
            if status == "online":
                self.execute(
                    "UPDATE devices SET ip_address=?, hostname=?, vendor=?, last_seen=?, status=? WHERE mac_address=?",
                    (ip, hostname, vendor, now, status, mac),
                )
            else:
                self.execute(
                    "UPDATE devices SET ip_address=?, hostname=?, vendor=?, status=? WHERE mac_address=?",
                    (ip, hostname, vendor, status, mac),
                )
            return existing["id"]
        cursor = self.execute(
            "INSERT INTO devices(ip_address, mac_address, hostname, vendor, first_seen, last_seen, status) VALUES(?,?,?,?,?,?,?)",
            (ip, mac, hostname, vendor, now, now, status),
        )
        return cursor.lastrowid

    def get_all_devices(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM devices ORDER BY last_seen DESC")

    def get_device_count(self) -> int:
        row = self.fetchone("SELECT COUNT(*) as cnt FROM devices WHERE status='online'")
        return row["cnt"] if row else 0

    def prune_stale_devices(self, days: int = 30) -> None:
        """Remove devices that haven't been seen in N days."""
        threshold = (datetime.now() - timedelta(days=days)).isoformat()
        try:
            self.execute("DELETE FROM devices WHERE last_seen < ?", (threshold,))
        except Exception as exc:
            logger.error("Failed to prune stale devices: %s", exc)

    def clear_all_devices(self) -> None:
        """Delete ALL devices, sessions, and traffic logs.
        Called when switching away from Demo Mode to a real scan mode,
        so demo-generated fake devices do not pollute real scan results.
        """
        try:
            self.execute("DELETE FROM traffic_logs")
            self.execute("DELETE FROM sessions")
            self.execute("DELETE FROM devices")
            logger.info("All devices cleared (mode switch)")
        except Exception as exc:
            logger.error("Failed to clear devices: %s", exc)

    # ─── Traffic Logs ─────────────────────────────────────────────────────────

    def insert_traffic(self, device_id: int, upload: float, download: float) -> None:
        now = datetime.now().isoformat()
        self.execute(
            "INSERT INTO traffic_logs(device_id, upload_speed, download_speed, timestamp) VALUES(?,?,?,?)",
            (device_id, upload, download, now),
        )

    def get_recent_traffic(self, device_id: int, limit: int = 60) -> list[sqlite3.Row]:
        return self.fetchall(
            "SELECT * FROM traffic_logs WHERE device_id=? ORDER BY timestamp DESC LIMIT ?",
            (device_id, limit),
        )

    # ─── Alerts ───────────────────────────────────────────────────────────────

    def insert_alert(self, alert_type: str, message: str, device_id: int | None = None) -> None:
        now = datetime.now().isoformat()
        self.execute(
            "INSERT INTO alerts(alert_type, device_id, message, created_at) VALUES(?,?,?,?)",
            (alert_type, device_id, message, now),
        )

    def get_unread_alerts(self) -> list[sqlite3.Row]:
        return self.fetchall(
            "SELECT * FROM alerts WHERE is_read=0 ORDER BY created_at DESC"
        )

    def get_all_alerts(self, limit: int = 100) -> list[sqlite3.Row]:
        return self.fetchall(
            "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?", (limit,)
        )

    def mark_alerts_read(self) -> None:
        self.execute("UPDATE alerts SET is_read=1 WHERE is_read=0")

    def clear_all_alerts(self) -> None:
        self.execute("DELETE FROM alerts")

    # ─── Routers (Multi-Router Engine) ────────────────────────────────────────

    def add_router(self, name: str, host: str, port: int, username: str, password_encrypted: str, use_ssl: bool = False, group_name: str = "General", tags: str = "") -> int:
        now = datetime.now().isoformat()
        cursor = self.execute(
            "INSERT INTO routers(name, host, port, username, password, use_ssl, group_name, tags, created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (name, host, port, username, password_encrypted, 1 if use_ssl else 0, group_name, tags, now)
        )
        return cursor.lastrowid

    def get_all_routers(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM routers ORDER BY is_favorite DESC, name ASC")

    def get_router(self, router_id: int) -> sqlite3.Row | None:
        return self.fetchone("SELECT * FROM routers WHERE id=?", (router_id,))

    def update_router(self, router_id: int, name: str, host: str, port: int, username: str, password_encrypted: str, use_ssl: bool, group_name: str, tags: str) -> None:
        self.execute(
            "UPDATE routers SET name=?, host=?, port=?, username=?, password=?, use_ssl=?, group_name=?, tags=? WHERE id=?",
            (name, host, port, username, password_encrypted, 1 if use_ssl else 0, group_name, tags, router_id)
        )

    def delete_router(self, router_id: int) -> None:
        self.execute("DELETE FROM routers WHERE id=?", (router_id,))

    def set_router_favorite(self, router_id: int, is_favorite: bool) -> None:
        self.execute("UPDATE routers SET is_favorite=? WHERE id=?", (1 if is_favorite else 0, router_id))

    # ─── Cleanup ──────────────────────────────────────────────────────────────

    def cleanup_old_logs(self, days: int = 30) -> None:
        """Delete traffic_logs older than `days` days."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        cursor = self.execute("DELETE FROM traffic_logs WHERE timestamp < ?", (cutoff,))
        if cursor.rowcount:
            logger.info("Cleaned up %d old traffic log entries", cursor.rowcount)

    # ─── Settings ─────────────────────────────────────────────────────────────

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.fetchone("SELECT value FROM settings WHERE key=?", (key,))
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        self.execute(
            "INSERT INTO settings(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    # ─── IAM Access Packages ──────────────────────────────────────────────────

    def add_access_package(self, pkg_id: str, name: str, pkg_type: str, duration_sec: int, quota_bytes: int, speed_dn: int, speed_up: int, price: float) -> None:
        now = datetime.now().isoformat()
        self.execute(
            "INSERT INTO access_packages(id, name, package_type, duration_seconds, quota_bytes, speed_limit_down, speed_limit_up, price, created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (pkg_id, name, pkg_type, duration_sec, quota_bytes, speed_dn, speed_up, price, now)
        )

    def get_all_access_packages(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM access_packages ORDER BY price ASC, name ASC")

    def delete_access_package(self, pkg_id: str) -> None:
        self.execute("DELETE FROM access_packages WHERE id=?", (pkg_id,))

    # ─── IAM Customers ────────────────────────────────────────────────────────

    def add_customer(self, name: str, phone: str = "", notes: str = "", active_token: str = "") -> int:
        now = datetime.now().isoformat()
        cursor = self.execute(
            "INSERT INTO customers(name, phone, notes, active_token, created_at) VALUES(?,?,?,?,?)",
            (name, phone, notes, active_token, now)
        )
        return cursor.lastrowid

    def get_all_customers(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM customers ORDER BY name ASC")

    def delete_customer(self, customer_id: int) -> None:
        self.execute("DELETE FROM customers WHERE id=?", (customer_id,))

    def update_customer_token(self, customer_id: int, active_token: str) -> None:
        self.execute("UPDATE customers SET active_token=? WHERE id=?", (active_token, customer_id))

    # ─── IAM Vouchers ─────────────────────────────────────────────────────────

    def add_voucher(self, code: str, package_id: str) -> int:
        now = datetime.now().isoformat()
        cursor = self.execute(
            "INSERT INTO vouchers(code, package_id, status, created_at) VALUES(?,?,?,?)",
            (code, package_id, "Active", now)
        )
        return cursor.lastrowid

    def get_all_vouchers(self) -> list[sqlite3.Row]:
        return self.fetchall(
            "SELECT v.*, p.name as package_name, p.speed_limit_down, p.speed_limit_up "
            "FROM vouchers v LEFT JOIN access_packages p ON v.package_id = p.id "
            "ORDER BY v.created_at DESC"
        )

    def update_voucher_status(self, code: str, status: str) -> None:
        used_at = datetime.now().isoformat() if status == "Used" else None
        if used_at:
            self.execute("UPDATE vouchers SET status=?, used_at=? WHERE code=?", (status, used_at, code))
        else:
            self.execute("UPDATE vouchers SET status=? WHERE code=?", (status, code))

    def delete_voucher(self, voucher_id: int) -> None:
        self.execute("DELETE FROM vouchers WHERE id=?", (voucher_id,))

