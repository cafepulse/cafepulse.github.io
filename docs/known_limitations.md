# Known Limitations (Batasan Sistem)

Transparansi adalah kunci. Dokumen ini merangkum apa yang *bisa* dan **tidak bisa** dilakukan oleh CafePulse saat ini. Kami mendesain CafePulse secara khusus untuk manajemen jaringan tamu dan hotspot, bukan sebagai pengganti alat jaringan lengkap.

> [!IMPORTANT]
> CafePulse telah melalui pengujian pengembangan dan validasi laboratorium internal secara komprehensif. Fase **Real World Validation** bertujuan memperluas cakupan pengujian ke berbagai model perangkat keras MikroTik dan kondisi jaringan produksi yang beragam guna memverifikasi kesiapan rilis secara utuh.

## 1. Bukan Pengganti Winbox
CafePulse tidak didesain untuk menggantikan **Winbox** atau antarmuka WebFig MikroTik.
* Anda tidak bisa mengkonfigurasi routing (OSPF, BGP).
* Anda tidak bisa melakukan setup awal interfaces (Ethernet, VLAN) dari nol melalui CafePulse.
* Anda tetap membutuhkan Winbox untuk manajemen infrastruktur inti router Anda.

## 2. Manajemen Firewall Terbatas
CafePulse secara otomatis dapat menerapkan aturan isolasi pengguna dan *rate limiting* yang berhubungan langsung dengan profil hotspot. Namun:
* Anda tidak bisa mengelola NAT rules secara bebas.
* Konfigurasi Mangle tingkat lanjut dan Queue Trees yang sangat spesifik harus tetap diatur via Winbox.

## 3. Kompatibilitas Sistem Lawas
* **Tidak Mendukung RouterOS v5:** Infrastruktur CafePulse mensyaratkan mekanisme keamanan API yang hanya stabil dimulai dari RouterOS v6.48+.
* **Legacy RouterBOARD:** Perangkat keras lawas dengan RAM di bawah 32MB atau arsitektur usang mungkin tidak merespons *polling* data jaringan waktu-nyata dengan cukup cepat, menyebabkan *API Timeout* atau *Connection Drop* di antarmuka CafePulse.

## 4. Dukungan CAPsMAN
Saat ini (Phase 5), CafePulse difokuskan pada pemantauan akses hotspot langsung dari Router Gateway/Controller utama.
* Pemantauan lalu-lintas klien *per-Access Point* (AP) individual yang dikontrol melalui **CAPsMAN belum didukung sepenuhnya**.
* Fitur CAPsMAN topology view direncanakan untuk pembaruan CafePulse Professional Edition di masa mendatang.

Jika Anda memiliki skenario spesifik yang menurut Anda seharusnya didukung tetapi gagal berjalan, silakan rujuk ke [Beta Tester Program](./beta_tester_program.md) untuk meminta penambahan fitur.
