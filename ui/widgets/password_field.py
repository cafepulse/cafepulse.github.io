"""
CafePulse — Reusable Password Field Widget
QLineEdit with an embedded vector-drawn show/hide visibility toggle.
Drawn dynamically with QPainter to guarantee crisp rendering on HiDPI displays.
"""

import logging
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt

logger = logging.getLogger("cafepulse.ui.passwordfield")


class PasswordField(QLineEdit):
    """
    Premium, reusable password input field.
    Features an inline show/hide password toggle.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Embedded QAction in trailing position
        self.toggle_action = QAction(self)
        self.addAction(self.toggle_action, QLineEdit.ActionPosition.TrailingPosition)
        
        self._is_visible = False
        self._update_icon()
        
        self.toggle_action.triggered.connect(self.toggle_visibility)

    def toggle_visibility(self) -> None:
        """Toggles the password echo mode between Password and Normal."""
        self._is_visible = not self._is_visible
        if self._is_visible:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
        self._update_icon()
        logger.debug(f"Password field visibility toggled: {self._is_visible}")

    def _update_icon(self) -> None:
        """Draws eye/eye-off vector icon using QPainter for perfect crispness."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 0, 0, 0))  # transparent
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Harmonious Slate-400 theme color (#94A3B8)
        color = QColor("#94A3B8")
        pen = QPen(color)
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Top and bottom arcs for the eye silhouette
        painter.drawArc(4, 8, 24, 16, 30 * 16, 120 * 16)
        painter.drawArc(4, 8, 24, 16, 210 * 16, 120 * 16)
        
        # Pupil circle
        painter.setBrush(QBrush(color))
        painter.drawEllipse(12, 12, 8, 8)
        
        if not self._is_visible:
            # Draw a clean vector diagonal line (slash) across the eye for 'hidden' state
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(6, 6, 26, 26)
            
        painter.end()
        self.toggle_action.setIcon(QIcon(pixmap))
