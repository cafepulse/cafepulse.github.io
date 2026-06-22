# Branding Resolution Recommendations — CafePulse (Revision 3.0)

This document contains recommendations for resolution adjustments, technical rationale, and risk analyses for all CafePulse branding files.

---

## 1. Resolution Recommendations Table

| Asset Name | Current Resolution | Recommended Resolution | Technical Justification & Impacts |
| :--- | :--- | :--- | :--- |
| **logo.png** | 1536 x 1024 | **1536 x 1536 (1:1)** | Re-centering on a square transparent canvas prevents off-center scaling bugs in square layouts (e.g., Sidebar logos, About headers). |
| **icon.ico** | 256 x 171 | **Multi-Resolution (1:1)** | Windows requires square icons. The bundle should contain: `16x16`, `32x32`, `48x48`, `64x64`, `128x128`, and `256x256` versions inside a single `.ico` file. This resolves blurry taskbar and shortcut icons. |
| **splash.png** | 1536 x 1024 | **960 x 640** | Lowering slightly from the raw 3:2 export avoids unnecessary disk footprint while keeping high DPI sharpness for standard laptop screen boots. |
| **installer_banner.png**| 1536 x 1024| **160 x 58** (or source standard)| Scaled explicitly to match standard Inno Setup header aspect ratios, preventing compiler stretch distortions. |
| **installer_sidebar.png**| 1536 x 1024| **499 x 312** (or source standard)| Scaled explicitly to match standard Inno Setup sidebar layout ratios. |

---

## 2. Platform Impact Matrix

### 2.1 UI Impact
- **Positive:** Icons are crisp on 4K/Retina displays. The Splash Screen logo appears larger and more premium.
- **Negative/Risk:** Larger image sizes inside UI widgets will increase memory footprint if loaded raw without scaling parameters. The PyQt loading code must specify `.scaled()` with `Qt.TransformationMode.SmoothTransformation`.

### 2.2 Installer Impact
- Standardized dimensions prevent the installer compiler from scaling assets arbitrarily, which can cause blurry edges.

### 2.3 Website & Marketing Impact
- High-resolution SVG vectors enable clean rendering on web landing pages, preventing raster pixelation.

---

## 3. Risk Analysis

| Risk | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Blurry/Stretched Icons** | High (current) | Low | Standardize `icon.ico` to a 1:1 aspect ratio using multi-resolution sizes. |
| **Layout Clipping on Low-Res Screens** | Medium | High | Put the revised `AboutPage` inside a responsive `QScrollArea` container so layouts do not clip on 1366x768 monitors. |
| **Increased Startup Boot Time** | Low | Medium | Ensure `splash.png` is optimized (compressed PNG) and does not exceed 1MB. |
