import hashlib
import os
from pathlib import Path

def generate_checksums():
    export_dir = Path(__file__).resolve().parent / "exports"
    if not export_dir.exists():
        print(f"Error: Directory {export_dir} does not exist.")
        return

    checksum_file = export_dir / "SHA256SUMS.txt"
    print(f"Generating SHA-256 checksums in {export_dir}...")
    
    with open(checksum_file, "w", encoding="utf-8") as out_f:
        for root, _, files in os.walk(export_dir):
            for file in sorted(files):
                if file == "SHA256SUMS.txt":
                    continue
                file_path = Path(root) / file
                
                # Calculate SHA256
                sha256_hash = hashlib.sha256()
                with open(file_path, "rb") as f:
                    # Read and update hash string value in blocks of 4K
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                
                hash_hex = sha256_hash.hexdigest()
                out_f.write(f"{hash_hex} *{file}\n")
                print(f"  {file}: {hash_hex}")
                
    print(f"Successfully generated {checksum_file}")

if __name__ == "__main__":
    generate_checksums()
