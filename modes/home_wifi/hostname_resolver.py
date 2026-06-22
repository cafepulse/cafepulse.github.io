"""
CafePulse — Hostname Resolver
Resolves IP addresses to hostnames using socket with strict timeout.
All lookups are non-blocking relative to caller — use from a worker thread.
"""

import logging
import socket
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

logger = logging.getLogger("cafepulse.homewifi.hostname")

_executor = ThreadPoolExecutor(max_workers=16, thread_name_prefix="hostname")


def resolve(ip: str, timeout: float = 1.5) -> str:
    """
    Resolve IP → hostname. Returns '' on failure.
    Uses a thread pool so multiple IPs can be resolved concurrently.
    """
    try:
        future = _executor.submit(socket.gethostbyaddr, ip)
        result = future.result(timeout=timeout)
        hostname = result[0]
        # Strip domain suffix for cleaner display
        return hostname.split(".")[0] if hostname else ""
    except (FutureTimeout, socket.herror, socket.gaierror, OSError):
        return ""
    except Exception as exc:
        logger.debug("Hostname resolution error for %s: %s", ip, exc)
        return ""


def resolve_batch(ips: list[str], timeout: float = 1.5) -> dict[str, str]:
    """
    Resolve multiple IPs concurrently.
    Returns {ip: hostname} dict.
    """
    futures = {ip: _executor.submit(socket.gethostbyaddr, ip) for ip in ips}
    results: dict[str, str] = {}
    for ip, future in futures.items():
        try:
            r = future.result(timeout=timeout)
            results[ip] = r[0].split(".")[0] if r[0] else ""
        except Exception:
            results[ip] = ""
    return results
