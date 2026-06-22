# CafePulse Screenshot Audit

This audit evaluates the visual capture coverage of the CafePulse system for web presence, marketing materials, and user documentation.

## Current State

- **Current Captured Screenshots**: Only a single visual capture exists (`assets/screenshots/dashboard.png` or `dashboard.png` inside the brain folder) representing the main dashboard page in Professional Edition Demo Mode (Dark Theme).
- **Missing Screenshots**: 
  - Home Page: A visual banner/hero capture is missing.
  - Product Page: Separate views representing the Business, Operations, Network, and Advanced workspaces are missing.
  - Home WiFi / Personal Network: Connected Devices list, DHCP settings, and Advanced scanner views are missing.
  - Hotspot / IAM: Voucher management tables, voucher generation forms, user logs, and monitoring KPIs are missing.
  - Network Configuration: Detailed layout views for DHCP bindings, interfaces, firewall lists, routing rules, DNS, queues, and system parameters are missing.
  - Settings: General visual themes, configurations, licensing center tables, and About layouts are missing.

## Risks & Issues

1. **Low Product Credibility**: Relying purely on graphics and illustrations without showing real software in action decreases user trust and conversion rates.
2. **Missing Feature Validation**: Prospective buyers cannot verify visual claims (like the "Cyber-Dark" or "Premium Light" themes, or voucher PDF generation tools) prior to download or purchase.
3. **Manual Inconsistency**: Manually taking screenshots across multiple builds can result in mismatched screen sizes, different high-DPI scaling factors, and visual inconsistencies (e.g. windows borders, custom sizing).

## Recommendations

1. **Automated Screenshot Harvesting**: Implement a Python script (`scratch/capture_all_screenshots.py`) that boots the PyQt6 GUI inside the professional local environment and captures all 24 required workspace panels programmatically.
2. **Clean Frame Capture**: Resize the window to standard **1280x800** layout boundaries prior to capture, maintaining a clean visual look without host OS borders.
3. **Double-Theme Coverage**: Capture screenshots in the default Cyber-Dark theme to highlight the modern interface aesthetics, and include Light theme variants where applicable.
