# CafePulse Screenshot Naming Standard

To ensure that assets are clean, self-documenting, and easy to maintain across the codebase and web repositories, CafePulse establishes a strict, lowercase naming standard for all visual interface captures.

## General Naming Rules

1. **Lowercase Only**: File names must be written completely in lowercase.
2. **Underscore Separation**: Words must be joined using single underscores (`_`). No spaces, hyphens, or uppercase letters.
3. **Descriptive Prefixes**: File names must be prefixed with the active module or page name (`home`, `product`, `homewifi`, `hotspot`, `network`, `settings`).
4. **Clean Extensions**: File names must use lowercase `.png` extension (no `.PNG` or `.jpg`).
5. **No Versioning Tags**: Avoid adding date tags, build numbers, or words like "final", "latest", or "new" (e.g. `home_hero_new_v2.png` is forbidden). Updates must overwrite the existing standard files directly to prevent breaking links.

## Standard Naming Map

Below is the approved naming map for CafePulse web screenshot assets:

| Standard File Name | Component / Page | Visual Description |
| :--- | :--- | :--- |
| `home_hero.png` | Landing Page | Full dashboard view with stats cards and active graph |
| `product_business.png` | Product Page | Analytics dashboard with sales and traffic grids |
| `product_operations.png` | Product Page | Bulk voucher creation and PDF templates |
| `product_network.png` | Product Page | Router overview with resource gauges |
| `product_advanced.png` | Product Page | Advanced firewall rule tracking and command lines |
| `homewifi_family.png` | WiFi Page | Basic mode showing simple family devices list |
| `homewifi_guest.png` | WiFi Page | Guest network management, bandwidth caps, isolations |
| `homewifi_screentime.png` | WiFi Page | Time limits, block/allow schedules, time statistics |
| `homewifi_schedules.png` | WiFi Page | Address leases list and DHCP assignment maps |
| `homewifi_security.png` | WiFi Page | Router access filtering and blacklisted clients list |
| `homewifi_connected.png` | WiFi Page | Active local client network listings |
| `hotspot_management.png` | Hotspot Page | Voucher packages configurations list |
| `hotspot_generator.png` | Hotspot Page | Popup dialog with fields for bulk voucher generation |
| `hotspot_monitoring.png` | Hotspot Page | List of connected customers and session durations |
| `hotspot_analytics.png` | Hotspot Page | Summary charts showing sales and data usage per package |
| `network_discovery.png` | Network Page | Physical interface binders and custom subnet overrides |
| `network_scan.png` | Network Page | Device sweep loading overlay and network scanner logs |
| `network_monitoring.png` | Network Page | Multi-interface bandwidth monitoring graphs |
| `network_analytics.png` | Network Page | Premium BI client diagnostics and historical graphs |
| `network_mikrotik_tools.png` | Network Page | System resource metrics, terminal shell, and logs |
| `settings_license.png` | Settings Page | License validation cards, hardware codes, deactivator |
| `settings_theme.png` | Settings Page | Visual preferences showing theme change dropdown |
| `settings_config.png` | Settings Page | Auto-prune settings, check interval sliders, backup path |
| `settings_about.png` | About Page | Product name, logo, developer credits, licenses, version |

## Implementation Path

All generated files will be written to:
- `website/assets/screenshots/` (for website content references)
- `assets/screenshots/` (for core repository documentation backup)
