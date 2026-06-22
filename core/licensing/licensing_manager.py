import json
import logging
from pathlib import Path
import platform
import uuid
import hashlib
from datetime import datetime
from core.security.credential_store import CredentialStore
import os
from core.app_paths import LICENSE_FILE
from core.licensing.rsa_manager import RSAManager

logger = logging.getLogger("cafepulse.licensing")

try:
    from core.licensing.secrets import SECRET_SALT
except ImportError:
    SECRET_SALT = "CafePulseDeveloperOfflineSecretSaltFallback!!!"

LICENSE_FILE_PATH = LICENSE_FILE  # Resolved to LOCALAPPDATA in packaged mode

class LicensingManager:
    """
    Manages local-first, offline-friendly license validation.
    Checks and validates machine-bound cryptographic license files.
    Calculates 5-year update entitlements and generates offline request files.
    """
    
    _is_pro = None
    _license_info = {}

    @classmethod
    def check_license(cls) -> bool:
        """
        Validates the local license file.
        Returns True if a valid Pro license exists for this machine, False otherwise.
        Note: Software remains fully functional even if update entitlement is expired.
        """
        # Cache status to avoid costly decryption/verification on every UI interaction
        if cls._is_pro is not None:
            return cls._is_pro

        if not LICENSE_FILE_PATH.exists():
            cls._is_pro = False
            cls._license_info = {}
            return False

        try:
            with open(LICENSE_FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                cls._is_pro = False
                return False

            # Check if it is the new RSA-signed format
            if content.startswith("{"):
                try:
                    data = json.loads(content)
                    if "data" in data and "signature" in data:
                        if RSAManager.verify_signature(data["data"], data["signature"]):
                            hwid = data["data"].get("hardware_id") or data["data"].get("hwid")
                            if hwid == "ANY" or hwid == cls.get_hwid():
                                lic_type = str(data["data"].get("license_type", "COMMERCIAL")).upper()

                                # Check Beta Expiry
                                is_expired_beta = False
                                if lic_type == "BETA":
                                    exp_str = data["data"].get("expiry") or data["data"].get("expires_at")
                                    if exp_str:
                                        try:
                                            if datetime.now() > datetime.fromisoformat(exp_str):
                                                is_expired_beta = True
                                        except Exception:
                                            pass

                                if is_expired_beta:
                                    logger.warning("Beta license expired. Downgrading to Free Edition.")
                                    cls._is_pro = False
                                    cls._license_info = {"license_type": "BETA_EXPIRED", "owner": data["data"].get("owner")}
                                    return False

                                cls._is_pro = True
                                # Map RSA license fields to the legacy structure expected by UI and AppState
                                cls._license_info = {
                                    "license_type": lic_type,
                                    "edition": data["data"].get("edition", "PROFESSIONAL"),
                                    "license_key": data["data"].get("license_key", "RSA-SIGNED-LICENSE"),
                                    "owner": data["data"].get("owner", "Valued Customer"),
                                    "email": data["data"].get("email", ""),
                                    "activated_at": data["data"].get("issue_date") or data["data"].get("activated_at", datetime.now().isoformat()),
                                    "expires_at": data["data"].get("expiry") or data["data"].get("expires_at"),
                                    "hwid": hwid,
                                    "device_name": data["data"].get("device_name", cls.get_device_name()),
                                    "os": data["data"].get("os", cls.get_os_info()),
                                    "machine_id": CredentialStore.encrypt("AUTHORIZED_MACHINE"),
                                    "founder_id": data["data"].get("founder_id", ""),
                                    "beta_cohort": data["data"].get("beta_cohort", ""),
                                    "notes": data["data"].get("notes", "")
                                }
                                logger.info("CafePulse Professional License (RSA Signed) Verified Successfully! Owner: %s", cls._license_info.get("owner"))
                                return True
                            else:
                                logger.warning("License file exists but Hardware ID does not match this machine.")
                                cls._is_pro = False
                                return False
                        else:
                            logger.warning("License signature verification failed (corrupted or invalid signature).")
                            cls._is_pro = False
                            return False
                except Exception as e:
                    logger.warning("RSA license validation error: %s. Falling back to legacy decryption.", e)

            # Fallback: Decrypt using our legacy machine-bound security store
            plaintext = CredentialStore.decrypt(content)
            if plaintext:
                data = json.loads(plaintext)
                if data.get("license_type") == "professional":
                    cls._is_pro = True
                    cls._license_info = data
                    logger.info("CafePulse Professional License (Legacy) Verified Successfully! Owner: %s", data.get("owner", "Valued Customer"))
                    return True

            logger.warning("License file decryption and signature verification both failed.")
            
        except Exception as e:
            logger.error("Failed to parse license file: %s", e)
            
        cls._is_pro = False
        cls._license_info = {}
        return False

    @classmethod
    def verify_serial_key(cls, owner_name: str, serial_key: str) -> bool:
        """
        Verifies a serial key offline against the owner name using a secure hashing algorithm.
        Prevents unauthorized key generation without knowing the developer's SECRET_SALT.
        """
        if not owner_name or not serial_key:
            return False
            
        try:
            # Clean up inputs (remove spaces and special characters for stability)
            clean_owner = "".join(c for c in owner_name.upper() if c.isalnum())
            if not clean_owner:
                return False
                
            active_salt = os.environ.get("CAFEPULSE_SECRET_SALT", SECRET_SALT)
            raw_string = f"CafePulse:{clean_owner}:{active_salt}"
            
            # Calculate deterministic signature
            hasher = hashlib.sha256()
            hasher.update(raw_string.encode('utf-8'))
            expected_sig = hasher.hexdigest()[:16].upper() # 16 Characters signature
            
            # Expected Key format: CP-PRO-[CLEAN_OWNER]-[SIGNATURE]
            expected_key = f"CP-PRO-{clean_owner}-{expected_sig}"
            
            # Strict verification
            return serial_key.upper().strip() == expected_key
        except Exception:
            return False

    @classmethod
    def get_license_info(cls) -> dict:
        """Returns details about the active license."""
        cls.check_license()
        return cls._license_info

    @classmethod
    def get_hwid(cls) -> str:
        """Generates a stable, deterministic, machine-bound Hardware ID. Uses Windows MachineGuid for VPN resilience."""
        try:
            machine_guid = ""
            if platform.system() == "Windows":
                try:
                    import winreg
                    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                    guid, _ = winreg.QueryValueEx(registry_key, "MachineGuid")
                    winreg.CloseKey(registry_key)
                    machine_guid = str(guid).strip()
                except Exception:
                    pass

            if machine_guid:
                raw = f"CafePulse:Locked:WinGuid:{machine_guid}"
            else:
                node = str(uuid.getnode())  # Primary MAC address fingerprint
                system = platform.system()
                machine = platform.machine()
                raw = f"CafePulse:Locked:Fallback:{node}:{system}:{machine}"

            h = hashlib.sha256(raw.encode('utf-8')).hexdigest().upper()
            return f"CP-HWID-{h[:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"
        except Exception:
            return "CP-HWID-UNKNOWN-PCID"

    @classmethod
    def get_device_name(cls) -> str:
        """Returns local PC hostname."""
        return platform.node() or "Local PC"

    @classmethod
    def get_os_info(cls) -> str:
        """Returns readable local OS name and release."""
        return f"{platform.system()} {platform.release()}"

    @classmethod
    def is_eligible_for_updates(cls) -> bool:
        """Checks if the active license has eligible update entitlement support."""
        if not cls.check_license():
            return False
        try:
            info = cls.get_license_info()
            expires_str = info.get("expires_at")
            if not expires_str:
                return False
            expires = datetime.fromisoformat(expires_str)
            return datetime.now() < expires
        except Exception:
            return False

    @classmethod
    def get_license_health(cls) -> tuple[str, str, str]:
        """Returns (status, countdown_text, next_action) for the top Health Card."""
        if not cls.check_license():
            info = cls.get_license_info()
            if info and info.get("license_type") == "BETA_EXPIRED":
                return "BETA Expired", "Downgraded to Free", "Purchase License"
            return "Not Activated", "No Active Support", "Aktivasi Diperlukan"
            
        info = cls.get_license_info()
        expires_str = info.get("expires_at")
        if not expires_str:
            return "Invalid", "No Active Support", "Aktivasi Ulang Diperlukan"
            
        try:
            expires = datetime.fromisoformat(expires_str)
            now = datetime.now()
            
            is_beta = info.get("license_type") == "BETA"
            
            if now < expires:
                delta = expires - now
                days = delta.days
                
                years = days // 365
                rem_days = days % 365
                months = rem_days // 30
                rem_days = rem_days % 30
                
                parts = []
                if years > 0:
                    parts.append(f"{years} Tahun")
                if months > 0:
                    parts.append(f"{months} Bulan")
                if rem_days > 0 or not parts:
                    parts.append(f"{rem_days} Hari")
                    
                countdown = " ".join(parts)
                
                if is_beta:
                    return "Beta Active", countdown, "Help Us Test!"
                return "Active", countdown, "No Action Required"
            else:
                if is_beta:
                    return "Beta Expired", "Beta Period Ended", "App Locked - Get Pro License"
                return "Expired Update Entitlement", "Update Support Expired", "Renew Update Support Recommended"
        except Exception:
            return "Invalid", "Error", "Aktivasi Ulang Diperlukan"

    @classmethod
    def generate_activation_request(cls, owner_name: str, email: str = "") -> str:
        """Generates base64-encoded JSON offline activation request (*.licreq)."""
        payload = {
            "request_type": "offline_activation_request",
            "owner": owner_name,
            "email": email,
            "hwid": cls.get_hwid(),
            "device_name": cls.get_device_name(),
            "os": cls.get_os_info(),
            "version": "1.0.0.0",
            "requested_at": datetime.now().isoformat()
        }
        
        import base64
        plaintext = json.dumps(payload)
        return base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')

    @classmethod
    def import_activation_file(cls, file_content: str) -> bool:
        """Imports an offline activation file (*.lic) and writes it to config/license.lic."""
        if not file_content:
            return False
        try:
            content = file_content.strip()
            
            # Try to verify as RSA signed JSON first
            if content.startswith("{"):
                try:
                    data = json.loads(content)
                    if "data" in data and "signature" in data:
                        if RSAManager.verify_signature(data["data"], data["signature"]):
                            hwid = data["data"].get("hardware_id") or data["data"].get("hwid")
                            if hwid == "ANY" or hwid == cls.get_hwid():
                                # Safe to write
                                LICENSE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
                                with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
                                    f.write(content)
                                cls._is_pro = None # Reset cache
                                logger.info("RSA License successfully imported locally for %s", data["data"].get("owner"))
                                return True
                            else:
                                logger.warning("RSA Import failed: HWID mismatch.")
                                return False
                        else:
                            logger.warning("RSA Import failed: RSA Signature verification failed.")
                            return False
                except Exception as e:
                    logger.warning("Failed to parse/import as RSA license: %s", e)
            
            # Fallback to old format
            plaintext = CredentialStore.decrypt(content)
            if not plaintext:
                logger.warning("Import failed: Decryption failed (not bound to this machine).")
                return False
                
            data = json.loads(plaintext)
            if data.get("license_type") != "professional":
                logger.warning("Import failed: License type is not professional.")
                return False
                
            # Safe to write
            LICENSE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(content)
                
            cls._is_pro = None # Reset cache
            logger.info("License successfully imported locally for %s", data.get("owner"))
            return True
        except Exception as e:
            logger.error("Failed to import license file: %s", e)
            return False

    @classmethod
    def activate_license(cls, raw_key: str, owner_name: str) -> bool:
        """
        Verifies the serial key (or RSA signed JSON/Base64) and activates the license locally by
        writing a signed or encrypted license file.
        """
        if not raw_key or not owner_name:
            return False
            
        # Check if raw_key is a JSON string representing a signed license
        # Or Base64 encoded signed license JSON
        is_rsa_license = False
        parsed_data = None
        
        try:
            parsed_data = json.loads(raw_key.strip())
            is_rsa_license = "data" in parsed_data and "signature" in parsed_data
        except Exception:
            pass
            
        if not is_rsa_license:
            try:
                import base64
                decoded = base64.b64decode(raw_key.strip()).decode('utf-8')
                parsed_data = json.loads(decoded)
                is_rsa_license = "data" in parsed_data and "signature" in parsed_data
            except Exception:
                pass
                
        if is_rsa_license:
            try:
                if RSAManager.verify_signature(parsed_data["data"], parsed_data["signature"]):
                    hwid = parsed_data["data"].get("hardware_id") or parsed_data["data"].get("hwid")
                    if hwid != cls.get_hwid():
                        logger.warning("RSA Activation failed: HWID mismatch.")
                        return False
                        
                    owner_in_lic = parsed_data["data"].get("owner", "")
                    clean_owner_lic = "".join(c for c in owner_in_lic.upper() if c.isalnum())
                    clean_owner_input = "".join(c for c in owner_name.upper() if c.isalnum())
                    if clean_owner_lic != clean_owner_input:
                        logger.warning("RSA Activation failed: Owner Name mismatch.")
                        return False
                        
                    # Write directly as JSON
                    LICENSE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
                    with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(json.dumps(parsed_data))
                    cls._is_pro = None # Reset cache
                    logger.info("License successfully activated via RSA signature for %s", owner_in_lic)
                    return True
                else:
                    logger.warning("RSA Activation failed: Invalid RSA Signature.")
                    return False
            except Exception as e:
                logger.error("RSA Activation error: %s", e)
                return False

        # Legacy activation flow: Strict offline validation using serial key signature verification
        if not cls.verify_serial_key(owner_name, raw_key):
            logger.warning("License activation failed: Invalid Serial Key or Owner Name mismatch.")
            return False
        
        try:
            now = datetime.now()
            # Gregorian penambahan 5 tahun yang kokoh
            try:
                expires = now.replace(year=now.year + 5)
            except ValueError:
                # Handle leap year Feb 29 fallback
                expires = now.replace(year=now.year + 5, day=28)
            
            payload = {
                "license_type": "professional",
                "license_key": raw_key.upper().strip(),
                "owner": owner_name,
                "activated_at": now.isoformat(),
                "expires_at": expires.isoformat(),
                "hwid": cls.get_hwid(),
                "device_name": cls.get_device_name(),
                "os": cls.get_os_info(),
                "machine_id": CredentialStore.encrypt("AUTHORIZED_MACHINE") # Safe binding marker
            }
            
            plaintext = json.dumps(payload)
            ciphertext = CredentialStore.encrypt(plaintext)
            
            LICENSE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(ciphertext)
                
            cls._is_pro = None # Reset cache
            logger.info("License successfully activated locally for %s (Legacy)", owner_name)
            return True
        except Exception as e:
            logger.error("Local activation failed: %s", e)
            return False

    @classmethod
    def deactivate(cls) -> None:
        """Removes the local license file."""
        if LICENSE_FILE_PATH.exists():
            try:
                LICENSE_FILE_PATH.unlink()
            except OSError:
                pass
        cls._is_pro = None
        cls._license_info = {}
        logger.info("License deactivated.")
