import random
import string
import logging

logger = logging.getLogger("cafepulse.voucher.helper")

# Safe characters list to prevent user confusion (removed 0, O, 1, I, l)
SAFE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def generate_random_code(length: int = 6, prefix: str = "", include_dash: bool = True) -> str:
    """
    Generates a highly readable random voucher code.
    Excludes confusing characters (0, O, 1, I, l) to ensure high operational usability.
    Format example: CAFE-AB79 or XY89ZH
    """
    try:
        # Compute how many random chars we need
        char_len = max(2, length)
        
        # Select random safe characters
        rand_part = "".join(random.choice(SAFE_CHARS) for _ in range(char_len))
        
        # Apply prefix kustom
        clean_prefix = "".join(c for c in prefix.upper() if c.isalnum())
        
        if clean_prefix:
            if include_dash:
                return f"{clean_prefix}-{rand_part}"
            return f"{clean_prefix}{rand_part}"
            
        # If no prefix, and include_dash is True, split the code in half for readability
        if include_dash and char_len >= 4:
            mid = char_len // 2
            return f"{rand_part[:mid]}-{rand_part[mid:]}"
            
        return rand_part
    except Exception as e:
        logger.error("Voucher code generation failed: %s", e)
        # Safe fallback
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
