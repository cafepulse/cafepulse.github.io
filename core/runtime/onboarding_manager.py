"""
CafePulse — Onboarding & Guided Tutorial Manager
Mengontrol status onboarding pertama kali (first launch) dan pelacakan
penayangan tutorial kontekstual menggunakan ConfigManager.
"""

import logging
from typing import Optional

logger = logging.getLogger("cafepulse.core.onboarding")

class OnboardingManager:
    _instance: Optional['OnboardingManager'] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_manager=None):
        # Mencegah re-inisialisasi jika instance sudah dikonfigurasi
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self._config = config_manager
        self._initialized = True
        logger.info("OnboardingManager initialized")

    def is_first_launch(self) -> bool:
        """Mengecek apakah ini pertama kalinya aplikasi dijalankan oleh user."""
        if not self._config:
            return True
        # Default True jika key 'onboarding_completed' belum ada
        return not self._config.get("onboarding", "completed", default=False)

    def mark_onboarding_completed(self) -> None:
        """Menyimpan status onboarding selesai ke dalam berkas konfigurasi."""
        if self._config:
            self._config.set("onboarding", "completed", value=True)
            logger.info("First launch onboarding marked as completed")

    def has_seen_tutorial(self, menu_id: str) -> bool:
        """Memeriksa apakah user sudah pernah melihat tutorial kontekstual untuk menu_id tertentu."""
        if not self._config:
            return False
        return self._config.get("onboarding", "tutorials_seen", menu_id, default=False)

    def mark_tutorial_seen(self, menu_id: str) -> None:
        """Menandai tutorial kontekstual menu_id tertentu sebagai sudah ditayangkan."""
        if self._config:
            self._config.set("onboarding", "tutorials_seen", menu_id, value=True)
            logger.info(f"Tutorial for menu '{menu_id}' marked as seen")

    def reset_all_tutorials(self) -> None:
        """Mereset semua status penayangan tutorial & onboarding ke kondisi awal."""
        if self._config:
            self._config.set("onboarding", "completed", value=False)
            
            # Hapus atau kosongkan registry tutorials_seen
            seen_dict = self._config.get("onboarding", "tutorials_seen", default={})
            if isinstance(seen_dict, dict):
                for k in seen_dict.keys():
                    self._config.set("onboarding", "tutorials_seen", k, value=False)
                    
            logger.info("Onboarding and guided tutorials have been reset to default state")
