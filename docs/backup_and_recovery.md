# Backup & Recovery Guide

Karena CafePulse menggunakan arsitektur *local-first*, tanggung jawab pencadangan data (*backup*) berada sepenuhnya di sisi klien. Anda harus secara mandiri mengamankan *database* jika tidak ingin kehilangan riwayat log dan profil router Anda saat komputer rusak atau diformat.



## 1. Lokasi Database Lokal
Semua konfigurasi, kredensial tersandi, riwayat klien, dan laporan (*logs*) CafePulse disimpan dalam satu file *database* tunggal:
* **Nama File:** `cafepulse.db`
* **Lokasi Default:** Berada tepat di direktori yang sama dengan eksekusi file utama (`CafePulse.exe` atau lokasi instalasi utama di sistem Anda).

## 2. Cara Melakukan Pencadangan (Backup)
Karena sifatnya portabel, pencadangan sangat mudah dilakukan:
1. Pastikan aplikasi CafePulse dalam keadaan **Tutup Penuh** (Tidak berjalan di *system tray* atau *background*).
2. Navigasikan *File Explorer* Anda ke lokasi instalasi CafePulse.
3. Salin (*copy*) file `cafepulse.db`.
4. Rekatkan (*paste*) file tersebut ke lokasi penyimpanan eksternal yang aman (misalnya: USB Flashdrive, Hard Disk Eksternal, atau layanan Cloud Storage pribadi Anda seperti Google Drive/Dropbox).

*Tips: Lakukan backup secara berkala (misal: seminggu sekali) jika Anda mengelola puluhan router aktif dengan pergerakan klien (voucher) yang tinggi.*

## 3. Cara Melakukan Pemulihan (Restore)
Jika Anda mengalami kegagalan sistem PC atau kerusakan database lokal:
1. Tutup aplikasi CafePulse.
2. Timpa (*overwrite*) atau ganti file `cafepulse.db` yang rusak di direktori instalasi dengan versi file `cafepulse.db` terbaru dari direktori pencadangan (backup) Anda.
3. Buka kembali aplikasi CafePulse. Semua profil, data, dan lisensi lokal Anda akan kembali seperti saat terakhir file tersebut dicadangkan.

## 4. Migrasi Instalasi ke PC Baru
Sifat data *local-first* dan struktur satu file (*single file architecture*) memungkinkan migrasi yang sangat lancar antar PC kerja Anda.
1. Salin seluruh *folder* CafePulse (atau cukup installer dan file `cafepulse.db` dari PC lama).
2. Pindahkan ke PC baru.
3. Letakkan `cafepulse.db` sejajar dengan lokasi instalasi di PC baru tersebut.
4. Saat pertama kali diluncurkan di PC baru, CafePulse akan otomatis membaca pengaturan router, lisensi, dan log lama tanpa memerlukan konfigurasi ulang.

> [!CAUTION]
> Jangan pernah membagikan file `cafepulse.db` Anda ke pihak publik, karena file ini menampung seluruh kredensial sandi akses MikroTik Anda (meski dalam keadaan terenkripsi).
