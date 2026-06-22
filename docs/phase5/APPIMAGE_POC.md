# AppImage Proof of Concept (PoC) Documentation — CafePulse
### *Targeting Linux Distribution Foundation (Sprint 1) — Locked: Juni 2026*

---

## 1. PENDAHULUAN

AppImage adalah format paket aplikasi portabel Linux yang tidak memerlukan instalasi. Panduan ini menjelaskan struktur pembuatan **AppDir** CafePulse dan kompilasi manual/otomatis menggunakan `appimagetool` untuk menghasilkan berkas target `CafePulse_Free.AppImage` dan `CafePulse_Professional.AppImage`.

---

## 2. STRUKTUR APPDIR

AppDir adalah representasi direktori dari filesystem virtual yang akan dibungkus oleh AppImage. Struktur direktori wajib disusun sebagai berikut sebelum kompilasi:

```
AppDir/
  ├── AppRun                 # Skrip runner eksekusi utama (Executable + chmod +x)
  ├── CafePulse.desktop      # Berkas metadata integrasi desktop Linux
  ├── cafepulse.png          # Logo ikon aplikasi resolusi tinggi (256x256)
  └── usr/
        ├── bin/             # Folder target binary hasil PyInstaller
        │     ├── CafePulse  # Biner eksekusi utama hasil kompilasi
        │     └── _internal/ # Dependensi PyQt6, numpy, dll. (PyInstaller folder)
        └── share/
              └── icons/     # Ikon sistem (opsional)
```

---

## 3. IMPLEMENTASI METADATA & RUNNER

### 3.1 Skrip Runner (`AppRun`)
Buat berkas bernama `AppRun` tepat di root folder `AppDir/` dan isi dengan shell script berikut:

```bash
#!/bin/sh
# Temukan letak path absolut dari direktori AppImage saat diekstrak ke /tmp oleh kernel
HERE="$(dirname "$(readlink -f "${0}")")"

# Eksekusi biner utama CafePulse dengan meneruskan argumen dari CLI
exec "${HERE}/usr/bin/CafePulse" "$@"
```
> [!IMPORTANT]
> Jangan lupa memberikan izin eksekusi pada skrip: `chmod +x AppDir/AppRun`

### 3.2 Berkas Desktop (`CafePulse.desktop`)
Buat berkas bernama `CafePulse.desktop` di root folder `AppDir/` untuk integrasi menu desktop Linux:

```ini
[Desktop Entry]
Type=Application
Name=CafePulse
Comment=CafePulse Network Operations & Hotspot Analytics Platform
Exec=CafePulse
Icon=cafepulse
Terminal=false
Categories=Network;Utility;System;
```

### 3.3 Ikon Aplikasi (`cafepulse.png`)
Salin logo PNG resolusi tinggi dari `assets/branding/logo.png` ke root `AppDir/` dengan nama `cafepulse.png`.

---

## 4. PROSES PACKAGING APPIMAGE

Ikuti langkah berikut pada sistem operasi Linux (atau dalam workflow GitHub Actions):

### Langkah 1: Unduh `appimagetool`
```bash
# Unduh biner tool resmi AppImageKit
wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

### Langkah 2: Ekstrak Tool (Menghindari Dependensi FUSE di CI)
Di dalam GitHub Actions runner, FUSE (Filesystem in Userspace) tidak terpasang secara default, sehingga AppImage tool tidak bisa dieksekusi langsung. Kita harus mengekstraksinya terlebih dahulu:
```bash
./appimagetool-x86_64.AppImage --appimage-extract
# Hasil ekstraksi akan berada di folder `squashfs-root/`
```

### Langkah 3: Asosiasikan Biner Hasil PyInstaller
Pindahkan direktori hasil build PyInstaller dari `dist/CafePulse` ke struktur `AppDir`:
```bash
mkdir -p AppDir/usr/bin
cp -r dist/CafePulse/* AppDir/usr/bin/
```

### Langkah 4: Jalankan Kompilasi AppImage
Jalankan perintah pengemasan AppDir menjadi satu file tunggal:
```bash
# Jalankan AppRun dari squashfs-root untuk melakukan kompilasi AppImage
./squashfs-root/AppRun AppDir CafePulse_Free.AppImage
```
Perintah di atas akan menghasilkan berkas biner portable final **`CafePulse_Free.AppImage`** di direktori kerja Anda.

---

## 5. VERIFIKASI EKSEKUSI (LAUNCH CHECKLIST)

Untuk memastikan AppImage berjalan dengan baik di komputer Linux pengguna:
1. Pindahkan berkas ke folder manapun.
2. Buka Terminal dan jalankan:
   ```bash
   chmod +x CafePulse_Free.AppImage
   ./CafePulse_Free.AppImage
   ```
3. Verifikasi UI PyQt6 memuat splash screen dan dasbor analitik utama termuat dengan lancar tanpa crash pustaka dynamic library.
