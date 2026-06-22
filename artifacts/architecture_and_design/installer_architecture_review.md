# CafePulse Installer Architecture Review

This report details the architectural design and structural specifications for compiling the CafePulse Free Edition and Professional Edition installers.

---

## 1. Selected Installer Engine

For the Windows deployment platform, we recommend **Inno Setup (Version 6+)** for the following technical reasons:
- **Zero Overhead**: Generates single-file, highly compressed setup executables without requiring external runtimes.
- **Silent Installation**: Supports standard CLI flags (`/VERYSILENT`, `/SUPPRESSMSGBOXES`) crucial for deployment by network technicians.
- **Rollback Protection**: Automatically rolls back file states if installation is cancelled or encounters write errors.

---

## 2. Target Installation Folder Structure

The setup wizard will extract the application package into the system Program Files folder (using the `{autopf}\CafePulse` constant):

```
{autopf}\CafePulse\
├── CafePulse.exe           # Main compiled PyQt6 desktop binary
├── LICENSE.txt             # Commercial license and EULA terms
├── README_FREE.md          # Guide for Free Edition users
├── README_PROFESSIONAL.md  # Guide for Professional Edition users
├── _internal\              # PyInstaller runtime folder containing DLLs and library files
├── assets\                 # Branding assets, logos, and UI splash graphics
├── config\                 # Default runtime configuration settings
│   └── settings.json       # Initial user preference configurations
├── logs\                   # [Created Writable] Local execution logger folder
└── exports\                # [Created Writable] Local voucher PDF export folder
```

---

## 3. Desktop, Start Menu, & Uninstaller Rules

- **Shortcuts**:
  * Create a Desktop shortcut: `{userdesktop}\CafePulse.lnk` pointing to `CafePulse.exe`.
  * Create a Start Menu shortcut folder: `{userprograms}\CafePulse\CafePulse.lnk`.
- **EULA Agreement Flow**:
  * The installer wizard will load `LICENSE.txt` and display it in a scrollable text area. The user **must** select the *"I accept the agreement"* radio button to unlock the "Next" button.
- **Uninstaller Specification**:
  * Creates a clean uninstaller registered in the Windows Add/Remove Programs panel.
  * *Critical Rule*: The uninstaller will remove all extracted binaries, DLLs, and registry keys. However, it **must** prompt the user:
    *"Apakah Anda ingin menghapus data database lokal (cafepulse.db) dan pengaturan konfigurasi?"*
    If the user selects "No", the local SQLite database and `settings.json` file inside the user application directory are preserved to prevent accidental data loss.

---

## 4. Edition-Specific Activation Flow

To maintain code unified efficiency, both Free and Professional distributions will use a **single, unified codebase** initialized with the following execution profiles:

### A. Free Edition Flow
* The user installs the Free package.
* Upon startup, the application detects no `license.lic` validation file inside `config/`.
* The GUI defaults to the Free Workspace layout, disabling the voucher generator, scheduling backups, and blocking multi-router connections.

### B. Professional Edition Flow
* The user installs the Professional package.
* Upon first startup, the client presents an activation dialog.
* **Online Activation**: The user inputs their owner name and serial key, and the client creates an encrypted local `license.lic` file bound to their HWID.
* **Offline Activation**:
  1. The user inputs their details and hits "Generate Activation Request".
  2. The client exports a base64-encoded `*.licreq` file.
  3. The user transfers this file to an internet-connected device and emails it to `cafepulse.network@gmail.com`.
  4. The developer returns an encrypted `*.lic` file.
  5. The user clicks "Import Activation File" on their offline machine.
  6. The client decrypts and verifies the HWID hash match, unlocking the Professional Edition.
