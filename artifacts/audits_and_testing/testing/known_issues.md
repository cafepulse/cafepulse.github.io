# CafePulse Known Issues

Daftar masalah yang telah diketahui (sedang dalam perbaikan atau sengaja ditoleransi untuk sementara karena keterbatasan teknis). Dokumen ini berguna bagi tim pendukung (Support) ketika merespons laporan dari pengguna.

### 1. `Issue_ID: KI-001` - Jeda 2 Detik saat Menutup Aplikasi
**Deskripsi**: Ketika pengguna menekan tombol (X) untuk keluar dari CafePulse, jendela terkadang membutuhkan waktu hingga 2-3 detik untuk benar-benar tertutup.
**Status**: Ditoleransi (Wajar).
**Penjelasan**: Ini merupakan bagian dari fitur *Safe Shutdown*. Aplikasi sedang memblokir penutupan paksa agar *worker* (seperti MikroTik API) bisa menyelesaikan *loop* ping terakhir dan mengamankan koneksi sebelum mematikan diri secara elegan.

### 2. `Issue_ID: KI-002` - Npcap Permission di Windows
**Deskripsi**: Beberapa fitur tingkat rendah tidak bisa berjalan jika aplikasi dijalankan tanpa hak *Administrator*.
**Status**: Sedang dicari solusi (*Workaround* tersedia).
**Penjelasan**: Pengguna disarankan untuk mengatur properti ikon CafePulse agar selalu **Run as Administrator**.

### 3. `Issue_ID: KI-003` - Antivirus False Positive
**Deskripsi**: Karena CafePulse melakukan pemindaian jaringan (*arp scan*, *ping* bertubi-tubi), beberapa Antivirus menganggapnya sebagai *Port Scanner* atau aplikasi mencurigakan.
**Status**: Ditoleransi.
**Penjelasan**: Ini wajar bagi aplikasi tipe Network Management System. Solusi sementaranya adalah mendaftarkan CafePulse ke dalam *Whitelist* (Pengecualian) Antivirus pengguna.
