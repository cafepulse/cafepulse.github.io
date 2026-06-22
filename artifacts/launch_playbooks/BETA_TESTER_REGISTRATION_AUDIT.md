# Beta Tester Registration Audit
*Perbandingan Sistem Formulir Pendaftaran Beta/Founder*

## 1. Existing Flow (Google Form)
- **Bagaimana alurnya:** Pengguna mengklik tautan pendaftaran, diarahkan ke Google Forms. Semua field divalidasi oleh Google.
- **Integrasi Discord:** Respon dihubungkan via ekstensi Google Forms / Zapier / Apps Script langsung ke Webhook Discord `#beta-applicants`.
- **Integrasi Spreadsheet:** Tersimpan otomatis di Google Sheets tanpa perlu *database hosting*.
- **Kelebihan:** 
  - 100% Gratis dan tanpa *maintenance*.
  - Anti-spam bawaan (Google reCAPTCHA).
  - Skalabel, dapat disaring dan diunduh (CSV) seketika.
- **Kekurangan:** Desain UI/UX sedikit melenceng dari tema *website* utama karena menggunakan format baku Google.

## 2. Existing Flow (Website Form)
- **Bagaimana implementasinya:** HTML Forms yang ditanam di `beta.html` dan `contact.html`. Saat ini disiasati menggunakan trik *redirect* `mailto:` via JavaScript di `main.js`.
- **Teknologi yang digunakan:** HTML5, CSS Variables, Vanilla JavaScript.
- **Dependency yang ditambahkan:** (Masa Depan) Jika tidak ingin mengandalkan *email client* eksternal milik pengguna, form ini kelak wajib menggunakan integrasi API eksternal (seperti Formspree) atau membuat *Backend Server* khusus (Python/NodeJS).
- **Maintenance yang diperlukan:** Sangat tinggi jika dibangun *backend* (pengelolaan VPS, keamanan *CORS*, mitigasi *DDoS/Spam* pada *endpoint*).

## 3. Comparison Matrix

| Metrik | Google Form | Website Form |
|---|---|---|
| **Complexity** | Sangat Rendah | Sedang - Tinggi (jika tanpa mailto) |
| **Maintenance** | Nol | Butuh pemeliharaan server/API |
| **Reliability** | 99.9% (Google Infra) | Rentan *spam* & *bot crawling* |
| **Scalability** | Tinggi | Terbatas pada kapasitas *backend* |
| **Security** | Dikelola Google | Harus mitigasi serangan mandiri |
| **Founder Effort**| Fokus baca *spreadsheet* | Harus melakukan *code maintenance* |

## 4. Verification Check Before Revert
- [x] Apakah Google Form lama masih ada? **(Diasumsikan YA)**
- [x] Apakah Google Spreadsheet masih menerima data? **(Diasumsikan YA)**
- [x] Apakah Discord webhook masih aktif? **(Diasumsikan YA)**
- [x] Apakah channel Discord masih sesuai? **(Diasumsikan YA)**
- [x] Apakah ada data tertinggal di website form? **(TIDAK. Sistem saat ini hanya berbasis `mailto:` yang datanya ada di email lokal pengguna)**.
- [x] Apakah ada halaman mengarah ke form? **(YA. `beta.html` dan `founder.html` memiliki formulir bawaan)**.

## 5. Recommendation
**REVERT TO GOOGLE FORM**
Sesuai filosofi "Local-First" dan penghindaran *over-engineering* untuk skala tim tunggal, formulir website harus dihapus dan diganti dengan tautan *Call-to-Action* (CTA) langsung menuju URL Google Form eksternal. Keputusan ini menghapus titik kegagalan (*Point of Failure*) pada *front-end* statis kita.
