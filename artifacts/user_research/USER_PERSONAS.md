# CAFEPULSE USER PERSONAS
### *User Research Document — v1.0.0 | Juni 2026*

---

> Dokumen ini mendefinisikan profil pengguna CafePulse secara mendalam, termasuk behavior, pain points, dan journey mereka. Setiap keputusan desain produk HARUS dapat dijustifikasi dengan kesesuaian terhadap minimal satu persona di sini.

---

## PERSONA 1 — "Budi" (Teknisi MikroTik Freelance)

### 📋 Profile Card

| Atribut | Detail |
|---|---|
| **Nama Persona** | Budi Santoso |
| **Usia** | 28 tahun |
| **Lokasi** | Malang, Jawa Timur |
| **Pekerjaan** | Freelance Network Technician |
| **Pendidikan** | SMK Teknik Jaringan, Bersertifikat MTCNA |
| **Penghasilan** | Rp 4-8 juta/bulan |
| **Perangkat** | Laptop Windows 10 + Smartphone Android |

### 🧠 Goals & Motivations

**Goal Utama:**
- Melayani klien lebih banyak dengan waktu yang sama
- Memberikan laporan profesional ke klien untuk membangun kepercayaan
- Mengotomatisasi tugas repetitif (backup, generate voucher massal)

**Motivasi:**
- Meningkatkan reputasi sebagai "teknisi andal" di komunitas
- Mengurangi waktu respons saat ada keluhan klien
- Mengelola 20-30 klien secara efisien tanpa "kehabisan kepala"

### 😤 Pain Points

1. **Monitoring klien terfragmentasi** — Harus buka Winbox satu-per-satu untuk cek status setiap klien
2. **Voucher generation lambat** — Buat 50 voucher di Winbox = 50 kali klik manual
3. **Tidak ada audit trail** — Tidak ada catatan siapa yang mengubah konfigurasi apa
4. **Klien minta laporan** — Sulit membuat laporan visual yang mudah dipahami oleh pemilik warnet
5. **Backup tidak terjadwal** — Sering lupa backup sebelum maintenance, panik saat konfigurasi terhapus

### 📱 Typical Day

```
07:00 — Cek WhatsApp: ada klien yang report internet lambat
07:15 — Remote ke router klien via Winbox, cek traffic
07:30 — Buat voucher batch 100 pcs untuk warnet Pak Ahmad
         (1 jam setengah, sangat melelahkan)
09:00 — Ke lokasi klien hotel untuk maintenance rutin
         Cek apakah backup terakhir ada (sering tidak ada)
10:30 — Perjalanan ke klien RT/RW Net berikutnya
12:00 — Makan siang, cek 5 grup WhatsApp keluhan klien
13:00 — Remote monitoring dari kafe, koneksi lambat jadi sering putus
16:00 — Kembali ke workshop, update spreadsheet klien manual
18:00 — Kirim "laporan" ke klien (screenshot Winbox, kurang profesional)
```

### 💡 Apa yang Diinginkan dari CafePulse?

> *"Saya mau bisa buka satu aplikasi dan langsung lihat semua router klien saya sekaligus. Mana yang bermasalah, mana yang oke. Dan bisa buat voucher 200 pcs dalam 2 menit, langsung cetak PDF."*

**Feature Priorities:**
1. Multi-router dashboard overview
2. Bulk voucher generation dengan export PDF siap cetak
3. Automated scheduled backup
4. Professional report generation untuk klien

### 💸 Willingness to Pay

**Harga:** Rp 450.000 - 500.000 (one-time, tanpa langganan)
**Trigger untuk beli:** Setelah lihat demo voucher generation di YouTube / rekomendasi teman teknisi

---

## PERSONA 2 — "Ibu Sari" (Pemilik Warnet)

### 📋 Profile Card

| Atribut | Detail |
|---|---|
| **Nama Persona** | Sari Dewi Rahayu |
| **Usia** | 42 tahun |
| **Lokasi** | Purwokerto, Jawa Tengah |
| **Pekerjaan** | Pemilik Warnet "Cyber Fast" (22 unit) |
| **Pendidikan** | SMA |
| **Penghasilan Warnet** | Rp 8-12 juta/bulan |
| **Tech Level** | Rendah-Menengah — Bisa pakai Windows, tidak paham jaringan |

### 🧠 Goals & Motivations

**Goal Utama:**
- Pastikan internet selalu lancar agar pelanggan tidak kabur
- Tahu berapa pelanggan aktif dan pendapatan per jam
- Bisa hubungi teknisi dengan cepat kalau ada masalah

**Motivasi:**
- Warnet adalah sumber pendapatan utama keluarga
- Persaingan dengan warnet lain di sekitar sangat ketat
- Ingin terlihat "profesional" di mata pelanggan

### 😤 Pain Points

1. **Tidak tahu kalau internet mati** — Sering tahu dari pelanggan yang sudah marah, terlambat
2. **Tidak bisa monitoring sendiri** — Setiap kali ada masalah harus panggil teknisi, keluar biaya
3. **Tidak tahu berapa pelanggan** — Hitung manual atau lihat kursi — tidak akurat
4. **Voucher habis saat ramai** — Teknisi tidak standby, toko tutup, kehilangan pendapatan
5. **Tidak ada laporan harian/bulanan** — Sulit tahu kapan jam sibuk untuk optimize operasional

### 💡 Apa yang Diinginkan dari CafePulse?

> *"Saya pengen ada alarm kalau internet mati, biar saya langsung telpon Mas Budi (teknisi). Dan pengen lihat sekarang ada berapa orang yang pakai internet, dari HP saya."*

**Feature Priorities:**
1. Alert otomatis saat koneksi bermasalah (notifikasi)
2. Dashboard sederhana: berapa klien aktif sekarang
3. Grafik jam ramai / jam sepi per minggu
4. Status voucher sisa

### 💸 Willingness to Pay

**Harga:** Rp 200.000 - 350.000 (dipengaruhi rekomendasi teknisi)
**Trigger untuk beli:** Teknisi yang memasang merekomendasikan + ada demo gratis di perangkatnya

---

## PERSONA 3 — "Ahmad" (Admin Jaringan RT/RW Net)

### 📋 Profile Card

| Atribut | Detail |
|---|---|
| **Nama Persona** | Ahmad Fauzi |
| **Usia** | 23 tahun |
| **Lokasi** | Sidoarjo, Jawa Timur |
| **Pekerjaan** | Admin RT/RW Net (120 pelanggan), merangkap kasir & teknisi |
| **Pendidikan** | D3 Teknik Informatika (dropout semester 5) |
| **Penghasilan** | Rp 2.5-3.5 juta/bulan |
| **Tech Level** | Menengah — Familiar dengan terminal/CLI, sudah pakai Winbox |

### 🧠 Goals & Motivations

**Goal Utama:**
- Kelola voucher hotspot untuk 120 pelanggan tanpa chaos
- Buat laporan pendapatan untuk ketua RT setiap bulan
- Deteksi pelanggan yang share password / colok kabel ilegal

### 😤 Pain Points

1. **Manajemen voucher kacau** — Google Sheets + Winbox = sering konflik data
2. **Tidak bisa deteksi abuse** — Tidak tahu kalau ada pelanggan yang share koneksi ke 5 orang
3. **Laporan ke ketua RT manual** — Copy-paste dari Winbox ke Word = 3 jam kerja
4. **Tidak ada history** — Kalau ada keluhan pelanggan bulan lalu, tidak ada data untuk dilihat
5. **Satu router, banyak masalah** — Tidak ada dashboard overview yang cepat

### 💡 Apa yang Diinginkan dari CafePulse?

> *"Saya butuh bisa lihat semua pelanggan aktif, deteksi yang curang, dan laporan otomatis. Sekarang saya mesti catat manual ke Excel, ribet banget."*

**Feature Priorities:**
1. DHCP Lease viewer dengan search & filter
2. Anomaly detection (banyak device dari satu akun)
3. Export laporan ke PDF/Excel
4. Monitoring bandwidth per user

### 💸 Willingness to Pay

**Harga:** Rp 150.000 - 300.000 (anggaran terbatas, perlu approval dari ketua RT)
**Trigger untuk beli:** Setelah coba versi free dan terbukti memudahkan pekerjaan

---

## PERSONA 4 — "Pak Doni" (Pemilik Guest House)

### 📋 Profile Card

| Atribut | Detail |
|---|---|
| **Nama Persona** | Dony Pranata |
| **Usia** | 47 tahun |
| **Lokasi** | Ubud, Bali |
| **Pekerjaan** | Pemilik Guest House 12 kamar |
| **Pendidikan** | S1 Pariwisata |
| **Occupancy Rate** | 70-85% (peak season) |
| **Tech Level** | Rendah — Delegasikan ke staf tapi ingin kontrol |

### 🧠 Goals & Motivations

**Goal Utama:**
- WiFi yang reliable = ulasan bintang 5 di Booking.com / Airbnb
- Kontrol bandwidth agar satu tamu tidak "mencuri" koneksi tamu lain
- Buat voucher WiFi kustom (branded dengan nama guest house)

### 😤 Pain Points

1. **Tamu besar bandwidth** — Satu tamu download 4K Netflix, semua kamar lambat
2. **Staf tidak bisa troubleshoot** — Saat ada masalah WiFi, staf hanya bisa hubungi pemilik
3. **Tidak ada voucher branded** — Voucher WiFi tulis tangan di kertas = tidak profesional
4. **Tidak tahu siapa terhubung** — Security concern: tamu luar masuk ke jaringan

### 💡 Apa yang Diinginkan dari CafePulse?

> *"Saya mau WiFi per kamar bisa saya batasi, dan saya mau kasih voucher WiFi dengan nama villa saya, bukan kode acak dari MikroTik."*

**Feature Priorities:**
1. Queue (bandwidth limiting) per profil/user
2. Branded voucher PDF dengan logo dan nama terhapus
3. Dashboard sederhana untuk staf (siapa yang terhubung)
4. Alert jika ada perangkat mencurigakan

### 💸 Willingness to Pay

**Harga:** Rp 350.000 - 600.000 (karena langsung impact bisnis)
**Trigger untuk beli:** Demo oleh supplier teknisi jaringan yang memasang MikroTik

---

## PERSONA 5 — "Rudi" (IT Admin Sekolah)

### 📋 Profile Card

| Atribut | Detail |
|---|---|
| **Nama Persona** | Rudi Firmansyah |
| **Usia** | 32 tahun |
| **Lokasi** | Surabaya, Jawa Timur |
| **Pekerjaan** | Staff IT SMA Negeri |
| **Pendidikan** | S1 Sistem Informasi |
| **Anggaran IT** | Rp 15-30 juta/tahun (termasuk hardware) |
| **Tech Level** | Menengah-Tinggi |

### 🧠 Goals & Motivations

**Goal Utama:**
- Pastikan lab komputer dan WiFi sekolah berfungsi optimal
- Buat laporan penggunaan internet untuk kepala sekolah
- Defend anggaran IT dengan data yang bisa dipertanggungjawabkan

### 😤 Pain Points

1. **Anggaran software terbatas** — Setiap pembelian software butuh proposal dan approval
2. **Siswa bypass pembatasan** — VPN, proxy — sulit dikontrol tanpa firewall rules yang baik
3. **Laporan kurang profesional** — Kepala sekolah minta laporan "penggunaan internet bulan ini"
4. **Downtime tidak terdokumentasi** — Tidak bisa tunjukkan ke yayasan berapa kali internet bermasalah

### 💡 Apa yang Diinginkan dari CafePulse?

> *"Saya butuh laporan penggunaan yang bisa saya tunjukkan ke kepala sekolah. Dan kalau ada masalah jaringan, saya mau ada history-nya jadi saya tidak disalahkan."*

**Feature Priorities:**
1. Comprehensive activity logs dengan export
2. PDF report generation untuk manajemen
3. Monitoring bandwidth agregat per jam/hari
4. Alert history sebagai bukti dokumentasi

### 💸 Willingness to Pay

**Harga:** Rp 100.000 - 250.000 (harus masuk anggaran, sering butuh kwitansi resmi)
**Trigger untuk beli:** Ada invoice resmi + bisa dibayar lewat transfer bank (bukan payment gateway)

---

## RINGKASAN MATRIX PERSONA

| Atribut | Budi (Teknisi) | Ibu Sari (Warnet) | Ahmad (RT/RW) | Pak Doni (Hotel) | Rudi (Sekolah) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Tech Level** | Tinggi | Rendah | Menengah | Rendah | Menengah-Tinggi |
| **WTP** | Rp 450K | Rp 300K | Rp 200K | Rp 500K | Rp 200K |
| **Primary Need** | Efisiensi multi-klien | Alert & monitoring | Voucher & laporan | Bandwidth control | Laporan & dokumentasi |
| **Discovery Channel** | YouTube / Discord | Teknisi rekomen | Teknisi rekomen | Teknisi supplier | Forum IT admin |
| **Priority Tier** | 🥇 Primary | 🥈 Secondary | 🥈 Secondary | 🥉 Tertiary | 🥉 Tertiary |

---

*Dokumen User Personas CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
