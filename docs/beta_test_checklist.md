# Beta Test Checklist

Dokumen panduan ini ditujukan bagi partisipan *Beta Tester Program* sebelum mengirimkan laporan stabilitas rilis CafePulse terbaru. Kami meminta Anda memvalidasi fungsionalitas inti menggunakan senarai periksa (*checklist*) berikut.



### 1. Modul Koneksi (Connection)
- [ ] **Berhasil Connect:** Aplikasi dapat terhubung menggunakan kredensial RouterOS API standard (SSL/Non-SSL).
- [ ] **Reconnect Handling:** Aplikasi tidak *crash* jika jaringan LAN tiba-tiba terputus dari PC; ia harus mencoba melakukan koneksi ulang secara diam-diam.
- [ ] **Wrong Password Rejection:** Aplikasi memberikan pesan kesalahan *Authentication Error* yang jelas jika salah memasukkan *password* atau *username*, tanpa menyebabkan jendela aplikasi tertutup sendiri (*Force Close*).

### 2. Modul Pemantauan (Monitoring)
- [ ] **Scan Berhasil:** *Network Scan* awal untuk mengambil *active leases* dan konfigurasi dasar sukses tanpa *timeout*.
- [ ] **Refresh Berhasil:** Menekan tombol pembaruan (*Refresh*) secara manual memperbarui tabel data antarmuka (contoh: Rx/Tx bytes berubah).
- [ ] **Disconnect Handling:** Aplikasi dapat memutus perangkat (*Kick Client*) dari daftar Hotspot Active, dan status pengguna tersebut hilang dari layar pada siklus *refresh* berikutnya.

### 3. Ketahanan Stabilitas (Stability & Polling)
- [ ] **1 Jam:** Tidak ada lonjakan RAM tak wajar setelah fitur *Auto-Refresh* berjalan selama satu jam (Memory Leak Check).
- [ ] **8 Jam:** Antarmuka (*UI*) tidak mengalami pembekuan (*freeze*) setelah dibiarkan aktif seharian.
- [ ] **24 Jam:** Tidak ada pesan kesalahan "Too Many Simultaneous Connections" pada RouterOS logs (*Winbox*) yang diakibatkan oleh kebocoran *socket* CafePulse.

### 4. Simulasi Router Reboot
- [ ] **Router Restart:** Lakukan *reboot* pada router MikroTik saat CafePulse sedang dalam status *Connected*.
- [ ] **Koneksi Terputus:** UI harus menyadari putusnya koneksi dan menampilkan status *Disconnected* atau *Reconnecting*.
- [ ] **Auto-Recovery:** Saat router kembali menyala (setelah *boot-up* ~1-2 menit), CafePulse **wajib** berhasil terkoneksi ulang secara otomatis (*Auto-Reconnect*) dan memuat ulang halaman utama.

Jika ada dari *checklist* di atas yang gagal pada sistem Anda, mohon sertakan informasi dari tabel kompatibilitas [MikroTik Compatibility Matrix](./mikrotik_compatibility_matrix.md) dalam tiket *bug report* Anda.
