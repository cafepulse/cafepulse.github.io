"""
CafePulse — Hotspot Detector
Identifies Android / iPhone hotspot subnets from local network interfaces.

Known hotspot subnet patterns:
  Android : 192.168.43.0/24
  iPhone  : 172.20.10.0/24
  Samsung : 192.168.0.0/24  (shared with home routers)
  Fallback: derived from local IP → /24
"""

import logging
import socket
import platform
import subprocess
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("cafepulse.hotspot.detector")

# ─── Known hotspot subnet signatures ──────────────────────────────────────────
HOTSPOT_SIGNATURES: list[tuple[str, str, str]] = [
    # (prefix,           type,     display_name)
    ("192.168.43.",  "android", "Android Hotspot"),
    ("172.20.10.",   "iphone",  "iPhone Hotspot"),
    ("192.168.49.",  "android", "Android WiFi Direct"),
    ("10.0.0.",      "generic", "Mobile Hotspot"),
    ("10.42.0.",     "linux",   "Linux Hotspot (NetworkManager)"),
    ("192.168.137.", "windows", "Windows Mobile Hotspot"),
]


@dataclass
class HotspotInfo:
    detected:     bool
    hotspot_type: str           # 'android', 'iphone', 'generic', 'unknown'
    display_name: str
    local_ip:     str
    subnet:       str           # CIDR e.g. '192.168.43.0/24'
    gateway:      str           # best-guess gateway IP


def detect_hotspot() -> HotspotInfo:
    """
    Try to detect the active hotspot connection by inspecting
    all local IP addresses and matching against known patterns.
    """
    local_ips = _get_all_local_ips()
    logger.debug("Local IPs for hotspot detection: %s", local_ips)

    for ip in local_ips:
        for prefix, h_type, display_name in HOTSPOT_SIGNATURES:
            if ip.startswith(prefix):
                parts  = ip.split(".")
                subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                # Gateway is usually .1
                gateway = f"{parts[0]}.{parts[1]}.{parts[2]}.1"
                logger.info("Hotspot detected: %s — %s (%s)", display_name, ip, subnet)
                return HotspotInfo(
                    detected=True,
                    hotspot_type=h_type,
                    display_name=display_name,
                    local_ip=ip,
                    subnet=subnet,
                    gateway=gateway,
                )

    # Fallback: use primary IP and derive /24
    primary = _get_primary_ip()
    if primary and primary != "127.0.0.1":
        parts  = primary.split(".")
        subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        gateway = f"{parts[0]}.{parts[1]}.{parts[2]}.1"
        logger.info("No known hotspot pattern — using primary IP: %s (%s)", primary, subnet)
        return HotspotInfo(
            detected=False,
            hotspot_type="unknown",
            display_name="Network (auto-detected)",
            local_ip=primary,
            subnet=subnet,
            gateway=gateway,
        )

    return HotspotInfo(
        detected=False,
        hotspot_type="unknown",
        display_name="Unknown",
        local_ip="",
        subnet="",
        gateway="",
    )


def _get_primary_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _get_all_local_ips() -> list[str]:
    """Return all non-loopback IPv4 addresses on this machine."""
    ips: list[str] = []
    try:
        hostname = socket.gethostname()
        infos = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for info in infos:
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass

    # Also try platform-specific commands for multi-NIC machines
    try:
        if platform.system() == "Windows":
            ips += _ips_windows()
        else:
            ips += _ips_linux()
    except Exception:
        pass

    # Always include primary
    primary = _get_primary_ip()
    if primary not in ips:
        ips.append(primary)

    return list(dict.fromkeys(ips))  # deduplicate, preserve order


def _ips_linux() -> list[str]:
    out = subprocess.check_output(
        ["ip", "-4", "addr", "show"], timeout=3, text=True, errors="ignore"
    )
    import re
    return re.findall(r"inet (\d{1,3}(?:\.\d{1,3}){3})/", out)


def _ips_windows() -> list[str]:
    out = subprocess.check_output(
        ["ipconfig"], timeout=3, text=True, errors="ignore",
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    import re
    return re.findall(r"IPv4 Address[.\s]+:\s*(\d{1,3}(?:\.\d{1,3}){3})", out)
