# CafePulse - Hotspot Mode Real-World Checklist

**Version Tested**: 

## 1. Hotspot Connect / Disconnect
- [ ] Enter Hotspot mode.
- [ ] Have a device connect to the hotspot. Ensure UI registers it.
- [ ] Disconnect device. Ensure UI registers device as 'offline' or left.

## 2. User Idle / Timeout
- [ ] Leave a device connected but idle (no traffic) for 30+ minutes.
- [ ] Check if the device state tracks properly (e.g. marked idle/offline depending on config).

## 3. Network Changes
- [ ] Restart the Hotspot adapter on the OS level.
- [ ] Observe CafePulse's behavior: should handle network dropping gracefully and retry, or show an alert, without crashing.
- [ ] Captive portal reset (if applicable).

## 4. UI Responsiveness
- [ ] Rapidly switch between Hotspot mode and Demo mode.
- [ ] Verify no background polling threads from Hotspot mode persist when switched to Demo.

## Notes & Issues Found
- ...
