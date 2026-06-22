"""
CafePulse — Diagnostic Export
Utility to bundle logs, configuration, and system info into a ZIP file
to assist support and debugging.
"""

import os
import sys
import platform
import zipfile
import json
import logging
from datetime import datetime
from pathlib import Path
from core.app_paths import LOGS_DIR, CRASH_LOGS_DIR, EXPORTS_DIR, SETTINGS_FILE

logger = logging.getLogger("cafepulse.diagnostic")

def export_diagnostics(output_dir: Path | str | None = None) -> str | None:
    """
    Creates a ZIP archive containing diagnostic info.
    Returns the path to the created ZIP file, or None if failed.
    Uses resolved paths from app_paths (P0 fix — safe in packaged mode).
    """
    # P0 Fix: Use EXPORTS_DIR from app_paths if no override provided
    resolved_out = Path(output_dir) if output_dir else EXPORTS_DIR
    try:
        resolved_out.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = resolved_out / f"CafePulse_Diagnostic_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 1. Gather System Info
            sys_info = {
                "os": platform.system(),
                "os_release": platform.release(),
                "os_version": platform.version(),
                "architecture": platform.machine(),
                "python_version": sys.version,
                "timestamp": datetime.now().isoformat(),
                "app_version": "1.0.0"
            }
            zf.writestr("system_info.json", json.dumps(sys_info, indent=4))
            
            # 2. Gather Logs — P0 fix: use LOGS_DIR from app_paths
            log_dir = LOGS_DIR
            if log_dir.exists():
                for log_file in log_dir.glob("*.log"):
                    zf.write(log_file, arcname=f"logs/{log_file.name}")
                    
            # 3. Gather Crash Logs — P0 fix: use CRASH_LOGS_DIR from app_paths
            crash_dir = CRASH_LOGS_DIR
            if crash_dir.exists():
                for crash_file in crash_dir.glob("*.txt"):
                    zf.write(crash_file, arcname=f"logs/crash/{crash_file.name}")
                    
            # 4. Gather Safe Config (Redacted) — P0 fix: use SETTINGS_FILE from app_paths
            config_file = SETTINGS_FILE
            if config_file.exists():
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        config_data = json.load(f)
                        
                    # Redact sensitive fields
                    if "mikrotik" in config_data:
                        if "password" in config_data["mikrotik"]:
                            config_data["mikrotik"]["password"] = "******"
                            
                    zf.writestr("config/settings_safe.json", json.dumps(config_data, indent=4))
                except Exception as e:
                    zf.writestr("config/settings_error.txt", f"Failed to read config: {str(e)}")

        logger.info("Diagnostic package created at: %s", zip_filename)
        return str(zip_filename)
        
    except Exception as exc:
        logger.error("Failed to export diagnostics: %s", exc)
        return None
