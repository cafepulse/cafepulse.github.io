# CafePulse Regression Tracker

Sebelum merilis *update* baru yang berisikan perbaikan atau fitur tambahan, pastikan komponen-komponen inti (*Core Features*) di bawah ini tidak rusak (Regresi). 

Jika ada komponen yang berstatus `[FAIL]`, **RILIS HARUS DIBATALKAN** hingga masalah terselesaikan.

## Core Features (Pasti Benar)
- [ ] **A01**: Aplikasi bisa terbuka dengan sukses dan memuat `cafepulse.db`.
- [ ] **A02**: Demo Mode berfungsi normal dan menghasilkan *traffic* simulasi.
- [ ] **A03**: Fitur klik Kanan (*Context Menu*) pada daftar perangkat tidak rusak.
- [ ] **A04**: Halaman Dashboard menampilkan Total Devices yang sinkron dengan halaman Devices.
- [ ] **A05**: *Safe Shutdown* berfungsi: tidak ada *process* Python tertinggal di *Task Manager* setelah aplikasi ditutup.

## Integrations (Jaringan)
- [ ] **I01**: MikroTik API Login berfungsi dengan baik (autentikasi dan *fail-auth* ditangani wajar).
- [ ] **I02**: Grafik Bandwidth berjalan mulus 1 FPS.
- [ ] **I03**: Ping ke perangkat di jaringan *Home WiFi* sukses dan mengembalikan warna hijau (Online).

*(Centang semua kotak ini secara manual sebelum membuat tag rilis v1.x.x)*
