# CafePulse User Manual Structure

This document outlines the table of contents and chapter structure for the official CafePulse User Manual.

---

## Chapter 1: Introduction
- **1.1 Welcome to CafePulse** (Product overview and pillars)
- **1.2 Free vs. Professional Editions** (Feature set comparison)
- **1.3 Minimum System Requirements** (Supported OS, dependencies)

---

## Chapter 2: Getting Started
- **2.1 Installing CafePulse**
  - Installing via Windows Setup Wizard (`CafePulse_Setup.exe`)
  - Extracting via standalone portable ZIP package
- **2.2 First-Time Onboarding Wizard**
  - Selecting closing behavior (Minimize to Tray vs Smart Safe Close)
  - Selecting layout theme (Light/Dark mode)
- **2.3 Understanding the Workspace Navigation** (Business, Operations, Network, Advanced)

---

## Chapter 3: Basic Local Monitoring
- **3.1 Device Manager Overview**
  - Running a local network scan
  - Identifying active MAC vendors
  - Renaming and categorizing devices
- **3.2 Live Bandwidth Monitor**
  - Reading the live upload/download speed chart
  - Adjusting graph refresh intervals

---

## Chapter 4: MikroTik Professional Observability
- **4.1 Router Connection Settings**
  - Configuring host IP, API port (8728), username, and password
  - Customizing connection timeouts and automatic reconnects
- **4.2 Router System Health**
  - Monitoring CPU load, RAM usage, and active uptime
- **4.3 Active Client Management**
  - Reviewing the DHCP Lease table
  - Inspecting DNS Cache entries
  - Monitoring active Hotspot users (viewing logins and setting profiles)

---

## Chapter 5: Advanced Settings & Customization
- **5.1 Privacy Masking**
  - Toggling sensitive data censors (hiding MAC and IP listings in public views)
- **5.2 Database Maintenance**
  - Configuring automatic log cleanup limits (e.g. 30 days)
  - Pruning inactive devices to keep database slim
- **5.3 Troubleshooting Log Recovery**
  - Accessing the local `logs/` directory
  - Submitting crash logs to support

---

## Appendix
- **Appendix A:** Keyboard Shortcuts Quick Reference (e.g., `Ctrl+Q` to Exit)
- **Appendix B:** Inno Setup command-line parameters
- **Appendix C:** MikroTik API configuration commands (RouterOS CLI setup helper)
