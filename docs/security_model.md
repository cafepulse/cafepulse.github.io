# Security Model (Model Keamanan)

Karena CafePulse membutuhkan akses *administrative/full* (melalui API) ke router infrastruktur jaringan Anda, kami mendesain perlindungan keamanan dengan pendekatan **Local-First & Offline-by-Default**.

*Catatan: Model keamanan ini telah diimplementasikan dan divalidasi selama pengembangan internal. Melalui fase **Real World Validation**, kami memastikan integritas perlindungan ini bekerja seragam di seluruh ragam topologi jaringan fisik berskala produksi.*

## 1. Arsitektur Data Lokal (Local-First)
Semua data jaringan, kredensial, *logs*, laporan audit, dan aktivitas pengguna tidak pernah meninggalkan komputer/perangkat Anda.
* **Tidak Ada Komputasi Awan (No Cloud):** CafePulse tidak memiliki arsitektur *cloud backend* untuk memproses *traffic* atau *logs* jaringan Anda.
* **Tidak Ada Telemetri Wajib:** Kami tidak mengirimkan data pengguna, MAC Address klien Anda, atau konfigurasi rahasia router Anda ke server kami. Anda memiliki kendali penuh secara *on-premise*.

## 2. Penyimpanan Kredensial
Penyimpanan kredensial perangkat router dikelola secara aman secara lokal.
* **SQLite Database:** Semua profil koneksi router dan kredensial login disimpan ke dalam file lokal `cafepulse.db`.
* **Enkripsi Lokal:** Password RouterOS Anda tidak disimpan dalam bentuk *plain-text*. Kami menggunakan algoritma enkripsi standar industri tingkat sistem untuk melakukan *hashing/encryption* kredensial sebelum ditulis ke dalam SQLite database.

## 3. Komunikasi Jaringan & API RouterOS
CafePulse berkomunikasi dengan router Anda murni menggunakan jaringan lokal/VPN yang sudah ada.
* Secara default, CafePulse menyarankan penggunaan port **API-SSL (8729)** untuk mencegah penyadapan kredensial di lapisan *layer-2/layer-3* LAN Anda. Jika router Anda tidak memiliki sertifikat SSL yang terkonfigurasi, Anda masih bisa menggunakan mode standar **API (8728)** secara lokal, namun kami memperingatkan risiko penggunaannya melalui jaringan Wi-Fi publik.
* Konektivitas selalu diinisiasi **dari** CafePulse (klien lokal) **ke** MikroTik Router. Router Anda tidak membutuhkan port eksternal/internet yang terbuka untuk digunakan oleh CafePulse.

## 4. Keamanan Fisik File Basis Data
Karena tidak menggunakan perlindungan kredensial *cloud*, tanggung jawab keamanan fisik bergeser ke lingkungan PC instalasi Anda.
* Sangat disarankan untuk memasang CafePulse pada mesin/PC yang memiliki sistem perlindungan *login* (seperti Windows Hello, BitLocker Drive Encryption, atau User Accounts dengan password kuat).
* Siapa saja yang dapat mengakses, menyalin, dan memecahkan enkripsi file `cafepulse.db` secara fisik dapat berpotensi memperoleh akses *login* ke router Anda.

Silakan baca selengkapnya mengenai pengamanan data mandiri di dokumen [Backup & Recovery Guide](./backup_and_recovery.md).
