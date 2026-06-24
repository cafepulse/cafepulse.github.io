# GITHUB RELEASE READINESS CHECKLIST — CAFEPULSE
### *Execution-Ready Release Verification Log — Locked: Juni 2026*

---

## 1. PEMETAAN BERKAS RILIS & VERIFIKASI UKURAN

Sebelum membuat rilis di GitHub, pastikan berkas biner di folder lokal `exports/` memiliki nama file yang **cocok secara persis (case-sensitive)** dengan tautan unduhan di `download.html`.

Berikut adalah manifest verifikasi berkas:

| Nama File Lokal | Target Nama File Upload | Ukuran Est. | Status Verifikasi |
| :--- | :--- | :--- | :--- |
| `exports/CafePulse_Free_Setup.exe` | **`CafePulse_Free_Setup.exe`** | ~63 MB | [ ] Verified |
| `exports/CafePulse_Free_Portable.zip` | **`CafePulse_Free_Portable.zip`** | ~127 MB | [ ] Verified |
| `exports/CafePulse_Free.AppImage` | **`CafePulse_Free.AppImage`** | ~118 MB | [ ] Verified |
| `exports/CafePulse_Professional_Setup.exe` | **`CafePulse_Professional_Setup.exe`** | ~63 MB | [ ] Verified |
| `exports/CafePulse_Professional_Portable.zip` | **`CafePulse_Professional_Portable.zip`** | ~127 MB | [ ] Verified |
| `exports/CafePulse_Professional.AppImage` | **`CafePulse_Professional.AppImage`** | ~118 MB | [ ] Verified |

---

## 2. KOMPATIBILITAS TAUTAN WEBSITE

Seluruh tautan unduhan di berkas `download.html` secara keras menggunakan format pola URL GitHub sebagai berikut:
`https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/[Target_Nama_File]`

*   **PENTING:** Jika ada perbedaan 1 karakter saja (termasuk huruf kapital/kecil), browser pengguna akan memicu error **404 Not Found** saat tombol klik unduhan ditekan.

---

## 3. LANGKAH-LANGKAH OPERASIONAL PUBLIKASI RILIS (5 TAHAP)

Lakukan proses ini secara berurutan pada akun GitHub organisasi `cafepulse` sebelum mengirimkan email:

### [ ] Tahap 1: Inisiasi Draft Release
1.  Buka repositori GitHub online: `github.com/cafepulse/cafepulse.github.io`.
2.  Buka tab **Releases** di sisi kanan halaman, lalu klik **Draft a new release**.

### [ ] Tahap 2: Setup Tagging Versi
1.  Buat tag versi baru: **`v1.1.0-alpha.1`** (sesuai banner beta di `download.html`).
2.  Set target branch: **`main`**.
3.  Judul Rilis: **`CafePulse v1.1.0 Closed Beta Release`**.

### [ ] Tahap 3: Unggah Aset Biner (Upload Assets)
1.  Seret (*drag and drop*) 6 file dari folder lokal `exports/` ke kotak pengunggahan aset rilis GitHub.
2.  Tunggu hingga seluruh proses pengunggahan selesai 100%. Jangan tutup halaman sebelum proses unggah selesai.

### [ ] Tahap 4: Pengaturan Aksesibilitas
1.  Centang opsi **"Set as the latest release"** (ini wajib agar tautan `/releases/latest/download/` aktif).
2.  Centang opsi **"This is a pre-release"** (menandai status beta terkontrol).

### [ ] Tahap 5: Publikasi & Uji Coba Link
1.  Klik tombol **Publish release**.
2.  Setelah rilis aktif, kunjungi situs web: `youbellkey.github.io/cafepulse-site/download.html`.
3.  Coba klik tombol unduh untuk Windows (EXE & ZIP) dan Linux (AppImage) secara mandiri untuk mengonfirmasi pengunduhan berjalan lancar.
