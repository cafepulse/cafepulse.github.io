"""
CafePulse — RSA Licensing System Unit & Integration Tests
Verifies correct RSA signature verification, legacy fallback compatibility,
hardware binding, expiration grace period, signature tampering detection,
and missing/corrupt signature handling.
"""

import sys
import json
import base64
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Redirect LICENSE_FILE_PATH to a temporary test path to isolate testing
import core.licensing.licensing_manager as lm
TEST_LICENSE_PATH = PROJECT_ROOT / "tests" / "temp_test_license.lic"
lm.LICENSE_FILE_PATH = TEST_LICENSE_PATH

from core.licensing.licensing_manager import LicensingManager
from core.licensing.rsa_manager import RSAManager
from tools.license_generator.generator import RSASigner
from core.security.credential_store import CredentialStore


def run_tests():
    print("==========================================================")
    print("   CafePulse RSA Licensing Migration - Integration Tests  ")
    print("==========================================================")
    
    # Pre-test cleanup
    if TEST_LICENSE_PATH.exists():
        TEST_LICENSE_PATH.unlink()
        
    LicensingManager._is_pro = None
    LicensingManager._license_info = {}

    try:
        hwid = LicensingManager.get_hwid()
        print(f"Current HWID: {hwid}")
        
        # Determine 5-year expiry
        now = datetime.now()
        try:
            five_years_expiry = now.replace(year=now.year + 5).isoformat()
        except ValueError:
            five_years_expiry = now.replace(year=now.year + 5, day=28).isoformat()

        # ---------------------------------------------------------
        # Test Case 1: Valid RSA License File
        # ---------------------------------------------------------
        print("\nTest Case 1: Valid RSA License File Verification...")
        valid_data = {
            "owner": "Warung Cyber Berkah",
            "edition": "PROFESSIONAL",
            "expiry": five_years_expiry,
            "hardware_id": hwid,
            "license_key": "CP-PRO-WARUNGCYBER-TEST1"
        }
        
        # Generate signature
        signature = RSASigner.generate_signature(valid_data)
        license_json = {
            "data": valid_data,
            "signature": signature
        }
        
        # Write to test license file
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json, indent=2))
            
        LicensingManager._is_pro = None # Clear cache
        
        assert LicensingManager.check_license() is True, "Valid license verification failed!"
        info = LicensingManager.get_license_info()
        assert info["owner"] == "Warung Cyber Berkah", "Owner mismatch in license info!"
        assert info["license_key"] == "CP-PRO-WARUNGCYBER-TEST1", "License key mismatch!"
        assert LicensingManager.is_eligible_for_updates() is True, "Active license must be eligible for updates!"
        status, countdown, _ = LicensingManager.get_license_health()
        assert status == "Active", "Health status must be Active!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 2: Modified License Content (Tampering)
        # ---------------------------------------------------------
        print("\nTest Case 2: Modified License Content Detection...")
        tampered_data = valid_data.copy()
        tampered_data["owner"] = "Warung Cyber Hackers" # Modifying only one text field
        
        license_json_tampered = {
            "data": tampered_data,
            "signature": signature # Re-use the original signature
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_tampered, indent=2))
            
        LicensingManager._is_pro = None
        assert LicensingManager.check_license() is False, "Modified license accepted! Tampering bypass detected."
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 3: Expired Entitlement Grace Period
        # ---------------------------------------------------------
        print("\nTest Case 3: Expired Entitlement grace period check...")
        past_expiry = (datetime.now() - timedelta(days=10)).isoformat()
        expired_data = {
            "owner": "Warung Cyber Berkah",
            "edition": "PROFESSIONAL",
            "expiry": past_expiry,
            "hardware_id": hwid,
            "license_key": "CP-PRO-WARUNGCYBER-TEST1"
        }
        
        expired_signature = RSASigner.generate_signature(expired_data)
        license_json_expired = {
            "data": expired_data,
            "signature": expired_signature
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_expired, indent=2))
            
        LicensingManager._is_pro = None
        
        # Lifetime check: software remains functional even if support expired
        assert LicensingManager.check_license() is True, "Expired update entitlement must NOT deactivate Pro edition!"
        assert LicensingManager.is_eligible_for_updates() is False, "Expired update entitlement must not be eligible for updates!"
        status, countdown, _ = LicensingManager.get_license_health()
        assert status == "Expired Update Entitlement", "Expected Expired Update Entitlement health status!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 4: Wrong Hardware ID (Hardware Lock)
        # ---------------------------------------------------------
        print("\nTest Case 4: Wrong Hardware ID Detection...")
        wrong_hwid_data = valid_data.copy()
        wrong_hwid_data["hardware_id"] = "CP-HWID-WRONG-HARDWARE-ID-1234"
        
        wrong_hwid_sig = RSASigner.generate_signature(wrong_hwid_data)
        license_json_wrong_hwid = {
            "data": wrong_hwid_data,
            "signature": wrong_hwid_sig
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_wrong_hwid, indent=2))
            
        LicensingManager._is_pro = None
        assert LicensingManager.check_license() is False, "License with incorrect HWID was accepted!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 5: Corrupted Signature
        # ---------------------------------------------------------
        print("\nTest Case 5: Corrupted Signature Detection...")
        corrupt_signature = signature[:-4] + "ABCD"
        license_json_corrupt_sig = {
            "data": valid_data,
            "signature": corrupt_signature
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_corrupt_sig, indent=2))
            
        LicensingManager._is_pro = None
        assert LicensingManager.check_license() is False, "License with corrupted signature was accepted!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 6: Missing Signature
        # ---------------------------------------------------------
        print("\nTest Case 6: Missing Signature Detection...")
        license_json_missing_sig = {
            "data": valid_data
            # "signature" key is missing
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_missing_sig, indent=2))
            
        LicensingManager._is_pro = None
        assert LicensingManager.check_license() is False, "License with missing signature was accepted!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 7: Invalid Public Key (Signed with different Private Key)
        # ---------------------------------------------------------
        print("\nTest Case 7: Invalid Public Key / Rogue Key Verification...")
        # Generate another rogue key pair
        rogue_private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        rogue_private_pem = rogue_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Sign valid data with the rogue private key
        rogue_signature = RSASigner.generate_signature(valid_data, private_key_pem=rogue_private_pem)
        
        license_json_rogue = {
            "data": valid_data,
            "signature": rogue_signature
        }
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(license_json_rogue, indent=2))
            
        LicensingManager._is_pro = None
        
        # The app should verify using its default public key and reject this rogue signature
        assert LicensingManager.check_license() is False, "License signed with rogue private key was accepted!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 8: Invalid License File (Malformed JSON/Content)
        # ---------------------------------------------------------
        print("\nTest Case 8: Invalid License File (Malformed JSON) Handling...")
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write("This is a completely random text that is not JSON at all.")
            
        LicensingManager._is_pro = None
        assert LicensingManager.check_license() is False, "Malformed non-JSON file caused a crash or was accepted!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 9: Legacy Fallback Compatibility (Fernet Decryption)
        # ---------------------------------------------------------
        print("\nTest Case 9: Legacy Fallback Compatibility...")
        legacy_payload = {
            "license_type": "professional",
            "license_key": "CP-PRO-LEGACYKEY-1234",
            "owner": "John Legacy Doe",
            "activated_at": datetime.now().isoformat(),
            "expires_at": five_years_expiry,
            "hwid": hwid,
            "device_name": LicensingManager.get_device_name(),
            "os": LicensingManager.get_os_info(),
            "machine_id": CredentialStore.encrypt("AUTHORIZED_MACHINE")
        }
        
        legacy_ciphertext = CredentialStore.encrypt(json.dumps(legacy_payload))
        
        with open(TEST_LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(legacy_ciphertext)
            
        LicensingManager._is_pro = None
        
        assert LicensingManager.check_license() is True, "Legacy encrypted license decryption fallback failed!"
        info_legacy = LicensingManager.get_license_info()
        assert info_legacy["owner"] == "John Legacy Doe", "Owner mismatch in legacy license info!"
        assert info_legacy["license_key"] == "CP-PRO-LEGACYKEY-1234", "Legacy license key mismatch!"
        print("   -> LULUS [OK]")

        # ---------------------------------------------------------
        # Test Case 10: Import RSA Signed License File
        # ---------------------------------------------------------
        print("\nTest Case 10: Importing RSA Signed License File...")
        # Reset deactivation
        LicensingManager.deactivate()
        assert LicensingManager.check_license() is False
        
        # Prepare the RSA signed string
        rsa_lic_string = json.dumps(license_json, indent=2)
        
        import_success = LicensingManager.import_activation_file(rsa_lic_string)
        assert import_success is True, "Importing valid RSA signed license string failed!"
        assert LicensingManager.check_license() is True, "Imported RSA license not recognized as active!"
        print("   -> LULUS [OK]")

    finally:
        # Post-test cleanup
        if TEST_LICENSE_PATH.exists():
            TEST_LICENSE_PATH.unlink()
            
    print("\n==========================================================")
    print("   ALL RSA LICENSING INTEGRATION TESTS PASSED [100% OK]  ")
    print("==========================================================")


if __name__ == "__main__":
    run_tests()
