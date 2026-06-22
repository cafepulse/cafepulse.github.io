# About Page Revision 2.0 Implementation Plan

This document details the plan to rewrite the CafePulse About Page widget (`ui/widgets/about_page.py`) to conform to the commercial-grade visual specifications in Revision 2.0.

---

## 1. Objectives
- Replace the basic static text layout with a professional, commercial-grade scrollable dashboard.
- Display detailed developer, product, philosophy, and licensing data.
- Dynamically query system version information, build numbers, and the active license status from `LicensingManager`.
- Ensure responsive visual reflow for multiple screen sizes and support dark/light theme switching.

---

## 2. Layout Structure (Qt Widgets)
- **Main Container:** Inherits `QWidget`, utilizing a `QVBoxLayout`.
- **Scroll Area:** A responsive `QScrollArea` to ensure usability on smaller resolutions (e.g. 1366x768 or compact views) with a translucent background and styled scrollbars.
- **Content Widget:** A single styled scrollable container utilizing a `QVBoxLayout` with structured sections:
  1. **Header Section:** Displaying the official scaled CafePulse logo alongside the product version and title.
  2. **Product & Story Split Layout:** Two column cards displaying the official "About CafePulse" summary and "The Story Behind CafePulse".
  3. **Development Philosophy Grid:** A grid flow layout of 6 cards representing the development pillars.
  4. **Technology Stack Card:** A grid card listing supported platforms and components.
  5. **Licensing Status Card:** A dynamically-updated card querying `LicensingManager` showing:
     - License Edition (Free/Basic vs Pro)
     - Serialization mask
     - Update Entitlement countdown and expiry status
     - Specific copyright and trade warnings
  6. **Developer & Contact Card:** Details of the founder, Solo Developer designation, country, and contact links (Web, Email, Discord).

---

## 3. Implementation Steps

### Phase 1: Resource Metadata Alignment
- Confirm version variables and import `LicensingManager` in `about_page.py`.
- Define helper functions to retrieve build date, license status, and expiration limits.

### Phase 2: Widget Reconstruction
- Design custom stylized cards (subclassing `QFrame` or utilizing styled CSS wrappers) for clean UI margins, borders, and gradients.
- Construct the flow layouts for the Philosophy Grid and Technical details.
- Wire theme updates through the existing `update_theme` method.

### Phase 3: Verification
- Compile and test the UI responsiveness by resizing the window.
- Verify that toggling licensing states in the Settings/License panel propagates and refreshes the About Page data.
