# CafePulse Known Issues & Troubleshooting (Skenario Error & Solusi)

Daftar bug potensial, peringatan sistem operasi, dan panduan pemecahan masalah (*workaround*) yang mungkin ditemui oleh para beta tester.

---

## 1. Proteksi Windows Defender SmartScreen

### Gejala:
Saat menjalankan berkas installer `CafePulse_Free_Setup.exe` atau `CafePulse_Professional_Setup.exe` untuk pertama kali, Windows Defender memunculkan jendela biru bertuliskan:
> **"Windows protected your PC"** (SmartScreen blocked an unrecognized app).

### Mengapa ini terjadi?
Hal ini adalah perilaku standar Windows untuk biner baru yang **belum ditandatangani secara digital** menggunakan Microsoft Authenticode Certificate berbayar (yang memerlukan biaya berlangganan tahunan cukup mahal).

### Solusi / Workaround:
1. Klik tautan teks **"More info"** di bagian atas teks dialog.
2. Tombol baru **"Run anyway"** akan muncul di bagian bawah.
3. Klik **"Run anyway"** untuk meluncurkan setup wizard. Aplikasi CafePulse 100% aman dan bebas dari malware.

---

## 2. Linux AppImage Gagal Meluncur (Missing Qt6 Dependencies)

### Gejala:
Mengklik ganda file `.AppImage` di beberapa distro Linux minimal tidak memunculkan antarmuka grafis aplikasi, atau memicu log error di terminal:
> `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`

### Mengapa ini terjadi?
Paket AppImage membawa biner program, tetapi PyQt6/Qt6 runtime membutuhkan pustaka grafis sistem operasi host (seperti pustaka XCB atau OpenGL driver) yang terkadang tidak terpasang di distro Linux minimal atau server edition.

### Solusi / Workaround:
Pasang paket dependensi sistem berikut melalui terminal distro masing-masing:
- **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update && sudo apt install -y libegl1 libgl1-mesa-glx libxcb-cursor0 libxkbcommon-x11-0
  ```
- **Fedora / RHEL:**
  ```bash
  sudo dnf install -y mesa-libGL libxcb libxkbcommon-x11
  ```
- **Arch Linux:**
  ```bash
  sudo pacman -Syu mesa libxcb libxkbcommon-x11
  ```

---

## 3. Kegagalan Koneksi Router (Router API Connection Failed)

### Gejala:
Aplikasi melaporkan `"Connection Timeout"` atau `"Authentication failed"` saat melakukan pengetesan profil koneksi MikroTik.

### Solusi / Workaround:
1. **Periksa Status Service API:** Buka Winbox router Anda, masuk ke **IP** ➔ **Services**. Pastikan service **api** (port default `8728`) atau **api-ssl** (port `8729`) berstatus **Enabled** (tidak berwarna abu-abu).
2. **Kredensial User:** Pastikan user API MikroTik Anda memiliki akses `read` dan `write` pada group permission-nya.
3. **Firewall Block:** Pastikan tidak ada firewall rule di MikroTik `/ip firewall filter` yang memblokir akses port 8728/8729 dari segmen IP komputer klien Anda.

---

## 4. Hardware ID (HWID) Tidak Cocok Setelah Ganti Hardware

### Gejala:
Lisensi Professional yang diimpor mendadak tidak aktif lagi dan menampilkan pesan error `"Invalid License (HWID Mismatch)"`.

### Mengapa ini terjadi?
Kunci lisensi diikat secara kriptografis ke identitas hardware PC Anda (HWID). Jika Anda mengganti komponen vital komputer (seperti motherboard atau CPU), HWID lokal akan berubah.

### Solusi / Workaround:
Selama masa beta, silakan buat Activation Request file `.licreq` baru dari tab Licensing aplikasi dan kirimkan ke email support <cafepulse.network@gmail.com> untuk penerbitan ulang lisensi baru secara gratis.
