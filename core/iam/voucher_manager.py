"""
CafePulse — Voucher Manager Subsystem
Handles token generation algorithms, dynamic mapping, and background provisioning
to both SQLite and MikroTik RouterOS.
"""

import random
import string
import logging

logger = logging.getLogger("cafepulse.iam.vouchers")


class VoucherManager:
    @staticmethod
    def generate_random_code(length: int = 6, prefix: str = "", numeric_only: bool = False) -> str:
        """
        Generates a secure, readable random access code.
        """
        chars = string.digits if numeric_only else (string.ascii_lowercase + string.digits)
        # Exclude hard-to-read characters (o, 0, i, l, 1) for better usability
        readable_chars = "".join(c for c in chars if c not in "o0il1")
        
        code = "".join(random.choice(readable_chars) for _ in range(length))
        if prefix:
            return f"{prefix}{code}"
        return code

    @staticmethod
    def provision_vouchers(db, api, package_id: str, count: int, length: int = 6, prefix: str = "", numeric_only: bool = False) -> list[str]:
        """
        Generates N vouchers, inserts them into local SQLite, and provisions
        them dynamically to MikroTik Hotspot users if api is active.
        """
        # Fetch package details
        pkg = db.fetchone("SELECT * FROM access_packages WHERE id=?", (package_id,))
        if not pkg:
            raise ValueError(f"Package ID '{package_id}' tidak ditemukan.")

        profile_name = pkg["id"] # We map package ID to RouterOS hotspot profile name
        uptime_limit = f"{pkg['duration_seconds']}s" if pkg["duration_seconds"] > 0 else None
        
        generated_codes = []
        
        for _ in range(count):
            # Generate unique code
            code = None
            for _ in range(10): # retry limit
                test_code = VoucherManager.generate_random_code(length, prefix, numeric_only)
                existing = db.fetchone("SELECT id FROM vouchers WHERE code=?", (test_code,))
                if not existing:
                    code = test_code
                    break
            
            if not code:
                # Fallback to longer random if collision limit reached
                code = VoucherManager.generate_random_code(length + 2, prefix, numeric_only)

            # Insert into SQLite locally
            db.add_voucher(code, package_id)
            generated_codes.append(code)

            # If MikroTik API is connected, push it dynamically to RouterOS
            if api:
                try:
                    # Maps voucher directly to Hotspot user
                    api.get_resource('/ip/hotspot/user').add(
                        name=code,
                        password=code, # Same username and password for simple voucher login
                        profile=profile_name,
                        limit_uptime=uptime_limit,
                        comment=f"CafePulse IAM - Package: {pkg['name']}"
                    )
                except Exception as e:
                    logger.error(f"Failed to provision voucher '{code}' to RouterOS: {e}")
                    
        logger.info(f"Successfully generated and provisioned {len(generated_codes)} vouchers for package {pkg['name']}.")
        return generated_codes
