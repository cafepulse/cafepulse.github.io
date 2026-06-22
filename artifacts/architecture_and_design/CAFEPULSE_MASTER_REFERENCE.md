# CAFEPULSE MASTER REFERENCE (DOKUMEN KEBENARAN MUTLAK)
### *Master Repository Topology, Code Connections, & AI Navigation Rules — v1.0.0 | Juni 2026*

---

> [!IMPORTANT]
> Dokumen ini adalah **sumber kebenaran mutlak (absolute truth)** mengenai struktur proyek, hubungan kode, dan konfigurasi repositori CafePulse. Baik Developer, AI Architect (ChatGPT), maupun AI Executor (Antigravity) wajib mematuhi panduan ini secara ketat untuk menghindari duplikasi berkas, kekacauan struktur, dan kegagalan sinkronisasi.

---

## BAGIAN 1 — TOPOLOGI REPOSITORI & HUBUNGAN REPO

Proyek CafePulse memiliki arsitektur repositori bertingkat (nested repositories) secara fisik di direktori lokal. Pemisahan repositori dilakukan antara kode aplikasi (private) dan file website publik (public).

### 1.1 Struktur Fisik Direktori Lokal
Berikut adalah kebenaran mutlak mengenai pembagian repositori lokal:

```
C:\Users\USER\Documents\Yubelki\CafePulse\             <-- [LEVEL 1] Parent Folder / Uncommitted App Clone
  │
  └── CafePulse\                                      <-- [LEVEL 2] Website Repo (cafepulse.github.io)
        │                                                           Remote: cafepulse/cafepulse.github.io.git
        │
        ├── CafePulse\                                <-- [LEVEL 3] Private App Repo (youbellkey/CafePulse)
        │     │                                                     Remote: youbellkey/CafePulse.git
        │     │                                                     *SUMBER UTAMA PENGEMBANGAN APLIKASI*
        │     └── website\                            <-- [LEVEL 4] Mirror Website Folder (App Archive)
        │
        └── website\                                  <-- [LEVEL 5] Duplicate website folder (Abaikan - Hapus)
```

### 1.2 Detail Repositori & Tugas Pembaruan

| Nama Repositori | URL Git Remote | Lokasi Lokal Mutlak | Cakupan Berkas & Aturan Pembaruan |
|---|---|---|---|
| **Private App Repo** | `youbellkey/CafePulse` | `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse` | - Seluruh kode Python (`main.py`, `core/`, `ui/`, `modes/`, `tests/`, `tools/`).<br>- Dokumen internal (`docs/`).<br>- Skrip installer (`installer/`).<br>- Konfigurasi lokal (`config/Settings_default.json`).<br>- *Wajib di-commit dan di-push ke branch main.* |
| **Public Website Repo** | `cafepulse/cafepulse.github.io` | `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse` | - File HTML/CSS/JS di root untuk website publik (`index.html`, `download.html`, `pricing.html`, dll.).<br>- File rilis executable dan portabel di `website/releases/v1.0.0/` untuk diunduh langsung.<br>- *Wajib di-commit dan di-push ke branch main untuk update live site.* |

> [!WARNING]
> Jangan pernah mencampuradukkan perintah git di direktori Level 2 dan Level 3. Menjalankan perintah `git add` di `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse` tanpa berpindah folder ke `CafePulse\` di dalamnya akan memperbarui repositori website publik, bukan repositori aplikasi.

---

## BAGIAN 2 — MANIFEST FILE & ANOTASI FOLDER (KEBENARAN MUTLAK)

Setiap berkas dan folder di dalam repositori **Private App** (`Level 3: .../CafePulse/CafePulse/CafePulse`) memiliki peran spesifik. Berikut adalah daftarnya:

### 2.1 File Root Aplikasi
- `main.py`: Entrypoint utama aplikasi. Mengatur inisialisasi PyQt6 QApplication, splash screen, deteksi mode (Demo/Home/MikroTik), penanganan crash debug, dan peluncuran `MainWindow`.
- `build.py`: Skrip untuk mengompilasi aplikasi Python menjadi file `.exe` tunggal menggunakan PyInstaller.
- `CafePulse.spec`: Berkas spesifikasi PyInstaller yang mengatur metadata, dependensi library, file ikon, dan aset eksternal untuk dibundel.
- `requirements.txt`: Daftar dependensi modul Python yang dibutuhkan (PyQt6, cryptography, psutil, reportlab, fpdf2, dll.).
- `CHANGELOG.md`: Dokumentasi perubahan fitur (Keep a Changelog standard).
- `gen_project_os_ai_pdf.py`: Script generator untuk mengompilasi seluruh file `.md` di `docs/` menjadi satu file PDF master: `CafePulse_Project_OS_AI_Complete.pdf`.

### 2.2 Struktur Folder Bisnis (`core/`)
- `core/analytics/health_engine.py`: Menghitung skor kesehatan jaringan lokal secara dinamis (0-100%) menggunakan parameter latensi, loss rate, dan throughput.
- `core/database/db_manager.py`: Mengatur koneksi SQLite3 lokal (`cafepulse.db`), manajemen checkpoint WAL (Write-Ahead Logging), dan isolasi transaksi data.
- `core/licensing/license_manager.py`: Memvalidasi kunci lisensi Professional Edition secara offline menggunakan verifikasi tanda tangan kriptografis RSA-2048.
- `core/licensing/machine_id.py`: Menghasilkan ID mesin unik berbasis SHA-256 dari hardware motherboard UUID, hostname, dan primary MAC address.
- `core/mikrotik/router_discovery.py`: Melacak router MikroTik aktif di segmen jaringan lokal menggunakan broadcast MNDP (MikroTik Neighbor Discovery Protocol) dan ICMP.
- `core/mikrotik/api_client.py`: Wrapper API RouterOS untuk mengeksekusi perintah command-line Winbox secara programatis ke perangkat MikroTik.
- `core/mikrotik/voucher_engine.py`: Mesin pembuat batch voucher hotspot MikroTik (generate username/password acak berdasarkan durasi dan kuota).
- `core/scanner/arp_scanner.py`: Pemindai jaringan lokal (ARP scanning + paralel ping sweep) yang aman, senyap (tanpa terminal cmd muncul), dan efisien.
- `core/security/vault.py`: Tempat penyimpanan kredensial terenkripsi (AES/Fernet) yang terikat secara unik pada kunci hardware mesin lokal.
- `core/runtime/session_manager.py`: Mengelola file status runtime `.lock` dan `.clean` untuk mencegah multi-instance dan menangani recovery pasca-crash tak terduga.

### 2.3 Struktur Folder Background Workers (`modes/`)
- `modes/demo/demo_worker.py`: Worker thread yang menyimulasikan data aktivitas jaringan untuk pengujian fungsionalitas UI tanpa perangkat keras fisik.
- `modes/home_wifi/wifi_worker.py`: Thread latar belakang yang menjalankan pemindaian ARP secara periodik dan resolusi hostname lokal secara non-blocking.
- `modes/hotspot/hotspot_worker.py`: Memantau status login hotspot dan masa aktif sesi pelanggan secara real-time.
- `modes/mikrotik/mikrotik_worker.py`: Melakukan polling periodik (CPU, RAM, traffic interface, active users) ke router MikroTik via koneksi API RouterOS.

### 2.4 Struktur Folder GUI PyQt6 (`ui/`)
- `ui/windows/main_window.py`: Window utama PyQt6 yang mengintegrasikan sidebar navigasi, top bar status, transisi halaman, dan penanganan penutupan aman (`closeEvent`).
- `ui/themes/dark_theme.py` & `light_theme.py`: Definisi stylesheet (QSS) modern bernuansa neon modern blue (dark) dan clean dashboard (light).
- `ui/widgets/dashboard_page.py`: Menampilkan rangkuman statistik, throughput grafik, status perangkat, dan widget pintasan utama.
- `ui/widgets/devices_page.py`: Menampilkan tabel perangkat yang aktif di jaringan dengan status dipercaya (Trusted), kategori, dan catatan kustom.
- `ui/widgets/settings_page.py`: Pengaturan preferensi (theme switch, scan interval, gateway override, log level).
- `ui/widgets/home_wifi_page.py`: Antarmuka khusus pemantauan jaringan lokal non-MikroTik.
- `ui/widgets/hotspot_page.py`: Dashboard integrasi hotspot lokal.
- `ui/widgets/mikrotik_dashboard.py`: Panel monitoring performa router MikroTik (CPU, RAM, bandwidth real-time).
- `ui/widgets/iam/`: Halaman manajemen akses pelanggan (vouchers, packages, guest manager).
- `ui/widgets/network/`: Halaman konfigurasi fitur router (interfaces, dns, routing, firewall, PPP).

---

## BAGIAN 3 — ARSITEKTUR KODE & IMPORT MAP (CODE CONNECTIONS)

Visualisasi alur komunikasi kode antar modul Python diatur secara modular. Berikut adalah bagan import dan pengiriman data:

```
                  ┌──────────────────────┐
                  │       main.py        │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────┐            ┌───────────────────┐
│core/runtime/session. │            │ui/windows/main.py │
└──────────────────────┘            └─────────┬─────────┘
                                              │
                                   ┌──────────┴──────────┐
                                   ▼                     ▼
                        ┌───────────────────┐   ┌──────────────────┐
                        │ui/widgets/pages   │   │ui/themes/        │
                        └──────────┬────────┘   └──────────────────┘
                                   │
                                   ▼
                        ┌───────────────────┐
                        │modes/workers      │
                        └──────────┬────────┘
                                   │
                                   ▼
                        ┌───────────────────┐
                        │core/scanner & api │
                        └──────────┬────────┘
                                   │
                                   ▼
                        ┌───────────────────┐
                        │core/database/db   │
                        └───────────────────┘
```

### 3.1 Hubungan Modular & Alur Data
1. **Entry Point Initialization**: `main.py` memanggil `core.runtime.session_manager.SessionManager` untuk memvalidasi status runtime. Jika aplikasi ditutup secara tidak wajar sebelumnya, session manager menampilkan dialog recovery, lalu meluncurkan `ui.windows.main_window.MainWindow`.
2. **Page Navigation**: `MainWindow` memuat `ui/themes/` dan menata tata letak `Sidebar`. Saat user berpindah menu, widget halaman yang sesuai di `ui/widgets/` dimuat ke area konten utama.
3. **Background Worker Processing**: Halaman UI seperti `HomeWifiPage` tidak melakukan pemindaian jaringan di UI Thread (agar aplikasi tidak lag). Halaman tersebut membuat instansi `modes.home_wifi.wifi_worker.WifiWorker` yang berjalan di thread terpisah (`QThread`).
4. **Core Scanning & API Calls**: Worker thread secara periodik memanggil class backend di layer `core/` (seperti `core.scanner.arp_scanner.ARPScanner` untuk scan IP/MAC atau `core.mikrotik.api_client` untuk router MikroTik).
5. **Data Persistence**: Class pemindai atau API client mengambil data mentah dari jaringan, menyaringnya, lalu memanggil `core.database.db_manager.DatabaseManager` untuk memperbarui tabel SQLite3 (`cafepulse.db`). Setelah selesai, worker mengirim sinyal PyQt (`pyqtSignal`) berisi data baru kembali ke UI Thread untuk diperbarui di layar secara instan.

---

## BAGIAN 4 — ATURAN NAVIGASI KETAT UNTUK AI AGENT (AI NAVIGATION RULES)

Setiap AI Agent (Antigravity, ChatGPT, dll.) yang bekerja di proyek CafePulse **WAJIB** mengikuti aturan navigasi ini untuk mencegah kerusakan struktur file:

1. **Verifikasi Folder Kerja (Cwd)**:
   - Sebelum mengedit kode Python aplikasi atau file `.md` dokumentasi, pastikan Anda berada di root folder aplikasi Level 3:
     `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse`
   - Jangan pernah mengedit berkas di Level 1 (`C:\Users\USER\Documents\Yubelki\CafePulse`), karena berkas-berkas di Level 1 adalah file cadangan / tidak terlacak.

2. **Aturan Sinkronisasi Website**:
   - Jika Anda melakukan perubahan pada desain atau fungsi halaman website (seperti tombol download di `download.html`):
     1. Ubah file utama di Level 2: `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\<file>.html`
     2. Salin (mirror) file tersebut ke Level 4: `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse\website\<file>.html` agar repositori arsip aplikasi tetap sinkron.

3. **Larangan Keras Duplikasi Folder**:
   - **TIDAK BOLEH** membuat folder di dalam folder yang memiliki nama yang sama (misal: `CafePulse/core/core/` atau `CafePulse/ui/ui/`).
   - Sebelum membuat folder atau file baru, selalu jalankan pemindaian direktori atau periksa Manifest di Bagian 2 dokumen ini untuk memastikan apakah file tersebut sudah ada atau belum.

4. **Operasi Git**:
   - Komit kode Python HANYA di direktori Level 3 (`youbellkey/CafePulse`).
   - Komit pembaruan website HANYA di direktori Level 2 (`cafepulse/cafepulse.github.io`).
   - Selalu periksa `git status` dan pastikan file binary besar seperti Setup `.exe` atau portabel `.zip` tidak tidak sengaja masuk ke repositori aplikasi private (kecuali diizinkan secara eksplisit di `.gitignore` website).

5. **Penamaan File Baru**:
   - Semua nama file baru harus ditulis dalam huruf kecil menggunakan format *snake_case* (misal: `network_helper.py`), kecuali untuk berkas dokumentasi markdown `.md` yang harus ditulis dalam huruf besar dengan *snake_case* (misal: `FEATURE_SPEC_PROFESSIONAL.md`).

---

## BAGIAN 5 — PANDUAN ANTI-BINGUNG & DIAGNOSTIK (TROUBLESHOOTING)

### 5.1 Mengapa Terjadi Duplikasi Berkas/Folder?
Duplikasi sering terjadi karena:
- LLM AI berasumsi bahwa folder root proyek adalah `C:\Users\USER\Documents\Yubelki\CafePulse` dan secara tidak sengaja membuat folder `CafePulse` baru di dalamnya saat diminta melakukan build.
- Kebingungan membedakan mana repositori website (`cafepulse.github.io`) dan repositori aplikasi (`youbellkey/CafePulse`).

### 5.2 Cara Memperbaiki Folder Terduplikasi
Jika Anda mendeteksi adanya folder seperti `C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse\CafePulse`, segera jalankan langkah pembersihan ini:
1. Pastikan file kode terbaru di dalam folder terdalam disalin ke folder Level 3 yang benar (`C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse`).
2. Jalankan perintah penghapusan folder terduplikasi yang tidak sengaja terbuat menggunakan shell terminal:
   `Remove-Item -Recurse -Force -Path "C:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\CafePulse\CafePulse"` (sesuaikan path).

### 5.3 Checklist Validasi Sebelum Mengakhiri Tugas
Sebelum AI Agent menyelesaikan tugas dan melaporkan ke developer:
- [ ] Apakah pekerjaan dilakukan di Level 3 (untuk aplikasi) atau Level 2 (untuk website)?
- [ ] Apakah ada file `.exe`, `.zip`, atau file binary besar lain yang tidak sengaja ditambahkan ke Git repositori aplikasi?
- [ ] Apakah file database lokal `cafepulse.db` dibersihkan/dihapus sebelum kompilasi installer?
- [ ] Apakah script `gen_project_os_ai_pdf.py` telah dijalankan untuk memperbarui PDF kompilasi master?

---

*Dokumen Kebenaran Mutlak CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
