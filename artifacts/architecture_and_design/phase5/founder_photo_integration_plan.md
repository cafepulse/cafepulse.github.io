# Founder Photo Integration Plan — CafePulse (Revision 3.0)

This plan details the implementation strategy for integrating the founder's portrait (`founder_youbellkey.png`) into the CafePulse UI.

---

## 1. Founder Identity Metadata

- **Public Brand Name:** Youbellkey
- **Legal Name:** Yubelki Yosef Pusli
- **Country:** Indonesia
- **Role:** Founder & Solo Developer

---

## 2. UI Placement & Styling Specifications

### 2.1 About Page: Developer Profile Card
- **Avatar Shape:** **Circle (Circular Crop).** Circular cropped images match the modern cyber-dark design system of CafePulse better than sharp rectangles.
- **Implementation (PyQt6):**
  - Read `assets/branding/founder_youbellkey.png`.
  - Apply a circular mask at runtime using a `QPainter` and `QPainterPath.addEllipse` to create a smooth circular crop.
  - Scale the circular avatar to `160x160` pixels.
- **Card Content layout:**
  - Column 1: Circular Avatar (`founder_youbellkey.png`).
  - Column 2: 
    - Text: **Youbellkey** (Large title, `#38BDF8`).
    - Text: **Founder & Solo Developer** (Subtitle, `#94A3B8`).
    - Text: **Indonesia** (Muted green/gray badge).
    - Bio description: Indonesian independent software engineer committed to offline, local-first tools.

### 2.2 Founder Program Panel (Settings / Licensing)
- Add a small circular founder icon (`32x32` pixels) next to the "Founder Program" descriptor in the licensing settings panel.

### 2.3 Website & Documentation Assets
- Export the cropped circular image to a dedicated asset subdirectory (`assets/branding/web/`) for use in the static website's About and Community sections.
- File named: `founder_youbellkey_avatar.png` (transparent background circular crop).
