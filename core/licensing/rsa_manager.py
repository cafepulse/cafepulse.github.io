"""
CafePulse — RSA Cryptographic Licensing Engine (Client Verification ONLY)
Provides digital signature verification for licenses using RSA 4096-bit, SHA-256, and PSS padding.
Does NOT contain private key loading or signature generation logic.
"""

import base64
import json
import logging
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger("cafepulse.licensing.rsa")

# Relative to project root
LICENSING_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PATH = LICENSING_DIR / "public_key.pem"

# Default hardcoded Public Key for client distribution fallback
DEFAULT_PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA8icAoXaTqyvmu0K5k77V
pyYjlwtQskCy19YyCBLOh5UcoT6UtY5NnWNEnfIfuYK/+yosLkdUuBHAWuRANWR2
4eVp3iJnBszeS8ZKipugHu/lAvq3MtfiVxOd99yhEmVs0VobRiD5kV9Vtuj6oZyg
wuZRLFvO1IlaAvDxIXHCQL34GiPlsbFS4nnGvxpIZRRr1Fb4JRjNzu5okL1/+q1S
pvmMvbkO/ctv7ndzgueeUzVbEP7y5fKS8ok6KumhPN1Qt6HHxkVz97BpjDM10clR
Otw53EWCKxShRUWcfsSNZq2Uj1bnaD7ug8bKy8m3gWTkCCtfsNsDlx35hiwGsVEd
yxKxaHYP9WaIJVvy/GvzAsWn6b/YVlyDC1rYi5WYudwDinwTWeEvDrFBaZN7+lnX
+3l5PC/fn39RQwmZQj/UONRHmtY0ffdlM8cfdMR4CiOWp9RzdE9z5oh3hD54CTil
9eNHGQAms90EyUQJMJQm3M/TmPGYCCMNylyHAky6S6DOlgizxdbxzbeKGf2hsolz
d9B3OIeMICFKaM/KqfrbsKVK4z9PHWAlieLecO+peYNIZDG4gql1vqjn7JZJknkQ
KTIvOOPOZykG56oJcnUAOVJmHatuLOp4HooFwmewW2NDgyYcZ1PEXEAdlnaMEE2K
HtpzxOGV9pjWlcgVmFiA8GUCAwEAAQ==
-----END PUBLIC KEY-----"""


class RSAManager:
    """
    Handles RSA signature verification.
    Uses RSA-4096, SHA256 and PSS padding to prevent tampering.
    """

    @classmethod
    def serialize_canonical(cls, data: dict) -> bytes:
        """
        Serializes a dictionary to a canonical JSON byte string to ensure
        the signature input is identical on both signer and verifier sides.
        """
        return json.dumps(
            data,
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=True
        ).encode('utf-8')

    @classmethod
    def load_public_key(cls, pem_bytes: bytes = None) -> object:
        """
        Loads the public key from:
        1. Explicit pem_bytes argument
        2. Local public_key.pem file if present
        3. Hardcoded DEFAULT_PUBLIC_KEY_PEM fallback
        """
        if not pem_bytes:
            if PUBLIC_KEY_PATH.exists():
                try:
                    with open(PUBLIC_KEY_PATH, "rb") as f:
                        pem_bytes = f.read()
                except Exception as e:
                    logger.warning("Failed to read public_key.pem: %s", e)
            
            if not pem_bytes:
                pem_bytes = DEFAULT_PUBLIC_KEY_PEM

        return serialization.load_pem_public_key(pem_bytes)

    @classmethod
    def verify_signature(cls, data: dict, signature_b64: str, public_key_pem: bytes = None) -> bool:
        """
        Verifies the signature of the data dict using the public key.
        Returns True if signature is valid, False otherwise.
        """
        if not signature_b64:
            logger.warning("Verification failed: signature is empty.")
            return False

        try:
            public_key = cls.load_public_key(public_key_pem)
            canonical_data = cls.serialize_canonical(data)
            signature_bytes = base64.b64decode(signature_b64.strip())

            public_key.verify(
                signature_bytes,
                canonical_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            logger.warning("RSA signature verification failed: signature is invalid.")
            return False
        except Exception as e:
            logger.error("RSA verification process encountered an error: %s", e)
            return False
