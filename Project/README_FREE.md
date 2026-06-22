# CafePulse Free Edition — Network Visibility Tool

> Modern, lightweight, local-first network monitoring. No cloud. No subscription.

---

## Installation

### Windows
1. Download `CafePulse_Free.zip`
2. Extract and run `CafePulse.exe`
3. No installation required — portable

### Linux
1. Download `CafePulse.AppImage`
2. `chmod +x CafePulse.AppImage && ./CafePulse.AppImage`

### From Source (developers)
```bash
git clone <repo>
cd CafePulse
pip install -r requirements.txt
python main.py
```

---

## Supported Platforms
- Windows 10/11 (64-bit)
- Ubuntu 20.04+ / Debian 11+
- Other Linux distributions (AppImage)

---

## Feature Overview

| Feature                  | Free Edition | Professional Edition |
|--------------------------|:------------:|:--------------------:|
| Demo Mode                | ✓            | ✓                    |
| Home WiFi Monitoring     | ✓            | ✓                    |
| Hotspot Monitoring       | ✓            | ✓                    |
| Device Discovery         | ✓            | ✓                    |
| Vendor Lookup            | ✓            | ✓                    |
| Basic Alerts             | ✓            | ✓                    |
| MikroTik Integration     | —            | ✓                    |
| Real-time Bandwidth      | —            | ✓                    |
| Advanced Analytics       | —            | ✓                    |
| AI-Assisted Insights     | —            | ✓                    |

---

## Limitations

CafePulse Free Edition **cannot** provide:
- Per-device bandwidth measurement without router access
- Deep packet inspection
- Encrypted traffic analysis
- Historical bandwidth trends

These features require **CafePulse Professional Edition** with MikroTik integration.

---

## Troubleshooting

**App won't start on Linux:**
```bash
sudo chmod +x CafePulse.AppImage
```

**Database error on startup:**
Delete `cafepulse.db` and restart — the app will create a fresh database.

**Devices not showing in Home WiFi mode:**
Run as administrator/root for ARP scan access.

---

## FAQ

**Is my data sent anywhere?**
Never. CafePulse is 100% offline-first. All data stays on your machine.

**Can I use this commercially (cafe, office)?**
Yes. CafePulse Free Edition is free for personal and commercial use.

---

## Want Deeper Visibility?

Want deeper visibility into your network?

CafePulse Professional Edition unlocks:
- Real-time bandwidth analytics per device
- Top bandwidth users at a glance
- MikroTik RouterOS integration
- Advanced traffic insights and congestion analysis
- Smart network analytics with AI-assisted recommendations

---

## Screenshots

Tangkapan layar akan tersedia pada dokumentasi rilis Beta di Github Pages.

---

## License

See `LICENSE.txt`
