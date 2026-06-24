# RouterOS API Setup

Agar CafePulse dapat berkomunikasi dengan router MikroTik Anda dan memantau status jaringan, Anda harus mengaktifkan layanan API (Application Programming Interface) di dalam RouterOS.

## 1. Mengaktifkan Layanan API
Layanan ini secara bawaan mungkin dinonaktifkan di beberapa versi RouterOS. Untuk mengaktifkannya:
1. Buka **Winbox** dan *login* ke router Anda.
2. Buka menu **IP** > **Services**.
3. Cari baris layanan bernama `api` (Port standar: `8728`) atau `api-ssl` (Port standar: `8729`).
4. Klik kanan pada layanan tersebut dan pilih **Enable**, atau klik tombol centang biru/hijau di menu atas.

## 2. Rekomendasi Keamanan
Untuk menjaga keamanan router Anda saat menggunakan CafePulse:
* **Gunakan API-SSL:** Jika router Anda mendukung dan telah terkonfigurasi dengan sertifikat, kami sangat menyarankan untuk hanya menggunakan port `api-ssl` (8729) guna mengenkripsi jalur komunikasi lokal Anda.
* **Batasi Akses (Available From):** Pada menu `IP` > `Services`, Anda dapat melakukan klik ganda pada `api` atau `api-ssl` dan mengisi kolom **Available From** dengan alamat IP (*IP Address*) dari PC yang menjalankan CafePulse (contoh: `192.168.88.10`). Ini secara efektif akan memblokir upaya akses API dari komputer/perangkat asing.

## 3. Hak Akses Pengguna (System Users)
CafePulse mensyaratkan izin baca/tulis yang memadai (*read/write/api*) ke konfigurasi router Anda.
1. Buka menu **System** > **Users**.
2. Pastikan akun yang digunakan oleh CafePulse masuk ke dalam *Group* (contoh: `full` atau `write`) yang memiliki setelan *policies* mencakup: `read`, `write`, dan `api`.
3. *(Opsional)* Demi keamanan dan kemudahan audit *log*, Anda dapat membuat *user* khusus baru (contoh: `cafepulse_user`) yang terpisah dari akun `admin` utama Anda.

Setelah langkah di atas selesai, Anda dapat memasukkan *IP Router*, *Username*, dan *Password* ke jendela utama CafePulse.
