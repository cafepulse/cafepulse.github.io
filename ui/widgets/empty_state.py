"""
CafePulse — Empty State Widget
Widget kosong informatif premium (Empty State) bertema gelap dengan Call-to-Action (CTA)
untuk menggantikan dummy data/charts ketika monitoring tidak aktif.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class EmptyStateWidget(QWidget):
    # Dipancarkan ketika user menekan tombol CTA "Aktifkan Demo Mode"
    quick_start_requested = pyqtSignal()

    def __init__(self, title: str, subtitle: str, icon: str = "📡", cta_text: str = "Aktifkan Demo Mode", parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("""
            QWidget#EmptyContainer {
                background-color: #0F1117;
            }
            QFrame#CardFrame {
                background-color: #161B27;
                border: 1px solid #1E2535;
                border-radius: 12px;
            }
            QLabel#IconLabel {
                font-size: 54px;
                background: transparent;
            }
            QLabel#TitleLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: #F8FAFC;
            }
            QLabel#SubtitleLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                color: #94A3B8;
            }
            QPushButton#CtaButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#CtaButton:hover {
                background-color: #2563EB;
            }
            QPushButton#CtaButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        
        self.setObjectName("EmptyContainer")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        card = QFrame()
        card.setObjectName("CardFrame")
        card.setFixedWidth(420)  # Standardize width to prevent dynamic resizing issues
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(14)  # Explicit spacing between widgets instead of QSS margins
        
        # Icon
        self.icon_lbl = QLabel(icon)
        self.icon_lbl.setObjectName("IconLabel")
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.icon_lbl)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("TitleLabel")
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title_lbl)
        
        # Subtitle
        self.sub_lbl = QLabel(subtitle)
        self.sub_lbl.setObjectName("SubtitleLabel")
        self.sub_lbl.setWordWrap(True)
        self.sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.sub_lbl)
        
        # CTA Button
        if cta_text:
            self.cta_btn = QPushButton(cta_text)
            self.cta_btn.setObjectName("CtaButton")
            self.cta_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.cta_btn.clicked.connect(self.quick_start_requested.emit)
            card_layout.addWidget(self.cta_btn)
            
        layout.addWidget(card)

    def update_theme(self, theme: str) -> None:
        """Dynamically styles the empty state canvas, container, and child components."""
        if theme == "light":
            self.setStyleSheet("""
                QWidget#EmptyContainer {
                    background-color: #F8FAFC;
                }
                QFrame#CardFrame {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
                QLabel#IconLabel {
                    font-size: 54px;
                    background: transparent;
                }
                QLabel#TitleLabel {
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 18px;
                    font-weight: bold;
                    color: #0F172A;
                }
                QLabel#SubtitleLabel {
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 13px;
                    color: #475569;
                }
                QPushButton#CtaButton {
                    background-color: #0284C7;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-family: 'Segoe UI', sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#CtaButton:hover {
                    background-color: #0369A1;
                }
                QPushButton#CtaButton:pressed {
                    background-color: #075985;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget#EmptyContainer {
                    background-color: #0F1117;
                }
                QFrame#CardFrame {
                    background-color: #161B27;
                    border: 1px solid #1E2535;
                    border-radius: 12px;
                }
                QLabel#IconLabel {
                    font-size: 54px;
                    background: transparent;
                }
                QLabel#TitleLabel {
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 18px;
                    font-weight: bold;
                    color: #F8FAFC;
                }
                QLabel#SubtitleLabel {
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 13px;
                    color: #94A3B8;
                }
                QPushButton#CtaButton {
                    background-color: #3B82F6;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-family: 'Segoe UI', sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#CtaButton:hover {
                    background-color: #2563EB;
                }
                QPushButton#CtaButton:pressed {
                    background-color: #1D4ED8;
                }
            """)
