"""
CafePulse — Home WiFi Engine
Orchestrates periodic ARP scans, tracks device state changes,
generates alerts for new/suspicious/disconnected devices.
"""

import logging
from datetime import datetime
from typing import Callable

from core.scanner.arp_scanner import scan_network, DiscoveredDevice

logger = logging.getLogger("cafepulse.homewifi.engine")


class HomeWifiEngine:
    """
    Stateful engine for Home WiFi Mode.
    Tracks previous scan state to detect:
     - New devices joining
     - Devices going offline
     - Repeated reconnections (suspicious)
    
    Call scan() periodically; registers callbacks same interface as DemoEngine.
    """

    def __init__(
        self,
        db,
        do_ping_sweep: bool = True,
        resolve_hostnames: bool = True,
        resolve_vendors: bool = True,
    ):
        self._db                = db
        self._do_ping_sweep     = do_ping_sweep
        self._resolve_hostnames = resolve_hostnames
        self._resolve_vendors   = resolve_vendors

        # Previous scan state: mac -> DiscoveredDevice
        self._known_devices: dict[str, DiscoveredDevice] = {}
        # Reconnect counter: mac -> count
        self._reconnect_counts: dict[str, int] = {}

        self._tick_count   = 0
        self._scan_errors  = 0

        self._on_tick_cbs:     list[Callable] = []
        self._on_alert_cbs:    list[Callable] = []
        self._on_progress_cbs: list[Callable] = []

    # ─── Callbacks ────────────────────────────────────────────────────────────

    def on_tick(self, cb: Callable) -> None:
        self._on_tick_cbs.append(cb)

    def on_alert(self, cb: Callable) -> None:
        self._on_alert_cbs.append(cb)

    def on_progress(self, cb: Callable) -> None:
        self._on_progress_cbs.append(cb)

    def _fire_tick(self, payload: dict) -> None:
        for cb in self._on_tick_cbs:
            try:
                cb(payload)
            except Exception as exc:
                logger.error("on_tick cb error: %s", exc)

    def _fire_alert(self, payload: dict) -> None:
        for cb in self._on_alert_cbs:
            try:
                cb(payload)
            except Exception as exc:
                logger.error("on_alert cb error: %s", exc)

    def _fire_progress(self, msg: str) -> None:
        for cb in self._on_progress_cbs:
            try:
                cb(msg)
            except Exception as exc:
                pass

    # ─── Main Scan ────────────────────────────────────────────────────────────

    def scan(self) -> None:
        """Run one network scan cycle. Blocks until scan is complete."""
        self._tick_count += 1
        logger.info("Home WiFi scan #%d starting…", self._tick_count)

        try:
            devices = scan_network(
                do_ping_sweep=self._do_ping_sweep,
                resolve_hostnames=self._resolve_hostnames,
                resolve_vendors=self._resolve_vendors,
                progress_cb=self._fire_progress,
            )
        except Exception as exc:
            self._scan_errors += 1
            logger.error("Scan error: %s", exc)
            self._fire_alert({
                "type":    "scan_error",
                "message": f"Scan failed: {exc}",
                "device":  "",
            })
            return

        self._process_results(devices)

    # ─── Results Processing ───────────────────────────────────────────────────

    def _process_results(self, devices: list[DiscoveredDevice]) -> None:
        current_macs = {d.mac for d in devices}
        prev_macs    = set(self._known_devices.keys())

        # ── New devices ───────────────────────────────────────────────────────
        new_macs = current_macs - prev_macs
        for mac in new_macs:
            dev = next(d for d in devices if d.mac == mac)
            label = dev.hostname or mac
            self._db.insert_alert(
                "new_device",
                f"New device joined: {label} ({dev.ip}) — {dev.vendor}",
            )
            self._fire_alert({
                "type":    "new_device",
                "message": f"New device joined: {label} ({dev.ip})",
                "device":  label,
            })
            logger.info("New device: %s / %s", label, mac)

        # ── Reconnecting devices ──────────────────────────────────────────────
        returning_macs = current_macs & prev_macs
        for mac in returning_macs:
            prev = self._known_devices[mac]
            if prev.status == "offline":
                self._reconnect_counts[mac] = self._reconnect_counts.get(mac, 0) + 1
                count = self._reconnect_counts[mac]
                label = prev.hostname or mac
                if count >= 3:
                    self._db.insert_alert(
                        "suspicious",
                        f"{label} has reconnected {count} times — possible unstable client",
                    )
                    self._fire_alert({
                        "type":    "suspicious",
                        "message": f"{label} reconnected {count}× — may be unstable",
                        "device":  label,
                    })

        # ── Devices gone offline ──────────────────────────────────────────────
        gone_macs = prev_macs - current_macs
        for mac in gone_macs:
            dev = self._known_devices[mac]
            dev.status = "offline"
            self._db.upsert_device(
                dev.ip, dev.mac, dev.hostname, dev.vendor, "offline"
            )

        # ── Upsert all current devices in DB ──────────────────────────────────
        for dev in devices:
            dev.status = "online"
            dev_id = self._db.upsert_device(
                dev.ip, dev.mac, dev.hostname, dev.vendor, "online"
            )

        # ── Update known state ────────────────────────────────────────────────
        for dev in devices:
            self._known_devices[dev.mac] = dev
        for mac in gone_macs:
            pass   # keep in known with offline status

        # ── Build tick payload ────────────────────────────────────────────────
        active = [d for d in devices if d.status == "online"]
        payload = {
            "scenario":       "Home WiFi",
            "device_count":   len(active),
            "total_upload":   0.0,   # not available without router
            "total_download": 0.0,
            "devices": [
                {
                    "id":       0,
                    "ip":       d.ip,
                    "mac":      d.mac,
                    "hostname": d.hostname or d.ip,
                    "vendor":   d.vendor,
                    "upload":   0.0,
                    "download": 0.0,
                }
                for d in active
            ],
            "tick":       self._tick_count,
            "new_count":  len(new_macs),
            "gone_count": len(gone_macs),
        }
        self._fire_tick(payload)
        logger.info(
            "Scan #%d done: %d online, %d new, %d gone",
            self._tick_count, len(active), len(new_macs), len(gone_macs),
        )
