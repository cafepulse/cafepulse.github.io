# CafePulse SHA256 Verification Strategy

Dokumen ini mendefinisikan standar verifikasi integritas berkas CafePulse menggunakan hash kriptografis SHA256, format berkas `SHA256SUMS.txt`, dan menyediakan naskah Python lintas platform untuk otomatisasi pembuatannya.

---

## 1. Tujuan Verifikasi Integritas

Untuk menjamin keamanan and keandalan berkas installer/binary CafePulse yang diunduh oleh pengguna akhir, sistem verifikasi integritas wajib diimplementasikan pada setiap rilis.
- **Mencegah Kerusakan Data:** Memastikan berkas tidak rusak atau terpotong selama proses unduhan akibat gangguan koneksi internet.
- **Pencegahan Malware/Tampering:** Memberikan kepastian kepada pengguna bahwa biner yang mereka terima 100% identik dengan yang diproduksi oleh build system developer, bebas dari penyisipan malware oleh pihak ketiga (MITM attack).

---

## 2. Struktur Berkas Manifest: `SHA256SUMS.txt`

Setiap rilis CafePulse wajib menyertakan berkas teks manifest bernama `SHA256SUMS.txt` yang diunggah sebagai aset rilis. Berkas ini menggunakan format standar UNIX yang kompatibel dengan perintah `sha256sum`:

```text
[SHA256_HASH_64_CHAR]  [Nama_Berkas_1]
[SHA256_HASH_64_CHAR]  [Nama_Berkas_2]
```

### Contoh Isi Berkas:
```text
3a19b88cf46e10fb56fb063a70b746c27ad7f8425546b878601ed2c0786765a3  CafePulse_Free_Setup.exe
7b23c91af18b2c4e56eb063b70b746d27ad7f8425546b878601ed2c0786765b4  CafePulse_Free_Portable.zip
a0aa9b6a6b04e0fb56fb063a70b746c27ad7f8425546b878601ed2c0786765a3  CafePulse_Free.AppImage
8f192b0c16b23d91cf32490ab762a11b89cd12356c9a3b8e72c81d2f09ba11a2  CafePulse_Professional_Setup.exe
2a192b0c16b23d91cf32490ab762a11b89cd12356c9a3b8e72c81d2f09ba11b3  CafePulse_Professional_Portable.zip
b0bb9b6a6b04e0fb56fb063a70b746c27ad7f8425546b878601ed2c0786765c5  CafePulse_Professional.AppImage
```

*Catatan: Gunakan tepat **dua spasi** di antara nilai hash and nama berkas untuk kompatibilitas utilitas otomatis.*

---

## 3. Otomatisasi Kalkulasi Lintas Platform (Python Script)

Untuk menghindari kesalahan manusia (*human error*) and ketidakcocokan format line-endings (`LF` di Linux vs `CRLF` di Windows), kalkulasi hash distandarisasi menggunakan naskah Python. 

Naskah di bawah ini dapat diintegrasikan langsung di akhir `build.py` atau dijalankan secara mandiri:

### Kode Skrip: `generate_hashes.py`
```python
import hashlib
import os
from pathlib import Path

def calculate_sha256(file_path: Path) -> str:
    """Menghitung hash SHA256 dari sebuah file secara aman dalam bentuk chunk."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_manifest(exports_dir: Path):
    """Menghasilkan file SHA256SUMS.txt di dalam direktori ekspor."""
    manifest_path = exports_dir / "SHA256SUMS.txt"
    lines = []
    
    # Deteksi seluruh file di exports_dir (kecuali file manifest itu sendiri)
    for file_name in sorted(os.listdir(exports_dir)):
        file_path = exports_dir / file_name
        if file_path.is_file() and file_name != "SHA256SUMS.txt":
            print(f"Mengalkulasi hash untuk: {file_name}...")
            file_hash = calculate_sha256(file_path)
            # Standard format: hash + 2 spasi + nama file
            lines.append(f"{file_hash}  {file_name}\n")
            
    # Tulis manifest dengan line ending LF (\n) standar UNIX
    with open(manifest_path, "w", newline="\n", encoding="utf-8") as f:
        f.writelines(lines)
        
    print(f"\n[SUKSES] Berkas manifest berhasil dibuat di: {manifest_path}")

if __name__ == "__main__":
    # Menargetkan direktori exports di root workspace
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    EXPORTS_DIR = PROJECT_ROOT / "exports"
    
    if EXPORTS_DIR.exists():
        generate_manifest(EXPORTS_DIR)
    else:
        print(f"[ERROR] Direktori ekspor tidak ditemukan di: {EXPORTS_DIR}")
```

---

## 4. Cara Verifikasi oleh Pengguna Akhir

Pengguna dapat memverifikasi berkas yang telah mereka unduh menggunakan perintah bawaan OS masing-masing:

### 4.1 Windows (PowerShell)
Gunakan perintah `Get-FileHash` pada berkas installer:
```powershell
Get-FileHash -Algorithm SHA256 .\CafePulse_Free_Setup.exe
```
Cocokkan string output hash (huruf besar/kecil tidak berpengaruh) dengan nilai hash yang tertulis di berkas `SHA256SUMS.txt` atau catatan rilis.

### 4.2 Linux (Terminal)
Pindahkan berkas `SHA256SUMS.txt` yang diunduh ke folder yang sama dengan berkas `.AppImage`, lalu jalankan:
```bash
sha256sum -c SHA256SUMS.txt --ignore-missing
```
Jika sukses, output akan menampilkan status `OK`:
```text
CafePulse_Free.AppImage: OK
```
