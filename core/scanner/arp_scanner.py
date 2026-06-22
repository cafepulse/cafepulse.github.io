"""
CafePulse — ARP Scanner (Cross-Platform)
Discovers devices on the local network using:
  Windows: arp -a  +  ping sweep via subprocess
  Linux:   arp -n  +  optional nmcli / iwconfig info

No packet sniffing, no root required for basic ARP read.
Ping sweep is threaded for speed.
"""

import logging
import platform
import re
import socket
import subprocess
import threading
from dataclasses import dataclass, field
from ipaddress import ip_network, IPv4Address
from typing import Callable

logger = logging.getLogger("cafepulse.scanner.arp")

PLATFORM = platform.system()   # "Windows" | "Linux" | "Darwin"


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class DiscoveredDevice:
    ip:       str
    mac:      str
    hostname: str = ""
    vendor:   str = ""
    status:   str = "online"


# ─── Subnet Detection ─────────────────────────────────────────────────────────

def get_local_subnet() -> str | None:
    """
    Detect the local network subnet (e.g. '192.168.1').
    Returns the base as string, or None if detection fails.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        parts = local_ip.rsplit(".", 1)
        return parts[0] if len(parts) == 2 else None
    except Exception as exc:
        logger.warning("Could not detect local subnet: %s", exc)
        return None


def get_local_ip() -> str:
    """Return the machine's LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ─── Ping Sweep ───────────────────────────────────────────────────────────────

def _ping_host(ip: str, timeout_ms: int = 300) -> None:
    """Send one ICMP ping to populate ARP cache. Fire-and-forget."""
    try:
        if PLATFORM == "Windows":
            subprocess.run(
                ["ping", "-n", "1", "-w", str(timeout_ms), ip],
                capture_output=True, timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            subprocess.run(
                ["ping", "-c", "1", "-W", "1", ip],
                capture_output=True, timeout=2,
            )
    except Exception:
        pass


def ping_sweep(subnet_base: str, max_threads: int = 64) -> None:
    """
    Ping all 254 hosts in a /24 subnet to populate ARP cache.
    subnet_base: e.g. '192.168.1'
    Runs in parallel threads (max_threads at a time).
    """
    logger.debug("Ping sweep on %s.0/24 …", subnet_base)
    semaphore = threading.Semaphore(max_threads)
    threads: list[threading.Thread] = []

    for i in range(1, 255):
        ip = f"{subnet_base}.{i}"

        def _run(addr=ip):
            with semaphore:
                _ping_host(addr)

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join(timeout=5)
    logger.debug("Ping sweep complete")


# ─── ARP Table Parsing ────────────────────────────────────────────────────────

def _run(cmd: list[str], timeout: int = 5) -> str:
    try:
        kwargs = {}
        if PLATFORM == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, **kwargs
        )
        return result.stdout
    except Exception as exc:
        logger.error("Command %s failed: %s", cmd, exc)
        return ""


def _parse_arp_windows(output: str) -> list[tuple[str, str]]:
    """
    Parse Windows `arp -a` output.
    Example line:   192.168.1.1          aa-bb-cc-dd-ee-ff     dynamic
    Returns list of (ip, mac) tuples.
    """
    results: list[tuple[str, str]] = []
    # Match IP and MAC (with - or : separator)
    pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+"
        r"([0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}"
        r"[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2})"
        r"\s+(dynamic|static)",
        re.IGNORECASE,
    )
    for match in pattern.finditer(output):
        ip  = match.group(1)
        mac = match.group(2).replace("-", ":").upper()
        results.append((ip, mac))
    return results


def _parse_arp_linux(output: str) -> list[tuple[str, str]]:
    """
    Parse Linux `arp -n` output.
    Example line: 192.168.1.1    ether   aa:bb:cc:dd:ee:ff   C   eth0
    Also handles older format without 'ether' column.
    Returns list of (ip, mac) tuples.
    """
    results: list[tuple[str, str]] = []
    pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+"
        r"\S+\s+"                               # hw type or flags
        r"([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}"
        r":[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})",
        re.IGNORECASE,
    )
    for match in pattern.finditer(output):
        ip  = match.group(1)
        mac = match.group(2).upper()
        if mac != "00:00:00:00:00:00":
            results.append((ip, mac))
    return results


def read_arp_table() -> list[tuple[str, str]]:
    """
    Read the system ARP cache and return (ip, mac) pairs.
    Cross-platform: Windows and Linux.
    """
    if PLATFORM == "Windows":
        output = _run(["arp", "-a"])
        return _parse_arp_windows(output)
    else:
        output = _run(["arp", "-n"])
        return _parse_arp_linux(output)


# ─── Hostname Resolution ──────────────────────────────────────────────────────

def resolve_hostname(ip: str, timeout: float = 0.5) -> str:
    """
    Reverse DNS lookup for an IP. Returns empty string if not resolved.
    Uses a short timeout to avoid blocking the scan thread.
    """
    old_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(timeout)
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname.split(".")[0]   # strip domain suffix
    except Exception:
        return ""
    finally:
        socket.setdefaulttimeout(old_timeout)


# ─── Full Scan ────────────────────────────────────────────────────────────────

def scan_network(
    do_ping_sweep: bool = True,
    resolve_hostnames: bool = True,
    resolve_vendors: bool = True,
    progress_cb: Callable[[str], None] | None = None,
) -> list[DiscoveredDevice]:
    """
    Full network scan:
    1. Detect subnet
    2. Optional ping sweep to populate ARP cache
    3. Read ARP table
    4. Resolve hostnames (parallel)
    5. Lookup vendors

    Returns list of DiscoveredDevice.
    """
    def _progress(msg: str) -> None:
        if progress_cb:
            progress_cb(msg)
        logger.debug("Scan: %s", msg)

    # ── 1. Detect subnet ──────────────────────────────────────────────────────
    subnet = get_local_subnet()
    if not subnet:
        logger.warning("Could not detect local subnet — ARP read only")
        _progress("No subnet detected — reading ARP cache only")
    else:
        _progress(f"Scanning subnet {subnet}.0/24 …")

    # ── 2. Ping sweep ─────────────────────────────────────────────────────────
    if do_ping_sweep and subnet:
        _progress("Running ping sweep…")
        ping_sweep(subnet)

    # ── 3. Read ARP table ─────────────────────────────────────────────────────
    _progress("Reading ARP table…")
    arp_entries = read_arp_table()
    logger.info("ARP table returned %d entries", len(arp_entries))

    if not arp_entries:
        return []

    # ── 4. Resolve hostnames (threaded) ───────────────────────────────────────
    devices: list[DiscoveredDevice] = [
        DiscoveredDevice(ip=ip, mac=mac) for ip, mac in arp_entries
    ]

    if resolve_hostnames:
        _progress("Resolving hostnames…")
        threads = []

        def _resolve(dev: DiscoveredDevice) -> None:
            dev.hostname = resolve_hostname(dev.ip)

        for dev in devices:
            t = threading.Thread(target=_resolve, args=(dev,), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join(timeout=2)

    # ── 5. Vendor lookup ─────────────────────────────────────────────────────
    if resolve_vendors:
        _progress("Looking up vendors…")
        from core.network.vendor_lookup import lookup_vendor
        for dev in devices:
            dev.vendor = lookup_vendor(dev.mac)

    _progress(f"Scan complete — {len(devices)} device(s) found")
    logger.info("Scan complete: %d devices", len(devices))
    return devices
