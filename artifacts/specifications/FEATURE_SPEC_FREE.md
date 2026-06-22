# CAFEPULSE FEATURE SPECIFICATION — FREE EDITION
### *Product Requirements Document — v1.0.0 | Juni 2026*

---

## OVERVIEW

Dokumen ini mendefinisikan spesifikasi lengkap semua fitur yang tersedia di CafePulse Free Edition. Setiap fitur didefinisikan dengan user story, acceptance criteria, dan edge cases.

---

## FEATURE 1 — NETWORK DISCOVERY & SCANNING

### User Story
> Sebagai admin jaringan, saya ingin CafePulse secara otomatis mendeteksi semua perangkat yang terhubung ke jaringan lokal saya, sehingga saya memiliki inventory perangkat yang akurat.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Scan Method** | ARP table reading + ICMP ping sweep (paralel, max 64 threads) |
| **Discovery Time** | Subnet /24 (254 host) selesai dalam ≤ 30 detik |
| **Information per Device** | IP address, MAC address, hostname (jika tersedia), vendor (dari OUI database) |
| **OUI Lookup** | Database lokal (tidak butuh internet), update manual via file |
| **Refresh Rate** | Auto-refresh setiap 30 detik (dapat dikonfigurasi: 15s, 30s, 60s, off) |
| **Silent Operation** | Tidak ada CMD/terminal window muncul selama scanning |

### Edge Cases
- Host yang tidak merespons ICMP tetap ditampilkan jika ada di ARP table
- DHCP router sering di-exclude dari ping sweep (whitelist IP gateway)
- Scan tidak crash jika network adapter tidak aktif

---

## FEATURE 2 — DEVICE INVENTORY MANAGER

### User Story
> Sebagai admin jaringan, saya ingin dapat melabeli dan mengkategorikan perangkat yang ditemukan, sehingga saya dengan mudah mengenali setiap device di jaringan saya.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Device Types** | Smartphone, Laptop/PC, Router, IoT Device, Unknown |
| **Custom Labels** | User dapat memberi nama custom per device (maks 64 karakter) |
| **Trusted Flag** | User dapat menandai device sebagai "Trusted" — device asing ditandai berbeda |
| **Persistence** | Label dan kategorisasi tersimpan di local database (tidak hilang setelah restart) |
| **Notes Field** | Text field untuk catatan bebas per device |
| **Sort & Filter** | Sortir by IP, MAC, vendor, last seen; filter by device type & trusted status |
| **Search** | Real-time search by IP, MAC, hostname, atau label kustom |

---

## FEATURE 3 — LIVE BANDWIDTH MONITOR

### User Story
> Sebagai admin jaringan, saya ingin melihat grafik bandwidth secara real-time, sehingga saya tahu kapan jaringan sedang sibuk dan bisa mengidentifikasi bottleneck.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Metric** | Throughput RX (download) dan TX (upload) |
| **Granularity** | Sampel setiap 1 detik |
| **Graph Display** | Grafik garis dengan range 60 detik terakhir (dapat diperluas) |
| **Unit** | Auto-scale: Kbps / Mbps |
| **Adapter Selection** | Dropdown untuk pilih network adapter (jika multi-NIC) |
| **Performance** | CPU usage grafik < 2% (hardware-accelerated via pyqtgraph) |

---

## FEATURE 4 — ALERT CENTER

### User Story
> Sebagai admin jaringan, saya ingin menerima notifikasi saat ada kejadian penting di jaringan (perangkat baru, gateway tidak tersedia, dll), sehingga saya tidak perlu terus-menerus memantau secara manual.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Alert Types** | Gateway unreachable, New unknown device joined, Device offline (jika dimonitor) |
| **Notification Method** | In-app toast notification (bottom-right corner, 5 detik) |
| **Alert History** | Semua alert tersimpan di database, dapat dilihat di Alert Center panel |
| **Alert Severity** | INFO, WARNING, CRITICAL (dengan warna berbeda) |
| **Read/Unread** | Alert baru ditandai sebagai unread hingga diklik |
| **Filter** | Filter by severity dan kategori |

---

## FEATURE 5 — THEME SYSTEM

### User Story
> Sebagai pengguna, saya ingin dapat memilih antara tema gelap dan terang sesuai preferensi saya.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Themes Available** | Dark Modern Blue (default), Light Mode |
| **Switching** | Instan tanpa restart aplikasi |
| **Persistence** | Preferensi tema tersimpan di settings.json |
| **Coverage** | Tema berlaku untuk semua komponen: window, dialog, chart, tooltip |

---

## FEATURE 6 — SETTINGS & CONFIGURATION

### User Story
> Sebagai pengguna, saya ingin dapat mengkonfigurasi perilaku CafePulse sesuai kebutuhan lingkungan jaringan saya.

### Acceptance Criteria

| Kriteria | Spec |
|---|---|
| **Scan Interval** | Pilihan: 15 detik, 30 detik, 1 menit, manual saja |
| **Gateway IP Override** | User dapat set IP gateway manual jika auto-detect gagal |
| **Language** | Bahasa Indonesia dan English (MVP: English, dengan plan untuk Indonesian) |
| **Startup Mode** | Demo / Home WiFi / MikroTik |
| **Log Level** | Debug (hanya untuk developer) / Normal |
| **Data Retention** | Berapa hari data disimpan: 7 hari, 30 hari, 90 hari, selamanya |

---

*Dokumen Feature Specification Free Edition CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
