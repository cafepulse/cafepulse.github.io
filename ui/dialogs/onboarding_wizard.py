"""
CafePulse — Onboarding Wizard Dialog
Dialog pemandu interaktif bertahap (wizard) yang elegan bertema gelap
untuk membimbing pengguna baru saat aplikasi pertama kali dijalankan.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class OnboardingWizard(QDialog):
    # Dipancarkan ketika wizard selesai dengan keputusan Demo Mode (True/False)
    onboarding_finished = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selamat Datang di CafePulse")
        self.resize(580, 420)
        
        # Style premium gelap HSL
        self.setStyleSheet("""
            QDialog {
                background-color: #0F1117;
            }
            QLabel#Title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 22px;
                font-weight: 700;
                color: #F8FAFC;
                margin-bottom: 8px;
            }
            QLabel#Desc {
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                color: #94A3B8;
                line-height: 1.6;
            }
            QLabel#FeatureItem {
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                color: #CBD5E1;
                line-height: 1.5;
            }
            QPushButton {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 600;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton#BtnNext {
                background-color: #3B82F6;
                color: white;
                border: none;
            }
            QPushButton#BtnNext:hover {
                background-color: #2563EB;
            }
            QPushButton#BtnBack {
                background-color: #1E2535;
                color: #F1F5F9;
                border: 1px solid #2D3748;
            }
            QPushButton#BtnBack:hover {
                background-color: #2D3748;
            }
            QPushButton#BtnSkip {
                background-color: transparent;
                color: #64748B;
                border: none;
            }
            QPushButton#BtnSkip:hover {
                color: #94A3B8;
            }
            QFrame#Separator {
                background-color: #1E2535;
                min-height: 1px;
                max-height: 1px;
                border: none;
            }
        """)
        
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(16)
        
        # Stacked Widget untuk navigasi slide
        self.stack = QStackedWidget()
        self._create_slides()
        layout.addWidget(self.stack)
        
        # Separator line
        sep = QWidget()
        sep.setObjectName("Separator")
        layout.addWidget(sep)
        
        # Panel Navigasi Tombol
        nav_layout = QHBoxLayout()
        
        self.btn_skip = QPushButton("Lewati")
        self.btn_skip.setObjectName("BtnSkip")
        self.btn_skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_skip.clicked.connect(self._on_skip_clicked)
        nav_layout.addWidget(self.btn_skip)
        
        nav_layout.addStretch()
        
        self.btn_back = QPushButton("Kembali")
        self.btn_back.setObjectName("BtnBack")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.clicked.connect(self._on_back_clicked)
        self.btn_back.setVisible(False)  # Sembunyikan di slide pertama
        nav_layout.addWidget(self.btn_back)
        
        self.btn_next = QPushButton("Lanjut")
        self.btn_next.setObjectName("BtnNext")
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self._on_next_clicked)
        nav_layout.addWidget(self.btn_next)
        
        layout.addLayout(nav_layout)

    def _create_slides(self):
        # Slide 0: Selamat Datang
        slide0 = QWidget()
        s0_lay = QVBoxLayout(slide0)
        s0_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s0_lay.setSpacing(16)
        
        logo = QLabel("📡")
        logo.setStyleSheet("font-size: 54px; margin-bottom: 8px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s0_lay.addWidget(logo)
        
        title0 = QLabel("Selamat Datang di CafePulse")
        title0.setObjectName("Title")
        title0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s0_lay.addWidget(title0)
        
        desc0 = QLabel(
            "CafePulse didesain sebagai pendamping monitoring jaringan café mandiri yang "
            "tangguh, ringan, dan offline-first. Aplikasi ini memantau bandwidth "
            "secara real-time serta mendeteksi semua perangkat aktif yang terhubung."
        )
        desc0.setObjectName("Desc")
        desc0.setWordWrap(True)
        desc0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s0_lay.addWidget(desc0)
        self.stack.addWidget(slide0)
        
        # Slide 1: Mode Operasional
        slide1 = QWidget()
        s1_lay = QVBoxLayout(slide1)
        s1_lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        s1_lay.setSpacing(12)
        
        title1 = QLabel("Fleksibilitas Mode Operasional")
        title1.setObjectName("Title")
        s1_lay.addWidget(title1)
        
        desc1 = QLabel("CafePulse menyediakan berbagai skenario untuk memantau café Anda:")
        desc1.setObjectName("Desc")
        s1_lay.addWidget(desc1)
        
        modes = [
            "• <b>Demo Mode</b>: Simulasi data café untuk memahami fitur visual program.",
            "• <b>Home WiFi Mode</b>: Pemindaian IP dinamis untuk mendeteksi penyusup lokal.",
            "• <b>Hotspot Mode</b>: Deteksi real-time pelanggan hotspot café Anda.",
            "• <b>MikroTik Mode</b>: Hubungkan langsung ke router MikroTik via port API."
        ]
        for m in modes:
            lbl = QLabel(m)
            lbl.setObjectName("FeatureItem")
            lbl.setWordWrap(True)
            s1_lay.addWidget(lbl)
        self.stack.addWidget(slide1)
        
        # Slide 2: Dashboard & Analitik
        slide2 = QWidget()
        s2_lay = QVBoxLayout(slide2)
        s2_lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        s2_lay.setSpacing(12)
        
        title2 = QLabel("Dashboard & Analitik Real-Time")
        title2.setObjectName("Title")
        s2_lay.addWidget(title2)
        
        desc2 = QLabel(
            "Semua grafik lalu lintas bandwidth dan data log perangkat yang Anda "
            "lihat direkam secara offline ke database lokal CafePulse. Data ini "
            "digunakan untuk memberikan analitik yang jujur mengenai beban jaringan café Anda."
        )
        desc2.setObjectName("Desc")
        desc2.setWordWrap(True)
        s2_lay.addWidget(desc2)
        
        features2 = [
            "• <b>Grafik Bandwidth</b>: Tren upload dan download yang terperinci.",
            "• <b>Keamanan Jaringan</b>: Notifikasi otomatis ketika perangkat tidak dikenal terdeteksi.",
            "• <b>Insights</b>: Laporan kesehatan jaringan café berbasis volume lalu lintas data."
        ]
        for f in features2:
            lbl = QLabel(f)
            lbl.setObjectName("FeatureItem")
            lbl.setWordWrap(True)
            s2_lay.addWidget(lbl)
        self.stack.addWidget(slide2)
        
        # Slide 3: Memulai Pemantauan
        slide3 = QWidget()
        s3_lay = QVBoxLayout(slide3)
        s3_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s3_lay.setSpacing(16)
        
        logo3 = QLabel("🚀")
        logo3.setStyleSheet("font-size: 54px; margin-bottom: 8px;")
        logo3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s3_lay.addWidget(logo3)
        
        title3 = QLabel("Siap Memulai CafePulse?")
        title3.setObjectName("Title")
        title3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s3_lay.addWidget(title3)
        
        desc3 = QLabel(
            "Navigasi menu utama berada di panel samping (Sidebar). Anda dapat "
            "membuka menu Pengaturan (Settings) kapan pun untuk mengubah parameter, "
            "serta memeriksa Crash Logs di menu Logs jika terjadi kendala teknis."
        )
        desc3.setObjectName("Desc")
        desc3.setWordWrap(True)
        desc3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s3_lay.addWidget(desc3)
        self.stack.addWidget(slide3)

    def _on_back_clicked(self):
        curr = self.stack.currentIndex()
        if curr > 0:
            self.stack.setCurrentIndex(curr - 1)
            self._update_navigation_buttons()

    def _on_next_clicked(self):
        curr = self.stack.currentIndex()
        if curr < self.stack.count() - 1:
            self.stack.setCurrentIndex(curr + 1)
            self._update_navigation_buttons()
        else:
            # Wizard selesai
            self._prompt_demo_mode()

    def _on_skip_clicked(self):
        self._prompt_demo_mode()

    def _update_navigation_buttons(self):
        curr = self.stack.currentIndex()
        self.btn_back.setVisible(curr > 0)
        
        if curr == self.stack.count() - 1:
            self.btn_next.setText("Selesai")
        else:
            self.btn_next.setText("Lanjut")

    def _prompt_demo_mode(self):
        """Menampilkan dialog konfirmasi untuk mengaktifkan Demo Mode setelah wizard selesai."""
        msg = QMessageBox(self)
        msg.setWindowTitle("CafePulse — Konfirmasi Workspace")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("<b>Bagaimana Anda ingin memulai CafePulse?</b>")
        msg.setInformativeText(
            "Pilih <b>Enable Demo Mode</b> untuk memuat simulasi data café dan mempelajari fitur secara instan.<br><br>"
            "Pilih <b>Start Empty Workspace</b> untuk memulai pemantauan kosong dari nol secara profesional."
        )
        
        # Premium dark styling for QMessageBox
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0F1117;
            }
            QLabel {
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1E2535;
                border: 1px solid #2D3748;
                border-radius: 6px;
                color: #F1F5F9;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #2D3748;
            }
        """)
        
        demo_btn = msg.addButton("Enable Demo Mode", QMessageBox.ButtonRole.YesRole)
        empty_btn = msg.addButton("Start Empty Workspace", QMessageBox.ButtonRole.NoRole)
        
        # Set highlight pada button YES
        demo_btn.setStyleSheet("""
            background-color: #3B82F6;
            color: white;
            border: none;
            padding: 8px 16px;
        """)
        
        msg.exec()
        
        use_demo = (msg.clickedButton() == demo_btn)
        self.onboarding_finished.emit(use_demo)
        
        if use_demo:
            self.accept()
        else:
            self.reject()
            
    def closeEvent(self, event):
        """Mencegah tombol X menutup onboarding secara kasar tanpa memilih."""
        # Sebaiknya diasumsikan user menolak demo jika menutup wizard secara kasar
        self.onboarding_finished.emit(False)
        self.reject()
        event.accept()
