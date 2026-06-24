# CafePulse First Launch Guide (Panduan Peluncuran Pertama)

Panduan onboarding pengguna saat pertama kali menjalankan aplikasi CafePulse desktop, melakukan konfigurasi router, and mengaktifkan lisensi Professional secara offline.

---

## 1. Inisialisasi Boot Awal & Safe Mode

### 1.1 Inisialisasi Database & Folder
Saat peluncuran pertama kali, CafePulse mendeteksi sistem operasi and otomatis membuat folder writable khusus untuk penyimpanan data agar aman dari pemblokiran UAC (User Account Control) Windows:
- **Windows:** `%LOCALAPPDATA%\CafePulse\` (Berisi file database `cafepulse.db`, folder `logs\`, and file konfigurasi `settings.json`).
- **Linux:** `~/.local/share/CafePulse/` (atau direktori per-user yang setara).

Database SQLite diinisialisasi otomatis dalam mode **WAL (Write-Ahead Logging)** untuk menjamin kestabilan penyimpanan log performa multi-threading.

### 1.2 Sistem Proteksi Startup (Safe Mode)
CafePulse mengelola penutupan aplikasi menggunakan mekanisme flag berkas `.clean` and `.lock`:
- Jika aplikasi ditutup secara tidak normal (misalnya mati lampu atau force-shutdown OS) sehingga bendera status bersih belum tertulis, saat boot berikutnya aplikasi akan memunculkan peringatan keselamatan:
  `"CafePulse was not closed properly. Would you like to boot in Safe Mode?"`
- **Safe Mode:** Menonaktifkan pemuatan profil koneksi otomatis and menghentikan background thread monitoring sementara untuk mengizinkan pengguna memperbaiki pengaturan database yang korup.

---

## 2. Pengaturan Profil Jaringan & Koneksi Router

Langkah-langkah menyambungkan CafePulse ke router board MikroTik Anda:

### 2.1 Menyiapkan Akses API RouterOS
Pastikan service API di router MikroTik Anda telah diaktifkan:
1. Buka Winbox, masuk ke menu **IP** ➔ **Services**.
2. Pastikan service **api** (port default `8728`) atau **api-ssl** (port default `8729`) dalam status **Enabled** (aktif).
3. Buat user group khusus di menu **System** ➔ **Users** yang memiliki izin (*read* dan *write*) untuk API.

Atau, jika Anda menggunakan **New Terminal** di MikroTik, jalankan perintah berikut untuk mengeksekusinya secara cepat:
```routeros
/ip service enable api
/user group add name=api_group policy=read,write,api
```

### 2.2 Membuat Profil Koneksi di Aplikasi
1. Luncurkan CafePulse, lalu klik ikon **Settings** (Pengaturan) atau tab **Connections**.
2. Klik tombol **"Add New Connection"**.
3. Isi parameter koneksi:
   - **Connection Name:** Nama pengenal router (misalnya: *Router Utama Indihome*).
   - **Router IP Address:** Alamat IP gateway router (misalnya: `192.168.88.1`).
   - **API Port:** Isi `8728` (untuk API biasa) atau `8729` (untuk API terenkripsi SSL).
   - **Username & Password:** Masukkan kredensial admin/user khusus MikroTik Anda.
4. Klik **"Test Connection"** untuk memverifikasi.
   - *Jika sukses:* Indikator akan berubah menjadi hijau ("Connection Established").
   - *Jika gagal (Timeout):* Periksa kembali apakah alamat IP benar dan firewall Windows tidak memblokir aplikasi.
   - *Jika gagal (Auth Error):* Periksa apakah *Username/Password* Anda benar dan memiliki izin `api`.
5. Klik **"Save Profile"**. CafePulse akan mengenkripsi kredensial Anda menggunakan algoritma AES-256 dan menyimpannya di dalam *Secure Local Vault* (`cafepulse.db`) yang secara persisten terikat dengan PC Anda. Kredensial tidak dapat dibaca meskipun file disalin ke PC lain tanpa kunci dekripsi Master OS Anda.

---

## 3. Proses Aktivasi Lisensi Professional (Offline RSA)

CafePulse Professional Edition menggunakan aktivasi lisensi 100% offline demi privasi dan fungsionalitas tanpa ketergantungan server cloud eksternal.

### Langkah 1: Ekspor Activation Request
1. Buka tab **Licensing** (Lisensi) di aplikasi CafePulse Anda.
2. Anda akan melihat deretan string **Hardware ID (HWID)** Anda (Contoh: `CP-HWID-3A19-B88C-F46E-10FB`).
3. Isi nama pemilik lisensi and alamat email Anda.
4. Klik tombol **"Generate Request File"** untuk mengekspor berkas bernama `activation_request.licreq` ke Desktop Anda.

### Langkah 2: Proses Pembayaran & Penerbitan Lisensi
1. Buka situs web resmi CafePulse, masuk ke halaman lisensi / checkout.
2. Lakukan pembayaran lisensi Professional sesuai panduan (Rp499.000 satu kali beli).
3. Unggah file `activation_request.licreq` Anda ke formulir pendaftaran lisensi website.
4. Sistem (atau developer) akan memverifikasi pembayaran and menandatangani request file Anda menggunakan private key RSA-4096 milik CafePulse, lalu mengirimkan file lisensi bernama **`license.lic`** ke email Anda.

### Langkah 3: Impor Berkas Lisensi
1. Kembali ke tab **Licensing** di aplikasi CafePulse Anda.
2. Klik tombol **"Import License File"**.
3. Pilih berkas **`license.lic`** yang Anda terima dari email, lalu klik **Open**.
4. Aplikasi akan membaca, melakukan verifikasi tanda tangan kriptografis secara lokal, and langsung mengaktifkan status **Professional Edition** secara permanen.
