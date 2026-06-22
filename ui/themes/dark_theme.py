"""
CafePulse — Dark Theme
Cyber-clean dark palette applied as a Qt stylesheet.
"""

DARK_STYLESHEET = """
/* ═══════════════════════════════════════════════════════════
   CafePulse Dark Theme — Cyber-Clean Edition
   ═══════════════════════════════════════════════════════════ */

/* ── Global ──────────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: #E2E8F0;
    outline: none;
}

QMainWindow, QWidget {
    background-color: #0F1117;
}

/* ── Sidebar ──────────────────────────────────────────────── */
#Sidebar {
    background-color: #161B27;
    border-right: 1px solid #1E2535;
    min-width: 200px;
    max-width: 200px;
}

#SidebarLogo {
    background-color: transparent;
    padding: 0px;
    font-size: 22px;
    font-weight: 800;
    color: #38BDF8;
    letter-spacing: 0.5px;
}

#SidebarVersionLabel {
    color: #475569;
    font-size: 10px;
    padding: 0px 16px 16px 16px;
}

QPushButton#NavButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 10px 16px;
    color: #94A3B8;
    font-size: 13px;
    font-weight: 500;
    margin: 2px 8px;
}

QPushButton#NavButton:hover {
    background-color: #1E2535;
    color: #E2E8F0;
}

QPushButton#NavButton:checked {
    background-color: #1E3A5F;
    color: #38BDF8;
    border-left: 3px solid #38BDF8;
}

/* ── Top Bar ──────────────────────────────────────────────── */
#TopBar {
    background-color: #161B27;
    border-bottom: 1px solid #1E2535;
    min-height: 52px;
    max-height: 52px;
    padding: 0 20px;
}

#TopBarModeLabel {
    background-color: #1E2535;
    color: #38BDF8;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

#TopBarStatusDot {
    font-size: 20px;
}

#TopBarStatusLabel {
    color: #94A3B8;
    font-size: 12px;
}

#TopBarDeviceCount {
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#QuickScanButton {
    background-color: #0EA5E9;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton#QuickScanButton:hover {
    background-color: #38BDF8;
}

QPushButton#QuickScanButton:pressed {
    background-color: #0284C7;
}

/* ── Content Area ─────────────────────────────────────────── */
#ContentArea {
    background-color: #0F1117;
    padding: 20px;
}

/* ── Dashboard Cards ──────────────────────────────────────── */
#DashCard {
    background-color: #161B27;
    border: 1px solid #1E2535;
    border-radius: 12px;
    /* NO padding here — layout margins handle internal spacing */
}

#DashCardTitle {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

#DashCardValue {
    color: #F1F5F9;
    /* font-size and font-weight are set inline per card to avoid Qt clipping */
}

#DashCardSub {
    color: #475569;
    font-size: 11px;
}

/* ── Section Headers ──────────────────────────────────────── */
#SectionHeader {
    color: #F1F5F9;
    font-size: 16px;
    font-weight: 700;
    padding-bottom: 4px;
}

#SectionSubtitle {
    color: #64748B;
    font-size: 12px;
}

/* ── Scrollbars ───────────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #0F1117;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #1E2535;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2D3A50;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

/* ── Tables ───────────────────────────────────────────────── */
QTableWidget {
    background-color: #161B27;
    border: 1px solid #1E2535;
    border-radius: 8px;
    gridline-color: #1E2535;
    selection-background-color: #1E3A5F;
}

QTableWidget QLineEdit, QTableView QLineEdit {
    background-color: #0B0F19;
    border: 1px solid #38BDF8;
    border-radius: 4px;
    padding: 2px 6px;
    margin: 0px;
    color: #F8FAFC;
    selection-background-color: #1E3A5F;
    selection-color: #38BDF8;
}

QTableWidget::item {
    padding: 6px 12px;
    color: #CBD5E1;
}

QTableWidget::item:selected {
    background-color: #1E3A5F;
    color: #38BDF8;
}

QHeaderView::section {
    background-color: #1E2535;
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 12px;
    border: none;
    letter-spacing: 0.5px;
}

/* ── Notification Badge ───────────────────────────────────── */
#AlertBadge {
    background-color: #EF4444;
    color: white;
    border-radius: 8px;
    font-size: 10px;
    font-weight: 700;
    padding: 1px 5px;
    min-width: 16px;
    max-width: 24px;
}

/* ── Status Indicator Colors ──────────────────────────────── */
#StatusOnline  { color: #22C55E; }
#StatusOffline { color: #475569; }
#StatusWarning { color: #F59E0B; }
#StatusDanger  { color: #EF4444; }

/* ── Input Fields ─────────────────────────────────────────── */
QLineEdit {
    background-color: #1E2535;
    border: 1px solid #2D3A50;
    border-radius: 8px;
    padding: 8px 12px;
    color: #E2E8F0;
    selection-background-color: #0EA5E9;
}

QLineEdit:focus {
    border-color: #0EA5E9;
}

/* ── Combo Box ────────────────────────────────────────────── */
QComboBox {
    background-color: #1E2535;
    border: 1px solid #2D3A50;
    border-radius: 8px;
    padding: 6px 12px;
    color: #E2E8F0;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #1E2535;
    border: 1px solid #2D3A50;
    selection-background-color: #1E3A5F;
    color: #E2E8F0;
}

/* ── General Buttons ──────────────────────────────────────── */
QPushButton {
    background-color: #1E2535;
    border: 1px solid #2D3A50;
    border-radius: 8px;
    padding: 8px 16px;
    color: #E2E8F0;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #2D3A50;
    border-color: #38BDF8;
}

QPushButton:pressed {
    background-color: #1E3A5F;
}

/* ── Separator ────────────────────────────────────────────── */
#SidebarSeparator {
    background-color: #1E2535;
    max-height: 1px;
    margin: 8px 16px;
}

/* ── Tooltip ──────────────────────────────────────────────── */
QToolTip {
    background-color: #1E2535;
    color: #E2E8F0;
    border: 1px solid #2D3A50;
    border-radius: 6px;
    padding: 4px 8px;
}
"""


# ─── Accent colors (for programmatic use) ─────────────────────────────────────
COLORS = {
    "bg_primary":     "#0F1117",
    "bg_secondary":   "#161B27",
    "bg_tertiary":    "#1E2535",
    "border":         "#1E2535",
    "accent_blue":    "#38BDF8",
    "accent_blue_dk": "#0EA5E9",
    "text_primary":   "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted":     "#475569",
    "success":        "#22C55E",
    "warning":        "#F59E0B",
    "danger":         "#EF4444",
    "info":           "#38BDF8",
}
