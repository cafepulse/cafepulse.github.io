# TECHNICAL DEBT RISK HEATMAP
**Phase:** RC1.2 Stabilization

Peta persebaran ini memberikan pandangan visual tentang klasifikasi *technical debt* saat ini di ekosistem CafePulse.

## Risk & Regression Matrix (4x4)

Kuadran ini menentukan posisi isu teknis. Targetnya adalah menyingkirkan semua yang berada di area **Kiri-Bawah (High Risk / Low Regression)** sebelum *Founder Release*.

| Regression Risk ⬇️ / Danger Risk ➡️ | LOW RISK | MEDIUM RISK | HIGH RISK | CRITICAL RISK |
| :---: | :---: | :---: | :---: | :---: |
| **HIGH** |  |  | `[TD-002]` Thread Lifecycle *(CLOSED)* |  |
| **MEDIUM** | `[TD-005]` UI Over-coupling |  |  |  |
| **LOW** | `[TD-007]` Mocked Advanced Config | `[TD-006]` Manual Licensing<br>`[TD-004]` Centralized Logs *(CLOSED)* | `[TD-001]` Version Sync *(CLOSED)*<br>`[TD-003]` Cache Cleanup *(CLOSED)* |  |

---

### Heatmap Legend
- 🟥 **Zona Bahaya Merah (High Risk / Low-Med Regression):** **CLOSED (Sprint 8)**. Upayanya kecil, tapi efek merusaknya besar jika rilis beta berjalan. (TD-001, TD-003 diselesaikan sepenuhnya).
- 🟧 **Zona Oranye (High Risk / High Regression):** **CLOSED (Sprint 8)**. Diselesaikan secara aman lewat arsitektur *collective wait* (TD-002) untuk mencegah zombie process.
- 🟨 **Zona Kuning (Medium Risk):** **RESOLVED / POST-FOUNDER**. TD-004 ditutup lewat logger sentral persisten. Otomatisasi kunci lisensi (TD-006) ditunda hingga setelah Founder Release.
- 🟩 **Zona Hijau (Low Risk):** Paling aman dibiarkan saja. Merombak di zona ini saat ini adalah pemborosan waktu atau bahkan bunuh diri arsitektur (TD-005, TD-007).

