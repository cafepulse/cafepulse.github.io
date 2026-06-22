"""
CafePulse — Sidebar Navigation Widget
Left panel with nav buttons grouped by 4 Workspaces, logo, and Pro licensing indicators.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from core.utils.version import __version__

logger = logging.getLogger("cafepulse.ui.sidebar")

# Grouped Workspace Navigation Definition
# format: (page_id, label, is_pro_only)
WORKSPACES = [
    ("BUSINESS", [
        ("dashboard", "⬡  Dashboard", False),
        ("analytics", "⬡  Analytics & BI", True),
    ]),
    ("OPERATIONS", [
        ("devices", "⬡  Device Manager", False),
        ("hotspot_detail", "⬡  Internet Access", False),
        ("alerts", "⬡  Alert Center", False),
    ]),
    ("NETWORK", [
        ("home_wifi_detail", "⬡  Personal Network", False),
        ("mikrotik_detail", "⬡  MikroTik Dashboard", True),
    ]),
    ("ADVANCED", [
        ("modes", "⬡  Mode Switcher", False),
        ("settings", "⬡  Settings", False),
        ("compatibility", "⬡  Compatibility Info", False),
        ("about", "⬡  About CafePulse", False),
    ])
]

def crop_image_padding(pixmap: QPixmap) -> QPixmap:
    """Crops transparent padding around the logo to allow it to be scaled prominently."""
    if pixmap.isNull():
        return pixmap
    image = pixmap.toImage()
    width = image.width()
    height = image.height()
    
    # Initialize bounds
    left, right, top, bottom = width, 0, height, 0
    has_pixels = False
    
    # Scan alpha values to find bounding box of content
    for y in range(height):
        for x in range(width):
            color = image.pixelColor(x, y)
            if color.alpha() > 10:
                has_pixels = True
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y
                
    if not has_pixels:
        return pixmap
        
    # Crop the image
    cropped_image = image.copy(left, top, right - left + 1, bottom - top + 1)
    return QPixmap.fromImage(cropped_image)

class Sidebar(QWidget):
    """
    Left navigation sidebar grouped by 4 Workspaces (Business, Operations, Network, Advanced).
    Emits `page_changed(page_id: str)` when a nav button is clicked.
    Dinamically adjusts to License Status (Basic vs Pro).
    """

    page_changed = pyqtSignal(str)

    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self._buttons: dict[str, QPushButton] = {}
        self._alert_badge: QLabel | None = None
        self._app_state = app_state
        self._menu_definitions: dict[str, tuple[str, bool]] = {} # map page_id -> (original_label, is_pro_only)
        
        # Populate flat map for convenience
        for _, items in WORKSPACES:
            for page_id, label, is_pro in items:
                self._menu_definitions[page_id] = (label, is_pro)
        
        self._workspace_headers = []
        self._build_ui()
        
        if self._app_state:
            self._app_state.mode_changed.connect(self.set_mode_label)
            self._app_state.alerts_updated.connect(self.set_alert_count)
            self._app_state.licensing_changed.connect(self.update_licensing_visuals)
            
            # Sync initial licensing state
            self.update_licensing_visuals(self._app_state.is_pro)
            
        self._activate("dashboard")

    # ─── Build ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo block
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(15, 16, 15, 0)
        logo_layout.setSpacing(10)
        
        logo_img = QLabel()
        from core.app_paths import LOGO_PATH
        import os
        img_path = str(LOGO_PATH)
        if not os.path.exists(img_path):
            img_path = str(LOGO_PATH.parent.parent / "logo.png")
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            pixmap = crop_image_padding(pixmap)
            pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_img.setPixmap(pixmap)
            logo_layout.addWidget(logo_img)
        
        logo_label = QLabel("CafePulse")
        logo_label.setObjectName("SidebarLogo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        logo_layout.addWidget(logo_label)
        self._logo_label = logo_label
        
        logo_layout.addStretch()
        layout.addWidget(logo_container)

        self._version_label = QLabel(f"v{__version__} — Free")
        self._version_label.setObjectName("SidebarVersionLabel")
        self._version_label.setStyleSheet("padding-left: 16px; margin-bottom: 12px;")
        layout.addWidget(self._version_label)

        # Separator
        sep = self._make_separator()
        layout.addWidget(sep)

        # Grouped Workspace Buttons
        for workspace_name, items in WORKSPACES:
            # Add Workspace Group Header Label
            header = QLabel(workspace_name)
            header.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    font-weight: 700;
                    color: #475569;
                    letter-spacing: 1.5px;
                    padding: 16px 16px 6px 16px;
                    background: transparent;
                }
            """)
            layout.addWidget(header)
            self._workspace_headers.append(header)

            for page_id, label, is_pro_only in items:
                btn = QPushButton(label)
                btn.setObjectName("NavButton")
                btn.setCheckable(True)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda checked, pid=page_id: self._on_nav_click(pid))

                # Alerts row: wrap in HBox so we can add badge
                if page_id == "alerts":
                    row = QWidget()
                    row.setObjectName("SidebarRow")
                    row.setStyleSheet("background: transparent;")
                    row_layout = QHBoxLayout(row)
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    row_layout.setSpacing(0)
                    row_layout.addWidget(btn)
                    
                    badge = QLabel("0")
                    badge.setObjectName("AlertBadge")
                    badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    badge.setFixedSize(22, 16)
                    badge.setVisible(False)
                    row_layout.addWidget(badge)
                    row_layout.addSpacing(12)
                    layout.addWidget(row)
                    self._alert_badge = badge
                else:
                    layout.addWidget(btn)

                self._buttons[page_id] = btn

        # Spacer pushes version/mode to bottom
        layout.addStretch()

        # Mode indicator at bottom
        sep2 = self._make_separator()
        layout.addWidget(sep2)

        mode_label = QLabel("● Demo Mode")
        mode_label.setObjectName("SidebarVersionLabel")
        mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_label.setStyleSheet("color: #38BDF8; font-size: 11px; padding: 12px 0;")
        mode_label.setObjectName("SidebarModeIndicator")
        layout.addWidget(mode_label)
        self._mode_indicator = mode_label

    def _make_separator(self) -> QFrame:
        sep = QFrame()
        sep.setObjectName("SidebarSeparator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        return sep

    # ─── Interaction ──────────────────────────────────────────────────────────

    def _on_nav_click(self, page_id: str) -> None:
        self._activate(page_id)
        self.page_changed.emit(page_id)

    def _activate(self, page_id: str) -> None:
        for pid, btn in self._buttons.items():
            btn.setChecked(pid == page_id)

    def set_active_page(self, page_id: str) -> None:
        self._activate(page_id)

    # ─── External Updates ─────────────────────────────────────────────────────

    def set_alert_count(self, count: int) -> None:
        if self._alert_badge:
            if count > 0:
                self._alert_badge.setText(str(min(count, 99)))
                self._alert_badge.setVisible(True)
            else:
                self._alert_badge.setVisible(False)

    def set_mode_label(self, mode_name: str) -> None:
        if self._mode_indicator:
            self._mode_indicator.setText(f"● {mode_name}")

    def update_licensing_visuals(self, is_pro: bool) -> None:
        """Dinamis merestrukturisasi label menu sidebar berdasarkan status lisensi."""
        logger.info("Updating sidebar UI visuals. Pro Status: %s", is_pro)
        
        # 1. Update Version Label
        if is_pro:
            self._version_label.setText(f"v{__version__} — Professional")
            self._version_label.setStyleSheet("color: #06B6D4; padding-left: 16px; margin-bottom: 12px; font-weight: 700;")
        else:
            self._version_label.setText(f"v{__version__} — Free")
            self._version_label.setStyleSheet("color: #64748B; padding-left: 16px; margin-bottom: 12px; font-weight: 500;")

        # 2. Update Nav Buttons Text (add lock indicators for Free Edition)
        for page_id, btn in self._buttons.items():
            orig_label, is_pro_only = self._menu_definitions.get(page_id, ("", False))
            if is_pro_only and not is_pro:
                # Add elegant lock/PRO tag
                btn.setText(f"{orig_label}  🔒")
                btn.setStyleSheet("color: #64748B;") # Muted gray color
            else:
                # Restores original label
                btn.setText(orig_label)
                btn.setStyleSheet("") # Clear style override

    def set_compact(self, compact: bool) -> None:
        """
        Updates the sidebar layout dynamically to compact mode or restores full mode.
        """
        if hasattr(self, "_logo_label") and self._logo_label:
            self._logo_label.setVisible(not compact)
        if hasattr(self, "_version_label") and self._version_label:
            self._version_label.setVisible(not compact)
        if hasattr(self, "_mode_indicator") and self._mode_indicator:
            self._mode_indicator.setVisible(not compact)
            
        for header in getattr(self, "_workspace_headers", []):
            header.setVisible(not compact)
            
        # Icon mapping for compact view
        compact_emojis = {
            "dashboard": "📊",
            "analytics": "📈",
            "devices": "💻",
            "hotspot_detail": "🔑",
            "alerts": "🔔",
            "home_wifi_detail": "📶",
            "mikrotik_detail": "🎛️",
            "modes": "🔌",
            "settings": "⚙️",
            "compatibility": "⚖️",
            "about": "ℹ️"
        }
        
        is_pro = self._app_state.is_pro if self._app_state else False
        for page_id, btn in self._buttons.items():
            orig_label, is_pro_only = self._menu_definitions.get(page_id, ("", False))
            clean_label = orig_label
            if is_pro_only and not is_pro:
                clean_label = f"{orig_label} 🔒"
                
            if compact:
                emoji = compact_emojis.get(page_id, "⬡")
                if is_pro_only and not is_pro:
                    btn.setText(f"{emoji}🔒")
                else:
                    btn.setText(emoji)
                btn.setToolTip(clean_label)
                btn.setStyleSheet("padding: 10px 0; text-align: center; font-size: 16px;")
            else:
                btn.setText(clean_label)
                btn.setToolTip("")
                if is_pro_only and not is_pro:
                    btn.setStyleSheet("color: #64748B; text-align: left; padding: 8px 16px;")
                else:
                    btn.setStyleSheet("text-align: left; padding: 8px 16px;")
                
        if compact:
            self.setFixedWidth(70)
        else:
            self.setFixedWidth(240)
