# Founder User Journey Simulation Report

**Profil:** Saya adalah Founder User baru yang awam terhadap CafePulse.

## 1. Menemukan Website
* **Tindakan:** Mengunjungi `cafepulse.github.io` berdasarkan undangan Discord.
* **Pengalaman:** Layout sederhana. Halaman *Pricing* tertera Rp499.000 untuk 1 PC dengan update gratis selama 5 tahun. Tidak ada kendala berarti.
* **Titik Kebingungan:** Tidak ada tombol "Beli Langsung" (*Direct Checkout*). Saya diarahkan untuk membaca panduan bahwa pembelian butuh ekspor `.licreq` terlebih dahulu. Ini sedikit aneh bagi saya yang biasa membeli software dengan metode *add to cart* standar.

## 2. Mengunduh CafePulse
* **Tindakan:** Mengunjungi laman Download. Terdapat tab Windows dan Linux.
* **Pengalaman:** Terdapat 4 opsi untuk Windows: Free Setup, Free Portable, Pro Setup, Pro Portable.
* **Titik Kebingungan:** Karena saya ingin menjadi Founder (berlisensi Premium), apakah saya harus langsung mendownload *Professional Setup*? Jika saya download versi Pro, apakah bisa langsung dipakai? Jawabannya ada pada peringatan (yang perlu saya baca teliti) bahwa versi Pro butuh HWID lisensi dari awal. Saya harus mengerti alurnya.

## 3. Instalasi (Windows)
* **Tindakan:** Mengklik `CafePulse_Professional_Setup.exe`.
* **Pengalaman:** Muncul *Blue Screen* Windows SmartScreen "Windows protected your PC".
* **Titik Kebingungan:** *Friction* paling tinggi! Jika saya tidak membaca `INSTALLATION_GUIDE.md`, saya mungkin akan membatalkan instalasi karena takut *malware*. Instruksi mengklik "More info" > "Run anyway" adalah penyelamat satu-satunya.

## 4. Aktivasi Lisensi (First Launch)
* **Tindakan:** Membuka aplikasi, lalu diminta aktivasi.
* **Pengalaman:** Saya masuk ke tab Licensing. Mengekspor `.licreq`. Lalu saya harus ke website/menghubungi developer untuk menyerahkan file ini. Setelah membayar, saya menerima `license.lic` via email, dan mengimpornya kembali ke aplikasi.
* **Titik Kebingungan:** Prosesnya manual. Saya harus menunggu balasan email dari Developer. Ini menunda momen "Aha!" saya dalam menggunakan aplikasi.

## 5. Fitur Utama (Koneksi Router)
* **Tindakan:** Membuka tab Connection, mencoba menambah Router.
* **Pengalaman:** Saya mengetikkan IP `192.168.1.1` dan menekan "Test". Berhasil.
* **Titik Kebingungan:** Jika koneksi API (`8728`) di Winbox saya dimatikan, aplikasinya hanya memberikan status "Gagal koneksi" tanpa ada petunjuk bahwa saya harus membuka Winbox ➔ IP ➔ Services. (Untungnya hal ini tertulis rapi di `FIRST_LAUNCH_GUIDE.md`).

## 6. Umpan Balik & Pelaporan Bug
* **Tindakan:** Saya menemukan *crash* dan masuk ke Discord.
* **Pengalaman:** Saya melihat `BUG_REPORT_TEMPLATE.md` di _pinned message_ Discord.
* **Titik Kebingungan:** Saya harus menekan `Win+R` dan mengetik `%LOCALAPPDATA%\CafePulse\logs` untuk mencari log. Untuk pengguna non-teknis ini merepotkan, namun karena target pasarnya adalah teknisi jaringan (Network Engineer), ini adalah friksi yang masih wajar dan mudah diikuti.

**Kesimpulan Simulasi:** Friksi paling utama adalah **Windows SmartScreen** dan alur lisensi asinkron **HWID-Exchange**. Keduanya mutlak diatasi melalui edukasi yang kuat pada website dan email *welcome onboarding*.
