# Panduan Harga dan Lisensi CafePulse (Offline RSA)

CafePulse menggunakan sistem lisensi offline kriptografis berbasis algoritma RSA-4096. Pendekatan **Local-First** ini memastikan aplikasi desktop Anda tetap berjalan dan fitur Professional dapat divalidasi 100% tanpa bergantung pada koneksi internet atau server lisensi pihak ketiga.

## 1. Perbedaan Edisi

CafePulse menyediakan dua edisi dengan model distribusi yang sama (installer yang sama), tetapi kapabilitasnya ditentukan oleh kunci lisensi Anda.

### Free Edition (Bawaan)
- **Harga:** Gratis selamanya.
- **Fitur Utama:** Sweep ARP Network, Deteksi Subnet Offline, Uji Koneksi Router.
- **Keterbatasan:** Tidak ada Background Polling, Tidak ada Integrasi Manajemen Voucher (Hotspot), dan Tidak ada Ekspor PDF.

### Professional Edition (Premium)
- **Harga:** Rp499.000 (Lisensi sekali bayar / One-Time Purchase).
- **Fitur Utama:** Seluruh fitur Free, ditambah Multi-threaded Background Polling (CPU, RAM, Active Users), Bulk Voucher Generator yang otomatis sinkron dengan API RouterOS, dan Manajemen Backup Konfigurasi Router.
- **Model Akses:** Tidak ada biaya bulanan (SaaS). Berlisensi selamanya untuk versi rilis major saat ini.

---

## 2. Alur Pembelian dan Aktivasi Lisensi

Aktivasi lisensi melibatkan pertukaran file secara aman antara aplikasi desktop Anda dan portal website kami (Midtrans).

### Langkah 1: Ekspor Hardware ID (HWID)
Aplikasi CafePulse mengunci lisensi spesifik pada perangkat komputer Anda menggunakan Hardware ID (`MachineGuid` untuk Windows, atau `/etc/machine-id` untuk Linux).
1. Buka aplikasi **CafePulse** di komputer Anda.
2. Masuk ke tab **Licensing** (Lisensi).
3. Isi nama dan email Anda.
4. Klik tombol **"Generate Request File"**.
5. Aplikasi akan mengekspor berkas bernama `activation_request.licreq` ke komputer Anda.

### Langkah 2: Proses Checkout (Website)
1. Kunjungi halaman [Pricing & Checkout](./pricing.html) di situs web resmi CafePulse.
2. Klik tombol pembelian untuk Professional Edition.
3. Anda akan diminta untuk mengunggah file `activation_request.licreq` milik Anda.
4. Lakukan pembayaran melalui sistem _Payment Gateway_ yang aman (kami mendukung QRIS, Transfer Bank, e-Wallet via integrasi Midtrans).

### Langkah 3: Menerima Berkas Lisensi
Setelah pembayaran berhasil dikonfirmasi oleh sistem, mesin kami akan secara otomatis memproses HWID Anda dan menandatanganinya secara kriptografis menggunakan Private Key RSA-4096 resmi CafePulse.
1. Anda akan menerima email yang melampirkan berkas bernama **`license.lic`**.
2. Simpan file tersebut dengan aman di komputer Anda (file ini adalah bukti kepemilikan lisensi digital Anda).

### Langkah 4: Aktivasi Secara Offline
1. Kembali ke aplikasi CafePulse, masuk ke tab **Licensing**.
2. Klik tombol **"Import License File"**.
3. Pilih file `license.lic` yang baru saja Anda terima.
4. Aplikasi akan memverifikasi tanda tangan digital tersebut secara matematis di dalam komputer Anda (tanpa perlu koneksi internet). Jika terverifikasi valid dan HWID cocok dengan komputer tersebut, fitur **Professional Edition** akan terbuka secara permanen!

> [!IMPORTANT]
> **Penting Mengenai Keamanan File Lisensi:**
> Jangan memodifikasi isi file `license.lic` menggunakan teks editor. Mengubah 1 karakter saja akan merusak integritas *cryptographic signature* (tanda tangan digital) dan menyebabkan aplikasi menolak file tersebut. Jika Anda memindahkan CafePulse ke perangkat keras yang baru, Anda mungkin perlu menghubungi dukungan teknis untuk permintaan transfer HWID.
