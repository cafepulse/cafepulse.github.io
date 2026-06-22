# CafePulse - MikroTik Mode Real-World Checklist

**Version Tested**: 

## 1. Connection & Credentials
- [ ] Login with correct IP, username, password. Ensure successful dashboard loading.
- [ ] Login with incorrect IP (unreachable). Ensure graceful timeout and error dialog, no crash.
- [ ] Login with valid IP but wrong password. Ensure "Authentication Failed" message, no crash.

## 2. API Stability
- [ ] Slow response: Simulate high latency to the router. App should not freeze (UI must remain responsive).
- [ ] Timeout: Unplug the router while scanning. App should report "Offline / Disconnected" gracefully.

## 3. Real-world Anomalies
- [ ] Interface rename: Rename a monitored interface in RouterOS. App should handle missing interface error smoothly.
- [ ] Bandwidth spike: Push 100Mbps+ traffic through the router. Ensure the Traffic Chart handles large numbers correctly without axis/graph breaking.

## 4. Safe Shutdown
- [ ] Close CafePulse while actively polling MikroTik.
- [ ] Verify the MikroTik API connection is cleanly closed to prevent lingering API sessions on the router.

## Notes & Issues Found
- ...
