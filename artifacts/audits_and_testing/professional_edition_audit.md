# CafePulse — PHASE 4: Professional Edition Audit
**Generated:** 2026-06-05

---

## LICENSE ACTIVATION FLOW (As-Built)

### Online Activation (Offline-Verified)

Despite being called "online activation," this is actually a **fully offline cryptographic process**:

1. User enters `Owner Name` + `Serial Key` (format: `CP-PRO-{CLEANNAME}-{SIG16}`)
2. `LicensingManager.verify_serial_key()` computes expected key from owner name + `SECRET_SALT`
3. If match: `activate_license()` writes an encrypted `license.lic` to `config/`
4. License is encrypted with a machine-bound Fernet key (derived from MAC + hostname + OS)
5. On next launch, `check_license()` decrypts and validates `license.lic`

**Net result: The "activation" is 100% local — no server contact required.**

---

## OFFLINE ACTIVATION FLOW

1. User enters Owner Name + Serial Key → `generate_activation_request()` produces a base64 blob
2. User saves this as a `.licreq` file and emails it to the developer
3. Developer (offline) generates a machine-bound `.lic` file
4. User imports `.lic` file via `import_activation_file()`
5. License is validated and written to `config/license.lic`

**Status:** The UI for this flow exists in `license_page.py`. The developer side (generating the `.lic` response) requires a separate developer tool that does NOT exist in the codebase.

**⚠️ MISSING: Developer-side activation tool for generating `.lic` response files.**

---

## HARDWARE LOCKING

**Is it implemented?** YES ✅

The machine-bound key is derived from:
```
CafePulse:Locked:{MAC}:{hostname}:{platform.system()}:{platform.machine()}
```

This key is used for Fernet symmetric encryption of the license file. If the `.lic` file is copied to another machine, decryption fails because the key is different.

**HWID format:** `CP-HWID-XXXX-XXXX-XXXX-XXXX` (16 hex chars from SHA-256)

---

## LICENSE VERIFICATION PROCESS

`LicensingManager.check_license()`:
1. File existence check
2. File read
3. Fernet decryption with machine-bound key
4. JSON parse
5. `license_type == "professional"` check
6. Returns `True`/`False`

**Caching:** Result is cached at class level after first call. Cache persists for app lifetime.

---

## FAILURE SCENARIO ANALYSIS

### License Invalid (bad file content)
- Decryption returns empty string
- `check_license()` returns `False`
- User treated as Free Edition
- No crash

**Verdict:** ✅ HANDLED

### License Missing (`config/license.lic` not found)
- `check_license()` returns `False` immediately
- Free Edition mode
- No error shown at startup

**Verdict:** ✅ HANDLED

### License Expired (update entitlement period ended)
- `is_eligible_for_updates()` returns `False`
- `get_license_health()` returns `"Expired Update Entitlement"`
- **The license is still considered VALID** — app runs in Professional mode
- Only update notifications are suppressed

**Verdict:** ✅ CORRECT BEHAVIOR per policy ("Software remains functional after update entitlement expires")

### Hardware Changed (MAC address change)
- Machine-bound key changes
- Old `license.lic` decrypts to garbage
- `check_license()` returns `False`
- User locked out of Professional Edition with no recovery path
- **No migration wizard exists**

**Verdict:** 🔴 CRITICAL — User who replaces NIC, connects via VPN (MAC randomization), or gets a new PC loses their license permanently. No documented recovery procedure exists.

### Hardware Changed — VPN / Virtual Adapter
- `uuid.getnode()` may return a virtual adapter's MAC when a VPN is active
- Machine key changes → license decryption fails
- **This can happen on every VPN session for some users**

**Verdict:** 🔴 CRITICAL — Active VPN may break license on every connect.

---

## 5-YEAR UPDATE ENTITLEMENT HANDLING

**Is it implemented?** YES ✅

`activate_license()` calculates:
```python
expires = now.replace(year=now.year + 5)
```
With correct leap-year fallback (Feb 29 → Feb 28).

`is_eligible_for_updates()` compares current time vs `expires_at`.

**Behavior after expiry:**
- License remains valid (Pro features stay unlocked)
- `get_license_health()` returns `"Expired Update Entitlement"`
- License page shows the status
- No force-downgrade to Free Edition

**Verdict:** ✅ CORRECT

---

## SECRET_SALT EXPOSURE (CRITICAL FINDING)

The serial key verification uses a hardcoded salt:
```python
SECRET_SALT = "CafePulseCommercialEditionOfflineSecretSalt2026!!!"
```

This is in plaintext in `core/licensing/licensing_manager.py`.

**Anyone who reads the source code can:**
1. Take any owner name (e.g., "PIRATE")
2. Compute `sha256("CafePulse:PIRATE:CafePulseCommercialEditionOfflineSecretSalt2026!!!").hexdigest()[:16].upper()`
3. Construct key: `CP-PRO-PIRATE-{16CHARS}`
4. Activate a valid Professional license without paying

**This is a zero-effort bypass for anyone with access to the source code or a decompiled binary.**

For a local desktop app with this price point (Rp499.000), this level of protection is arguably acceptable — but the developer must be aware.

**Verdict:** 🟠 HIGH — Known limitation of offline-first licensing. Accepted risk for desktop software at this price tier, but must be documented.

---

## PROFESSIONAL EDITION VERDICT

| Check | Result |
|---|---|
| License activation flow functional | ✅ YES |
| Offline activation flow functional (user side) | ✅ YES |
| Offline activation flow functional (developer side) | 🔴 NO — tool missing |
| Hardware locking implemented | ✅ YES |
| License verification functional | ✅ YES |
| License expiration handled | ✅ YES |
| 5-Year update entitlement working | ✅ YES |
| Hardware change recovery | 🔴 NO — user locked out |
| VPN/virtual adapter resilience | 🔴 NO — MAC-dependent |
| Secret salt protection | 🟠 WEAK — known limitation |

**Overall Professional Edition Readiness: CONDITIONALLY READY (document hardware change limitation, build developer activation tool)**

---

*End of Phase 4 — Professional Edition Audit*
