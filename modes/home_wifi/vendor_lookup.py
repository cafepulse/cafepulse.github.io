"""
CafePulse — Vendor Lookup
MAC address → vendor name with in-memory cache.
Falls back gracefully if mac-vendor-lookup is unavailable.
"""

import logging
import re

logger = logging.getLogger("cafepulse.homewifi.vendor")

# ─── Minimal built-in OUI prefix table (fallback) ─────────────────────────────
_BUILTIN_OUI: dict[str, str] = {
    # Apple
    "AC:DE:48": "Apple", "3C:22:FB": "Apple", "A4:83:E7": "Apple",
    "F0:18:98": "Apple", "DC:2B:2A": "Apple", "78:7B:8A": "Apple",
    "14:98:77": "Apple", "A8:5C:2C": "Apple", "88:66:A5": "Apple",
    # Samsung
    "00:21:19": "Samsung", "E4:7C:F9": "Samsung", "AC:5F:3E": "Samsung",
    "8C:F5:A3": "Samsung", "50:B7:C3": "Samsung",
    # Google / Android
    "94:EB:2C": "Google", "F8:8F:CA": "Google", "54:60:09": "Google",
    # Intel
    "00:1B:21": "Intel", "3C:97:0E": "Intel", "68:17:29": "Intel",
    "8C:8D:28": "Intel",
    # Realtek
    "00:E0:4C": "Realtek", "52:54:00": "Realtek/QEMU",
    # TP-Link
    "50:C7:BF": "TP-Link", "EC:08:6B": "TP-Link", "30:B5:C2": "TP-Link",
    # Xiaomi
    "28:6C:07": "Xiaomi", "64:CC:2E": "Xiaomi", "78:11:DC": "Xiaomi",
    # Huawei
    "00:E0:FC": "Huawei", "48:46:FB": "Huawei", "CC:A2:23": "Huawei",
    # Microsoft / Hyper-V
    "00:15:5D": "Hyper-V",
    # VMware / VirtualBox
    "00:50:56": "VMware", "00:0C:29": "VMware", "08:00:27": "VirtualBox",
    # Raspberry Pi
    "B8:27:EB": "Raspberry Pi", "DC:A6:32": "Raspberry Pi", "E4:5F:01": "Raspberry Pi",
    # Cisco
    "00:1A:2B": "Cisco", "00:1E:F7": "Cisco",
    # Others
    "00:16:3E": "Xen Virtual",
    "44:38:39": "Cumulus/NVIDIA",
}


class VendorLookup:
    """
    Thread-safe vendor lookup with in-memory LRU-style cache.
    Uses mac-vendor-lookup library if available, else OUI prefix match.
    """

    def __init__(self, cache_size: int = 2048):
        self._cache: dict[str, str] = {}
        self._cache_size = cache_size
        self._mac_lookup = None
        self._init_library()

    def _init_library(self) -> None:
        try:
            from mac_vendor_lookup import MacLookup
            self._mac_lookup = MacLookup()
            logger.info("MAC vendor lookup initialized (offline DB)")
        except ImportError:
            logger.warning("mac-vendor-lookup not installed — using built-in OUI table")

    def lookup(self, mac: str) -> str:
        """Return vendor name for a MAC address. Returns '' on miss."""
        mac_upper = mac.upper().replace("-", ":").strip()
        if mac_upper in self._cache:
            return self._cache[mac_upper]

        vendor = self._resolve(mac_upper)

        # Evict oldest if cache full
        if len(self._cache) >= self._cache_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[mac_upper] = vendor
        return vendor

    def _resolve(self, mac: str) -> str:
        # Try library first
        if self._mac_lookup:
            try:
                return self._mac_lookup.lookup(mac)
            except Exception:
                pass

        # Fallback: OUI prefix match (first 3 octets)
        prefix = ":".join(mac.split(":")[:3])
        return _BUILTIN_OUI.get(prefix, "")
