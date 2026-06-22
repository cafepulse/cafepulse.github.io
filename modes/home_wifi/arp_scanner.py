"""
CafePulse — ARP Scanner
Cross-platform network discovery via ARP table population + parsing.

Windows: ping broadcast → arp -a
Linux:   ip neigh / arp -n → ping sweep (if needed)

No packet sniffing. No monitor mode. No raw sockets.
"""

import logging
import platform
import re
import socket
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("cafepulse.homewifi.arp")

_IS_WINDOWS = platform.system() == "Windows"
_IS_LINUX   = platform.system() == "Linux"


@dataclass
class ARPEntry:
    ip:  str
    mac: str


# ─── Local Network Detection ──────────────────────────────────────────────────

def get_local_network() -> Optional[str]:
    """
    Detect the local machine's IP and derive the /24 subnet.
    Returns e.g. '192.168.1.0/24' or None on failure.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        # Assume /24 for home networks
        parts = local_ip.split(".")
        subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        return subnet
    except Exception as exc:
        logger.warning("Could not detect local network: %s", exc)
        return None


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ─── Ping Sweep ───────────────────────────────────────────────────────────────

def _ping_host(ip: str, timeout_ms: int = 300) -> bool:
    """Ping a single host. Returns True if reachable."""
    try:
        kwargs = {}
        if _IS_WINDOWS:
            cmd = ["ping", "-n", "1", "-w", str(timeout_ms), ip]
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
            **kwargs
        )
        return result.returncode == 0
    except Exception:
        return False


def ping_sweep(subnet: str, max_workers: int = 64, heartbeat_cb = None) -> list[str]:
    """
    Ping all hosts in subnet concurrently.
    Returns list of responsive IPs.
    """
    try:
        network = ipaddress.IPv4Network(subnet, strict=False)
        hosts   = [str(h) for h in network.hosts()]
    except ValueError as exc:
        logger.error("Invalid subnet '%s': %s", subnet, exc)
        return []

    logger.info("Ping sweep: %s (%d hosts)", subnet, len(hosts))
    alive: list[str] = []

    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ping") as ex:
        future_map = {ex.submit(_ping_host, ip): ip for ip in hosts}
        count = 0
        for future in as_completed(future_map):
            ip = future_map[future]
            count += 1
            if count % 10 == 0 and heartbeat_cb:
                try:
                    heartbeat_cb()
                except Exception:
                    pass
            try:
                if future.result():
                    alive.append(ip)
            except Exception:
                pass

    logger.info("Ping sweep complete: %d hosts alive", len(alive))
    return alive



# ─── ARP Table Parsing ────────────────────────────────────────────────────────

def _parse_arp_windows(output: str) -> list[ARPEntry]:
    entries: list[ARPEntry] = []
    # Windows arp -a: "  192.168.1.1       aa-bb-cc-dd-ee-ff     dynamic"
    pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+([\da-fA-F]{2}[-:][\da-fA-F]{2}[-:][\da-fA-F]{2}"
        r"[-:][\da-fA-F]{2}[-:][\da-fA-F]{2}[-:][\da-fA-F]{2})"
    )
    for match in pattern.finditer(output):
        ip  = match.group(1)
        mac = match.group(2).replace("-", ":").upper()
        if not ip.endswith(".255") and not ip.startswith("224."):
            entries.append(ARPEntry(ip=ip, mac=mac))
    return entries


def _parse_arp_linux(output: str) -> list[ARPEntry]:
    entries: list[ARPEntry] = []
    # `ip neigh` format: "192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE"
    # `arp -n`  format: "192.168.1.1  ether  aa:bb:cc:dd:ee:ff  C  eth0"
    mac_pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3}).*?([\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}"
        r":[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2})"
    )
    for line in output.splitlines():
        if "FAILED" in line or "incomplete" in line:
            continue
        match = mac_pattern.search(line)
        if match:
            ip  = match.group(1)
            mac = match.group(2).upper()
            if not ip.endswith(".255"):
                entries.append(ARPEntry(ip=ip, mac=mac))
    return entries


def read_arp_table() -> list[ARPEntry]:
    """Read the OS ARP cache and return parsed entries."""
    try:
        if _IS_WINDOWS:
            out = subprocess.check_output(
                ["arp", "-a"],
                timeout=5,
                text=True,
                errors="ignore",
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return _parse_arp_windows(out)
        else:
            # Try `ip neigh` first (more reliable on modern Linux)
            try:
                out = subprocess.check_output(
                    ["ip", "neigh"], timeout=5, text=True, errors="ignore"
                )
                entries = _parse_arp_linux(out)
                if entries:
                    return entries
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass
            # Fallback: arp -n
            out = subprocess.check_output(
                ["arp", "-n"], timeout=5, text=True, errors="ignore"
            )
            return _parse_arp_linux(out)
    except Exception as exc:
        logger.error("ARP table read failed: %s", exc)
        return []


# ─── Main Scan Function ───────────────────────────────────────────────────────

def scan_network(
    subnet: Optional[str] = None,
    do_ping_sweep: bool = True,
    ping_workers: int = 64,
    heartbeat_cb = None,
) -> list[ARPEntry]:
    """
    Full network scan:
    1. Detect subnet (if not provided)
    2. Optional ping sweep to populate ARP table
    3. Read ARP table
    Returns deduplicated list of ARPEntry filtered to target subnet.
    """
    if subnet is None:
        subnet = get_local_network()
    if subnet is None:
        logger.error("Cannot detect subnet — scan aborted")
        return []

    logger.info("Starting scan on %s", subnet)

    if heartbeat_cb:
        try:
            heartbeat_cb()
        except Exception:
            pass

    if do_ping_sweep:
        ping_sweep(subnet, max_workers=ping_workers, heartbeat_cb=heartbeat_cb)

    if heartbeat_cb:
        try:
            heartbeat_cb()
        except Exception:
            pass

    entries = read_arp_table()

    if heartbeat_cb:
        try:
            heartbeat_cb()
        except Exception:
            pass

    # Filter to target subnet only (Windows arp -a returns ALL interfaces)
    try:
        target_net = ipaddress.IPv4Network(subnet, strict=False)
    except ValueError:
        target_net = None

    local_ip = get_local_ip()

    # Deduplicate by MAC + filter
    seen_macs: set[str] = set()
    unique: list[ARPEntry] = []
    for e in entries:
        # Skip broadcast, multicast, zero, and self
        if e.mac in seen_macs:
            continue
        if e.mac in ("FF:FF:FF:FF:FF:FF", "00:00:00:00:00:00"):
            continue
        if e.mac.startswith("01:") or e.mac.startswith("33:33:"):
            continue
        if e.ip == local_ip:
            continue
        # Filter to target subnet
        if target_net:
            try:
                if ipaddress.IPv4Address(e.ip) not in target_net:
                    continue
            except ValueError:
                continue
        seen_macs.add(e.mac)
        unique.append(e)

    logger.info("Scan found %d unique devices (subnet-filtered)", len(unique))
    return unique

