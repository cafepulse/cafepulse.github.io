# CURRENT SPRINT
### *Active Sprint Focus: Sprint 8 — Founder Release Readiness*

---

## 1. SPRINT GOAL
Memastikan seorang Founder User yang belum pernah melihat CafePulse sebelumnya dapat secara mandiri (tanpa bantuan developer): menemukan website, memahami produk, mengunduh, menginstal, mengaktifkan lisensi, menjalankan aplikasi, memahami fitur, serta melaporkan bug dan feedback dengan format yang benar.

---

## 2. ACTIVE TASKS (STATUS PELAKSANAAN)

- [x] **Project OS Update**
  - [x] Sinkronisasi `ROADMAP.md`, `PROJECT_STATE.md`, `DECISION_LOG.md`, `CURRENT_SPRINT.md`.
  - [x] Tambahkan D-014 (Founder Release Readiness Initiated).
- [x] **Founder Onboarding & Testing Guides**
  - [x] Buat `FOUNDER_RELEASE_CHECKLIST.md` (Checklist final kesiapan rilis).
  - [x] Buat `INSTALLATION_GUIDE.md` (Instruksi detail instalasi OS Windows & Linux).
  - [x] Buat `FIRST_LAUNCH_GUIDE.md` (Pengenalan Workspace & fitur inti).
  - [x] Buat `FOUNDER_TESTING_GUIDE.md` (Arahan dan panduan pemberian feedback).
- [x] **Reporting Templates**
  - [x] Buat `BUG_REPORT_TEMPLATE.md` (Format standar log, reproduksi, OS).
  - [x] Buat `FEEDBACK_TEMPLATE.md` (Format standar UX/Performa/Fitur).
- [x] **Audits & Verification**
  - [x] Audit halaman Website (Download, Pricing, Docs, Discord).
  - [x] Simulasikan alur "Founder Experience".
  - [x] Terbitkan `RELEASE_READINESS_REPORT.md` (Audit akhir kesiapan rilis).
- [x] **Beta Tester Registration Revert**
  - [x] Audit `BETA_TESTER_REGISTRATION_AUDIT.md`.
  - [x] Ganti formulir dengan Google Form link di semua halaman HTML.
  - [x] Update Project OS (`D-016`).
- [x] **P0 Critical Mission (Interrupt)**
  - [x] Audit 10 Fase daur hidup Thread & Subprocess (TD-002).
  - [x] Implementasi Patch Plan (Collective Wait, hapus `terminate()`, kill zombie `ping`).
  - [x] Update Project OS (`D-017`, `D-018`).
- [x] **P0 Critical Mission 2 (Interrupt)**
  - [x] Finalisasi struktur direktori: Flatten `Project/` ke dalam root repository (D-019).
  - [x] Sinkronisasi ulang bug fix (Terminal Flash & Zombie Thread) ke dalam direktori root.
  - [x] Update `build.py` & `.github/workflows` agar mendukung root-based execution.

---

## 3. TASK BOARD

| In Progress | Blockers | Next Action |
|---|---|---|
| *Tidak ada* | *Tidak ada* | Seluruh panduan, template, audit rilis, dan revert pendaftaran telah diselesaikan dan dirilis. |

---

## 4. DEFINITION OF SPRINT DONE
Sprint ini dinyatakan selesai apabila:
1. Seluruh panduan dan kerangka umpan balik (onboarding, installation, first-launch, bug, feedback) telah didokumentasikan dengan rapi.
2. Laporan audit kesiapan rilis (Release Readiness Report) telah diproduksi.
3. Tidak ada _Feature Development_ atau perubahan arsitektur aplikasi (engine, database, worker) di sepanjang sprint.
