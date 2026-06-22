# Error Code: ERR_MT_001
**Title**: MikroTik Connection Failed / Connection Refused

## Gejala (Symptoms)
Saat mencoba berpindah ke **MikroTik Mode**, aplikasi CafePulse memunculkan dialog error bahwa koneksi gagal atau terputus secara tiba-tiba (Connection Refused).

## Penyebab Umum
1. **IP Address Salah**: Alamat IP yang dimasukkan bukan alamat Router MikroTik yang valid.
2. **Layanan API Mati**: Layanan API di dalam RouterOS (MikroTik) belum diaktifkan.
3. **Firewall Block**: Aturan firewall komputer atau router memblokir *port* koneksi.
4. **Beda Subnet**: Komputer yang menjalankan CafePulse tidak terhubung di jaringan yang sama dengan Router.

## Solusi & Langkah Perbaikan
1. **Periksa IP**: Buka CMD dan ketik `ping <ip-mikrotik>`. Pastikan ada balasan (*Reply*).
2. **Aktifkan API**:
   - Buka aplikasi **Winbox**.
   - Masuk ke menu `IP` > `Services`.
   - Pastikan layanan `api` (port default 8728) berstatus aktif (tidak di-disable).
3. **Cek Kredensial**: Pastikan Username dan Password MikroTik yang diinputkan di CafePulse benar.
