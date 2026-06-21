# CafePulse System Requirements (Spesifikasi Sistem)

Spesifikasi perangkat keras (hardware) dan sistem operasi (software) minimum dan rekomendasi untuk menjalankan CafePulse secara optimal di Windows dan Linux, serta tingkat kompatibilitas RouterOS.

---

## 1. Spesifikasi Perangkat Lunak (Software Compatibility)

### 1.1 Client Operating System
CafePulse berjalan sebagai aplikasi desktop native 64-bit.

- **Windows Support:**
  - *Minimum:* Windows 10 (Build 1809 atau lebih baru).
  - *Rekomendasi:* Windows 11 (64-bit).
- **Linux Support:**
  - Distro Linux x86_64 dengan desktop manager modern (Ubuntu 20.04+, Debian 11+, Fedora 36+, Arch Linux).
  - Pustaka Qt6/PyQt6 dependencies wajib terpasang jika distro tidak memuatnya (lihat [Installation Guide](./documentation.html?doc=installation_guide)).

### 1.2 MikroTik RouterOS Compatibility
CafePulse terhubung ke routerboard Anda melalui protokol API RouterOS.
- **RouterOS v6.x:** Didukung penuh (API protocol standar).
- **RouterOS v7.x:** Didukung penuh (termasuk optimalisasi koneksi API baru).
- **RouterOS API Service:** Port `8728` (clear text) atau `8729` (SSL encrypted) harus diizinkan terbuka di router.

---

## 2. Spesifikasi Perangkat Keras (Hardware Requirements)

Aplikasi desktop CafePulse didesain sangat efisien and ringan (menggunakan memori di bawah 120 MB saat berjalan).

| Komponen | Spesifikasi Minimum | Spesifikasi Rekomendasi |
|---|---|---|
| **CPU / Prosesor** | Intel Core i3 Gen-4 / AMD Ryzen 3 (Dual-Core 2.0 GHz) | Intel Core i5 Gen-8 / AMD Ryzen 5 atau lebih baru |
| **Memory (RAM)** | 2 GB RAM | 4 GB RAM atau lebih |
| **Disk Space** | 200 MB (aplikasi) + 500 MB (database log) | SSD dengan 1 GB ruang kosong |
| **Display / Layar** | Resolusi 1366 x 768 piksel | Resolusi Full HD 1920 x 1080 piksel |
| **Network Interface** | Port Ethernet atau WiFi Adapter | Gigabit Ethernet / AC WiFi Adapter |

---

## 3. Catatan Ketersediaan Jaringan (Network Access)
CafePulse berjalan 100% secara lokal.
- **Internet Access:** **Tidak diperlukan** untuk operasional harian.
- **Local Access:** Komputer klien wajib berada di dalam satu subnet jaringan lokal menuju alamat IP API router MikroTik yang dituju.
