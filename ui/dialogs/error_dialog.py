"""
CafePulse — Smart Error Dialog
A custom PyQt dialog that presents unhandled errors or worker errors
in a user-friendly way, suggesting actionable solutions instead of
showing raw stack traces.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class SmartErrorDialog(QDialog):
    def __init__(self, title: str, message: str, exception_type: str = "", traceback_text: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("CafePulse — Terjadi Kesalahan")
        self.resize(620, 420)
        self.setStyleSheet("background:#0F1117; color:#E2E8F0; font-family:'Segoe UI',sans-serif;")
        
        self.title = title
        self.message = message
        self.exception_type = exception_type
        self.traceback_text = traceback_text
        
        # Deteksi otomatis perintah perbaikan dependensi jika hilang
        self.cmd_to_copy = None
        exc_str = (self.exception_type + " " + self.message).lower()
        if "modulenotfounderror" in exc_str or "import" in exc_str:
            if "routeros_api" in exc_str or "routeros-api" in exc_str:
                self.cmd_to_copy = "pip install routeros-api==0.21.0"
                
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        icon_lbl = QLabel("⚠️")
        icon_lbl.setStyleSheet("font-size:32px;")
        
        title_lbl = QLabel(self.title)
        title_lbl.setStyleSheet("font-size:18px; font-weight:700; color:#EF4444;")
        
        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Message
        msg_lbl = QLabel(self._get_smart_suggestion())
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("font-size:14px; color:#F8FAFC; line-height:1.5;")
        layout.addWidget(msg_lbl)
        
        # Details Toggle
        self.details_btn = QPushButton("Tampilkan Detail Teknis")
        self.details_btn.setStyleSheet("color:#3B82F6; text-align:left; border:none; font-size:12px; font-weight:600; background:transparent;")
        self.details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.details_btn.clicked.connect(self._toggle_details)
        layout.addWidget(self.details_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # Traceback Box (Hidden by default)
        self.trace_box = QTextEdit()
        self.trace_box.setReadOnly(True)
        self.trace_box.setStyleSheet("background:#161B27; border:1px solid #1E2535; border-radius:6px; color:#94A3B8; font-family:Consolas,monospace; font-size:11px;")
        if self.traceback_text:
            self.trace_box.setText(f"Exception: {self.exception_type}\n\n{self.traceback_text}")
        else:
            self.trace_box.setText("Tidak ada detail teknis tambahan.")
        self.trace_box.setVisible(False)
        layout.addWidget(self.trace_box)

        # Buttons Layout
        btn_layout = QHBoxLayout()
        
        if self.cmd_to_copy:
            self.copy_btn = QPushButton("Salin Perintah Perbaikan")
            self.copy_btn.setStyleSheet(
                "background:#3B82F6; color:white; border:none; border-radius:6px; padding:8px 16px; font-weight:600;"
            )
            self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.copy_btn.clicked.connect(self._copy_command)
            btn_layout.addWidget(self.copy_btn)
            
        btn_layout.addStretch()
        
        close_btn = QPushButton("Tutup")
        close_btn.setStyleSheet("background:#1E2535; color:#F1F5F9; border:1px solid #2D3748; border-radius:6px; padding:8px 16px; font-weight:600;")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)

    def _copy_command(self):
        if self.cmd_to_copy:
            QApplication.clipboard().setText(self.cmd_to_copy)
            self.copy_btn.setText("Tersalin! ✓")
            self.copy_btn.setStyleSheet(
                "background:#10B981; color:white; border:none; border-radius:6px; padding:8px 16px; font-weight:600;"
            )
            self.copy_btn.setEnabled(False)

    def _get_smart_suggestion(self) -> str:
        """Menganalisis error secara dinamis dan menyajikan solusi bersahabat."""
        exc_str = (self.exception_type + " " + self.message).lower()
        
        # 1. Pustaka MikroTik Hilang
        if "modulenotfounderror" in exc_str and "routeros_api" in exc_str:
            return (
                "Fitur <b>MikroTik Mode</b> membutuhkan pustaka pendukung tambahan yaitu <b>routeros_api</b>.<br><br>"
                "<b>Kemungkinan Penyebab:</b><br>"
                "• Pustaka tersebut belum terinstall pada virtual environment saat ini.<br>"
                "• Aplikasi berjalan di environment baru yang belum di-setup dependensinya.<br><br>"
                "<b>Solusi:</b><br>"
                "1. Klik tombol <b>Salin Perintah Perbaikan</b> di bawah.<br>"
                "2. Buka Terminal / CMD pada sistem Anda.<br>"
                "3. Tempel (Paste) perintah tersebut dan tekan <b>Enter</b>.<br>"
                "4. Masuk kembali ke MikroTik Mode tanpa harus me-restart aplikasi."
            )
        
        # 2. Masalah Koneksi/Timeout
        elif "connectionrefused" in exc_str or "timeout" in exc_str or "routerosapi" in exc_str:
            return (
                "CafePulse gagal terhubung ke perangkat router MikroTik Anda.<br><br>"
                "<b>Kemungkinan Penyebab:</b><br>"
                "• IP Address router yang dimasukkan salah atau berada di subnet berbeda.<br>"
                "• Layanan API pada RouterOS (port 8728) belum diaktifkan.<br>"
                "• Akses diblokir oleh firewall router.<br><br>"
                "<b>Solusi:</b><br>"
                "1. Pastikan komputer Anda terhubung ke jaringan router MikroTik.<br>"
                "2. Buka Winbox -> masuk ke <b>IP -> Services</b>, lalu pastikan layanan <b>api</b> dalam kondisi aktif (port 8728).<br>"
                "3. Uji koneksi ping ke IP router melalui terminal Anda."
            )
        
        # 3. Konfigurasi Rusak
        elif "jsondecode" in exc_str:
            return (
                "File konfigurasi (settings.json) terdeteksi rusak atau tidak terbaca.<br><br>"
                "<b>Solusi:</b><br>"
                "CafePulse telah memulihkan konfigurasi sistem menggunakan nilai default bawaan pabrik."
            )
            
        # 4. Hak Akses File
        elif "permissionerror" in exc_str or "access denied" in exc_str:
            return (
                "Sistem operasi menolak izin penulisan berkas sistem.<br><br>"
                "<b>Solusi:</b><br>"
                "Jalankan aplikasi CafePulse sebagai administrator (klik kanan -> <b>Run as Administrator</b>)."
            )
            
        else:
            return (
                f"Kesalahan internal terdeteksi: <i>{self.message}</i><br><br>"
                "<b>Solusi:</b><br>"
                "Jika masalah berlanjut, mohon restart aplikasi atau hubungi founder/developer untuk analisis lebih mendalam."
            )

    def _toggle_details(self):
        visible = not self.trace_box.isVisible()
        self.trace_box.setVisible(visible)
        if visible:
            self.details_btn.setText("Sembunyikan Detail Teknis")
        else:
            self.details_btn.setText("Tampilkan Detail Teknis")

def show_smart_error(title: str, message: str, exc_type: str = "", tb_text: str = ""):
    app = QApplication.instance()
    if not app:
        return
    dlg = SmartErrorDialog(title, message, exc_type, tb_text)
    dlg.exec()
