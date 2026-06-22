# CafePulse Release Standardization Guide

Dokumen ini mendefinisikan standar resmi untuk struktur aset, penamaan rilis (naming convention), dan pengemasan produk CafePulse pada setiap edisi rilis.

---

## 1. Target Aset Rilis Resmi

Setiap kali kompilasi rilis selesai, sistem harus menghasilkan total **6 aset distribusi** (3 untuk Free Edition, 3 untuk Professional Edition).

### 1.1 Free Edition
Aset Free Edition ditujukan untuk pengguna gratis (pemantauan dasar, sweeps ARP offline).
- **Windows Installer:** `CafePulse_Free_Setup.exe` (Menempatkan program di Program Files, database di per-user APPDATA).
- **Windows Portable:** `CafePulse_Free_Portable.zip` (Arsip mandiri, siap dijalankan tanpa instalasi).
- **Linux AppImage:** `CafePulse_Free.AppImage` (Paket mandiri Linux x86_64, portable, siap eksekusi).

### 1.2 Professional Edition
Aset Professional Edition ditujukan untuk pengguna berlisensi Premium (MikroTik RouterOS API integration, Voucher generator, PDF exporting).
- **Windows Installer:** `CafePulse_Professional_Setup.exe`
- **Windows Portable:** `CafePulse_Professional_Portable.zip`
- **Linux AppImage:** `CafePulse_Professional.AppImage`

---

## 2. Skema Penamaan (Naming Convention)

CafePulse menggunakan **Semantic Versioning (SemVer)** dengan format rilis yang teratur sebagai berikut:

### 2.1 Stable Release
Rilis stabil adalah build publik yang telah lulus uji coba beta penuh.
- **Format Tag Git:** `v[Major].[Minor].[Patch]` (Contoh: `v1.0.0`, `v1.0.1`)
- **Format Nama Rilis GitHub:** `CafePulse [Edition] [Version]`
  - Contoh: `CafePulse Free 1.0.0`
  - Contoh: `CafePulse Professional 1.0.0`
- **Nama Berkas Aset:**
  - `CafePulse_Free_Setup.exe`
  - `CafePulse_Free_Portable.zip`
  - `CafePulse_Free.AppImage`
  - `CafePulse_Professional_Setup.exe`
  - `CafePulse_Professional_Portable.zip`
  - `CafePulse_Professional.AppImage`

### 2.2 Beta Release
Rilis beta adalah build pratinjau yang didistribusikan secara terbatas ke tester (misalnya melalui saluran Discord) untuk menguji kestabilan fitur baru.
- **Format Tag Git:** `v[Major].[Minor].[Patch]-beta.[Build]` (Contoh: `v1.0.0-beta.1`, `v1.0.0-beta.2`)
- **Format Nama Rilis GitHub:** `CafePulse [Edition] [Version] (Beta)`
  - Contoh: `CafePulse Free 1.0.0-beta.1 (Beta)`
  - Contoh: `CafePulse Professional 1.0.0-beta.1 (Beta)`
- **Nama Berkas Aset:** Sama dengan struktur aset stabil (misalnya `CafePulse_Free_Setup.exe` untuk rilis "Latest Beta"). Hal ini memudahkan naskah instalasi dan pelacakan pembaruan.

---

## 3. Penanganan Khusus: Founder Release

### 3.1 Rekomendasi Arsitektur
**Rekomendasi Utama:** *Jangan membuat berkas biner/installer ketiga khusus untuk Founder Edition.*
Menciptakan berkas terpisah seperti `CafePulse_Founder_Setup.exe` akan menimbulkan kerumitan tak perlu pada build pipeline, menambah ukuran penyimpanan repositori, dan mempersulit mekanisme pembaruan otomatis (auto-updater) di masa depan.

### 3.2 Strategi Implementasi
Sebagai gantinya, gunakan **pendekatan berbasis Lisensi Kriptografis (RSA-4096)**:
1. **Biner Tunggal:** Pengguna Founder mengunduh berkas biner standar **Professional Edition** (`CafePulse_Professional_Setup.exe` atau `.AppImage`).
2. **Parameter Lisensi:** Lisensi kriptografis yang diterbitkan oleh Founder (melalui `issue_license.py`) berisi data parameter tipe lisensi khusus:
   ```json
   {
     "tier": "Founder",
     "owner": "Nama Pembeli",
     "hwid": "PC-UUID-HASH-XXXX",
     "expiry": "perpetual"
   }
   ```
3. **Deteksi Runtime UI:** Saat booting, modul `LicensingManager` membaca parameter `"tier": "Founder"`. Aplikasi akan mengubah visual UI secara dinamis:
   - Menampilkan visual badge khusus **"Founder Edition"** pada bilah sisi (sidebar) and dialog "About".
   - Mengaktifkan tema visual warna emas/kuning elegan eksklusif untuk Founder.
   - Menyertakan nama Founder secara permanen di footer UI sebagai tanda apresiasi.

Mekanisme ini menjaga build system tetap bersih dan ringkas sementara Founder tetap menerima pengalaman eksklusif yang dipersonalisasi.
