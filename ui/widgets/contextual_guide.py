"""
CafePulse — Contextual Guide Card
Widget melayang (floating overlay card) PyQt6-native dengan visual glassmorphism
untuk menampilkan bantuan kontekstual sekali-tayang pada setiap menu.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class ContextualGuideCard(QFrame):
    # Dipancarkan ketika tombol "Mengerti" diklik oleh user
    dismissed = pyqtSignal()

    def __init__(self, title: str, html_content: str, parent=None):
        super().__init__(parent)
        
        self.setObjectName("GuideCard")
        
        # Semi-transparent dark background (glassmorphism) with high HSL border accent
        self.setStyleSheet("""
            QFrame#GuideCard {
                background-color: rgba(22, 27, 39, 0.9);
                border: 1.5px solid #3B82F6;
                border-radius: 10px;
            }
            QLabel#TipIcon {
                font-size: 24px;
                background: transparent;
            }
            QLabel#TipTitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #3B82F6;
                background: transparent;
            }
            QLabel#TipDesc {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                color: #CBD5E1;
                line-height: 1.5;
                background: transparent;
            }
            QPushButton#BtnDismiss {
                background-color: #1E2535;
                border: 1px solid #2D3748;
                border-radius: 5px;
                color: #F1F5F9;
                padding: 6px 12px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton#BtnDismiss:hover {
                background-color: #3B82F6;
                color: white;
                border-color: #3B82F6;
            }
        """)
        
        # Set shadow effect
        try:
            from PyQt6.QtWidgets import QGraphicsDropShadowEffect
            from PyQt6.QtGui import QColor
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 180))
            shadow.setOffset(0, 4)
            self.setGraphicsEffect(shadow)
        except Exception:
            pass

        self._setup_ui(title, html_content)

    def _setup_ui(self, title: str, html_content: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        # Header Row
        hdr_layout = QHBoxLayout()
        hdr_layout.setSpacing(8)
        
        icon = QLabel("💡")
        icon.setObjectName("TipIcon")
        hdr_layout.addWidget(icon)
        
        title_lbl = QLabel(title)
        title_lbl.setObjectName("TipTitle")
        hdr_layout.addWidget(title_lbl)
        
        hdr_layout.addStretch()
        layout.addLayout(hdr_layout)
        
        # Description
        desc_lbl = QLabel(html_content)
        desc_lbl.setObjectName("TipDesc")
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)
        
        # Footer Action Row
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        btn_dismiss = QPushButton("Mengerti ✓")
        btn_dismiss.setObjectName("BtnDismiss")
        btn_dismiss.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_dismiss.clicked.connect(self._on_dismiss)
        footer_layout.addWidget(btn_dismiss)
        
        layout.addLayout(footer_layout)

    def _on_dismiss(self):
        self.dismissed.emit()
        self.deleteLater()
        
    def show_floating(self, parent_widget: QWidget, x_offset: int = 24, y_offset: int = 24):
        """Posisikan guide card di atas parent secara melayang di pojok kanan bawah."""
        self.setParent(parent_widget)
        self.adjustSize()
        
        # Hitung posisi di pojok kanan bawah parent
        p_width = parent_widget.width()
        p_height = parent_widget.height()
        
        w_width = self.width()
        w_height = self.height()
        
        # Batasi lebar maksimal agar terlihat proporsional
        if w_width > 320:
            self.setFixedWidth(320)
            self.adjustSize()
            w_width = self.width()
            w_height = self.height()
            
        pos_x = p_width - w_width - x_offset
        pos_y = p_height - w_height - y_offset
        
        self.move(pos_x, pos_y)
        self.show()
        self.raise_()
