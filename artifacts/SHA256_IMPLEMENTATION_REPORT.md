# SHA-256 Checksum Implementation Report

## 1. Objective
Automate the generation of SHA-256 integrity hashes for all compiled binaries and distribute them securely alongside the release artifacts to ensure verifiable downloads.

## 2. Implementation Architecture
I have introduced a centralized Python script, `generate_sha256.py`, located in the repository root. This script scans the `exports/` directory and generates a standard `SHA256SUMS.txt` file compatible with Linux `sha256sum -c` and Windows PowerShell `Get-FileHash`.

### Pipeline Integration
The checksum generation has been injected into both build pipelines:
1. **Windows Local Builds:** `build_installer.bat` now invokes `python generate_sha256.py` immediately after `ISCC.exe` completes the compilation of the `CafePulse_Free_Setup.exe` and `CafePulse_Professional_Setup.exe` files.
2. **Linux CI/CD Builds:** The `.github/workflows/build-linux.yml` file now contains a `Generate SHA-256 Checksums` step that runs `python generate_sha256.py` right before the `upload-artifact` step. This ensures that the AppImage binaries are hashed securely within the immutable GitHub Actions runner environment.

## 3. Website Updates
- Updated `js/main.js` to serve optimized download commands that support reliable fetching.
- Updated `download.html` (and localized variants) to provide instructions on integrity verification. The link to `SHA256SUMS.txt` now accurately points to the expected artifact in the GitHub Releases payload.

## 4. Verification Procedure
Upon the next release tag (e.g., `v1.1.0-beta`), the GitHub Actions workflow will output `CafePulse-Linux-Distributions` containing:
- `CafePulse_Free.AppImage`
- `CafePulse_Professional.AppImage`
- `CafePulse_Free_Portable.zip`
- `CafePulse_Professional_Portable.zip`
- `SHA256SUMS.txt`

Users can verify their downloads by running:
**Windows:**
```powershell
Get-FileHash .\CafePulse_Free_Setup.exe -Algorithm SHA256
```
**Linux:**
```bash
sha256sum -c SHA256SUMS.txt --ignore-missing
```
