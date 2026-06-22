"""
CafePulse — Build Automation Script
Generates CafePulse_Free_Portable.zip and CafePulse_Professional_Portable.zip distributions.
Uses CafePulse.spec for PyInstaller configuration.
"""

import os
import sys
import shutil
import subprocess
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def clean_build_env():
    print("[1/6] Cleaning up old build artifacts...")
    for dir_name in ["build", "dist"]:
        path = PROJECT_ROOT / dir_name
        if path.exists():
            shutil.rmtree(path)
            print(f"      Removed {dir_name}/ directory.")
            
    spec_cache = PROJECT_ROOT / "CafePulse.spec"
    if spec_cache.exists():
        print("      Note: Retaining CafePulse.spec as configuration source.")
        
def inject_version_to_iss():
    print("[2/6] Injecting centralized version to Installers...")
    version_file = PROJECT_ROOT / "core" / "utils" / "version.py"
    if not version_file.exists():
        print(f"      [WARN] Version file not found at {version_file}")
        return
        
    version = "1.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
        if match:
            version = match.group(1)
            
    print(f"      Extracted version: {version}")
    
    # Update all .iss files
    iss_dir = PROJECT_ROOT / "installer"
    if not iss_dir.exists():
        return
        
    for iss_file in iss_dir.rglob("*.iss"):
        with open(iss_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = re.sub(r'#define MyAppVersion\s+".*?"', f'#define MyAppVersion "{version}"', content)
        
        with open(iss_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"      Injected version into: {iss_file.name}")

def run_pyinstaller():
    print("[3/6] Running PyInstaller via CafePulse.spec...")
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller is not installed. Please run: pip install pyinstaller")
        sys.exit(1)
    
    spec_file = PROJECT_ROOT / "CafePulse.spec"
    if not spec_file.exists():
        print(f"Error: CafePulse.spec not found at {spec_file}")
        sys.exit(1)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        str(spec_file),
    ]
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("Error: PyInstaller build failed.")
        sys.exit(result.returncode)
    print("      PyInstaller build completed successfully.")

def prepare_dist_folder(dist_name: str, is_pro: bool):
    print(f"[4/6] Preparing {dist_name}...")
    dist_dir = PROJECT_ROOT / "dist" / "CafePulse"
    target_dir = PROJECT_ROOT / "build_output" / dist_name
    
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True)
    
    # 1. Copy the executable and its dependencies
    print(f"      Copying binary files to {dist_name}...")
    shutil.copytree(dist_dir, target_dir / "CafePulse", dirs_exist_ok=True)
    
    # 2. Copy required asset and config directories
    print(f"      Copying assets...")
    shutil.copytree(PROJECT_ROOT / "assets", target_dir / "CafePulse" / "assets", dirs_exist_ok=True)
    
    # Copy clean default config (NOT the developer's personal settings.json)
    config_dest = target_dir / "CafePulse" / "config"
    config_dest.mkdir(parents=True, exist_ok=True)
    default_settings = PROJECT_ROOT / "config" / "settings_default.json"
    if default_settings.exists():
        shutil.copy(default_settings, config_dest / "settings_default.json")
    else:
        print("      [WARN] config/settings_default.json not found — skipping.")
    
    # 3. Create empty writable directories (placeholders — user data goes to LOCALAPPDATA)

    (target_dir / "CafePulse" / "logs").mkdir(exist_ok=True)
    (target_dir / "CafePulse" / "exports").mkdir(exist_ok=True)
    
    # 4. Copy License
    if (PROJECT_ROOT / "LICENSE").exists():
        shutil.copy(PROJECT_ROOT / "LICENSE", target_dir / "CafePulse" / "LICENSE")
        
    # 5. Copy respective README
    if is_pro:
        if (PROJECT_ROOT / "README_PROFESSIONAL.md").exists():
            shutil.copy(PROJECT_ROOT / "README_PROFESSIONAL.md", target_dir / "CafePulse" / "README_PROFESSIONAL.md")
    else:
        if (PROJECT_ROOT / "README_FREE.md").exists():
            shutil.copy(PROJECT_ROOT / "README_FREE.md", target_dir / "CafePulse" / "README_FREE.md")

def create_zip(dist_name: str):
    print(f"[5/6] Zipping {dist_name}...")
    source_dir = PROJECT_ROOT / "build_output" / dist_name
    export_dir = PROJECT_ROOT.parent / "exports"
    export_dir.mkdir(exist_ok=True)
    
    zip_path = export_dir / dist_name
    # make_archive appends .zip automatically
    shutil.make_archive(str(zip_path), 'zip', source_dir)
    print(f"      Created: {zip_path}.zip")

def main():
    print("=== CafePulse Build System ===")
    
    # 0. Clean and Prep
    clean_build_env()
    inject_version_to_iss()
    
    # 1. Compile
    run_pyinstaller()
    
    # 2. Prepare Free Version (portable ZIP)
    prepare_dist_folder("CafePulse_Free_Portable", is_pro=False)
    create_zip("CafePulse_Free_Portable")
    
    # 3. Prepare Professional Version (portable ZIP)
    prepare_dist_folder("CafePulse_Professional_Portable", is_pro=True)
    create_zip("CafePulse_Professional_Portable")
    
    print("[6/6] Build Complete!")
    print(f"Distribution files are located in: {PROJECT_ROOT.parent / 'exports'}")

if __name__ == "__main__":
    main()
