"""
CafePulse — Hotspot Scanner
Orchestrates: detect hotspot subnet → ARP scan → enrich → session tracking → alerts.
Reuses Phase 3 ARP/vendor/hostname infrastructure — no duplication.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

from modes.home_wifi.arp_scanner      import scan_network, ARPEntry, _ping_host
from modes.home_wifi.hostname_resolver import resolve_batch
from modes.home_wifi.vendor_lookup    import VendorLookup
from modes.hotspot.hotspot_detector   import detect_hotspot, HotspotInfo
from modes.hotspot.session_tracker    import SessionTracker

logger = logging.getLogger("cafepulse.hotspot.scanner")


@dataclass
class HotspotScanResult:
    hotspot_info:  HotspotInfo
    devices:       list[dict]
    joined:        list[str]     # MACs that joined this scan
    left:          list[str]     # MACs that left this scan
    active_sessions: list[dict]
    scan_duration: float
    last_scan_time: str
    last_scan_time: str
    error:         Optional[str] = None


class HotspotScanner:
    """
    Quick-refresh hotspot scanner with session tracking.
    Designed for smaller subnets (typically 254 hosts max).
    Default scan interval: 10 seconds.
    """

    def __init__(self, db, vendor_lookup: Optional[VendorLookup] = None):
        self._db             = db
        self._vendor         = vendor_lookup or VendorLookup()
        self._tracker        = SessionTracker(db, mode="hotspot")
        self._hotspot_info:  Optional[HotspotInfo] = None
        self._scan_count     = 0
        self._session_macs:  set[str] = set()   # MACs discovered in this session
        self._missed_counts: dict[str, int] = {}
        self._on_heartbeat_cb = None

        # Callbacks
        self._on_result_cbs: list[Callable] = []
        self._on_alert_cbs:  list[Callable] = []

    # ─── Callbacks ────────────────────────────────────────────────────────────

    def on_result(self, cb: Callable) -> None:
        self._on_result_cbs.append(cb)

    def on_alert(self, cb: Callable) -> None:
        self._on_alert_cbs.append(cb)

    def on_heartbeat(self, cb: Callable) -> None:
        self._on_heartbeat_cb = cb

    def _emit_heartbeat(self) -> None:
        if hasattr(self, "_on_heartbeat_cb") and self._on_heartbeat_cb:
            try:
                self._on_heartbeat_cb()
            except Exception:
                pass

    def _emit_alert(self, alert_type: str, message: str,
                    device_id: Optional[int] = None) -> None:
        self._db.insert_alert(alert_type, message, device_id)
        for cb in self._on_alert_cbs:
            try:
                cb({"type": alert_type, "message": message})
            except Exception:
                pass

    def _is_valid_device(self, ip: str, mac: str) -> bool:
        if not ip or not mac: return False
        mac = mac.lower()
        if mac in ("ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"): return False
        if ip.startswith("169.254.") or ip.startswith("224.") or ip.startswith("239."): return False
        if ip.endswith(".255") or ip == "0.0.0.0" or ip == "255.255.255.255": return False
        return True

    # ─── Scan ─────────────────────────────────────────────────────────────────

    def run_scan(self, subnet: Optional[str] = None) -> HotspotScanResult:
        import time
        start = time.monotonic()
        self._scan_count += 1

        self._emit_heartbeat()

        # Auto-detect hotspot on first scan or when subnet not provided
        if self._hotspot_info is None or subnet is not None:
            self._hotspot_info = detect_hotspot()
            if subnet:
                self._hotspot_info.subnet = subnet

        hinfo = self._hotspot_info

        if not hinfo.subnet:
            err = "No network detected — connect to a hotspot first"
            logger.warning(err)
            result = HotspotScanResult(
                hotspot_info=hinfo, devices=[], joined=[], left=[],
                active_sessions=[], scan_duration=0, last_scan_time=datetime.now().strftime("%H:%M:%S"), error=err,
            )
            self._fire_result(result)
            return result

        # ── ARP scan (fast — small subnet) ───────────────────────────────────
        try:
            arp_entries: list[ARPEntry] = scan_network(
                subnet=hinfo.subnet,
                do_ping_sweep=True,
                ping_workers=32,   # hotspot nets are small, 32 is enough
                heartbeat_cb=self._emit_heartbeat,
            )
        except Exception as exc:
            logger.error("Hotspot ARP scan failed: %s", exc)
            result = HotspotScanResult(
                hotspot_info=hinfo, devices=[], joined=[], left=[],
                active_sessions=[], scan_duration=0, last_scan_time=datetime.now().strftime("%H:%M:%S"), error=str(exc),
            )
            self._fire_result(result)
            return result

        self._emit_heartbeat()

        scanned_macs = {e.mac for e in arp_entries}

        # ── Active ping verification for known session devices ─────────────────────────────
        mac_to_ip: dict[str, str] = {e.mac: e.ip for e in arp_entries}
        ping_failed_macs: set[str] = set()
        if self._session_macs:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            candidates = [(mac, mac_to_ip[mac]) for mac in self._session_macs if mac in mac_to_ip]
            if candidates:
                with ThreadPoolExecutor(max_workers=32, thread_name_prefix="hs_verify") as ex:
                    fut_map = {ex.submit(_ping_host, ip, 400): mac for mac, ip in candidates}
                    for fut in as_completed(fut_map):
                        mac = fut_map[fut]
                        self._emit_heartbeat()
                        try:
                            if not fut.result():
                                ping_failed_macs.add(mac)
                                logger.debug("Hotspot ping verify FAILED: %s", mac)
                        except Exception:
                            pass

        scanned_macs -= ping_failed_macs
        self._emit_heartbeat()

        # ── Hostname resolution ──────────────────────────────────────────
        ips = [e.ip for e in arp_entries]
        hostnames = resolve_batch(ips, timeout=1.0)
        self._emit_heartbeat()

        # ── Query existing devices from DB to use as source of truth ───────────
        try:
            db_devices = self._db.fetchall("SELECT id, ip_address, mac_address, hostname, vendor, status, last_seen FROM devices")
            db_map = {d["mac_address"].lower(): d for d in db_devices}
        except Exception as exc:
            logger.error("Failed to query devices from database: %s", exc)
            db_map = {}

        # ── Enrich + DB upsert ──────────────────────────────────────────
        current_macs:  set[str]   = set()
        mac_to_dev_id: dict[str, int] = {}
        enriched:      list[dict] = []

        valid_entries = [e for e in arp_entries
                         if self._is_valid_device(e.ip, e.mac)
                         and e.mac not in ping_failed_macs]

        scanned_mac_set = set()
        for entry in valid_entries:
            mac_lower = entry.mac.lower()
            scanned_mac_set.add(mac_lower)
            self._missed_counts[mac_lower] = 0
            self._session_macs.add(entry.mac)
            hostname = hostnames.get(entry.ip, "")
            vendor   = self._vendor.lookup(entry.mac) or "Unknown Vendor"

            # Use last-known hostname from DB if resolution failed
            if not hostname or hostname.startswith("device-") or hostname.startswith("Unknown"):
                if mac_lower in db_map:
                    prev_host = db_map[mac_lower]["hostname"]
                    if prev_host and not prev_host.startswith("device-") and not prev_host.startswith("Unknown"):
                        hostname = prev_host

            if not hostname:
                hostname = f"Unknown Device ({entry.ip})"

            is_new = False
            dev_id = None

            if mac_lower in db_map:
                db_device = db_map[mac_lower]
                dev_id = db_device["id"]
            else:
                is_new = True

            dev_id = self._db.upsert_device(
                ip=entry.ip, mac=entry.mac,
                hostname=hostname, vendor=vendor, status="online",
            )
            current_macs.add(entry.mac)
            mac_to_dev_id[entry.mac] = dev_id

            # New device alert (Truly new to the system)
            if is_new:
                self._emit_alert(
                    "new_device",
                    f"New device on hotspot: {hostname} ({entry.ip}) — {vendor}",
                    dev_id,
                )

            enriched.append({
                "id":       dev_id,
                "ip":       entry.ip,
                "mac":      entry.mac,
                "hostname": hostname,
                "vendor":   vendor,
                "upload":   0.0,
                "download": 0.0,
                "status":   "online",
                "last_seen": datetime.now().strftime("%H:%M:%S")
            })

        self._emit_heartbeat()

        # ── Detect devices that went offline ──────────────────────────────────
        actually_missing = []
        for mac_lower, db_device in db_map.items():
            if mac_lower in scanned_mac_set:
                continue

            mac = db_device["mac_address"]
            hostname = db_device["hostname"]
            last_ip = db_device["ip_address"]
            dev_id = db_device["id"]

            ls = db_device["last_seen"]
            if "T" in ls:
                ls = ls.split("T")[1][:8]

            if db_device["status"] == "offline":
                # Already offline in DB, keep it offline and include in list
                enriched.append({
                    "id":       dev_id,
                    "ip":       "",
                    "mac":      mac,
                    "hostname": hostname,
                    "vendor":   db_device["vendor"] or "Unknown Vendor",
                    "upload":   0.0,
                    "download": 0.0,
                    "status":   "offline",
                    "last_seen": ls
                })
            else:
                # Device was online in DB but is missing in the current scan
                # Apply 3-scan grace period threshold
                if mac in ping_failed_macs:
                    self._missed_counts[mac_lower] = 99
                    threshold = 1
                else:
                    self._missed_counts[mac_lower] = self._missed_counts.get(mac_lower, 0) + 1
                    threshold = 3

                if self._missed_counts[mac_lower] >= threshold:
                    actually_missing.append(mac)
                    self._db.upsert_device("", mac, hostname, db_device["vendor"] or "", "offline")
                    enriched.append({
                        "id":       dev_id,
                        "ip":       "",
                        "mac":      mac,
                        "hostname": hostname,
                        "vendor":   db_device["vendor"] or "Unknown Vendor",
                        "upload":   0.0,
                        "download": 0.0,
                        "status":   "offline",
                        "last_seen": ls
                    })
                else:
                    # Keep online
                    current_macs.add(mac)
                    mac_to_dev_id[mac] = dev_id
                    enriched.append({
                        "id":       dev_id,
                        "ip":       last_ip,
                        "mac":      mac,
                        "hostname": hostname,
                        "vendor":   db_device["vendor"] or "Unknown Vendor",
                        "upload":   0.0,
                        "download": 0.0,
                        "status":   "online",
                        "last_seen": ls
                    })

        self._emit_heartbeat()

        # ── Session tracking ──────────────────────────────────────────────────
        joined, left = self._tracker.on_scan_result(current_macs, mac_to_dev_id)

        # Alerts for join/leave events
        for mac in joined:
            dev = next((d for d in enriched if d["mac"] == mac), None)
            if dev:
                self._emit_alert(
                    "reconnect",
                    f"Device joined hotspot: {dev['hostname']} ({dev['ip']})",
                    dev["id"],
                )

        if left:
            self._emit_alert(
                "reconnect",
                f"{len(left)} device(s) disconnected from hotspot",
            )

        # Frequent reconnect detection
        reconnects = self._tracker.get_reconnect_counts(limit=1)
        if reconnects and reconnects[0]["sessions"] >= 5:
            dev_name = reconnects[0]["hostname"]
            self._emit_alert(
                "reconnect",
                f"Frequent reconnections detected: {dev_name} "
                f"({reconnects[0]['sessions']} sessions)",
            )

        active_sessions = self._tracker.get_active_sessions()
        duration = time.monotonic() - start

        result = HotspotScanResult(
            hotspot_info=hinfo,
            devices=enriched,
            joined=joined,
            left=left,
            active_sessions=active_sessions,
            scan_duration=round(duration, 2),
            last_scan_time=datetime.now().strftime("%H:%M:%S"),
        )

        logger.info(
            "Hotspot scan #%d: %d devices, %d joined, %d left, %.1fs",
            self._scan_count, len(enriched), len(joined), len(left), duration,
        )
        self._fire_result(result)
        return result

    def _fire_result(self, result: HotspotScanResult) -> None:
        for cb in self._on_result_cbs:
            try:
                cb(result)
            except Exception as exc:
                logger.error("Result callback error: %s", exc)

    def shutdown(self) -> None:
        """Close all sessions on scanner shutdown."""
        self._tracker.close_all()
