"""
CafePulse — WiFi Scanner
Orchestrates: ARP scan → hostname resolve → vendor lookup → DB upsert → alert.
"""

import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Callable, Optional

from modes.home_wifi.arp_scanner    import scan_network, get_local_ip, ARPEntry, _ping_host
from modes.home_wifi.hostname_resolver import resolve_batch
from modes.home_wifi.vendor_lookup  import VendorLookup

logger = logging.getLogger("cafepulse.homewifi.scanner")


@dataclass
class ScanResult:
    entries:       list[dict]   # [{ip, mac, hostname, vendor, device_id}]
    new_devices:   list[dict]   # devices seen for the first time
    missing:       list[str]    # MACs that went offline
    scan_duration: float        # seconds
    last_scan_time: str
    subnet:        str
    local_ip:      str
    error:         Optional[str] = None


class WiFiScanner:
    """
    High-level scanner that runs ARP discovery and maintains a known-device set.
    Designed to be called repeatedly from WiFiWorker.
    """

    SUSPICIOUS_THRESHOLD = 5  # new devices in one scan = suspicious

    def __init__(self, db, vendor_lookup: VendorLookup):
        self._db            = db
        self._vendor        = vendor_lookup
        self._session_macs: set[str]  = set()   # MACs seen since worker start
        self._missed_counts: dict[str, int] = {}
        self._scan_count    = 0
        self._on_heartbeat_cb = None

        # Callbacks
        self._on_result_cbs:  list[Callable[[ScanResult], None]] = []
        self._on_alert_cbs:   list[Callable[[str, str, Optional[int]], None]] = []

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

    def _emit_alert(self, alert_type: str, message: str, device_id: Optional[int] = None) -> None:
        self._db.insert_alert(alert_type, message, device_id)
        for cb in self._on_alert_cbs:
            try:
                cb({"type": alert_type, "message": message})
            except Exception as exc:
                logger.error("Alert callback error: %s", exc)

    def _is_valid_device(self, ip: str, mac: str) -> bool:
        if not ip or not mac: return False
        mac = mac.lower()
        if mac in ("ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"): return False
        if ip.startswith("169.254.") or ip.startswith("224.") or ip.startswith("239."): return False
        if ip.endswith(".255") or ip == "0.0.0.0" or ip == "255.255.255.255": return False
        return True

    # ─── Core Scan ────────────────────────────────────────────────────────────

    def run_scan(
        self,
        subnet: Optional[str] = None,
        do_ping_sweep: bool = True,
    ) -> ScanResult:
        """Execute one full scan cycle."""
        import time
        start = time.monotonic()
        self._scan_count += 1
        local_ip = get_local_ip()

        self._emit_heartbeat()

        try:
            arp_entries: list[ARPEntry] = scan_network(
                subnet=subnet,
                do_ping_sweep=do_ping_sweep,
                heartbeat_cb=self._emit_heartbeat,
            )
        except Exception as exc:
            logger.error("ARP scan failed: %s", exc)
            result = ScanResult(
                entries=[], new_devices=[], missing=[],
                scan_duration=0, subnet=subnet or "unknown",
                local_ip=local_ip, error=str(exc),
            )
            return result

        self._emit_heartbeat()

        scanned_macs = {e.mac for e in arp_entries}

        # ── Active ping verification for known session devices ────────────────
        ip_to_mac = {e.ip: e.mac for e in arp_entries}
        mac_to_ip: dict[str, str] = {e.mac.lower(): e.ip for e in arp_entries}

        ping_failed_macs: set[str] = set()
        if self._session_macs:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            candidates = [
                (mac, mac_to_ip[mac])
                for mac in self._session_macs
                if mac in mac_to_ip
            ]
            if candidates:
                with ThreadPoolExecutor(max_workers=32, thread_name_prefix="verify") as ex:
                    fut_map = {
                        ex.submit(_ping_host, ip, 400): mac
                        for mac, ip in candidates
                    }
                    for fut in as_completed(fut_map):
                        mac = fut_map[fut]
                        self._emit_heartbeat()
                        try:
                            if not fut.result():
                                ping_failed_macs.add(mac)
                                logger.debug("Ping verify FAILED: %s — marking offline", mac)
                        except Exception:
                            pass

        scanned_macs -= ping_failed_macs
        self._emit_heartbeat()

        # ── Hostname batch resolution ─────────────────────────────────────────
        ips = [e.ip for e in arp_entries]
        hostnames = resolve_batch(ips, timeout=1.2)
        self._emit_heartbeat()

        # ── Query existing devices from DB to use as source of truth ───────────
        try:
            db_devices = self._db.fetchall("SELECT id, ip_address, mac_address, hostname, vendor, status, last_seen FROM devices")
            db_map = {d["mac_address"].lower(): d for d in db_devices}
        except Exception as exc:
            logger.error("Failed to query devices from database: %s", exc)
            db_map = {}

        # ── Build enriched entry list ─────────────────────────────────────────
        enriched:    list[dict] = []
        new_devices: list[dict] = []

        valid_entries = [
            e for e in arp_entries
            if self._is_valid_device(e.ip, e.mac) and e.mac.lower() not in ping_failed_macs
        ]

        scanned_mac_set = set()
        for entry in valid_entries:
            mac_lower = entry.mac.lower()
            scanned_mac_set.add(mac_lower)
            self._missed_counts[mac_lower] = 0
            self._session_macs.add(mac_lower)
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
            is_reconnect = False
            dev_id = None

            if mac_lower in db_map:
                db_device = db_map[mac_lower]
                dev_id = db_device["id"]
                if db_device["status"] == "offline":
                    is_reconnect = True
            else:
                is_new = True

            dev_id = self._db.upsert_device(
                ip=entry.ip, mac=entry.mac,
                hostname=hostname, vendor=vendor,
                status="online",
            )
            
            enriched_entry = {
                "id":       dev_id,
                "ip":       entry.ip,
                "mac":      entry.mac,
                "hostname": hostname,
                "vendor":   vendor,
                "upload":   0.0,
                "download": 0.0,
                "status":   "online",
                "last_seen": datetime.now().strftime("%H:%M:%S")
            }
            enriched.append(enriched_entry)

            # Emit alerts based on true status transitions
            if is_new:
                new_devices.append(enriched_entry)
                self._emit_alert(
                    "new_device",
                    f"New device joined: {hostname} ({entry.ip}) — {vendor or 'unknown vendor'}",
                    dev_id,
                )
            elif is_reconnect:
                self._emit_alert(
                    "reconnect",
                    f"Device is back online: {hostname} ({entry.ip})",
                    dev_id,
                )

        self._emit_heartbeat()

        # ── Detect devices that went offline ─────────────────────────────────
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
                # Apply threshold grace period logic
                if mac.lower() in ping_failed_macs:
                    self._missed_counts[mac_lower] = 99  # confirmed dead, skip grace
                    threshold = 1
                else:
                    self._missed_counts[mac_lower] = self._missed_counts.get(mac_lower, 0) + 1
                    threshold = 3

                if self._missed_counts[mac_lower] >= threshold:
                    actually_missing.append(mac)
                    self._db.upsert_device(
                        ip="", mac=mac,
                        hostname=hostname, vendor=db_device["vendor"] or "",
                        status="offline",
                    )
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
                    self._emit_alert(
                        "offline",
                        f"Device went offline: {hostname} ({last_ip or 'unknown IP'})",
                        dev_id,
                    )
                else:
                    # Still within grace period, keep online in list
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

        # ── Suspicious: many new devices at once ──────────────────────────────
        if len(new_devices) >= self.SUSPICIOUS_THRESHOLD:
            self._emit_alert(
                "suspicious",
                f"{len(new_devices)} new devices detected simultaneously — possible network intrusion scan",
            )

        duration = time.monotonic() - start
        result = ScanResult(
            entries=enriched,
            new_devices=new_devices,
            missing=actually_missing,
            scan_duration=round(duration, 2),
            last_scan_time=datetime.now().strftime("%H:%M:%S"),
            subnet=subnet or "auto",
            local_ip=local_ip,
        )

        for cb in self._on_result_cbs:
            try:
                cb(result)
            except Exception as exc:
                logger.error("Result callback error: %s", exc)

        logger.info(
            "Scan #%d: %d devices, %d new, %.1fs",
            self._scan_count, len(enriched), len(new_devices), duration,
        )
        return result
