@echo off
title CafePulse Installer Compiler
echo ==================================================
echo CafePulse Windows Installer Compiler
echo ==================================================
echo.

set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

:: 1. Check if compiled distribution exists
if not exist "dist\CafePulse\CafePulse.exe" (
    echo [ERROR] CafePulse executable not found at: dist\CafePulse\CafePulse.exe
    echo Please compile the application first using: python build.py
    echo.
    pause
    exit /b 1
)

:: 2. Ensure icon.ico exists in assets\branding
if not exist "assets\branding\icon.ico" (
    echo [WARNING] assets\branding\icon.ico is missing.
    echo Trying to generate it from assets\branding\logo.png if Pillow is installed...
    python -c "from PIL import Image; img = Image.open('assets/branding/logo.png'); img.save('assets/branding/icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])" 2>nul
    
    if not exist "assets\branding\icon.ico" (
        echo [ERROR] Could not automatically generate icon.ico.
        echo Please place icon.ico in: assets\branding\icon.ico
        echo.
        pause
        exit /b 1
    ) else (
        echo [SUCCESS] Auto-generated icon.ico successfully!
    )
)

:: 3. Find Inno Setup ISCC compiler
set ISCC_PATH=
for %%P in (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
    "%ProgramFiles%\Inno Setup 6\ISCC.exe"
    "%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe"
    "%ProgramFiles%\Inno Setup 5\ISCC.exe"
) do (
    if exist "%%~P" set ISCC_PATH="%%~P"
)

if "%ISCC_PATH%"=="" (
    echo [ERROR] Inno Setup compiler (ISCC.exe) was not found on your system.
    echo.
    echo To build the installer:
    echo 1. Download and install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo 2. Run this script again, or open the .iss files in installer/ folder directly in Inno Setup.
    echo.
    pause
    exit /b 1
)

echo [INFO] Inno Setup compiler found at: %ISCC_PATH%
echo [INFO] Running installer compilation for FREE EDITION...
%ISCC_PATH% "installer\free\CafePulse_Free_Setup.iss"
set FREE_STATUS=%ERRORLEVEL%

echo.
echo [INFO] Running installer compilation for PROFESSIONAL EDITION...
%ISCC_PATH% "installer\professional\CafePulse_Professional_Setup.iss"
set PRO_STATUS=%ERRORLEVEL%

echo.
echo ==================================================
if %FREE_STATUS% equ 0 (
    if %PRO_STATUS% equ 0 (
        echo [SUCCESS] Both installers compiled successfully!
        echo Output files:
        echo   - ..\exports\CafePulse_Free_Setup.exe
        echo   - ..\exports\CafePulse_Professional_Setup.exe
    ) else (
        echo [WARNING] Free Edition succeeded, but Professional Edition failed!
    )
) else (
    echo [ERROR] Installer compilation failed!
)
echo ==================================================

echo.
pause
