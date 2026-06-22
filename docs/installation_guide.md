# CafePulse Installation Guide (Panduan Instalasi)

Panduan lengkap langkah demi langkah untuk menginstal dan menjalankan CafePulse di sistem operasi Windows dan Linux.

---

## 1. Panduan Instalasi Windows

CafePulse mendukung Windows 10 dan Windows 11 (arsitektur 64-bit).

### 1.1 Menggunakan Windows Installer (`.exe`)
Ini adalah metode instalasi standar yang direkomendasikan untuk sebagian besar pengguna.
1. Unduh berkas **`CafePulse_Free_Setup.exe`** atau **`CafePulse_Professional_Setup.exe`** dari halaman unduhan.
2. Klik ganda berkas setup yang diunduh.
3. Jika muncul jendela peringatan **Windows Defender SmartScreen** ("Windows protected your PC"):
   - Klik teks tautan **"More info"** di bagian atas teks peringatan.
   - Klik tombol **"Run anyway"** yang muncul di bagian bawah.
   *(Peringatan ini muncul karena biner belum ditandatangani sertifikat Microsoft Authenticode berbayar).*
4. Ikuti instruksi installer: setujui Perjanjian Lisensi (EULA) and pilih folder instalasi (default di `C:\Program Files\CafePulse`).
5. Centang kotak "Create a desktop shortcut" untuk memudahkan peluncuran.
6. Klik **Finish**. Aplikasi siap diluncurkan dari Desktop atau menu Start.

### 1.2 Menggunakan Windows Portable (`.zip`)
Metode ini tidak memerlukan proses instalasi atau hak akses administrator sistem.
1. Unduh berkas **`CafePulse_Free_Portable.zip`** atau **`CafePulse_Professional_Portable.zip`**.
2. Klik kanan file `.zip` yang diunduh, lalu pilih **Extract All...** (Ekstrak Semua).
3. Tentukan direktori tujuan ekstraksi (misalnya di folder Documents atau Desktop), lalu klik **Extract**.
4. Buka folder hasil ekstraksi, cari berkas bernama **`CafePulse.exe`** (dengan ikon logo CafePulse).
5. Klik ganda untuk langsung menjalankan aplikasi.

---

## 2. Panduan Instalasi Linux

CafePulse didistribusikan di Linux sebagai paket **AppImage** mandiri (arsitektur x86_64), yang dapat berjalan di berbagai distro populer (Ubuntu, Debian, Fedora, Arch Linux, dll.) tanpa proses instalasi yang rumit.

### 2.1 Menyiapkan Dependensi Awal (PyQt6 Runtimes)
Sebagian besar distro Linux desktop modern telah menyertakan dependensi grafis dasar. Namun, jika aplikasi gagal meluncur, pastikan pustaka Qt6 dan XCB terpasang di sistem Anda.

- **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update
  sudo apt install -y libegl1 libgl1-mesa-glx libxcb-cursor0 libxkbcommon-x11-0
  ```
- **Fedora / RHEL:**
  ```bash
  sudo dnf install -y mesa-libGL libxcb libxkbcommon-x11
  ```
- **Arch Linux:**
  ```bash
  sudo pacman -Syu mesa libxcb libxkbcommon-x11
  ```

### 2.2 Menjalankan AppImage via File Manager (GUI)
1. Unduh berkas **`CafePulse_Free.AppImage`** atau **`CafePulse_Professional.AppImage`**.
2. Buka aplikasi File Manager Linux Anda dan temukan berkas yang baru diunduh.
3. Klik kanan berkas `.AppImage`, lalu pilih **Properties** (Properti).
4. Masuk ke tab **Permissions** (Izin).
5. Centang opsi **"Allow executing file as program"** (Izinkan mengeksekusi berkas sebagai program).
6. Tutup jendela Properties, lalu klik ganda berkas `.AppImage` untuk meluncurkannya.

### 2.3 Menjalankan AppImage via Terminal (CLI)
Buka terminal Anda, masuk ke folder tempat berkas diunduh, lalu jalankan perintah berikut:
```bash
# Memberikan izin eksekusi pada berkas
chmod +x CafePulse_Free.AppImage

# Menjalankan aplikasi
./CafePulse_Free.AppImage
```

---

## 3. Catatan Integrasi Desktop (Linux AppImage Launcher)
Agar AppImage terintegrasi ke menu aplikasi desktop Linux Anda secara permanen:
1. Pasang alat bantu pihak ketiga gratis seperti **AppImageLauncher** (https://github.com/TheAssassin/AppImageLauncher).
2. Alat ini akan otomatis mendeteksi setiap AppImage yang Anda klik ganda, menanyakan apakah Anda ingin mengintegrasikannya, and membuat shortcut peluncur resmi di menu aplikasi sistem operasi Anda.
