"""
CafePulse — Responsive Form Row Widget
Dynamically reflows between horizontal (Label | Input) and vertical (Label above Input) alignments based on responsive breakpoints.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

class ResponsiveFormRow(QWidget):
    def __init__(self, label_text: str, widget: QWidget, hint_text: str = "", parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self._widget = widget
        self._label = QLabel(label_text)
        self._label.setObjectName("InfoLabel")
        self._label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        self._label.setWordWrap(True)
        
        self._field_container = QWidget()
        self._field_layout = QVBoxLayout(self._field_container)
        self._field_layout.setContentsMargins(0, 0, 0, 0)
        self._field_layout.setSpacing(2)
        self._field_layout.addWidget(self._widget)
        
        self._hint = None
        if hint_text:
            self._hint = QLabel(hint_text)
            self._hint.setStyleSheet("color: #4A5568; font-size: 10px;")
            self._hint.setWordWrap(True)
            self._field_layout.addWidget(self._hint)
            
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(16)
        self._grid.setVerticalSpacing(4)
        
        self.set_horizontal(True)
        
    def set_horizontal(self, is_horiz: bool):
        self._grid.removeWidget(self._label)
        self._grid.removeWidget(self._field_container)
        
        if is_horiz:
            self._label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self._label.setMinimumWidth(140)
            self._label.setMaximumWidth(180)
            self._grid.addWidget(self._label, 0, 0)
            self._grid.addWidget(self._field_container, 0, 1)
            self._grid.setColumnStretch(0, 0)
            self._grid.setColumnStretch(1, 1)
        else:
            self._label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self._label.setMinimumWidth(0)
            self._label.setMaximumWidth(16777215)
            self._grid.addWidget(self._label, 0, 0)
            self._grid.addWidget(self._field_container, 1, 0)
            self._grid.setColumnStretch(0, 1)
            self._grid.setColumnStretch(1, 0)
            
    def adapt_layout(self, bp: str):
        is_horiz = bp in ("large", "medium")
        self.set_horizontal(is_horiz)

    def update_theme(self, theme: str) -> None:
        if theme == "light":
            self._label.setStyleSheet("color: #475569; font-size: 12px;")
            if self._hint:
                self._hint.setStyleSheet("color: #64748B; font-size: 10px;")
        else:
            self._label.setStyleSheet("color: #94A3B8; font-size: 12px;")
            if self._hint:
                self._hint.setStyleSheet("color: #4A5568; font-size: 10px;")
