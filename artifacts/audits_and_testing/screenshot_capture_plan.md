# CafePulse Website V1: Screenshot Capture Plan

To showcase the CafePulse desktop application on the product website, we need professional, high-resolution screenshots. This plan outlines specifications, categories, and capture guidelines.

---

## 1. Capture Guidelines & Specifications

To ensure the screenshots look premium and display crisp details:
- **Dimensions / Aspect Ratio**: 
  - Standard widescreen: **16:9** (minimum **1920x1080** px for standard retina/desktop displays).
  - Compact dialogs: **4:3** or aspect-ratio locked based on default window size.
- **Theme Selection**: Capture screenshots exclusively in **Cyber-Dark Mode** to align with the website's dark UI branding.
- **Data Anonymization**: 
  - Mask sensitive credentials (e.g. RouterOS passwords, private external IP addresses).
  - Use realistic sample data (e.g. local IPs `192.168.88.x`, standard MAC addresses, mock customer vouchers).
- **Format**: Lossless **PNG** format (compress with tools like `optipng` to minimize file size on GitHub Pages).

---

## 2. Screenshot Categories & Naming Registry

All screenshot files must be stored in: `website/assets/screenshots/` (or `website/images/`).

| Category | Filename Target | Window Content / Mock State | Description |
| :--- | :--- | :--- | :--- |
| **Dashboard** | `scr_dashboard.png` | Main Dashboard workspace with live client counters and system status dot (green). | Shows overall network overview at a glance. |
| **Devices** | `scr_device_manager.png` | Table showing discovered local devices, resolved vendors (Apple, Intel), and IP addresses. | Demonstrates local-first discovery scanner. |
| **Hotspot** | `scr_hotspot_voucher.png` | Voucher Generator panel displaying active limits, batch settings, and PDF preview. | Showcases the ease of batch voucher printing. |
| **Analytics** | `scr_analytics_charts.png` | Live PyQtGraph speed charts plotting active WAN upload/download traffic. | Displays observability module. |
| **MikroTik** | `scr_mikrotik_stats.png` | Router CPU, RAM utilization charts, and DHCP lease lists. | Highlights RouterOS native integration. |
| **Settings** | `scr_settings.png` | Connection configuration drawers and offline backup scheduler settings. | Demonstrates control parameters. |
| **About** | `scr_about_dialog.png` | Dialog showing app version (`v1.0.0.0`) and "Founder" program badge badge. | Shows build details. |
| **License** | `scr_licensing.png` | Pro module activation drawer displaying license status validation success. | Demonstrates simple Pro activation. |

---

## 3. Web Page Asset Placement

- **Homepage (`index.html`)**: Insert `scr_dashboard.png` inside the Hero area and `scr_hotspot_voucher.png` in the quick features overview.
- **Product Page (`product.html`)**: Embed `scr_device_manager.png`, `scr_analytics_charts.png`, and `scr_mikrotik_stats.png` next to their respective workspace descriptions.
- **Download Page (`download.html`)**: Display `scr_about_dialog.png` to preview the desktop app user interface.
