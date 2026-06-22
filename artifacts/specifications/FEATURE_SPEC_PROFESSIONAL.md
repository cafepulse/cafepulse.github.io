# CAFEPULSE FEATURE SPECIFICATION — PROFESSIONAL EDITION
### *Product Requirements Document — v1.0.0 | Juni 2026*

---

## OVERVIEW

Dokumen ini mendefinisikan spesifikasi lengkap semua fitur tingkat lanjut (advanced features) yang eksklusif tersedia di CafePulse Professional Edition. Setiap fitur didefinisikan dengan user story, kriteria penerimaan (acceptance criteria), dan penanganan edge cases.

---

## FEATURE 1 — MIKROTIK ROUTEROS API INTEGRATION

### User Story
> Sebagai pemilik bisnis/admin jaringan, saya ingin menghubungkan CafePulse secara langsung ke router MikroTik saya, sehingga saya dapat memantau interface, daftar DHCP, firewall, dan routing secara real-time langsung dari satu desktop dashboard tanpa perlu membuka Winbox.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **API Connectivity** | Koneksi via RouterOS API port default 8728 (tanpa SSL) atau 8729 (dengan SSL/TLS) |
| **API Wrapper** | Menggunakan library `routeros-api` dengan koneksi persisten yang aman |
| **Interface Monitoring** | Menampilkan bandwidth rx/tx real-time dari semua interface router (Ethernet, VLAN, WLAN) |
| **DHCP Lease Viewer** | Sinkronisasi tabel DHCP lease MikroTik dengan local database, menampilkan IP, MAC, status aktif, dan hostname |
| **Firewall & Routing Control** | Menampilkan daftar rules firewall filter, NAT, dan tabel routing aktif; mendukung trigger enable/disable rule |
| **Performance** | Polling rate API terisolasi di background thread (`MikrotikWorker`) untuk mencegah UI freeze |

### Edge Cases
- Jika koneksi API terputus (kabel dicabut/router reboot), status berubah menjadi "Disconnected" dan sistem mencoba menyambung kembali setiap 10 detik.
- Credentials disimpan di database lokal secara terenkripsi (AES/Fernet) menggunakan kunci yang terikat dengan ID mesin pengguna.

---

## FEATURE 2 — IDENTITY & ACCESS MANAGEMENT (IAM)

### User Story
> Sebagai pengelola jaringan hotspot/cafe, saya ingin mengelola database pelanggan, paket akses, dan status sesi pengguna secara terpusat, agar saya dapat mengontrol hak akses internet pelanggan saya dengan mudah.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **User Directory** | Database lokal pelanggan hotspot terintegrasi dengan tabel `vouchers` dan `routers` |
| **Active Sessions** | Menampilkan daftar user yang sedang aktif login, durasi penggunaan, dan sisa kuota data |
| **Package Plans** | Pembuatan profil paket akses: batas kecepatan (Rate Limit, misal: 2M/512k), batas waktu (Limit Uptime), dan masa aktif |
| **Force Disconnect** | Admin dapat memutuskan sesi user aktif secara paksa dengan menghapus session di RouterOS via API |
| **Sync Engine** | Sinkronisasi otomatis data user antara database lokal CafePulse dengan database user hotspot MikroTik |

---

## FEATURE 3 — CRYPTOGRAPHIC OFFLINE VOUCHER GENERATOR

### User Story
> Sebagai pemilik cafe, saya ingin membuat ratusan voucher hotspot secara massal (bulk) untuk dijual ke pelanggan, lengkap dengan cetakan voucher fisik berukuran kecil yang berisi kode login dan petunjuk penggunaan.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **Bulk Generation** | Membuat hingga 500 voucher unik secara acak (username & password) dalam satu kali eksekusi |
| **Complexity Rules** | Karakter username/password acak dapat disesuaikan (angka saja, huruf saja, atau kombinasi tanpa karakter membingungkan seperti l, 1, O, 0) |
| **Voucher Profiles** | Asosiasi voucher ke paket akses MikroTik yang telah dibuat (misal: Paket 2 Jam, Paket Harian) |
| **PDF Rendering** | Ekspor lembar voucher siap cetak ke format PDF berdesain premium menggunakan ReportLab |
| **Ticket Details** | Setiap tiket voucher berisi: Nama Hotspot, Kode Voucher (atau QR Code untuk auto-login), Batas Waktu/Kuota, Harga, dan Petunjuk Login |

---

## FEATURE 4 — ADVANCED NETWORK DNA RADAR VIEW

### User Story
> Sebagai administrator jaringan, saya ingin melihat visualisasi grafis dari hubungan antar perangkat di jaringan saya secara real-time, agar saya dapat mendeteksi penyusup atau memvisualisasikan beban bandwidth dengan cepat.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **Visualization Style** | Radar grafis berbentuk node-link diagram interaktif berbasis library `pyqtgraph` |
| **Node Representation** | Router berada di pusat radar; perangkat klien berada di orbit luar berdasarkan latensi/kekuatan sinyal |
| **Traffic Indication** | Ketebalan garis hubungan menunjukkan volume transfer data; warna garis menunjukkan status (Hijau: Aman, Kuning: Sibuk, Merah: Bahaya/Kritis) |
| **Interaction** | Mengklik salah satu node perangkat memunculkan pop-up detail informasi (IP, MAC, Hostname, dan grafik bandwidth mini) |
| **GPU Acceleration** | Kecepatan render radar dioptimalkan menggunakan akselerasi hardware PyQtGraph (CPU usage < 5%) |

---

## FEATURE 5 — HARDWARE-LOCKED LICENSE ACTIVATION

### User Story
> Sebagai penyedia software, saya ingin membatasi penggunaan Professional Edition agar hanya dapat aktif di komputer yang membeli lisensi resmi tanpa memerlukan koneksi internet untuk aktivasinya.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **Hardware Binding** | ID Mesin 16-karakter dihasilkan dari hashing (SHA-256) kombinasi serial motherboard, UUID Windows, dan MAC address utama |
| **License Format** | Berkas JSON `.lic` disimpan di `%APPDATA%/CafePulse/config/license.lic` |
| **Cryptographic Sign** | Berkas lisensi berisi data pembeli dan tanda tangan digital RSA-2048 yang dibuat dengan kunci privat pengembang |
| **Offline Verification** | Aplikasi memverifikasi tanda tangan lisensi menggunakan kunci publik RSA yang ditanam di dalam source code |
| **Grace Period** | Jika lisensi tidak valid atau kedaluwarsa, aplikasi otomatis menurunkan fitur ke Free Edition tanpa menghentikan aplikasi |

---

## FEATURE 6 — AUTOMATED NETWORK HEALTH AUDIT REPORTING

### User Story
> Sebagai administrator IT, saya ingin menghasilkan laporan audit kesehatan jaringan secara berkala dalam format PDF profesional, agar saya dapat memberikan laporan keandalan sistem kepada manajemen atau pemilik bisnis.

### Kriteria Penerimaan (Acceptance Criteria)

| Kriteria | Spec |
|---|---|
| **Trigger** | Tombol "Generate Audit Report" di panel Analytics/Dashboard |
| **Metrics Captured** | Rata-rata CPU/RAM router, rekam jejak alert kritis, statistik uptime, dan distribusi jenis perangkat |
| **Report PDF Design** | Dokumen multi-halaman PDF dengan kop surat kustom, grafik performa, dan kesimpulan penilaian kesehatan |
| **Score Engine** | Algoritma penilaian mandiri (A/B/C/D/F) berdasarkan data kepatuhan konfigurasi keamanan MikroTik |
| **Local Export** | File PDF disimpan di folder `exports/reports/` dengan penamaan otomatis berformat timestamp |

---

*Dokumen Feature Specification Professional Edition CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
