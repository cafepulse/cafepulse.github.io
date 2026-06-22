# CAFEPULSE 1.0.0.0
# MASTER PRODUCT & RELEASE ROADMAP (OFFICIALLY LOCKED)

> **Status:** DIKUNCI & FINAL (OFFICIALLY LOCKED)  
> **Tanggal Penguncian:** 31 Mei 2026  
> **Versi Target:** 1.0.0.0  
> **Platform Didukung:** Windows (EXE, MSI), Linux (AppImage, DEB), macOS (DMG)  
> **Domain Resmi:** cafepulse.net  

---

## 1. IDENTITAS & FILOSOFI PRODUK

### Definisi Produk
CafePulse adalah **MikroTik Operations Platform** modern yang menggabungkan:
*   Monitoring & Analytics
*   Router Management
*   Hotspot & Voucher Management
*   Configuration Tools
*   Network Operations
*   Business Intelligence (BI)

ke dalam satu aplikasi desktop adaptif yang bersifat **Local-First**, **Offline-Friendly**, dan **Workflow-Driven** (*Powerful but Understandable*).

### Target Pengguna
1.  Teknisi MikroTik (Prioritas Utama)
2.  RT/RW Net
3.  Kafe & Tempat Usaha
4.  Hotel Kecil
5.  Sekolah / Lembaga Pendidikan
6.  Usaha dengan Hotspot Publik

---

## 2. WORKSPACE SYSTEM & EDISI PRODUK

### Workspace Adaptif
*   **Workspace Business:** KPI Jaringan, Statistik Pengunjung, Jam Ramai, Kesehatan Jaringan, Alert Penting. (Fokus: Pemilik Usaha, Supervisor, Manajer).
*   **Workspace Operations:** Voucher, Users, Devices, DHCP, Backup, Logs. (Fokus: Operator & Admin Hotspot).
*   **Workspace Network:** IP, DNS, DHCP Network, PPP, Wireless, Bridge, VLAN, Interfaces. (Fokus: Teknisi Jaringan).
*   **Workspace Advanced:** Firewall, NAT, Mangle, Routing, Queue, Scripts, Scheduler. (Fokus: Network Engineer).

### Perbandingan Edisi

| Fitur | CafePulse Free (Gratis Selamanya) | CafePulse Professional (One-Time Purchase) |
|---|:---:|:---:|
| **Discovery** | Scan & Neighbor Discovery | Multi Router Scan & Management |
| **Monitoring** | Dasar (CPU, RAM, Uptime, Router Info) | Lengkap & Historis (Grafik Realtime) |
| **Hotspot** | Monitoring User Aktif | Hotspot Manager & Voucher Generator |
| **Network Manager** | Monitoring DHCP Lease Aktif | IP, DNS, DHCP, PPP, Wireless, Bridge, VLAN |
| **Backup** | Backup Manual | Automated Scheduled Backup & Versioning |
| **Advanced Tools** | Logs Dasar (Viewer) | Firewall, Queue, Routing, Scheduler, Scripts |
| **BI & Analytics** | Tidak Tersedia | Business Intelligence, Smart Insight Assistant (AI) |

---

## 3. KEPUTUSAN STRATEGIS & MODEL BISNIS (LOCKED)

*   **Model Lisensi:** 1 Lisensi = 1 PC.
*   **Masa Pembaruan:** Gratis update selama 5 tahun. Setelah 5 tahun, software tetap berjalan penuh secara lokal namun pembaruan dihentikan hingga lisensi diperpanjang.
*   **Aktivasi Lisensi:** Mendukung **Online Activation** dan **Offline Activation** (Request File ➜ Activation File) untuk mengakomodasi instalasi di jaringan terisolasi.
*   **Model Pembayaran:** Pembayaran lokal Indonesia terintegrasi Payment Gateway (QRIS, DANA, GoPay, ShopeePay, OVO, Virtual Account, Transfer Bank, Kartu Kredit).
*   **Harga Patokan:** Rp 499.000 (One-Time Purchase) dengan harga promo peluncuran Rp 399.000 selama 30 hari pertama.
*   **Program Kemitraan:** Program Afiliasi dengan komisi 10% per transaksi dan diskon referral 5% - 10%.
*   **Saluran Dukungan:** Email Resmi (`support@cafepulse.app` / `support@cafepulse.net`) dan Server Discord Komunitas.
*   **Aspek Legal Sebelum Rilis:** EULA (End User License Agreement), Privacy Policy, Terms of Service, dan Registrasi Merek Dagang CafePulse.

---

## 4. TAHAPAN EKSEKUSI TEKNIS (PHASE ROADMAP)

### PHASE 1 — FOUNDATION STABILIZATION (STATUS: LULUS ✓)
*   Pembangunan **Pulse Engine** (Event System & Multi-threaded Task Management).
*   Lapisan Database Lokal menggunakan **SQLite** (`cafepulse.db`) dengan mode WAL untuk stabilitas.
*   **Settings & Theme Manager** terpusat (Tema Utama: *Dark Modern Blue*).
*   Sistem **Structured Logging & Error Handling** (Global Exception Handler & Crash Logger di `/logs/crash/`).
*   **Recovery System** otomatis jika terjadi pemadaman listrik/shutdown tidak aman (Safe Mode & Auto Recovery).

### PHASE 2 — SMART CONNECTION PLATFORM (STATUS: SELESAI ✓)
*   **MikroTik Discovery Engine:** Scan otomatis melalui API, API SSL, Neighbor Discovery, Local Network Scan, dan MAC Detection.
*   **Smart Router List:** Manajemen multi-router berbasis grup dan tag kustom.
*   **Connection Profiles & Vault:** Penyimpanan kredensial terenkripsi yang aman (*Secure Credential Vault*).
*   **Connection Health Check:** Metrik kualitas latensi realtime dan penanganan diskoneksi (*Auto Reconnect* dengan capped exponential backoff).

### PHASE 3 — OPERATIONS PLATFORM (STATUS: AKTIF 🚀)
*   **Hotspot Manager:** Dashboard operasional hotspot, pemantauan user aktif/offline, statistik login harian, dan operasi cepat (Create/Disable/Enable/Delete/Bulk Action).
*   **Voucher Generator (Fitur Unggulan):** Batch generator voucher (hingga 500 voucher sekaligus), kustomisasi profil kuota/durasi, kode acak atau dengan awalan kustom (*prefix*), ekspor PDF/Excel/CSV siap cetak berbagai ukuran (Kecil, Sedang, Besar).
*   **Device Manager:** Deteksi nama perangkat, MAC, IP, dan vendor otomatis (Local Cache OUI) dengan pengelompokan jenis (Smartphone, Laptop, IoT).
*   **DHCP Lease Center:** Manajemen reservasi IP, pelepas lease (*Release*), dan pencarian lease cepat.
*   **Backup Manager:** Pengambilan konfigurasi MikroTik terjadwal (harian, mingguan, bulanan) dengan versioning kustom dan restore langsung dari UI.
*   **Structured Logs & Diagnostic:** Filter logs komersial dan fitur *Export Diagnostic Package* (ZIP) untuk mempermudah pelaporan bug.

### PHASE 4 — NETWORK PLATFORM (STATUS: RENCANA BERIKUTNYA 📅)
*   **Network Overview:** Status WAN, DNS, DHCP, Interfaces, dan PPP Ringkas di satu layar.
*   **Smart Troubleshooting (Internet Health Center):** Penilaian mandiri latensi, kehilangan paket data (*packet loss*), dan skor kesehatan jaringan (Health Score 0-100%).
*   **VLAN Creation Wizard:** Wizard konfigurasi VLAN aman 4 langkah untuk menggantikan kompleksitas Winbox.
*   **Network Topology View:** Pemetaan topologi jaringan otomatis (Router ➜ Switch ➜ Access Point ➜ Client).
*   **Modul Manajemen Jaringan:**
    *   *IP Address Manager:* Smart suggestions subnet & duplikasi IP validation.
    *   *DNS Manager:* Static DNS setup, Cache viewer, & DNS Flush.
    *   *PPP Manager:* Manajemen PPPoE, PPTP, L2TP, SSTP, & OpenVPN serta monitoring session aktif.
    *   *Wireless Manager:* Visualisasi interferensi frekuensi, pengontrol Access Point & Client list.
    *   *Bridge Manager:* Penugasan port fisik ke jembatan virtual.

### PHASE 5 — ADVANCED NETWORK PLATFORM (STATUS: VISI MASA DEPAN 🔮)
*   *Firewall Workspace:* Manajemen Rule Filter, NAT (Port Forwarding), dan Mangle secara intuitif.
*   *Queue Manager:* Pembagian bandwidth dinamis (Simple Queue, Queue Tree, PCQ) dengan grafik utilisasi realtime.
*   *Automation Engine:* Script Center terintegrasi, Scheduler MikroTik, dan eksekusi skrip otomatis berbasis pemicu *alert*.

---

## 5. KRITERIA SELESAI RILIS 1.0.0.0 (DEFINITION OF DONE)
Aplikasi CafePulse 1.0.0.0 dianggap siap jual jika dan hanya jika:
1.  Seluruh modul dari **Phase 1** hingga **Phase 4** terimplementasi penuh secara fungsional dan stabil.
2.  Telah lulus uji coba ketahanan durasi panjang (**Stress Test 24/72 Jam**) tanpa kebocoran memori (*memory leaks*), dibuktikan dengan tersedianya `stress_test_report.md`.
3.  Kredensial disimpan dalam **Secure Vault terenkripsi** di tingkat lokal.
4.  Installer native untuk **Windows** (Inno Setup) dan **Linux** (AppImage) telah diuji dan berfungsi penuh.
5.  Situs web resmi (`cafepulse.net`) dan dokumentasi lengkap (*quick start*, *troubleshooting*) telah terbit.
6.  Sistem pembayaran lokal teruji sukses secara end-to-end.
