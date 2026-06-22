# CafePulse - Startup Test Checklist

**Version Tested**: 

## 1. Normal Startup
- [ ] Open application normally.
- [ ] Ensure all log files are generated in `/logs`.
- [ ] Ensure `cafepulse.db` is present in the root folder.
- [ ] Ensure `settings.json` is loaded correctly from `/config`.
- [ ] Verify UI loads within 2 seconds on SSD.
- [ ] Verify splash screen / initialization status (if implemented) runs smoothly.

## 2. Corrupted Environment Handling
- [ ] **Missing Database**: Delete `cafepulse.db` and open app. App should recreate it automatically without crashing.
- [ ] **Corrupted Database**: Write random text into `cafepulse.db`. App should detect corruption, backup the old file, create a fresh database, and notify the user safely without raw exception traces.
- [ ] **Missing Config**: Delete `config/settings.json`. App should fallback to default config and create a new JSON file.
- [ ] **Corrupted Config**: Put invalid JSON (e.g. `{"invalid: json`) into `settings.json`. App should backup the file and reset to defaults.
- [ ] **Missing Writable Directories**: Make `/logs` or `/exports` read-only (or simulate it). App should handle it gracefully, falling back to safe mode or warning the user.

## Notes & Issues Found
- ...
