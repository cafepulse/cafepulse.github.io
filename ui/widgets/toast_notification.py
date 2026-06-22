"""
CafePulse — Toast Notification
Lightweight overlay notification that slides in from the bottom-right corner,
stays for a few seconds, then fades out. No third-party dependencies.
"""

import logging
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt6.QtGui import QColor, QPainter, QPainterPath

logger = logging.getLogger("cafepulse.ui.toast")

# ── Alert type → (icon, accent color) ────────────────────────────────────────
_STYLES: dict[str, tuple[str, str]] = {
    "new_device":  ("📡", "#38BDF8"),   # blue
    "offline":     ("📴", "#94A3B8"),   # gray
    "suspicious":  ("⚠️",  "#F59E0B"),  # amber
    "reconnect":   ("🔄", "#22C55E"),   # green
    "error":       ("❌", "#EF4444"),   # red
    "info":        ("ℹ️",  "#38BDF8"),  # blue
    "warning":     ("⚠️",  "#F59E0B"),  # amber
}
_DEFAULT_STYLE = ("🔔", "#64748B")


class ToastNotification(QWidget):
    """
    A single toast popup.
    Parent MUST be the top-level QMainWindow so positioning works correctly.
    """

    @staticmethod
    def show_toast(parent_widget: QWidget, message: str, duration_ms: int = 3000, alert_type: str = "info") -> None:
        """
        Helper method to show a quick toast notification from any widget.
        Attempts to use the parent window's ToastManager if available,
        otherwise creates and shows a standalone ToastNotification.
        """
        try:
            window = parent_widget.window()
            if window and hasattr(window, "_toast_mgr") and window._toast_mgr:
                window._toast_mgr.show_toast(alert_type, message, duration_ms)
                return
        except Exception:
            pass
            
        try:
            toast = ToastNotification(parent_widget.window() or parent_widget, alert_type, message, duration_ms)
            # Standalone placement at bottom-right corner as a fallback
            try:
                pw = (parent_widget.window() or parent_widget).width()
                ph = (parent_widget.window() or parent_widget).height()
                toast.adjustSize()
                toast.move(pw - toast.width() - 20, ph - toast.height() - 20)
            except Exception:
                pass
            toast.show()
        except Exception as e:
            logger.error("Failed to show standalone toast: %s", e)

    def __init__(self, parent: QWidget, alert_type: str, message: str,
                 duration_ms: int = 4000):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint |
                         Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedWidth(340)

        icon, accent = _STYLES.get(alert_type, _DEFAULT_STYLE)
        self._accent = accent
        self._opacity = 1.0

        # ── Layout ────────────────────────────────────────────────────────────
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)

        # Left accent bar (painted manually)
        self._accent_color = QColor(accent)

        # Icon
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("background: transparent; font-size: 18px;")
        icon_lbl.setFixedWidth(24)
        root.addWidget(icon_lbl)

        # Text block
        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        # Type label
        type_text = alert_type.replace("_", " ").title()
        type_lbl = QLabel(type_text)
        type_lbl.setStyleSheet(
            f"background: transparent; color: {accent}; "
            f"font-size: 10px; font-weight: 700; letter-spacing: 0.8px;"
        )
        text_col.addWidget(type_lbl)

        # Message — truncate if too long
        display_msg = message if len(message) <= 80 else message[:77] + "…"
        msg_lbl = QLabel(display_msg)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet(
            "background: transparent; color: #E2E8F0; font-size: 11px;"
        )
        text_col.addWidget(msg_lbl)
        root.addLayout(text_col)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(18, 18)
        close_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #4A5568; border: none; "
            "font-size: 10px; padding: 0; }"
            "QPushButton:hover { color: #94A3B8; }"
        )
        close_btn.clicked.connect(self._dismiss)
        root.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignTop)

        self.adjustSize()

        # ── Auto-dismiss timer ────────────────────────────────────────────────
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._start_fade_out)
        self._timer.start(duration_ms)

    # ── Painting ──────────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setOpacity(self._opacity)

        # Background card
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        p.fillPath(path, QColor("#0F172A"))

        # Border
        p.setPen(QColor("#1E293B"))
        p.drawPath(path)

        # Left accent stripe
        stripe = QPainterPath()
        stripe.addRoundedRect(0, 0, 4, self.height(), 2, 2)
        p.fillPath(stripe, self._accent_color)

    # ── Opacity property for animation ────────────────────────────────────────

    def get_opacity(self) -> float:
        return self._opacity

    def set_opacity(self, value: float) -> None:
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    # ── Dismiss ───────────────────────────────────────────────────────────────

    def _dismiss(self):
        self._timer.stop()
        self._start_fade_out()

    def _start_fade_out(self):
        self._anim = QPropertyAnimation(self, b"opacity", self)
        self._anim.setDuration(350)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.finished.connect(self.close)
        self._anim.start()


# ── Toast Manager ─────────────────────────────────────────────────────────────

class ToastManager:
    """
    Manages a stack of active toasts anchored to the bottom-right of the
    parent window.  Call show_toast() from any thread-safe slot.

    Usage:
        self._toast_mgr = ToastManager(main_window)
        self._toast_mgr.show_toast("new_device", "iPhone joined the network")
    """

    MARGIN_RIGHT  = 20
    MARGIN_BOTTOM = 20
    SPACING       = 10

    def __init__(self, parent: QWidget):
        self._parent  = parent
        self._active: list[ToastNotification] = []

    def show_toast(self, alert_type: str, message: str,
                   duration_ms: int = 4000) -> None:
        toast = ToastNotification(self._parent, alert_type, message, duration_ms)
        toast.destroyed.connect(lambda: self._remove(toast))
        self._active.append(toast)
        self._reposition()
        toast.show()

    def _remove(self, toast: ToastNotification) -> None:
        try:
            self._active.remove(toast)
        except ValueError:
            pass
        self._reposition()

    def _reposition(self) -> None:
        """Stack toasts from the bottom-right upward."""
        pw = self._parent.width()
        ph = self._parent.height()
        y = ph - self.MARGIN_BOTTOM
        for toast in reversed(self._active):
            if not toast.isVisible():
                continue
            toast.adjustSize()
            h = toast.height()
            y -= h
            x = pw - toast.width() - self.MARGIN_RIGHT
            toast.move(x, y)
            y -= self.SPACING
