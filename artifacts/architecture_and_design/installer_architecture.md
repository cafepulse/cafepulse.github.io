# CafePulse — PHASE 6: Inno Setup Installer Architecture
**Generated:** 2026-06-05

---

## INSTALLER DIRECTORY STRUCTURE

```
installer/
├── free/
│   ├── CafePulse_Free_Setup.iss
│   └── README_installer_free.txt
└── professional/
    ├── CafePulse_Pro_Setup.iss
    └── README_installer_pro.txt
```

Output files (after compilation):
```
exports/
├── CafePulse_Free_Setup.exe
└── CafePulse_Professional_Setup.exe
```

---

## FREE EDITION INSTALLER — DESIGN SPEC

**File:** `installer/free/CafePulse_Free_Setup.iss`

### [Setup] Section
```ini
AppId={{D1A39E8F-5F11-47A4-BF32-EA517A78A009}
AppName=CafePulse Free Edition
AppVersion=1.0.0
AppPublisher=CafePulse
AppPublisherURL=https://youbellkey.github.io/cafepulse-site/
AppSupportURL=https://youbellkey.github.io/cafepulse-site/contact.html
AppUpdatesURL=https://youbellkey.github.io/cafepulse-site/download.html
DefaultDirName={autopf}\CafePulse
DefaultGroupName=CafePulse
OutputDir=..\..\exports
OutputBaseFilename=CafePulse_Free_Setup
SetupIconFile=..\..\assets\branding\icon.ico
WizardImageFile=..\..\assets\branding\installer_sidebar.png
WizardSmallImageFile=..\..\assets\branding\icon.ico
LicenseFile=..\..\LICENSE.txt
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
VersionInfoVersion=1.0.0.0
VersionInfoCompany=CafePulse
VersionInfoDescription=CafePulse Free Edition Setup
VersionInfoProductName=CafePulse
VersionInfoProductVersion=1.0.0.0
```

### [Languages] Section
```ini
Name: "english"; MessagesFile: "compiler:Default.isl"
```

### [Tasks] Section
```ini
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional Icons:"
Name: "startmenuicon"; Description: "Create a Start Menu shortcut"; GroupDescription: "Additional Icons:"; Flags: checked
```

### [Files] Section
```ini
; Application binary and dependencies (PyInstaller onedir output)
Source: "..\..\dist\CafePulse\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Assets (bundled into install directory — read-only, static)
Source: "..\..\assets\branding\icon.ico"; DestDir: "{app}\assets\branding"; Flags: ignoreversion

; License and README
Source: "..\..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\README_FREE.md"; DestDir: "{app}"; DestName: "README.md"; Flags: ignoreversion
```

### [Dirs] Section — APPDATA Writable Directories
```ini
; Create writable user-data directories in APPDATA (survives UAC)
Name: "{userappdata}\CafePulse"
Name: "{userappdata}\CafePulse\config"
Name: "{userappdata}\CafePulse\logs"
Name: "{userappdata}\CafePulse\logs\crash"
Name: "{userappdata}\CafePulse\exports"
```

### [INI] Section — Default Settings Deployment
```ini
; Write default settings.json to APPDATA on first install
; (This creates a minimal clean config for first-time users)
Filename: "{userappdata}\CafePulse\config\settings.json"; Section: ""; Key: ""; String: ""
```
*(Note: Full settings.json deployment handled via [Files] or [Code] section — see below)*

### [Icons] Section
```ini
Name: "{group}\CafePulse"; Filename: "{app}\CafePulse.exe"; IconFilename: "{app}\assets\branding\icon.ico"
Name: "{group}\Uninstall CafePulse"; Filename: "{uninstallexe}"
Name: "{autodesktop}\CafePulse"; Filename: "{app}\CafePulse.exe"; IconFilename: "{app}\assets\branding\icon.ico"; Tasks: desktopicon
```

### [Run] Section
```ini
Filename: "{app}\CafePulse.exe"; Description: "Launch CafePulse"; Flags: nowait postinstall skipifsilent
```

### [Code] Section — First-Run Settings Deployment
```pascal
procedure CurStepChanged(CurStep: TSetupStep);
var
  AppDataPath: String;
  SettingsPath: String;
begin
  if CurStep = ssPostInstall then
  begin
    AppDataPath := ExpandConstant('{userappdata}\CafePulse\config');
    SettingsPath := AppDataPath + '\settings.json';
    if not FileExists(SettingsPath) then
    begin
      FileCopy(ExpandConstant('{app}\config\settings_default.json'), SettingsPath, False);
    end;
  end;
end;
```

---

## PROFESSIONAL EDITION INSTALLER — DESIGN SPEC

**File:** `installer/professional/CafePulse_Pro_Setup.iss`

Identical to Free Edition with these changes:

```ini
AppId={{A2B39E8F-6G22-58B5-CF43-FB628B89B010}  ; Different GUID for Pro
AppName=CafePulse Professional Edition
OutputBaseFilename=CafePulse_Professional_Setup
VersionInfoDescription=CafePulse Professional Edition Setup
```

Additional files:
```ini
Source: "..\..\README_PROFESSIONAL.md"; DestDir: "{app}"; DestName: "README.md"; Flags: ignoreversion
```

The Professional installer does NOT pre-activate the license. License activation is done by the user inside the application via the License page.

---

## UNINSTALLER DESIGN

Inno Setup automatically creates an uninstaller. Key behaviors:

- Removes `{app}\` (install directory) completely
- Does NOT remove `{userappdata}\CafePulse\` (user data preserved)
- User data (database, logs, settings) persists after uninstall — correct behavior for a desktop app
- A post-uninstall prompt can be added: "Remove saved data and license files?"

---

## REQUIRED PREREQUISITES

| Requirement | Inno Setup Action |
|---|---|
| Windows 10 or 11 | `MinVersion=10.0` in [Setup] |
| x64 architecture | `ArchitecturesAllowed=x64compatible` |
| Python runtime | Bundled by PyInstaller — no separate install needed |
| Visual C++ Runtime | Usually bundled by PyInstaller or pre-installed on Win10+ |
| .NET | Not required |
| Administrator rights | Not required at runtime (APPDATA-based) |

---

## BUILD PIPELINE (Complete)

```
Step 1: python build.py
        → PyInstaller compiles CafePulse EXE
        → Creates dist/CafePulse/

Step 2: Create config/settings_default.json
        → Clean defaults (no developer session data)

Step 3: ISCC installer/free/CafePulse_Free_Setup.iss
        → Creates exports/CafePulse_Free_Setup.exe

Step 4: ISCC installer/professional/CafePulse_Pro_Setup.iss
        → Creates exports/CafePulse_Professional_Setup.exe

Step 5: Create portable ZIPs
        → exports/CafePulse_Free_Portable.zip
        → exports/CafePulse_Professional_Portable.zip

Step 6: Upload to GitHub Releases as v0.9-beta
```

---

## FILES TO CREATE

| File | Status |
|---|---|
| `installer/free/CafePulse_Free_Setup.iss` | 🔴 NOT YET CREATED |
| `installer/professional/CafePulse_Pro_Setup.iss` | 🔴 NOT YET CREATED |
| `config/settings_default.json` | 🔴 NOT YET CREATED |
| Updated `CafePulse.spec` with datas[] | 🔴 NOT YET FIXED |
| Updated `main.py` with APPDATA paths | 🔴 NOT YET FIXED |

---

*End of Phase 6 — Inno Setup Installer Architecture*
