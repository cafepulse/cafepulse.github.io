import sys
import unittest
import json
import base64
import time
from pathlib import Path
from datetime import datetime, timedelta

# Ensure Project Root is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.licensing.licensing_manager import LicensingManager
from core.licensing.rsa_manager import RSAManager
from tools.license_generator.generator import generate_signed_license, generate_key
from core.security.credential_store import CredentialStore

class TestRSALicensingWorkflow(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_hwid = LicensingManager.get_hwid()
        cls.now = datetime.now()
        cls.issue_date = cls.now.isoformat()
        
        pk_path = PROJECT_ROOT / "core" / "licensing" / "private_key.pem"
        if pk_path.exists():
            cls.private_key_pem = pk_path.read_bytes()
        else:
            cls.private_key_pem = None

    def test_01_commercial_license(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Com Test",
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=self.test_hwid,
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        res = LicensingManager.import_activation_file(lic_content)
        self.assertTrue(res, "Import failed for valid Commercial License")
        self.assertTrue(LicensingManager.check_license(), "Check failed for valid Commercial License")
        info = LicensingManager.get_license_info()
        self.assertEqual(info.get("license_type"), "COMMERCIAL")

    def test_02_founder_license(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Fnd Test",
            edition="PROFESSIONAL",
            license_type="FOUNDER",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=self.test_hwid,
            founder_id="FND-999",
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertTrue(LicensingManager.import_activation_file(lic_content))
        self.assertTrue(LicensingManager.check_license())
        info = LicensingManager.get_license_info()
        self.assertEqual(info.get("license_type"), "FOUNDER")
        self.assertEqual(info.get("founder_id"), "FND-999")

    def test_03_beta_license(self):
        expiry_dt = self.now + timedelta(days=30)
        lic = generate_signed_license(
            owner_name="Beta Test",
            edition="PROFESSIONAL",
            license_type="BETA",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id="ANY",
            beta_cohort="TEST",
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertTrue(LicensingManager.import_activation_file(lic_content))
        self.assertTrue(LicensingManager.check_license())
        info = LicensingManager.get_license_info()
        self.assertEqual(info.get("license_type"), "BETA")

    def test_04_expired_beta(self):
        expiry_dt = self.now - timedelta(days=1)
        lic = generate_signed_license(
            owner_name="Expired Beta",
            edition="PROFESSIONAL",
            license_type="BETA",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id="ANY",
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertTrue(LicensingManager.import_activation_file(lic_content))
        # Check license should return False (Downgrade to Free)
        self.assertFalse(LicensingManager.check_license())
        info = LicensingManager.get_license_info()
        self.assertEqual(info.get("license_type"), "BETA_EXPIRED")
        
        status, _, _ = LicensingManager.get_license_health()
        self.assertEqual(status, "BETA Expired")

    def test_05_tampered_founder(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Tamper Fnd",
            edition="PROFESSIONAL",
            license_type="FOUNDER",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=self.test_hwid,
            founder_id="FND-888",
            private_key_pem=self.private_key_pem
        )
        lic["data"]["owner"] = "Hacker" # Tampering payload
        lic_content = json.dumps(lic)
        self.assertFalse(LicensingManager.import_activation_file(lic_content))

    def test_06_tampered_commercial(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Tamper Com",
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=self.test_hwid,
            private_key_pem=self.private_key_pem
        )
        lic["signature"] = lic["signature"][:-2] + "AA" # Tampering signature
        lic_content = json.dumps(lic)
        self.assertFalse(LicensingManager.import_activation_file(lic_content))

    def test_07_wrong_hwid(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Wrong HWID",
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id="CP-HWID-WRONG",
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertFalse(LicensingManager.import_activation_file(lic_content))

    def test_08_valid_hwid(self):
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name="Valid HWID",
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=self.test_hwid,
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertTrue(LicensingManager.import_activation_file(lic_content))

    def test_09_licreq_workflow(self):
        req_b64 = LicensingManager.generate_activation_request("Req Owner", "req@example.com")
        req_json = base64.b64decode(req_b64).decode('utf-8')
        req_data = json.loads(req_json)
        
        self.assertEqual(req_data["owner"], "Req Owner")
        self.assertEqual(req_data["hwid"], self.test_hwid)
        self.assertIn("version", req_data)
        
        expiry_dt = self.now.replace(year=self.now.year + 5)
        lic = generate_signed_license(
            owner_name=req_data["owner"],
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=self.issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=req_data["hwid"],
            private_key_pem=self.private_key_pem
        )
        lic_content = json.dumps(lic)
        self.assertTrue(LicensingManager.import_activation_file(lic_content))

    def test_10_legacy_compatibility(self):
        key = generate_key("Legacy Tester")
        from core.security.credential_store import CredentialStore
        
        # Simulating saving legacy license format
        legacy_data = {
            "license_type": "professional",
            "owner": "Legacy Tester",
            "license_key": key
        }
        enc_payload = CredentialStore.encrypt(json.dumps(legacy_data))
        
        self.assertTrue(LicensingManager.import_activation_file(enc_payload))
        self.assertTrue(LicensingManager.check_license())
        info = LicensingManager.get_license_info()
        self.assertEqual(info.get("license_type"), "professional")

if __name__ == "__main__":
    unittest.main()
