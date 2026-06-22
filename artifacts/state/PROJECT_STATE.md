# PROJECT STATE
### *Current System State & Technical Debt — Locked: Juni 2026*

---

## 1. CURRENT STATUS
CafePulse saat ini berada pada fase **Pre-Founder Stabilization**. 
Fokus pengembangan utama adalah **Founder Experience**, dokumentasi kelancaran onboarding, dan penyediaan _Feedback Loop_ yang terstruktur, bukan _Feature Development_.

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

---

## 6. NEXT PRIORITY (PRIORITAS BERIKUTNYA)
1. **Sprint 8 — Founder Release Readiness (ACTIVE)**: Memastikan pengalaman pengguna pertama (Founder Onboarding, Installation, Licensing) terdokumentasi dan berjalan mulus tanpa bantuan developer.
   - *Update Berjalan:* Semua aset _Website_ statis GitHub Pages telah dipindahkan dari folder `website/` kembali ke _Root Directory_ untuk memulihkan _broken links_ dan mengizinkan `cafepulse.github.io` merender _index_ secara otomatis. Artefak dan Git telah disinkronisasikan sepenuhnya.
   - *Update Berjalan:* Registrasi *Beta Tester* dan pendaftaran *Founder* via *website form kustom* telah dihapus dan diganti secara penuh menjadi CTA yang mengarah ke ekosistem **Google Form** yang lebih teruji, demi mengurangi *technical debt* (*D-016*).
