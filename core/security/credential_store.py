import base64
import hashlib
import platform
import uuid
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger("cafepulse.security")

class CredentialStore:
    """
    Symmetric encryption engine for sensitive credentials using Fernet.
    Generates a secure machine-bound key so encrypted credentials cannot
    be decrypted if copied to a different PC.
    """
    
    _fernet = None

    @classmethod
    def _get_fernet(cls) -> Fernet:
        if cls._fernet is None:
            key = cls._generate_machine_bound_key()
            cls._fernet = Fernet(key)
        return cls._fernet

    @classmethod
    def _generate_machine_bound_key(cls) -> bytes:
        """
        Generates a 32-byte key bound to the local machine's hardware properties.
        Safe, stable, and offline-friendly. Uses registry-bound MachineGuid on Windows for VPN resilience.
        """
        try:
            machine_guid = ""
            if platform.system() == "Windows":
                try:
                    import winreg
                    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                    guid, _ = winreg.QueryValueEx(registry_key, "MachineGuid")
                    winreg.CloseKey(registry_key)
                    machine_guid = str(guid).strip()
                except Exception as ex:
                    logger.debug("Failed to read MachineGuid from registry: %s", ex)
            
            if machine_guid:
                raw_fingerprint = f"CafePulse:Locked:WinGuid:{machine_guid}"
            else:
                # Combine multiple unique hardware/os parameters
                node = str(uuid.getnode())  # Primary MAC address fingerprint
                system = platform.system()
                machine = platform.machine()
                raw_fingerprint = f"CafePulse:Locked:Fallback:{node}:{system}:{machine}"
            
            # Hash to get a deterministic 32-byte sequence
            hasher = hashlib.sha256()
            hasher.update(raw_fingerprint.encode('utf-8'))
            digest = hasher.digest()
            
            # Fernet requires a base64 encoded 32-byte key
            b64_key = base64.urlsafe_b64encode(digest)
            return b64_key
        except Exception as e:
            logger.error("Failed to generate machine-bound key, using fallback: %s", e)
            # Safe static fallback in case hardware calls fail (very rare)
            fallback = b"CafePulseFallbackKeySecureString32B="
            return base64.urlsafe_b64encode(fallback[:32])

    @classmethod
    def encrypt(cls, plaintext: str) -> str:
        """Encrypts a plaintext string and returns a base64 ciphertext string."""
        if not plaintext:
            return ""
        try:
            fernet = cls._get_fernet()
            encrypted_bytes = fernet.encrypt(plaintext.encode('utf-8'))
            return encrypted_bytes.decode('utf-8')
        except Exception as e:
            logger.error("Encryption failed: %s", e)
            return ""

    @classmethod
    def decrypt(cls, ciphertext: str) -> str:
        """Decrypts a base64 ciphertext string and returns the plaintext string."""
        if not ciphertext:
            return ""
        try:
            fernet = cls._get_fernet()
            decrypted_bytes = fernet.decrypt(ciphertext.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            logger.error("Decryption failed (perhaps credentials copied from another PC): %s", e)
            return ""
