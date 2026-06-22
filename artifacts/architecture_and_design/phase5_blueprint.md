PHASE 5 — MIKROTIK MODE TECHNICAL EXECUTION BLUEPRINT
1. RECOMMENDED MODULE ARCHITECTURE

Tujuan utama:
hindari “smart abstraction” berlebihan.

Gunakan arsitektur modular datar dan eksplisit.

Recommended Architecture Style

Gunakan:

Layered Modular Desktop Architecture

Bukan:

MVVM kompleks
event bus
dependency injection framework
plugin system
FINAL PHASE 5 MODULE STRUCTURE
core/
│
├── mikrotik/
│   ├── connection_manager.py
│   ├── polling_worker.py
│   ├── router_client.py
│   ├── reconnect_handler.py
│   ├── timeout_handler.py
│   ├── health_engine.py
│   ├── congestion_engine.py
│   ├── hotspot_monitor.py
│   ├── traffic_monitor.py
│   └── mikrotik_models.py
│
├── analytics/
│   ├── analytics_engine.py
│   ├── trend_engine.py
│   ├── history_engine.py
│   └── insight_engine.py
│
├── database/
│   ├── db_manager.py
│   ├── db_writer.py
│   ├── retention_manager.py
│   └── schema_validator.py
│
├── logging_system/
│   ├── app_logger.py
│   └── error_reporter.py
│
└── security/
    ├── credential_store.py
    └── config_encryption.py
2. RECOMMENDED FILE STRUCTURE ADDITIONS

Tambahan spesifik untuk MikroTik mode:

modes/
└── mikrotik/
    ├── mikrotik_controller.py
    ├── mikrotik_mode_state.py
    └── mikrotik_ui_adapter.py
UI STRUCTURE
ui/
├── windows/
│   └── mikrotik_dashboard.py
│
├── widgets/
│   ├── bandwidth_chart.py
│   ├── hotspot_table.py
│   ├── health_score_card.py
│   ├── congestion_card.py
│   └── live_stats_bar.py
│
└── dialogs/
    ├── mikrotik_login_dialog.py
    ├── reconnect_dialog.py
    └── connection_test_dialog.py
3. QTHREAD SEPARATION PLAN

Ini bagian paling kritikal.

JANGAN campur:

API polling
analytics
database writes
UI rendering

dalam thread yang sama.

RECOMMENDED THREAD MODEL
Main Thread

HANYA:

UI rendering
signal receiving
chart updates
table refresh

Tidak boleh:

polling
database insert
RouterOS call
THREAD 1 — MikroTik Polling Worker
polling_worker.py

Tugas:

RouterOS polling
bandwidth retrieval
hotspot users
interface traffic
queue stats

Interval:
default 2 detik.

Output:
Qt signals only.

THREAD 2 — Analytics Worker
analytics_engine.py

Tugas:

congestion estimation
health score
trend analysis
reconnect pattern detection

Jangan akses UI langsung.

THREAD 3 — Database Writer
db_writer.py

Tugas:

batched SQLite inserts
cleanup scheduling
lightweight write queue

Penting:
database write jangan langsung dari polling thread.

WHY THIS STRUCTURE IS SAFE

Karena:

polling tidak blocked oleh SQLite
analytics tidak freeze UI
chart rendering tetap smooth
thread responsibility jelas

Ini jauh lebih maintainable dibanding event architecture kompleks.

4. DATA FLOW ARCHITECTURE
SIMPLE SAFE FLOW
RouterOS API
    ↓
Polling Worker (QThread)
    ↓
Qt Signal
    ↓
Main Controller
    ↓
├── UI Update
├── Analytics Queue
└── Database Queue
IMPORTANT RULE

Polling worker:

collect data only
zero UI logic
zero chart logic
zero SQLite logic

Ini penting untuk stabilitas.

5. REALTIME POLLING ARCHITECTURE
RECOMMENDED STRATEGY

Gunakan:

QTimer INSIDE QThread

Bukan:

while True loops
sleep-heavy loops
POLLING EXECUTION FLOW
QThread start
    ↓
QTimer every 2s
    ↓
RouterOS API request
    ↓
normalize response
    ↓
emit signals
WHY THIS IS BETTER

Karena:

lebih stabil untuk Qt ecosystem
easier stop/start
cleaner shutdown
less race condition risk
POLLING SPLIT RECOMMENDATION

Jangan polling semua endpoint sekaligus.

FAST POLLING (2s)
realtime bandwidth
active users
interface stats
MEDIUM POLLING (10s)
DHCP leases
hotspot sessions
queue lists
SLOW POLLING (30-60s)
health score recalculation
trend aggregation
analytics snapshot
6. RECONNECT STRATEGY
RECOMMENDED RECONNECT MODEL

Gunakan:

Finite State Connection Manager

Simple saja.

CONNECTION STATES
DISCONNECTED
CONNECTING
CONNECTED
RECONNECTING
FAILED
RECONNECT FLOW
timeout/error
    ↓
mark disconnected
    ↓
retry after delay
    ↓
progressive retry
RECOMMENDED RETRY INTERVAL
Attempt 1 → 3 sec
Attempt 2 → 5 sec
Attempt 3 → 10 sec
Attempt 4+ → 20 sec

Max:
jangan infinite spam reconnect.

IMPORTANT

Saat reconnect:

UI tetap responsive
charts freeze gracefully
tampilkan stale state
jangan clear semua data mendadak
7. TIMEOUT STRATEGY
ABSOLUTE REQUIREMENT

Semua RouterOS request wajib timeout.

SAFE TIMEOUT RECOMMENDATION
API timeout:
3–5 seconds
ON TIMEOUT

Jangan:

crash
reconnect langsung tiap timeout tunggal

Gunakan:

timeout threshold

Contoh:

3 consecutive timeouts
→ trigger reconnect

Ini mengurangi reconnect palsu saat router sibuk.

8. SAFE UI UPDATE ARCHITECTURE
STRICT RULE

UI update:
ONLY via Qt signals.

NEVER DO

❌ direct widget manipulation from worker thread

SAFE FLOW
Worker Thread
    ↓ emit signal
Main Thread Slot
    ↓
Update widgets
CHART UPDATE SAFETY

Untuk PyQtGraph:

reuse plot objects
update data only
jangan recreate chart tiap polling
DEVICE TABLE SAFETY

Jangan full redraw table tiap 2 detik.

Gunakan:

row update only
diff-based refresh

Ini penting untuk RAM dan CPU stability.

9. SQLITE WRITE STRATEGY
JANGAN WRITE SETIAP POLLING

Itu akan:

membebani disk
meningkatkan fragmentation
memperbesar freeze risk
RECOMMENDED DATABASE FLOW

Gunakan:

In-Memory Write Queue

Simple Python list/deque cukup.

WRITE INTERVAL
every 5–10 seconds

Batch insert.

EXAMPLE

Daripada:

500 insert realtime

Lakukan:

single executemany()
SQLITE PERFORMANCE SETTINGS

Saat startup:

PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

Ini sangat penting untuk long runtime stability.

RETENTION POLICY

Auto cleanup:

traffic_logs > 30 days

Configurable.

10. HISTORICAL ANALYTICS PIPELINE
KEEP IT LIGHTWEIGHT

Jangan realtime analytics kompleks.

SAFE ANALYTICS PIPELINE
polling data
    ↓
temporary memory cache
    ↓
periodic aggregation
    ↓
SQLite history tables
RECOMMENDED ANALYTICS WINDOW

Gunakan:

1 minute aggregation
5 minute aggregation
hourly summary

Bukan raw second-by-second permanent storage.

NETWORK HEALTH SCORE

Gunakan deterministic rules saja.

EXAMPLE FACTORS
latency stability
disconnect frequency
congestion level
packet loss estimation
device overload
HEALTH SCORE RANGE
0–100

Simple dan mudah dipahami user.

11. LOGGING FLOW
REQUIRED LOG TYPES
app.log

General runtime.

mikrotik.log

Connection activity:

reconnects
timeout
API errors
analytics.log

Optional lightweight insights log.

LOGGING RULES

Gunakan:

rotating logs
max size limits

Contoh:

5MB × 5 files
NEVER LOG

❌ raw passwords
❌ sensitive credentials

12. FAILURE RECOVERY FLOW
REQUIRED FAILURE RECOVERY
CASE 1 — Router Disconnect

Recovery:

auto reconnect
preserve cached data
UI warning banner
CASE 2 — SQLite Locked

Recovery:

retry write later
queue buffering
no crash
CASE 3 — Polling Worker Crash

Recovery:

auto restart worker
log traceback
notify UI silently
CASE 4 — Corrupted Config

Recovery:

load default config
generate backup
safe mode startup
SAFE MODE

Minimal startup:

disable MikroTik polling
allow settings repair

Ini sangat penting untuk software komersial desktop.

13. PERFORMANCE SAFETY RECOMMENDATIONS
ABSOLUTE PERFORMANCE RULES
DO NOT STORE EVERYTHING

Jangan simpan:

every packet
raw RouterOS dumps
unbounded history
LIMIT CHART HISTORY

Recommended:

last 5–10 minutes realtime

Sisanya:
aggregated summaries.

LIMIT MEMORY CACHE

Gunakan:

deque(maxlen=...)

untuk:

bandwidth history
health trend
alerts cache
AVOID OBJECT EXPLOSION

Jangan buat:

custom object per packet
nested abstractions
dynamic plugin loaders

Gunakan dict sederhana bila cukup.

TARGET SAFE LOAD

Untuk solo-maintained desktop app:

100–300 active devices

sudah realistis dan cukup kuat.

Jangan design untuk “10,000 enterprise devices”.

14. ANTI-OVERENGINEERING RECOMMENDATIONS
DO NOT BUILD

❌ microservices
❌ plugin architecture
❌ websocket systems
❌ distributed queue
❌ dependency injection container
❌ repository pattern mania
❌ CQRS/event sourcing
❌ enterprise telemetry systems

PREFER

✅ flat modules
✅ explicit function calls
✅ simple state containers
✅ Qt signals
✅ lightweight SQLite
✅ deterministic rule engines

IMPORTANT SOLO-FOUNDER RULE

Jika suatu abstraction:

tidak mengurangi bug
tidak mengurangi maintenance
tidak membuat debugging lebih mudah

maka:
JANGAN dibuat.

15. EXACT IMPLEMENTATION ORDER FOR PHASE 5
STEP 1 — MikroTik Connection Layer

Implement:

RouterOS API wrapper
connection validation
timeout handling
reconnect handler

Goal:
stable persistent connection.

STEP 2 — Polling Worker

Implement:

QThread polling
QTimer polling loop
clean stop/start
signal emission

Goal:
stable realtime updates.

STEP 3 — UI Live Dashboard Integration

Implement:

realtime charts
active users
top bandwidth table
live status bar

Goal:
smooth responsive UX.

STEP 4 — Database Write Queue

Implement:

batched inserts
WAL mode
retention cleanup
reconnect-safe writes

Goal:
long runtime stability.

STEP 5 — Historical Analytics

Implement:

aggregation pipeline
usage history
trend summaries
congestion estimation

Goal:
meaningful historical data.

STEP 6 — Health Engine

Implement:

health score
reconnect detection
overload detection
warning system

Goal:
smart monitoring feel.

STEP 7 — Recovery Systems

Implement:

worker restart
safe mode
fallback configs
startup validation

Goal:
commercial-grade resilience.

STEP 8 — Optimization & Stability Testing

Test:

24h runtime
reconnect storms
router reboot
DB stress
UI responsiveness

Goal:
real-world reliability.

FINAL ARCHITECTURAL RECOMMENDATION

CafePulse Phase 5 sebaiknya menjadi:

“A deterministic local desktop observability engine”

bukan:

enterprise NMS
SIEM platform
cloud analytics stack

Keunggulan utama CafePulse justru:

ringan
cepat
offline-first
mudah dipahami
mudah dirawat solo founder
stabil runtime panjang
UI modern tanpa kompleksitas enterprise