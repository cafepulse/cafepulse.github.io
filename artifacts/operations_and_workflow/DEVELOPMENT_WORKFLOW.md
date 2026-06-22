# CAFEPULSE DEVELOPMENT WORKFLOW
### *Standar Operasional Pengembangan — v1.0.0 | Juni 2026*

---

## BAGIAN 1 — GIT BRANCHING STRATEGY

### 1.1 Branch Structure

```
main                    ← Production-ready, hanya dari release merge
├── develop             ← Integration branch, hanya dari feature merge
│   ├── feature/*       ← Fitur baru
│   ├── fix/*           ← Bug fixes
│   ├── hotfix/*        ← Critical fixes dari main (bypass develop)
│   └── docs/*          ← Dokumentasi saja
└── release/v*          ← Release candidate (dari develop)
```

### 1.2 Branch Naming Convention

| Tipe | Format | Contoh |
|---|---|---|
| Feature | `feature/[nama-fitur]` | `feature/voucher-bulk-export-pdf` |
| Bug Fix | `fix/[deskripsi-singkat]` | `fix/terminal-popup-subprocess-windows` |
| Hotfix | `hotfix/[issue-code]` | `hotfix/crash-on-startup-v093` |
| Release | `release/v[semver]` | `release/v1.0.0` |
| Docs | `docs/[topik]` | `docs/project-bible-v1` |

### 1.3 Commit Message Convention

Format: `[TYPE]: [Subject line]`

| Type | Digunakan Untuk |
|---|---|
| `feat` | Fitur baru |
| `fix` | Bug fix |
| `refactor` | Refactoring tanpa perubahan behavior |
| `docs` | Perubahan dokumentasi saja |
| `style` | Formatting, whitespace (tanpa perubahan logic) |
| `test` | Penambahan atau perbaikan test |
| `chore` | Build system, dependency updates |
| `perf` | Peningkatan performa |

**Contoh commit messages yang baik:**
```
feat: add bulk voucher PDF export with custom branding
fix: hide CMD terminal window during ping sweep on Windows
docs: add Project Bible v1.0.0 to docs/project_bible/
refactor: extract _make_startupinfo() helper to home_wifi/arp_scanner.py
```

---

## BAGIAN 2 — RELEASE PIPELINE

### 2.1 Semantic Versioning

Format: `MAJOR.MINOR.PATCH.BUILD`

| Komponen | Kapan Naik |
|---|---|
| MAJOR | Breaking changes, perubahan fundamental arsitektur |
| MINOR | Fitur baru yang backward-compatible |
| PATCH | Bug fixes, hotfixes |
| BUILD | Auto-increment untuk setiap build internal |

**Contoh:** `1.0.0.0` → `1.0.1.0` (patch fix) → `1.1.0.0` (minor feature) → `2.0.0.0` (major)

### 2.2 Release Checklist

Sebelum setiap release, wajib melalui checklist berikut:

#### 🔧 Pre-Build

- [ ] Semua feature branches sudah di-merge ke `develop`
- [ ] Zero open CRITICAL atau HIGH bugs
- [ ] `CHANGELOG.md` sudah diperbarui dengan semua perubahan
- [ ] Version number sudah diperbarui di:
  - [ ] `main.py` (`APP_VERSION`)
  - [ ] `assets/branding/version_info.txt`
  - [ ] `installer/free/CafePulse_Free_Setup.iss`
  - [ ] `installer/professional/CafePulse_Professional_Setup.iss`
  - [ ] `website/download.html` (versi display)
- [ ] `requirements.txt` sudah diperbarui

#### 🏗️ Build Phase

- [ ] Jalankan `python build.py` — pastikan output clean tanpa error
- [ ] Verifikasi EXE di `dist/CafePulse/CafePulse.exe` dapat dijalankan
- [ ] Verifikasi portable ZIP di `exports/` tersimpan dengan benar
- [ ] Jalankan `build_installer.bat` — kompilasi kedua installer
- [ ] Test instalasi Free Edition dari setup EXE di mesin fresh
- [ ] Test instalasi Professional Edition dari setup EXE

#### 🧪 Testing Phase

- [ ] Jalankan full test suite: `python -m pytest tests/ -v`
- [ ] Manual testing checklist:
  - [ ] Fresh install → scan jaringan dalam 60 detik ✓
  - [ ] Koneksi ke router MikroTik berhasil (Professional)
  - [ ] Generate 10 voucher PDF berhasil (Professional)
  - [ ] Backup manual berhasil (Professional)
  - [ ] Shutdown bersih — tidak ada dialog "not closed properly" di restart berikutnya
  - [ ] Tidak ada CMD window muncul saat scanning

#### 🚀 Release Phase

- [ ] Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Upload file installer ke `website/releases/v1.0.0/`
- [ ] Update `website/download.html` dengan link versi terbaru
- [ ] Verifikasi download dari website berhasil
- [ ] Post announcement di Discord + komunitas

---

## BAGIAN 3 — CODE QUALITY STANDARDS

### 3.1 Python Code Standards

**Format & Style:**
- Mengikuti PEP 8 dengan batas baris 120 karakter
- Gunakan type hints untuk semua fungsi publik
- Docstring menggunakan format Google Style

```python
# ✅ Good
def ping_host(ip: str, timeout_ms: int = 300) -> bool:
    """Test if a host is reachable via ICMP ping.
    
    Args:
        ip: Target IP address as string.
        timeout_ms: Timeout in milliseconds.
        
    Returns:
        True if host responded, False otherwise.
    """
    ...

# ❌ Bad
def ping(ip, timeout=300):
    # ping host
    ...
```

**Subprocess Windows Rules:**
- SELALU gunakan `STARTUPINFO` dengan `SW_HIDE` untuk subprocess di Windows
- TIDAK PERNAH gunakan `subprocess.run()` atau `subprocess.Popen()` tanpa `startupinfo` parameter
- Gunakan helper function `_make_startupinfo()` yang sudah ada di setiap modul

```python
# ✅ Correct Pattern
def _make_startupinfo():
    if platform.system() == "Windows":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        return si
    return None

result = subprocess.run(cmd, startupinfo=_make_startupinfo(), ...)

# ❌ NEVER DO THIS (causes terminal popup)
result = subprocess.run(cmd, ...)
```

### 3.2 Error Handling Standards

- SELALU log exceptions dengan `logger.exception()` bukan hanya `pass`
- User-facing errors harus menggunakan `QMessageBox` dengan pesan yang human-friendly
- Background worker errors harus emit signal ke UI thread, TIDAK boleh crash silently

```python
# ✅ Good
try:
    router_client.connect()
except ConnectionError as e:
    logger.exception("Failed to connect to router %s", router_ip)
    self.connection_failed.emit(str(e))

# ❌ Bad  
try:
    router_client.connect()
except:
    pass
```

### 3.3 Threading Rules

- Background workers menggunakan `QThread` atau `QRunnable` — TIDAK pernah `threading.Thread` untuk Qt operations
- UI updates dari background thread HARUS menggunakan `QMetaObject.invokeMethod()` atau signals
- TIDAK PERNAH memanggil Qt widget dari non-main thread

---

## BAGIAN 4 — TESTING STANDARDS

### 4.1 Test Structure

```
tests/
├── unit/
│   ├── test_arp_scanner.py
│   ├── test_oui_lookup.py
│   ├── test_voucher_engine.py
│   ├── test_license_manager.py
│   └── test_health_engine.py
└── integration/
    ├── test_database_manager.py
    ├── test_config_manager.py
    └── test_startup_sequence.py
```

### 4.2 Test Requirements

- **Minimum Coverage:** 70% untuk modul `core/`
- **Coverage Exempt:** UI components (`ui/`), demo mode (`modes/demo/`)
- Setiap bug fix HARUS disertai test yang mereproduksi bug tersebut

### 4.3 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=core --cov-report=term-missing

# Run specific test file
python -m pytest tests/unit/test_arp_scanner.py -v
```

---

*Dokumen Development Workflow CafePulse — v1.0.0 | Juni 2026 | Youbellkey*
