# AUDIT ALINEASI PROPOSAL KOLABORASI — CAFEPULSE

Dokumen ini menyajikan hasil audit kepatuhan total terhadap naskah proposal kolaborasi **CafePulse v2.0** (`NANANGMRK_ADVISOR_PROPOSAL_V2.md` dan bodi HTML pada `generate_proposal_pdf.py`) berdasarkan dokumen *Single Source of Truth* (SSOT) yang telah disepakati sebelumnya (`PROPOSAL_STATE_NANANGMRK.md`, `PARTNERSHIP_ARCHITECTURE_NANANGMRK.md`, `SOURCE_OF_TRUTH_MAP.md`, dan `DECISION_LOG.md`).

---

## 1. Temuan Kritis

*   **Penyimpangan Positioning Proyek:** Proposal v2.0 masih menggunakan istilah "Winbox Companion" dan "pendamping setia Winbox" sebanyak 6 kali. Ini bertentangan dengan evolusi CafePulse sebagai platform operasi mandiri berbasis integrasi RouterOS API.
*   **Persepsi Ketergantungan (Dependency Perception):** Redaksi kalimat pada masalah dan solusi membuat CafePulse terkesan seperti bungkusan kosmetik (*wrapper*) atau shortcut Winbox, bukannya sebuah ruang kerja operasional (*operational workspace*) terisolasi.
*   **Ketidakakuratan Klaim Teknis (Technical Misalignment):**
    1.  *Klaim AES-256:* Proposal menyebutkan kredensial disimpan dengan "AES-256 tingkat militer". Secara faktual di kode (`credential_store.py`), enkripsi simetris menggunakan **Fernet (AES-128)** yang diikat ke `MachineGuid` Windows Registry.
    2.  *Klaim Backup PC Lokal:* Proposal menyebutkan scheduled backups "langsung disimpan ke penyimpanan PC lokal". Secara faktual di kode (`devices_page.py` / `BackupWorker`), pencadangan dieksekusi di sisi router MikroTik memanfaatkan perintah API `/system/backup/save`. Pemindahan biner otomatis ke folder PC lokal belum diimplementasikan di v1.0.
*   **Framing Hubungan Kemitraan (Advisor Hubris):** Beberapa istilah seperti "Hubungan Kemitraan" (*Partnership*), "Kemitraan Teknis", dan "Metadata Kemitraan" memberikan kesan rekrutmen bisnis yang terlalu berat, padahal tujuannya adalah meminta masukan evaluasi teknis privat (*Technical & Product Feedback*).
*   **Ketiadaan Founder Story:** Proposal tidak memuat halaman cerita pendiri (*Founder Story*), sehingga kehilangan jangkar kepercayaan personal (*trust anchor*) yang sangat penting bagi seorang solo developer.

---

## 2. Ketidaksesuaian dengan SSOT

| Elemen Proposal | Wording v2.0 Saat Ini | Kepatuhan SSOT / Decision Log | Rekomendasi Tindakan |
| :--- | :--- | :--- | :--- |
| **Positioning Produk** | "Winbox Companion" / "Pendamping Winbox" | **Tidak Patuh**. SSOT menegaskan CafePulse adalah platform mandiri: *"Local-First MikroTik Network Operations Platform"*. | Ganti seluruh istilah companion dengan platform operasi lokal mandiri. |
| **Klaim Enkripsi** | "AES-256 tingkat militer" | **Tidak Patuh**. Kode menggunakan `cryptography.fernet` yang menggunakan AES-128. | Ubah menjadi "Enkripsi simetris standar industri (Fernet/AES-128) terikat mesin lokal". |
| **Klaim Backup** | "Disimpan langsung ke penyimpanan PC lokal" | **Tidak Patuh**. Backup saat ini dibuat dan disimpan di memori router itu sendiri via API. | Ubah menjadi "Pencadangan konfigurasi terjadwal langsung di penyimpanan router". |
| **Advisor Framing** | "Metadata Kemitraan", "Kemitraan Teknis" | **Tidak Patuh**. SSOT `PROPOSAL_STATE` menyarankan framing *Technical/Product Advisor Program*. | Ganti menjadi "Detail Dokumen", "Umpan Balik Teknis", atau "Kolaborasi Evaluatif". |
| **Struktur Halaman** | Halaman 8 & 9 terpisah, tidak ada Founder Story | **Tidak Patuh**. SSOT meminta Founder Story masuk tanpa merusak target tata letak 12 halaman. | Gabungkan Halaman 8 & 9 lama menjadi satu halaman, gunakan slot kosong untuk Founder Story. |

---

## 3. Hasil Global Positioning & Dependency Audit (Task 1 & 2)

Daftar kalimat lama yang diidentifikasi melanggar positioning dan usulan revisinya:

### Temuan 1: Halaman 2 (Executive Summary)
*   **Kalimat Lama (Line 31):**
    > "CafePulse adalah platform operasi desktop *local-first* yang dirancang sebagai pendamping setia Winbox (*Winbox Companion*) untuk menyederhanakan manajemen operasional jaringan MikroTik di Indonesia."
*   **Kalimat Baru:**
    > "CafePulse adalah platform operasi jaringan MikroTik lokal (*Local-First MikroTik Network Operations Platform*) berbasis desktop yang dirancang untuk menyederhanakan manajemen operasional harian secara mandiri dan aman."
*   **Alasan Perubahan:** Menggeser positioning produk ke arah platform operasi mandiri dan menghapus sebutan wrapper/companion.

### Temuan 2: Halaman 2 (Briefing Box)
*   **Kalimat Lama (Line 36):**
    > "\* **Project Type:** Aplikasi Desktop Operasional Jaringan (Winbox Companion)"
*   **Kalimat Baru:**
    > "\* **Project Type:** Local-First MikroTik Network Operations Platform (Aplikasi Desktop)"
*   **Alasan Perubahan:** Menghilangkan sebutan Winbox Companion pada data metadata.

### Temuan 3: Halaman 3 (Problem Statement)
*   **Kalimat Lama (Line 48-49):**
    > "1. **Kompleksitas Antarmuka Winbox:** Bagi operator non-teknis..., Winbox terlalu rumit...\n2. **Risiko Salah Konfigurasi:** Memberikan hak akses Winbox penuh..."
*   **Kalimat Baru:**
    > "1. **Kurva Pembelajaran Manajemen Jaringan:** Bagi operator non-teknis..., pengelolaan parameter jaringan harian melalui antarmuka konfigurasi tingkat tinggi terlalu rumit...\n2. **Risiko Operasional Akibat Akses Penuh:** Memberikan akses konfigurasi router tingkat tinggi secara bebas kepada operator..."
*   **Alasan Perubahan:** Menghapus framing bahwa Winbox adalah "masalah utama", diganti dengan kompleksitas manajemen jaringan umum dan risiko operasional akibat akses yang tidak dibatasi.

### Temuan 4: Halaman 3 (Problem Callout)
*   **Kalimat Lama (Line 53-54):**
    > "Menyerahkan akses router langsung kepada operator non-teknis adalah titik lemah keamanan. Diperlukan lapisan perantara aman yang membatasi kontrol hanya pada fungsi operasional harian."
*   **Kalimat Baru:**
    > "Menyerahkan akses langsung ke konsol konfigurasi router kepada operator non-teknis adalah risiko operasional utama. Diperlukan platform operasional terisolasi (*operational workspace*) yang membatasi hak kontrol hanya pada fungsi administratif harian."
*   **Alasan Perubahan:** Menghapus istilah "lapisan perantara" yang menurunkan nilai produk menjadi wrapper pasif. Menggunakan istilah "operational workspace".

### Temuan 5: Halaman 4 (Solution Overview - Judul & Paragraf)
*   **Kalimat Lama (Line 60-61):**
    > "#### **Pendamping Setia Winbox (Winbox Companion)**\nCafePulse hadir sebagai jembatan operasional yang memisahkan konfigurasi sensitif (Winbox) dari tugas administratif harian..."
*   **Kalimat Baru:**
    > "#### **Ruang Kerja Operasional MikroTik Mandiri**\nCafePulse hadir sebagai ruang kerja operasional (*operational workspace*) mandiri yang mengintegrasikan RouterOS API secara aman untuk menangani tugas administratif harian..."
*   **Alasan Perubahan:** Mempertegas identitas platform mandiri yang terintegrasi langsung dengan API RouterOS.

### Temuan 6: Halaman 4 (Solution Overview - Paragraf Penutup)
*   **Kalimat Lama (Line 67):**
    > "CafePulse tidak bertujuan untuk menggantikan peran Winbox dalam konfigurasi jaringan tingkat tinggi. Sebaliknya, aplikasi ini menjadi filter pelindung operasional bagi operator harian."
*   **Kalimat Baru:**
    > "CafePulse dirancang untuk memisahkan kontrol konfigurasi tingkat tinggi dengan kebutuhan operasional harian. Aplikasi ini bertindak sebagai ruang kerja terisolasi yang melindungi stabilitas jaringan dari risiko kesalahan operasional manusia."
*   **Alasan Perubahan:** Menghapus kalimat defensif "tidak bertujuan menggantikan Winbox" yang memperlemah positioning produk.

---

## 4. Hasil Audit Klaim Teknis (Task 4)

Klasifikasi kebenaran klaim teknis pada CafePulse:

### [A] Implemented and Verified (Dapat Dipertahankan & Diterangkan Akurat)
*   **RSA-4096 Licensing Engine:** Menggunakan verifikasi tanda tangan digital asimetris RSA-4096 dengan padding PSS dan hash SHA-256 untuk memvalidasi berkas `.lic` secara offline (Sesuai [D-001]).
*   **Hardware Fingerprint (HWID):** Lisensi diikat secara kriptografis pada identitas perangkat keras (`MachineGuid` di registri Windows dengan fallback MAC Address `uuid.getnode()`).
*   **Offline Subnet Detection Fallback Chain:** Deteksi IP gateway dan subnet LAN secara dinamis melalui 6-stage fallback chain tanpa koneksi internet (Sesuai [D-005]).
*   **SQLite WAL Mode Persistence:** Riwayat statistik monitoring disimpan secara persisten ke database lokal (`cafepulse.db`) dalam mode Write-Ahead Logging untuk menghindari konflik thread I/O (Sesuai [D-002]).

### [B] Implemented but Details Misrepresented (Harus Direvisi)
*   **AES-256 Credential Encryption:** Di proposal tertulis "AES-256". Kode program menggunakan pustaka `cryptography.fernet` yang mengimplementasikan **AES-128** dalam mode CBC dengan penandatanganan HMAC-SHA256.
    *   *Tindakan:* Ubah kata "AES-256 tingkat militer" menjadi "Enkripsi simetris standar industri (Fernet/AES-128) terikat mesin lokal".

### [C] Planned but Present in Current Proposal (Harus Disesuaikan/Dihapus)
*   **Local PC Backup Storage:** Di proposal tertulis backup scheduled "langsung disimpan ke penyimpanan PC lokal tanpa cloud". Saat ini biner program hanya mengirim instruksi API `/system/backup/save` yang menyimpan berkas di memori internal router MikroTik. Proses penarikan otomatis (.backup transfer) ke direktori lokal PC belum selesai diuji.
    *   *Tindakan:* Ubah menjadi "Pencadangan konfigurasi terjadwal otomatis di dalam penyimpanan router secara berkala".

### [D] Marketing Assumption (Harus Dihapus)
*   *Penggunaan Jargon "Tingkat Militer" (Military Grade):* Istilah ini menurunkan kredibilitas engineering di depan praktisi senior.
    *   *Tindakan:* Hapus kata "tingkat militer" dari seluruh dokumen.

---

## 5. Rekomendasi Revisi Halaman & Struktur Layout (Task 3, 5, 6 & 7)

Untuk menjaga estetika dan mempertahankan total halaman tepat **12 Halaman** (sesuai tata letak pencetakan `generate_proposal_pdf.py` saat ini) tanpa menyisakan ruang kosong yang canggung:

### Rencana Restrukturisasi Halaman:
1.  **Halaman 1:** Cover Page (Tetap)
2.  **Halaman 2:** Executive Summary (Posisi produk diperbaiki)
3.  **Halaman 3:** Masalah yang Ingin Diselesaikan (Dependency Winbox dihilangkan)
4.  **Halaman 4:** Apa Itu CafePulse (Solution Overview, positioning mandiri)
5.  **Halaman 5:** Kemampuan Utama (Claim backup disesuaikan)
6.  **Halaman 6:** **Filosofi Desain Local-First** (Menggantikan "Local-First Architecture" lama dengan poin eksplisit tentang Data Control, Offline-Capable, No Subscription, dan Kriptografi RSA).
7.  **Halaman 7:** Mengapa NanangMrk? (Framing diperhalus ke arah evaluasi ahli)
8.  **Halaman 8:** **Ketentuan & Batasan Kolaborasi** (Penggabungan tabel *Advisor Invitation* dan checklist *Collaboration Boundaries* lama agar muat di satu halaman padat dan bernilai tinggi).
9.  **Halaman 9:** **Mengapa Saya Membangun CafePulse** (NEW — Founder Story yang personal namun profesional, menjelaskan latar belakang solo developer, empati pada UMKM, dan komitmen jangka panjang).
10. **Halaman 10:** Langkah Selanjutnya (Next Step - Alur evaluasi lab mandiri)
11. **Halaman 11:** Appendix: Pemindai Jaringan (Menghapus dependensi visual Winbox)
12. **Halaman 12:** Closing Page (Perbaikan positioning penutup)

---

## 6. Penilaian Kepatuhan Proposal (Scoring)

| Aspek Penilaian | Skor Sebelum Audit | Skor Setelah Audit (Target) | Catatan Perubahan Utama |
| :--- | :--- | :--- | :--- |
| **Global Positioning** | 4 / 10 | 10 / 10 | Menghapus sebutan "Winbox Companion" dan "pendamping". Pemosisian penuh sebagai platform operasi lokal mandiri. |
| **Dependency Perception** | 5 / 10 | 10 / 10 | Menghapus narasi "tidak menggantikan Winbox" dan "shortcut menu Winbox" di Appendix. |
| **Local-First Alignment** | 7 / 10 | 10 / 10 | Penjelasan eksplisit mengenai kedaulatan data (data control), offline total, dan lisensi offline tanpa pelacakan. |
| **Technical Claims** | 6 / 10 | 10 / 10 | Koreksi faktual AES-256 menjadi AES-128 Fernet, serta memosisikan backup pada penyimpanan internal router (bukan PC lokal). |
| **Advisor Framing** | 6 / 10 | 10 / 10 | Mengganti istilah kemitraan formal (*partnership*) dengan review teknis privat. |
| **Founder Story** | 0 / 10 | 10 / 10 | Penambahan halaman "Mengapa Saya Membangun CafePulse" untuk membangun kepercayaan personal. |
| **Layout & Page Integrity** | 9 / 10 | 10 / 10 | Penggabungan halaman minor menjadi satu halaman padat, menyisakan slot halaman 9 yang pas untuk Founder Story tanpa mengubah target total 12 halaman. |
| **RATA-RATA SKOR** | **5.3 / 10** | **10 / 10** | **Peningkatan Kredibilitas Total di Depan Praktisi Senior** |
