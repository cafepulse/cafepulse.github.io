from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

class DashCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "", accent: str = "#38BDF8", parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMinimumHeight(120)
        self.setMinimumWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(3)

        title_lbl = QLabel(title.upper())
        title_lbl.setObjectName("DashCardTitle")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        self._value_lbl = QLabel(value)
        self._value_lbl.setObjectName("DashCardValue")
        self._value_lbl.setStyleSheet(f"color: {accent}; font-size: 30px; font-weight: 700;")
        self._value_lbl.setMinimumHeight(40)
        self._value_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._value_lbl)

        self._sub_lbl = QLabel(subtitle)
        self._sub_lbl.setObjectName("DashCardSub")
        self._sub_lbl.setWordWrap(True)
        layout.addWidget(self._sub_lbl)

    def update_value(self, value: str) -> None:
        self._value_lbl.setText(value)

    def update_sub(self, sub: str) -> None:
        self._sub_lbl.setText(sub)
