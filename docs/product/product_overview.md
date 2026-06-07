# CafePulse Product Overview

CafePulse is a modern, lightweight, **local-first network monitoring and observability tool** designed for network administrators, solo developers, and coffee shop owners. 

By prioritizing offline functionality and direct router APIs, CafePulse gives you deep visibility into your network environments without sending sensitive logs or credentials to the cloud.

---

## 1. Core Product Pillars

### 1.1 Local-First & Privacy-First
All data—including MikroTik API passwords, device names, connection histories, and bandwidth logs—is stored in a local SQLite database (`cafepulse.db`). CafePulse operates fully offline.

### 1.2 MikroTik Observability
Built-in native integration with RouterOS API. Monitor DHCP leases, IP addresses, DNS cache tables, system resource load, and active hotspot users dynamically.

### 1.3 Adaptive & Responsive
A PyQt6 GUI designed to reflow smoothly from compact views on standard monitors to full-screen dashboards on wide administration terminals.

---

## 2. Technical Architecture

CafePulse is built using a modern, reliable desktop stack:

- **GUI Framework:** PyQt6 (Qt 6.7.1) for high-performance, cross-platform interface rendering.
- **Database Engine:** SQLite (configured with auto-cleanup and crash recovery) for lightweight local persistence.
- **Plotting & Visualization:** `pyqtgraph` for interactive, hardware-accelerated live network speed charts.
- **Communication Layer:** `routeros-api` for direct connection to MikroTik RouterOS devices.
- **Packaging:** PyInstaller, compiled with custom Windows resource schemas and multi-resolution icons.

---

## 3. Core Capabilities
- **Device Manager:** Automatic network discovery, IP tracking, and MAC address vendor resolution.
- **MikroTik Dashboard:** Interactive monitoring of RouterOS system metrics (CPU, RAM, Uptime), interfaces, and active clients.
- **Dynamic Alert Center:** Live toast notifications and database-backed warning triggers (e.g. gateway unreachable, CPU spikes, unknown MAC joins).
- **Theme Engine:** Built-in dynamic theme switcher supporting standard-compliant cyber-dark and light sheets.
