# Branding Scale Revision Plan — CafePulse (Revision 3.0)

This plan outlines the layout and code adjustments required to increase the visual presence of branding elements (logo, text, and titles) by approximately **300%** across the CafePulse ecosystem.

---

## 1. Scale Adjustments by Component

### 1.1 Startup Splash Screen
- **Current Layout:** Logo scaled to `80x80` pixels. Slogan at `11px`.
- **Target Scale (+300%):** Increase logo size to `240x240` pixels. Slogan size to `14px`, and title size to `36px` bold.
- **Code Changes:** Update [splash_screen.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/splash_screen.py) where the `logo_lbl.setPixmap` scaling is defined.
- **Dampak Visual:** Logo becomes the massive, high-contrast focal center during startup.

### 1.2 About Page Widget
- **Current Layout:** Logo scaled to `96x96` pixels. Title at `32px`.
- **Target Scale (+300%):** Increase logo size to `288x288` pixels. Slogan size to `16px`.
- **Code Changes:** Update [about_page.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/ui/widgets/about_page.py) header logo scaling.
- **Dampak Visual:** Clearer layout separating the brand symbol from the text.

### 1.3 Main Window & Dialog Titlebars
- **Current Layout:** Window icon scaled to `64x64` at runtime.
- **Target Scale:** Ensure high-definition window icons (standard 256x256 pixel buffer loading) are passed to `app.setWindowIcon`.
- **Code Changes:** Modify [main.py](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/main.py) and login dialog loaders to load larger icons smoothly.

### 1.4 Windows Installer (Inno Setup)
- **Current Layout:** Uses the standard small icon.
- **Target Scale:** Configure Inno Setup compiler to scale and crop the `installer_sidebar.png` and `installer_banner.png` (originally `1536x1024`) to match standard Inno wizard scaling ratios (`499x312` and `79x29` respectively) without stretching artifacts.
- **Code Changes:** Modify [setup_script.iss](file:///c:/Users/USER/Documents/Yubelki/CafePulse/CafePulse/assets/branding/setup_script.iss) to declare:
  ```pascal
  WizardImageFile=installer_sidebar.png
  WizardSmallImageFile=installer_banner.png
  WizardImageStretch=no
  ```
