# CAFEPULSE PROJECT BIBLE
### *The Foundational Document & Constitution — v1.0.0 | Locked: Juni 2026*

> **Status:** DIKUNCI & FINAL (SSOT) — Perubahan pada dokumen ini hanya boleh dilakukan melalui keputusan strategis dengan justifikasi tertulis yang kuat.

---

## 1. VISION & MISSION

### 1.1 Vision Statement
> **"Menjadi platform operasi jaringan lokal yang paling dipercaya dan digunakan oleh operator jaringan Indonesia — dari warnet hingga ISP kecil — dengan filosofi Local-First yang menempatkan privasi dan kontrol penuh di tangan pengguna."**

### 1.2 Mission Statement
> **"Memberikan alat operasional jaringan kelas enterprise kepada operator jaringan skala kecil dan menengah di Indonesia, dengan harga yang terjangkau, tanpa ketergantungan cloud, dan tanpa kompromi terhadap privasi data."**

### 1.3 Tagline Resmi
**"Local-First Network Intelligence."**

---

## 2. PROBLEM STATEMENT & CORE PRINCIPLES

### 2.1 Problem Statement
Mengelola jaringan MikroTik skala menengah (kafe, warnet, RT/RW Net) sering kali memicu kelelahan operasional (*operational fatigue*) karena Winbox yang terlalu teknis dan manual, serta tersebarnya data operasional (spreadsheets, catatan, log). Solusi modern yang ada di pasar memaksa pengguna beralih ke cloud/SaaS, yang merampas privasi data operasional serta ketergantungan internet luar yang tidak andal di daerah rural.

### 2.2 Core Principles (The Local-First Manifesto)
1. **Data Sovereignty:** Data Anda adalah milik Anda. Sepenuhnya. Selalu.
2. **Zero Cloud Dependency:** Semua fungsi inti beroperasi 100% offline.
3. **No Hidden Telemetry:** Tidak ada pengumpulan data, log aktivitas, atau pelacakan telemetri.
4. **Local Encryption:** Kredensial router disimpan terenkripsi di database SQLite lokal.
5. **Anti-Subscription (No SaaS Trap):** Model pembelian satu kali (*one-time purchase*) demi ketenangan finansial.
6. **Anti-Lockout Graceful Fallback:** Lisensi tidak valid akan menurunkan status ke Free Edition secara anggun, bukan mengunci sistem (*no lockout*).

---

## 3. TECH STACK & CONSTRAINTS

### 3.1 Tech Stack
*   **Language:** Python 3.12+ (Native Desktop Execution)
*   **UI Engine:** PyQt6 (C++ Native Performance & Low Memory Footprint)
*   **Database:** SQLite3 (Serverless, WAL Mode enabled for concurrent reads/writes)
*   **Cryptography:** Python `cryptography` library (RSA-4096 asimetris)
*   **PDF Compiler:** fpdf2 (Documentation compile) & ReportLab (Voucher PDF export layouts)
*   **Installer:** PyInstaller (Compile to standalone binaries) & Inno Setup 6 (Windows installers)

### 3.2 Constraints
*   **Offline Mode:** Sistem aktivasi dan verifikasi lisensi wajib mendukung 100% offline (file-exchange `.licreq` -> `.lic`).
*   **Windows UAC Compatibility:** Aplikasi harus berjalan dengan hak akses user biasa tanpa memerlukan hak administrator/elevasi Windows UAC.
*   **Single-PC Licensing:** Lisensi diikat mutlak menggunakan Hardware ID (HWID) per PC untuk mengelola eksklusivitas.
*   **Separation of Folders:** Folder instalasi bersifat read-only. Folder data user (`LOCALAPPDATA/CafePulse/`) bersifat writable.

---

## 4. TECHNICAL & ARCHITECTURE RULES

### 4.1 Technical Rules
1. **Startup Validation:** Wajib memeriksa versi Python (>= 3.12), direktori log/ekspor, database integrity (`PRAGMA integrity_check`), dan dependensi sebelum GUI dimuat.
2. **Safe Mode Recovery:** Jika startup validation gagal atau database rusak, aplikasi harus memuat menu *Safe Mode / Recovery Window* berisi daftar error secara detail dan fallback database bersih.
3. **Thread Isolation (QThreads):** Tugas I/O blocking (seperti polling API MikroTik, sweeps ARP, WiFi monitoring) harus didelegasikan ke thread worker terpisah (`QThread`) untuk menjaga UI tetap reaktif.
4. **Signaling & Slots:** Background thread dilarang memanipulasi widget UI secara langsung. Interaksi wajib menggunakan sistem Qt Signals & Slots.

### 4.2 Architecture Rules
1. **No Cloud Backend:** Larangan absolut untuk melakukan sinkronisasi data konfigurasi, kredensial, logs, atau statistik ke server cloud eksternal.
2. **No Packet Sniffing:** Pemetaan jaringan hanya menggunakan kueri API resmi, neighbor discovery (MNDP), dan sweeps ARP. Penggunaan library packet sniffing (seperti scapy/libpcap) dilarang.
3. **No Asyncio Rewrite:** Loop event asinkron dikendalikan sepenuhnya oleh event loop PyQt6. Penggunaan `asyncio` dilarang untuk menghindari memory leaks di thread utama.
4. **SQLite WAL Mode:** Wajib menggunakan mode WAL (`PRAGMA journal_mode=WAL`) agar penulisan background thread tidak mengunci pembacaan UI thread.

---

## 5. CODING STANDARDS & NAMING CONVENTIONS

### 5.1 Coding Standards
*   Patuhi pedoman gaya kode **PEP 8** secara ketat.
*   Batas maksimal panjang baris adalah **120 karakter**.
*   Dokumentasikan modul, kelas, dan fungsi public menggunakan docstring yang jelas.
*   Pertahankan separation of concerns: Pisahkan UI widgets, Core Engine, Database Layer, dan Utilities.

### 5.2 Naming Conventions
*   **Packages & Modules (Files):** lowercase dengan underscores (`snake_case`, contoh: `rsa_manager.py`).
*   **Classes:** CapWords (`CamelCase`, contoh: `RSAManager`, `MainWindow`).
*   **Functions & Variables:** lowercase dengan underscores (`snake_case`, contoh: `verify_signature`, `is_pro`).
*   **UI Widgets:** CapWords (`CamelCase`, contoh: `LicensePage`, `DashboardTab`).
*   **Constants:** UPPERCASE dengan underscores (`UPPER_CASE`, contoh: `DEFAULT_PUBLIC_KEY_PEM`).

---

## 6. SECURITY & ENCRYPTION RULES

1. **Private Key Isolation:** File kunci privat RSA (`private_key.pem`) adalah properti paling rahasia developer. File ini **TIDAK BOLEH** dimasukkan ke dalam paket instalasi klien publik, dan harus dikecualikan di `.gitignore`.
2. **Hardcoded Public Key:** Kunci publik RSA ditanam secara aman di dalam `rsa_manager.py` klien untuk memvalidasi tanda tangan lisensi offline secara instan.
3. **Obfuscation of Credentials:** Kredensial login router MikroTik yang disimpan di SQLite lokal wajib dienkripsi/obfuskasi menggunakan kunci enkripsi lokal yang terikat pada UUID hardware PC user.

---

## 7. NON GOALS (APA YANG TIDAK AKAN DILAKUKAN CAFEPULSE)

*   Tidak akan membuat versi dashboard web cloud.
*   Tidak akan bermigrasi ke model langganan bulanan (SaaS).
*   Tidak akan mengintegrasikan telemetri atau tracking analitik pengguna.
*   Tidak akan mendukung router non-MikroTik (fokus eksklusif pada RouterOS).
