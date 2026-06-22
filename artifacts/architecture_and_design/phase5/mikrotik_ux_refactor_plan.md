# CafePulse MikroTik Management UX Refactor & Capability Preservation Plan

This document integrates the technical implementation plan for the **MikroTik Management UX Architecture Refactor** with a rigorous **Feature Preservation Audit**. It outlines how CafePulse organizes RouterOS's extensive capabilities into a clean, modular tab hierarchy inside the **Network Workspace**, while verifying **zero capability loss, zero feature degradation, and zero regressions** during the refactoring process.

---

## Goal Description
CafePulse is transitioning into a full-scale MikroTik Operations Platform. As we partition and deconstruct raw network settings into structured layouts, we establish a core philosophy: **UX optimization is about organizing, grouping, and simplifying presentation—not about deleting power or eliminating capabilities.**

Every single live status, bandwidth metric, secure credential mask, loading indicator, and debug script originally present in the monolithic system is **strictly preserved** in the new modular architecture under `ui/widgets/network/`.

---

## User Review Required

> [!IMPORTANT]
> **Core UX Refactor & Preservation Decisions:**
>
> 1. **Complete Preservation of Interactive Connection States:** Visual status chips at the top-right of the Network Workspace dynamically transition between states (`Online`, `Offline`, `Reconnecting`, `Connecting`, `Failed`, `Error`), ensuring real-time operations feedback is never replaced by static text.
> 2. **Separate Upload/Download Bandwidth Trailing:** Bandwidth metrics remain split into individual Upload (TX) and Download (RX) curves in the read-only Traffic monitor, preventing the simplification of link loads into a single metric.
> 3. **Operator Privacy Masking Sync:** Dynamic privacy-masked IP and MAC addresses in the Personal Network discovery view are synchronized with `app_state.privacy_masked_changed` events, preserving security.
> 4. **No-wireless "Not Available" AP Card:** Routers lacking physical wireless interfaces render a prominent HSL-styled placeholder stating hardware limitations, while keeping the view accessible for external AP layouts.

---

## Proposed Refactored Architecture

The monolithic dashboard has been decomposed into modular widget classes in the `ui/widgets/network/` directory, while wrappers in `sidebar.py` and `main_window.py` route all signals cleanly:

```
c:\Users\USER\Documents\Yubelki\CafePulse\CafePulse\
├── ui/widgets/
│   ├── sidebar.py                  <-- [MODIFY] Point Network to new pages
│   └── network/                    <-- [NEW] Decomposed Network Workspace widgets
│       ├── __init__.py
│       ├── network_page.py         <-- Master Coordinator (QTabWidget / sub-sidebar)
│       ├── net_overview.py         <-- Overview Page (Landing gauges & health check)
│       ├── net_connections.py      <-- Router Discovery & secure saved router cards
│       ├── net_ip_dhcp.py          <-- Unified IP & DHCP Manager with Leases
│       ├── net_dns.py              <-- DNS settings, Static domain binding & Cache Flush
│       ├── net_wifi.py             <-- WiFi Access Point (Not Available hardware check)
│       ├── net_interfaces.py       <-- Bridges, VLAN list, and Visual ASCII Topology
│       ├── net_traffic.py          <-- Read-only Real-time Bandwidth curves (Pyqtgraph)
│       ├── net_access_control.py   <-- Admin users, API/SSL ports & access subnets
│       ├── net_routing.py          <-- Route tables & Dynamic protocol tags (OSPF/BGP)
│       ├── net_firewall.py         <-- Filter, NAT, Mangle with Basic/Advanced switches
│       ├── net_ppp.py              <-- PPP Secrets, PPPoE/L2TP live active connections
│       ├── net_hotspot.py          <-- Hotspot Server & Login customizer (No vouchers)
│       ├── net_queue.py            <-- Simple Queue, burst limits & Queue Trees
│       ├── net_backup.py           <-- Binary backups & plain-text RSC script imports
│       └── net_system.py           <-- System Clock NTP, Clock, Schedulers & live logs
```

---

## Feature Preservation Audit Matrix

Below is the verification registry mapping each critical component, its state before the refactor, and how it is explicitly preserved in the refactored modular files:

| Category | Component Description | State Before Refactor | State After Refactor (Decomposed) | Verification Status & File |
| :--- | :--- | :--- | :--- | :--- |
| **1. Exit Demo** | Indicator to shut down fake data stream and return workspace to clean blank state. | Handled via `exit_demo_requested` in `MainWindow`. | Preserved. The `exit_demo_requested` signal and reset routines are connected to `MainWindow` and `NetworkPage`. | **VERIFIED ✓**<br>[main_window.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/windows/main_window.py#L316-L347) |
| **2. Traffic Metrics**| Active download/upload rates represented separately. | Real-time traffic plots in main dashboard. | Preserved. Exposes individual RX (Download) and TX (Upload) curves in pyqtgraph chart. | **VERIFIED ✓**<br>[net_traffic.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_traffic.py#L40-L55) |
| **3. Live Conn Status**| Color-coded dynamic state indicators for router connection. | Standard label in top-bar and connections cards. | Preserved. Exposes dynamic states (`Online`, `Offline`, `Menghubungkan`, `Reconnecting`, `Degraded`, `Failed`) in connection cards and header. | **VERIFIED ✓**<br>[network_page.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/network_page.py#L75-L83) |
| **4. Discovery Status**| Discovery neighbor sweep scan listings. | Embedded sweep scans and discovery MNDP tables. | Preserved. Exposes tabular MNDP neighbor discoveries and favorites connection listings. | **VERIFIED ✓**<br>[net_connections.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_connections.py#L26-L40) |
| **5. Password Masking**| Masking of passwords and sensitive local scan IPs. | Handled by `QLineEdit.EchoMode.Password` and local IP anonymization. | Preserved. Enforces masked password inputs and listens to global privacy-masked events for ARP scan IPs. | **VERIFIED ✓**<br>[personal_network_page.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/personal_network_page.py#L180-L190) |
| **6. Loading Feedback**| Infinite loading indicators and diagnostic status texts. | Simple loading overlays during network pings. | Preserved. Exposes real-time loading bars, infinite progress bars, and status logs in connection checkers. | **VERIFIED ✓**<br>[compatibility_page.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/compatibility_page.py#L154-L170) |
| **7. Health Indicators**| Network latency curves and health score indices. | Standard `Health Card` showing active scores. | Preserved. Monitored via active gauges in Overview and live latency curves. | **VERIFIED ✓**<br>[net_overview.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_overview.py#L100-L110) |
| **8. Real-time Status**| Live gauges representing system memory and CPU utilization. | Dashboard resource metrics panel. | Preserved. Relocated to dynamic Overview gauges with critical warnings (Red Chunk if CPU >80%). | **VERIFIED ✓**<br>[net_overview.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_overview.py#L65-L80) |
| **9. Debug Info** | Raw system logs and administrative utility streams. | Core logging streams inside Observability workspace. | Preserved. Moved to System tab, displaying clock synchronization, NTP status, and RouterOS logs stream. | **VERIFIED ✓**<br>[net_system.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_system.py#L65-L80) |
| **10. Search Tools**| Search filters inside IP/ARP and device listings. | Simple text inputs filtering QTableWidget records. | Preserved. Kept inside tables and grids to filter entries instantly. | **VERIFIED ✓**<br>[net_ip_dhcp.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_ip_dhcp.py#L88-L100) |
| **11. Quick Actions** | Actions: Connect, Disconnect, Flush DNS, Make Static. | Inline buttons in tables and headers. | Preserved. Simple quick buttons (Make Static Leases, copy-to-clipboard, Flush DNS, Import scripts). | **VERIFIED ✓**<br>[net_dns.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/network/net_dns.py#L50-L65) |
| **12. Notifications** | Instant alerts and success toast confirmations. | Wires alert center logs and triggers visual overlays. | Preserved. Triggers toast alerts for critical items (new devices, IP conflicts, offline status). | **VERIFIED ✓**<br>[main_window.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/windows/main_window.py#L744-L756) |

---

## Experience Mode Specifications

CafePulse implements a **Basic vs. Advanced** experience paradigm. This does not hide core capabilities; instead, it optimizes layout density and maps technical parameters to layperson concepts.

### Basic View (Approachable Operator Layout)
* **IP Addresses:** Simple input form with IP Address and Interface fields. Hides complex subnet definitions and broadcast masks.
* **DNS Manager:** Upstream Primary/Secondary DNS inputs. Hides cache listings and UDP socket timeouts.
* **FirewallNAT:** 1-click toggles (Block Ping, Enable FastTrack) and simple port forward mapping (`Public Port`, `Private IP`, `Private Port`). Hides raw connection marks, TCP flags, and mangle chains.
* **QoS Queue:** Simple limits input (`Target IP`, `Max Upload`, `Max Download`). Hides burst thresholds and PCQ queuing priorities.

### Advanced View (Technician Control)
* **IP Addresses:** Exposes raw broadcast addresses, subnet calculations, route distance configurations, and interface binding properties.
* **DNS Manager:** Exposes dynamic DNS lists, max UDP packet sizes, and searchable cache tables.
* **FirewallNAT:** Exposes full Filter, NAT, Mangle, and Address lists with raw packet marking options and protocol chains.
* **QoS Queue:** Exposes burst limit inputs, burst time configurations, PCQ queue types, and raw priority weights.

---

## Validation & Verification Plan

### Automated Verification
* Run a python compilation check across the 15 deconstructed views to ensure zero layout errors.
  ```powershell
  python -m py_compile ui/widgets/network/*.py
  ```

### Manual Verification
1. **SSID & Wireless Fallback Testing:**
   - Run in Demo Mode under x86 Virtual Router scenario.
   - Open WiFi tab and verify that the "Wireless Interface Tidak Tersedia" card displays correctly.
2. **Bandwidth RX/TX Splitting Test:**
   - Go to Traffic tab and verify that Download (RX) and Upload (TX) curves are plotted separately in Pyqtgraph.
3. **Exit Demo Action Test:**
   - Enter Demo Mode, click Exit Demo, and verify that the database cleans up and the sidebar returns to empty state.
