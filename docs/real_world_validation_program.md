# Real World Validation Program

Dokumen ini merupakan tindak lanjut dari proposal pengujian lapangan (*Field Validation Proposal*) yang melibatkan pengujian stabilitas CafePulse secara operasional pada lingkungan jaringan komersial berbeban menengah.

> [!IMPORTANT]
> CafePulse telah melalui pengujian pengembangan dan validasi laboratorium internal. Fase **Real World Validation** bertujuan memperluas cakupan pengujian ke berbagai model perangkat MikroTik, versi RouterOS, dan kondisi jaringan produksi yang beragam untuk memastikan *Release Readiness* (Kesiapan Rilis).

## 1. Tujuan Pengujian

| Area Validasi          | Tujuan                                                            |
| ---------------------- | ----------------------------------------------------------------- |
| RouterOS Compatibility | Memastikan fungsi berjalan konsisten pada berbagai versi RouterOS |
| Hardware Compatibility | Memastikan fungsi berjalan pada berbagai seri RouterBOARD         |
| Stability Testing      | Mengamati kestabilan penggunaan jangka panjang                    |
| Monitoring Accuracy    | Memverifikasi akurasi data monitoring                             |
| Network Discovery      | Memastikan hasil pemindaian jaringan konsisten                    |
| Hotspot Operations     | Memastikan fitur hotspot berjalan sesuai ekspektasi               |

## 2. Target Jaringan Pengujian
Kami merekomendasikan program ini dilakukan oleh *Beta Tester* / *Founder* pada lingkungan nyata berikut:
* **Jenis Jaringan:** Warung Kopi / Cafe / Coworking Space / Asrama (Sistem *Hotspot Voucher* wajib aktif).
* **Jumlah Pengguna:** Rata-rata 20 hingga 80 perangkat aktif bersamaan per hari.
* **Perangkat Keras Router:** Minimal kelas hAP ac2, hEX (RB750Gr3), atau seri RB4011/RB1100.

## 3. Checklist Validasi Lapangan
Para tester lapangan diharapkan untuk mengeksekusi skenario berikut selama setidaknya 7 hari beruntun:
- [ ] Meninggalkan PC operator dalam keadaan menyala dengan CafePulse terhubung ke router.
- [ ] Membuat *batch* 50 voucher, lalu 100 voucher, untuk melihat respons antarmuka.
- [ ] Menguji fitur deteksi perangkat tak dikenal (*Rogue Device/Network Scan*).
- [ ] Menggunakan fitur Kick/Disconnect Klien langsung dari CafePulse UI.

## 4. Cara Pelaporan Hasil
Kami menyarankan pelaporan visual untuk mendukung validasi ini. Mohon kumpulkan hasil pengujian dan kirimkan melalui *channel* pelaporan resmi kami dengan melampirkan *screenshot* berikut:
* **Tangkapan Layar 1:** Halaman *Dashboard* utama setelah CafePulse berjalan tanpa dimatikan selama 3 hingga 7 hari (terlihat indikator koneksi & *uptime*).
* **Tangkapan Layar 2:** Hasil halaman *Active Devices* dengan beban puluhan klien (sensor privasi MAC/IP sebagian diperbolehkan).
* **Tangkapan Layar 3:** Hasil *generate voucher* atau halaman fitur *Hotspot Voucher Generator*.
* **Tangkapan Layar 4 (Opsional):** Hasil dari fungsi *Network Scan* /*Device Discovery*.

## 5. Dokumentasi Sukarela

Jika berkenan, penguji dapat membantu menyediakan:
* Screenshot Dashboard
* Screenshot Network Scan
* Screenshot Device Discovery
* Screenshot Hotspot Generator
* Informasi model router
* Versi RouterOS

Tujuannya adalah murni untuk:
1. Validasi kompatibilitas silang perangkat keras.
2. Mempercepat reproduksi masalah jika ditemui.
3. Penyempurnaan dokumentasi perangkat lunak.

Terima kasih atas partisipasi Anda dalam membawa perangkat lunak operasional ini menjadi siap rilis!
