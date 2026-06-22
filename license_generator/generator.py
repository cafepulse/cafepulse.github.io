"""
CafePulse 1.0.0.0 — Official Developer License Generator
This tool is strictly FOR DEVELOPER AND FOUNDER USE ONLY.
Keep the SECRET_SALT strictly confidential.
"""

import hashlib
import sys

import os
import sys
from pathlib import Path

# Add project root to path so we can import core
project_root = Path(__file__).resolve().parent.parent / "Project"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from core.licensing.secrets import SECRET_SALT
except ImportError:
    SECRET_SALT = "CafePulseDeveloperOfflineSecretSaltFallback!!!"
SECRET_SALT = os.environ.get("CAFEPULSE_SECRET_SALT", SECRET_SALT)

def generate_key(owner_name: str) -> str:
    """
    Generates a cryptographically signed offline-friendly serial key.
    Bound to the owner's name using SHA-256 and the secret developer salt.
    """
    # Normalize owner name (keep alphanumeric only, convert to uppercase)
    clean_owner = "".join(c for c in owner_name.upper() if c.isalnum())
    if not clean_owner:
        raise ValueError("Nama pemilik harus mengandung setidaknya satu karakter alfanumerik!")
        
    raw_string = f"CafePulse:{clean_owner}:{SECRET_SALT}"
    
    # Hash to compute signature
    hasher = hashlib.sha256()
    hasher.update(raw_string.encode('utf-8'))
    signature = hasher.hexdigest()[:16].upper() # 16 Char deterministic signature
    
    # Format: CP-PRO-[OWNER]-[SIGNATURE]
    return f"CP-PRO-{clean_owner}-{signature}"

class RSASigner:
    """
    Handles RSA signature generation using the developer's Private Key.
    This class is developer-only and should not be bundled in client-only modules.
    """
    @classmethod
    def load_private_key(cls, pem_bytes: bytes = None):
        from cryptography.hazmat.primitives import serialization
        if not pem_bytes:
            private_key_path = project_root / "core" / "licensing" / "private_key.pem"
            if not private_key_path.exists():
                raise FileNotFoundError(f"RSA Private Key file not found at {private_key_path}")
            with open(private_key_path, "rb") as f:
                pem_bytes = f.read()

        return serialization.load_pem_private_key(
            pem_bytes,
            password=None
        )

    @classmethod
    def generate_signature(cls, data: dict, private_key_pem: bytes = None) -> str:
        import base64
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        from core.licensing.rsa_manager import RSAManager
        
        private_key = cls.load_private_key(private_key_pem)
        canonical_data = RSAManager.serialize_canonical(data)
        
        signature = private_key.sign(
            canonical_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

def generate_signed_license(owner_name: str, edition: str, license_type: str, issue_date: str, expiry_date: str, hardware_id: str, email: str = "", founder_id: str = "", beta_cohort: str = "", notes: str = "", private_key_pem: bytes = None) -> dict:
    """
    Generates an RSA-signed license dictionary using the developer's Private Key.
    """
    data = {
        "owner": owner_name,
        "email": email,
        "edition": edition,
        "license_type": license_type,
        "issue_date": issue_date,
        "expiry": expiry_date,
        "hwid": hardware_id,
        "founder_id": founder_id,
        "beta_cohort": beta_cohort,
        "notes": notes
    }
        
    signature = RSASigner.generate_signature(data, private_key_pem)
    
    return {
        "data": data,
        "signature": signature
    }

def main():
    print("====================================================")
    print("   CafePulse 1.0.0.0 — Official License Generator   ")
    print("            (FOR FOUNDER & DEVELOPER USE ONLY)       ")
    print("====================================================")
    
    if len(sys.argv) > 1:
        owner = " ".join(sys.argv[1:])
        try:
            key = generate_key(owner)
            print(f"\n[OK] Lisensi Berhasil Dibuat!")
            print(f"Pemilik:      {owner}")
            print(f"Serial Key:   {key}\n")
        except Exception as e:
            print(f"\n[ERROR] Gagal: {e}\n")
        return
        
    print("\nAlat pembuat kunci lisensi interaktif.")
    print("Masukkan nama pemilik di bawah ini.")
    
    while True:
        try:
            owner = input("\nMasukkan Nama Pembeli (atau ketik 'exit' untuk keluar): ").strip()
            if not owner:
                continue
            if owner.lower() == 'exit':
                break
                
            key = generate_key(owner)
            print(f"\n[SUKSES] Kunci Lisensi Terbit!")
            print(f"Pemilik:    {owner}")
            print(f"Serial Key: {key}")
            print("-" * 50)
        except ValueError as ve:
            print(f"[ERROR] {ve}")
        except KeyboardInterrupt:
            break
            
    print("\nLicense generator closed.")

if __name__ == "__main__":
    main()
