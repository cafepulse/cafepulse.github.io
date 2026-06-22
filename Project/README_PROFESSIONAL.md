# CafePulse Professional Edition — MikroTik Network Observability

> Professional local-first AI-assisted network monitoring for MikroTik environments.

---

## MikroTik Setup Guide

### Enable API on MikroTik Router

```routeros
/ip service enable api
/ip service set api port=8728
```

Create a monitoring user:
```routeros
/user add name=cafepulse password=YOUR_PASSWORD group=read
```

### Connect CafePulse Professional to Router

1. Open CafePulse → Modes → MikroTik Mode
2. Enter: Host IP, Port (default 8728), Username, Password
3. Click "Test Connection"
4. If successful, click "Start Monitoring"

---

## Performance Recommendations

- Use a dedicated read-only API user
- Set polling interval ≥ 2 seconds (default)
- For routers with 100+ clients, increase to 5 seconds
- Keep CafePulse running on a machine on the same LAN

---

## Troubleshooting

**Connection refused:**
- Verify API service is enabled: `/ip service print`
- Check firewall allows port 8728 from monitor machine

**Authentication failed:**
- Verify username/password are correct
- Check user has `read` group permissions

**High CPU on router:**
- Increase polling interval in Settings → Network → Polling Interval

---

## License & Activation

CafePulse uses a secure RSA-First licensing system.

### Offline Activation Workflow
1. Open **License Management** in CafePulse.
2. Click **Generate License Request**.
3. Enter your Name and Email, then save the `.licreq` file.
4. Send the `.licreq` file to your CafePulse portal or administrator.
5. You will receive a `.lic` signed license file in return.
6. Click **Import License File (.lic)** in the app to activate your Professional Edition.

See `LICENSE.txt` for legal terms.
