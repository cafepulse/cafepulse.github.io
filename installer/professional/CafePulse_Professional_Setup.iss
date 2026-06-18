; =============================================================================
; CafePulse PROFESSIONAL EDITION — Inno Setup Installer Script
; =============================================================================
; Target:    CafePulse_Professional_Setup.exe
; Output:    ..\..\exports\CafePulse_Professional_Setup.exe
; Requires:  Inno Setup 6.x  (https://jrsoftware.org/isinfo.php)
;            PyInstaller build already completed (dist\CafePulse\ exists)
; =============================================================================

#define MyAppName        "CafePulse"
#define MyAppEdition     "Professional Edition"
#define MyAppVersion     "1.0.0"
#define MyAppFullVersion "1.0.0.0"
#define MyAppPublisher   "Youbellkey"
#define MyAppURL         "https://cafepulse.github.io/"
#define MyAppSupportURL  "https://cafepulse.github.io/contact.html"
#define MyAppDownloadURL "https://cafepulse.github.io/download.html"
#define MyAppExeName     "CafePulse.exe"
#define MyAppDataDir     "{localappdata}\CafePulse"

[Setup]
; Unique GUID for Professional Edition — different from Free Edition GUID
AppId={{A2B39E8F-6G22-58B5-CF43-FB628B89B010}
AppName={#MyAppName} {#MyAppEdition}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppEdition} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppDownloadURL}

; Installation path
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=..\..\exports
OutputBaseFilename=CafePulse_Professional_Setup

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

; Version info
VersionInfoVersion={#MyAppFullVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} {#MyAppEdition} Setup
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppFullVersion}

; No admin rights required
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

; ── Default config seed ───────────────────────────────────────────────────────
Source: "..\..\config\settings_default.json"; DestDir: "{app}\config"; Flags: ignoreversion

; ── Legal and documentation files ────────────────────────────────────────────
Source: "..\..\LICENSE";              DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\README_PROFESSIONAL.md";  DestDir: "{app}"; DestName: "README.md"; Flags: ignoreversion

; ── Professional Edition Activation Guide ────────────────────────────────────
; (Create this file to guide Pro users through the license activation process)
; Source: "..\..\docs\ACTIVATION_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; ── Create writable user-data directories in LOCALAPPDATA (no UAC required) ──
Name: "{localappdata}\CafePulse"
Name: "{localappdata}\CafePulse\config"
Name: "{localappdata}\CafePulse\logs"
Name: "{localappdata}\CafePulse\logs\crash"
Name: "{localappdata}\CafePulse\exports"

[Icons]
; Start Menu
Name: "{group}\{#MyAppName} Professional"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\branding\icon.ico"; Comment: "Launch CafePulse Professional Edition"
Name: "{group}\Uninstall {#MyAppName}";    Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\branding\icon.ico"; Tasks: desktopicon; Comment: "Launch CafePulse Professional Edition"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName} Professional Edition"; Flags: nowait postinstall skipifsilent

[Code]
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
        'Do you want to remove your CafePulse user data (settings, logs, database, and license file)?' + #13#10 + #13#10 +
        UserDataPath + #13#10 + #13#10 +
        'Select No to keep your license and data for a future reinstall.',
        mbConfirmation, MB_YESNO or MB_DEFBUTTON2
      );
      if Response = IDYES then
        DelTree(UserDataPath, True, True, True);
    end;
  end;
end;
