# Error Code: ERR_SCAN_001
**Title**: Network Interface Not Found / Scan Timeout

## Gejala (Symptoms)
Saat berada di **Home WiFi Mode**, proses *scanning* terus-menerus gagal atau perangkat tidak ada yang terdeteksi sama sekali meskipun komputer terkoneksi ke WiFi.

## Penyebab Umum
1. **Network Adapter Tidak Aktif**: WiFi atau LAN di komputer sedang *disabled*.
2. **Kehilangan Hak Akses (Permissions)**: Modul *packet sniffing* (seperti Npcap atau Scapy) membutuhkan akses Administrator.
3. **Subnet Tidak Valid**: Konfigurasi jaringan memberikan IP yang tidak valid (misal `169.254.x.x`).

## Solusi & Langkah Perbaikan
1. **Jalankan sebagai Administrator**: Tutup CafePulse, lalu klik kanan ikon CafePulse dan pilih **Run as Administrator**.
2. **Cek Koneksi**: Buka *Control Panel* > *Network Connections* dan pastikan ada satu *adapter* jaringan yang sedang terkoneksi ke internet.
3. **Install Ulang Npcap**: Jika Anda menggunakan mode sniffer pasif, pastikan paket `Npcap` sudah terpasang di Windows.
