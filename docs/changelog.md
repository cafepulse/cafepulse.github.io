# Changelog

Berikut adalah riwayat perubahan dan pembaruan versi dari perangkat lunak CafePulse.

---

## [TBD Version]

Ini adalah rilis pratinjau perdana (Beta Release) yang ditujukan untuk pengujian kompatibilitas di lapangan (*Real World Validation*).

### Ditambahkan
- **Local-First Architecture:** Mesin *database* SQLite3 lokal dengan mode *Write-Ahead Logging* (WAL).
- **RouterOS API Client:** Integrasi penuh pembacaan dan penulisan via port 8728/8729.
- **Dashboard Module:** Tampilan *real-time* untuk CPU *router*, *bandwidth* antarmuka, dan *uptime*.
- **Hotspot Manager:** Fitur menambah, mengubah, dan menghapus (Kick) pengguna Hotspot secara langsung.
- **Voucher Engine:** Sistem penghasil *voucher* massal.
- **Secure Local Vault:** Sistem enkripsi profil kata sandi *router* menggunakan AES-256 tingkat militer.
- **Offline Licensing Engine:** Sistem aktivasi RSA-4096 untuk pengujian edisi Professional tanpa koneksi internet.

### Diketahui (Known Bugs)
- Pemutusan sambungan secara paksa (Mati listrik) dapat menyebabkan munculnya peringatan *Safe Mode* pada *boot* berikutnya karena berkas `.lock` belum terhapus.
- *[Bug spesifik lainnya akan didata seiring berjalannya Validasi Lapangan]*
