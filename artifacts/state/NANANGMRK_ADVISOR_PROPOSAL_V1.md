# PROPOSAL KOLABORASI INTELOWONGAN: ADVISOR PROGRAM
## **CAFEPULSE — LOCAL-FIRST MIKROTIK OPERATIONS PLATFORM**

---

### **1. COVER**

**Judul:**
Platform Operasi Jaringan MikroTik Lokal Indonesia: Kemitraan Penasihat Teknis (*Technical Advisor*)

**Disiapkan Untuk:**
Mas Nanang (NanangMrk)
*Edukator MikroTik & Praktisi Jaringan Indonesia*

**Disiapkan Oleh:**
Youbellkey
*Solo Developer & Inisiator Proyek CafePulse*

**Kontak:**
Email: `cafepulse.network@gmail.com`
Web: [youbellkey.github.io/cafepulse-site/](https://youbellkey.github.io/cafepulse-site/)
Tanggal: Juni 2026

---

### **2. EXECUTIVE SUMMARY**

CafePulse adalah platform operasi desktop *local-first* yang dirancang sebagai pendamping setia Winbox (*Winbox Companion*) untuk mempermudah manajemen jaringan MikroTik di Indonesia. Proyek mandiri (*solo developer*) ini dibuat untuk membantu operator jaringan skala kecil hingga menengah—seperti RT/RW Net, warnet, hotspot UMKM, dan sekolah—dalam menangani tugas operasional harian tanpa biaya langganan bulanan (*one-time purchase*).

Kami menyadari bahwa integritas teknis dan keamanan adalah segalanya di dunia jaringan. Oleh karena itu, kami ingin mengundang Mas Nanang bergabung secara privat sebagai **Technical Advisor** CafePulse sebelum meluncurkan versi v1.0 stabil ke publik. Kolaborasi ini bertujuan untuk memvalidasi sirkuit keamanan RouterOS API, menyempurnakan fitur operasional seperti *Bulk Voucher Generator*, serta memastikan CafePulse benar-benar memberikan solusi nyata bagi teknisi jaringan lokal di Indonesia.

---

### **3. APA ITU CAFEPULSE**

Di pasar lokal Indonesia, MikroTik RouterOS merupakan tulang punggung jaringan. Namun, sebagian besar pemilik usaha kecil (misalnya pemilik warnet atau pengelola hotspot sekolah) tidak mengerti cara menggunakan Winbox yang kompleks, sedangkan membiarkan mereka mengakses Winbox langsung berisiko merusak konfigurasi router secara tidak sengaja.

CafePulse hadir untuk memecahkan masalah ini dengan memisahkan lapisan konfigurasi berat (Winbox) dengan lapisan operasional harian. Sebagai **Winbox Companion**, CafePulse memungkinkan operator:
- Memantau lalu lintas data bandwidth secara visual dan mendeteksi perangkat terhubung (ARP Sweeping lokal).
- Menghasilkan ratusan voucher hotspot massal dan mengekspornya menjadi berkas PDF siap cetak dalam hitungan menit (*integrated voucher engine*).
- Menjalankan pencadangan otomatis (*scheduled backups*) secara lokal tanpa bergantung pada cloud pihak ketiga.
- Menyimpan riwayat monitoring secara persisten pada database lokal (`cafepulse.db`), sehingga data bandwidth klien tidak hilang meskipun router di-reboot.

---

### **4. MENGAPA SAYA MENGHUBUNGI ANDA**

Kanal edukasi YouTube Mas Nanang adalah rujukan utama bagi ribuan teknisi jaringan di Indonesia. Mas Nanang memiliki reputasi yang sangat dihormati karena selalu menyajikan ulasan teknis secara kritis, objektif, dan berfokus pada solusi praktis lapangan.

Saya menghubungi Mas Nanang bukan untuk meminta promosi komersial, membuat video ulasan berbayar, atau mempublikasikan link unduhan secara instan. Saya menghubungi Mas Nanang sebagai **insinyur/praktisi ahli** untuk meminta umpan balik kritis terhadap proyek lokal ini. Kami ingin memastikan:
1.  **Validasi Keamanan:** Apakah mekanisme integrasi API RouterOS yang kami gunakan sudah mematuhi standar keamanan pengujian Anda?
2.  **Kesesuaian Fitur:** Apakah fitur pencetakan voucher PDF dan pemindaian subnet lokal kami sudah sesuai dengan kebutuhan harian RT/RW Net di Indonesia?
3.  **Kritik Arsitektur:** Di bagian mana dari aplikasi desktop PyQt6 ini yang masih memiliki celah teknis atau I/O database yang perlu disempurnakan?

---

### **5. MENGAPA CAFEPULSE BERBEDA**

CafePulse dirancang sejak awal dengan filosofi yang berbeda dengan kompetitor monitoring cloud global:
*   **Local-First & Offline-First:** Aplikasi berjalan 100% di komputer pengguna. Kredensial router Anda tidak pernah dikirim ke cloud eksternal. Kami merekomendasikan penggunaan *dedicated read-only API user* di RouterOS demi isolasi keamanan lab secara mutlak.
*   **Sistem Lisensi Sekali Bayar (One-Time Purchase):** Lisensi seharga Rp499.000 (tidak ada biaya langganan bulanan/SaaS) diaktivasi 100% secara offline via kriptografi RSA-4096. 
*   **Dukungan Permanent Free Edition:** Kami menyediakan edisi gratis selamanya untuk pemindaian IP lokal, memastikan alat ini tetap berguna bagi komunitas tanpa paksaan upgrade komersial.
*   **Disiplin Rekayasa Project OS AI:** Pengembangan CafePulse mengikuti framework rekayasa perangkat lunak yang ketat dan sistematis untuk menjamin keterbacaan kode, kestabilan multi-threading worker, dan pemeliharaan jangka panjang.

---

### **6. ADVISOR INVITATION**

Kami memahami waktu Mas Nanang sangat berharga. Oleh karena itu, program penasihat ini kami rancang secara sukarela, fleksibel, dan berorientasi nilai tanpa ikatan target pemasaran:

#### **A. Kontribusi yang Kami Harapkan (Fleksibel):**
*   Mencoba CafePulse di lab pribadi Anda menggunakan RouterBOARD cadangan.
*   Memberikan kritik dan masukan teknis (baik via email atau chat tertulis) terkait celah keamanan API, kestabilan antarmuka, atau alur voucher generator.
*   Membantu kami menentukan prioritas fitur pada roadmap rilis v1.0 stabil.

#### **B. Manfaat & Privilese Advisor:**
1.  **Complimentary Lifetime License:** Kami segera memberikan lisensi Professional 5-Tahun untuk keperluan pengujian lab Anda. Setelah Anda aktif memberikan masukan teknis awal, lisensi tersebut akan ditingkatkan secara permanen menjadi *Lifetime Professional License (Local Persistence Guaranteed)*.
2.  **Technical Advisor Recognition:** Nama atau profil resmi Anda akan dicantumkan pada halaman khusus "Technical Advisor" di dalam aplikasi CafePulse dan situs web resmi kami sebagai bentuk apresiasi kontribusi Anda terhadap komunitas jaringan lokal Indonesia.
3.  **Direct Developer Access:** Saluran komunikasi langsung dengan pengembang (Youbellkey) untuk mendiskusikan roadmap produk atau mengajukan kustomisasi fitur spesifik.

#### **C. Batasan Komitmen (Bebas Tekanan):**
*   **Tidak ada kewajiban** membuat konten video di YouTube.
*   **Tidak ada kewajiban** mempromosikan CafePulse kepada pengikut Anda.
*   Hubungan ini sepenuhnya merupakan kolaborasi evaluatif demi kemajuan alat lokal Indonesia.

---

### **7. PENUTUP**

CafePulse dibangun untuk menjadi solusi praktis, aman, dan terjangkau bagi para operator jaringan lokal di Indonesia. Masukan dari Mas Nanang selaku praktisi senior akan sangat menentukan tingkat keselamatan teknis dan kegunaan aplikasi ini sebelum menyentuh tangan ribuan pengguna di Indonesia.

Jika Mas Nanang bersedia meluangkan waktu sejenak untuk berdiskusi santai atau menguji aplikasi di lab pribadi Anda, silakan hubungi kami kembali di:
Email: `cafepulse.network@gmail.com`

Terima kasih atas segala dedikasi Mas Nanang bagi edukasi dunia jaringan Indonesia.

Hormat saya,

**Youbellkey**
*Solo Developer & Inisiator CafePulse*
