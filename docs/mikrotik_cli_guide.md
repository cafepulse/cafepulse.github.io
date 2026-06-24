# MikroTik CLI Guide for CafePulse

Bagi Network Administrator (atau pengguna *Virtual Machine*) yang lebih nyaman menggunakan baris perintah (Command Line Interface / CLI) ketimbang antarmuka grafis Winbox, dokumen ini merangkum seluruh perintah *Terminal* RouterOS yang relevan untuk menyiapkan, mengamankan, dan men- *debug* koneksi CafePulse.

## 1. Konfigurasi Layanan API

CafePulse membutuhkan layanan API untuk berkomunikasi dengan router.

**Mengaktifkan API standar (Port 8728):**
```routeros
/ip service enable api
```

**Mengaktifkan API-SSL (Port 8729) [Direkomendasikan]:**
```routeros
/ip service enable api-ssl
```

**Membatasi Akses API ke IP Tertentu (Keamanan Ekstra):**
Untuk mencegah akses API dari perangkat yang tidak sah, Anda dapat membatasi layanan API agar hanya menerima koneksi dari IP komputer yang menjalankan CafePulse (misalnya `192.168.88.10`).
```routeros
/ip service set api address=192.168.88.10/32
```
*(Ganti `192.168.88.10` dengan IP statis PC Anda).*

**Melihat Status Layanan API:**
```routeros
/ip service print where name="api" or name="api-ssl"
```
*(Pastikan tidak ada tanda `X` di sebelah kiri nama layanan, yang berarti dinonaktifkan).*

## 2. Konfigurasi Pengguna (System Users)

CafePulse memerlukan izin baca (`read`), tulis (`write`), dan eksekusi API (`api`). Sangat disarankan membuat pengguna (*user*) khusus yang terpisah dari akun `admin`.

**Membuat Group Khusus untuk CafePulse:**
```routeros
/user group add name=cafepulse_group policy=read,write,api
```

**Membuat Pengguna Baru (Kaitkan dengan Group di atas):**
```routeros
/user add name=cafepulse_user group=cafepulse_group password="SandiKuatAnda"
```

**Memverifikasi Daftar Pengguna:**
```routeros
/user print
```

## 3. Pemecahan Masalah (Troubleshooting) via CLI

Jika CafePulse mengalami kendala (*timeout*, gagal memuat daftar klien, atau tidak dapat login), Anda dapat men- *debug* kondisi router secara langsung.

**Memeriksa Beban CPU Router:**
Penyebab paling umum koneksi API gagal atau lambat adalah CPU router yang mencapai batas 100%.
```routeros
/system resource print
```
Atau pemantauan *real-time*:
```routeros
/system resource monitor
```

**Memeriksa Status Koneksi di Port API:**
Melihat apakah PC CafePulse berhasil menjalin sambungan jaringan (*TCP Handshake*) ke *port* 8728/8729 di router.
```routeros
/ip firewall connection print where dst-address~":8728" or dst-address~":8729"
```

**Memeriksa Status Hotspot:**
Memastikan layanan Hotspot MikroTik Anda benar-benar berjalan dan menampung *active leases*.
```routeros
/ip hotspot print
/ip hotspot active print
```

## 4. Keamanan Lanjutan (API-SSL Certificates)

Jika Anda memutuskan menggunakan `api-ssl` (Port 8729), router MikroTik Anda harus memiliki sertifikat yang valid. Jika Anda belum memilikinya, Anda dapat men- *generate* sertifikat *Self-Signed* langsung dari CLI.

**Membuat Sertifikat Self-Signed untuk API:**
```routeros
/certificate add name=CafePulse_Cert common-name=CafePulse_Cert days-valid=3650 key-usage=key-cert-sign,tls-server
/certificate sign CafePulse_Cert
```

**Memasang Sertifikat ke Layanan API-SSL:**
```routeros
/ip service set api-ssl certificate=CafePulse_Cert
```

## 5. Analisis Log Autentikasi (System Logs)

Jika CafePulse berulang kali memunculkan pesan *Authentication Error*, Anda dapat memantau log sistem MikroTik untuk melihat alasan spesifik penolakan koneksi (apakah salah sandi atau IP diblokir).

**Melihat Log Login Terakhir:**
```routeros
/log print where message~"login failure" or message~"api"
```

## 6. Manajemen Klien Darurat (Emergency Kick)

Meski CafePulse menyediakan tombol *Kick* di antarmukanya, Anda juga bisa menendang (*disconnect*) pengguna *Hotspot* secara manual melalui CLI jika aplikasi sedang tidak aktif.

**Menghapus Pengguna Aktif dari Hotspot (berdasarkan User):**
```routeros
/ip hotspot active remove [find user="nama_pengguna"]
```

**Menghapus Pengguna berdasarkan IP Address:**
```routeros
/ip hotspot active remove [find address="10.5.50.25"]
```

Dengan menguasai perintah-perintah CLI (Terminal) di atas, Anda dapat melakukan inisialisasi lingkungan pengujian, mengamankan jalur komunikasi, serta men- *debug* perilaku koneksi CafePulse sepenuhnya melalui *console* (SSH/Telnet) atau layar terminal Virtual Machine tanpa perlu menyentuh antarmuka GUI Winbox sama sekali.
