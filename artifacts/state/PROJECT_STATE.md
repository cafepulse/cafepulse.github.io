# PROJECT STATE
### *Current System State & Technical Debt — Locked: Juni 2026*

---

## 1. CURRENT STATUS
CafePulse saat ini berada pada fase **Closed Beta Launch**. 
Fokus utama adalah pelaksanaan kampanye uji coba beta tertutup (Closed Beta), pengumpulan feedback, triase bug, dan menjaga kestabilan operasional rilis.

---

## 2. FEATURE STATUS

### 2.1 Completed Features (Selesai & Stabil)
*   **Startup Validation & Safe Mode Recovery:** Pengecekan runtime sebelum boot, penanganan berkas `.lock`/`.clean`, dan menu recovery saat crash.
*   **WAL SQLite Database Integration:** Kueri database asinkron yang aman untuk data router dan log metrik.
*   **RSA-4096 Licensing System:** Modul validasi offline, pengikatan hardware ID (HWID), and grace-mode auto-downgrade.
*   **Hotspot Voucher PDF Engine:** Batch generator voucher hotspot dengan ekspor PDF siap cetak.
*   **Offline Subnet Fallback Chain:** Pemindaian ARP jaringan lokal 6-tahap yang tangguh saat komputer offline (tidak ada internet).
*   **Silent subprocess execution:** Eksekusi shell tools (`ipconfig`, `arp`) secara tersembunyi tanpa cmd window flashing.
*   **Windows Setup Installers:** Build Free & Pro installer yang memisahkan folder program dan writable LOCALAPPDATA.
*   **Midtrans Licensing Workflow Design:** Alur eksekusi asinkron website-to-desktop untuk lisensi Professional (terdokumentasi, siap implementasi teknis web).

### 2.2 Active Features (Sedang Dijalankan/Simulasi)
*   **Pulse Engine Worker Thread:** Polling metrics asinkron ke API MikroTik RouterOS (real untuk visualisasi dashboard utama, mock/simulasi untuk filter lanjutan).
*   **Local Network Sweeps:** Scan ARP and neighbor discovery (MNDP) untuk memetakan IP terdekat secara lokal-first.

### 2.3 Pending Features (Belum Diimplementasikan/Mocked)
*   **Network & Advanced Write Actions:** Penulisan konfigurasi (VLAN creation, Bridge management, Firewall rules, Queue limits) ke RouterOS API rill (saat ini masih visual mockup).
*   **Auto-Updater System:** Sistem pembaruan otomatis (saat ini user harus menginstal installer baru secara manual untuk menimpa biner lama).

---

## 3. KNOWN ISSUES (MASALAH TERIDENTIFIKASI)

1.  **Windows Defender SmartScreen False-Positive:** File installer (`.exe`) dicurigai Windows SmartScreen karena tidak ditandatangani sertifikat digital berbayar (Microsoft Authenticode Certificate).
2.  **Manual License Provisioning:** Penerbitan lisensi komersial/founder/beta memerlukan intervensi manual developer menggunakan skrip `issue_license.py` karena belum terhubung ke webhook otomatis Midtrans.

---

## 4. TECHNICAL DEBT STATUS
*   **TD-001 (Hardcoded Version):** CLOSED
*   **TD-003 (Build Cache Cleanup):** CLOSED
*   **TD-004 (Centralized Logging):** CLOSED
*   **TD-002 (Thread Lifecycle):** CLOSED
*   **TD-005 (Refactor UI System):** DO NOT TOUCH
*   **TD-006 (Testing Framework):** POST FOUNDER
*   **TD-007 (Midtrans Integration):** POST FOUNDER

---

## 5. RECENTLY COMPLETED SPRINTS
*   Linux Distribution Foundation
*   Release Standardization
*   GitHub Pages Preparation
*   Technical Debt Audit
*   Technical Debt Batch 1
*   Batch 1 Verification
*   Project OS Synchronization & Release Readiness Audit
*   Directory Structure Finalization & Terminal/Zombie Bug Consolidation (Root Merged)
*   Sprint 8 — Founder & Website Release Readiness (Selesai, situs web siap dengan integrasi Google Form & Gmail)

---

## 6. NEXT PRIORITY (PRIORITAS BERIKUTNYA)
1. **Sprint 9 — Closed Beta Campaign**:
   - Distribusi biner rilis beta kepada 10 tester terdaftar.
   - Pemantauan pelaporan bug dan integrasi feedback dari tester.
   - Triase berkas diagnostik dan perbaikan regresi jika ditemukan.
