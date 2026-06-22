# CafePulse: Beta Tester Program Final Guidelines

This document details the operational rules, bug reporting workflows, diagnostic collection requirements, and license reward parameters for the CafePulse Beta Tester Program.

---

## 1. Program Size & Legal Boundaries

- **Tester Limit**: The program maintains a strict limit of **10 active Beta Testers**.
- **Legal Boundaries**: 
  - Beta Testers are **not investors** and **not business partners**.
  - Testing participation is voluntary. Rewards are restricted to the license keys detailed in Section 2.

---

## 2. Reward Architecture

Rewards are unlocked upon validation of reported issues by the developer:

| Contributor Tier | Reward | Validation Requirements |
| :--- | :--- | :--- |
| **Top Contributor** | **5-Year Professional License** | Uncovers structural bugs (e.g., database lockups, multithreading crashes) or provides major guide updates. |
| **Contributor** | **1-Year Professional License** | Documents and submits at least **3 validated bugs** with complete system parameters. |

---

## 3. Bug Reporting & Diagnostic Workflow

Testers must submit issues using this structured process:

### 3.1 Step 1: Log Retrieval
- Main logs are saved locally in the `logs/` directory.
- Crash trace files are written to `logs/crash/`.
- The user must locate and attach these logs (or copy the text stack trace) when submitting a bug.

### 3.2 Step 2: System Spec Declaration
Every report must declare:
1. **Host OS**: Windows version (e.g. Windows 11 Build 22621) or Linux distro.
2. **Router Details**: MikroTik RouterBOARD model and RouterOS firmware version.
3. **App Details**: Active CafePulse edition, theme, and connection type (API vs. API-SSL).

### 3.3 Step 3: Step-by-Step Reproduction
- Testers must provide clear instructions to replicate the bug.
- Example:
  1. *Open Connection profiles tab.*
  2. *Connect using API-SSL.*
  3. *Switch to DHCP Lease tab and click 'Release' on an active lease.*
  4. *Application freezes.*

### 3.4 Step 4: Screenshot & Visual Evidence
- Attach high-resolution screenshots highlighting the visual error or UI clip.
- Anonymize private credentials or public WAN IPs before attachment.
