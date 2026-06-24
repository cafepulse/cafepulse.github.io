# Changelog

Berikut adalah riwayat perubahan dan pembaruan versi dari perangkat lunak CafePulse.

---

## [0.9.0-beta] - 2026-06-25

Ini adalah rilis pratinjau perdana (Beta Release) yang ditujukan untuk pengujian kompatibilitas di lapangan (*Real World Validation*).

### Ditambahkan
- **Local-First Architecture:** Mesin *database* SQLite3 lokal dengan mode *Write-Ahead Logging* (WAL).
- **RouterOS API Client:** Integrasi penuh pembacaan dan penulisan via port 8728/8729.
- **Dashboard Module:** Tampilan *real-time* untuk CPU *router*, *bandwidth* antarmuka, dan *uptime*.
- **Hotspot Manager:** Fitur menambah, mengubah, dan menghapus (Kick) pengguna Hotspot secara langsung.
- **Voucher Engine:** Sistem penghasil *voucher* massal untuk Free Edition (10 per angkatan).
- **Secure Local Vault:** Sistem enkripsi profil kata sandi *router* menggunakan AES-256 tingkat militer.
- **Offline Licensing Engine:** Sistem aktivasi RSA-4096 untuk pengujian edisi Professional tanpa koneksi internet.

### Diketahui (Known Bugs)
- Pemutusan sambungan secara paksa (Mati listrik) dapat menyebabkan munculnya *Safe Mode* pada *boot* berikutnya karena berkas `.lock` belum terhapus.
- Grafik *Bandwidth* mungkin terlihat patah-patah jika CPU *router* sedang berada di 100% sehingga respons API terhambat.
