# CODE RELATION MAP
### *Codebase Topology, Dependency Graphs & Architectural Blueprint — Locked: Juni 2026*

---

## 1. STRUKTUR DIREKTORI (FOLDER TOPOLOGY)

```

  ├── assets/                      # Aset grafis aplikasi (logo.svg, splash.png, icon.ico)
  ├── config/                      # Pengaturan default awal (settings_default.json)
  ├── core/                        # Modul logika inti & operasi backend aplikasi
  │     ├── analytics/             # Pengukur kesehatan jaringan (health_engine.py)
  │     ├── database/              # SQLite database manager (db_manager.py)
  │     ├── iam/                   # Modul manajemen pengguna hotspot & session tracking
  │     ├── licensing/             # Modul lisensi asimetris (rsa_manager.py, licensing_manager.py)
  │     ├── logging_system/        # Setup file logging and rotation
  │     ├── mikrotik/              # Wrapper API RouterOS & MNDP discovery
  │     ├── network/               # Manajemen sub-jaringan (ARP, neighbor lists)
  │     ├── runtime/               # Verifikasi dependensi awal (dependency_registry.py)
  │     ├── scanner/               # Modul pemindaian jaringan inti (arp_scanner.py - 6-stage chain)
  │     ├── security/              # Secure credential vault (credential_vault.py)
  │     └── utils/                 # Utilities & Config file reader (config_manager.py)
  ├── installer/                   # Skrip kompilasi setup installer Windows (Inno Setup .iss)
  │     ├── free/                  # Installer Free Edition
  │     └── professional/          # Installer Professional Edition
  ├── modes/                       # Worker & polling schedulers (Pulse Engine)
  │     ├── hotspot/               # Logika pemantau hotspot & DHCP active leases
  │     ├── home_wifi/             # Logika pemindai perangkat WiFi lokal (arp_scanner.py, wifi_worker.py)
  │     ├── mikrotik/              # Modul polling API MikroTik RouterOS
  │     └── demo/                  # Mode demo data simulasi
  ├── ui/                          # Seluruh antarmuka grafis (PyQt6)
  │     ├── dialogs/               # Jendela pop-up error, recovery, and license activation
  │     ├── themes/                # File stylesheet QSS (dark_theme.py, light_theme.py)
  │     ├── widgets/               # Komponen/Tab UI modular (dashboard_tab.py, license_page.py)
  │     └── windows/               # Windows container utama (main_window.py)
  ├── main.py                      # Entry point eksekusi utama aplikasi desktop
  └── build.py                     # Skrip otomasi kompilasi biner (PyInstaller)
```

---

## 2. STRUKTUR FILE UTAMA (KEY FILE FUNCTIONALITIES)

| File | Fungsi Utama |
|---|---|
| `main.py` | Entry point. Melakukan startup validation, memverifikasi status recovery crash (.clean/.lock), memuat database, setup logging, and meluncurkan GUI. |
| `core/app_paths.py` | Mengelola resolusi path global (Program Files vs LOCALAPPDATA per-user) secara aman. |
| `core/database/db_manager.py` | Menginisialisasi skema tabel, melakukan `integrity_check`, and mengeksekusi kueri SQLite. |
| `core/licensing/rsa_manager.py` | Kriptografi RSA. Memuat public key and memverifikasi signature file `.lic`. |
| `core/licensing/licensing_manager.py` | Mengekstraksi Hardware ID (UUID/CPU) per PC and memeriksa validitas status Pro. |
| `core/security/credential_vault.py` | Mengamankan password login router MikroTik menggunakan enkripsi machine-bound. |
| `core/mikrotik/router_discovery.py` | Memindai jaringan lokal menggunakan MNDP/UDP broadcast untuk mencari router MikroTik terdekat. |
| `core/scanner/arp_scanner.py` | Engine pemindaian ARP jaringan lokal dengan rantai deteksi subnet 6-tahap (6-stage offline fallback chain) yang tidak bergantung pada ping public DNS. |
| `modes/home_wifi/arp_scanner.py` | Implementasi scanner WiFi lokal dengan integrasi thread monitoring perangkat GUI. |
| `core/utils/config_manager.py` | Membaca and menulis konfigurasi aplikasi (`settings.json`) dengan mode fallback. |
| `modes/hotspot/hotspot_detector.py` | Thread Worker. Melakukan polling berkala API MikroTik untuk data user active hotspot dengan filter UAC/cmd tersembunyi. |
| `ui/windows/main_window.py` | Container GUI utama. Mengelola navigasi tab, pemuatan tema, sinkronisasi state shutdown QThread yang aman, and inisialisasi thread engine. |
| `ui/widgets/license_page.py` | Panel lisensi. Menampilkan HWID, mengimpor berkas lisensi, and memicu validasi RSA. |

---

## 3. RELASI ANTAR FILE & DEPENDENCY GRAPH

```
[ main.py ]
   │
   ├───> [ core/app_paths.py ] 
   │
   ├───> [ core/logging_system.py ]
   │
   ├───> [ core/utils/config_manager.py ]
   │
   ├───> [ core/database/db_manager.py ]
   │
   └───> [ ui/windows/main_window.py ]
             │
             ├───> [ core/licensing/licensing_manager.py ]
             │         │
             │         └───> [ core/licensing/rsa_manager.py ]
             │
             ├───> [ ui/widgets/dashboard_tab.py ]
             │
             ├───> [ modes/hotspot/hotspot_detector.py ] (QThread)
             │         │
             │         └───> [ core/mikrotik/router_discovery.py ]
             │
             └───> [ modes/home_wifi/wifi_worker.py ] (QThread)
                       │
                       └───> [ modes/home_wifi/arp_scanner.py ]
                                 │
                                 └───> [ core/scanner/arp_scanner.py ]
```

---

## 4. RELASI ANTAR LAYER (CAFEPULSE NATIVE ARCHITECTURE)

Implementasi alur data and logika modular di CafePulse disusun sebagai berikut:

```
[ FRONTEND / PyQt6 UI ] (main_window.py, dashboard_tab.py, dialogs/)
        │
        │ (Signals & Slots / Event-Driven)
        v
[ CONTROL & CORE ENGINE ] (Pulse Engine, QThreads, hotspot_detector.py, wifi_worker.py)
        │
        ├── (RouterOS API TCP Protocol) ──> [ MIKROTIK LAYER ] (API Wrapper)
        │                                         │
        ├── (Local Socket Scan / ARP Chain) ──> [ LOCAL SCAN LAYER ] (arp_scanner.py)
        │                                         │
        ├── (Local SQLite Transactions)           v
        │                                   [ Network Hardware ]
        v
[ PERSISTENCE / DATABASE LAYER ] (DatabaseManager, db_manager.py)
        │
        ^ (HWID Checks / RSA Public Key validation)
[ BUSINESS & SECURITY LAYER ] (RSAManager, LicensingManager, CredentialVault)
```

### Penjelasan Alur Data:
1.  **Booting:** `main.py` meluncurkan splash screen, memverifikasi `.clean` & `.lock` files untuk memastikan shutdown sebelumnya sukses, memverifikasi dependensi via `runtime`, and memuat setelan dari `utils`. `LicensingManager` mengekstraksi UUID motherboard dan memverifikasi tanda tangan `license.lic` via `RSAManager`.
2.  **Inisialisasi UI:** `MainWindow` membaca tema (`dark_theme.py`) and memuat widget halaman. Jika lisensi valid, mode *Professional* diaktifkan secara visual.
3.  **Engine Start:** `MainWindow` meluncurkan background thread `QThread` (seperti `hotspot_detector.py` dan `wifi_worker.py`).
4.  **Data Polling & Scan:** Background thread mengirim kueri TCP non-blocking ke API router MikroTik atau menjalankan pemindaian subnet lokal offline via `core/scanner/arp_scanner.py`. Sinyal UI dilepaskan secara aman untuk mencegah race condition shutdown.
5.  **UI Update:** Thread worker mengirim sinyal PyQt (`pyqtSignal`) berisi data parsing terbaru ke thread utama UI untuk memperbarui grafik dashboard secara reaktif tanpa lag.

---

## 5. RISK PROFILE (CRITICAL & SAFE FILES)

### 5.1 Entry Points
*   **Aplikasi Utama Desktop:** [main.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/main.py)
*   **Penerbitan Lisensi (Offline):** [license_generator/issue_license.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/license_generator/issue_license.py)
*   **Otomasi Build PyInstaller:** [build.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/build.py)

### 5.2 High Risk Files (Sangat Sensitif - Modifikasi Berpotensi Merusak Sistem)
*   [core/app_paths.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/core/app_paths.py): Mengurusi izin filesystem dan path UAC. Kesalahan kecil dapat mencegah aplikasi booting.
*   [core/licensing/rsa_manager.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/core/licensing/rsa_manager.py): Jantung keamanan lisensi. Modifikasi yang tidak pas dapat mengunci pengguna sah atau menyebabkan kebocoran otentikasi.
*   [core/database/db_manager.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/core/database/db_manager.py): Kegagalan migrasi skema tabel di file ini berisiko merusak database user.
*   [core/scanner/arp_scanner.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/core/scanner/arp_scanner.py) & [modes/home_wifi/arp_scanner.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/modes/home_wifi/arp_scanner.py): Bertanggung jawab atas pemindaian jaringan lokal. Kesalahan subprocess flag (`STARTUPINFO`) dapat memicu command window berkedip di Windows atau hang.

### 5.3 Safe To Modify (Aman Dimodifikasi)
*   [ui/themes/dark_theme.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/themes/dark_theme.py) & [light_theme.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/themes/light_theme.py): Hanya mengurusi visual styling QSS.
*   [ui/widgets/dashboard_tab.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/dashboard_tab.py): Tampilan dasbor analitik. Aman untuk penyesuaian visual widget.
*   [gen_pdf.py](file:///C:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/gen_pdf.py) & generators sejenis: Skrip compiler laporan mandiri.

---

## 6. KNOWLEDGE GRAPH (TEXTUAL REPRESENTATION)

```
[main.py] -> initializes -> [app_paths.py]
[main.py] -> initializes -> [logging_system.py]
[main.py] -> validates -> [dependency_registry.py]
[main.py] -> boots -> [main_window.py]
[main_window.py] -> reads -> [config_manager.py]
[main_window.py] -> requests authorization -> [licensing_manager.py]
[licensing_manager.py] -> decrypts signature -> [rsa_manager.py]
[rsa_manager.py] -> verifies integrity of -> [license.lic]
[main_window.py] -> launches -> [hotspot_detector.py] (QThread)
[main_window.py] -> launches -> [wifi_worker.py] (QThread)
[wifi_worker.py] -> triggers scan via -> [home_wifi/arp_scanner.py]
[home_wifi/arp_scanner.py] -> executes chain in -> [core/scanner/arp_scanner.py]
[hotspot_detector.py] -> queries -> [RouterOS API]
[hotspot_detector.py] -> writes metrics -> [db_manager.py]
[db_manager.py] -> reads/writes -> [cafepulse.db]
[hotspot_detector.py] -> triggers UI update on -> [dashboard_tab.py]
```
