# MikroTik Compatibility Matrix

Dokumen ini memuat daftar versi RouterOS dan seri perangkat keras (Hardware) MikroTik yang kompatibel dengan CafePulse. 
Saat ini, CafePulse sedang bersiap memasuki tahap **Real World Validation**, sehingga sebagian besar kompatibilitas perangkat keras fisik masih berstatus *Pending Validation*.

## 1. Kompatibilitas RouterOS

| Versi RouterOS | Status Integrasi | Keterangan |
| :--- | :--- | :--- |
| **v7.23.x** | ✅ Internal Testing | Digunakan sebagai basis pengembangan utama |
| **v7.1x.x - v7.22.x** | ⏳ Not Yet Tested | Menunggu pengujian lapangan |
| **v6.48.x - v6.49.x** | ⏳ Not Yet Tested | Menunggu pengujian lapangan pada perangkat lawas |
| **v5.x dan di bawahnya** | ❌ Tidak Mendukung | API versi lawas tidak didukung oleh CafePulse |

*(Pembaruan CafePulse akan selalu berfokus pada pengujian versi stabil yang dirilis oleh MikroTik).*

---

## 2. Kompatibilitas Perangkat Keras (Hardware)

Meskipun CafePulse menggunakan API standar, beberapa fungsi khusus dipengaruhi oleh sumber daya perangkat keras. Tabel ini akan terus diperbarui melalui laporan dari partisipan [Real World Validation Program](./real_world_validation_program.md).

| Seri Perangkat | Status Integrasi | Catatan Khusus |
| :--- | :--- | :--- |
| **VM / x86 ISO** | ✅ Internal Testing | Basis pengujian lab internal (RouterOS v7.23) |
| **CHR (Cloud Hosted)** | ✅ Internal Testing | Arsitektur virtualisasi didukung penuh |
| **hAP Lite** (RB941) | ⏳ Not Yet Tested | Membutuhkan validasi beban CPU |
| **hAP ac2 / ac3** | ⏳ Not Yet Tested | Target pengujian utama untuk kafe ukuran sedang |
| **hEX** (RB750Gr3) | ⏳ Not Yet Tested | Target pengujian utama untuk manajemen *voucher* |
| **RB1100 Series** | ⏳ Not Yet Tested | Menunggu validasi skala Enterprise |
| **CCR Series** | ⏳ Not Yet Tested | Menunggu validasi untuk *query* ribuan *lease* |

Jika Anda menggunakan perangkat dengan status `Not Yet Tested` dan berhasil (atau menemui kendala) saat menjalankannya, mohon bantuannya untuk melaporkan hasil tersebut kepada kami melalui panduan [Real World Validation Program](./real_world_validation_program.md) agar kami dapat segera memperbarui matriks kompatibilitas di atas.
