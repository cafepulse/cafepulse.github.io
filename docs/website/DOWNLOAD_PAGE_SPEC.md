# CafePulse Download Page Specification

Spesifikasi desain dan teknis untuk memperbarui halaman `download.html` guna mendistribusikan berkas Windows (EXE/ZIP) dan Linux (AppImage) secara profesional.

---

## 1. Tata Letak Visual (Layout Grid)

Halaman unduhan akan menggunakan pembagian tata letak dua kolom (**2-Column Grid**):
1. **Kolom Kiri (Main Column - 2fr):**
   - **Tab Seleksi Platform:** Tombol toggle visual yang responsif untuk memilih sistem operasi: **[ Windows ]** atau **[ Linux ]**.
   - **Kartu Produk Edisi (Free vs Professional):** Kartu unduhan terpisah untuk edisi Gratis and edisi Professional dengan ukuran file, tipe berkas, and tombol unduh yang jelas.
2. **Kolom Kanan (Aside Sidebar - 1fr):**
   - **Quick Command Box:** Perintah cepat satu baris (PowerShell untuk Windows, wget untuk Linux).
   - **Version Information Panel:** Panel ringkas berisi versi terbaru, tanggal rilis, and tautan ke file integritas `SHA256SUMS.txt`.

---

## 2. Spesifikasi Teknis Aset Unduhan

Semua tautan unduhan harus merujuk ke redirect terbaru repositori publik GitHub Pages (`cafepulse/cafepulse.github.io`).

### 2.1 Edisi Windows (Tab Windows Aktif)
- **Aset 1: CafePulse Free Installer**
  - *Teks Utama:* Download Free Edition (Setup)
  - *Tipe Berkas:* Windows Installer (`.exe`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe`
- **Aset 2: CafePulse Free Portable**
  - *Teks Utama:* Download Free Edition (Portable ZIP)
  - *Tipe Berkas:* Compressed Archive (`.zip`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Portable.zip`
- **Aset 3: CafePulse Professional Installer**
  - *Teks Utama:* Download Professional Edition (Setup)
  - *Tipe Berkas:* Windows Installer (`.exe`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional_Setup.exe`
- **Aset 4: CafePulse Professional Portable**
  - *Teks Utama:* Download Professional Edition (Portable ZIP)
  - *Tipe Berkas:* Compressed Archive (`.zip`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional_Portable.zip`

### 2.2 Edisi Linux (Tab Linux Aktif)
- **Aset 1: CafePulse Free AppImage**
  - *Teks Utama:* Download Free Edition (AppImage)
  - *Tipe Berkas:* Executable Binary (`.AppImage`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage`
- **Aset 2: CafePulse Professional AppImage**
  - *Teks Utama:* Download Professional Edition (AppImage)
  - *Tipe Berkas:* Executable Binary (`.AppImage`)
  - *Tautan:* `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional.AppImage`

---

## 3. Spesifikasi Quick Command (Terminal Installers)

Menampilkan terminal commands satu klik di kolom kanan untuk kenyamanan teknisi jaringan.

### 3.1 Perintah Windows PowerShell (Quick Setup)
Tautan diubah untuk menggunakan redirect rilis otomatis:
```powershell
Invoke-WebRequest -Uri "https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe" -OutFile "CafePulse_Free_Setup.exe"; .\CafePulse_Free_Setup.exe
```

### 3.2 Perintah Linux Terminal (Quick Run)
Naskah CLI satu baris untuk mengunduh, memberi izin eksekusi, and meluncurkan AppImage Free secara langsung:
```bash
wget https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage && chmod +x CafePulse_Free.AppImage && ./CafePulse_Free.AppImage
```

---

## 4. Metadata Rilis Dinamis
Integrasikan JavaScript (`js/main.js`) untuk memuat informasi tanggal rilis and ukuran berkas secara dinamis dari GitHub API Releases endpoint, mencegah informasi usang (*stale metadata*) pada halaman HTML.
Tautan untuk berkas verifikasi integrity hash diletakkan secara terhormat:
`https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/SHA256SUMS.txt`
