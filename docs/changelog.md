# Changelog

Berikut adalah riwayat perubahan dan pembaruan versi dari perangkat lunak CafePulse.

---

## [Pre-Release Documentation Update] - 2026-06-25

Rilis pembaruan ini berfokus secara eksklusif pada **Perombakan Dokumentasi Besar-besaran (Documentation Overhaul)** untuk mempersiapkan fase pengujian lapangan (*Real World Validation*) dan penjangkauan *Advisor*.

### Ditambahkan (Operasional & Keamanan)
- **Security Model:** Menambahkan `security_model.md` untuk menjelaskan perlindungan kredensial *SQLite Vault* dengan AES-256.
- **Backup & Recovery:** Menambahkan panduan mitigasi data di `backup_and_recovery.md`.
- **Architecture Overview:** Menambahkan tinjauan sistem teknis dasar (Python, PyQt6, SQLite) di `architecture_overview.md`.
- **CLI Guide:** Menambahkan *cheat sheet* baris perintah RouterOS tingkat lanjut di `mikrotik_cli_guide.md` (Termasuk sertifikat API-SSL dan *Emergency Kick*).

### Ditambahkan (Validasi Lapangan)
- **Compatibility Matrix:** Menambahkan `mikrotik_compatibility_matrix.md` untuk merangkum kompatibilitas per versi RouterOS (v6.49.x, v7.x) dan tipe perangkat keras.
- **Validation Program:** Menyusun prosedur pengujian kesiapan rilis di lingkungan produksi pada `real_world_validation_program.md`.
- **Beta Checklist:** Menambahkan daftar periksa spesifik penguji Beta pada `beta_test_checklist.md`.

### Disempurnakan (Positioning & Legal)
- Mengunci narasi produk sebagai **"Local-First MikroTik Network Operations Platform"**, bukan sekadar *"Winbox Companion"*.
- Membuang terminologi "Pengujian VM/Mencari Bug" dan menggantinya dengan **"Release Readiness Validation"**.
- Melengkapi seluruh halaman legal esensial (EULA, Terms of Service, Privacy Policy, Refund Policy, dan Trademark Notes) untuk kesiapan peluncuran komersial.
