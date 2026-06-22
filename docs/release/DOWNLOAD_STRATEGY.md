# CafePulse Download & Hosting Strategy

Dokumen ini menganalisis strategi distribusi biner CafePulse secara publik dari infrastruktur GitHub, mengatasi tantangan akses repositori privat, dan menjamin kestabilan link unduhan jangka panjang.

---

## 1. Tantangan Repositori Privat (Private vs Public Repo)

### 1.1 Kondisi Saat Ini
- Repositori utama program `youbellkey/CafePulse` diatur sebagai **Privat** demi melindungi kode sumber (source code) PyQt6, database schema, and logika lisensi RSA dari publik.
- Konsekuensinya, fitur GitHub Releases pada repositori privat **tidak dapat diakses oleh publik**. Upaya mengunduh aset rilis dari URL privat tanpa menyertakan Personal Access Token (PAT) akan menghasilkan error `404 Not Found` atau `403 Forbidden`.

### 1.2 Solusi Jembatan Repositori Publik
Untuk mendistribusikan berkas secara gratis, aman, dan mudah bagi pengguna akhir, CafePulse memanfaatkan repositori **publik** GitHub Pages:
`cafepulse/cafepulse.github.io`
- Repositori ini bersifat publik karena digunakan untuk meng-host website promosi CafePulse.
- Dengan menerbitkan rilis (Releases) pada repositori publik ini, seluruh aset biner (Free & Professional) dapat diunduh oleh siapa saja tanpa perlu token otentikasi.

---

## 2. Strategi URL Unduhan (Download URL Strategy)

Untuk memberikan pengalaman pengguna yang mulus pada website dan aplikasi update, dua jenis format URL unduhan digunakan secara strategis:

### 2.1 Latest Release Redirect URL (Direkomendasikan untuk Tombol Utama)
Format URL ini secara dinamis mengarahkan (redirect) browser pengguna ke aset rilis terbaru (versi tertinggi) secara otomatis.
- **URL Unduhan Free Edition Setup:**
  `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe`
- **URL Unduhan Free Edition AppImage:**
  `https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage`
- **Keuntungan Jangka Panjang:**
  - **Tinggi Kestabilan:** Tombol "Download" pada website tidak perlu diubah tautannya setiap kali developer merilis versi baru (misalnya dari `1.0.0` ke `1.0.1`). GitHub secara otomatis mengarahkan ke tag terbaru.
  - **Efisiensi:** Beban bandwidth sepenuhnya ditanggung oleh CDN global GitHub yang sangat cepat and andal, mengurangi kebutuhan hosting mandiri yang mahal.
  - **Keamanan:** Mencegah link rusak (*dead links*) akibat kesalahan pengetikan manual versi baru pada halaman HTML website.

### 2.2 Version Specific URL (Arsip Sejarah & Rollback)
Format URL ini mengarah langsung ke berkas biner versi spesifik.
- **Format:**
  `https://github.com/cafepulse/cafepulse.github.io/releases/download/[Version_Tag]/[Asset_Name]`
- **Contoh:**
  `https://github.com/cafepulse/cafepulse.github.io/releases/download/v1.0.0/CafePulse_Free_Setup.exe`
- **Kapan Digunakan:**
  - Digunakan di halaman arsip website ("Release History") untuk memungkinkan pengguna mengunduh versi lama jika versi terbaru mengalami regresi atau ketidakcocokan perangkat keras.
  - Digunakan untuk merujuk build tertentu dalam laporan bug (*bug reports*).

---

## 3. Keamanan Jalur Unduhan (Security Analysis)

Untuk memastikan bahwa strategi pengalihan unduhan aman untuk jangka panjang:
1. **Pencegahan Hijacking:** Alamat unduhan harus selalu di-hardcode ke domain resmi GitHub (`github.com/cafepulse/cafepulse.github.io`). Hindari penggunaan shortener pihak ketiga (seperti bit.ly) pada tombol unduhan utama karena dapat disabotase atau disalahgunakan untuk meluncurkan serangan phising.
2. **HTTPS Enforced:** Semua komunikasi unduhan wajib menggunakan protokol `HTTPS` (TLS 1.3) untuk mencegah modifikasi biner di tengah jalan oleh ISP nakal (Man-In-The-Middle attack).
3. **Verifikasi Hash:** Di setiap halaman rilis, manifest `SHA256SUMS.txt` wajib dicantumkan secara terbuka untuk memungkinkan verifikasi integritas lokal sebelum eksekusi program.
