import time
import socket
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal

from core.scanner.arp_scanner import get_local_subnet, read_arp_table, ping_sweep
from core.network.vendor_lookup import normalize_mac, lookup_vendor
from core.mikrotik.router_client import RouterClient

logger = logging.getLogger("cafepulse.core.mikrotik.discovery")

@dataclass
class RouterDiscoveryResult:
    ip_address: str
    identity: str = "Unknown Router"
    routeros_version: str = "Unknown"
    architecture: str = "Unknown"
    board_name: str = "Unknown"
    api_available: bool = False
    api_ssl_available: bool = False
    status: str = "Unknown"  # "Ready", "API Disabled", "Unreachable", "Unknown"
    response_time: float = 0.0  # in ms
    last_seen: str = ""  # ISO timestamp


class RouterDiscovery:
    """
    Core utility for discovering and querying RouterOS/MikroTik devices on the local subnet.
    Processes:
      1. Local Subnet Detection
      2. Host Discovery (ARP Cache + Active Ping Sweep)
      3. Port Scanning (8728 & 8729)
      4. MAC Vendor Matching
      5. Basic Info Extraction (Identity/Resource query via default credentials)
    """

    @staticmethod
    def check_port(ip: str, port: int, timeout: float = 0.4) -> bool:
        """Helper to quickly check if a TCP port is open."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                return True
        except Exception:
            return False

    @classmethod
    def discover_routers(cls, progress_cb=None) -> list[RouterDiscoveryResult]:
        """
        Runs synchronous discovery on the active local subnet.
        Suitable for QThread / background worker execution to prevent blocking UI.
        """
        def _log(msg: str):
            if progress_cb:
                progress_cb(msg)
            logger.info("Discovery: %s", msg)

        _log("Mendeteksi subnet lokal host...")
        subnet = get_local_subnet()
        candidate_ips: set[str] = set()

        if subnet:
            _log(f"Subnet terdeteksi: {subnet}.0/24. Menjalankan ping sweep...")
            # Include potential gateway IPs directly as priority candidates
            candidate_ips.add(f"{subnet}.1")
            candidate_ips.add(f"{subnet}.254")
            
            # Run quick ping sweep to populate ARP cache
            try:
                ping_sweep(subnet, max_threads=64)
            except Exception as e:
                logger.warning("Ping sweep error: %s", e)
        else:
            _log("Subnet lokal tidak terdeteksi. Melanjutkan via pembacaan ARP cache saja.")

        # Read ARP table to find alive hosts
        _log("Membaca tabel ARP...")
        arp_entries = []
        try:
            arp_entries = read_arp_table()
        except Exception as e:
            logger.error("Failed to read ARP table: %s", e)

        mac_vendors = {}
        for ip, mac in arp_entries:
            candidate_ips.add(ip)
            # Lookup vendor
            try:
                mac_vendors[ip] = lookup_vendor(mac)
            except Exception:
                mac_vendors[ip] = "Unknown"

        # Always verify localhost for development/sandbox environments
        candidate_ips.add("127.0.0.1")

        _log(f"Menemukan {len(candidate_ips)} IP kandidat untuk dipindai...")
        results: list[RouterDiscoveryResult] = []
        threads = []
        lock = threading.Lock()

        def _scan_host(ip: str):
            t_start = time.time()
            api_open = cls.check_port(ip, 8728, timeout=0.3)
            ssl_open = cls.check_port(ip, 8729, timeout=0.3)
            latency = (time.time() - t_start) * 1000  # in ms
            
            vendor = mac_vendors.get(ip, "Unknown")
            is_mikrotik_mac = "mikrotik" in vendor.lower()

            # A potential RouterOS device has either open API ports or is identified as MikroTik via MAC
            if not (api_open or ssl_open or is_mikrotik_mac):
                return

            res = RouterDiscoveryResult(
                ip_address=ip,
                api_available=api_open,
                api_ssl_available=ssl_open,
                response_time=round(latency, 2),
                last_seen=datetime.now().isoformat()
            )

            # If ports are closed but MAC is MikroTik, then API is Disabled
            if not (api_open or ssl_open):
                res.identity = "MikroTik Device"
                res.status = "API Disabled"
                with lock:
                    results.append(res)
                return

            # Port is open -> API Enabled. Let's try standard/default credentials.
            # standard username: admin, password: ""
            port = 8728 if api_open else 8729
            use_ssl = not api_open and ssl_open
            
            try:
                client = RouterClient(ip, "admin", "", port=port, use_ssl=use_ssl)
                client.connect()
                api = client.get_api()
                
                # Fetch System Identity
                identity_res = api.get_resource("/system/identity").get()
                if identity_res and isinstance(identity_res, list) and len(identity_res) > 0:
                    res.identity = identity_res[0].get("name", "MikroTik Router")
                else:
                    res.identity = "MikroTik Router"

                # Fetch System Resources
                resource_res = api.get_resource("/system/resource").get()
                if resource_res and isinstance(resource_res, list) and len(resource_res) > 0:
                    res.routeros_version = resource_res[0].get("version", "Unknown")
                    res.architecture = resource_res[0].get("architecture-name", "Unknown")
                    res.board_name = resource_res[0].get("board-name", "Unknown")

                client.disconnect()
                res.status = "Ready"  # Found and credentials valid!
            except Exception as e:
                err_str = str(e).lower()
                if "auth" in err_str or "login" in err_str or "credential" in err_str or "password" in err_str:
                    # Port is open but default credentials failed -> status Unknown (credentials required)
                    res.identity = "RouterOS (Credentials Required)"
                    res.status = "Unknown"
                else:
                    # Unreachable or other network failure
                    res.identity = "RouterOS Device"
                    res.status = "Unreachable"

            with lock:
                results.append(res)

        for ip in candidate_ips:
            t = threading.Thread(target=_scan_host, args=(ip,), daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join(timeout=3.0)

        _log(f"Pindaian selesai. Menemukan {len(results)} MikroTik router.")
        return sorted(results, key=lambda r: (r.status != "Ready", r.ip_address))


class RouterDiscoveryWorker(QThread):
    """
    QThread wrapper around RouterDiscovery to prevent freezing the PyQt GUI.
    """
    progress_updated = pyqtSignal(str)
    finished = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            results = RouterDiscovery.discover_routers(
                progress_cb=self.progress_updated.emit
            )
            self.finished.emit(results)
        except Exception as e:
            logger.error("Error in RouterDiscoveryWorker: %s", e)
            self.finished.emit([])


class RouterDiagnostics:
    """
    Intelligent Network Diagnostics Engine.
    Detects network blocking factors such as Client Isolation, Captive Portal,
    Subnet Mismatches, and Closed Discovery API Ports.
    """

    @classmethod
    def get_default_gateway(cls) -> str | None:
        """Determines the default gateway IP address on Windows and Linux."""
        import subprocess
        import re
        import platform
        from core.scanner.arp_scanner import get_local_subnet

        try:
            sys_platform = platform.system()
            if sys_platform == "Windows":
                output = subprocess.run(
                    ["route", "print", "0.0.0.0"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    creationflags=subprocess.CREATE_NO_WINDOW
                ).stdout
                matches = re.findall(r"0\.0\.0\.0\s+0\.0\.0\.0\s+(\d{1,3}(?:\.\d{1,3}){3})", output)
                if matches:
                    return matches[0]
            else:
                output = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=2).stdout
                matches = re.findall(r"default via (\d{1,3}(?:\.\d{1,3}){3})", output)
                if matches:
                    return matches[0]
        except Exception as e:
            logger.warning("Failed to resolve default gateway: %s", e)

        # Fallback to detected subnet base + .1
        subnet = get_local_subnet()
        if subnet:
            return f"{subnet}.1"
        return None

    @classmethod
    def check_captive_portal(cls) -> tuple[bool, str | None]:
        """Checks for HTTP interception (Captive Portal / Hotspot redirection)."""
        import urllib.request

        url = "http://clients3.google.com/generate_204"
        try:
            class RedirectHandler(urllib.request.HTTPRedirectHandler):
                def http_error_302(self, req, fp, code, msg, headers):
                    self.redirect_url = headers.get('Location')
                    return super().http_error_302(req, fp, code, msg, headers)
                http_error_301 = http_error_302
                http_error_303 = http_error_302
                http_error_307 = http_error_302

            handler = RedirectHandler()
            handler.redirect_url = None
            opener = urllib.request.build_opener(handler)
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with opener.open(req, timeout=2.0) as resp:
                status = resp.getcode()
                if handler.redirect_url:
                    return True, handler.redirect_url
                if status != 204 and status != 200:
                    return True, resp.geturl()
                if status == 200:
                    content = resp.read(100)
                    if len(content.strip()) > 0:
                        return True, resp.geturl()
            return False, None
        except Exception:
            return False, None

    @classmethod
    def run_diagnostics(cls, progress_cb=None) -> dict:
        """
        Runs synchronous network diagnostics on the local host.
        """
        def _log(msg: str):
            if progress_cb:
                progress_cb(msg)
            logger.info("Diagnostics: %s", msg)

        import time
        from core.scanner.arp_scanner import get_local_ip, read_arp_table

        _log("Menginisialisasi analisis diagnosis jaringan...")
        time.sleep(0.4)

        # 1. Gather host and gateway info
        _log("Membaca konfigurasi IP komputer dan Gateway...")
        host_ip = get_local_ip()
        gateway_ip = cls.get_default_gateway()
        time.sleep(0.3)

        # 2. Check Gateway Reachability (Ping)
        gateway_reachable = False
        if gateway_ip:
            _log(f"Menguji koneksi fisik ke Gateway ({gateway_ip})...")
            gateway_reachable = RouterDiscovery.check_port(gateway_ip, 80, timeout=0.5) or \
                                RouterDiscovery.check_port(gateway_ip, 53, timeout=0.5)
            
            # Simple ping sweep / check fallback if TCP is closed
            if not gateway_reachable:
                # Ping check
                import platform
                import subprocess
                try:
                    kwargs = {}
                    if platform.system() == "Windows":
                        cmd = ["ping", "-n", "1", "-w", "500", gateway_ip]
                        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                    else:
                        cmd = ["ping", "-c", "1", "-W", "1", gateway_ip]
                    res = subprocess.run(cmd, capture_output=True, timeout=1.5, **kwargs)
                    gateway_reachable = res.returncode == 0
                except Exception:
                    gateway_reachable = False

        # 3. Check Subnet mask & APIPA state
        _log("Menganalisis alokasi subnet host...")
        subnet_mismatch = False
        if host_ip == "127.0.0.1" or host_ip.startswith("169.254"):
            subnet_mismatch = True
        elif gateway_ip:
            host_prefix = ".".join(host_ip.split(".")[:3])
            gw_prefix = ".".join(gateway_ip.split(".")[:3])
            if host_prefix != gw_prefix:
                subnet_mismatch = True
        time.sleep(0.3)

        # 4. Check Client / AP Isolation
        _log("Memeriksa status tabel ARP (AP/Client Isolation)...")
        client_isolation = False
        arp_entries = []
        try:
            arp_entries = read_arp_table()
        except Exception:
            pass
            
        # If gateway is online but only 0-1 devices in ARP table (excluding self/localhost)
        if gateway_reachable and len(arp_entries) <= 1:
            client_isolation = True
        time.sleep(0.3)

        # 5. Check Captive Portal / Hotspot
        _log("Menguji pencegatan HTTP (Captive Portal)...")
        captive_portal, portal_url = cls.check_captive_portal()
        time.sleep(0.3)

        # 6. Check RouterOS API Ports on Gateway
        _log("Memindai status port API MikroTik di Gateway...")
        api_enabled = False
        if gateway_ip and gateway_reachable:
            api_open = RouterDiscovery.check_port(gateway_ip, 8728, timeout=0.4)
            ssl_open = RouterDiscovery.check_port(gateway_ip, 8729, timeout=0.4)
            api_enabled = api_open or ssl_open
        time.sleep(0.3)

        _log("Analisis diagnosis selesai.")
        
        # Build suggested solution text
        solution = "Jaringan terlihat normal. Hubungkan manual jika Router menggunakan IP non-standar."
        if not gateway_ip:
            solution = "Komputer Anda tidak mendapatkan gateway IP. Silakan hubungkan kabel LAN atau Wi-Fi."
        elif not gateway_reachable:
            solution = "Koneksi fisik ke Gateway terputus. Periksa kabel LAN, Wi-Fi, atau status Router."
        elif captive_portal:
            solution = "Jaringan ini memblokir akses internet (Captive Portal/Hotspot aktif). Silakan login terlebih dahulu melalui browser."
        elif client_isolation:
            solution = "Isolasi Klien/AP aktif di Wi-Fi ini, memblokir pencarian antar perangkat. Silakan gunakan Tambah Manual IP Router."
        elif subnet_mismatch:
            solution = "Komputer Anda berada di subnet yang berbeda dari Router. Atur IP komputer Anda menjadi statis di range Router."
        elif gateway_reachable and not api_enabled:
            solution = "Router ditemukan tetapi port API (8728/8729) ditutup. Buka Winbox -> System -> Services -> aktifkan 'api' atau 'api-ssl'."

        return {
            "host_ip": host_ip,
            "gateway_ip": gateway_ip or "Tidak Terdeteksi",
            "gateway_reachable": gateway_reachable,
            "captive_portal": captive_portal,
            "captive_portal_url": portal_url,
            "client_isolation": client_isolation,
            "subnet_mismatch": subnet_mismatch,
            "api_enabled": api_enabled,
            "solution": solution
        }


class RouterDiagnosticsWorker(QThread):
    """
    QThread background worker for running intelligent network diagnostics.
    """
    progress_updated = pyqtSignal(str)
    finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            report = RouterDiagnostics.run_diagnostics(
                progress_cb=self.progress_updated.emit
            )
            self.finished.emit(report)
        except Exception as e:
            logger.error("Error in RouterDiagnosticsWorker: %s", e)
            self.finished.emit({
                "host_ip": "127.0.0.1",
                "gateway_ip": "Tidak Terdeteksi",
                "gateway_reachable": False,
                "captive_portal": False,
                "client_isolation": False,
                "subnet_mismatch": False,
                "api_enabled": False,
                "solution": f"Gagal menjalankan diagnosis jaringan:\n{e}"
            })

