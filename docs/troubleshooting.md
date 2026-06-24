# Troubleshooting Guide (Panduan Pemecahan Masalah)

Jika Anda menemui masalah saat menggunakan CafePulse, silakan rujuk ke daftar solusi dari masalah umum berikut sebelum Anda mengajukan tiket laporan *bug*.

> [!NOTE]
> Sebagai bagian dari proses **Release Readiness Validation**, kami aktif memetakan kompatibilitas lintas perangkat. Jika sebuah isu koneksi tidak terpecahkan oleh panduan di bawah, hal tersebut sangat berharga untuk dilaporkan demi menyempurnakan penanganan (handling) aplikasi terhadap tipe *hardware* spesifik.

### Masalah 1: "Connection Failed" / "Router Not Found"
**Gejala:** CafePulse tidak dapat menemukan router Anda atau koneksi ditolak di lapisan jaringan (*Network Layer*).
* **Periksa IP Address:** Pastikan IP Address Router yang dimasukkan di profil koneksi sudah benar (biasanya alamat Gateway seperti `192.168.88.1`).
* **Periksa Firewall PC:** Pastikan Windows Defender atau Antivirus pihak ketiga Anda tidak memblokir aplikasi `CafePulse.exe` dari akses jaringan lokal.
* **Jaringan Tepat:** Pastikan PC/Laptop tempat Anda menjalankan CafePulse terhubung ke jaringan (*Wi-Fi/LAN*) yang diatur oleh router MikroTik tersebut.

### Masalah 2: "Authentication Error"
**Gejala:** Router berhasil dihubungi, namun CafePulse menolak login.
* **Username/Password Salah:** Periksa kembali nama pengguna dan kata sandi Anda. Anda dapat memeriksanya dengan masuk melalui aplikasi Winbox.
* **Izin Akses (Groups):** Pastikan *user* yang digunakan oleh CafePulse memiliki grup kebijakan (Policies) minimum `read`, `write`, dan `api` di pengaturan Winbox (`System > Users`).

### Masalah 3: "API Timeout" / Aplikasi Bergerak Lambat
**Gejala:** Saat memuat daftar perangkat aktif atau memuat halaman *Dashboard*, CafePulse terhenti lama atau muncul galat batas waktu (Timeout).
* **CPU Router Tinggi:** Periksa beban kerja CPU Router MikroTik Anda via Winbox. Jika penggunaan mencapai 100%, router akan mengabaikan respons API.
* **Layanan API Nonaktif:** Buka Winbox, pergi ke `IP > Services`. Pastikan layanan `api` (Port 8728) atau `api-ssl` (Port 8729) berstatus *Enabled* (tidak berwarna abu-abu/ditandai silang).
* **Pembatasan Port/Alamat:** Jika Anda mengkonfigurasi kolom `Available From` di `IP > Services`, pastikan IP PC Anda saat ini diizinkan untuk mengaksesnya.

### Masalah 4: Data Hotspot / Pengguna Tidak Tampil
**Gejala:** Anda berhasil terhubung dan menuju Dashboard, namun tidak ada daftar pengguna *Hotspot* yang aktif.
* **Paket Hotspot Tidak Ada:** Fitur *Dashboard* utama menuntut agar fitur *Hotspot* dikonfigurasi dan menyala pada router Anda.
* **Sistem yang Tidak Didukung:** Periksa daftar [MikroTik Compatibility Matrix](./mikrotik_compatibility_matrix.md) untuk memastikan apakah konfigurasi lawas (seperti RouterOS v5) menjadi penyebab masalah tersebut.

Jika panduan di atas tidak membuahkan hasil, silakan kumpulkan rekaman layar aplikasi dan berkas *log* Anda sesuai [Bug Reporting Guide](./bug_reporting_guide.md).
