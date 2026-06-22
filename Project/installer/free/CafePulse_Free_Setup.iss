; =============================================================================
; CafePulse FREE EDITION — Inno Setup Installer Script
; =============================================================================
; Target:    CafePulse_Free_Setup.exe
; Output:    ..\..\exports\CafePulse_Free_Setup.exe
; Requires:  Inno Setup 6.x  (https://jrsoftware.org/isinfo.php)
;            PyInstaller build already completed (dist\CafePulse\ exists)
; =============================================================================

#define MyAppName        "CafePulse"
#define MyAppEdition     "Free Edition"
#define MyAppVersion "1.1.0-alpha.1"
#define MyAppFullVersion "1.0.0.0"
#define MyAppPublisher   "Youbellkey"
#define MyAppURL         "https://cafepulse.github.io"
#define MyAppSupportURL  "https://cafepulse.github.io/contact.html"
#define MyAppDownloadURL "https://cafepulse.github.io/download.html"
#define MyAppExeName     "CafePulse.exe"
#define MyAppDataDir     "{localappdata}\CafePulse"

[Setup]
; Unique GUID for Free Edition — do NOT reuse for Professional Edition
AppId={{D1A39E8F-5F11-47A4-BF32-EA517A78A009}
AppName={#MyAppName} {#MyAppEdition}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppEdition} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppDownloadURL}

; Installation path — uses autopf (Program Files for x64 or x86 as appropriate)
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=..\..\..\exports
OutputBaseFilename=CafePulse_Free_Setup

; Branding
SetupIconFile=..\..\assets\branding\icon.ico
WizardImageFile=..\..\assets\branding\installer_sidebar.bmp
WizardSmallImageFile=..\..\assets\branding\installer_small.bmp

; License displayed during install
LicenseFile=..\..\LICENSE

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Architecture — Windows 64-bit only
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Minimum Windows version: Windows 10
MinVersion=10.0.17763

; Prevent multiple simultaneous installer instances
AppMutex=CafePulseSetupMutex_Free

; Version info embedded in the installer EXE itself
VersionInfoVersion={#MyAppFullVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} {#MyAppEdition} Setup
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppFullVersion}

; --- SmartScreen & Privilege Notes ---
; Windows SmartScreen will warn on unsigned installers.
; To fully bypass SmartScreen, sign this installer with an EV Code Signing Certificate.
; Without a certificate, users must click "More info" -> "Run anyway" on first launch.
;
; Install-for-whom dialog: the two lines below make Windows show a dialog
; asking whether to install for current user only OR for all users (admin).
; This is the correct behaviour — do NOT remove these two lines.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";   Description: "Create a Desktop shortcut";    GroupDescription: "Additional Icons:"; Flags: unchecked
Name: "startmenuicon"; Description: "Create a Start Menu shortcut"; GroupDescription: "Additional Icons:"

[Files]
; ── Application binaries (PyInstaller onedir output) ──────────────────────────
Source: "..\..\dist\CafePulse\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Default config seed (copied to LOCALAPPDATA on first launch by app_paths.py) ─
Source: "..\..\config\settings_default.json"; DestDir: "{app}\config"; Flags: ignoreversion

; ── Legal and documentation files ────────────────────────────────────────────
Source: "..\..\LICENSE";     DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\README_FREE.md";  DestDir: "{app}"; DestName: "README.md"; Flags: ignoreversion

[Dirs]
; ── Create writable user-data directories in LOCALAPPDATA (no UAC required) ──
Name: "{localappdata}\CafePulse"
Name: "{localappdata}\CafePulse\config"
Name: "{localappdata}\CafePulse\logs"
Name: "{localappdata}\CafePulse\logs\crash"
Name: "{localappdata}\CafePulse\exports"

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}";          Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\branding\icon.ico"; Comment: "Launch CafePulse Network Operations Platform"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional, based on task selection)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\branding\icon.ico"; Tasks: desktopicon; Comment: "Launch CafePulse Network Operations Platform"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove LOCALAPPDATA user data on uninstall — prompt handled by code section
; (We do NOT auto-delete user data — it's preserved unless user explicitly requests removal)

[Code]
// ── First-run settings seed ──────────────────────────────────────────────────
// The app itself handles seeding via app_paths.seed_settings_if_missing().
// This installer only creates the directories — no Pascal code needed for seeding.

// ── Uninstall cleanup prompt ─────────────────────────────────────────────────
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  UserDataPath: String;
  Response: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    UserDataPath := ExpandConstant('{localappdata}\CafePulse');
    if DirExists(UserDataPath) then
    begin
      Response := MsgBox(
        'Do you want to remove your CafePulse user data (settings, logs, and database)?' + #13#10 + #13#10 +
        UserDataPath + #13#10 + #13#10 +
        'Select No to keep your data for a future reinstall.',
        mbConfirmation, MB_YESNO or MB_DEFBUTTON2
      );
      if Response = IDYES then
        DelTree(UserDataPath, True, True, True);
    end;
  end;
end;
