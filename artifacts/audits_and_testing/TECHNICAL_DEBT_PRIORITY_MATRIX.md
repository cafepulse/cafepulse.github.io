# TECHNICAL DEBT PRIORITIZATION MATRIX

Tabel ringkasan berikut merangkum hasil audit dari dokumen `TECHNICAL_DEBT_AUDIT.md`. Matriks ini disusun berdasarkan keseimbangan antara tingkat bahaya risiko (*Risk*) dengan besaran pekerjaan perbaikan dan ancaman regresi kode jika diubah saat ini (*Regression Risk*).

| Debt ID | Kategori | Risk | Regression Risk | Fix Size | Recommendation |
| ------- | -------- | ---- | --------------- | -------- | -------------- |
| **TD-001** | Build / Release (Hardcoded Version) | HIGH | LOW | S | **FIX BEFORE FOUNDER RELEASE** |
| **TD-002** | Architecture / UI (Zombie Thread) | HIGH | HIGH | M | **FIX BEFORE FOUNDER RELEASE** |
| **TD-003** | Build / Release (Cache Automation) | HIGH | LOW | S | **FIX BEFORE FOUNDER RELEASE** |
| **TD-004** | Architecture / Documentation (Logs) | MEDIUM | LOW | M | **FIX BEFORE FOUNDER RELEASE** |
| **TD-005** | UI (Oversized Widgets / Coupling) | LOW | MEDIUM | L | **DO NOT TOUCH** |
| **TD-006** | Licensing / Website (Manual Keys) | MEDIUM | LOW | L | **FIX AFTER FOUNDER RELEASE** |
| **TD-007** | Database / MikroTik (Mocked Configs) | LOW | LOW | XL | **FIX AFTER FOUNDER RELEASE** |

---

### Kriteria Keputusan:
1.  **Fix Before Founder Release:** Masalah kecil namun berisiko fatal pada kestabilan pengujian (Bug laporan versi yang salah, log yang hilang, crash/zombie memory).
2.  **Fix After Founder Release:** Kekurangan infrastruktur otomatisasi pembayaran atau pengerjaan fitur yang dapat ditunda tanpa merusak pengalaman fitur inti.
3.  **Do Not Touch:** Masalah kosmetik pada kode (UI coupling) yang berjalan sempurna saat ini namun berpotensi memicu puluhan error sintaksis baru jika dibongkar. Sama sekali dilarang disentuh di fase rilis *Candidate Stabilization*.
