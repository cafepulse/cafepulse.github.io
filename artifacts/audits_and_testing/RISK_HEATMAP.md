# TECHNICAL DEBT RISK HEATMAP
**Phase:** RC1.2 Stabilization

Peta persebaran ini memberikan pandangan visual tentang klasifikasi *technical debt* saat ini di ekosistem CafePulse.

## Risk & Regression Matrix (4x4)

Kuadran ini menentukan posisi isu teknis. Targetnya adalah menyingkirkan semua yang berada di area **Kiri-Bawah (High Risk / Low Regression)** sebelum *Founder Release*.

| Regression Risk ⬇️ / Danger Risk ➡️ | LOW RISK | MEDIUM RISK | HIGH RISK | CRITICAL RISK |
| :---: | :---: | :---: | :---: | :---: |
| **HIGH** |  |  | `[TD-002]` Thread Lifecycle Zombie |  |
| **MEDIUM** | `[TD-005]` UI Over-coupling |  |  |  |
| **LOW** | `[TD-007]` Mocked Advanced Config | `[TD-006]` Manual Licensing<br>`[TD-004]` Fragmented Logs | `[TD-001]` Hardcoded Versions<br>`[TD-003]` Stale PyInstaller Cache |  |

---

### Heatmap Legend
- 🟥 **Zona Bahaya Merah (High Risk / Low-Med Regression):** WAJIB dibenahi. Upayanya kecil, tapi efek merusaknya besar jika rilis beta berjalan. (TD-001, TD-003)
- 🟧 **Zona Oranye (High Risk / High Regression):** HARUS diselesaikan dengan kehati-hatian. Ada di jalur kritis (TD-002) karena menyangkut stabilisasi *threading*.
- 🟨 **Zona Kuning (Medium Risk):** Penting dibenahi, namun bisa diakali secara manual (TD-006) atau diperbaiki dengan ukuran kerja sedang (TD-004).
- 🟩 **Zona Hijau (Low Risk):** Paling aman dibiarkan saja. Merombak di zona ini saat ini adalah pemborosan waktu atau bahkan bunuh diri arsitektur (TD-005, TD-007).
