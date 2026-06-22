# CafePulse [Edition] v[Version]

[Tanggal Rilis: YYYY-MM-DD]

---

## 1. Overview
[Berikan deskripsi singkat tentang rilis ini. Apakah ini rilis minor, major, perbaikan bug darurat, atau rilis beta berkala? Sebutkan fokus utama perubahan dalam 2-3 kalimat.]

---

## 2. Key Changes (Daftar Perubahan Utama)

### 2.1 New Features (Fitur Baru)
- **[Nama Fitur]:** [Deskripsi singkat fitur baru dan bagaimana cara menggunakannya.]
- **[Nama Fitur]:** [Deskripsi singkat fitur baru.]

### 2.2 Improvements (Peningkatan)
- **[Modul/Komponen]:** [Deskripsi peningkatan kinerja, optimalisasi visual, atau kestabilan sistem.]
- **[Modul/Komponen]:** [Deskripsi peningkatan lainnya.]

### 2.3 Bug Fixes (Perbaikan Bug)
- **[Deskripsi Masalah]:** [Jelaskan apa yang diperbaiki dan dampaknya bagi pengguna.]
- **[Deskripsi Masalah]:** [Jelaskan perbaikan lainnya.]

---

## 3. Known Issues (Masalah yang Diketahui)
- **[Identifikasi Masalah]:** [Jelaskan kendala yang masih ada, skenario terjadinya, dan cara penanganan sementara (workaround) jika tersedia.]

---

## 4. Upgrade Notes (Panduan Pembaruan)
- **Windows Installer:** Cukup unduh berkas `CafePulse_[Edition]_Setup.exe` terbaru dan jalankan. Installer akan menimpa biner lama secara otomatis tanpa menghapus database local Anda.
- **Windows Portable:** Unduh `CafePulse_[Edition]_Portable.zip`, ekstrak ke folder baru, lalu pindahkan database Anda (`cafepulse.db`) dari folder lama ke folder baru jika Anda menggunakan database lokal kustom (abaikan jika database berada di `%LOCALAPPDATA%`).
- **Linux AppImage:** Unduh `CafePulse_[Edition].AppImage`, jalankan perintah `chmod +x` untuk memberi izin eksekusi, lalu jalankan seperti biasa.

---

## 5. File Integrity Verification (Verifikasi Integritas File)

Gunakan file `SHA256SUMS.txt` untuk mencocokkan checksum dari berkas yang diunduh.

### Checksum Hash:
```text
[Tempel isi file SHA256SUMS.txt di sini]
```

### Cara Verifikasi di Windows (PowerShell):
```powershell
Get-FileHash -Algorithm SHA256 .\CafePulse_[Edition]_Setup.exe
```

### Cara Verifikasi di Linux:
```bash
sha256sum -c SHA256SUMS.txt
```
