# Founder Release Checklist
### *Panduan Final Kesiapan Rilis Founder Edition*

Gunakan checklist ini untuk memverifikasi kesiapan CafePulse sebelum secara resmi didistribusikan kepada Founder/Beta Tester.

## 1. Build & Compilation
- [ ] PyInstaller berhasil membangun biner Windows (`.exe`) tanpa peringatan dependensi kritis.
- [ ] Skrip `build.py` berhasil memutus *cache* sebelum *build* (Pembersihan `build/` dan `dist/`).
- [ ] Versi aplikasi (di dalam `version.py`) telah disuntikkan secara dinamis ke skrip Inno Setup (`.iss`).
- [ ] Linux AppImage berhasil dikompilasi (x86_64) via GitHub Actions.

## 2. Installer & Packaging
- [ ] Inno Setup Windows (`CafePulse_Professional_Setup.exe`) dapat berjalan di PC segar tanpa *error*.
- [ ] Portable Windows (`.zip`) berisi semua *runtime* dan dapat langsung dijalankan tanpa hak administrator.
- [ ] Aplikasi menulis ke direktori aman `%LOCALAPPDATA%\CafePulse` dan tidak *crash* akibat perlindungan folder `C:\Program Files`.
- [ ] Skrip eksekusi Linux (`chmod +x`) sukses dijalankan.

## 3. Licensing System (RSA-4096)
- [ ] Modul penangkap *Hardware ID* (HWID) menghasilkan string unik berbasis komponen mesin.
- [ ] Ekspor file `.licreq` sukses ditulis ke _Desktop_ atau dokumen pengguna.
- [ ] Skrip sisi-server / manual (`issue_license.py`) sukses membaca `.licreq` dan memproduksi `.lic`.
- [ ] Proses impor file `.lic` di klien terverifikasi sukses mengubah versi aplikasi dari *Free* menjadi *Professional* secara permanen (tanpa *restart* paksa).

## 4. Documentation & Founder Guidance
- [ ] `INSTALLATION_GUIDE.md` siap dibaca dan tautan unduhan relevan tersedia.
- [ ] `FIRST_LAUNCH_GUIDE.md` tersedia untuk menuntun pengguna mengatur profil router.
- [ ] `FOUNDER_TESTING_GUIDE.md` tersedia untuk menuntun fokus pengujian Founder.
- [ ] Template pelaporan `BUG_REPORT_TEMPLATE.md` dan `FEEDBACK_TEMPLATE.md` tersedia.

## 5. Public Website & GitHub Pages
- [ ] Domain / URL GitHub Pages CafePulse aktif dan memuat desain terbaru.
- [ ] Tautan `download` pada website mengarah secara presisi ke *Release Asset* GitHub.
- [ ] Halaman *Pricing* mendeskripsikan secara jelas perbedaan fitur *Free* vs *Professional*.
- [ ] Tautan *Discord Community* aktif dan valid.

## 6. Release Assets & Integrity
- [ ] *Draft Release* di repositori GitHub memuat file `.exe`, `.zip`, dan `.AppImage`.
- [ ] File `SHA256SUMS.txt` telah dihasilkan dan disematkan di halaman rilis.
- [ ] *Release Notes* (Changelog) menyertakan informasi bahwa ini adalah build *Founder Edition / RC1.2*.

## 7. Founder Delivery Package
- [ ] *Welcome Email* / Pesan Discord kepada tester berisi ucapan terima kasih dan instruksi *download*.
- [ ] Penyerahan salinan berkas instruksi instalasi dan pedoman umpan balik.
- [ ] Persetujuan kerahasiaan / etika *tester* (opsional, untuk mencegah penyebaran rilis tertutup).
