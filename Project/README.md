# CafePulse — Local-First Network Operations Platform for MikroTik

**CafePulse** is a lightweight, local-first desktop application designed for operating, managing, and monitoring local networks and MikroTik RouterOS-powered systems. Built for internet cafe (warnet) owners, small ISP operators, RT/RW Net administrators, and home network power users, CafePulse offers professional-grade dashboards without cloud dependencies or SaaS subscriptions.

---

## Key Features

### Free Edition
* **Local Discovery:** Active ARP and ping network scanning to identify connected hosts.
* **Device Inventory:** Categorize and track local devices with vendor lookup (OUI database).
* **Bandwidth Monitoring:** Live charting of network throughput.
* **Modern Interface:** High-fidelity PyQt6-based dark and light theme options.

### Professional Edition (Offline Activation)
* **RouterOS Integration:** Direct interaction with MikroTik routers using the official RouterOS API.
* **Hotspot & Voucher Management:** Live view of active hotspot sessions, voucher generation, and PDF voucher exporting.
* **System Operations:** Execute commands, monitor system resources, and manage automated backups.
* **Offline-First Security:** Cryptographic machine-locked licensing designed for offline network installations.

---

## Status: v0.9 Beta
CafePulse is currently in **v0.9 Beta**. We are actively gathering feedback from our beta testers and founder users.

---

## Project Structure
* `core/` — Core business logic (analytics, licensing, RouterOS clients, security).
* `ui/` — Graphical user interface components and styling built on PyQt6.
* `modes/` — Background worker threads for demo, local WiFi, and MikroTik modes.
* `installer/` — Inno Setup configurations to compile the installer executables.
* `website/` — Source HTML/CSS files for the official landing site.
* `tools/` — Developer utilities (such as the offline license generator).

---

## Getting Started (For Users)

1. **Download:** Grab the latest `CafePulse_Free_Setup.exe` from the [Official Website](https://youbellkey.github.io/cafepulse-site/).
2. **Install:** Run the setup installer (does not require administrator privileges).
3. **Launch:** Run CafePulse from your Start Menu or Desktop.

---

## Developer Guide

### Prerequisites
* Python 3.10+
* Windows 10 or 11 (64-bit)

### Installation & Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/cafepulse/CafePulse.git
   cd CafePulse
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Building the Executable & Installers
1. Compile the PyInstaller distributions (produces portable ZIPs in the `exports` folder):
   ```bash
   python build.py
   ```
2. Build the Inno Setup installers (requires Inno Setup 6.x installed on your PATH):
   ```cmd
   build_installer.bat
   ```

---

## License
Refer to the [LICENSE](LICENSE) file for usage guidelines.

## Links & Contact
* **Official Website:** [youbellkey.github.io/cafepulse-site/](https://youbellkey.github.io/cafepulse-site/)
* **Support Email:** `cafepulse.network@gmail.com`
