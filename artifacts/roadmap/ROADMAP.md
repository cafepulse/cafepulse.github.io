# CAFEPULSE ROADMAP
### *Product Direction, Milestones & Feature Priorities — Locked: Juni 2026*

---

## 1. VERSIONING STATE

*   **Current Version:** `1.0.0-RC1.2` / `1.1.0-alpha.1` (Linux CI and AppImage Stabilized)
*   **Next Milestone Version:** `1.0.0-Beta` (Public/Closed Discord Beta Testing)
*   **Target Stable Version:** `1.0.0.0` (Stable Commercial Release)

---

## 2. ACTIVE SPRINTS ROADMAP

### COMPLETED SPRINTS
*   **Sprint 1 — Linux Distribution Foundation:** Selesai
*   **Sprint 2 — Release Standardization:** Selesai
*   **Sprint 3 — GitHub Pages Preparation:** Selesai
*   **Sprint 4 — Technical Debt Audit:** Selesai
*   **Sprint 5 — Technical Debt Batch 1:** Selesai
*   **Sprint 6 — Batch 1 Verification:** Selesai
*   **Sprint 7 — Project OS Synchronization:** Selesai
*   **Sprint 7.5 — Directory Consolidation & P0 Bugfixes:** Selesai (Flat-Root Repository, Zombie Process Fix, Terminal Flashing Fix)
*   **Sprint 8 — Founder & Website Release Readiness:** Selesai (Menyusun panduan, onboarding, instalasi, audit rilis, dan revert pendaftaran ke Google Form)

### ACTIVE SPRINT
*   **Sprint 9 — Closed Beta Campaign:** Sedang berjalan (Distribusi biner rilis beta, monitoring pelaporan bug, triase log, dan pengumpulan feedback).

### NEXT SPRINT (PENDING DECISION)
Akan ditentukan sesuai temuan dan feedback dari Closed Beta Campaign.

---

## 3. TAHAPAN EKSEKUSI TEKNIS (PHASE ROADMAP)

### PHASE 1 — FOUNDATION STABILIZATION (STATUS: LULUS ✓)
*   Pembangunan **Pulse Engine** (Event System & Multi-threaded Task Management).
*   Database SQLite lokal (`cafepulse.db`) dengan mode WAL untuk stabilitas.
*   Structured Logging & Error Handling (Global Exception Handler & Crash Logger).
*   Safe Mode & Auto Recovery system.

### PHASE 2 — SMART CONNECTION PLATFORM (STATUS: SELESAI ✓)
*   Neighbor Discovery & Local Network sweeps.
*   Connection Profiles & Vault terenkripsi.
*   Connection Quality & Auto Reconnect mechanism.

### PHASE 3 — OPERATIONS & LICENSING FREEZE (STATUS: SELESAI ✓)
*   **Hotspot Manager:** Active users monitoring, daily stats.
*   **Voucher Generator (Core Premium Feature):** Bulk generation up to 500 codes, custom speed limits, PDF template export layouts.
*   **DHCP Lease Center:** Lease list, Release, & IP reservation.
*   **Backup Manager:** Automated config backup and versioning.
*   **RSA Licensing Module:** RSA-4096 signature verification, HWID binding, anti-tampering PyInstaller obfuscation.
*   **Centralized Reorganization:** Eliminating Level 3 folders and establishing Project OS framework.

### PHASE 4 — NETWORK PLATFORM (STATUS: RENCANA BERIKUTNYA 📅)
*   **Network Overview:** WAN, DNS, DHCP, PPP status panel.
*   **Smart Troubleshooting:** Latency, packet loss checks (Internet Health Score 0-100%).
*   **VLAN Creation Wizard:** Secure 4-step virtual interface setup wizard.
*   **IP/DNS/Bridge/PPP Managers:** Core network configurations from UI.
*   **Network Topology View:** Graphical link mapping (Router ➜ Switch ➜ AP ➜ Client).

### PHASE 5 — ADVANCED OPERATIONS & OFFLINE AI (STATUS: VISI MASA DEPAN 🔮)
*   **Firewall & NAT Workspace:** Rule filtering & Port Forwarding manager UI.
*   **Bandwidth Queue Controller:** PCQ/Simple Queue bandwidth visual controller.
*   **Automation Center:** Action triggers based on network alerts.
*   **Offline AI Analytics:** Local machine-learning model (no cloud) to detect network anomaly signatures.

---

## 4. FEATURE PRIORITIES (PRIORITAS FITUR)

| Prioritas | Fitur | Target Rilis | Deskripsi |
|---|---|---|---|
| **P0** | Founder Release Readiness | Pre-Founder | Finalisasi instalasi, onboarding, dokumentasi, dan installer untuk rilis Founder pertama. |
| **P1** | Website Polish & Changelog | Beta Launch | Pembaruan layout download, pricing, dan GitHub Pages repository. |
| **P2** | Closed Beta Campaign | Beta Launch | Distribusi build ke tester komunitas. |
| **P3** | Network Workspace API | v1.0.0.0 Stable | Menyambungkan mock UI Network (VLAN, IP, DNS) ke RouterOS API rill. |
| **P4** | Advanced Workspace API | v1.0.0.0 Stable | Menyambungkan mock UI Firewall/Queue ke RouterOS API rill. |
| **P5** | Fleet Dashboard | Post v1.0.0.0 | Pemantauan multi-routerboard secara simultan dari satu dasbor. |

---

## 5. LONG TERM GOAL (TUJUAN JANGKA PANJANG)
Menghasilkan ekosistem pengelolaan jaringan MikroTik lokal terlengkap di Indonesia yang berjalan 100% tanpa cloud, serta menjadi basis perangkat lunak berlisensi Perpetual/Lifetime yang menguntungkan bagi teknisi dan founder tunggal.
