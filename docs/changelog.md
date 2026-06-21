# CafePulse Beta Changelog (Catatan Perubahan)

Daftar perbaikan bug, fitur baru, dan penyempurnaan teknis yang telah diterapkan di rilis beta terbaru CafePulse (RC1.2 / v1.1.0-alpha.1).

---

## [1.1.0-alpha.1] - Juni 2026

### Perbaikan Bug (Bug Fixes)
- **Headless PyQt6 Linux Build Crash:** Menyelesaikan crash runner headless Ubuntu dengan menyuntikkan env `QT_QPA_PLATFORM: offscreen` dan menginstal pustaka dependen Qt6 (`libxcb-cursor0`).
- **AppImageKit 404:** Memperbaiki link unduhan `appimagetool` CI/CD workflow yang patah ke repositori aktif baru.
- **PyInstaller Cache Conflict (pyimod02_importers):** Menambahkan langkah *clean sweep* folder build (`build/` & `dist/`) di Windows bat script untuk mencegah konflik file cache impor yang memicu crash `.exe`.
- **Offline Subnet Sweep Error:** Mengatasi error "No network sweep base" saat client offline dengan mengimplementasikan rantai fallback 6-tahap (6-stage local subnet fallback chain).
- **Directory Nesting Cleanup:** Menghapus folder duplikat level 3 untuk memusatkan source code dan mencegah overhead kompilasi.

### Peningkatan Sistem (Improvements)
- **Linux AppImage Distribution:** Pipeline rilis otomatis berhasil menghasilkan biner portabel `CafePulse_Free.AppImage` dan `CafePulse_Professional.AppImage` siap jalan.
- **Unified SHA256 Manifest:** Checksum file manifest `SHA256SUMS.txt` sekarang dibuat otomatis lewat skrip Python lintas platform agar line endings selalu seragam.
- **Platform-Agnostic RSA Licensing:** Mengintegrasikan sistem penandatanganan offline RSA-4096 terpusat yang bekerja secara identik di sistem operasi Windows maupun Linux.
