# THREAD LIFECYCLE INVESTIGATION
**Target Area:** TD-002 (PyQt6 QThread Lifecycle)
**Status:** Completed

## Latar Belakang
Audit TD-002 sebelumnya mencatat adanya *High Risk* terkait *zombie thread* dan manajemen penghentian *worker thread* di latar belakang (`wifi_worker`, `mikrotik_worker`, `demo_worker`). Sesuai arahan Architect, dilakukan investigasi statis terhadap implementasi *Thread Lifecycle* sebelum perubahan kode apapun dilakukan.

## Investigasi Alur Eksekusi
Berikut adalah hasil penelusuran alur *shutdown* (penutupan aplikasi) dari pemicu hingga titik henti *worker*:

1. **Trigger (closeEvent):**
   - Saat pengguna menekan (X) atau memilih *Exit*, `MainWindow.closeEvent()` dipanggil.
   - Event dilempar ke `_close_app()`, kemudian ke `_finalize_and_exit()`.
2. **Shutdown Sequence:**
   - Langkah ke-3 dalam `_finalize_and_exit()` adalah memanggil `self._stop_all_workers()`.
3. **Pemberhentian Worker (_stop_all_workers):**
   - Mengiterasi seluruh *worker* (`_demo_worker`, `_wifi_worker`, `_hotspot_worker`, `_mikrotik_worker`).
   - Memanggil fungsi `stop()` pada tiap *worker*.
   - Memanggil `worker.wait(5000)`. Jika dalam 5 detik *worker* belum mati, dilakukan penghentian paksa via `worker.terminate()` (diikuti `worker.wait(1000)`).

## Investigasi Internal Worker
Bagaimana masing-masing *worker* merespons panggilan `stop()`?

1. **`wifi_worker.py` (dan `demo_worker`, `hotspot_worker`):**
   - *Architecture:* Menggunakan *infinite loop* `while self._running:` dan `msleep()`. Tidak memanggil event loop Qt `exec()`.
   - *Response:* Fungsi `stop()` mengatur flag `self._running = False` dan langsung memanggil `self.wait(5000)`.
   - *Kesimpulan:* Berjalan normal. Loop akan segera berhenti pada iterasi maksimal 500ms berikutnya.

2. **`polling_worker.py` (MikroTik Worker):**
   - *Architecture:* Menggunakan sinkronisasi `QTimer` dan memanggil `self.exec()` untuk memulai Qt event loop.
   - *Response:* Fungsi `stop()` menghentikan semua timer, lalu memanggil `self.quit()` (untuk keluar dari event loop `exec()`), dan diikuti `self.wait()`.
   - *Kesimpulan:* `quit()` dikirim dengan benar, event loop berhenti secara elegan (Graceful Shutdown).

## Kesimpulan Investigasi (Zombie Thread Realitas vs Potensi)

**TIDAK ADA BUKTI NYATA KEMUNCULAN ZOMBIE THREAD PADA KONDISI NORMAL.**

Sistem secara arsitektural telah memiliki jaring pengaman (fallback `terminate()`) jika thread tersangkut. Regresi *race condition database* yang disebutkan ("P0 - Thread Database Race on Shutdown") sesungguhnya telah ditambal (patched) pada pengembangan Sprint 1/2 melalui mekanisme `closeEvent` yang ketat. 

Satu-satunya anomali kecil adalah **redudansi pemanggilan `wait()`**. Fungsi `stop()` di *worker* memanggil `wait(5000)`, dan `_stop_all_workers` juga kembali memanggil `wait(5000)`. Hal ini membuat UI *freeze* ganda, tapi tidak menciptakan memori bocor (leak).

## Rekomendasi Tindakan

1. **Status:** **DO NOT TOUCH (UNTUK SAAT INI)**.
2. Tidak perlu melakukan perombakan arsitektur (`TD-002`) pada fase ini karena sistem terbukti aman (*fail-safe*). Perbaikan kecil (penghapusan `wait` ganda) dapat dilakukan, namun risikonya tidak sepadan dengan keuntungan stabilitas saat ini.
3. Fokus eksekusi dialihkan sepenuhnya ke implementasi **Batch 1** (TD-001, TD-003, TD-004) sesuai persetujuan Architect.
