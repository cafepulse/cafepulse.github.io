# CAFEPULSE — FINAL TECHNICAL EXECUTION SPECIFICATION

## Claude AI Execution Master Document

### Version 1.0 — Solo Developer Optimized

---

# IMPORTANT EXECUTION INSTRUCTION FOR CLAUDE AI

This document is NOT a conceptual proposal.

This document is a:

# strict technical execution specification.

Claude AI MUST:

* prioritize stability
* prioritize maintainability
* prioritize low complexity
* avoid overengineering
* avoid enterprise-level architecture
* avoid experimental technologies

The goal is:

# a stable, polished, local-first desktop software product.

---

# PRIMARY DEVELOPMENT OBJECTIVE

Build:

# CafePulse

A modern desktop network visibility & AI-assisted monitoring application with:

## FREE BASIC VERSION

and

## ONE-TIME PURCHASE PRO VERSION

The application MUST:

* work offline
* avoid cloud dependency
* avoid SaaS infrastructure
* support Windows and Linux
* be realistic for solo developer maintenance

---

# DEVELOPMENT PRIORITY ORDER

Claude AI MUST prioritize in this exact order:

1. Stability
2. Clean architecture
3. Smooth UX
4. Reliable packaging
5. Lightweight performance
6. Feature completeness
7. Visual polish
8. Advanced analytics

---

# STRICT NON-GOALS

DO NOT IMPLEMENT:

❌ cloud backend
❌ subscription infrastructure
❌ packet sniffing engine
❌ monitor mode WiFi capture
❌ enterprise SIEM architecture
❌ full IDS/IPS system
❌ deep packet inspection
❌ distributed services
❌ Docker/Kubernetes deployment
❌ web app conversion
❌ GPU-heavy AI
❌ online authentication servers

---

# FINAL TECH STACK (LOCKED)

Claude AI MUST use ONLY these technologies.

---

# LANGUAGE

```text id="h3n3rm"
Python 3.12
```

---

# UI FRAMEWORK

```text id="yx1b2z"
PyQt6
```

Reason:

* stable
* modern
* excellent desktop support
* best balance between performance and UI quality

---

# CHARTING

```text id="l9v7mz"
PyQtGraph
```

Reason:

* lightweight
* realtime capable
* better than matplotlib for monitoring apps

---

# DATABASE

```text id="6x4bqt"
SQLite
```

---

# ORM / DATABASE ACCESS

Use:

```text id="d0m1s3"
sqlite3 standard library
```

DO NOT use:

* SQLAlchemy
* heavy ORM frameworks

Reason:
keep project lightweight and simple.

---

# ROUTER API

Use:

```text id="n0c7vx"
routeros-api
```

---

# DEVICE VENDOR LOOKUP

Use:

```text id="z6j8ke"
mac-vendor-lookup
```

with local cache support.

---

# THREADING MODEL

STRICTLY USE:

```text id="i8y4tu"
QThread
```

DO NOT use:

* multiprocessing
* asyncio
* gevent

Reason:
reduce complexity and prevent UI conflicts.

---

# PACKAGING

Use:

```text id="y0s2ra"
PyInstaller
```

---

# WINDOWS INSTALLER

Use:

```text id="s3l6pw"
Inno Setup
```

---

# LINUX DISTRIBUTION

Generate:

```text id="u8x1dm"
AppImage
```

---

# CONFIGURATION FORMAT

Use:

```text id="m4v9ab"
JSON
```

---

# LOGGING

Use:

```text id="f7k2qo"
Python logging module
```

---

# FINAL APPLICATION ARCHITECTURE

# REQUIRED ROOT STRUCTURE

```text id="yv0q4f"
CafePulse/
│
├── core/
├── modes/
├── ui/
├── database/
├── assets/
├── config/
├── logs/
├── exports/
├── tests/
│
├── main.py
├── requirements.txt
├── README_BASIC.md
├── README_PRO.md
└── LICENSE.txt
```

---

# CORE DIRECTORY STRUCTURE

```text id="p4n8mv"
core/
│
├── scanner/
├── analytics/
├── network/
├── database/
├── logging_system/
├── licensing/
├── security/
└── utils/
```

---

# MODES DIRECTORY STRUCTURE

```text id="x6m3tw"
modes/
│
├── demo/
├── home_wifi/
├── hotspot/
└── mikrotik/
```

---

# UI DIRECTORY STRUCTURE

```text id="j5q7ls"
ui/
│
├── windows/
├── widgets/
├── dialogs/
├── themes/
└── assets/
```

---

# DATABASE DESIGN

# DATABASE ENGINE

Use:

```text id="q1r8vf"
SQLite
```

Database file:

```text id="e0z7pd"
cafepulse.db
```

---

# REQUIRED TABLES

## devices

```sql id="4y3mzn"
id
ip_address
mac_address
hostname
vendor
first_seen
last_seen
status
```

---

## sessions

```sql id="b7v9xo"
id
device_id
session_start
session_end
mode
```

---

## traffic_logs

```sql id="u1n4qa"
id
device_id
upload_speed
download_speed
timestamp
```

---

## alerts

```sql id="v8x0mc"
id
alert_type
device_id
message
created_at
```

---

## settings

```sql id="t2k6rs"
id
key
value
```

---

# REQUIRED DATABASE FEATURES

Claude AI MUST implement:

## database initialization

## schema validation

## auto table creation

## corruption handling

## safe reconnect

## auto cleanup for old logs

---

# UI/UX EXECUTION RULES

# VISUAL STYLE

CafePulse MUST feel:

* modern
* smooth
* cyber-clean
* lightweight
* professional

---

# MUST INCLUDE

## dark mode default

## responsive layouts

## modern dashboard cards

## realtime charts

## animated transitions (lightweight only)

## notification center

## searchable device table

---

# MUST NOT INCLUDE

❌ excessive animations
❌ RGB gamer overload
❌ enterprise complexity
❌ terminal-heavy interface

---

# MAIN WINDOW STRUCTURE

# REQUIRED LEFT SIDEBAR

Sections:

```text id="v1u8mj"
Dashboard
Devices
Analytics
Alerts
Modes
Settings
About
```

---

# REQUIRED TOP BAR

Include:

* current mode
* network status
* active device count
* quick scan button

---

# REQUIRED DASHBOARD

Must include:

* live device count
* live chart
* alerts summary
* active mode
* network health score

---

# APPLICATION MODES EXECUTION

# MODE 1 — DEMO MODE

# PURPOSE

Presentation and testing mode.

---

# REQUIREMENTS

Generate:

* fake devices
* fake traffic
* fake bandwidth
* fake alerts

---

# REQUIRED SCENARIOS

```text id="v7z2xr"
Home Network
Small Cafe
Gaming Night
Coworking Space
Busy Event
```

---

# MUST RUN

Without internet connection.

---

# MODE 2 — HOME WIFI MODE

# PURPOSE

Plug & Play local monitoring.

---

# WINDOWS IMPLEMENTATION

Use:

* arp
* ping sweep
* netsh

---

# LINUX IMPLEMENTATION

Use:

* arp
* nmcli
* iwconfig

---

# FEATURES

## device discovery

## hostname detection

## vendor lookup

## online/offline tracking

## suspicious device alerts

---

# IMPORTANT LIMITATION

Claude AI MUST explicitly state in README:

Home WiFi Mode CANNOT accurately provide:

* full bandwidth analytics
* encrypted traffic inspection
* per-app monitoring

without router-level integration.

---

# MODE 3 — HOTSPOT MODE

# PURPOSE

Temporary hotspot monitoring.

---

# FEATURES

## subnet scan

## portable monitoring

## quick refresh scan

## hotspot session tracking

---

# MUST SUPPORT

* Android hotspot
* iPhone hotspot

---

# MODE 4 — MIKROTIK MODE

# THIS IS THE CORE PRO FEATURE

---

# ROUTER CONNECTION REQUIREMENTS

Claude AI MUST implement:

## connection validation

## reconnect system

## timeout handling

## invalid credential handling

## safe disconnect

---

# FEATURES

## realtime upload/download

## queue monitoring

## active hotspot users

## top bandwidth users

## historical analytics

## congestion analysis

## network health score

---

# POLLING INTERVAL

Default:

```text id="d7t5yn"
2 seconds
```

Must be configurable.

---

# ANALYTICS ENGINE

# BASIC ANALYTICS

## device frequency

## peak usage time

## active session duration

## repeated reconnect detection

---

# PRO ANALYTICS

## top bandwidth users

## congestion estimation

## activity trend analysis

## traffic history

---

# AI-ASSISTED INSIGHTS

# IMPORTANT

AI MUST be:

* deterministic
* lightweight
* rule-based

NOT machine-learning-heavy.

---

# IMPLEMENT USING

Simple rule engine only.

---

# REQUIRED INSIGHT EXAMPLES

```text id="y6m9ae"
Network congestion likely caused by high simultaneous activity.
```

---

```text id="s9r3vk"
This device shows unusually frequent reconnections.
```

---

```text id="w2f7qb"
Peak network usage usually occurs between 8 PM and 10 PM.
```

---

# SECURITY REQUIREMENTS

# REQUIRED

## local credential encryption

## password masking

## safe config storage

## optional MAC anonymization

---

# DO NOT IMPLEMENT

❌ cloud auth
❌ online DRM
❌ invasive telemetry

---

# ERROR HANDLING REQUIREMENTS

THIS IS MANDATORY.

Claude AI MUST implement:

---

# GLOBAL EXCEPTION HANDLER

Application MUST NEVER silently crash.

---

# STARTUP VALIDATION

Check:

* config files
* database
* dependencies
* writable directories

---

# SAFE MODE

If startup fails:
launch minimal recovery mode.

---

# LOGGING SYSTEM

Generate:

```text id="w6p2xc"
logs/app.log
```

---

# THREADING EXECUTION RULES

# STRICT RULES

## UI updates ONLY from main thread

## scanning in QThread workers

## analytics in separate QThread

## no blocking loops in UI

---

# PERFORMANCE REQUIREMENTS

# TARGET MEMORY USAGE

```text id="t5r8nk"
< 500MB RAM typical usage
```

---

# APPLICATION MUST

## start fast

## remain responsive

## support long runtime

---

# README REQUIREMENTS

# README_BASIC.md

Must include:

## installation

## supported platforms

## feature overview

## limitations

## troubleshooting

## FAQ

## screenshots placeholder section

---

# REQUIRED UPGRADE SECTION

This section MUST feel:

* helpful
* professional
* non-aggressive

---

# REQUIRED PSYCHOLOGY STYLE

Use wording similar to:

```text id="f8d4sy"
Want deeper visibility into your network?

CafePulse Pro unlocks:
- realtime bandwidth analytics
- top bandwidth users
- MikroTik integration
- advanced traffic insights
- smart network analytics
```

---

# README_PRO.md

Must include:

## MikroTik setup guide

## testing instructions

## troubleshooting

## router connection examples

## performance recommendations

---

# LICENSE SYSTEM

# BASIC VERSION

No activation required.

---

# PRO VERSION

Use:

* offline license key
* local machine validation
* no cloud verification

---

# LICENSE STORAGE

Store locally in encrypted config.

---

# PACKAGING REQUIREMENTS

# WINDOWS OUTPUT

Generate:

```text id="n7v2le"
CafePulse.exe
```

and:

```text id="q3m6bo"
CafePulse_Installer.exe
```

---

# LINUX OUTPUT

Generate:

```text id="s0x8ju"
CafePulse.AppImage
```

---

# FINAL DISTRIBUTION FILES

Claude AI MUST generate:

---

# FREE VERSION

```text id="x5j2vu"
CafePulse_Basic.zip
```

Contents:

* executable
* config
* assets
* logs
* README_BASIC.md
* LICENSE.txt

---

# PRO VERSION

```text id="m9r1zk"
CafePulse_Pro.zip
```

Contents:

* executable
* installer
* MikroTik modules
* analytics modules
* README_PRO.md
* LICENSE.txt

---

# DEVELOPMENT EXECUTION PHASES

# PHASE 1 — FOUNDATION

Implement ONLY:

* architecture
* UI shell
* SQLite
* logging
* config system
* startup validation

DO NOT implement advanced analytics yet.

---

# PHASE 2 — DEMO MODE

Implement:

* fake devices
* fake charts
* fake alerts

Goal:
stable visual dashboard.

---

# PHASE 3 — HOME WIFI MODE

Implement:

* scanning
* vendor lookup
* device management
* alerts

Goal:
fully usable Basic version.

---

# PHASE 4 — HOTSPOT MODE

Implement:

* hotspot scanning
* temporary sessions
* fast refresh

---

# PHASE 5 — MIKROTIK MODE

Implement:

* RouterOS API
* realtime bandwidth
* historical analytics

Goal:
core Pro functionality.

---

# PHASE 6 — UI POLISH

Implement:

* visual improvements
* transitions
* dashboard refinement

---

# PHASE 7 — AI INSIGHTS

Implement:

* rule engine
* smart recommendations
* congestion detection

---

# PHASE 8 — STABILITY & PACKAGING

Implement:

* installers
* safe mode
* final logging
* packaging
* final ZIP exports

---

# FINAL PRODUCT GOAL

CafePulse MUST become:

# BASIC VERSION

A modern lightweight smart WiFi monitoring tool.

---

# PRO VERSION

A professional local-first AI-assisted network observability tool for advanced users and MikroTik-based monitoring.

---

# FINAL EXECUTION RULE

Claude AI MUST always choose:

* simpler architecture
* more stable solution
* fewer dependencies
* lower maintenance burden

over:

* impressive but fragile engineering.

Because this project is designed for:

# a solo founder building a real sellable software product.
