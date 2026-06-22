# Founder Testing Guide
### *Pedoman Pengujian untuk Founder User CafePulse*

Terima kasih telah menjadi bagian dari **CafePulse Founder Program**. 
Versi yang Anda unduh saat ini adalah versi _Pre-Release_ (Beta Tertutup). 

## 1. Tujuan Program Founder
Tujuan utama keterlibatan Anda adalah membantu kami menemukan titik buta (_blind spots_) yang tidak terlihat oleh developer. Fokus kami pada fase ini bukanlah mempercantik tampilan, melainkan memastikan bahwa alat yang sangat esensial bagi teknisi jaringan berjalan tanpa celah:
- Stabilitas deteksi IP/MAC lokal.
- Kestabilan membaca beban CPU/RAM Router.
- Efisiensi alat *bulk generator* Voucher Hotspot.
- Pengalaman aktivasi lisensi *offline* secara mulus.

## 2. Area Pengujian Fokus (Penting)
Saat menjalankan aplikasi, kami sangat menghargai jika Anda dapat memusatkan pengujian pada aspek berikut:
1. **Instalasi:** Apakah Windows Defender/SmartScreen menahan aplikasi terlalu lama? Apakah panduan memadai?
2. **Konektivitas:** Apakah profil MikroTik Anda tersimpan dan terbaca dengan baik?
3. **Polling CPU/Traffic:** Apakah grafik *dashboard* bergerak mulus dan akurat sesuai Winbox?
4. **Offline ARP Sweep:** Coba putuskan koneksi internet PC Anda (tetapi tetap terhubung ke router via LAN), jalankan _Network Sweep_ dari Sidebar, dan pastikan IP/MAC lokal tetap terdeteksi.
5. **PDF Voucher Engine:** Generate 100+ voucher, dan evaluasi hasil ekspor berkas PDF-nya.

## 3. Cara Memberikan Feedback & Melaporkan Bug
Karena ini adalah versi pra-rilis, sistem pelaporan masalah tidak dilakukan dari dalam aplikasi. Kami menyediakan jalur komunikasi *direct* melalui **Discord/Telegram khusus Founder**.

### Mengajukan Feedback (Saran / Kritik UX)
Jika Anda merasa ada desain yang kaku, lambat, atau fitur yang membingungkan, gunakan format template `FEEDBACK_TEMPLATE.md` dan kirimkan ke kanal `#feedback`.

### Melaporkan Bug (Error / Crash)
Jika aplikasi terhenti tiba-tiba (_crash_), kehilangan data, atau tombol tidak berfungsi, mohon gunakan kerangka `BUG_REPORT_TEMPLATE.md`.
**Sangat Penting:** Lampirkan selalu file `cafepulse.log` atau `crash.log` Anda! File ini tidak mengandung kata sandi Anda dan sangat vital bagi teknisi kami untuk melacak baris kode penyebab kerusakan.
- **Lokasi Log (Windows):** Tekan `Win + R`, ketik `%LOCALAPPDATA%\CafePulse\logs`, tekan Enter.
- **Lokasi Log (Linux):** `~/.local/share/CafePulse/logs/`

Kejelian Anda mengamankan fondasi CafePulse menuju perangkat lunak profesional. Sekali lagi, terima kasih!
