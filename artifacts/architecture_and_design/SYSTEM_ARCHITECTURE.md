# CAFEPULSE SYSTEM ARCHITECTURE
### *Technical Architecture Document — v1.0.0 | Juni 2026*

---

## BAGIAN 1 — ARSITEKTUR SISTEM TINGKAT TINGGI

### 1.1 Architectural Philosophy

CafePulse mengikuti arsitektur **Layered Local-First Desktop Application**. Tidak ada server backend, tidak ada cloud dependency, tidak ada microservices. Semua beroperasi dalam satu proses aplikasi Python.

```
┌─────────────────────────────────────────────────────────────────┐
│                       CAFEPULSE DESKTOP APP                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    UI LAYER (PyQt6)                       │   │
│  │  Windows │ Widgets │ Dialogs │ Themes │ Charts           │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                            │ Signals & Events                    │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │               BUSINESS LOGIC LAYER (Core)                │   │
│  │  Analytics │ Licensing │ IAM │ Runtime │ Security         │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │              DATA ACCESS LAYER                           │   │
│  │  SQLite (cafepulse.db) │ Config JSON │ Logs              │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │              NETWORK INTEGRATION LAYER                   │   │
│  │  RouterOS API │ ARP Scanner │ Ping Engine │ OUI Database  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                    Local Network Only                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## BAGIAN 2 — TECHNOLOGY STACK

### 2.1 Stack Utama

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| **Language** | Python | 3.10+ | Ekosistem library yang kaya, cepat dikembangkan |
| **GUI Framework** | PyQt6 | 6.7.1 | Native performance, rich widgets, cross-platform |
| **Database** | SQLite | Built-in | Zero config, lokal, reliable, WAL mode |
| **Charting** | pyqtgraph | Latest | GPU-accelerated, real-time capable |
| **Router API** | routeros-api | Latest | Official-compatible RouterOS API client |
| **Packaging** | PyInstaller | Latest | Single EXE output, Windows support |
| **Installer** | Inno Setup | 6.x | Professional Windows installer |

### 2.2 Third-Party Libraries

| Library | Fungsi |
|---|---|
| `cryptography` | Enkripsi credential vault |
| `psutil` | System resource monitoring (CPU, RAM) |
| `reportlab` | PDF generation (voucher, laporan) |
| `openpyxl` | Excel export |
| `paramiko` | SSH fallback untuk router access |

---

## BAGIAN 3 — MODULE ARCHITECTURE

### 3.1 Struktur Direktori & Modul

```
CafePulse/
├── main.py                     # Entrypoint: init, splash, mode detection, UI launch
│
├── core/                       # Business logic layer
│   ├── analytics/              # Network health, statistics, BI computation
│   │   ├── health_engine.py    # Real-time network health scoring (0-100%)
│   │   └── statistics_engine.py # Historical data aggregation
│   ├── database/               # Database access objects
│   │   ├── db_manager.py       # SQLite connection & WAL management
│   │   └── migrations.py       # Schema versioning & migration
│   ├── iam/                    # Identity & access management (hotspot users)
│   │   └── user_manager.py     # RouterOS user/hotspot user management
│   ├── licensing/              # License management
│   │   ├── license_manager.py  # License verification & activation
│   │   └── machine_id.py       # Hardware fingerprint generation
│   ├── mikrotik/               # MikroTik RouterOS integration
│   │   ├── api_client.py       # RouterOS API connection wrapper
│   │   ├── router_discovery.py # Auto-discovery & gateway detection
│   │   └── voucher_engine.py   # Hotspot voucher generation
│   ├── network/                # Local network utilities
│   │   └── oui_lookup.py       # MAC vendor OUI database lookup
│   ├── runtime/                # Application runtime management
│   │   └── session_manager.py  # Startup validation, CLEAN_FLAG management
│   ├── scanner/                # Network scanning engines
│   │   ├── arp_scanner.py      # ARP table reader + ping sweep
│   │   └── ping_engine.py      # ICMP ping utilities
│   ├── security/               # Cryptographic utilities
│   │   └── vault.py            # Encrypted credential storage
│   └── utils/                  # Generic utilities
│       └── file_utils.py       # Path resolution, export helpers
│
├── ui/                         # Presentation layer
│   ├── dialogs/                # Modal dialogs (about, license, export)
│   ├── themes/                 # CSS-like Qt stylesheet definitions
│   ├── widgets/                # Reusable widget components
│   │   ├── network/            # Network-specific widgets (dashboard panels)
│   │   └── shared/             # Cross-module shared widgets (cards, charts)
│   └── windows/                # Top-level window definitions
│       └── main_window.py      # Main application window
│
├── modes/                      # Operating mode workers (background threads)
│   ├── demo/                   # Demo mode with simulated data
│   ├── home_wifi/              # Local WiFi scanning mode
│   ├── hotspot/                # Hotspot detection & management mode
│   └── mikrotik/               # Full MikroTik RouterOS mode
│
├── config/                     # Configuration files
│   ├── settings.json           # User preferences & app settings
│   └── settings_default.json   # Factory defaults (committed to repo)
│
├── assets/                     # Static assets
│   ├── branding/               # Logo, icons, splash screen
│   ├── fonts/                  # Bundled fonts (Inter, JetBrains Mono)
│   └── screenshots/            # App screenshots for website/docs
│
├── installer/                  # Inno Setup scripts
│   ├── free/                   # Free Edition installer config
│   └── professional/           # Professional Edition installer config
│
├── website/                    # GitHub Pages website
│   ├── index.html              # Landing page
│   ├── download.html           # Download page
│   ├── pricing.html            # Pricing page
│   └── assets/                 # Website assets
│
└── tests/                      # Automated test suite
    ├── unit/                   # Unit tests per module
    └── integration/            # Integration tests
```

---

## BAGIAN 4 — DATA MODEL

### 4.1 Database Schema (cafepulse.db)

```sql
-- Devices discovered on local network
CREATE TABLE devices (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address      TEXT NOT NULL,
    mac_address     TEXT,
    hostname        TEXT,
    vendor          TEXT,       -- From OUI database lookup
    device_type     TEXT,       -- 'smartphone', 'laptop', 'router', 'iot', 'unknown'
    is_trusted      INTEGER DEFAULT 0,
    first_seen      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen       TIMESTAMP,
    notes           TEXT
);

-- MikroTik router connections
CREATE TABLE routers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,          -- User-defined label
    ip_address      TEXT NOT NULL,
    api_port        INTEGER DEFAULT 8728,
    use_ssl         INTEGER DEFAULT 0,
    username        TEXT,
    password_hash   TEXT,       -- Encrypted via vault
    group_tag       TEXT,
    last_connected  TIMESTAMP,
    is_active       INTEGER DEFAULT 1
);

-- Network health snapshots
CREATE TABLE health_snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    router_id       INTEGER REFERENCES routers(id),
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_usage       REAL,
    ram_usage       REAL,
    uptime_seconds  INTEGER,
    rx_bytes        INTEGER,
    tx_bytes        INTEGER,
    active_clients  INTEGER,
    health_score    INTEGER     -- 0-100 composite score
);

-- Alert history
CREATE TABLE alerts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity        TEXT,       -- 'info', 'warning', 'critical'
    category        TEXT,       -- 'network', 'security', 'system', 'device'
    title           TEXT NOT NULL,
    message         TEXT,
    is_read         INTEGER DEFAULT 0,
    router_id       INTEGER REFERENCES routers(id),
    device_id       INTEGER REFERENCES devices(id)
);

-- User settings (key-value store)
CREATE TABLE settings (
    key             TEXT PRIMARY KEY,
    value           TEXT,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Voucher records (Professional Edition)
CREATE TABLE vouchers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    router_id       INTEGER REFERENCES routers(id),
    profile_name    TEXT,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL,
    duration_hours  INTEGER,
    quota_mb        INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_used         INTEGER DEFAULT 0,
    used_at         TIMESTAMP,
    batch_id        TEXT        -- Group identifier for bulk-generated vouchers
);
```

---

## BAGIAN 5 — SECURITY ARCHITECTURE

### 5.1 Credential Security Model

```
┌──────────────────────────────────────────────────┐
│             CREDENTIAL SECURITY CHAIN             │
│                                                    │
│  User Input (password)                             │
│      ↓                                             │
│  Fernet Symmetric Encryption                       │
│      ↓                                             │
│  Machine-Derived Key Generation                    │
│  (UUID + hostname + MAC address hash)              │
│      ↓                                             │
│  Encrypted Blob → Stored in SQLite                 │
│                                                    │
│  Decryption only possible on same machine         │
└──────────────────────────────────────────────────┘
```

### 5.2 License Security Model

```
┌──────────────────────────────────────────────────┐
│              LICENSE SECURITY CHAIN               │
│                                                    │
│  Machine Fingerprint Generation:                   │
│  - UUID (from winreg / /etc/machine-id)           │
│  - Hostname                                        │
│  - Primary MAC Address                             │
│      ↓                                             │
│  SHA-256 Hash → 16-char Machine ID                │
│      ↓                                             │
│  License Key = HMAC-SHA256(owner_name + machine_id│
│               + product_code + SECRET_SALT)        │
│      ↓                                             │
│  Stored in: config/license.lic (JSON)              │
│  Path: %APPDATA%/CafePulse/config/license.lic     │
└──────────────────────────────────────────────────┘
```

**Known Security Limitations (to be addressed in v1.1+):**
- SECRET_SALT currently compiled into binary — should be externally distributed
- MAC address changes (VPN, NIC replacement) can invalidate license — migration flow needed

### 5.3 Network Security Posture

- **No outbound connections** to external servers during normal operation
- All RouterOS API connections are **LAN-only** (local IP ranges)
- Password stored with **machine-bound encryption** — credential dump requires physical access
- No telemetry, no analytics phone-home, no update checks that send device data

---

## BAGIAN 6 — STARTUP & LIFECYCLE MANAGEMENT

### 6.1 Application Startup Sequence

```
1. main.py called
2. ── Check LOCK_FILE (prevent multi-instance)
3. ── Check CLEAN_FLAG (detect improper shutdown)
   └── If missing: show "Recovery" dialog → run DB integrity check
4. ── Initialize logging system
5. ── Load QApplication (PyQt6)
6. ── Show SplashScreen
7. ── Initialize DatabaseManager → ensure schema up-to-date
8. ── Load ConfigManager → read settings.json
9. ── Determine operating mode (demo / home_wifi / mikrotik)
10. ── Initialize MainWindow
11. ── Remove SplashScreen → Show MainWindow
12. ── Write LOCK_FILE
13. ── app.exec() ← Qt event loop
```

### 6.2 Shutdown Sequence (Proper)

```
1. User clicks X / Alt+F4
2. MainWindow.closeEvent() triggered
3. ── Show SafeCloseDialog (if workers active)
4. ── Stop all background worker threads gracefully
5. ── DatabaseManager.close() → flush WAL checkpoint
6. ── Write CLEAN_FLAG (signals clean exit)
7. ── Delete LOCK_FILE
8. ── sys.exit(0)
```

---

*Dokumen Arsitektur Sistem CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
