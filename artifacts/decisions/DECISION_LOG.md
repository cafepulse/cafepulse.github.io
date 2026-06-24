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

---

## [D-022] Inisiasi Discovery Fase Proposal Kolaborasi NanangMrk

*   **Date:** 2026-06-24
*   **Decision:** Menetapkan dokumen Proposal Project State (`PROPOSAL_STATE_NANANGMRK.md`) sebagai Single Source of Truth (SSOT) sebelum menyusun draft proposal, email, atau materi pemasaran kepada NanangMrk.
*   **Reason:** Memastikan seluruh materi penjangkauan (*outreach*) didasarkan pada realitas teknis CafePulse (local-first, one-time purchase) dan bebas dari asumsi tidak terverifikasi (*UNKNOWN*). Menghindari risiko salah penempatan (*positioning*) serta mengamankan kredibilitas produk di mata tokoh edukasi MikroTik Indonesia.
*   **Alternatives Rejected:** Langsung menghubungi NanangMrk melalui pesan ulasan sponsor transaksional tanpa penyusunan State (ditolak karena berpotensi merusak brand CafePulse, tidak menghargai kepakaran subjek, dan rentan terhadap penolakan akibat kekhawatiran keamanan API RouterOS).
*   **Impact:** Menghasilkan strategi komunikasi berbasis *Advisor Approach* yang terhormat, berorientasi nilai jangka panjang, serta memiliki mitigasi risiko keamanan dan pemosisian produk yang matang.

---

## [D-023] Penundaan Sementara Penjangkauan NanangMrk (NO-GO Assessment)

*   **Date:** 2026-06-24
*   **Decision:** Menangguhkan pengiriman proposal kolaborasi aktif kepada NanangMrk (*NO-GO*) sampai selesainya Closed Beta Campaign (v0.9) dan termitigasinya isu peringatan Windows Defender SmartScreen pada biner instalasi `.exe` CafePulse.
*   **Reason:** Mencegah risiko rusaknya reputasi keamanan dan kredibilitas produk akibat deteksi "untrusted software" di lab pengujian tokoh influencer utama, serta memastikan stabilitas multi-threading biner desktop sebelum diuji secara eksternal.
*   **Alternatives Rejected:**
    *   *Go (Melanjutkan Outreach Segera):* Ditolak karena terlalu berbahaya bagi reputasi CafePulse. Peringatan UAC SmartScreen atau bug crash tak terduga pada router berbeban tinggi milik NanangMrk dapat memicu sentimen negatif publik secara permanen.
*   **Impact:** Memberikan ruang bagi developer untuk mematangkan biner melalui Closed Beta 10 tester awal dan menyiapkan dokumentasi pendukung sebelum inisiasi penjangkauan dilakukan.

---

## [D-024] Status CONDITIONAL GO untuk Advisor Discovery Outreach

*   **Date:** 2026-06-24
*   **Decision:** Mengubah status kelayakan penjangkauan inisiasi awal privat (*Advisor Discovery Outreach*) dari *NO-GO* menjadi *CONDITIONAL GO*, dengan syarat fokus 100% pada permintaan evaluasi konseptual/opini ahli secara privat, transparan menjelaskan SmartScreen & status Beta, serta menyediakan instruksi aman RouterOS API read-only.
*   **Reason:** Audit kritis menunjukkan bahwa alasan penangguhan sebelumnya (SmartScreen, closed beta status, visual mockups) adalah blocker bagi peluncuran komersial publik (*Public Launch/Review*), tetapi bukan blocker bagi diskusi visi privat dengan penasihat teknis. Ahli jaringan senior memahami false-positives SmartScreen pada Python non-signed, dan justru menyukai pemberian masukan di tingkat konseptual awal sebelum kode difinalisasi.
*   **Alternatives Rejected:**
    *   *Mempertahankan NO-GO Mutlak:* Ditolak karena menyebabkan kehilangan momentumClosed Beta dan melewatkan kesempatan umpan balik kritis di fase desain arsitektur yang krusial.
    *   *GO Tanpa Syarat (Unconditional GO):* Ditolak karena tanpa transparansi masalah SmartScreen dan RouterOS API, subjek berisiko menolak akibat kekhawatiran keamanan kredensial.
*   **Impact:** Mengaktifkan inisiasi kontak privat dengan NanangMrk di bawah kerangka *Advisor Program* tepercaya, mempercepat umpan balik arsitektur, dan mempersiapkan evolusi kemitraan secara organik.

---

## [D-025] Pengesahan Revisi Arsitektur Kemitraan & Kelayakan Desain Proposal (CONDITIONAL READY)

*   **Date:** 2026-06-24
*   **Decision:** Mengesahkan revisi akhir arsitektur kemitraan (Penerapan Lisensi Opsi C 5-Tahun/Lifetime, Pengakuan Technical Advisor resmi, penambahan mitigasi *Perceived Lack of Differentiation*), memetakan logika penawaran nilai (*Why Should NanangMrk Care?*), dan menetapkan kesiapan masuk ke tahap *Proposal Design Phase* (Skor Kesiapan 8.5/10 - Ready for Proposal Design, outreach ditunda).
*   **Reason:** Model lisensi Opsi C memberikan insentif kontribusi bertahap yang adil (*Value-Creation Lock*). Pengakuan *Technical Advisor* menyelaraskan reputasi subjek tanpa membebani dengan operasional harian. Perancangan proposal dapat dimulai secara terisolasi, sementara pengiriman pesan outreach tetap ditangguhkan hingga biner stabil dan masalah SmartScreen diselesaikan.
*   **Alternatives Rejected:**
    *   *Membiarkan Lifetime License Langsung di Awal (Option B):* Ditolak karena melewatkan pengungkit insentif feedback aktif.
    *   *Melakukan Outreach Aktif Langsung:* Ditolak karena blocker teknis SmartScreen belum dimitigasi di sisi kode.
*   **Impact:** Menyelesaikan fase Discovery & State Definition proyek kemitraan secara penuh, menetapkan parameter nilai penawaran, dan memberikan lampu hijau untuk memulai perancangan dokumen proposal (*Proposal Design Phase*).

---

## [D-026] Penyusunan Paket Email Outreach Tahap Eksekusi (NANANGMRK_EMAIL_OUTREACH_PACKAGE_V1.md)

*   **Date:** 2026-06-24
*   **Decision:** Menyelesaikan penyusunan paket email penjangkauan (pilihan 10 subjek, draf email pertama, draf follow-up 7 & 14 hari, strategi lampiran gambar, dan checklist kesiapan) serta merekomendasikan keputusan akhir *SEND AFTER MINOR FIXES* untuk dieksekusi dalam 24 jam ke depan.
*   **Reason:** Mengubah dokumen strategi tingkat tinggi menjadi artefak operasional siap pakai oleh pengembang. Penundaan inisiasi email murni disebabkan oleh faktor kesiapan logistik minor (seperti unggah biner beta aktif untuk download link, kompilasi proposal ke PDF, capture screenshot, dan email signature) yang bernilai operasional, bukan masalah konseptual.
*   **Alternatives Rejected:**
    *   *Send Now (Kirim Sekarang):* Ditolak karena link unduhan belum aktif dan screenshot belum siap, yang akan merusak impresi pertama subjek jika ia langsung menguji.
    *   *Do Not Send (Jangan Dikirim):* Ditolak karena seluruh arsitektur nilai penawaran telah matang dan hanya menyisakan penyempurnaan logistik minor.
*   **Impact:** Menyediakan draf komunikasi email final yang terstruktur, sopan, dan transparan, siap dideploy segera setelah prasyarat logistik minor terpenuhi.

---

## [D-027] Hasil Audit Kesiapan Aset Penjangkauan & Optimasi Aset Eksisting

*   **Date:** 2026-06-24
*   **Decision:** Mengesahkan pemanfaatan 3 berkas gambar antarmuka PyQt6 eksisting (`dashboard_overview.png`, `hotspot_generator.png`, dan `license_manager.png` beresolusi 1600x1000) dan biner installer lokal di direktori `exports/` tanpa membuat gambar baru, serta menyetujui langkah konversi proposal markdown ke PDF instan (Print to PDF via browser/VS Code).
*   **Reason:** Mengurangi pengulangan kerja (*waste reduction*) dan mempercepat inisiasi penjangkauan. Berkas screenshot yang ditemukan memiliki kualitas dan aspek visual yang 100% matang dan representatif bagi materi email. Installer lokal juga sudah lengkap, menyisakan kebutuhan *minor fixes* untuk unggah biner secara online ke GitHub Releases.
*   **Alternatives Rejected:**
    *   *Membuat Screenshot Baru dari Awal:* Ditolak karena memakan waktu dan tidak memberikan peningkatan nilai visual yang signifikan dibanding aset berkualitas tinggi yang sudah tersedia di folder `assets/screenshots/`.
*   **Impact:** Status kesiapan screenshot bergeser dari *NOT READY* menjadi *READY*, memangkas estimasi waktu persiapan eksekusi kirim menjadi kurang dari 30 menit (tersisa hanya konversi proposal ke PDF dan pengunggahan biner online).

---

## [D-028] Finalisasi Review Eksekusi & Penyesuaian Strategi Penjangkauan NanangMrk

*   **Date:** 2026-06-24
*   **Decision:** Mengesahkan penyesuaian akhir paket penjangkauan: (1) Mengganti `license_manager.png` dengan `network_scan.png` pada Top 3 Screenshot email untuk menonjolkan utilitas teknis jaringan, (2) Memilih subjek email personal `"Saya Sedang Membangun CafePulse dan Ingin Meminta Pendapat Mas Nanang"` untuk human touch tertinggi, (3) Menerbitkan `GITHUB_RELEASE_CHECKLIST.md` untuk sinkronisasi case-sensitive unduhan online, (4) Menetapkan nama proposal PDF resmi `CafePulse_Advisor_Proposal_NanangMrk_v1.0.pdf`, dan (5) Menetapkan rekomendasi akhir *SEND AFTER MINOR FIXES*.
*   **Reason:** Audit kritis menunjukkan bahwa panel lisensi kurang memicu minat teknis di email pertama dibanding panel pemindaian subnet ARP. Subjek email dengan human touch terbukti meminimalkan filter spam personal. Dokumen checklist rilis menjamin kecocokan penulisan link unduhan di website GitHub Pages.
*   **Alternatives Rejected:**
    *   *Menggunakan license_manager.png di email pertama:* Ditolak karena kurang menunjukkan aktivitas rekayasa jaringan yang nyata di hadapan subjek.
*   **Impact:** Seluruh kesiapan logistik terstruktur rapi, memberikan kepastian eksekusi pengiriman email kepada NanangMrk dalam waktu kurang dari 24 jam dengan estimasi pengerjaan minor selama 20 menit.

---

## [D-029] Penyelesaian Sprint Final Eksekusi & Penerbitan Aset PDF Resmi

*   **Date:** 2026-06-24
*   **Decision:** Mengesahkan eksekusi pembuatan proposal PDF resmi (`CafePulse_Advisor_Proposal_NanangMrk_v1.0.pdf` berukuran ~49 KB) melalui otomasi skrip PyQt6 `export_pdf.py` secara lokal, melakukan validasi case-sensitive link unduhan pada `download.html`, dan menyepakati pengalihan Top 3 Screenshot email ke: `dashboard_overview.png`, `hotspot_generator.png`, dan `network_scan.png`.
*   **Reason:** Menyelesaikan gap teknis terakhir untuk status *SEND NOW*. Biner lokal terbukti lengkap dan siap diunggah secara online. Tautan unduhan di website telah diverifikasi 100% kompatibel dengan aset rilis.
*   **Alternatives Rejected:**
    *   *Mengekspor PDF Menggunakan Tools Eksternal Online:* Ditolak karena melanggar prinsip kepatuhan offline/local-first proyek. Otomasi skrip PyQt6 lokal menjamin privasi proposal 100%.
*   **Impact:** Status operasional dipastikan matang, hanya menyisakan tugas deployment *minor fixes* (pengunggahan berkas online ke GitHub Releases oleh pengembang) sebelum outreach email pertama dikirimkan hari ini.

---

## [D-030] Finalisasi Eksekusi Penjangkauan dan Pembersihan Identitas

*   **Date:** 2026-06-25
*   **Decision:** Mengganti secara menyeluruh istilah "Winbox Companion" menjadi "Local-First MikroTik Network Operations Platform" di seluruh draf komunikasi email, memperbarui referensi nama lampiran PDF proposal menjadi `CafePulse_Real_World_Validation_Proposal.pdf`, memperbaiki *dead link* (`youbellkey.github.io` ke `cafepulse.github.io`), dan menetapkan status akhir menjadi *SEND NOW*.
*   **Reason:** Penyelarasan SSOT CafePulse sebagai entitas platform independen telah tercapai. Keberadaan *dead link* berisiko merusak tingkat kepercayaan dari *advisor* teknis. Audit rilis GitHub v1.1.0-alpha.1 telah memverifikasi seluruh 6 tautan biner telah tayang secara riil.
*   **Alternatives Rejected:**
    *   *Mempertahankan "Winbox Companion" karena faktor Curiosity:* Ditolak karena mendegradasi posisi *branding* CafePulse yang kini telah berevolusi dari sekadar utilitas pendamping menjadi *Network Operations Platform* utuh.
*   **Impact:** Keseluruhan paket *Outreach* menjadi sempurna dan 100% siap (*SEND NOW*) untuk dieksekusi secara manual ke email NanangMrk.




