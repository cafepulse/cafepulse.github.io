"""
CafePulse — Hotspot Session Tracker
Tracks device join/leave events using the sessions table.
Maintains in-memory state of open sessions, persists to SQLite.
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("cafepulse.hotspot.sessions")


class SessionTracker:
    """
    Manages device sessions for Hotspot Mode.

    A session = one continuous connection period for a device.
    On join  → INSERT sessions row with session_start
    On leave → UPDATE sessions row with session_end
    """

    def __init__(self, db, mode: str = "hotspot"):
        self._db   = db
        self._mode = mode
        # { mac_address: session_id }
        self._open_sessions: dict[str, int] = {}
        self._session_stats: dict[str, int] = {}   # mac → total sessions count

    # ─── Core API ─────────────────────────────────────────────────────────────

    def on_scan_result(
        self,
        current_macs:  set[str],
        mac_to_dev_id: dict[str, int],
    ) -> tuple[list[str], list[str]]:
        """
        Compare current scan results with open sessions.

        Returns:
            joined  — MACs that just joined
            left    — MACs that just left
        """
        previously_online = set(self._open_sessions.keys())
        joined = list(current_macs - previously_online)
        left   = list(previously_online - current_macs)

        # Open sessions for new devices
        for mac in joined:
            dev_id = mac_to_dev_id.get(mac)
            if dev_id:
                sid = self._open_session(dev_id, mac)
                self._session_stats[mac] = self._session_stats.get(mac, 0) + 1
                logger.debug("Session opened: %s (sid=%d)", mac, sid)

        # Close sessions for departed devices
        for mac in left:
            self._close_session(mac)
            logger.debug("Session closed: %s", mac)

        return joined, left

    def _open_session(self, device_id: int, mac: str) -> int:
        """Insert a new session row and return its ID."""
        now = datetime.now().isoformat()
        cursor = self._db.execute(
            "INSERT INTO sessions(device_id, session_start, mode) VALUES (?,?,?)",
            (device_id, now, self._mode),
        )
        sid = cursor.lastrowid
        self._open_sessions[mac] = sid
        return sid

    def _close_session(self, mac: str) -> None:
        """Set session_end for an open session."""
        sid = self._open_sessions.pop(mac, None)
        if sid:
            now = datetime.now().isoformat()
            self._db.execute(
                "UPDATE sessions SET session_end=? WHERE id=?",
                (now, sid),
            )

    def close_all(self) -> None:
        """Close all open sessions (called when mode stops)."""
        for mac in list(self._open_sessions.keys()):
            self._close_session(mac)
        logger.info("All hotspot sessions closed")

    # ─── Analytics Queries ────────────────────────────────────────────────────

    def get_active_sessions(self) -> list[dict]:
        """Return all currently-open sessions with device info."""
        rows = self._db.fetchall(
            """
            SELECT s.id, s.device_id, s.session_start, s.mode,
                   d.ip_address, d.mac_address, d.hostname, d.vendor
            FROM sessions s
            JOIN devices d ON s.device_id = d.id
            WHERE s.session_end IS NULL
            ORDER BY s.session_start DESC
            """
        )
        now = datetime.now()
        result = []
        for row in rows:
            try:
                start = datetime.fromisoformat(row["session_start"])
                duration_s = int((now - start).total_seconds())
            except Exception:
                duration_s = 0
            result.append({
                "session_id":    row["id"],
                "device_id":     row["device_id"],
                "session_start": row["session_start"],
                "ip":            row["ip_address"],
                "mac":           row["mac_address"],
                "hostname":      row["hostname"],
                "vendor":        row["vendor"],
                "duration_s":    duration_s,
                "duration_str":  _fmt_duration(duration_s),
            })
        return result

    def get_session_count(self, device_id: Optional[int] = None) -> int:
        """Total sessions, optionally filtered by device."""
        if device_id:
            row = self._db.fetchone(
                "SELECT COUNT(*) as c FROM sessions WHERE device_id=?", (device_id,)
            )
        else:
            row = self._db.fetchone("SELECT COUNT(*) as c FROM sessions")
        return row["c"] if row else 0

    def get_reconnect_counts(self, limit: int = 10) -> list[dict]:
        """Devices with most reconnections (repeated joins)."""
        rows = self._db.fetchall(
            """
            SELECT d.hostname, d.mac_address, COUNT(s.id) as sessions
            FROM sessions s
            JOIN devices d ON s.device_id = d.id
            GROUP BY s.device_id
            ORDER BY sessions DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in rows]


def _fmt_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        return f"{h}h {m}m"
