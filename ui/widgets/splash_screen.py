import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPainterPath

class CafePulseSplashScreen(QWidget):
    """
    A stunning, frameless, rounded-corner Splash Screen for CafePulse.
    Loads assets/branding/splash.png as a full-size high-res background,
    rendering dynamic loading status text and a sleek progress bar on top.
    """
    def __init__(self, splash_path: str):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.SplashScreen | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Increased scale by 300% (600x400 canvas for prominent visibility)
        self.setFixedSize(600, 400)
        
        # Load background pixmap
        self.background_pixmap = None
        if os.path.exists(splash_path):
            self.background_pixmap = QPixmap(splash_path).scaled(
                600, 400, 
                Qt.AspectRatioMode.IgnoreAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
        self._build_ui()

    def _build_ui(self) -> None:
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        
        # Push all contents to the bottom overlay area
        layout.addStretch()
        
        # Translucent dark backing overlay for loading widgets (to ensure readability on any background)
        overlay_frame = QFrame()
        overlay_frame.setObjectName("OverlayFrame")
        overlay_frame.setStyleSheet("""
            QFrame#OverlayFrame {
                background-color: rgba(11, 15, 25, 0.75);
                border: 1px solid rgba(30, 41, 59, 0.4);
                border-radius: 8px;
            }
        """)
        
        overlay_layout = QVBoxLayout(overlay_frame)
        overlay_layout.setContentsMargins(20, 16, 20, 16)
        overlay_layout.setSpacing(8)
        
        # Slogan (large/dominant version)
        self.slogan_lbl = QLabel("Offline-First Network Observability")
        self.slogan_lbl.setStyleSheet("""
            font-family: 'Segoe UI', -apple-system, sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: #38BDF8;
            letter-spacing: 1.5px;
            background: transparent;
        """)
        self.slogan_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(self.slogan_lbl)
        
        # Status Label
        self.status_lbl = QLabel("Inisialisasi sistem...")
        self.status_lbl.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 11px;
            color: #94A3B8;
            background: transparent;
        """)
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(self.status_lbl)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(30, 41, 59, 0.6);
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #A78BFA);
                border-radius: 3px;
            }
        """)
        overlay_layout.addWidget(self.progress_bar)
        
        layout.addWidget(overlay_frame)

    def set_status(self, text: str, progress_val: int) -> None:
        """Updates loading text and progress bar percentage."""
        self.status_lbl.setText(text)
        self.progress_bar.setValue(progress_val)
        
        # Refresh and process events to repaint instantly
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()

    def paintEvent(self, event) -> None:
        """Paints the background image with 12px rounded corners."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Define rounded rect path
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 12, 12)
        painter.setClipPath(path)
        
        if self.background_pixmap:
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            # Fallback flat color if background_pixmap loading fails
            painter.setBrush(QColor("#0B0F19"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.rect())
            
        painter.end()
