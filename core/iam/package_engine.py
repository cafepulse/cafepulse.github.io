"""
CafePulse — Access Package Conversion Engine
Converts approachable layperson metrics (Mbps, Days, GB) to low-level technical parameters
(Kbps, Seconds, Bytes) and maps them to RouterOS-compatible profiles.
"""

class PackageEngine:
    @staticmethod
    def duration_to_seconds(value: int, unit: str) -> int:
        """Converts hours, days, or weeks to seconds."""
        unit = unit.lower()
        if unit == "jam" or unit == "hour" or unit == "h":
            return value * 3600
        elif unit == "hari" or unit == "day" or unit == "d":
            return value * 86400
        elif unit == "minggu" or unit == "week" or unit == "w":
            return value * 86400 * 7
        return value

    @staticmethod
    def quota_to_bytes(gb_value: float) -> int:
        """Converts gigabytes (GB) to bytes."""
        return int(gb_value * 1024 * 1024 * 1024)

    @staticmethod
    def speed_to_kbps(mbps_value: float) -> int:
        """Converts megabits per second (Mbps) to kilobits per second (Kbps)."""
        return int(mbps_value * 1024)

    @staticmethod
    def make_rate_limit_string(speed_dn_kbps: int, speed_up_kbps: int) -> str:
        """
        Creates a RouterOS rate-limit string.
        Format: rx-rate/tx-rate (upload/download on RouterOS)
        """
        return f"{speed_up_kbps}k/{speed_dn_kbps}k"
