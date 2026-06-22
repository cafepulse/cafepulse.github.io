# Linux Risks and Blockers Report — CafePulse
### *Targeting Linux Distribution Foundation (Sprint 1) — Locked: Juni 2026*

---

## 1. PENDAHULUAN

Dokumen ini memetakan seluruh potensi risiko teknis, keterbatasan arsitektur, dan blocker (penghambat) yang dapat mempengaruhi kestabilan, performa, atau kemudahan pengemasan CafePulse di sistem operasi Linux.

---

## 2. RISIKO TEKNIS & PROFIL MITIGASI

### 2.1 Ketergantungan terhadap Server Tampilan (Display Server: X11 vs Wayland)
> [!WARNING]
> PyQt6 (yang membungkus toolkit Qt6) sangat sensitif terhadap server tampilan yang digunakan oleh distro Linux modern.
- **Risiko:** Distro Linux terbaru (seperti Ubuntu 22.04+ atau Fedora) menggunakan **Wayland** secara default menggantikan **X11**. Terkadang, library Qt6 terkompilasi PyInstaller gagal memuat backend Wayland secara native, memicu error:
  `qt.qpa.plugin: Could not load the Qt platform plugin "wayland" even though it was found.`
- **Mitigasi:**
  - Memaksa penggunaan backend XWayland (X11 emulation) dengan menyetel environment variable di shell / AppImage runner:
    `export QT_QPA_PLATFORM=xcb`
  - Menyertakan library `libqxcb.so` beserta semua dependensi X11 xcb dalam paket AppImage.

### 2.2 Keandalan Hardware ID (HWID) Tanpa Registry
- **Risiko:** Di Windows, registry `MachineGuid` sangat stabil dan tahan terhadap perubahan hardware minor (seperti pergantian kartu LAN/MAC address). Di Linux, ID mesin `/etc/machine-id` dihasilkan saat OS pertama kali diinstal. Namun, jika user menjalankan aplikasi di dalam container, sandbox virtual (seperti Flatpak/Snap), atau melakukan pembersihan system-wide, berkas ini bisa berubah atau terisolasi, menyebabkan status lisensi CafePulse ter-reset.
- **Mitigasi:** Menggabungkan minimal 3 parameter unik dalam fallback chain HWID di Linux:
  1. `/etc/machine-id` (System ID).
  2. Motherboard UUID (`/sys/class/dmi/id/product_uuid` - memerlukan hak akses read tertentu).
  3. MAC Address primer (`uuid.getnode()`).

---

## 3. DAFTAR BLOCKER TEKNIS

Saat ini **tidak ditemukan blocker mutlak** yang menghentikan porting CafePulse ke Linux. Namun, terdapat beberapa blocker operasional/kondisional yang perlu diwaspadai:

### 3.1 Izin Eksekusi Command CLI Jaringan (`ping`)
- **Blocker:** Di beberapa distribusi Linux yang diamankan secara ketat (seperti Arch Linux atau Fedora di bawah konfigurasi SELinux tertentu), utilitas `ping` dibatasi hak eksekusinya untuk user biasa (non-root) atau memerlukan capability `CAP_NET_RAW`.
- **Dampak:** Skenario *ping sweep* pada modul scanning ARP lokal mungkin gagal mengumpulkan cache IP gateway.
- **Solusi/Mitigasi:** Program tetap dapat membaca entri ARP cache yang sudah ada (`arp -n`), namun tidak dapat memicu ARP updates secara agresif via ping.

### 3.2 Dynamic Linker Compatibility (glibc Version Lock-in)
- **Blocker:** AppImage dibangun di GitHub Actions menggunakan `ubuntu-22.04` yang memuat pustaka C standar (`glibc`) versi tertentu. Jika pengguna mencoba menjalankan AppImage di distro Linux yang jauh lebih lama (misal CentOS 7 atau Ubuntu 18.04) yang memiliki versi `glibc` lebih rendah dari runner compile, aplikasi akan gagal boot dengan error:
  `/lib/x86_64-linux-gnu/libc.so.6: version 'GLIBC_2.35' not found`
- **Solusi/Mitigasi:** Ini adalah aturan dasar AppImage: *Build on the oldest system you target*. Penggunaan runner `ubuntu-22.04` (glibc 2.35) adalah pilihan yang seimbang untuk distro modern. Jika ingin mendukung distro yang lebih tua, kompilasi harus diturunkan ke runner `ubuntu-20.04` (glibc 2.31).
