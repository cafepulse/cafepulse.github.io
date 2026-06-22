# MikroTik RouterOS API Activation Guide

To connect CafePulse to your MikroTik router, the RouterOS API service must be active. Follow these quick configuration steps.

---

## 1. Enabling API via Winbox or SSH

Open a terminal session on your RouterOS device and execute the following configuration command to enable the API service on the standard port (8728):

```bash
/ip service set api disabled=no port=8728
```

If you prefer to encrypt your API connection (recommended for secure environments, using port 8729), run:

```bash
/ip service set api-ssl disabled=no port=8729
```

---

## 2. Verify Port Routing

Ensure that the API ports are accessible from your diagnostic workstation. You can check the current services status by running:

```bash
/ip service print
```

Look for the `api` and `api-ssl` entries in the output list. They should be marked without the `D` (disabled) flag.

---

## 3. Create a Dedicated Operations User

It is a security best-practice to create a dedicated operations user for CafePulse instead of utilizing the master administrator account.

Run the following command to create a user group with read and write API permission attributes:

```bash
/user group add name=cafepulse-ops policies=read,write,api,test
/user add name=cafepulse password=YOUR_SECURE_PASSWORD group=cafepulse-ops
```

Input these credentials in the CafePulse connection drawer settings to establish the monitoring links.
