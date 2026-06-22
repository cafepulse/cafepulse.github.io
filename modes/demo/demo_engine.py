"""
CafePulse — Demo Engine
Generates realistic fake network data for 5 scenarios.
All data is written to SQLite so the full DB layer is exercised.
"""

import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

logger = logging.getLogger("cafepulse.demo.engine")


# ─── Scenario Definitions ─────────────────────────────────────────────────────

@dataclass
class DemoScenario:
    name:           str
    display_name:   str
    device_count:   tuple[int, int]          # (min, max) active devices
    upload_range:   tuple[float, float]      # Mbps per device
    download_range: tuple[float, float]
    alert_chance:   float                    # 0.0 – 1.0 per tick
    reconnect_chance: float


SCENARIOS: dict[str, DemoScenario] = {
    "home_network": DemoScenario(
        name="home_network",
        display_name="Home Network",
        device_count=(3, 8),
        upload_range=(0.1, 2.0),
        download_range=(0.5, 15.0),
        alert_chance=0.03,
        reconnect_chance=0.02,
    ),
    "small_cafe": DemoScenario(
        name="small_cafe",
        display_name="Small Café",
        device_count=(10, 20),
        upload_range=(0.1, 1.5),
        download_range=(0.5, 8.0),
        alert_chance=0.08,
        reconnect_chance=0.05,
    ),
    "gaming_night": DemoScenario(
        name="gaming_night",
        display_name="Gaming Night",
        device_count=(5, 12),
        upload_range=(1.0, 8.0),
        download_range=(5.0, 40.0),
        alert_chance=0.12,
        reconnect_chance=0.04,
    ),
    "coworking_space": DemoScenario(
        name="coworking_space",
        display_name="Coworking Space",
        device_count=(15, 30),
        upload_range=(0.3, 4.0),
        download_range=(1.0, 20.0),
        alert_chance=0.06,
        reconnect_chance=0.03,
    ),
    "busy_event": DemoScenario(
        name="busy_event",
        display_name="Busy Event",
        device_count=(30, 50),
        upload_range=(0.1, 3.0),
        download_range=(0.5, 10.0),
        alert_chance=0.20,
        reconnect_chance=0.10,
    ),
}


# ─── Fake Data Pools ──────────────────────────────────────────────────────────

FAKE_HOSTNAMES = [
    "iPhone-Alex", "Galaxy-S24-Maria", "MacBook-Pro-James",
    "DESKTOP-WIN11", "iPad-Kitchen", "Android-Reza",
    "Laptop-Budi", "iPhone-Sari", "SmartTV-LG", "PS5-Living",
    "Xbox-Room2", "Echo-Dot", "Ring-Camera", "HP-Printer",
    "Surface-Pro", "Pixel-7-Ana", "ThinkPad-HR", "iMac-Design",
    "NAS-Home", "RaspberryPi-4", "Chromecast-TV", "Roku-Ultra",
    "OnePlus-Nord", "Xiaomi-Pad", "Asus-ZenBook", "Dell-XPS",
    "Nintendo-Switch", "AppleTV-4K", "Nest-Hub", "Kindle-Fire",
]

FAKE_VENDORS = [
    "Apple Inc.", "Samsung Electronics", "Dell Inc.", "Lenovo Group",
    "HP Inc.", "Asus Tek", "Microsoft Corp.", "Google LLC",
    "Xiaomi Communications", "OnePlus Technology", "Sony Interactive",
    "LG Electronics", "Amazon Technologies", "Raspberry Pi Foundation",
    "TP-Link Technologies", "Intel Corporate", "ASRock Incorporated",
]

ALERT_MESSAGES = [
    ("reconnect", "Device reconnected {count} times in the last 5 minutes: {host}"),
    ("bandwidth", "High bandwidth usage detected: {host} is using {dl:.1f} Mbps"),
    ("new_device", "New unknown device joined the network: {mac}"),
    ("congestion", "Network congestion detected — {count} devices active simultaneously"),
    ("suspicious", "Unusual activity pattern detected from {host}"),
]


def _random_mac() -> str:
    return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))


def _random_ip(base: str = "192.168.1") -> str:
    return f"{base}.{random.randint(2, 254)}"


# ─── Demo Engine ──────────────────────────────────────────────────────────────

@dataclass
class DeviceState:
    device_id:   int
    ip:          str
    mac:         str
    hostname:    str
    vendor:      str
    upload:      float = 0.0
    download:    float = 0.0
    reconnects:  int   = 0


class DemoEngine:
    """
    Stateful fake-data generator.
    Call tick() periodically; it updates DB and calls registered callbacks.
    """

    def __init__(self, db, scenario_name: str = "small_cafe"):
        self._db = db
        self._scenario: DemoScenario = SCENARIOS.get(scenario_name, SCENARIOS["small_cafe"])
        self._devices: list[DeviceState] = []
        self._tick_count: int = 0

        # Aggregated totals for the chart
        self._total_upload:   float = 0.0
        self._total_download: float = 0.0

        # Callbacks: registered by UI layer
        self._on_tick_cbs:  list[Callable] = []
        self._on_alert_cbs: list[Callable] = []

        self._seed_devices()
        logger.info("DemoEngine initialized — scenario: %s", self._scenario.display_name)

    # ─── Setup ────────────────────────────────────────────────────────────────

    def _seed_devices(self) -> None:
        """Pre-populate the device pool for this scenario."""
        count = random.randint(*self._scenario.device_count)
        used_ips: set[str] = set()
        used_macs: set[str] = set()

        for i in range(count):
            while True:
                ip = _random_ip()
                if ip not in used_ips:
                    used_ips.add(ip)
                    break
            while True:
                mac = _random_mac()
                if mac not in used_macs:
                    used_macs.add(mac)
                    break

            hostname = random.choice(FAKE_HOSTNAMES)
            vendor   = random.choice(FAKE_VENDORS)

            dev_id = self._db.upsert_device(ip, mac, hostname, vendor, "online")
            self._devices.append(DeviceState(
                device_id=dev_id, ip=ip, mac=mac,
                hostname=hostname, vendor=vendor,
            ))

        logger.debug("DemoEngine seeded %d devices", len(self._devices))

    def change_scenario(self, scenario_name: str) -> None:
        """Switch to a different demo scenario and re-seed."""
        if scenario_name not in SCENARIOS:
            logger.warning("Unknown scenario: %s", scenario_name)
            return
        self._scenario = SCENARIOS[scenario_name]
        self._devices.clear()
        self._tick_count = 0
        self._seed_devices()
        logger.info("DemoEngine switched to scenario: %s", scenario_name)

    # ─── Callbacks ────────────────────────────────────────────────────────────

    def on_tick(self, cb: Callable) -> None:
        self._on_tick_cbs.append(cb)

    def on_alert(self, cb: Callable) -> None:
        self._on_alert_cbs.append(cb)

    def _fire_tick(self, payload: dict) -> None:
        for cb in self._on_tick_cbs:
            try:
                cb(payload)
            except Exception as exc:
                logger.error("on_tick callback error: %s", exc)

    def _fire_alert(self, payload: dict) -> None:
        for cb in self._on_alert_cbs:
            try:
                cb(payload)
            except Exception as exc:
                logger.error("on_alert callback error: %s", exc)

    # ─── Tick ─────────────────────────────────────────────────────────────────

    def tick(self) -> None:
        """
        Advance simulation by one step.
        Updates all device speeds, writes traffic to DB, may generate alerts.
        """
        self._tick_count += 1
        s = self._scenario
        total_up   = 0.0
        total_down = 0.0

        # ── Randomly toggle some devices online/offline ───────────────────────
        for dev in self._devices:
            if random.random() < s.reconnect_chance:
                dev.reconnects += 1
                self._db.upsert_device(dev.ip, dev.mac, dev.hostname, dev.vendor, "offline")
                time.sleep(0.01)
                self._db.upsert_device(dev.ip, dev.mac, dev.hostname, dev.vendor, "online")

        # ── Update speeds for active devices ─────────────────────────────────
        active_devices = []
        for dev in self._devices:
            # Smooth random walk for realistic feel
            noise_up   = random.uniform(-0.3, 0.5)
            noise_down = random.uniform(-0.5, 1.5)
            dev.upload   = max(0.0, min(
                random.uniform(*s.upload_range) + noise_up,
                s.upload_range[1] * 1.5,
            ))
            dev.download = max(0.0, min(
                random.uniform(*s.download_range) + noise_down,
                s.download_range[1] * 1.5,
            ))

            # Write to DB
            self._db.insert_traffic(dev.device_id, dev.upload, dev.download)

            total_up   += dev.upload
            total_down += dev.download
            active_devices.append(dev)

        self._total_upload   = total_up
        self._total_download = total_down

        # ── Maybe generate an alert ───────────────────────────────────────────
        if random.random() < s.alert_chance:
            self._generate_alert(active_devices)

        # ── Fire tick payload ─────────────────────────────────────────────────
        payload = {
            "scenario":       s.display_name,
            "device_count":   len(self._devices),
            "total_upload":   round(total_up, 2),
            "total_download": round(total_down, 2),
            "devices":        [
                {
                    "id":       d.device_id,
                    "ip":       d.ip,
                    "mac":      d.mac,
                    "hostname": d.hostname,
                    "vendor":   d.vendor,
                    "upload":   round(d.upload, 2),
                    "download": round(d.download, 2),
                }
                for d in active_devices
            ],
            "tick": self._tick_count,
        }
        self._fire_tick(payload)

    # ─── Alert Generation ─────────────────────────────────────────────────────

    def _generate_alert(self, devices: list[DeviceState]) -> None:
        if not devices:
            return

        alert_type, template = random.choice(ALERT_MESSAGES)
        dev = random.choice(devices)

        message = template.format(
            host=dev.hostname,
            mac=dev.mac,
            dl=dev.download,
            count=random.randint(3, 12),
        )

        self._db.insert_alert(alert_type, message, dev.device_id)
        self._fire_alert({"type": alert_type, "message": message, "device": dev.hostname})
        logger.debug("Alert generated: [%s] %s", alert_type, message)

    # ─── Accessors ────────────────────────────────────────────────────────────

    @property
    def scenario(self) -> DemoScenario:
        return self._scenario

    @property
    def scenario_names(self) -> list[str]:
        return list(SCENARIOS.keys())

    @staticmethod
    def get_display_names() -> dict[str, str]:
        return {k: v.display_name for k, v in SCENARIOS.items()}
