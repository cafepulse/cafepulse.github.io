# CafePulse Favicon Audit

This audit evaluates the current icon formats and integration standards of the CafePulse website for modern web and mobile browsers.

## Current State

- **Current Assets**: A single `assets/icon.ico` file exists, which has been compiled to a 1:1 multi-resolution format (supporting 16x16, 32x32, up to 256x256 pixel bounds).
- **Missing Elements**:
  - PNG Favicons: High-DPI transparent favicons (16x16 and 32x32) are missing.
  - Apple Touch Icons: No high-resolution touch icon (180x180 pixels) is declared for iOS Safari bookmarks or home screen shortcuts.
  - Android Web App Icons: No app-manifest-ready icons (192x192 and 512x512 pixels) are compiled.
  - PWA Web Manifest: No `site.webmanifest` configuration is present in the website folder.

## Risks & Issues

1. **Blurry Browser Tabs**: High-DPI screens (Retina displays, 4K monitors) may render standard `.ico` scaling poorly if the browser defaults to low-resolution fallback assets.
2. **Generic Shortcuts**: If mobile visitors add the CafePulse website to their home screen, iOS and Android will generate a generic text/screenshot shortcut instead of displaying a professional product brand icon.
3. **No Web App Manifest**: Modern search engines and browsers score websites lower on mobile integration metrics when PWA standard manifests are missing.

## Recommendations

1. **Programmatic Icon Compilation**: Implement a utility script (`scratch/generate_favicons_and_og.py`) using PIL to crop transparent margins and compile the following standard formats from the high-resolution `logo.png` (or `logo_light.png`):
   - `favicon.ico` (Multi-resolution: 16x16, 32x32, 48x48)
   - `favicon-16x16.png` (Standard tab icon)
   - `favicon-32x32.png` (High-DPI tab icon)
   - `apple-touch-icon.png` (180x180, iOS touch icon)
   - `android-chrome-192x192.png` (PWA application grid icon)
   - `android-chrome-512x512.png` (PWA splash screen icon)
2. **PWA Manifest Injection**: Create a `site.webmanifest` file mapping the app parameters (name, theme colors, icons list) and linking it in the `<head>` of all HTML pages.
3. **Link tags standards**: Configure standard favicon link tags:
   ```html
   <link rel="apple-touch-icon" sizes="180x180" href="./assets/apple-touch-icon.png">
   <link rel="icon" type="image/png" sizes="32x32" href="./assets/favicon-32x32.png">
   <link rel="icon" type="image/png" sizes="16x16" href="./assets/favicon-16x16.png">
   <link rel="manifest" href="./site.webmanifest">
   ```
