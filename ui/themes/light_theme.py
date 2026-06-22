"""
CafePulse — Light Theme
Premium, clean light palette applied as a Qt stylesheet.
"""

LIGHT_STYLESHEET = """
/* ═══════════════════════════════════════════════════════════
   CafePulse Light Theme — Premium Clean Edition
   ═══════════════════════════════════════════════════════════ */

/* ── Global ──────────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: #0F172A;
    outline: none;
}

QMainWindow, QWidget {
    background-color: #F8FAFC;
}

/* ── Sidebar ──────────────────────────────────────────────── */
#Sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    min-width: 200px;
    max-width: 200px;
}

#SidebarLogo {
    background-color: transparent;
    padding: 0px;
    font-size: 22px;
    font-weight: 800;
    color: #0284C7;
    letter-spacing: 0.5px;
}

#SidebarVersionLabel {
    color: #94A3B8;
    font-size: 10px;
    padding: 0px 16px 16px 16px;
}

QPushButton#NavButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 10px 16px;
    color: #475569;
    font-size: 13px;
    font-weight: 500;
    margin: 2px 8px;
}

QPushButton#NavButton:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

QPushButton#NavButton:checked {
    background-color: #E0F2FE;
    color: #0284C7;
    border-left: 3px solid #0284C7;
}

/* ── Top Bar ──────────────────────────────────────────────── */
#TopBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    min-height: 52px;
    max-height: 52px;
    padding: 0 20px;
}

#TopBarModeLabel {
    background-color: #F1F5F9;
    color: #0284C7;
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
    color: #475569;
    font-size: 12px;
}

#TopBarDeviceCount {
    color: #0F172A;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#QuickScanButton {
    background-color: #0284C7;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton#QuickScanButton:hover {
    background-color: #0369A1;
}

QPushButton#QuickScanButton:pressed {
    background-color: #075985;
}

/* ── Content Area ─────────────────────────────────────────── */
#ContentArea {
    background-color: #F8FAFC;
    padding: 20px;
}

/* ── Dashboard Cards ──────────────────────────────────────── */
#DashCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

#DashCardTitle {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

#DashCardValue {
    color: #0F172A;
}

#DashCardSub {
    color: #64748B;
    font-size: 11px;
}

/* ── Section Headers ──────────────────────────────────────── */
#SectionHeader {
    color: #0F172A;
    font-size: 16px;
    font-weight: 700;
    padding-bottom: 4px;
}

#SectionSubtitle {
    color: #475569;
    font-size: 12px;
}

/* ── Scrollbars ───────────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #F8FAFC;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

/* ── Tables ───────────────────────────────────────────────── */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #F1F5F9;
    selection-background-color: #E0F2FE;
}

QTableWidget QLineEdit, QTableView QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #0284C7;
    border-radius: 4px;
    padding: 2px 6px;
    margin: 0px;
    color: #0F172A;
    selection-background-color: #E0F2FE;
    selection-color: #0284C7;
}

QTableWidget::item {
    padding: 6px 12px;
    color: #334155;
}

QTableWidget::item:selected {
    background-color: #E0F2FE;
    color: #0284C7;
}

QHeaderView::section {
    background-color: #F1F5F9;
    color: #475569;
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
#StatusOffline { color: #64748B; }
#StatusWarning { color: #F59E0B; }
#StatusDanger  { color: #EF4444; }

/* ── Input Fields ─────────────────────────────────────────── */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0F172A;
    selection-background-color: #E0F2FE;
}

QLineEdit:focus {
    border-color: #0284C7;
}

/* ── Combo Box ────────────────────────────────────────────── */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 12px;
    color: #0F172A;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    selection-background-color: #E0F2FE;
    color: #0F172A;
}

/* ── General Buttons ──────────────────────────────────────── */
QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 16px;
    color: #334155;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #F1F5F9;
    border-color: #0284C7;
}

QPushButton:pressed {
    background-color: #E2E8F0;
}

/* ── Separator ────────────────────────────────────────────── */
#SidebarSeparator {
    background-color: #E2E8F0;
    max-height: 1px;
    margin: 8px 16px;
}

/* ── Tooltip ──────────────────────────────────────────────── */
QToolTip {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 4px 8px;
}
"""

COLORS = {
    "bg_primary":     "#F8FAFC",
    "bg_secondary":   "#FFFFFF",
    "bg_tertiary":    "#F1F5F9",
    "border":         "#E2E8F0",
    "accent_blue":    "#0284C7",
    "accent_blue_dk": "#0369A1",
    "text_primary":   "#0F172A",
    "text_secondary": "#475569",
    "text_muted":     "#94A3B8",
    "success":        "#22C55E",
    "warning":        "#F59E0B",
    "danger":         "#EF4444",
    "info":           "#0284C7",
}
