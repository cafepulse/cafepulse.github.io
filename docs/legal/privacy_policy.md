# Privacy Policy for CafePulse

**Last Updated: June 2, 2026**

CafePulse ("Company," "we," "us," or "our") is committed to protecting your privacy. This Privacy Policy explains how our desktop application handles information.

---

## 1. Local-First & Offline-First Core Principle

CafePulse is designed as a **local-first and offline-first desktop application**.
- All network monitoring statistics, device database logs, router credentials, and configuration settings are **stored locally on your device** (typically in an SQLite database file `cafepulse.db` and configuration folder `config/`).
- The Software does **not** transmit your network traffic data, MikroTik credentials, active device lists, or usage telemetry to our servers or any third-party cloud provider.
- No network connections are established by the application other than:
  1. Direct local connections to your MikroTik router (via port 8728 or as configured by you).
  2. Local-area network scans (ping and ARP scanning) initiated manually by you.

---

## 2. Information We Collect

### 2.1 License Verification
When you activate a Professional Edition license key, the Software may contact our license server (`license.cafepulse.com`) over HTTPS to validate the key. The information transmitted includes:
- The license key string.
- An anonymous, hashed hardware identifier (to enforce the single-workstation activation policy).
- The version of the Software being activated.

We do **not** collect or transmit any personally identifiable information, router IP addresses, or database content during this validation process.

### 2.2 Error and Crash Reporting
If the application crashes, a local crash log is written to `logs/crash/` on your computer. 
- Crash reports are **not** transmitted to us automatically.
- If you opt to submit a crash log manually to our support team for troubleshooting, the report will contain platform statistics (OS version, Python version, CPU architecture) and the traceback of the code error. It will not contain database records or passwords.

---

## 3. Security of Your Local Data

Because all credentials (including MikroTik passwords and database logs) reside locally on your workstation, the security of this data depends on the security of your computer.
- We recommend restricting unauthorized access to your computer.
- Database files containing credentials should be protected using operating-system-level folder encryption or local permission settings.

---

## 4. Updates to this Policy

We may update this Privacy Policy from time to time. The "Last Updated" date at the top of this page will reflect the latest version. Your continued use of the Software after updates constitutes acceptance of the modified policy.

---

## 5. Contact Information

For any inquiries related to your privacy or data security, please contact us:
- **Email:** privacy@cafepulse.com
- **Website:** https://cafepulse.com/privacy
