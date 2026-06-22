"""
CafePulse — Dependency Registry
Modul ini bertanggung jawab untuk melacak, memverifikasi, dan mengelola dependensi
aplikasi (baik Core maupun Optional) secara terpusat untuk arsitektur desktop yang stabil.
"""

import importlib
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

logger = logging.getLogger("cafepulse.core.dependency")

@dataclass
class DependencyInfo:
    import_name: str
    pypi_name: str
    is_required: bool
    description: str
    install_command: str

class DependencyRegistry:
    """
    Registry pusat yang mencatat semua pustaka eksternal pihak ketiga
    dan memvalidasi ketersediaannya di lingkungan Python saat runtime.
    """
    
    _DEPENDENCIES: Dict[str, DependencyInfo] = {
        # --- CORE DEPENDENCIES (Wajib untuk jalannya aplikasi) ---
        "PyQt6": DependencyInfo(
            import_name="PyQt6",
            pypi_name="PyQt6",
            is_required=True,
            description="Framework utama GUI aplikasi desktop PyQt6.",
            install_command="pip install PyQt6==6.7.1"
        ),
        "pyqtgraph": DependencyInfo(
            import_name="pyqtgraph",
            pypi_name="pyqtgraph",
            is_required=True,
            description="Visualisasi grafik lalu lintas bandwidth jaringan secara real-time.",
            install_command="pip install pyqtgraph==0.13.7"
        ),
        "mac_vendor_lookup": DependencyInfo(
            import_name="mac_vendor_lookup",
            pypi_name="mac-vendor-lookup",
            is_required=True,
            description="Pencarian informasi manufaktur perangkat berdasarkan MAC Address.",
            install_command="pip install mac-vendor-lookup==0.1.12"
        ),
        "cryptography": DependencyInfo(
            import_name="cryptography",
            pypi_name="cryptography",
            is_required=True,
            description="Kriptografi tingkat lanjut untuk mengamankan data konfigurasi & kredensial.",
            install_command="pip install cryptography==43.0.1"
        ),
        "psutil": DependencyInfo(
            import_name="psutil",
            pypi_name="psutil",
            is_required=True,
            description="Mengakses informasi perangkat keras dan statistik jaringan sistem lokal.",
            install_command="pip install psutil==6.0.0"
        ),
        
        # --- OPTIONAL DEPENDENCIES (Hanya dibutuhkan oleh fitur/mode tertentu) ---
        "routeros_api": DependencyInfo(
            import_name="routeros_api",
            pypi_name="routeros-api",
            is_required=False,
            description="API resmi RouterOS MikroTik untuk interaksi & pemantauan router dari jauh.",
            install_command="pip install routeros-api==0.21.0"
        )
    }

    @classmethod
    def is_available(cls, import_name: str) -> bool:
        """
        Memeriksa apakah modul tertentu dapat diimpor dengan aman pada environment saat ini.
        Menggunakan dynamic import di dalam try-except.
        """
        try:
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False

    @classmethod
    def get_info(cls, import_name: str) -> DependencyInfo:
        """Mengambil metadata informasi dependensi berdasarkan nama import."""
        if import_name not in cls._DEPENDENCIES:
            raise KeyError(f"Dependensi '{import_name}' tidak terdaftar di registry.")
        return cls._DEPENDENCIES[import_name]

    @classmethod
    def check_all(cls) -> Tuple[List[DependencyInfo], List[DependencyInfo]]:
        """
        Melakukan audit menyeluruh terhadap semua dependensi yang terdaftar.
        Mengembalikan tuple: (missing_required_list, missing_optional_list)
        """
        missing_required = []
        missing_optional = []
        
        for name, info in cls._DEPENDENCIES.items():
            if not cls.is_available(name):
                if info.is_required:
                    logger.error(f"[AUDIT] Dependensi CORE Hilang: {info.pypi_name} ({name})")
                    missing_required.append(info)
                else:
                    logger.warning(f"[AUDIT] Dependensi OPTIONAL Hilang: {info.pypi_name} ({name})")
                    missing_optional.append(info)
            else:
                logger.debug(f"[AUDIT] Dependensi tersedia: {info.pypi_name} ✓")
                
        return missing_required, missing_optional
