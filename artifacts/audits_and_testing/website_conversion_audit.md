# CafePulse Revision 3.0: Website Conversion Audit

This audit evaluates the conversion funnel on the static website through simulated user sessions, identifying layout friction and conversion blockers.

---

## 1. User Observation Block Simulations

### 1.1 The 30-Second Glance (First Impression)
- **Objective**: Does the user understand what the product is and who it is for?
- **Findings**: The hero title is bold and states: *"Powerful MikroTik Operations Platform"*.
- **Risks**: The subtitle lacks specific targeting. A home WiFi user might think this is for them, whereas it is actually for commercial/intranet administrators.
- **Recommendations**: Refine the hero copy to clearly define target users: *"A local-first management utility for RT/RW Net providers, local coffee shops, and network technicians."*
- **Priority Level**: **HIGH**

### 1.2 The 60-Second Scan (Features & Price)
- **Objective**: Does the user find the price, version differences, and download locations?
- **Findings**: The main CTA buttons are placed in the hero section. However, the exact price is not shown in the home copy unless they navigate to the Pricing page.
- **Risks**: Users hate hidden pricing. If they scan the home page and see no price tags, they may suspect a monthly cloud billing model.
- **Recommendations**: Add a small price badge directly in the hero area or right below the CTAs: *"Rp499.000 (One-Time Purchase). No monthly fees."*
- **Priority Level**: **HIGH**

### 1.3 The 120-Second Inspection (Trust & Integration)
- **Objective**: Does the user understand how to install and connect it, and how the licensing works?
- **Findings**: The download options are clear, but there is no visual preview of the actual application dashboard on the home page (the home page currently uses `assets/splash.png` as a general placeholder).
- **Risks**: Users are hesitant to download a desktop file (`.exe`) without seeing screenshots of the actual app dashboard, charts, and voucher panels.
- **Recommendations**: Replace general artwork with actual **anonymized application screenshots** (dashboard view, voucher generator) in the features overview section.
- **Priority Level**: **CRITICAL**

---

## 2. Key Conversion Blockers Identified

1. **"Lifetime" Skepticism**:
   - *Issue*: Stating "Lifetime Updates" on a Rp499.000 one-time product looks like scam copy.
   - *Resolution*: Use the standard **5-Year Update Entitlement** format to build business credibility.
2. **Missing App Previews**:
   - *Issue*: No actual application interface previews are visible.
   - *Resolution*: Follow the `screenshot_capture_plan.md` to add high-fidelity screenshots.
3. **No Direct Setup Details**:
   - *Issue*: Users want to know how the app connects to the router (API vs SSH) before downloading.
   - *Resolution*: Display the command `/ip service set api disabled=no` directly on the homepage features section.
