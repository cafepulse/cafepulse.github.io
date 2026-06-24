# Known Issues & FAQ

Dokumen ini merangkum isu-isu perangkat lunak yang telah diketahui (sedang dalam perbaikan) serta pertanyaan umum (FAQ) dari para pengguna penguji (*Beta Testers*).

---

## Known Issues (Isu yang Diketahui)

### 1. Pesan Peringatan "Safe Mode" Sering Muncul
**Deskripsi:** Jika OS Windows Anda *crash* atau aplikasi ditutup secara paksa via Task Manager, pada peluncuran berikutnya aplikasi mungkin meminta *booting* ke Safe Mode.
**Workaround:** Klik **"No, boot normally"** jika Anda yakin *database* tidak korup. Tim sedang mengembangkan mekanisme penutupan anggun (*graceful shutdown*) yang lebih baik pada *thread* latar belakang.

### 2. Rendering UI Mengecil pada Monitor 4K
**Deskripsi:** Pada beberapa instalasi Windows 10/11 dengan layar beresolusi 4K (DPI di atas 150%), font di tabel *Dashboard* terlihat sangat kecil.
**Workaround:** Klik kanan *shortcut* CafePulse -> *Properties* -> *Compatibility* -> *Change high DPI settings* -> Centang *Override high DPI scaling behavior* (Pilih *System*).

---

## Frequently Asked Questions (FAQ)

**T: Apakah CafePulse bisa mengubah *routing* atau alamat IP WAN?**
J: Tidak. CafePulse adalah alat operasi Hotspot. Untuk *routing* kompleks, Anda tetap harus menggunakan Winbox.

**T: Apakah saya perlu menginstal web server (XAMPP/MySQL)?**
J: Tidak! CafePulse adalah aplikasi mandiri. Semuanya sudah berada di dalam satu *executable*.

**T: Apakah kunci lisensi Professional saya berlaku selamanya?**
J: Ya. Model lisensi kami adalah *One-Time Purchase* (Satu Kali Beli).

**T: Mengapa koneksi RouterOS sering *Timeout*?**
J: Pastikan CPU Router MikroTik Anda tidak sedang 100%, dan pastikan Anda menggunakan port API yang benar (8728) atau (8729 untuk SSL).
