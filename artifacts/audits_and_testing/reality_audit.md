# CafePulse — PHASE 1: Complete Repository Reality Audit
**Generated:** 2026-06-05  
**Scope:** Full filesystem audit of all major project folders  
**Purpose:** Identify dead code, placeholders, broken imports, missing dependencies, legacy naming, and technical debt.

---

## SEVERITY LEGEND
- 🔴 **CRITICAL** — Blocks installer packaging or application launch
- 🟠 **HIGH** — Blocks a major user-facing feature
- 🟡 **MEDIUM** — Degrades quality or creates confusion
- 🟢 **LOW** — Cleanup / polish items

---

## 1. ROOT DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| `{core` directory exists | 🟡 MEDIUM | Malformed directory name `{core` in project root. Likely created accidentally by a mis-parsed shell command. Contains 0 useful files. **Dead directory.** |
| `cafepulse.db` in root | 🟡 MEDIUM | Live database file committed to repo root. This is the developer's personal session DB (765 KB). Should be `.gitignore`d, not distributed. |
| `crash_debug.txt` in root | 🟢 LOW | Stale debug file in root. Not part of build output. Should be removed or gitignored. |
| `test_out.txt` in root | 🟢 LOW | Stale test output file. Should be gitignored. |
| `*.md` audit files in root | 🟢 LOW | 10+ audit/consistency markdown files scattered in root (not `docs/`). Messy but not blocking. |
| `build.py` naming | 🟡 MEDIUM | `build.py` header says "Generates `CafePulse_Basic.zip` and `CafePulse_Pro.zip`" but actual output is `CafePulse_Free.zip` and `CafePulse_Professional.zip`. Stale docstring. |
| `CafePulse.spec` — absolute paths | 🔴 CRITICAL | `version` and `icon` fields use absolute paths tied to the developer's machine (`C:\Users\USER\...`). Will fail on any other machine during PyInstaller build. |
| `CafePulse.spec` — empty `datas=[]` | 🔴 CRITICAL | No data files (assets, config, fonts) are declared in the spec. PyInstaller will NOT bundle `assets/`, `config/`, or any runtime files. Packaged app will crash on launch. |

---

## 2. `assets/` DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| `assets/235205426.zip` | 🟡 MEDIUM | Unknown ZIP file in assets root. Appears to be a downloaded zip (numeric name = download ID). Dead file. |
| `assets/screenshots/` — EMPTY | 🟠 HIGH | Screenshots directory exists but is empty. Website product page likely references screenshots that don't exist in this path. |
| `assets/branding/logo.png` — 2.1 MB | 🟡 MEDIUM | Uncompressed PNG at 2.1 MB. Excessive for a splash screen asset. Should be optimized. |
| `assets/branding/setup_script.iss` — wrong URL | 🟡 MEDIUM | `AppURL` set to `https://cafepulse.com` (unregistered domain). Should be `https://youbellkey.github.io/cafepulse-site/`. |
| `assets/branding/setup_script.iss` — single edition | 🟠 HIGH | Only one `.iss` file exists for a single generic setup. No `Free` vs `Professional` edition separation in the installer script. |
| `assets/branding/icon.ico` exists (root) | 🟢 LOW | `icon.ico` exists in both `assets/` root AND `assets/branding/`. Duplicate. `build.py` uses `assets/branding/icon.ico`. Root copy is dead. |

---

## 3. `core/` DIRECTORY

### `core/licensing/`
| Finding | Severity | Details |
|---|---|---|
| `SECRET_SALT` hardcoded in source | 🟠 HIGH | `verify_serial_key()` contains `SECRET_SALT = "CafePulseCommercialEditionOfflineSecretSalt2026!!!"` in plaintext. Anyone reading source code can generate valid serial keys for any owner name. |
| License file path is relative | 🔴 CRITICAL | `LICENSE_FILE_PATH = Path("config/license.lic")` uses a relative path. When packaged and launched from `C:\Program Files\CafePulse\`, this resolves to `C:\Program Files\CafePulse\config\license.lic` which requires admin write access to create. License activation will fail silently on most systems. |
| `LicensingManager._is_pro` is class variable | 🟡 MEDIUM | Class-level cache `_is_pro = None` persists across tests/reloads within the same Python process. Not an issue for production use but creates confusion in testing. |

### `core/security/`
| Finding | Severity | Details |
|---|---|---|
| Machine-bound key uses MAC address | 🟠 HIGH | `uuid.getnode()` returns the MAC address. If the user's network card changes, or they use a VPN that randomizes MACs, the decryption key changes and their license becomes permanently unreadable. No migration/recovery path exists. |
| Fallback key is weak | 🟡 MEDIUM | Fallback encryption key `b"CafePulseFallbackKeySecureString32B="` is a static, known string. If hardware calls fail, all encrypted data uses this key — effectively plaintext. |

### `core/database/`
| Finding | Severity | Details |
|---|---|---|
| `db_path` is relative in `main.py` | 🔴 CRITICAL | `db_filename = config.get("database", "filename", default="cafepulse.db")`. No absolute path resolution. After packaging, resolves relative to the EXE launch directory, which varies by user shortcut. Database will be recreated on every launch from a different working directory. |

### `core/runtime/`
| Finding | Severity | Details |
|---|---|---|
| No `__init__.py` found | 🟡 MEDIUM | `core/runtime/` lists files but no `__init__.py` was confirmed. Must verify Python importability. |

### `core/bandwidth_monitor.py` (root of core/)
| Finding | Severity | Details |
|---|---|---|
| Loose file in `core/` root | 🟢 LOW | `bandwidth_monitor.py` sits directly in `core/` instead of `core/network/`. Inconsistent with the module structure. |

---

## 4. `ui/` DIRECTORY

### `ui/widgets/` — Stub/Alias Files
| File | Severity | Finding |
|---|---|---|
| `home_wifi_page.py` | 🟢 LOW | Backward-compat alias → `PersonalNetworkPage`. Functional but legacy naming. |
| `hotspot_page.py` | 🟢 LOW | Backward-compat alias → `IamPage`. The name `HotspotPage → IamPage` is conceptually misleading. |
| `mikrotik_dashboard.py` | 🟢 LOW | Backward-compat alias → `NetworkPage`. Functional. |

### `ui/widgets/` — Placeholder Pages
| File | Severity | Finding |
|---|---|---|
| `placeholder_page.py` | 🟡 MEDIUM | Generic placeholder widget. Used for features not yet built. If any navigation item silently loads this, user sees blank content with no explanation. |

### `ui/widgets/network/` — UI Mockup Status
| File | Severity | Finding |
|---|---|---|
| `net_firewall.py` | 🟠 HIGH | High-fidelity UI mockup. Firewall rules displayed are static/fake data. No live RouterOS API calls. |
| `net_hotspot.py` | 🟠 HIGH | High-fidelity UI mockup. Hotspot user data is not live. |
| `net_dns.py` | 🟠 HIGH | High-fidelity UI mockup. DNS entries are not live. |
| `net_ppp.py` | 🟠 HIGH | High-fidelity UI mockup. PPP sessions not live. |
| `net_queue.py` | 🟠 HIGH | High-fidelity UI mockup. Queue rules not live. |
| `net_routing.py` | 🟠 HIGH | High-fidelity UI mockup. Routing table not live. |
| `net_system.py` | 🟠 HIGH | RouterOS system info mockup. Not live. |
| `net_backup.py` | 🟠 HIGH | Backup UI may trigger real API calls but fallback behavior unverified. |
| `net_connections.py` | 🟡 MEDIUM | Connections may be partially live via RouterOS API. |
| `net_interfaces.py` | 🟡 MEDIUM | Interfaces may be partially live via RouterOS API. |
| `net_ip_dhcp.py` | 🟡 MEDIUM | DHCP leases may be partially live. |
| `net_wifi.py` | 🟡 MEDIUM | WiFi scan is live via local adapter, not RouterOS. |

---

## 5. `config/` DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| `settings.json` → `"edition": "basic"` | 🟡 MEDIUM | Edition key says `"basic"` — this is legacy naming. Should be `"free"` for Free Edition. |
| `settings.json` → `"default_mode": "demo"` | 🟠 HIGH | Network default mode is `"demo"`. If a fresh install retains this, the user may never see live data and assume the app is broken. |
| `config/.clean` file committed | 🟢 LOW | `.clean` session flag is committed to git. This is a runtime file, should be gitignored. |
| `config/license.lic` committed | 🟡 MEDIUM | Developer's personal `license.lic` is committed to the repository. Should be gitignored. |

---

## 6. `docs/` DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| 44+ markdown files | 🟢 LOW | Excessive number of overlapping audit, strategy, and planning documents. No user impact but adds repository noise. |
| No `reality_audit.md` yet | — | This file (being created now). |

---

## 7. `website/` DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| Download links point to non-existent GitHub Releases | 🔴 CRITICAL | `download.html` links to `https://github.com/cafepulse/CafePulse/releases/latest/download/CafePulse_Setup.exe`. No GitHub Release exists. All download buttons return 404. |
| `winget install CafePulse` shown | 🔴 CRITICAL | App is NOT published to winget. This instruction will fail publicly. |
| Linux AppImage advertised | 🟠 HIGH | Linux build has never been created. `CafePulse.AppImage` link returns 404. |
| `og_preview.png` exists | 🟢 PASS | OG image present in `website/assets/`. |
| Screenshots directory has 5 images | 🟢 PASS | `dashboard_overview.png`, `network_workspace.png`, etc. exist. |
| Contact form has no backend | 🟠 HIGH | `contact.html` form has `id="contact-form"` but no `action` attribute and no server endpoint. Form data goes nowhere. The `contact-status-msg` is shown/hidden via JS but the message is never sent. |
| `mailto:cafepulse.network@gmail.com` present | 🟢 PASS | Direct email link exists as fallback. Functional. |

---

## 8. `build/` AND `build_output/` DIRECTORIES

| Finding | Severity | Details |
|---|---|---|
| `build/` directory empty or stale | 🟡 MEDIUM | PyInstaller work directory. Not relevant to distribution. Should be gitignored. |
| `build_output/` — content unknown | 🟡 MEDIUM | May contain stale build artifacts from previous runs. Not part of release pipeline. Should be gitignored. |
| `dist/` directory exists | 🟡 MEDIUM | PyInstaller output directory. Should be gitignored in production. |

---

## 9. `scratch/` DIRECTORY

| Finding | Severity | Details |
|---|---|---|
| `compile_reports_to_pdf.py` | 🟢 LOW | Development utility. Not part of app. Appropriate location. |

---

## 10. MISSING FILES (Expected but Not Found)

| Expected File | Severity | Impact |
|---|---|---|
| `installer/free/CafePulse_Free_Setup.iss` | 🔴 CRITICAL | No installer script for Free Edition. Cannot build installer. |
| `installer/professional/CafePulse_Pro_Setup.iss` | 🔴 CRITICAL | No installer script for Professional Edition. Cannot build installer. |
| `.gitignore` | 🟠 HIGH | No `.gitignore` found in project root. Database, logs, build artifacts, session files all get committed. |
| `assets/branding/splash.png` (website) | 🟢 PASS | Splash exists in branding folder. ✓ |
| `config/settings_default.json` | 🟡 MEDIUM | No clean default settings template for fresh installs. Installer copies developer's personal `settings.json`. |

---

## SUMMARY TABLE

| Category | Critical | High | Medium | Low |
|---|---|---|---|---|
| PyInstaller / Build | 2 | 1 | 1 | 0 |
| Paths / Packaging | 2 | 0 | 1 | 0 |
| Licensing | 1 | 1 | 1 | 0 |
| Security | 0 | 2 | 1 | 0 |
| Website / Download | 2 | 2 | 0 | 0 |
| UI Mockups | 0 | 8 | 4 | 3 |
| Config | 0 | 1 | 2 | 1 |
| Assets | 0 | 1 | 2 | 1 |
| Repository Hygiene | 0 | 1 | 2 | 4 |
| **TOTAL** | **7** | **17** | **14** | **9** |

---

*End of Phase 1 — Repository Reality Audit*
