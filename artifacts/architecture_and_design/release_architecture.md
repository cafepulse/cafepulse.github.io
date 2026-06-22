# CafePulse Release Architecture Plan

This document outlines the package structure, asset inclusions, legal documentation, and runtime dependencies for the Free and Professional Editions of CafePulse.

---

## 1. Product Editions Packaging

To preserve code simplicity, CafePulse uses a single code branch. The edition features are unlocked at runtime based on the license state stored in the SQLite database and settings config.

### A. CafePulse Free Edition
* **Scope**: Targeted for single-owner operations, home WiFi testing, and simple network diagnostics.
* **Included Modules**:
  * Home WiFi Mode (dynamic ARP/Ping client discovery sweeps).
  * Startup Validator & Safe Mode Recovery.
  * Local Database Storage (WAL enabled, 30-day traffic prune).
  * System Log & Diagnostics Viewer.
  * Basic Settings (Light/Dark themes).
  * MikroTik Neighbor & Port Discovery (TCP Winbox/API scanning).
* **Limitations**:
  * Voucher batch size limited to 10 tokens.
  * Multi-router saving disabled (only 1 active profile profile).
  * Advanced network management pages display lock widgets.

### B. CafePulse Professional Edition
* **Scope**: Designed for commercial cafés, RT/RW Net operators, small hotels, and advanced network administrators.
* **Included Modules**:
  * Unlocked Voucher Batch Generator (up to 500 vouchers per run).
  * Multi-Router Credentials Vault and connection list.
  * Full MikroTik Operations Mode (real-time bandwidth monitor + DHCP stats).
  * AI Network Insights & Traffic Analytics charts.
  * Advanced Network Workspace forms (Firewall, NAT, DNS, VLAN, PPP, QoS, Backup simulators).
  * EULA compliance activation binding (1 License = 1 PC, 5-Year Update Entitlement).

---

## 2. Mandatory Distribution Assets

Any compiled distribution package must package the following files and folders:

```
📁 CafePulse/
├── 📄 CafePulse.exe           # Main compiled executable
├── 📁 assets/
│   ├── 📄 icon.ico            # Main window application icon
│   ├── 📄 logo.png            # Topbar branding asset
│   └── 📄 splash.png          # App boot splash image
├── 📁 config/
│   └── 📄 settings.json       # Default configuration templates (copied on first boot)
├── 📁 docs/
│   └── 📁 legal/
│       ├── 📄 eula.md         # End User License Agreement
│       └── 📄 privacy.md      # Data Privacy policies (100% local processing)
└── 📄 LICENSE.txt             # Core software copyright notice
```

---

## 3. Required Documentation Bundle

The documentation must reside locally within the release payload as well as on the official web portal:

1. **`README_FREE.md`**: Guides administrators through setting up client sweeps and standard WiFi network checking.
2. **`README_PROFESSIONAL.md`**: Provides instruction for connection setup on RouterOS API, credential storage safety, offline license activation key files, and bulk voucher generation.
3. **`EULA (legal/eula.md)`**: Clarifies the 1 PC node activation lock, Best Effort Support model, and the 5-Year Update Entitlement boundaries.

---

## 4. Runtime Dependencies & Verification

The compiled package runs on Windows 10/11 (64-bit) systems. The following packages must be frozen into the executable package by PyInstaller:

| Import Name | Package Name (PyPI) | Version | Function in CafePulse |
| :--- | :--- | :--- | :--- |
| `PyQt6` | `PyQt6` | `6.7.1` | Main desktop application windowing framework. |
| `pyqtgraph` | `pyqtgraph` | `0.13.7` | High-performance graph canvas for real-time charting. |
| `mac_vendor_lookup` | `mac-vendor-lookup` | `0.1.12` | Resolves MAC addresses to vendor manufacturers locally. |
| `cryptography` | `cryptography` | `43.0.1` | Secures the MikroTik password vault using AES-256. |
| `psutil` | `psutil` | `6.0.0` | Queries host machine system load and loopback sockets. |
| `routeros_api` | `routeros-api` | `0.21.0` | Establishes API socket connection to RouterOS. |

*Note*: Optional libraries must not trigger compilation failures. If `routeros_api` is absent in developer runtimes, the app gracefully boots into home network sweep modes and displays informative warnings in logs.
