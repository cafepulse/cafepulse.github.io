# CafePulse Test Matrix

Dokumen ini memetakan berbagai skenario sistem operasi dan kondisi jaringan yang wajib diuji sebelum setiap rilis Mayor (v1.x, v2.x).

| OS Target | RAM / Storage | Skenario Pengujian | Status (Pass/Fail) | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| Windows 10 (22H2) | 8GB / SSD | Mode WiFi, Demo, Hotspot | | |
| Windows 11 (23H2) | 16GB / SSD | Mode MikroTik (Full Traffic) | | |
| Windows 10 (Old) | 4GB / HDD | Startup & Memory footprint | | Waktu muat tidak boleh > 5s |
| Ubuntu 22.04 LTS | 8GB / SSD | AppImage: Demo & Scan | | Uji izin pcap (root) |

## Network Matrix
| Kondisi Jaringan | Ekspektasi Reaksi Sistem | Status |
| :--- | :--- | :--- |
| Router Power Cut | Menampilkan dialog error, reconnect setelah hidup | |
| Beda Subnet | Scan mengembalikan 0 atau fallback aman | |
| Latency Spike > 1000ms | Polling MikroTik tidak *freeze* di UI, toleransi timeout | |
| WiFi Adapter Disable | Menghentikan scan, memberi alert `Network Interface Down` | |
