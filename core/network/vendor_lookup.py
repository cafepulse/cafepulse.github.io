"""
CafePulse — MAC Vendor Lookup
Local-first cache using mac-vendor-lookup library.
Falls back gracefully if DB unavailable or MAC is unknown.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger("cafepulse.network.vendor")

_lookup_instance = None
_vendor_cache: dict[str, str] = {}   # prefix -> vendor name
_initialized   = False
_available     = False


def _get_lookup():
    """Lazy-init the MacLookup singleton."""
    global _lookup_instance, _initialized, _available
    if _initialized:
        return _lookup_instance
    _initialized = True
    try:
        from mac_vendor_lookup import MacLookup
        _lookup_instance = MacLookup()
        # Use the bundled offline DB — no internet required
        _available = True
        logger.info("MAC vendor lookup initialized (offline DB)")
    except Exception as exc:
        logger.warning("mac-vendor-lookup not available: %s", exc)
        _lookup_instance = None
        _available = False
    return _lookup_instance


def normalize_mac(mac: str) -> str:
    """Normalize MAC to uppercase colon-separated: AA:BB:CC:DD:EE:FF"""
    clean = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(clean) != 12:
        return mac.upper()
    return ":".join(clean[i:i+2].upper() for i in range(0, 12, 2))


def lookup_vendor(mac: str) -> str:
    """
    Return vendor name for a MAC address.
    Uses in-memory cache first, then mac-vendor-lookup library.
    Returns 'Unknown' if not found.
    Thread-safe for reading; first call may be slow.
    """
    mac_norm = normalize_mac(mac)
    prefix   = mac_norm[:8]  # OUI: first 3 bytes

    if prefix in _vendor_cache:
        return _vendor_cache[prefix]

    lkp = _get_lookup()
    if not lkp:
        return "Unknown"

    try:
        vendor = lkp.lookup(mac_norm)
        _vendor_cache[prefix] = vendor
        return vendor
    except Exception:
        _vendor_cache[prefix] = "Unknown"
        return "Unknown"
