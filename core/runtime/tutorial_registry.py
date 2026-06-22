"""
CafePulse — Contextual Tutorial Registry
Daftar konten panduan kontekstual sekali-tayang untuk menu-menu utama CafePulse.
"""

TUTORIALS = {
    "dashboard": {
        "title": "Dashboard Utama",
        "description": "Di sini Anda dapat melihat jumlah <b>Perangkat Aktif</b>, statistik <b>Upload/Download</b>, serta status <b>Kesehatan Jaringan</b> secara real-time.<br><br><i>Gunakan tombol di pojok kanan atas untuk memicu pemindaian manual.</i>"
    },
    "analytics": {
        "title": "Analisis Bandwidth",
        "description": "Tab ini menyajikan grafik tren penggunaan data historis. CafePulse merekam fluktuasi bandwidth secara offline-first untuk membantu mendeteksi jam-jam sibuk café Anda secara akurat."
    },
    "modes": {
        "title": "Pemilihan Mode Operasional",
        "description": "Pilih skenario operasional CafePulse Anda:<br>"
                       "• <b>Demo Mode</b>: Simulasi data café.<br>"
                       "• <b>Home WiFi</b>: Pemindaian mandiri lokal.<br>"
                       "• <b>Hotspot</b>: Deteksi pelanggan hotspot.<br>"
                       "• <b>MikroTik</b>: Integrasi RouterOS langsung."
    },
    "devices": {
        "title": "Daftar Perangkat",
        "description": "Melacak semua perangkat yang terhubung ke jaringan café Anda lengkap dengan MAC Address, IP Address, Nama Vendor, dan status aktif secara detail."
    },
    "alerts": {
        "title": "Pusat Peringatan & Keamanan",
        "description": "Semua anomali jaringan, perangkat asing tak dikenal, atau putusnya koneksi router akan tercatat di sini dengan detail dan tingkat prioritas keamanan."
    },
    "mikrotik_detail": {
        "title": "Koneksi RouterOS MikroTik",
        "description": "Anda sedang berada di panel MikroTik Mode. Hubungkan CafePulse langsung ke API router (port 8728) untuk mengambil DHCP Leases riil dan mengukur lalu lintas interface router secara akurat."
    },
    "settings": {
        "title": "Pengaturan Sistem",
        "description": "Di menu ini Anda dapat memodifikasi preferensi visual, konfigurasi database, tingkat kepatuhan log, serta melakukan <b>Reset Panduan & Tutorial</b> kapan pun dibutuhkan."
    },
    "about": {
        "title": "Mengenai CafePulse",
        "description": "CafePulse didesain sebagai solusi monitoring jaringan mandiri yang hemat daya, offline-first, dan tangguh untuk pemilik café modern."
    }
}
