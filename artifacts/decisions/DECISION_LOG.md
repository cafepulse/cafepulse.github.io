# DECISION LOG
### *Architectural & Design Decision Records — Locked: Juni 2026*

---

## [D-001] RSA-4096 Offline Licensing Mechanism

*   **Date:** 2026-06-05
*   **Decision:** Menggunakan verifikasi tanda tangan digital asimetris RSA-4096 dengan padding PSS untuk otentikasi lisensi klien Professional secara lokal tanpa koneksi internet.
*   **Reason:** Memenuhi manifesto *Local-First*. Traditional serial keys mudah di-keygen atau di-crack. Kriptografi kunci asimetris menjamin parameter lisensi (seperti Hardware ID dan Expiry Date) tidak dapat dimodifikasi oleh pengguna tanpa merusak tanda tangan digital.
*   **Alternatives Rejected:**
    *   *Online Licensing Server Check:* Ditolak karena melanggar prinsip offline-first dan ketergantungan server luar.
    *   *Symmetric Key Hashing (MD5/SHA256):* Ditolak karena algoritma verifikasi di sisi klien menyimpan secret key yang bisa di-reverse engineer.
*   **Impact:** Keamanan lisensi sangat tinggi. Namun, proses penerbitan lisensi menjadi semi-manual (Founder harus menjalankan skrip `issue_license.py` untuk menandatangani file `.licreq` dari pembeli).

---

## [D-002] SQLite dengan WAL (Write-Ahead Logging) Mode

*   **Date:** 2026-06-05
*   **Decision:** Menggunakan engine database SQLite3 lokal dengan mengaktifkan mode WAL (`PRAGMA journal_mode=WAL`).
*   **Reason:** SQLite bersifat serverless, portabel, dan sangat andal untuk penyimpanan lokal. Mode WAL memungkinkan operasi baca dari thread utama UI berjalan berbarengan dengan operasi tulis metrik dari background thread worker (Pulse Engine) tanpa memicu error locking.
*   **Alternatives Rejected:**
    *   *Client-Server DB (MySQL/PostgreSQL):* Ditolak karena membebani pengguna dengan instalasi service DB eksternal yang rumit.
    *   *Default SQLite Rollback Journal:* Ditolak karena memicu error `database is locked` saat polling interval tinggi.
*   **Impact:** I/O database lokal sangat cepat, aman, dan kompatibel dengan multi-threading.

---

## [D-003] Pemisahan Direktori Writable ke LOCALAPPDATA

*   **Date:** 2026-06-06
*   **Decision:** Memisahkan file biner aplikasi (read-only di `Program Files`) dengan database, logs, temp, dan file lisensi yang harus disimpan di direktori per-user Windows (`%LOCALAPPDATA%\CafePulse\`).
*   **Reason:** Sistem keamanan Windows UAC memblokir penulisan file apa pun ke folder `C:\Program Files\` oleh user biasa, yang menyebabkan aplikasi crash saat mencoba menulis log atau menyimpan database jika dijalankan tanpa hak administrator.
*   **Alternatives Rejected:**
    *   *Run as Administrator (Elevated UAC):* Ditolak karena melanggar best practices keamanan OS Windows.
    *   *Registry Storage:* Ditolak karena mempersulit backup manual database oleh pengguna.
*   **Impact:** Aplikasi boot bersih tanpa Windows permission dialog, database dan log aman dari proteksi folder sistem.

---

## [D-004] Centralized Restructuring (Level 3 to Level 2)

*   **Date:** 2026-06-21
*   **Decision:** Menghapus folder bertingkat Level 3 (`CafePulse/CafePulse/CafePulse`) dan memusatkan seluruh file ke Level 2 (`CafePulse/CafePulse`) dengan subfolder terisolasi (`Project`, `website`, `exports`, `license_generator`, `artifacts`).
*   **Reason:** Struktur bertingkat pasif menyebabkan kerancuan source code aktif, duplikasi file, dan kebingungan developer tunggal maupun AI asisten dalam menentukan Single Source of Truth (SSOT).
*   **Alternatives Rejected:**
    *   *Mempertahankan Nested Layout:* Ditolak karena resiko kesalahan kompilasi and kebocoran file privat ke repositori publik sangat tinggi.
*   **Impact:** Workspace menjadi sangat rapi, file-file terpisah sesuai fungsinya, dan pipeline kompilasi/build menjadi terprediksi dan stabil.

---

## [D-005] Offline Subnet Detection Fallback Chain

*   **Date:** 2026-06-21
*   **Decision:** Mengimplementasikan rantai deteksi subnet 6-tahap (6-stage local subnet fallback chain) yang berjalan secara lokal untuk menemukan subnet mask dan IP gateway pengguna tanpa bergantung pada ping server eksternal (seperti `8.8.8.8`).
*   **Reason:** Memastikan fitur Network Sweeper / ARP Scanner tetap berfungsi 100% saat komputer klien offline (tidak terkoneksi ke internet) tetapi terhubung ke LAN/WLAN. Metode lama menggunakan koneksi UDP dummy ke `8.8.8.8` akan gagal total dalam kondisi offline, menyebabkan scanner melaporkan "Device Found = 0".
*   **Alternatives Rejected:**
    *   *Hardcoded Subnet (e.g., always scan 192.168.1.0/24):* Ditolak karena banyak router menggunakan subnet default yang berbeda (192.168.88.0/24, 10.0.0.0/24, dll.).
    *   *System Command Only (e.g., subprocess parsing of ipconfig):* Dijadikan salah satu rantai fallback tetapi bukan metode utama karena parsing output teks commands bergantung pada bahasa sistem Windows (id-ID, en-US, dll.) yang rentan error.
*   **Impact:** ARP scanning menjadi sangat andal dan robust dalam berbagai skenario jaringan (online, offline, dual-homed, custom subnets).

---

## [D-006] Strict Clean Build Directory Sweeps

*   **Date:** 2026-06-21
*   **Decision:** Mengharuskan penghapusan penuh folder cache build (`Project/build/` dan `Project/dist/`) sebelum menjalankan proses kompilasi PyInstaller.
*   **Reason:** Mencegah terjadinya konflik runtime akibat penggunaan kembali (reuse) berkas loader cache (`pyimod02_importers.pyc` lama) yang tidak kompatibel dengan hook runtime PyInstaller baru, yang memicu error `AttributeError` saat eksekusi `.exe`.
*   **Alternatives Rejected:**
    *   *Menggunakan opsi `--clean` PyInstaller saja:* Terkadang tidak sepenuhnya menghapus sisa file internal di platform Windows jika file terkunci atau terdistorsi. Penghapusan direktori secara manual/skrip terbukti lebih bersih dan aman.
*   **Impact:** Pipeline build stabil, waktu kompilasi sedikit lebih lama (~1 menit tambahan), namun menjamin binary yang dihasilkan 100% bebas dari distorsi cache.

---

## [D-007] Standardisasi Penamaan Rilis & Penanganan Founder Edition

*   **Date:** 2026-06-21
*   **Decision:** Menetapkan penamaan standard untuk berkas rilis stabil (`CafePulse_[Edition]_Setup.exe`, `CafePulse_[Edition]_Portable.zip`, `CafePulse_[Edition].AppImage`) dan tag rilis (`vX.Y.Z` untuk stabil, `vX.Y.Z-beta.N` untuk beta). Untuk **Founder Edition**, diputuskan untuk menggunakan basis penamaan biner versi *Professional Stable* biasa (tanpa tag nama file terpisah) tetapi ditandai di tingkat metadata, visual badge UI, dan tipe parameter lisensi kriptografis.
*   **Reason:** Memisahkan nama berkas biner khusus untuk "Founder Edition" secara fisik akan mengacaukan pembaruan otomatis (auto-updater) dan menambah kerumitan build pipeline (Inno Setup / PyInstaller) secara tidak perlu. Tipe lisensi asimetris RSA-4096 sudah cukup kuat membedakan pengguna Founder secara lokal.
*   **Alternatives Rejected:**
    *   *Membuat build terpisah CafePulse_Founder_Setup.exe:* Ditolak karena menambah overhead kompilasi ganda dan duplikasi kode rilis.
*   **Impact:** Build pipeline tetap sederhana (2 edisi: Free & Professional) sementara identitas Founder dijamin aman secara lisensi kriptografis.

---

## [D-008] Jalur Unduhan Publik Menggunakan GitHub Pages Releases Redirects

*   **Date:** 2026-06-21
*   **Decision:** Menggunakan repositori publik `cafepulse/cafepulse.github.io` sebagai hosting rilis binary publik untuk menghindari batasan akses dari repositori kode utama `youbellkey/CafePulse` yang bersifat privat.
*   **Reason:** Repositori kode utama bersifat privat demi keamanan IP produk, sehingga GitHub Actions / Releases di repositori tersebut memerlukan token otentikasi (PAT) untuk diunduh. Pengguna publik harus bisa mengunduh biner secara bebas tanpa token. Memanfaatkan repositori GitHub Pages publik sebagai jembatan rilis memungkinkan akses download langsung melalui `/releases/latest/download/` yang aman, andal, dan gratis.
*   **Alternatives Rejected:**
    *   *Menghosting biner di server VPS eksternal:* Ditolak karena menambah biaya operasional, ketergantungan downtime server, dan beban perawatan infrastruktur tambahan.
*   **Impact:** Pengguna dapat mengunduh aplikasi dengan kecepatan CDN GitHub tanpa autentikasi, sementara keamanan source code utama di repositori privat tetap terjaga.

---

## [D-009] Verifikasi Integritas Checksum Lintas Platform (SHA256SUMS)

*   **Date:** 2026-06-21
*   **Decision:** Setiap rilis akan secara otomatis memproduksi file manifest `SHA256SUMS.txt` berisi hash dari seluruh aset rilis. Proses kalkulasi ini diotomatisasi menggunakan skrip Python lintas platform agar menghasilkan output hash yang identik baik di Linux (CI) maupun Windows (local developer PC).
*   **Reason:** Menjamin integritas berkas rilis terhadap kemungkinan kerusakan data unduhan atau intervensi pihak ketiga (man-in-the-middle). Menggunakan utilitas native seperti `sha256sum` (Linux) atau `Get-FileHash` (Windows PowerShell) rentan terhadap perbedaan format spasi dan line endings (`LF` vs `CRLF`), sehingga skrip Python mandiri dipilih sebagai standarisasi.
*   **Alternatives Rejected:**
    *   *Kalkulasi manual:* Ditolak karena rentan kesalahan manusia (*human error*).
*   **Impact:** File manifest terstandarisasi selalu diproduksi secara konsisten untuk setiap rilis, memungkinkan verifikasi integritas oleh pengguna ahli.

---

## [D-010] Keseragaman Sistem Pembayaran & Lisensi Windows & Linux

*   **Date:** 2026-06-21
*   **Decision:** Memutuskan untuk menggunakan satu sistem lisensi kriptografis terpadu (RSA-4096) dan alur pembayaran website yang sama untuk pengguna Windows dan Linux.
*   **Reason:** Menjaga kesederhanaan model bisnis *local-first* CafePulse. Karena proses pembelian lisensi dan penerbitan key sepenuhnya diproses di website (terpisah dari client application), aplikasi desktop di Windows maupun Linux cukup menggunakan pustaka kriptografi Python (`cryptography` / RSA) yang sama untuk memvalidasi berkas lisensi `.lic` yang dibeli.
*   **Alternatives Rejected:**
    *   *Sistem pembayaran terpisah atau lisensi khusus Linux:* Ditolak karena menambah overhead perawatan ganda dan mempersulit administrasi pembelian bagi teknisi yang mengelola jaringan di lingkungan multi-OS.
*   **Impact:** Menghilangkan redundansi logika bisnis. Lisensi yang dibeli bersifat universal (dapat digunakan di platform Windows maupun Linux selama HWID dicocokkan saat pembuatan lisensi).

---

## [D-011] Technical Debt Batch 1 Closed

*   **Date:** 2026-06-22
*   **Decision:** Menutup siklus pengerjaan Technical Debt Batch 1 setelah audit dan implementasi terverifikasi.
*   **Status/Isi:**
    *   TD-001 (Hardcoded Version): Selesai
    *   TD-003 (Build Cache Cleanup): Selesai
    *   TD-004 (Centralized Logging): Selesai
    *   Verifikasi menunjukkan PASS tanpa ada regresi yang ditemukan pada sistem.

---

## [D-012] Pre-Founder Stabilization Entry

*   **Date:** 2026-06-22
*   **Decision:** Menaikkan status CafePulse dari Release Candidate (RC1.2) menjadi fase Pre-Founder Stabilization.
*   **Isi:** Fokus pengembangan utama sekarang berpindah dari pembangunan fitur-fitur baru ke arah stabilitas, penulisan dokumentasi, kesiapan rilis (release readiness), serta materi onboarding khusus untuk Founder.

---

## [D-013] Midtrans Integration & Offline Licensing Flow Architecture

*   **Date:** 2026-06-22
*   **Decision:** Menetapkan arsitektur aliran checkout (pembelian lisensi) menggunakan Midtrans sebagai payment gateway di website, dikombinasikan dengan sistem pembuatan lisensi (RSA) secara asinkron/backend.
*   **Reason:** Aplikasi CafePulse adalah *Local-First* dan tidak boleh melakukan kontak langsung ke Midtrans atau server lisensi manapun dari dalam aplikasi desktop. Oleh karena itu, otorisasi transaksi dipindah ke website.
*   **Flow:**
    1. Pengguna mengekstrak HWID dari aplikasi desktop (menghasilkan file `.licreq`).
    2. Pengguna mengunggah `.licreq` di website CafePulse dan membayar via Midtrans.
    3. Setelah sukses (Webhook Midtrans), backend server (atau founder manual) akan menggunakan `issue_license.py` untuk menandatangani HWID dengan Private Key RSA-4096.
    4. File `license.lic` yang telah terenkripsi dikirim via email.
    5. Pengguna mengimpor file `license.lic` ke aplikasi desktop. Aplikasi memverifikasi *Signature* tanpa koneksi internet.
*   **Alternatives Rejected:**
    *   *In-App Checkout (Membuka frame Midtrans di dalam PyQt6):* Ditolak karena melanggar prinsip *Local-First* (aplikasi butuh akses ke web eksternal) dan mempersulit arsitektur aplikasi offline.
*   **Impact:** Memastikan keamanan lisensi sangat tinggi dan aplikasi desktop benar-benar tidak membutuhkan internet. Implementasi Midtrans dapat ditunda atau dilakukan independen dari siklus rilis aplikasi desktop.

---

## [D-014] Founder Release Readiness Initiated

*   **Date:** 2026-06-22
*   **Decision:** Memulai **Sprint 8 — Founder Release Readiness**. Menunda seluruh _Feature Development_, modifikasi _engine_, database, dan pelunasan sisa *Technical Debt*. Fokus utama dialihkan pada *Founder Experience* (Onboarding, Panduan Instalasi, dan Pelaporan Bug).
*   **Reason:** Aplikasi telah stabil. Hambatan terbesar untuk pelepasan Beta/Founder saat ini adalah ketiadaan panduan penggunaan, template laporan masalah yang standar, serta risiko kebingungan pengguna awal (_friction_) saat mengunduh dan mengatur aplikasi untuk pertama kalinya.
*   **Impact:** Menghasilkan _Founder Release Checklist_ komprehensif, panduan instalasi mendalam, skenario _first-launch_, pedoman pelaporan _bug/feedback_, dan evaluasi kesiapan rilis. Mencegah timbulnya impresi negatif akibat _onboarding_ yang buruk.

---

## [D-015] GitHub Pages Root Directory Restructuring

*   **Date:** 2026-06-22
*   **Decision:** Mengembalikan seluruh aset situs web statis (`.html`, `css/`, `js/`, `assets/`, `lang/`) ke dalam *root directory* repositori `cafepulse.github.io` dan menghapus sub-direktori `website/`.
*   **Reason:** Terjadi konflik dan kesalahan publikasi pada GitHub Pages. Arsitektur GitHub Pages mengharuskan *file* `index.html` dan aset terkait berada langsung di *root* (`/`) agar situs dapat dirender secara otomatis di *domain* publik tanpa konfigurasi *build step* tambahan. Pemindahan ke dalam direktori `website/` (pada *Sprint 3*) menyebabkan *broken links* dan bentrok dengan *commit* yang masuk dari *remote*.
*   **Impact:** Menghindari kebingungan dalam satu tim terkait di mana *file* web harus diedit. Seluruh halaman HTML kini dikelola secara *flat* di *root* repositori. Ruang lingkup aplikasi *Python* dan aset statis web berbaur di direktori yang sama, namun telah dikategorikan secara logis oleh penamaan _file_ (seperti `core/`, `modes/`, dsb. untuk aplikasi, dan `css/`, `js/`, `*.html` untuk situs web).

---

## [D-016] Beta Tester & Founder Registration Reverted to Google Forms

*   **Date:** 2026-06-22
*   **Decision:** Menghapus dan menonaktifkan formulir registrasi kustom (*Website Form*) pada halaman Beta Tester dan Founder. Pendaftaran dikembalikan sepenuhnya menggunakan platform Google Forms yang ada sebelumnya.
*   **Reason:** Evaluasi ulang terhadap konteks CafePulse (solo developer, tanpa tim support/backend khusus). Pembuatan formulir *website custom* berisiko menambah *technical debt*, kompleksitas pemeliharaan *server/API*, titik kegagalan (*Point of Failure*), dan kelemahan keamanan (*spam*). Google Form sudah terbukti stabil, gratis, anti-spam bawaan, dan sudah terintegrasi lancar ke Discord *webhook* melalui Spreadsheet. Keputusan ini selaras dengan filosofi CafePulse untuk menghindari *over-engineering*.
*   **Impact:** Menghapus elemen `beta-report-form` dan skrip pendukung dari `beta.html` dan `founder.html`. Halaman tersebut kini hanya menyajikan *Call-to-Action* (CTA) yang menautkan pengunjung langsung ke Google Form. Beban *maintenance* pada *front-end* berkurang drastis.


---

## [D-017] Artifact Generator Strict Compliance (Fail Fast & Verbatim Copy)

*   **Date:** 2026-06-22
*   **Decision:** Menerapkan aturan strict *Fail Fast*, *Case-Insensitive Matching*, dan penyisipan penanda *GENERATED_ARTIFACT = TRUE* pada skrip generator Project OS.
*   **Reason:** Saat mengompilasi ZIP artefak untuk AI eksternal, sering terjadi insiden *Documentation Hallucination* di mana generator (LLM) membuat _placeholder_ dokumen inti (seperti PROJECT_STATE.md) karena gagal menemukannya di direktori yang benar akibat *case-sensitivity* atau kegagalan *discovery*. Jika dokumen _placeholder_ menimpa dokumen asli, Project OS akan hancur dan kehilangan memori state.
*   **Impact:** Memastikan generator artefak harus menyalin file secara verbatim dari rtifacts/. Jika ia memutuskan untuk melakukan generate *fallback* karena file benar-benar tidak ada, ia harus menyisipkan penanda eksplisit. Jika pembuatan *fallback* berisiko menimpa file eksisting, skrip harus langsung *Crash/Fail Fast*.

---

## [D-018] Graceful Thread Shutdown Architecture (No Terminate)

*   **Date:** 2026-06-22
*   **Decision:** Melarang secara mutlak penggunaan pemanggilan QThread.terminate() dan internal self.wait() di dalam daur hidup (*lifecycle*) worker *PyQt6*. Mengadopsi arsitektur asinkron *Collective Wait* pada Main Thread.
*   **Reason:** Penyelesaian isu P0 TD-002 (Shutdown Zombie Process). Penggunaan worker.terminate() secara paksa membunuh OS thread, menyebabkan blok inally diabaikan, koneksi *socket* RouterOS menggantung, _database lock_ .wal SQLite terabaikan, dan subprocess (seperti *ping*) menjadi zombie. Selain itu, fungsi stop() pada _worker_ sebelumnya mengandung self.wait(5000), yang mengunci (*block*) Main Thread selama 5 detik dikali jumlah _worker_.
*   **Impact:** Penutupan CafePulse sekarang dikendalikan oleh *Main Window* yang memberikan sinyal stop() asinkron secara serentak ke semua _worker_, lalu melakukan polling QApplication.processEvents() selama maksimal 5 detik. Pekerja yang gagal berhenti tidak akan diputus paksa (*terminate*), membiarkan OS merebut kembali memori secara alami setelah sys.exit() tanpa merusak integritas *database* atau meninggalkan *socket* dalam keadaan *dangling*.

---

## [D-019] Locked Project Directory Structure (Root Merged)

*   **Date:** 2026-06-22
*   **Decision:** Menghapus folder `Project/` secara permanen dan menyatukan seluruh kode aplikasi Python (`core/`, `ui/`, `modes/`, `main.py`) langsung di direktori *root* bersamaan dengan aset website statis (`assets/`, `css/`, `js/`, `*.html`).
*   **Reason:** AI Assistants secara konsisten mengalami kebingungan (*hallucination/conflict*) antara direktori `Project/` dan root. Beberapa agen menerapkan *bug fixes* pada file duplikat yatim-piatu di root karena menyangka kode berada di sana berdasarkan [D-015], sehingga hasil kompilasi dari `Project/` kehilangan perbaikan krusial (seperti perbaikan *zombie process* dan *terminal flashing*).
*   **Impact:** Struktur direktori terkunci pada arsitektur *Flat-Root*. Setiap perbaikan atau modifikasi fitur wajib dilakukan langsung di root. Segala bentuk duplikasi folder `Project/` di masa depan sangat dilarang keras.

---

## [D-020] Founder Program Deferred

*   **Date:** 2026-06-22
*   **Decision:** Menunda pembukaan program pembelian lisensi Founder (Founder Program) pada website publik dan mengganti seluruh tombol aksi pembelian/pendaftaran dengan penanda "Coming Soon".
*   **Reason:** Fokus saat ini dialihkan sepenuhnya pada validasi stabilitas dan keandalan sistem melalui program Beta Tester (Closed Beta) yang lebih terkontrol, sebelum meluncurkan penjualan komersial.
*   **Alternatives Rejected:** Membiarkan link pembelian aktif dengan formulir manual.
*   **Impact:** Mengamankan ekspektasi pengguna awal dan memberikan waktu bagi developer untuk mematangkan build rilis.

---

## [D-021] Website Bug Reporting & Beta Tester Registration

*   **Date:** 2026-06-22
*   **Decision:** Mengganti alur registrasi Beta Tester kustom dengan tautan eksternal ke Google Forms (`forms.gle/VPwQ3jRBySbCEvKX7`) untuk pendaftaran dan pelaporan bug. Pada halaman Beta, disediakan pula akses cepat ke Gmail (memanfaatkan template link Gmail dinamis) serta opsi "Copy Email" untuk kemudahan pengiriman log manual.
*   **Reason:** Memangkas kompleksitas pemeliharaan backend email/formulir kustom di server statis GitHub Pages dan menghindari risiko spamming serta kegagalan pengiriman log biner/gambar berukuran besar.
*   **Alternatives Rejected:** Menggunakan service FormSubmit secara langsung. Ditolak karena batasan ukuran file log dan ketergantungan email aktivasi eksternal.
*   **Impact:** Alur pendaftaran dan pelaporan bug menjadi sangat stabil, mudah dikelola secara manual oleh developer via spreadsheet Google Forms, dan bebas dari overhead server side.

