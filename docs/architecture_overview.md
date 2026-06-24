# Architecture Overview

Dokumen ini menjelaskan gambaran struktur rekayasa (*engineering architecture*) dari CafePulse. Ini dikhususkan bagi para Penasihat Teknis (*Technical Advisors*), Kontributor, dan Penguji Tingkat Lanjut (*Advanced Testers*) untuk memahami logika cara kerja di balik kap aplikasi.

## 1. Filosofi Inti: "Local-First Desktop App"
CafePulse tidak dibangun sebagai aplikasi web SaaS (Software as a Service) atau aplikasi dengan topologi *Client-Server* cloud. Aplikasi ini adalah *standalone desktop executable* (Aplikasi Desktop Mandiri).
* **Alasan Desain:** Kecepatan dan keamanan. Banyak lokasi target (Warung Kopi, Kafe) memiliki konfigurasi jaringan NAT/Firewall ketat di mana koneksi langsung dari Cloud ke dalam Router sulit ditembus tanpa integrasi VPN atau agen khusus tambahan. Model *local-first* menjembatani kesenjangan ini dengan beroperasi langsung di dalam LAN.

## 2. Stack Teknologi Utama
CafePulse menggunakan *stack* Python yang disederhanakan:
* **Backend Runtime:** Python 3.x (Di- *bundle* secara native pada versi instalasi `.exe` dan `.AppImage` melalui PyInstaller).
* **Graphic User Interface (GUI):** PyQt6 digunakan sebagai pondasi komponen *frontend*, menghubungkan event (*signals & slots*) asynchronous untuk menjamin UI tidak membeku saat fungsi *polling* bekerja di *background*.
* **Basis Data:** SQLite3, *database* yang tak memerlukan sistem server independen. Keandalannya menjaga satu *file-based database* `cafepulse.db` memastikan latensi *query* mendekati 0ms.

## 3. Protokol MikroTik RouterOS API
Alih-alih menggunakan koneksi *SSH*, CafePulse berkomunikasi menggunakan **RouterOS API Protocol**.
* Semua implementasi berbasis *sentences*, terdiri dari instruksi kueri komando (misal: `/ip/hotspot/active/print`), atribut parameter, dan argumen pencarian.
* Karena komunikasi diinisiasi melalui soket sinkron (atau secara berurutan dalam rentang *timeout* sempit), CafePulse menggunakan kelas *Worker Threads* (QThread) terpisah dari *Main UI Thread* untuk melakukan komunikasi bolak-balik tanpa memengaruhi interaksi pengguna.

## 4. Struktur Workspace Logika (Internal Directories)
Pada lingkungan sistem operasi (atau mode pengembang lokal), logika CafePulse dapat dilihat dengan topologi sebagai berikut:
* `core/`: Tempat dimana mesin koneksi API (`api_engine.py`) dan *polling workers* berada.
* `ui/`: Konstruktor visualisasi PyQt6 (`dashboard.py`, `active_clients.py`).
* `database/`: Penanganan model ORM ringan untuk *setup* tabel profil Router dan fungsi pencatatan *Log*.

Dengan arsitektur ini, CafePulse meminimalisasi *overhead* memori di pihak pengguna (biasanya beroperasi di bawah beban ~100MB RAM), sementara mengekstrak puluhan titik data secara *real-time* ke antarmukanya.

> [!NOTE]
> Selama fase **Production Environment Validation**, efisiensi arsitektur *multithreading* ini akan diverifikasi lebih lanjut pada berbagai kelas arsitektur CPU *router* fisik (seperti MIPSBE, ARM, dan Tile) guna memastikan skalabilitas operasi di lapangan.
