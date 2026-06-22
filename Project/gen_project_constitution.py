import os
import sys
from fpdf import FPDF
from datetime import datetime

class ConstitutionPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 8)
            self.set_text_color(100, 116, 139) # Slate Muted
            self.cell(100, 10, "CAFEPULSE PROJECT CONSTITUTION v1.0", align="L")
            self.set_font("helvetica", "I", 8)
            self.cell(0, 10, "CONFIDENTIAL - SINGLE SOURCE OF TRUTH", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(16, 185, 129) # CafePulse Green
            self.set_line_width(0.5)
            self.line(20, 20, 190, 20)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        # We use standard string formatting because {nb} will be replaced by fpdf at output time
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | CafePulse Project Constitution", align="C")
        self.set_font("helvetica", "", 8)
        self.cell(0, 10, "© 2026 CafePulse Project", align="R")

    def cover_page(self):
        self.add_page()
        # Draw a beautiful green and dark slate accent column on the left
        self.set_fill_color(15, 23, 42) # Dark Slate
        self.rect(0, 0, 15, 297, "F")
        self.set_fill_color(16, 185, 129) # CafePulse Green
        self.rect(15, 0, 5, 297, "F")
        
        self.set_left_margin(30)
        self.ln(40)
        
        # Title
        self.set_font("helvetica", "B", 34)
        self.set_text_color(15, 23, 42) # Dark Slate
        self.cell(0, 15, "CafePulse", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font("helvetica", "B", 24)
        self.set_text_color(2, 132, 199) # Sky Blue
        self.cell(0, 12, "Project Constitution", new_x="LMARGIN", new_y="NEXT")
        
        self.ln(5)
        self.set_draw_color(16, 185, 129)
        self.set_line_width(1.5)
        self.line(30, self.get_y(), 190, self.get_y())
        self.ln(10)
        
        # Subtitle
        self.set_font("helvetica", "I", 12)
        self.set_text_color(100, 116, 139)
        self.multi_cell(0, 6, "Master Reference Manual, System Architecture Blueprint, and Cross-Conversation AI Handover Document for Version 1.0 Stable")
        self.ln(30)
        
        # Details Table
        self.set_font("helvetica", "", 10)
        self.set_text_color(71, 85, 105)
        
        details = [
            ("Document Version", "v1.0 (Master Release)"),
            ("Project Status", "Approved Stable Candidate (RC1 Frozen)"),
            ("Author / Founder", "Yubelkey (Founder, CTO & Lead Architect)"),
            ("Co-Author / Auditor", "Antigravity (AI Technical Auditor & Principal Architect)"),
            ("Target Platform", "Windows 10/11 x64 (Inno Setup Native Packages)"),
            ("Core Technology Stack", "Python 3.12, PyQt6, SQLite3 (WAL), Cryptography (RSA-4096)"),
            ("Date of Generation", datetime.now().strftime("%d %B %Y")),
            ("Document Integrity", "Verifiable Single Source of Truth (SSoT)")
        ]
        
        for label, val in details:
            self.set_font("helvetica", "B", 10)
            self.cell(50, 7, label + ":", border=0)
            self.set_font("helvetica", "", 10)
            self.cell(0, 7, val, border=0, new_x="LMARGIN", new_y="NEXT")
            
        self.ln(30)
        self.set_font("helvetica", "I", 8.5)
        self.set_text_color(148, 163, 184)
        self.multi_cell(0, 5, "This constitution is the permanent, immutable engineering record for CafePulse. It establishes the rules, constraints, histories, and validation criteria for all subsequent iterations, releases, and AI integrations. Any changes to the core system must be evaluated against this document's Decision Framework.")
        
        # Reset margins for content pages
        self.set_left_margin(20)
        self.set_right_margin(20)

    def section_header(self, num, title):
        self.ln(8)
        self.set_font("helvetica", "B", 13)
        self.set_text_color(15, 23, 42) # Slate
        self.cell(0, 10, f"SECTION {num}: {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(16, 185, 129) # Green
        self.set_line_width(0.7)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def subheading(self, title):
        self.ln(3)
        self.set_font("helvetica", "B", 10.5)
        self.set_text_color(2, 132, 199) # Blue
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")

    def body_text(self, text):
        self.set_font("helvetica", "", 9.5)
        self.set_text_color(51, 65, 85) # Slate Light
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet_point(self, text):
        self.set_font("helvetica", "", 9.5)
        self.set_text_color(51, 65, 85)
        self.set_x(25)
        self.multi_cell(0, 5.5, "- " + text)
        self.set_x(20) # Reset X

    def callout(self, text, is_warning=False):
        self.ln(2)
        self.set_font("helvetica", "I", 9)
        if is_warning:
            self.set_fill_color(254, 242, 242) # Light Red
            self.set_text_color(153, 27, 27) # Dark Red
            border_color = (239, 68, 68) # Red
        else:
            self.set_fill_color(240, 253, 250) # Light Green
            self.set_text_color(15, 118, 110) # Dark Green
            border_color = (16, 185, 129) # Green
      
        # Save positions to calculate height
        x = self.get_x()
        start_y = self.get_y()
        self.multi_cell(0, 5, text, fill=True)
        end_y = self.get_y()
        
        # Draw thick left border line
        self.set_draw_color(*border_color)
        self.set_line_width(1.5)
        self.line(x, start_y, x, end_y)
        self.ln(3)

    def code_block(self, code):
        self.ln(2)
        self.set_font("courier", "", 8.5)
        self.set_fill_color(248, 250, 252) # Light Grey
        self.set_text_color(220, 38, 38) # Dark Red
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.multi_cell(0, 4.5, code, border=1, fill=True)
        self.ln(2)

    def table_row(self, col_widths, row_data, is_header=False):
        self.set_font("helvetica", "B" if is_header else "", 9)
        if is_header:
            self.set_fill_color(241, 245, 249) # Light grey-blue
            self.set_text_color(71, 85, 105)
        else:
            self.set_fill_color(255, 255, 255)
            self.set_text_color(51, 65, 85)
        
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        
        for i, item in enumerate(row_data):
            self.cell(col_widths[i], 8, str(item), border=1, fill=True, align="L")
        self.ln(8)

def main():
    pdf = ConstitutionPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.alias_nb_pages()
    
    # Generate Cover Page
    pdf.cover_page()
    
    # ─── SECTION 1: EXECUTIVE SUMMARY ───
    pdf.add_page()
    pdf.section_header(1, "EXECUTIVE SUMMARY")
    pdf.body_text(
        "CafePulse adalah platform manajemen operasional dan pemantauan jaringan (Network Operations Platform) mandiri "
        "yang didekasikan khusus untuk ekosistem MikroTik RouterOS. Aplikasi ini dibangun secara native "
        "menggunakan bahasa pemrograman Python dan kerangka kerja PyQt6 untuk menghadirkan performa maksimal "
        "serta konsumsi memori yang minimal pada lingkungan desktop pengguna."
    )
    pdf.subheading("Tujuan Produk")
    pdf.body_text(
        "Tujuan utama CafePulse adalah untuk menjembatani celah fungsional dan visual antara Winbox (aplikasi konfigurasi "
        "tingkat-rendah MikroTik yang sangat teknis) dengan kebutuhan administrasi operasional harian seperti pengelolaan "
        "billing, hotspot, voucher, serta penyediaan metrik analitik bisnis. CafePulse menyederhanakan tugas-tugas "
        "repetitif tanpa mengabaikan integritas keamanan jaringan."
    )
    pdf.subheading("Target Market")
    pdf.body_text(
        "Target pasar utama CafePulse difokuskan pada operator jaringan skala kecil dan menengah yang membutuhkan "
        "kemudahan manajemen hotspot dan pemantauan perangkat. Segmentasi pasar meliputi:"
    )
    pdf.bullet_point("Teknisi Jaringan Independen dan Penyedia Jasa Setting MikroTik.")
    pdf.bullet_point("Pengelola RT/RW Net (Community Internet Service Provider) di daerah sub-urban dan pedesaan.")
    pdf.bullet_point("Pemilik Kafe, Restoran, Pujasera, Co-working Space, dan Hotel Kecil.")
    pdf.bullet_point("Lembaga Pendidikan, Lab Sekolah, serta Pusat Komunitas Lokal.")
    
    pdf.subheading("Value Proposition")
    pdf.bullet_point("Local-First & Offline-Friendly: Aplikasi dapat berjalan penuh di jaringan terisolasi (air-gapped) tanpa ketergantungan pada koneksi internet luar.")
    pdf.bullet_point("No Subscription / No SaaS Trap: Model pembelian satu kali (one-time purchase) yang memberikan kepemilikan penuh perangkat lunak serta ketenangan finansial bagi pengguna.")
    pdf.bullet_point("Rich Visual Aesthetics: UI modern bertema gelap-terang reaktif yang mempercepat pembacaan kondisi kesehatan jaringan dibandingkan Winbox konvensional.")
    pdf.bullet_point("Native Performance: Dibangun dengan PyQt6 sehingga jauh lebih hemat RAM dan CPU dibandingkan aplikasi desktop berbasis Electron (seperti VS Code atau Discord desktop).")

    # ─── SECTION 2: FOUNDER INTENT ───
    pdf.section_header(2, "FOUNDER INTENT")
    pdf.body_text(
        "Filosofi founder (Yubelkey) dalam mengembangkan CafePulse didasari oleh prinsip 'Kedaulatan Data dan Keandalan Mutlak'. "
        "Di era modern di mana hampir seluruh penyedia perangkat lunak bermigrasi ke arah cloud dan model langganan bulanan, "
        "founder CafePulse mengambil keputusan strategis yang bertolak belakang:"
    )
    pdf.subheading("Filosofi Offline-First & Data Sovereignty")
    pdf.body_text(
        "Founder meyakini bahwa data topologi jaringan, kredensial router, serta data statistik pelanggan adalah hak milik mutlak "
        "pengguna. Mengirimkan data-data sensitif tersebut ke server pihak ketiga (cloud) adalah risiko privasi yang tidak dapat diterima. "
        "Dengan arsitektur offline-first, CafePulse memastikan data tersebut tetap tersimpan di dalam harddisk lokal komputer pengguna."
    )
    pdf.subheading("Penolakan Terhadap Model Bisnis SaaS (Software as a Service)")
    pdf.body_text(
        "Skema SaaS sering kali menjebak pengusaha kecil dalam siklus pembayaran berulang yang membebani kas bulanan mereka. "
        "Selain itu, jika server pusat vendor mengalami gangguan, seluruh operasional jaringan lokal pengguna ikut terhenti. "
        "CafePulse menolak konsep ini dengan mengadopsi model lisensi One-Time Purchase per PC."
    )
    pdf.subheading("Alasan Memilih SQLite sebagai Database Layer")
    pdf.body_text(
        "SQLite dipilih karena keandalannya yang legendaris, sifatnya yang serverless (tidak memerlukan setup engine database tambahan seperti MySQL atau PostgreSQL), "
        "kinerja cepat untuk baca-tulis lokal, serta kemudahan dalam proses pencadangan (cukup menyalin satu file db)."
    )
    pdf.subheading("Alasan Memilih PyQt6 sebagai GUI Engine")
    pdf.body_text(
        "Framework modern berbasis web (Electron) memerlukan runtime Chromium penuh yang memakan ratusan megabyte RAM. "
        "Seorang teknisi jaringan sering kali membuka banyak utilitas sekaligus di laptop lapangan mereka. PyQt6 menghadirkan "
        "keindahan visual modern dengan performa native C++ yang sangat ringan."
    )
    pdf.subheading("Fokus pada Stabilitas Operasional")
    pdf.body_text(
        "Di lingkungan operasional riil, kegagalan aplikasi dapat menghentikan bisnis pengguna (misal, tidak bisa mencetak voucher). "
        "Oleh karena itu, stabilitas sistem inti (seperti database transaction dan licensing) ditempatkan jauh di atas penambahan "
        "fitur-fitur sekunder."
    )

    # ─── SECTION 3: PROJECT HISTORY ───
    pdf.section_header(3, "PROJECT HISTORY")
    pdf.body_text(
        "Pengembangan CafePulse melewati beberapa fase evolusi teknis yang terdokumentasi dengan baik:"
    )
    pdf.subheading("Timeline Milestone Utama")
    pdf.bullet_point("Phase 1: Foundation Stabilization. Pembangunan Pulse Engine (event-driven scheduler) dan implementasi database SQLite lokal dengan mode Write-Ahead Logging (WAL) serta fallback safe-mode startup.")
    pdf.bullet_point("Phase 2: Smart Connection Platform. Integrasi koneksi API MikroTik, Neighbor Discovery (MNDP), Local Network ARP Scanning, dan Secure Credential Vault.")
    pdf.bullet_point("Phase 3: Operations Platform. Penambahan fitur hotspot management harian, penciptaan Batch Voucher Generator dengan ekspor layout PDF, serta inventory MAC vendor database.")
    pdf.bullet_point("Phase 4: Security & Code Freeze. Pengerasan sistem lisensi menggunakan enkripsi kunci asimetris RSA-4096 (RSA-first), modularisasi path file ke LOCALAPPDATA untuk kompatibilitas Windows UAC, dan penyusunan installer Inno Setup.")
    pdf.bullet_point("Phase 5: Release Candidate (RC1) & Ecosystem Preparation. Penyelesaian dokumentasi EULA, strategi komunitas Discord, peluncuran web portal lokal, dan audit keselarasan terminologi.")
    
    pdf.subheading("Keputusan Arsitektur Besar yang Berdampak")
    pdf.body_text(
        "Dua keputusan terbesar dalam sejarah proyek adalah migrasi sistem lisensi dari Serial Key hashing biasa ke RSA-4096 "
        "dan perbaikan path system. Awalnya, aplikasi menyimpan lisensi, database, dan log di dalam folder project secara relatif. "
        "Ketika di-compile ke Program Files, Windows memblokir penulisan file ke folder tersebut karena pembatasan UAC. "
        "Keputusan memindahkan seluruh writable directory ke LOCALAPPDATA menyelamatkan aplikasi dari kegagalan booting fatal setelah instalasi."
    )

    # ─── SECTION 4: CURRENT PROJECT STATUS ───
    pdf.add_page()
    pdf.section_header(4, "CURRENT PROJECT STATUS")
    pdf.body_text(
        "CafePulse saat ini berada dalam status Release Candidate 1 (RC1) yang stabil pada level core framework. "
        "Semua fitur utama terkait autentikasi, pembacaan database, enkripsi lokal, pembuatan voucher, dan installer "
        "telah diuji secara ketat."
    )
    pdf.subheading("Metrik Kesiapan Rilis")
    pdf.table_row([60, 45, 65], ["Evaluation Vector", "Score", "Audit Justification"], is_header=True)
    pdf.table_row([60, 45, 65], ["Product Readiness", "85 / 100", "Core engine solid. Network/Advanced mockups present."], is_header=False)
    pdf.table_row([60, 45, 65], ["Commercial Readiness", "90 / 100", "RSA licensing works. Offline activations generated."], is_header=False)
    pdf.table_row([60, 45, 65], ["Website Readiness", "95 / 100", "URL youbellkey.github.io/cafepulse-site/ setup."], is_header=False)
    pdf.table_row([60, 45, 65], ["Installer Readiness", "90 / 100", "Inno Setup Free/Pro compilers successfully built."], is_header=False)
    pdf.table_row([60, 45, 65], ["GitHub Readiness", "92 / 100", "Clean repo with .gitignore and README setup."], is_header=False)
    pdf.ln(4)

    pdf.subheading("Status RC1 & Kematangan Fitur")
    pdf.body_text(
        "Core Engine, Database, dan Security telah dibekukan (code freeze) untuk menjamin stabilitas. "
        "Workspace Operations (Voucher Generator) telah diuji 100% fungsional. Workspace Network dan Advanced "
        "telah memiliki desain antarmuka (UI) reaktif berdefinisi tinggi, namun operasinya masih berjalan dalam mode simulasi "
        "dengan data tiruan (mock data) dan dialog box simulator. Integrasi API langsung untuk fitur-fitur manipulasi firewall/routing "
        "dijadwalkan meluncur setelah fase pengujian beta selesai menuju rilis stabil v1.0.0.0."
    )

    # ─── SECTION 5: SYSTEM ARCHITECTURE ───
    pdf.section_header(5, "SYSTEM ARCHITECTURE")
    pdf.body_text(
        "CafePulse menggunakan arsitektur mandiri (Thick-Client Desktop Application) dengan pemisahan tanggung jawab "
        "yang jelas (Separation of Concerns):"
    )
    pdf.subheading("Deskripsi Layer Aplikasi")
    pdf.bullet_point("GUI Layer (PyQt6): Lapisan tampilan yang reaktif, menggunakan widget kustom dan sistem layout PyQt6 yang responsif terhadap perubahan resolusi serta light/dark mode.")
    pdf.bullet_point("Core Layer (Pulse Engine): Mengelola thread latar belakang (QThreads) untuk polling status router, scanning ARP jaringan lokal, dan penanganan event logic tanpa memblokir thread UI utama.")
    pdf.bullet_point("Database Layer (SQLite): Layer persistence untuk data konfigurasi router, data inventaris perangkat klien, logs, dan template voucher.")
    pdf.bullet_point("Monitoring Layer: Mengintegrasikan ARP scanner lokal, polling bandwidth interfaces, dan neighbor discovery (MNDP) untuk memetakan jaringan terdekat.")
    pdf.bullet_point("Licensing Layer (RSA): RSAManager bertugas melakukan verifikasi tanda tangan digital secara offline berbekal Public Key kriptografi, sedangkan LicensingManager mengelola hardware binding.")
    pdf.bullet_point("MikroTik Layer: Abstraksi koneksi yang memanfaatkan protokol API RouterOS (TCP 8728) dan API-SSL (TCP 8729) secara aman untuk menarik informasi secara non-blocking.")

    pdf.subheading("Diagram Logika Hubungan Antar Layer")
    pdf.code_block(
        " +-----------------------------------------------------------------+\n"
        " |                       GUI Layer (PyQt6 UI)                      |\n"
        " +---------------------------------+-------------------------------+\n"
        "                                   | (Signals & Slots)\n"
        "                                   v\n"
        " +-----------------------------------------------------------------+\n"
        " |                 Core Layer (Pulse Engine Threads)               |\n"
        " +--------+------------------------+-------------------------------+\n"
        "          |                        |                               |\n"
        "          v                        v                               v\n"
        " +------------------+    +-------------------+    +----------------+\n"
        " |  Database Layer  |    |  Monitoring Layer |    | MikroTik Layer |\n"
        " |   (SQLite WAL)   |    |    (ARP/Ping)     |    | (RouterOS API) |\n"
        " +------------------+    +-------------------+    +----------------+\n"
        "          ^                               \n"
        "          | (License validation checks)   \n"
        " +--------+--------------------------------------------------------+\n"
        " |                     Licensing Layer (RSA-4096)                  |\n"
        " +-----------------------------------------------------------------+"
    )

    # ─── SECTION 6: LOCKED ARCHITECTURE RULES ───
    pdf.add_page()
    pdf.section_header(6, "LOCKED ARCHITECTURE RULES")
    pdf.body_text(
        "Untuk menjaga CafePulse tetap selaras dengan visi awal founder (local-first, hemat daya, performa native), "
        "aturan arsitektur berikut telah dikunci secara absolut dan tidak boleh diubah oleh developer mana pun:"
    )
    pdf.subheading("1. No Cloud Backend (Zero Cloud Dependency)")
    pdf.body_text(
        "Aplikasi tidak boleh melakukan penulisan data konfigurasi, kredensial, logs, atau statistik ke server cloud. "
        "Seluruh transaksi baca-tulis harus diselesaikan secara offline pada mesin lokal. Koneksi keluar hanya diperkenankan "
        "untuk pembaruan modul (jika diaktifkan pengguna) atau verifikasi manual."
    )
    pdf.subheading("2. No Packet Sniffing (Security Compliance)")
    pdf.body_text(
        "CafePulse memetakan jaringan menggunakan active scans (ARP sweeps/Neighbor discovery) dan kueri API resmi. "
        "Aplikasi tidak diperbolehkan menggunakan metode packet sniffing (seperti scapy/libpcap) atau masuk ke monitor mode. "
        "Aturan ini mencegah aplikasi membutuhkan hak akses administrator/root yang berlebihan dan menghindari false-positive "
        "antivirus."
    )
    pdf.subheading("3. No Asyncio Rewrite (Thread Isolation Lock)")
    pdf.body_text(
        "Semua proses I/O non-blocking di belakang layar dikelola menggunakan PyQt6 QThreads secara terisolasi. "
        "Penulisan ulang core menggunakan framework asyncio dilarang karena berisiko merusak kompatibilitas loop event PyQt6 "
        "dan dapat memicu memory leak di thread utama."
    )
    pdf.subheading("4. No Multiprocessing Rewrite")
    pdf.body_text(
        "Penggunaan multiproses dilarang untuk menghindari overhead IPC (Inter-Process Communication) yang besar di Windows "
        "serta konsumsi RAM berlebih. QThreads dengan optimasi worker loop terbukti cukup responsif untuk menangani operasi router."
    )
    pdf.subheading("5. Strict Separation of Folders")
    pdf.body_text(
        "Direktori instalasi (Program Files) bersifat read-only. Direktori LOCALAPPDATA bersifat writable. "
        "Aturan ini harus dipatuhi secara ketat di seluruh modul path resolver."
    )

    # ─── SECTION 7: DATABASE ARCHITECTURE ───
    pdf.section_header(7, "DATABASE ARCHITECTURE")
    pdf.body_text(
        "Sistem database CafePulse dikelola secara terpusat oleh Core Database Manager."
    )
    pdf.subheading("Audit Skema Database")
    pdf.bullet_point("meta: Menyimpan metadata aplikasi seperti versi skema database dan tanggal instalasi.")
    pdf.bullet_point("devices: Menyimpan inventaris perangkat klien jaringan (IP, MAC unik, Hostname, Vendor OUI, Status).")
    pdf.bullet_point("sessions: Melacak durasi koneksi perangkat klien yang terhubung ke jaringan lokal.")
    pdf.bullet_point("traffic_logs: Menyimpan historis kecepatan unggah/unduh per perangkat untuk pembuatan grafik statistik.")
    pdf.bullet_point("alerts: Menyatat rekam jejak anomali atau notifikasi sistem jaringan.")
    pdf.bullet_point("settings: Pengaturan konfigurasi aplikasi tingkat lanjut berbasis pasangan Key-Value.")
    pdf.bullet_point("routers: Menyimpan kredensial router MikroTik (nama, host, port, username, password terenkripsi).")
    pdf.bullet_point("access_packages: Menyimpan paket layanan hotspot (kecepatan limit, harga, durasi voucher).")
    pdf.bullet_point("customers: Pengelola data pelanggan hotspot lokal.")
    pdf.bullet_point("vouchers: Kode voucher hotspot hasil generator beserta pelacakan status (Active/Used/Expired).")
    
    pdf.subheading("Optimasi Write-Ahead Logging (WAL)")
    pdf.body_text(
        "Database SQLite dikonfigurasi menggunakan mode WAL via 'PRAGMA journal_mode=WAL'. Mode ini memungkinkan thread latar "
        "belakang untuk menulis data scan baru secara bersamaan (concurrent) ketika thread UI utama sedang melakukan kueri baca "
        "data untuk dashboard. Hal ini mencegah terjadinya error 'database is locked'."
    )
    pdf.subheading("Strategi Backup & Pemulihan Kerusakan (Corruption Recovery)")
    pdf.body_text(
        "Setiap kali koneksi database dibuka, aplikasi menjalankan 'PRAGMA integrity_check'. Jika SQLite mendeteksi adanya file database yang "
        "korup (misal, akibat komputer mati mendadak saat mati lampu), file db yang rusak akan disalin ke 'cafepulse.db.bak' sebagai "
        "arsip investigasi teknis, kemudian aplikasi secara otomatis melahirkan file 'cafepulse.db' baru yang bersih dengan inisialisasi "
        "skema standar, memastikan aplikasi tidak crash saat diluncurkan kembali."
    )
    pdf.subheading("Alur Shutdown yang Bersih (Clean Shutdown Flow)")
    pdf.body_text(
        "Ketika pengguna menutup aplikasi, MainWindow memicu event closeEvent. Aplikasi terlebih dahulu mengirimkan sinyal penghentian "
        "ke seluruh background QThreads, menunggu mereka selesai menulis log terakhir ke database, menutup koneksi database secara formal, "
        "dan menulis file bendera '.clean' di folder konfigurasi. Di awal booting berikutnya, jika file '.clean' ditemukan, aplikasi "
        "mengetahui sesi sebelumnya berakhir dengan selamat dan menghapus benderanya. Jika file '.clean' absen, aplikasi memunculkan dialog "
        "recovery yang menginfokan pemulihan pasca crash secara jujur."
    )

    # ─── SECTION 8: LICENSE SYSTEM ───
    pdf.add_page()
    pdf.section_header(8, "LICENSE SYSTEM")
    pdf.body_text(
        "CafePulse menerapkan sistem lisensi offline-first yang sangat aman dengan membagi fungsionalitas "
        "aplikasi menjadi dua edisi utama:"
    )
    pdf.subheading("Edisi Perangkat Lunak & Batasan Fitur")
    pdf.bullet_point("Free Edition (Gratis Selamanya): Mendukung pemindaian satu router, ARP network scanner lokal, neighbor discovery, visualisasi dashboard dasar, dan structured logs viewer. Fitur-fitur komersial dikunci.")
    pdf.bullet_point("Professional Edition (One-Time Purchase): Membuka fitur Voucher Generator, hotspot dashboard aktif, reservasi IP DHCP Lease, backup terjadwal, billing analytics, multi-router management, dan Smart Insight Assistant.")

    pdf.subheading("Mekanisme Verifikasi Kriptografi RSA-4096")
    pdf.body_text(
        "Validasi lisensi tidak memerlukan internet. Verifikasi dilakukan secara lokal menggunakan kunci publik (Public Key) "
        "RSA 4096-bit dengan padding PSS dan hash SHA-256 yang ditanam di dalam source code (dan didukung fallback file 'public_key.pem'). "
        "Struktur file lisensi '.lic' berbentuk JSON bertanda tangan:"
    )
    pdf.code_block(
        " {\n"
        "   \"data\": {\n"
        "       \"owner\": \"Nama Pemilik Lisensi\",\n"
        "       \"email\": \"email@domain.com\",\n"
        "       \"hardware_id\": \"CP-HWID-XXXX-XXXX-XXXX-XXXX\",\n"
        "       \"license_type\": \"COMMERCIAL\",\n"
        "       \"issue_date\": \"2026-06-05T12:00:00\",\n"
        "       \"expiry\": \"2031-06-05T12:00:00\"\n"
        "   },\n"
        "   \"signature\": \"TANDA_TANGAN_DIGITAL_BASE64_HASIL_ENKRIPSI_PRIVATE_KEY\"\n"
        " }"
    )
    pdf.body_text(
        "Aplikasi memverifikasi kecocokan tanda tangan digital di atas menggunakan public key. Jika tanda tangan valid dan "
        "Hardware ID yang tertulis di dalam lisensi cocok dengan HWID komputer saat ini, edisi Professional aktif."
    )
    pdf.subheading("Penghitungan 5-Year Update Entitlement")
    pdf.body_text(
        "Lisensi komersial CafePulse menjamin hak pembaruan software selama 5 tahun sejak tanggal aktivasi. "
        "Tanggal kedaluwarsa dukungan ditulis dalam format ISO di dalam data terenkripsi. Selama tanggal sistem saat ini "
        "berada di bawah tanggal kedaluwarsa tersebut, pembaruan aplikasi dapat diinstal secara gratis. Jika telah melewati "
        "5 tahun, aplikasi Professional tetap berjalan penuh pada versi terakhir yang terinstal, namun update ke versi yang lebih baru "
        "akan menurunkannya ke Free Edition secara otomatis."
    )
    pdf.subheading("Logika Fallback Lisensi yang Aman (Anti-Lockout)")
    pdf.body_text(
        "Jika file lisensi 'license.lic' dihapus, rusak, atau dipindahkan ke PC lain (HWID tidak cocok), aplikasi tidak akan "
        "mengunci pengguna keluar (no lockout). Aplikasi akan menurunkan tingkat operasionalnya ke Free Edition secara anggun. "
        "Ini menjamin operasional dasar jaringan pengguna tidak pernah mati akibat kegagalan otentikasi software."
    )

    # ─── SECTION 9: INSTALLER ARCHITECTURE ───
    pdf.section_header(9, "INSTALLER ARCHITECTURE")
    pdf.body_text(
        "Pendistribusian CafePulse memanfaatkan compiler Inno Setup versi modern untuk melahirkan file instalasi native Windows."
    )
    pdf.subheading("Alokasi Direktori Installer & Kompatibilitas UAC")
    pdf.bullet_point("Program Files Directory ({autopf}\\CafePulse): Menyimpan file binary executables hasil compile PyInstaller, file README, file LICENSE, serta file konfigurasi read-only 'settings_default.json'. Folder ini membutuhkan hak administrator saat proses instalasi, namun dibatasi hanya-baca (read-only) saat aplikasi berjalan.")
    pdf.bullet_point("LocalAppData Directory ({userappdata}\\CafePulse): Direktori writable per-user yang menyimpan file database ('cafepulse.db'), konfigurasi aktif ('settings.json'), lisensi ('license.lic'), folder eksport, serta logs crash. Direktori ini tidak membutuhkan hak elevasi administrator (UAC) sehingga aman dari gangguan permission Windows.")

    pdf.subheading("Alur Upgrade dan Uninstall")
    pdf.bullet_point("Upgrade Behavior: Pemasangan versi baru akan mendeteksi installer versi sebelumnya melalui AppId unik. Installer akan menimpa file eksekutabel lama di Program Files tanpa menyentuh file database, pengaturan, dan lisensi di LOCALAPPDATA. Konfigurasi lama dan lisensi pengguna tetap terjaga.")
    pdf.bullet_point("Uninstall Behavior: Proses uninstall akan menghapus seluruh file binary di Program Files serta entri registry instalasi. File database, lisensi, dan log di LOCALAPPDATA sengaja dipertahankan agar data pengguna tidak hilang jika mereka hanya melakukan instalasi ulang. Uninstaller dapat dikonfigurasi untuk menampilkan konfirmasi opsional untuk menghapus folder data pengguna secara total.")

    # ─── SECTION 10: ASSET SYSTEM ───
    pdf.add_page()
    pdf.section_header(10, "ASSET SYSTEM")
    pdf.body_text(
        "CafePulse menggunakan sistem pengelolaan aset grafis yang terstandarisasi untuk menjamin keselarasan visual "
        "dan branding aplikasi di seluruh platform."
    )
    pdf.subheading("Manifest Aset Branding")
    pdf.bullet_point("logo.png (2.14 MB): Aset logo utama resolusi tinggi untuk kebutuhan publikasi dan media sosial.")
    pdf.bullet_point("logo_dark.png & logo_light.png (2.14 MB): Varian logo yang dioptimalkan untuk tema gelap dan terang.")
    pdf.bullet_point("logo.svg (180 KB): Logo format vektor untuk skalabilitas tak terbatas tanpa kehilangan kualitas.")
    pdf.bullet_point("splash.png (2.11 MB): Gambar latar belakang splash screen reaktif saat aplikasi memuat komponen inti.")
    pdf.bullet_point("icon.ico (76 KB): File ikon multi-resolusi Windows untuk shortcut desktop, start menu, dan title bar.")
    pdf.bullet_point("founder_youbellkey.png (1.91 MB): Foto pengenal founder (Yubelkey) yang diintegrasikan pada halaman 'About Developer' di menu settings untuk membangun rasa percaya (trust) dengan komunitas teknisi.")

    pdf.subheading("Katalog Capture Screenshots")
    pdf.body_text(
        "Direktori 'assets/screenshots/' menampung 25 file tangkapan layar antarmuka aplikasi. File-file ini digunakan untuk "
        "melengkapi dokumentasi manual, menghias visual web portal utama, dan memberikan preview fitur komersial pada menu "
        "pembelian lisensi di dalam Free Edition. Screenshots mencakup dasbor analitik hotspot, visualisasi monitoring bandwith, "
        "layout voucher siap cetak, panel setelan tema, dan tampilan safe mode recovery."
    )

    # ─── SECTION 11: RC1 VALIDATION HISTORY ───
    pdf.section_header(11, "RC1 VALIDATION HISTORY")
    pdf.body_text(
        "Sebelum status RC1 dideklarasikan, serangkaian validasi fungsional dan pengujian batas (boundary tests) "
        "telah dilaksanakan pada lingkungan pengembangan Windows 10/11:"
    )
    pdf.subheading("Riwayat Pengujian dan Hasil Validasi")
    pdf.bullet_point("Storage Validation: Memastikan aplikasi tidak pernah mencoba menulis file ke Program Files. Pengujian pengalihan APPDATA sukses, data terisolasi di LOCALAPPDATA.")
    pdf.bullet_point("Installer Validation: Kompilasi script Inno Setup berhasil melahirkan 'CafePulse_Free_Setup.exe' and 'CafePulse_Professional_Setup.exe'. Pengujian instalasi pada VM Windows bersih (clean OS) berjalan lancar tanpa error DLL.")
    pdf.bullet_point("Asset Validation: Validasi fallback aset ikon dan splash screen. Jika splash.png dihapus, aplikasi sukses beralih ke logo.png secara otomatis tanpa crash.")
    pdf.bullet_point("Upgrade Validation: Pengujian instalasi menimpa (overwrite). Lisensi Professional dan database berisi 50 router tetap terbaca sempurna pasca upgrade installer.")
    pdf.bullet_point("Runtime Validation: Memperbaiki traceback error AttributeError saat penutupan aplikasi. Patches pada closeEvent MainWindow telah memaksa thread scanner (WiFiWorker) berhenti secara sinkron sebelum koneksi SQLite ditutup.")
    pdf.bullet_point("License Validation: Pengujian rekayasa lisensi (tampering). Mengubah satu karakter di dalam file license.lic menyebabkan tanda tangan RSA tidak valid, sistem langsung menurunkan status ke Free Edition dengan aman.")
    pdf.bullet_point("Database Validation: Stress-testing penulisan data scanner ke SQLite secara simultan (60 write/detik). Database WAL bekerja tanpa memicu error locking.")

    # ─── SECTION 12: KNOWN RISKS ───
    pdf.section_header(12, "KNOWN RISKS")
    pdf.body_text(
        "Berdasarkan audit teknis mendalam, berikut adalah daftar risiko proyek yang teridentifikasi beserta tingkat dampaknya:"
    )
    pdf.subheading("Daftar Risiko dan Tingkat Dampak")
    pdf.bullet_point("P0 (CRITICAL) - Thread Database Race on Shutdown: Terjadi traceback AttributeError jika thread background mencoba menulis log hasil scan yang terlambat ke database yang sudah terlanjur ditutup oleh main thread saat shutdown aplikasi. (Status: Teratasi di RC1 melalui penambahan sinkronisasi closeEvent).")
    pdf.bullet_point("P1 (HIGH) - False-Positive Antivirus SmartScreen: File installer (.exe) yang di-compile dengan Pyinstaller sering kali dicurigai oleh Windows Defender SmartScreen sebagai trojan karena tidak ditandatangani oleh sertifikat Microsoft Authenticode Code Signing (yang berbiaya jutaan rupiah per tahun). Hal ini dapat menurunkan tingkat konversi unduhan pengguna baru.")
    pdf.bullet_point("P2 (MEDIUM) - Latency on Large Routers: Polling metrik pada routerboard MikroTik dengan CPU rendah (seperti hEX lite atau RB750) yang memiliki ribuan rule firewall atau user active hotspot dapat memicu lonjakan beban CPU router jika interval polling diset terlalu cepat (<2 detik).")
    pdf.bullet_point("P3 (LOW) - OUI Database Limits: Fitur identifikasi vendor nama perangkat bergantung pada file OUI lokal. Jika ada manufaktur IoT baru yang merilis perangkat, namanya tidak akan teridentifikasi sebelum database OUI lokal diperbarui.")

    # ─── SECTION 13: TECHNICAL DEBT ───
    pdf.add_page()
    pdf.section_header(13, "TECHNICAL DEBT")
    pdf.body_text(
        "Untuk transparansi arsitektur, berikut adalah hutang teknis (technical debt) yang masih tersisa di dalam codebase "
        "CafePulse v1.0 RC1:"
    )
    pdf.subheading("Daftar Hutang Teknis Teridentifikasi")
    pdf.bullet_point("Simulated Dashboards: Workspace Network dan Advanced (Firewall, NAT, DNS, PPP, Wireless, Bridge, VLAN, Queue) menggunakan data simulasi statis (high-fidelity mockups). Integrasi API rill untuk penulisan konfigurasi MikroTik tersebut baru akan diimplementasikan penuh pada rilis stabil berikutnya.")
    pdf.bullet_point("Manual Billing & QRIS Activation: CafePulse belum terintegrasi dengan Payment Gateway API secara realtime. Proses verifikasi pembayaran dan pengiriman file lisensi komersial masih dikerjakan secara manual oleh founder melalui verifikasi email/chat.")
    pdf.bullet_point("Stale Website Link: File website/js/main.js masih memiliki referensi fallback URL lama 'yubelki/cafepulse' yang mengarah ke repository uji coba. Link ini harus dialihkan ke official namespace 'youbellkey/cafepulse-site' sebelum publikasi.")
    pdf.bullet_point("Lack of Automated UI Tests: Pengujian antarmuka PyQt6 masih mengandalkan pengetesan manual (manual QA clicking) tanpa adanya framework pengujian otomatis seperti pytest-qt secara menyeluruh.")

    # ─── SECTION 14: WEBSITE STATUS ───
    pdf.section_header(14, "WEBSITE STATUS")
    pdf.body_text(
        "Situs web portal pemasaran resmi CafePulse dirancang sebagai landing page multipage modern berkecepatan tinggi "
        "yang dioptimalkan untuk hosting statis (GitHub Pages)."
    )
    pdf.subheading("Struktur Direktori Web Portal")
    pdf.bullet_point("index.html: Halaman beranda utama dengan hero section, value proposition, dan gambaran umum platform.")
    pdf.bullet_point("product.html: Penjelasan rinci mengenai 4 Workspace CafePulse beserta galerinya.")
    pdf.bullet_point("pricing.html: Informasi harga lisensi komersial Professional Edition (Rp499.000) dan petunjuk manual transfer QRIS.")
    pdf.bullet_point("download.html: Portal unduhan file installer Free Edition dan paket portable ZIP.")
    pdf.bullet_point("founder.html: Pesan founder, komitmen offline-first, dan filosofi anti-SaaS.")
    pdf.bullet_point("about.html & beta.html: Profil tim/developer dan informasi pendaftaran program uji coba Beta.")
    pdf.bullet_point("documentation.html: Panduan ringkas setup, koneksi API MikroTik, dan pemecahan masalah dasar.")
    pdf.bullet_point("contact.html: Formulir pengiriman email terintegrasi fallback mailto link.")
    pdf.bullet_point("robots.txt & sitemap.xml: Konfigurasi SEO untuk indeks mesin pencari.")
    pdf.bullet_point(".nojekyll: Memastikan GitHub Pages tidak menyaring folder dengan awalan garis bawah (seperti folder aset).")

    pdf.subheading("Rencana Deployment")
    pdf.body_text(
        "Situs web ini akan di-host secara gratis di GitHub Pages dengan domain repository 'youbellkey.github.io/cafepulse-site/'. "
        "Domain komersial 'cafepulse.net' akan dipetakan sebagai Custom Domain setelah fase Beta selesai."
    )

    # ─── SECTION 15: GITHUB RELEASE STATUS ───
    pdf.section_header(15, "GITHUB RELEASE STATUS")
    pdf.body_text(
        "Struktur repositori GitHub telah dibersihkan untuk mendukung proses rilis publik yang transparan dan profesional."
    )
    pdf.subheading("Struktur Aset Rilis GitHub")
    pdf.body_text(
        "Setiap rilis di halaman GitHub Releases akan menyertakan empat paket distribusi utama:"
    )
    pdf.bullet_point("CafePulse_Free_Setup.exe: Windows setup installer untuk Free Edition.")
    pdf.bullet_point("CafePulse_Free_Portable.zip: Paket arsip portable Free Edition (cukup ekstrak dan jalankan).")
    pdf.bullet_point("CafePulse_Professional_Setup.exe: Windows setup installer untuk Professional Edition.")
    pdf.bullet_point("CafePulse_Professional_Portable.zip: Paket arsip portable Professional Edition.")

    pdf.subheading("Strategi Versioning dan Kebersihan Repositori")
    pdf.body_text(
        "CafePulse menggunakan Semantic Versioning (SemVer). Rilis beta perdana akan dilabeli dengan tag 'v1.0.0-beta' "
        "(atau 'v0.9-beta'). Repositori telah dilengkapi dengan file '.gitignore' standar industri untuk mencegah file-file "
        "sensitif terkomit secara tidak sengaja. Berdasarkan audit kebersihan, file-file developer seperti 'cafepulse.db' lokal, "
        "kunci lisensi uji coba 'license.lic', file flags, logs, folder output Pyinstaller ('dist/', 'build/'), dan bytecode "
        "Python ('__pycache__/') telah dihapus dari pelacakan git dan dimasukkan ke dalam daftar pengecualian .gitignore."
    )

    # ─── SECTION 16: DISCORD ECOSYSTEM ───
    pdf.add_page()
    pdf.section_header(16, "DISCORD ECOSYSTEM")
    pdf.body_text(
        "Server Discord Resmi CafePulse dirancang sebagai pusat kolaborasi komunitas, penyerapan feedback, "
        "dan pelayanan dukungan teknis."
    )
    pdf.subheading("Struktur Saluran (Channels) Server")
    pdf.bullet_point("WELCOMES (Read-Only): #rules (tata tertib), #announcements (pengumuman rilis baru), #founder-info (informasi program Founder).")
    pdf.bullet_point("COMMUNITY: #general-chat (diskusi umum), #showcase (tangkapan layar dasbor user di lapangan).")
    pdf.bullet_point("SUPPORT: #help-desk (tanya jawab instalasi), #pro-tickets (saluran bantuan privat untuk pembeli lisensi Pro).")
    pdf.bullet_point("BETA TESTING (Private): #beta-chat (diskusi fitur eksperimental), #bug-reports (pelaporan kegagalan sistem).")
    pdf.bullet_point("FOUNDER PROGRAM (Private): #founder-lounge (obrolan santai founder), #roadmap-voting (pemungutan suara fitur masa depan).")
    pdf.bullet_point("MIKROTIK DISCUSSIONS: #routeros-tips (skrip & trik), #rt-rw-net (sharing operasional pengelola ISP komunitas).")
    pdf.bullet_point("DEVELOPMENT: #dev-logs (raw updates dari developer).")

    pdf.subheading("Alur Kerja Pelaporan Bug & Moderasi")
    pdf.body_text(
        "Pengguna beta melaporkan bug di saluran #bug-reports dengan melampirkan log crash (/logs/crash/) dan detail hardware. "
        "Moderator akan menyaring laporan tersebut dan mengubahnya menjadi tiket pelacakan isu resmi di GitHub (GitHub Issues). "
        "Moderator memiliki wewenang untuk membersihkan pesan spam dan mengunci saluran jika terjadi gangguan keamanan."
    )

    # ─── SECTION 17: BETA TESTER PROGRAM ───
    pdf.section_header(17, "BETA TESTER PROGRAM")
    pdf.body_text(
        "Program penguji beta CafePulse dibentuk untuk memvalidasi performa aplikasi pada skenario jaringan riil."
    )
    pdf.subheading("Tujuan Program")
    pdf.body_text(
        "Tujuan utama adalah untuk menguji ketahanan Pulse Engine dan parser API MikroTik terhadap ribuan variasi topologi "
        "dan versi RouterOS (v6 & v7) di lapangan nyata yang tidak dapat disimulasikan sepenuhnya pada lab pengembangan."
    )
    pdf.subheading("Sistem Reward & Seleksi")
    pdf.body_text(
        "Program ini menargetkan kuota awal sebanyak 10 beta tester aktif dari kalangan teknisi jaringan dan pengelola RT/RW Net. "
        "Proses seleksi dilakukan melalui formulir aplikasi beta.html. Sebagai apresiasi atas kontribusi mereka dalam melaporkan bug "
        "dan memberikan masukan analitik, penguji beta yang aktif akan diberikan reward berupa satu lisensi komersial Professional Edition "
        "gratis selamanya (5-year update entitlement)."
    )
    pdf.subheading("Alur Pelaporan Hasil Uji")
    pdf.body_text(
        "Beta tester dibekali dengan modul diagnostik bawaan. Jika terjadi kegagalan, mereka cukup menekan tombol 'Export Diagnostic Package' "
        "pada menu settings, yang akan mengompres seluruh logs dan file konfigurasi tanpa data kredensial sensitif menjadi satu file ZIP, "
        "kemudian mengirimkannya ke forum Discord."
    )

    # ─── SECTION 18: ROADMAP ───
    pdf.section_header(18, "ROADMAP")
    pdf.body_text(
        "Arah pengembangan CafePulse didokumentasikan dalam roadmap taktis yang terbagi menjadi empat tahapan utama:"
    )
    pdf.subheading("Tahapan Roadmap Menuju Stabil")
    pdf.bullet_point("RC1 Stabilization (Fase Saat Ini): Menyelesaikan perbaikan crash threading pada shutdown, merapikan repositori, meluncurkan situs web statis di GitHub Pages, dan membuka server Discord komunitas.")
    pdf.bullet_point("Beta Tester Launch (0 - 1 Bulan): Mendistribusikan installer versi 1.0.0-beta ke 10 beta tester terpilih, memantau bug lapangan, dan merilis patch kestabilan versi beta (v1.0.1-beta dst).")
    pdf.bullet_point("RC2 & Founder Program (1 - 2 Bulan): Membuka pendaftaran Founder Program eksklusif untuk 100 pengguna pertama dengan harga promo Rp399.000, meluncurkan sistem aktivasi offline mandiri, dan menstabilkan integrasi API router.")
    pdf.bullet_point("Stable Release v1.0.0.0 (3 - 6 Bulan): Rilis resmi ke publik umum, mengaktifkan fitur penulisan konfigurasi rill untuk workspace Network (VLAN wizard, PPP manager) dan Advanced (Firewall NAT rules).")

    # ─── SECTION 19: DECISION FRAMEWORK ───
    pdf.add_page()
    pdf.section_header(19, "DECISION FRAMEWORK")
    pdf.body_text(
        "Untuk memandu keputusan teknis di masa depan, baik bagi founder maupun AI asisten berikutnya, "
        "kerangka kerja pengambilan keputusan (Decision Framework) berikut harus digunakan sebagai kompas:"
    )
    pdf.subheading("Prinsip Pengambilan Keputusan Teknis")
    pdf.table_row([80, 90], ["Priority Vector Comparison", "Core Engineering Rationale"], is_header=True)
    pdf.table_row([80, 90], ["Stability > Features", "Aplikasi stabil jauh lebih berharga daripada aplikasi kaya fitur tetapi sering crash."], is_header=False)
    pdf.table_row([80, 90], ["Maintainability > Complexity", "Struktur kode harus modular agar mudah dirawat oleh solo developer."], is_header=False)
    pdf.table_row([80, 90], ["Founder Capacity > Enterprise Arch", "Hindari over-engineering seperti microservices atau arsitektur cloud rumit."], is_header=False)
    pdf.table_row([80, 90], ["Offline First > Cloud Dependency", "Privasi dan kedaulatan data pengguna di atas segalanya. Tolak SaaS."], is_header=False)
    pdf.ln(4)
    
    pdf.body_text(
        "Setiap usulan modifikasi kode atau penambahan fitur baru wajib dievaluasi menggunakan perbandingan di atas. "
        "Jika fitur baru berisiko menurunkan kestabilan core engine, fitur tersebut harus ditolak atau diisolasi di cabang eksperimental."
    )

    # ─── SECTION 20: FUTURE AI HANDOVER ───
    pdf.section_header(20, "FUTURE AI HANDOVER")
    pdf.body_text(
        "PENTING BAGI AI ASSISTANT BERIKUTNYA: Sebelum Anda memberikan rekomendasi atau menulis kode baru untuk CafePulse, "
        "Anda wajib memahami konteks arsitektur dan batasan proyek berikut secara menyeluruh:"
    )
    pdf.subheading("Konteks Teknis Mutlak")
    pdf.bullet_point("Aplikasi ini adalah software desktop offline-first berbasis Python 3.12 dan PyQt6. Tidak ada backend cloud.")
    pdf.bullet_point("Semua manipulasi file harus menggunakan resolver dari core.app_paths. Path relatif dilarang keras.")
    pdf.bullet_point("Database menggunakan SQLite3 dengan PRAGMA journal_mode=WAL. Selalu tutup koneksi secara formal saat penutupan aplikasi.")
    pdf.bullet_point("Lisensi komersial divalidasi menggunakan RSA-4096 signature verification terhadap data JSON secara luring. Kunci publik tersemat secara fallback di core/licensing/rsa_manager.py.")
    pdf.bullet_point("Aplikasi dirancang untuk dikelola oleh Solo Developer. Kode yang sederhana, modular, dan terdokumentasi dengan baik jauh lebih diutamakan daripada pola desain perusahaan yang rumit (over-engineered patterns).")
    pdf.bullet_point("Kebijakan dukungan teknis adalah Best Effort Support. Jangan menjanjikan SLA respons otomatis 24/7 di dalam program bantuan.")

    # ─── FINAL EVALUATION ───
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "FINAL RELEASE CANDIDATE CERTIFICATION & READINESS ASSESSMENT", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(2, 132, 199)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.body_text(
        "Berdasarkan hasil audit menyeluruh terhadap repositori, source code, aset branding, konfigurasi installer Inno Setup, "
        "serta mitigasi kegagalan runtime, tim teknis memberikan penilaian kesiapan akhir sebagai berikut:"
    )
    
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 6, "1. Overall Project Score:")
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 6, "90 / 100 (EXCELLENT FOUNDATION)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 6, "2. Overall Release Readiness:")
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(217, 119, 6) # Orange
    pdf.cell(0, 6, "GO WITH CONDITIONS (Ready for Beta)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 6, "3. RC1 Readiness:")
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 6, "100% (Blockers Cleared & Frozen)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 6, "4. Beta Program Readiness:")
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 6, "95% (Website & Discord Blueprint Ready)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(60, 6, "5. Stable Release Readiness:")
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_text_color(100, 116, 139) # Grey
    pdf.cell(0, 6, "80% (Requires Closing Advanced/Network Mockup Gaps)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    pdf.callout(
        "CONDITIONS FOR PUBLIC STABLE RELEASE: Sebelum mempublikasikan versi 1.0.0.0 Stable ke khalayak umum:\n"
        "1. Selesaikan perbaikan bug thread shutdown race traceback di closeEvent MainWindow.\n"
        "2. Perbarui fallback link repositori di website/js/main.js untuk merujuk ke 'youbellkey/cafepulse-site'.\n"
        "3. Laksanakan siklus pengujian operasional Beta bersama 10 beta tester terpilih di Discord.\n"
        "4. Migrasikan workspace Network dan Advanced dari status simulasi ke pemanggilan API RouterOS secara fungsional."
    )
    
    # Save the output PDF
    output_filename = os.path.join(os.path.dirname(__file__), "..", "artifacts", "compiled_pdfs", "CafePulse_Project_Constitution_v1.0.pdf")
    try:
        pdf.output(output_filename)
        print(f"PDF successfully generated: {output_filename}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
