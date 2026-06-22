# Linux Compatibility Audit Report — CafePulse
### *Targeting Linux Distribution Foundation (Sprint 1) — Locked: Juni 2026*

---

## 1. PENDAHULUAN & CAKUPAN AUDIT

Laporan ini memetakan kesesuaian basis kode (codebase) CafePulse saat ini agar dapat berjalan secara native di sistem operasi berbasis **Linux**. Audit difokuskan pada pemisahan ketergantungan OS (OS decoupling), perintah terminal, interaksi file sistem, manajemen lisensi, dan penyimpanan kredensial.

---

## 2. RINGKASAN STATUS KOMPATIBILITAS (PLATFORM MATRIX)

| Fitur / Komponen | Kategori | File Terkait | Dampak & Solusi Adaptasi |
| :--- | :--- | :--- | :--- |
| **pywin32 / win32*** | **Compatible (Not Used)** | *None* | Tidak digunakan dalam kode Python. |
| **winreg / Windows Registry** | **Requires Adaptation** | `core/licensing/licensing_manager.py`<br>`core/security/credential_store.py` | Digunakan untuk membaca `MachineGuid` sebagai HWID. Di Linux harus digantikan dengan membaca `/etc/machine-id` atau `/var/lib/dbus/machine-id`. |
| **Path Separators** | **Compatible (Safe)** | `core/app_paths.py` | Kode secara konsisten menggunakan `pathlib.Path` dan operator `/` yang bersifat cross-platform. |
| **PowerShell Dependency** | **Compatible (Not Used)** | *None* | Aplikasi tidak bergantung pada pemanggilan `powershell.exe`. |
| **CMD / Subprocess Commands** | **Compatible (Decoupled)** | `core/scanner/arp_scanner.py`<br>`modes/home_wifi/arp_scanner.py`<br>`core/mikrotik/router_discovery.py` | Perintah ping, ipconfig/ip, dan arp telah memiliki cabang platform Windows/Linux yang terisolasi. |
| **Windows Shell Integration** | **Compatible (Protected)** | `main.py` | Pemanggilan `AppUserModelID` dibatasi dalam blok `if sys.platform == "win32"`. |
| **Startup / Auto-Start** | **Compatible (Not Used)** | *None* | Tidak ada penulisan ke folder `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` atau Registry Run keys di kode. |
| **User Data Folder Layout** | **Requires Adaptation** | `core/app_paths.py` | Menggunakan fallback `Path.home() / ".cafepulse"`. Direkomendasikan mengikuti standar XDG (`~/.config/CafePulse`). |

---

## 3. AUDIT RINCI & REKOMENDASI ADAPTASI

### 3.1 Windows Registry & `winreg` (Tinggi)
> [!WARNING]
> Ketergantungan modul `winreg` saat ini bersifat eksklusif pada platform Windows. Modul ini diimpor secara dinamis di dalam fungsi penentu Hardware ID (HWID) dan pembuatan kunci enkripsi kredensial.
- **Masalah:** Di Linux, pemanggilan `import winreg` akan menghasilkan `ModuleNotFoundError`.
- **Adaptasi Aktual Saat Ini:** Kode memiliki blok penanganan error (`try-except`) yang menangkap kegagalan impor dan beralih ke fallback MAC Address (`uuid.getnode()`).
- **Rekomendasi Optimal:** Daripada menggunakan MAC Address fallback yang rentan berubah (misal jika interface jaringan dimatikan), gunakan pembacaan ID mesin Linux standar:
  ```python
  # Menggantikan winreg di Linux
  if platform.system() != "Windows":
      for path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
          if os.path.exists(path):
              with open(path, "r") as f:
                  machine_guid = f.read().strip()
                  break
  ```

### 3.2 Eksekusi Subprocess & Perintah Jaringan (Sedang)
Aplikasi memanggil utilitas baris perintah sistem untuk melakukan discovery jaringan dan ping.
- **Subprocess Flag:** `startupinfo` (dwFlags, SW_HIDE) hanya digunakan jika `PLATFORM == "Windows"` untuk mencegah terminal berkedip. Di Linux, `startupinfo = None` dikirim ke `subprocess.Popen` / `subprocess.run`, yang sepenuhnya aman dan kompatibel.
- **Ping Command:**
  - Windows: `ping -n 1 -w <timeout_ms> <ip>`
  - Linux: `ping -c 1 -W 1 <ip>`
- **ARP Command:**
  - Windows: `arp -a` (di-parsing dengan regex kolom Windows).
  - Linux: `arp -n` (di-parsing dengan regex khusus format output Linux).
- **IP Address Fetch:**
  - Windows: `ipconfig` (di-parsing dengan regex Windows).
  - Linux: `ip -4 addr show` (di-parsing dengan regex Linux).
- **Gateway Fetch:**
  - Windows: `route print 0.0.0.0`
  - Linux: `ip route` (di-parsing dengan regex `default via (\d{1,3}(?:\.\d{1,3}){3})`).

*Hasil Audit:* **100% Kompatibel.** Semua perintah sistem di atas telah terbungkus rapi dalam percabangan kondisi platform yang tepat.

### 3.3 Folder Filesystem Writable & XDG Base Directory (Rendah)
> [!NOTE]
> CafePulse memisahkan berkas instalasi read-only (`sys._MEIPASS`) dengan data konfigurasi/database yang dapat ditulis.
- **Windows:** `%LOCALAPPDATA%\CafePulse\` (contoh: `C:\Users\USER\AppData\Local\CafePulse`).
- **Linux Fallback Saat Ini:** `Path.home() / ".cafepulse"` (contoh: `/home/user/.cafepulse`).
- **Rekomendasi Adaptasi:** Agar mematuhi spesifikasi standar desktop Linux (XDG Base Directory), letakkan konfigurasi di `$XDG_CONFIG_HOME/CafePulse` (default: `~/.config/CafePulse`) dan database di `$XDG_DATA_HOME/CafePulse` (default: `~/.local/share/CafePulse`).

### 3.4 Windows Installer & Packaging Assumptions (Tinggi)
- **Windows Build:** Menggunakan PyInstaller untuk kompilasi biner `onedir` dan Inno Setup (`ISCC.exe`) untuk membuat installer `.exe`.
- **Linux Build:** Inno Setup tidak dapat berjalan di Linux (kecuali melalui Wine, yang sangat tidak disarankan). 
- **Solusi:** Distribusi Linux akan didistribusikan menggunakan format **AppImage**. Format ini mengemas seluruh binary, library Qt6, dan runner menjadi berkas portabel tunggal (`CafePulse.AppImage`) yang dapat langsung dijalankan pengguna tanpa instalasi.

---

## 4. KESIMPULAN AUDIT

**CafePulse memiliki tingkat kompatibilitas Linux yang sangat tinggi.** 
Arsitektur kode sejak awal dirancang dengan isolasi platform yang baik. Tidak ada penggunaan API biner Windows level rendah (seperti direct DLL calls ke Kernel32 atau user32 diluar kosmetik icon taskbar), dan semua ketergantungan utilitas jaringan CLI telah didecoupling dengan skema fallback yang memadai. Proyek ini sangat siap dipindahkan ke fase build Linux.
