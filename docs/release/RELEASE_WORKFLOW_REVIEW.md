# CafePulse Release Workflow Review

Dokumen ini berisi hasil audit terhadap sistem kompilasi (build system) Windows lokal, workflow CI/CD Linux (GitHub Actions), dan merekomendasikan standardisasi integrasi versi (version injection) serta otomatisasi pembuatan hash.

---

## 1. Audit Build System Saat Ini

Siklus kompilasi CafePulse saat ini terbagi menjadi dua alur independen:

### 1.1 Windows Build System (Lokal)
- **Komponen:** `Project/build.py` (PyInstaller) dan `Project/build_installer.bat` (Inno Setup Compiler).
- **Hasil Evaluasi:**
  - Pembersihan direktori cache (`build/`, `dist/`) berjalan dengan baik, mencegah error impor runtime `pyimod02_importers`.
  - Output berkas portable `.zip` dan setup `.exe` telah diseragamkan untuk disimpan di parent directory `exports/` secara konsisten.
  - *Kekurangan:* Tidak ada otomatisasi pembuatan manifest hash `SHA256SUMS.txt`. Developer harus mengalkulasinya secara manual.

### 1.2 Linux Build System (GitHub Actions)
- **Komponen:** `.github/workflows/build-linux.yml`.
- **Hasil Evaluasi:**
  - Berhasil menyelesaikan kegagalan headless kompilasi PyQt6/PyQtGraph menggunakan `QT_QPA_PLATFORM: offscreen` dan instalasi `libxcb-cursor0`.
  - Struktur pengemasan AppImage (`AppDir` structure, desktop file, launcher) telah tervalidasi sukses.
  - Penyelarasan direktori `exports/` di root repositori telah berjalan sukses untuk mengumpulkan `.AppImage` and `.zip` portable.
  - *Kekurangan:* URL unduhan `appimagetool` sebelumnya patah (404) karena mengarah ke repository lama. Ini telah berhasil diperbaiki ke repository mandiri terbaru.

---

## 2. Masalah Kritis: Redundansi Versi (Hardcoded Version Strings)

### 2.1 Temuan Audit Codebase
Hasil audit menunjukkan nilai versi `"1.0.0"` (atau `"1.0.0.0"`) tersebar dan ditulis secara manual (*hardcoded*) di **8 berkas berbeda**:
1. `Project/main.py` -> `app.setApplicationVersion("1.0.0")`
2. `Project/installer/free/CafePulse_Free_Setup.iss` -> `#define MyAppVersion "1.0.0"`
3. `Project/installer/professional/CafePulse_Professional_Setup.iss` -> `#define MyAppVersion "1.0.0"`
4. `Project/assets/branding/version_info.txt` -> `StringStruct(u'FileVersion', u'1.0.0.0')`
5. `Project/config/settings_default.json` -> `"version": "1.0.0"`
6. `Project/core/licensing/licensing_manager.py` -> `"version": "1.0.0.0"`
7. `Project/ui/widgets/about_page.py` -> `self.version_lbl = QLabel("Version 1.0.0 ...")`
8. `Project/ui/widgets/sidebar.py` -> `self._version_label = QLabel("v1.0.0 ...")`

### 2.2 Risiko
Menulis versi secara manual di banyak file meningkatkan risiko kelalaian rilis (misalnya, memperbarui versi di UI tetapi lupa memperbarui di installer `.iss` atau skrip lisensi), yang dapat mengakibatkan kegagalan validasi lisensi offline atau ketidaksesuaian informasi rilis.

---

## 3. Rekomendasi Solusi: Centralized Version Injection

Untuk menerapkan standarisasi rilis, diusulkan penerapan **Single Source of Truth (SSOT) untuk Versi** pada sprint berikutnya:

### 3.1 Python Runtime Injection
Buat berkas versi terpusat di `Project/core/__init__.py`:
```python
__version__ = "1.0.0-RC1.2"
```
Di semua berkas Python (`main.py`, `about_page.py`, `sidebar.py`, `licensing_manager.py`), hilangkan hardcode string dan impor secara dinamis:
```python
from core import __version__
app.setApplicationVersion(__version__)
```

### 3.2 Build Time Pre-processor Injection (Otomatisasi Skrip)
Untuk berkas non-Python (seperti `.iss` Inno Setup, `.yml` workflow, and `version_info.txt`), modifikasi `build.py` untuk bertindak sebagai pre-compiler:
1. Skrip `build.py` membaca `__version__` dari `core/__init__.py`.
2. Skrip melakukan penggantian regex (regex replace) nilai versi secara otomatis pada berkas-berkas konfigurasi installer sebelum PyInstaller / Inno Setup dijalankan:
   - Contoh regex replacement pada berkas ISS:
     ```python
     # Membaca file ISS dan mengganti baris versi secara dinamis
     content = re.sub(r'#define MyAppVersion\s+".*?"', f'#define MyAppVersion "{version}"', content)
     ```
3. Melakukan kompilasi menggunakan parameter versi yang telah ter-inject bersih.
4. Mengembalikan (*revert*) perubahan berkas konfigurasi ke keadaan semula setelah build selesai untuk menjaga kebersihan git diff.

---

## 4. Rekomendasi Otomatisasi Rilis (Release Packaging Pipeline)

Untuk memastikan rilis konsisten di masa mendatang:
1. **Otomatisasi SHA256:** Tambahkan pemanggilan skrip `generate_hashes.py` (yang dirancang di `SHA256_STRATEGY.md`) langsung ke langkah akhir `build.py` (setelah zip dibuat) dan langkah akhir build-linux workflow (sebelum artifact di-upload).
2. **Kompilasi Sekaligus:** Jalankan build Windows (lokal) dan build Linux (CI) secara pararel. Aset-aset yang diunggah ke rilis publik wajib menyertakan berkas `SHA256SUMS.txt` yang berisi hash dari semua edisi berkas.
3. **Penyelarasan Tag Git:** Jangan merilis binary tanpa membuat Git Tag terlebih dahulu. Pembuatan Git Tag secara otomatis bertindak sebagai pemicu (trigger) build release standar.
