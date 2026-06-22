"""
CafePulse — Placeholder Page
Generic placeholder for pages not yet implemented (Phases 3–7).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class PlaceholderPage(QWidget):
    """Shown for nav sections not yet implemented."""

    def __init__(self, title: str, description: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel("⬡")
        icon.setStyleSheet("font-size: 48px; color: #1E2535;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("SectionHeader")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        if description:
            desc_lbl = QLabel(description)
            desc_lbl.setObjectName("SectionSubtitle")
            desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(desc_lbl)

        phase_lbl = QLabel("Coming in a future phase")
        phase_lbl.setStyleSheet("color: #1E3A5F; font-size: 11px; margin-top: 8px;")
        phase_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(phase_lbl)
