# CAFEPULSE LAUNCH PLAYBOOK
### *Panduan Eksekusi Peluncuran Produk — v1.0.0 | Juni 2026*

---

## OVERVIEW

Dokumen ini adalah panduan operasional step-by-step untuk peluncuran CafePulse v1.0.0. Setiap item diberi owner, deadline relatif (T = hari launch), dan status tracking.

---

## PHASE T-30: PERSIAPAN FINAL (30 HARI SEBELUM LAUNCH)

### 🏗️ Product Readiness

| # | Task | Owner | Status |
|---|---|---|---|
| 1 | Semua Phase 1-3 features implemented & tested | Dev | ✅ |
| 2 | Stress test 24 jam selesai tanpa memory leak | Dev | 📋 |
| 3 | Zero critical bugs open | Dev | 🔄 |
| 4 | Installer Free Edition berjalan di Windows 10/11 fresh install | Dev | ✅ |
| 5 | Installer Professional Edition berjalan & aktivasi lisensi works | Dev | ✅ |
| 6 | Uninstall bersih (tidak meninggalkan registry sampah) | Dev | 📋 |

### 📄 Legal & Compliance

| # | Task | Owner | Status |
|---|---|---|---|
| 7 | EULA (End User License Agreement) final & approved | Dev | 📋 |
| 8 | Privacy Policy published di website | Dev | 📋 |
| 9 | Terms of Service published | Dev | 📋 |
| 10 | Copyright notice dalam aplikasi dan installer | Dev | ✅ |

### 🌐 Website & Download

| # | Task | Owner | Status |
|---|---|---|---|
| 11 | cafepulse.github.io live dan semua halaman accessible | Dev | ✅ |
| 12 | Download buttons di download.html berfungsi | Dev | ✅ |
| 13 | Pricing page akurat (harga, fitur matrix) | Dev | ✅ |
| 14 | Contact form atau email yang berfungsi | Dev | ✅ |
| 15 | Screenshot terbaru di halaman produk | Dev | 📋 |

---

## PHASE T-14: KOMUNIKASI & KOMUNITAS (14 HARI SEBELUM)

### 📱 Social Media & Community Prep

| # | Task | Owner | Status |
|---|---|---|---|
| 16 | Discord server setup: channels, roles, welcome message | Dev | 📋 |
| 17 | Email blast ke 50 beta tester (preview + launch date) | Dev | 📋 |
| 18 | Draft postingan Facebook (grup MikroTik Indonesia) | Dev | 📋 |
| 19 | Demo video YouTube diproduksi & diupload | Dev | 📋 |
| 20 | Affiliate program link aktif & tracking working | Dev | 📋 |

### 💳 Payment System

| # | Task | Owner | Status |
|---|---|---|---|
| 21 | Payment gateway terintegrasi (atau manual via transfer) | Dev | 📋 |
| 22 | Test payment end-to-end: QRIS / Transfer Bank | Dev | 📋 |
| 23 | Automated license key delivery via email berfungsi | Dev | 📋 |
| 24 | Invoice/kwitansi template siap | Dev | 📋 |

---

## PHASE T-7: FINAL CHECKS (7 HARI SEBELUM)

### 🧪 Quality Assurance

| # | Task | Verifikasi |
|---|---|---|
| 25 | Full test suite passed | `pytest tests/ -v` → semua hijau |
| 26 | Manual smoke test checklist | Lihat Section 6 di bawah |
| 27 | Download di website berfungsi | Download dari HP & laptop berbeda |
| 28 | License activation flow end-to-end | Install → activate → verify Pro features |
| 29 | Backup dan recovery flow | Create backup → restore → verifikasi |

### 📝 Documentation

| # | Task | Status |
|---|---|---|
| 30 | README.md final & akurat | 📋 |
| 31 | Quick Start Guide ada di website | 📋 |
| 32 | Troubleshooting FAQ published | 📋 |
| 33 | CHANGELOG.md v1.0.0 entry sudah ada | 📋 |

---

## LAUNCH DAY (T=0)

### ⏰ Launch Day Timeline

```
08:00 — Final build verification (download dari website, test install)
09:00 — Push "Live" announcement di Discord
09:30 — Post di Facebook grup MikroTik Indonesia
10:00 — Post di Facebook grup Teknisi Jaringan Indonesia
10:30 — Post di Facebook grup Warnet & Hotspot Indonesia
11:00 — Reply semua komentar/pertanyaan di semua platform
13:00 — Monitor download stats & first buyer reports
15:00 — Respond ke support requests (max response 4 jam)
18:00 — Day 1 recap: berapa download, berapa buyers, isu apa yang muncul
20:00 — Deploy hotfix jika ada critical bug yang ditemukan
```

### 🚨 Contingency Plans

**Jika ada critical bug di launch day:**
1. Immediately pull download dari website (ganti dengan pesan "Brief maintenance")
2. Fix bug → build ulang → re-upload dalam 4 jam
3. Komunikasi transparan ke Discord: "Found and fixing issue X"
4. Extend Founder period pricing 3 hari sebagai kompensasi

**Jika payment gateway bermasalah:**
1. Segera switch ke metode manual: transfer bank langsung
2. Update website dengan instruksi transfer manual
3. Kirim email ke yang sudah tertarik dengan instruksi alternatif

---

## POST-LAUNCH (T+1 HINGGA T+30)

### 📊 Day 1-7 Priorities

| # | Task | Frekuensi |
|---|---|---|
| 1 | Monitor bug reports & crash logs | Setiap 4 jam |
| 2 | Respond support requests | Max 24 jam |
| 3 | Deploy hotfixes jika diperlukan | As needed |
| 4 | Engage dengan pengguna baru di Discord | Harian |
| 5 | Track conversion metrics | Harian |

### 📈 Week 2-4 Priorities

| # | Task | Frekuensi |
|---|---|---|
| 1 | Survey kepuasan pengguna (Google Form ke buyers) | Sekali di minggu 2 |
| 2 | Release v1.0.1 patch (bug fixes dari feedback launch) | Minggu 2-3 |
| 3 | Rekrut affiliate partners aktif | Mingguan |
| 4 | Engage YouTuber untuk review/sponsorship | Mingguan |
| 5 | Track NPS dan update roadmap jika perlu | Akhir bulan |

---

## SMOKE TEST CHECKLIST (MANUAL QA)

Sebelum launch, lakukan manual test ini di mesin yang BERSIH (fresh install):

### Free Edition Smoke Test

- [ ] Install dari `CafePulse_Free_Setup.exe` — selesai tanpa error
- [ ] Aplikasi berjalan dari Start Menu shortcut
- [ ] Splash screen muncul dan hilang dengan normal
- [ ] Dashboard terbuka dengan data demo yang terlihat
- [ ] Scan jaringan berhasil mendeteksi minimal 1 device
- [ ] Tidak ada CMD/terminal window muncul saat scanning
- [ ] Tutup aplikasi — tidak muncul dialog "not properly closed" saat dibuka kembali
- [ ] Uninstall bersih dari Control Panel

### Professional Edition Smoke Test

- [ ] Install dari `CafePulse_Professional_Setup.exe`
- [ ] Masukkan license key → aktivasi berhasil
- [ ] Koneksi ke router MikroTik berhasil (butuh router fisik/VM)
- [ ] Hotspot user list terbuka dan menampilkan data live
- [ ] Generate 10 voucher → export PDF berhasil
- [ ] Manual backup ke MikroTik berhasil
- [ ] Semua fitur Free Edition masih berfungsi

---

*Dokumen Launch Playbook CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
