# Branding Asset Audit — CafePulse (Revision 3.0)

This document contains a visual and technical audit of all branding files stored in the `assets/branding/` directory.

---

## 1. Inventory of Branding Assets

A programmatic audit of the branding directory was executed. Below is the list of current files, their formats, and resolutions.

| Filename | Format | Current Dimensions | Aspect Ratio | Audit Observations |
| :--- | :--- | :--- | :--- | :--- |
| **logo.png** | PNG | 1536 x 1024 | 3:2 | Landscape layout. It contains the logo symbol centered on a white canvas. |
| **logo.svg** | SVG | Vector | Flexible | High-fidelity vector source. Scalable for any size without quality loss. |
| **logo_dark.png** | PNG | 1536 x 1024 | 3:2 | Same as `logo.png` but prepared for dark layouts. |
| **logo_light.png**| PNG | 1536 x 1024 | 3:2 | Same as `logo.png` but prepared for light layouts. |
| **icon.png** | PNG | 1536 x 1024 | 3:2 | Square logo symbol in a 3:2 landscape container (may clip if squashed). |
| **icon.ico** | ICO | 256 x 171 | ~3:2 | Non-square aspect ratio. Standard Windows icons must be 1:1 square. |
| **icon.icns** | ICNS | 1024 x 1024 | 1:1 | Correct square aspect ratio for macOS. |
| **splash.png** | PNG | 1536 x 1024 | 3:2 | High-resolution landscape image. |
| **installer_banner.png**| PNG| 1536 x 1024 | 3:2 | High-resolution landscape image. |
| **installer_sidebar.png**| PNG| 1536 x 1024 | 3:2 | High-resolution landscape image. |
| **founder_youbellkey.png**| PNG| 1254 x 1254 | 1:1 | Perfect square photo of the founder. Excellent resolution for avatars. |
| **founder_photo_hd.png**| PNG| 1254 x 1254 | 1:1 | Copy of `founder_youbellkey.png`. |

---

## 2. Key Issues Identified

1.  **Icon Ratio Mismatch (`icon.ico`):** The `icon.ico` has a dimension of `256x171` (3:2 ratio). Windows requires square `1:1` icon dimensions (e.g. 16x16, 32x32, 48x48, 256x256). Using a non-square icon can lead to stretching or clipping on taskbars and shortcuts.
2.  **Logo Canvas Overhead:** The files `logo.png`, `logo_dark.png`, and `logo_light.png` are `1536x1024` pixels. Most of this space is white or transparent padding. In UI widgets like `AboutPage` and `Sidebar`, the logo looks very small because the widget loads the outer `1536x1024` canvas bounds rather than the actual symbol.
3.  **Installer Banner Aspect Ratio:** In Inno Setup, standard installer banners are `499x312` (sidebar) and `79x29` (top header banner). The `1536x1024` images will be dynamically squashed by the compiler.
