# PROPOSAL KOLABORASI EVALUASI TEKNIS: ADVISOR PROGRAM (V2.0)
## **CAFEPULSE — LOCAL-FIRST MIKROTIK OPERATIONS PLATFORM**

---

### **HALAMAN 1: COVER PAGE**

**Logo Proyek:**
`assets/logo.png`

**Judul Utama:**
# CAFEPULSE
## Local-First MikroTik Operations Platform

**Subjudul:**
### Technical Advisor Collaboration Proposal

**Detail Dokumen:**
*   **Disiapkan Untuk:** Mas Nanang (NanangMrk)  
    *Edukator MikroTik & Praktisi Jaringan Indonesia*
*   **Disiapkan Oleh:** Youbellkey  
    *Solo Developer & Inisiator Proyek CafePulse*
*   **Email Kontak:** `cafepulse.network@gmail.com`
*   **Situs Resmi:** [https://cafepulse.github.io/](https://cafepulse.github.io/)
*   **Tanggal Dokumen:** Juni 2026

---

### **HALAMAN 2: EXECUTIVE SUMMARY**

CafePulse adalah platform operasi jaringan MikroTik lokal (*Local-First MikroTik Network Operations Platform*) berbasis desktop yang dirancang secara mandiri untuk menyederhanakan manajemen operasional jaringan secara terintegrasi dan aman. Proyek ini diinisiasi secara mandiri (*solo developer*) guna membantu pemilik usaha kecil hingga menengah—seperti RT/RW Net, warnet, hotspot UMKM, dan sekolah—dalam menjalankan tugas administratif operasional jaringan harian secara mudah, aman, dan tanpa biaya langganan bulanan (*one-time purchase*).

Kami memahami bahwa integritas teknis, keamanan kredensial, dan keandalan adalah prioritas mutlak dalam administrasi jaringan. Oleh karena itu, kami bermaksud mengundang Mas Nanang bergabung secara privat sebagai **Technical Advisor** sebelum peluncuran resmi versi v1.0 stabil. Kolaborasi evaluatif ini berfokus pada validasi aspek keamanan RouterOS API, pengujian performa database lokal, serta penyelarasan fungsional generator voucher agar benar-benar menjawab tantangan nyata para teknisi di lapangan.

#### **Ringkasan Kolaborasi (Briefing Box):**
*   **Project Type:** Local-First MikroTik Network Operations Platform (Aplikasi Desktop)
*   **Developer:** Youbellkey (Solo Developer)
*   **Target Market:** RT/RW Net, Hotspot UMKM, Administrator Jaringan Lokal
*   **Business Model:** Free Edition (Permanen) + Professional Edition (Lisensi Sekali Bayar)
*   **Advisor Request:** Evaluasi Keamanan API & Uji Coba Fungsional Lab (Tanpa Target Komersial)

---

### **HALAMAN 3: PROBLEM STATEMENT**

#### **Tantangan Operasional Jaringan MikroTik di Lapangan**
Di pasar infrastruktur internet Indonesia, MikroTik RouterOS merupakan tulang punggung utama. Namun, pengelolaan jaringan harian sering menghadapi hambatan nyata:
1.  **Kurva Pembelajaran Manajemen Jaringan:** Bagi operator non-teknis (pemilik kafe, staf sekolah, atau pengelola RT/RW Net pemula), pengelolaan parameter jaringan harian melalui antarmuka konfigurasi tingkat tinggi terlalu rumit dan membingungkan.
2.  **Risiko Operasional Akibat Akses Penuh:** Memberikan akses konfigurasi router tingkat tinggi secara bebas kepada operator non-teknis meningkatkan risiko kesalahan fatal yang dapat memicu *downtime* jaringan secara tidak sengaja.
3.  **Ketiadaan Riwayat Monitoring Persisten:** Data statistik bandwidth di RouterOS bawaan akan hilang ketika router di-reboot, menghambat analisis performa jangka panjang.
4.  **Generasi Voucher Hotspot yang Kaku:** Pembuatan voucher massal bawaan RouterOS terasa kaku, tidak memiliki visualisasi ramah pengguna, dan memerlukan integrasi eksternal untuk pencetakan siap cetak.

> **Risiko Operasional Akses:**
> Menyerahkan akses langsung ke konsol konfigurasi router kepada operator non-teknis adalah risiko operasional utama. Diperlukan platform operasional terisolasi (*operational workspace*) yang membatasi hak kontrol hanya pada fungsi administratif harian.

---

### **HALAMAN 4: SOLUTION OVERVIEW**

#### **Ruang Kerja Operasional MikroTik Mandiri**
CafePulse hadir sebagai ruang kerja operasional (*operational workspace*) mandiri yang mengintegrasikan RouterOS API secara aman untuk menangani tugas administratif harian. Aplikasi desktop lokal ini menyederhanakan pemantauan bandwidth, pembuatan voucher, dan manajemen klien dari satu dasbor visual terpadu.

**Dasbor Utama CafePulse:**
`assets/screenshots/dashboard_overview.png`
*Caption: Gambar 4.1: Dasbor Utama menyajikan visualisasi bandwidth real-time, status router, pemantauan resource, dan pintasan voucher hotspot secara instan.*

CafePulse dirancang untuk memisahkan kontrol konfigurasi tingkat tinggi dengan kebutuhan operasional harian. Aplikasi ini bertindak sebagai ruang kerja terisolasi yang melindungi stabilitas jaringan dari risiko kesalahan operasional manusia.

---

### **HALAMAN 5: KEY CAPABILITIES**

#### **Fitur Utama CafePulse**
CafePulse memadukan fungsionalitas pemantauan persisten dengan kemudahan manajemen voucher massal.

**Tampilan Hotspot Generator:**
`assets/screenshots/hotspot_generator.png`
*Caption: Gambar 5.1: Antarmuka pembuatan voucher hotspot massal terintegrasi.*

*   **Voucher Engine Terintegrasi:** Pembuatan ratusan voucher hotspot massal dengan template khusus yang siap diekspor menjadi berkas PDF siap cetak dalam hitungan detik.
*   **Monitoring Bandwidth Persisten:** Statistik lalu lintas bandwidth disimpan secara berkala ke database lokal (`cafepulse.db`), memastikan data analitik tetap utuh meskipun router di-reboot.
*   **Pencadangan Konfigurasi Otomatis:** Penjadwalan backup file konfigurasi router secara otomatis langsung di dalam penyimpanan router secara berkala, memastikan ketersediaan cadangan konfigurasi saat terjadi kegagalan sistem.
*   **Pemindai Jaringan Terintegrasi:** Deteksi status perangkat di subnet lokal secara cepat guna mengidentifikasi pengguna asing atau anomali jaringan melalui rantai fallback deteksi subnet offline 6-tahap.

---

### **HALAMAN 6: LOCAL-FIRST DESIGN PHILOSOPHY**

#### **Filosofi Desain Local-First**
Dalam administrasi jaringan, privasi data dan kedaulatan infrastruktur adalah hal mutlak. Berbeda dengan platform monitoring berbasis cloud (SaaS) yang memaksa kredensial router dikirim ke internet, CafePulse dirancang dengan pendekatan **Local-First & Offline-Capable**:

```
[ PC Operator / Desktop Client ] 
       │ (Menjalankan Aplikasi CafePulse & Database SQLite Lokal)
       ▼ (Koneksi Enkripsi RouterOS API - Port 8728/8729)
[ Router MikroTik / RouterOS ]
       x (TIDAK ADA data kredensial atau statistik dikirim ke Cloud)
```

#### **Mengapa Local-First Penting bagi Jaringan Anda:**
*   **Kedaulatan Data Penuh (Data Control):** Semua data operasional, kredensial, dan metrik disimpan secara lokal pada database SQLite pengguna (`cafepulse.db`). Tidak ada data sensitif yang dikirim ke server luar.
*   **Kemampuan Offline Total (Offline-Capable):** Seluruh modul inti—monitoring, generator voucher, scanning, dan backup—tetap berfungsi penuh tanpa ketergantungan pada koneksi internet luar.
*   **Enkripsi Kredensial Lokal:** Informasi kredensial API router disimpan lokal dengan enkripsi simetris standar industri (Fernet / AES-128) yang diikat secara kriptografis pada identitas perangkat keras (`MachineGuid` registri Windows).
*   **Lisensi Kriptografi Offline (RSA-4096):** Verifikasi status lisensi dilakukan secara matematis menggunakan kunci publik asimetris secara lokal, tanpa tracking internet periodik.

---

### **HALAMAN 7: WHY NANANGMRK**

#### **Umpan Balik Teknis yang Terarah dan Objektif**
Kanal YouTube dan forum edukasi Mas Nanang adalah standar emas bagi ribuan teknisi jaringan di Indonesia. Reputasi Mas Nanang dibangun atas dasar analisis kritis, objektivitas pengujian laboratorium, dan solusi praktis yang terbukti di lapangan.

Kami menghubungi Mas Nanang bukan untuk meminta publisitas promosi komersial atau sponsor video. Kami mencari masukan kritis dari seorang **praktisi senior** secara privat untuk mengevaluasi:
1.  **Integritas Keamanan:** Apakah penanganan API RouterOS oleh CafePulse sudah mematuhi praktik terbaik keselamatan jaringan dan isolasi API user?
2.  **Efektivitas Fungsional:** Apakah generator voucher dan layout PDF pencetakan kami sudah cukup andal untuk digunakan pengelola RT/RW Net di pelosok?
3.  **Kritik Arsitektur:** Masukan terkait pembagian thread background worker asinkron PyQt6 agar aplikasi tetap responsif dan bebas dari kebocoran memori.

---

### **HALAMAN 8: ADVISOR TERMS & BOUNDARIES**

Kami sangat menghargai waktu dan keahlian profesional Anda. Kolaborasi evaluasi teknis ini dirancang secara fleksibel, berorientasi pada kontribusi teknis timbal balik, tanpa beban komitmen pemasaran:

| Kontribusi Yang Diharapkan | Benefit & Pengakuan Advisor |
| :--- | :--- |
| **Pengujian Lab Mandiri**<br>Menguji CafePulse menggunakan RouterBOARD cadangan di lab simulasi Anda. | **Complimentary Lifetime License**<br>Akses lisensi Professional penuh secara gratis selamanya untuk keperluan lab personal Anda. |
| **Umpan Balik Teknis**<br>Memberikan masukan tertulis terkait stabilitas API, database, atau alur UI/UX. | **Technical Advisor Recognition**<br>Pencantuman nama resmi di halaman "Technical Advisor" dalam aplikasi dan situs web resmi. |

#### **Batasan Kolaborasi Terjamin (Collaboration Boundaries):**
*   **[✓] Tanpa Konten Video Sponsor:** Mas Nanang tidak memiliki kewajiban membuat video ulasan di YouTube.
*   **[✓] Tanpa Kewajiban Promosi:** Tidak ada keharusan membagikan link unduhan atau merekomendasikan produk di forum Anda.
*   **[✓] Tanpa Skema Afiliasi Komersial:** Hubungan murni bersifat evaluatif teknis, tanpa target penjualan atau komisi komersial.
*   **[✓] Kebebasan Partisipasi:** Anda berhak memberikan umpan balik secara tertutup dan menarik diri kapan saja jika kesibukan utama Anda tidak memungkinkan.

---

### **HALAMAN 9: MENGAPA SAYA MEMBANGUN CAFEPULSE**

Perjalanan pengembangan CafePulse dimulai dari pengamatan sederhana di lapangan. Sebagai pengembang yang sering berinteraksi dengan komunitas teknologi lokal, saya melihat bagaimana para pemilik usaha kecil menengah (seperti RT/RW Net, warnet, dan hotspot UMKM) berjuang mengelola infrastruktur jaringan mereka. MikroTik RouterOS adalah tulang punggung yang sangat andal, namun kurva pembelajaran konfigurasi terlalu tinggi bagi operator non-teknis. Staf administrasi sering kali harus mengakses konsol router hanya untuk mencetak voucher hotspot atau memantau penggunaan data harian, yang memicu risiko kesalahan konfigurasi secara tidak sengaja.

Saya melihat adanya kesenjangan antara kompleksitas konfigurasi jaringan dan kesederhanaan operasional bisnis harian. Hal ini mendorong saya untuk membangun CafePulse sebagai ruang kerja operasional terisolasi (*operational workspace*) yang ramah visual.

Dalam proses pengembangannya, saya berkomitmen pada tiga prinsip utama:
*   **Filosofi Local-First:** Keamanan jaringan tidak boleh dikompromikan oleh awan (cloud). Kredensial dan metrik jaringan harus tetap berada 100% di bawah kendali operator lokal.
*   **Fokus Solusi Praktis:** Mengutamakan fitur-fitur yang langsung memecahkan masalah harian, seperti voucher engine PDF siap cetak, monitoring bandwidth persisten dengan SQLite WAL, dan network subnet scanning offline.
*   **Komitmen Jangka Panjang:** Sebagai solo developer, saya mendedikasikan proyek ini untuk mendukung digitalisasi UMKM Indonesia melalui model lisensi sekali bayar (*one-time purchase*) yang berkelanjutan, menjamin CafePulse terus dipelihara dan diperbarui tanpa beban langganan bulanan.

---

### **HALAMAN 10: NEXT STEP**

#### **Alur Kerja Sama Evaluatif**
Untuk memulai kolaborasi evaluatif ini, kami merancang langkah-langkah praktis berikut:

1.  **Peninjauan Proposal:** Mas Nanang meninjau proposal kolaborasi evaluatif privat ini.
2.  **Diskusi Singkat:** Obrolan tertulis santai melalui email untuk klarifikasi pertanyaan awal.
3.  **Pengiriman Build & Lisensi:** Kami mengirimkan installer CafePulse Professional (.exe/.zip) beserta file lisensi aktivasi offline.
4.  **Uji Coba Lab:** Mas Nanang menjalankan aplikasi di lab menggunakan router simulator cadangan.
5.  **Penyampaian Feedback:** Pengiriman kritik teknis, saran optimasi, atau temuan bug secara berkala via email/chat kapan pun sempat.

---

### **HALAMAN 11: APPENDIX**

#### **Appendix: Pemindai Jaringan**
Sebagai bagian dari fungsionalitas pendukung, CafePulse menyertakan pemindai subnet lokal untuk memetakan perangkat aktif secara asinkron tanpa mengganggu aktivitas monitoring utama.

**Pemindai Subnet Lokal (Network Scan):**
`assets/screenshots/network_scan.png`
*Caption: Gambar 11.1: Modul pemindaian jaringan lokal menyajikan daftar IP aktif, MAC Address, dan vendor perangkat secara real-time.*

Modul ini membantu pengelola jaringan mengidentifikasi perangkat terhubung secara visual dan mengaudit keamanan subnet lokal secara cepat.

---

### **HALAMAN 12: CLOSING PAGE**

**Logo Proyek:**
`assets/logo.png`

## **CafePulse**
### *Local-First MikroTik Network Operations Platform*

---

#### **Informasi Kontak & Akses:**
*   **Website:** [https://cafepulse.github.io/](https://cafepulse.github.io/)
*   **Email:** `cafepulse.network@gmail.com`
*   **Developer:** Youbellkey (Solo Developer)

**Terima kasih atas segala dedikasi Mas Nanang bagi kemajuan edukasi dunia jaringan di Indonesia.**
