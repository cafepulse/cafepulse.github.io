# TECHNICAL DEBT AUDIT REPORT
**Phase:** Release Candidate Stabilization (RC1.2 / 1.1.0-alpha.1)

---

## Debt ID: TD-001
### Category: Build / Release
### Location: 
- `main.py`, `.iss` installer scripts, `settings.json`, `about_page.py`, `sidebar.py`
### Description: 
Versi aplikasi (seperti `1.1.0-alpha.1` atau `RC1.2`) saat ini di-*hardcode* di berbagai file sumber, file konfigurasi, dan skrip *installer* alih-alih dikelola dari satu titik referensi (*Single Source of Truth*).
### Root Cause: 
Ketiadaan modul manajemen versi terpusat (seperti `version.py`) dan penggunaan praktik *manual version bumping* selama pengembangan awal.
### Risk Level: HIGH
### Business Impact: 
- **Beta Users:** Risiko pengguna melaporkan bug dengan informasi versi yang salah/berbeda antara UI dan file log.
- **Maintainability:** Pengembang dapat lupa memperbarui versi di salah satu lokasi, menyebabkan ketidakkonsistenan *installer* dengan biner *executable*.
### Regression Risk: LOW
### Estimated Fix Size: S
### Recommended Timing: FIX BEFORE FOUNDER RELEASE
### Justification: 
Ketidakkonsistenan pelaporan versi akan sangat menghambat proses triase *bug* selama fase *Closed Beta*. Perbaikannya sangat terisolasi (hanya pemusatan variabel dan *injection* ke *build script*).
### Resolution Status: 
**CLOSED** (Selesai pada Sprint sebelumnya, menggunakan modul `version.py` tersentralisasi).

---

## Debt ID: TD-002
### Category: Architecture / UI
### Location: 
- `modes/*/*_worker.py`, `core/mikrotik/polling_worker.py`
### Description: 
*Thread lifecycle management* untuk proses asinkron (seperti MikroTik API polling dan *network sweep*) menggunakan PyQt6 `QThread` namun belum menerapkan mekanisme penghentian atau pelepasan memori (*teardown/cleanup*) yang aman (`quit()`, `wait()`, `terminate()`).
### Root Cause: 
Penanganan *signals/slots* dan penutupan aplikasi yang belum sempurna saat interupsi paksa atau aplikasi ditutup tiba-tiba.
### Risk Level: HIGH
### Business Impact: 
- **Beta & Professional Users:** Aplikasi berpotensi *hang* (freeze) saat ditutup, atau meninggalkan proses *zombie* di latar belakang yang memakan memori CPU/RAM pengguna secara diam-diam.
### Regression Risk: HIGH
### Estimated Fix Size: M
### Recommended Timing: FIX BEFORE FOUNDER RELEASE
### Justification: 
Isu *zombie thread* akan merusak pengalaman pengguna dan menyebabkan komplain performa PC (*resource leak*). Walaupun regresi berisiko, isu ini harus ditangani sebelum aplikasi menyentuh komputer klien nyata.
### Resolution Status: 
**CLOSED** (Selesai di Sprint 7.5. Diatasi sepenuhnya lewat arsitektur *GracefulShutdownMonitor* (D-018) dan meratakan *root folder* (D-019) untuk mencegah regresi bug kembali).

---

## Debt ID: TD-003
### Category: Build / Release
### Location: 
- `build.py`, `scripts/` (Windows `.bat` dan Linux CI)
### Description: 
Skrip otomasi *build* PyInstaller belum sepenuhnya membersihkan *cache* sisa kompilasi (`build/`, `dist/`, `.spec` sementara) secara agresif sebelum melakukan kompilasi versi rilis yang baru.
### Root Cause: 
Pendekatan kompilasi inkremental saat fase *rapid prototyping* tanpa siklus `clean sweep` yang ketat.
### Risk Level: HIGH
### Business Impact: 
- **Maintainability & Beta Users:** Risiko terjadinya *cache poisoning* dari *importer* PyInstaller lama (contoh: modul usang terbawa masuk ke rilis baru), yang menyebabkan aplikasi gagal dijalankan setelah instalasi.
### Regression Risk: LOW
### Estimated Fix Size: S
### Recommended Timing: FIX BEFORE FOUNDER RELEASE
### Justification: 
Penambahan perintah `rmdir /s /q build dist` atau pembersihan modul yang *stale* di awal skrip rilis sangat esensial untuk menjamin biner rilis bersih.
### Resolution Status: 
**CLOSED** (Pembersihan _cache_ build terotomatisasi di `build.py` dan `build-linux.yml`).

---

## Debt ID: TD-004
### Category: Architecture / Documentation
### Location: 
- Tersebar di berbagai modul (`core/` dan `ui/`)
### Description: 
Logika penulisan log ganda dan absennya standardisasi persisten (*duplicate & missing logging*). Beberapa modul menggunakan `print()`, sementara modul lainnya menggunakan `logging` Python, namun tidak disentralisasi ke dalam sistem file log yang persisten untuk *bug reporting*.
### Root Cause: 
Pengembangan iteratif secara paralel tanpa modul *Logger* inti yang membungkus semua interaksi file.
### Risk Level: MEDIUM
### Business Impact: 
- **Maintainability:** Jika aplikasi *crash* di mesin *beta tester*, *developer* akan kesulitan melacak akar masalah (seperti *stack trace* enkripsi RSA yang gagal atau API error).
### Regression Risk: LOW
### Estimated Fix Size: M
### Recommended Timing: FIX BEFORE FOUNDER RELEASE
### Justification: 
Agar pengujian *Beta* efektif, sistem pelaporan kesalahan (log file) mutlak dibutuhkan.
### Resolution Status: 
**CLOSED** (Sistem _logging_ tersentralisasi dan persisten telah diimplementasi di seluruh arsitektur *Project OS*).

---

## Debt ID: TD-005
### Category: UI
### Location: 
- `ui/widgets/devices_page.py`, `ui/widgets/sidebar.py`
### Description: 
Komponen UI yang berukuran besar (*oversized widgets*) memikul dua beban komputasi sekaligus: mengatur tampilan (GUI) dan mengambil/mengolah data dari _Network Layer_ atau *Database*.
### Root Cause: 
*Tight coupling* antara lapisan Presentasi (PyQt6) dan lapisan Logika Bisnis (*Business Logic/Data Fetching*).
### Risk Level: LOW
### Business Impact: 
- **Maintainability:** Menyulitkan pengujian GUI secara otomatis dan membuat kode sulit dimodifikasi jika ada penambahan fitur di masa depan. Tidak berdampak langsung ke pengguna.
### Regression Risk: MEDIUM
### Estimated Fix Size: L
### Recommended Timing: DO NOT TOUCH
### Justification: 
Aplikasi masih berfungsi normal secara visual. Merombak UI (*refactoring* MVC/MVVM) di fase stabilisasi sangat berbahaya dan berisiko menciptakan regresi (*bug* tampilan baru).

---

## Debt ID: TD-006
### Category: Licensing / Website
### Location: 
- `license_generator/issue_license.py`, Integrasi Payment Gateway
### Description: 
Pembuatan lisensi komersial belum diotomatisasi secara penuh melalui *webhook* server *backend* dari Midtrans.
### Root Cause: 
CafePulse dirancang sebagai aplikasi *Local-First* tanpa *cloud backend* besar, sehingga otorisasi transaksi masih terputus antara *website* (pembayaran) dan *developer* (penerbitan manual).
### Risk Level: MEDIUM
### Business Impact: 
- **Founder Program:** *Founder* (developer) harus menerbitkan kunci `.lic` secara manual dan mengirimkannya via email kepada setiap pelanggan. Menimbulkan perlambatan operasional jika skala pengguna membesar.
### Regression Risk: LOW
### Estimated Fix Size: L
### Recommended Timing: FIX AFTER FOUNDER RELEASE
### Justification: 
Untuk skala *Beta Testing* (terbatas), penerbitan kunci secara manual via skrip Python masih sangat bisa ditoleransi dan diterima (Bahkan ini adalah pendekatan paling aman di tahap awal).

---

## Debt ID: TD-007
### Category: Database / MikroTik
### Location: 
- `ui/widgets/compatibility_page.py`, Modul Jaringan Lanjutan
### Description: 
Beberapa fitur konfigurasi penulisan ke RouterOS (VLAN creation, Bridge management, Firewall rules) masih berbentuk struktur *mock* UI dan data *dummy*.
### Root Cause: 
Sesuai perencanaan *Roadmap*, fitur manajemen tulis API dikesampingkan sementara untuk mengejar stabilitas fondasi observasi dan *polling*.
### Risk Level: LOW
### Business Impact: 
- **Professional Users:** Ekosistem kontrol RouterOS terasa kurang lengkap di tahap Beta.
### Regression Risk: LOW
### Estimated Fix Size: XL
### Recommended Timing: FIX AFTER FOUNDER RELEASE
### Justification: 
Tidak relevan dengan uji coba stabilitas dasar. Fitur-fitur lanjutan akan diluncurkan bertahap melalui iterasi pasca-rilis.
