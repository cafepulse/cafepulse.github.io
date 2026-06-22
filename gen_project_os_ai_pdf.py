"""
CafePulse - Project OS AI Complete Documentation PDF Generator
==============================================================
Mengkompilasi semua dokumen Project OS AI menjadi satu PDF premium.
Menggunakan fpdf2 dengan sanitasi karakter Latin-1 untuk kompatibilitas.

Jalankan dari root folder proyek:
    python gen_project_os_ai_pdf.py
"""

import sys
import re
import unicodedata
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("ERROR: fpdf2 tidak terinstall. Jalankan: pip install fpdf2")
    sys.exit(1)


# ── Configuration ─────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent
OUTPUT_FILE  = PROJECT_ROOT.parent / "artifacts" / "compiled_pdfs" / "CafePulse_Project_OS_AI_Complete.pdf"

# Brand Colors (CafePulse)
COLOR_PRIMARY    = (59,  130, 246)
COLOR_DARK       = (15,  23,  42)
COLOR_PANEL      = (30,  41,  59)
COLOR_ACCENT     = (6,   182, 212)
COLOR_SUCCESS    = (16,  185, 129)
COLOR_WHITE      = (255, 255, 255)
COLOR_LIGHT_GRAY = (226, 232, 240)
COLOR_TEXT_DARK  = (30,  41,  59)
COLOR_TEXT_MID   = (71,  85,  105)
COLOR_TEXT_LIGHT = (100, 116, 139)
COLOR_ROW_ALT    = (248, 250, 252)
COLOR_QUOTE_BG   = (239, 246, 255)
COLOR_CODE_BG    = (15,  23,  42)
COLOR_CODE_FG    = (6,   182, 212)
COLOR_DANGER     = (239, 68,  68)

# Document map: (display_title, file_path, section_number)
DOCUMENTS = [
    ("Project Bible",              "../artifacts/bible/PROJECT_BIBLE.md",   "01"),
    ("Product Strategy",           "../artifacts/strategy_and_marketing/PRODUCT_STRATEGY.md",     "02"),
    ("Go-to-Market Playbook",      "../artifacts/strategy_and_marketing/GO_TO_MARKET.md",         "03"),
    ("System Architecture",        "../artifacts/architecture_and_design/SYSTEM_ARCHITECTURE.md", "04"),
    ("User Personas & Research",   "../artifacts/user_research/USER_PERSONAS.md",   "05"),
    ("Business Model Canvas",      "../artifacts/business_model/BUSINESS_MODEL_CANVAS.md","06"),
    ("KPI & Metrics Dashboard",    "../artifacts/metrics_and_kpi/KPI_METRICS.md",           "07"),
    ("Feature Spec - Free Edition","../artifacts/specifications/FEATURE_SPEC_FREE.md",       "08"),
    ("Development Workflow",       "../artifacts/operations_and_workflow/DEVELOPMENT_WORKFLOW.md",   "09"),
    ("Launch Playbook",            "../artifacts/launch_playbooks/LAUNCH_PLAYBOOK.md",        "10"),
    ("CafePulse Master Reference", "../artifacts/architecture_and_design/CAFEPULSE_MASTER_REFERENCE.md", "11"),
    ("Feature Spec - Professional Edition", "../artifacts/specifications/FEATURE_SPEC_PROFESSIONAL.md", "12"),
    ("Changelog",                  "../artifacts/changelog/CHANGELOG.md",                   "13"),
]

SECTION_SUBTITLES = {
    "01": "Fondasi, Visi, Misi & Filosofi Produk",
    "02": "Positioning, Moat Kompetitif & Strategi Pertumbuhan",
    "03": "Saluran Distribusi, Messaging & Launch Phases",
    "04": "Stack Teknologi, Modul Sistem & Data Model",
    "05": "Profil 5 Persona Pengguna & Matrix Prioritas",
    "06": "Business Model Canvas, Unit Economics & Value Map",
    "07": "North Star Metric, KPI Bisnis & Product Metrics",
    "08": "User Stories & Acceptance Criteria - Free Edition",
    "09": "Git Strategy, Release Pipeline & Code Standards",
    "10": "Countdown Launch, Contingency Plans & Day-1 Timeline",
    "11": "Topologi Repositori, Manifest Berkas & Panduan Navigasi AI",
    "12": "User Stories & Kriteria Penerimaan - Professional Edition",
    "13": "Catatan Riwayat Rilis & Rekam Jejak Pembaruan",
}


# ── Text Sanitization ─────────────────────────────────────────────────────────

# Map for common Unicode characters → Latin-1 equivalents
CHAR_MAP = {
    '\u2014': '--',   # em dash
    '\u2013': '-',    # en dash
    '\u2018': "'",    # left single quote
    '\u2019': "'",    # right single quote
    '\u201C': '"',    # left double quote
    '\u201D': '"',    # right double quote
    '\u2022': '*',    # bullet
    '\u2026': '...',  # ellipsis
    '\u2192': '->',   # right arrow
    '\u2190': '<-',   # left arrow
    '\u2713': 'OK',   # check mark
    '\u2714': 'OK',   # heavy check mark
    '\u274C': 'X',    # cross mark
    '\u25B8': '>',    # right-pointing triangle
    '\u00B7': '.',    # middle dot
    '\u00D7': 'x',   # multiplication sign
    '\u00E9': 'e',   # e acute
    '\u21D2': '=>',  # right double arrow
    '\u2665': '<3',  # heart
    '\u2764': '<3',  # heavy heart
    '\u2728': '*',   # sparkles
    '\u26A0': '(!)', # warning sign
    '\u2705': '[OK]', # white heavy check mark
    '\u2611': '[x]',  # check box
    '\u2610': '[ ]',  # empty check box
    '\u27A4': '->',   # right arrow
    '\u00AB': '<<',   # left guillemet
    '\u00BB': '>>',   # right guillemet
    '\u2044': '/',    # fraction slash
    '\u00A0': ' ',    # non-breaking space
    '\u00AE': '(R)',  # registered trademark
    '\u00B0': 'deg',  # degree sign
    '\u03B1': 'alpha',# greek alpha
    '\u03B2': 'beta', # greek beta
    '\uFFFD': '?',    # replacement character
}

def sanitize(text: str) -> str:
    """Convert text to Latin-1 compatible string."""
    # Apply explicit map first
    for char, replacement in CHAR_MAP.items():
        text = text.replace(char, replacement)
    
    # Encode to Latin-1, replacing any remaining non-encodable chars
    encoded = text.encode('latin-1', errors='replace')
    return encoded.decode('latin-1')


def clean_md(text: str) -> str:
    """Remove inline markdown formatting and sanitize."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*',   r'\1', text)
    text = re.sub(r'`([^`]+)`',     r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'#{1,6}\s+',     '',    text)
    return sanitize(text.strip())


# ── PDF Class ─────────────────────────────────────────────────────────────────

class CafePulsePDF(FPDF):

    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(left=18, top=18, right=18)
        self._cur_section = ''

    # ── Header / Footer ───────────────────────────────────────────────────────

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 210, 3.5, 'F')
        self.set_xy(18, 5.5)
        self.set_font('Helvetica', 'B', 6.5)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 4, 'CAFEPULSE  |  PROJECT OS AI DOCUMENTATION SUITE', align='L')
        self.set_xy(18, 5.5)
        self.set_font('Helvetica', '', 6.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 4, sanitize(self._cur_section), align='R')
        self.set_text_color(*COLOR_TEXT_DARK)
        self.ln(6)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_draw_color(*COLOR_LIGHT_GRAY)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(2)
        self.set_font('Helvetica', '', 6.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 4, 'CafePulse Project OS AI  |  Youbellkey  |  Juni 2026  |  CONFIDENTIAL', align='L')
        self.set_xy(18, self.get_y())
        self.cell(0, 4, f'Halaman {self.page_no() - 1}', align='R')

    # ── Cover Page ────────────────────────────────────────────────────────────

    def add_cover(self):
        self.add_page()
        # Background
        self.set_fill_color(*COLOR_DARK)
        self.rect(0, 0, 210, 297, 'F')
        # Top bars
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 210, 8, 'F')
        self.set_fill_color(*COLOR_ACCENT)
        self.rect(0, 8, 210, 2, 'F')
        # Left accent
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 75, 6, 155, 'F')
        # Decorative circles (top right corner)
        self.set_fill_color(30, 60, 114)
        self.ellipse(145, 15, 80, 80, 'F')
        self.set_fill_color(*COLOR_DARK)
        self.ellipse(162, 32, 46, 46, 'F')

        # Brand name
        self.set_xy(20, 88)
        self.set_font('Helvetica', 'B', 48)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 18, 'CafePulse', align='L')

        # Subtitle label
        self.set_xy(20, 110)
        self.set_font('Helvetica', '', 10.5)
        self.set_text_color(*COLOR_ACCENT)
        self.cell(0, 6, 'PROJECT OS AI DOCUMENTATION SUITE', align='L')

        # Title block
        self.set_xy(20, 126)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*COLOR_WHITE)
        self.multi_cell(170, 9, 'Complete Project Documentation\nv1.0.0  --  Juni 2026', align='L')

        # Description box
        self.set_fill_color(30, 41, 59)
        self.set_draw_color(*COLOR_PRIMARY)
        self.set_line_width(0.4)
        self.rect(20, 160, 170, 58, 'FD')

        self.set_xy(28, 165)
        self.set_font('Helvetica', 'B', 8.5)
        self.set_text_color(*COLOR_ACCENT)
        self.cell(0, 5, 'DOKUMEN YANG TERCAKUP', align='L')

        self.set_xy(28, 173)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*COLOR_WHITE)
        docs_text = '  |  '.join(d[0] for d in DOCUMENTS)
        self.multi_cell(155, 5, sanitize(docs_text), align='L')

        self.set_xy(28, 207)
        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 5, '10 Dokumen Strategis  |  Local-First  |  MikroTik Operations Platform', align='L')

        # Divider
        self.set_draw_color(*COLOR_PRIMARY)
        self.set_line_width(0.5)
        self.line(20, 242, 190, 242)

        # Publisher line
        self.set_xy(20, 246)
        self.set_font('Helvetica', 'B', 8.5)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(90, 5, 'Youbellkey', align='L')
        self.set_xy(20, 246)
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 5, 'cafepulse.github.io  |  Confidential Internal Document', align='R')

        # Version badge
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(20, 254, 38, 8, 'F')
        self.set_xy(20, 255.5)
        self.set_font('Helvetica', 'B', 7)
        self.set_text_color(*COLOR_WHITE)
        self.cell(38, 5, 'VERSION 1.0.0', align='C')

        # Status badge
        self.set_fill_color(*COLOR_SUCCESS)
        self.rect(62, 254, 30, 8, 'F')
        self.set_xy(62, 255.5)
        self.cell(30, 5, 'LOCKED', align='C')

        # Bottom bars
        self.set_fill_color(*COLOR_ACCENT)
        self.rect(0, 287, 210, 2, 'F')
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 289, 210, 8, 'F')

    # ── Table of Contents ─────────────────────────────────────────────────────

    def add_toc(self):
        self.add_page()
        # Top accent
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 210, 3.5, 'F')

        self.set_xy(18, 14)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 10, 'Daftar Isi', align='L')

        self.set_xy(18, 26)
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 5, 'CafePulse Project OS AI Documentation Suite -- v1.0.0', align='L')

        self.set_draw_color(*COLOR_LIGHT_GRAY)
        self.line(18, 34, 192, 34)

        self.set_y(40)
        for i, (title, path, num) in enumerate(DOCUMENTS):
            y = self.get_y()
            # Alternating bg
            if i % 2 == 0:
                self.set_fill_color(*COLOR_ROW_ALT)
                self.rect(18, y, 174, 10, 'F')
            # Number badge
            self.set_fill_color(*COLOR_PRIMARY)
            self.rect(18, y + 1.5, 14, 7, 'F')
            self.set_xy(18, y + 2.5)
            self.set_font('Helvetica', 'B', 7)
            self.set_text_color(*COLOR_WHITE)
            self.cell(14, 5, num, align='C')
            # Title
            self.set_xy(36, y + 2.5)
            self.set_font('Helvetica', 'B', 9.5)
            self.set_text_color(*COLOR_TEXT_DARK)
            self.cell(120, 5, sanitize(title), align='L')
            # Dots
            self.set_xy(155, y + 2.5)
            self.set_font('Helvetica', '', 9)
            self.set_text_color(*COLOR_TEXT_LIGHT)
            self.cell(35, 5, '. . . . . . . .', align='R')
            self.ln(10)

        self.ln(8)
        self.set_draw_color(*COLOR_LIGHT_GRAY)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(5)
        self.set_font('Helvetica', 'I', 7.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.multi_cell(174, 4.5,
            'Dokumen ini berisi informasi strategis dan operasional yang bersifat RAHASIA. '
            'Tidak untuk disebarkan kepada pihak luar tanpa izin tertulis dari Youbellkey.',
            align='C')

    # ── Section Cover ─────────────────────────────────────────────────────────

    def add_section_cover(self, num: str, title: str, subtitle: str = ''):
        self.add_page()
        self._cur_section = f'{num}. {title}'
        # Dark header block
        self.set_fill_color(*COLOR_PANEL)
        self.rect(0, 0, 210, 78, 'F')
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 6, 78, 'F')
        # Big section number
        self.set_xy(18, 14)
        self.set_font('Helvetica', 'B', 44)
        self.set_text_color(50, 100, 200)
        self.cell(0, 18, f'{num}.', align='L')
        # Title
        self.set_xy(18, 40)
        self.set_font('Helvetica', 'B', 17)
        self.set_text_color(*COLOR_WHITE)
        self.cell(0, 9, sanitize(title.upper()), align='L')
        # Subtitle
        if subtitle:
            self.set_xy(18, 52)
            self.set_font('Helvetica', '', 9)
            self.set_text_color(*COLOR_ACCENT)
            self.cell(0, 5, sanitize(subtitle), align='L')
        # Meta
        self.set_xy(18, 65)
        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 5, 'CafePulse Project OS AI  |  v1.0.0  |  Juni 2026', align='L')
        self.set_y(88)

    # ── Heading ───────────────────────────────────────────────────────────────

    def heading(self, text: str, level: int):
        text = sanitize(text)
        self.ln(2)
        if level == 1:
            self.set_fill_color(*COLOR_PRIMARY)
            self.rect(18, self.get_y(), 4, 8, 'F')
            self.set_xy(25, self.get_y())
            self.set_font('Helvetica', 'B', 12.5)
            self.set_text_color(*COLOR_PRIMARY)
            self.cell(0, 8, text, align='L')
            self.ln(11)
        elif level == 2:
            self.set_xy(18, self.get_y())
            self.set_font('Helvetica', 'B', 10.5)
            self.set_text_color(*COLOR_TEXT_DARK)
            self.cell(0, 7, text, align='L')
            self.set_draw_color(*COLOR_LIGHT_GRAY)
            self.line(18, self.get_y(), 192, self.get_y())
            self.ln(8)
        elif level >= 3:
            self.set_xy(18, self.get_y())
            self.set_font('Helvetica', 'B', 9.5)
            self.set_text_color(*COLOR_ACCENT)
            self.cell(0, 6, '> ' + text, align='L')
            self.ln(7)

    # ── Paragraph ─────────────────────────────────────────────────────────────

    def para(self, text: str):
        text = sanitize(clean_md(text))
        if not text:
            return
        self.set_xy(18, self.get_y())
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*COLOR_TEXT_DARK)
        self.multi_cell(174, 4.5, text, align='L')
        self.ln(1.5)

    # ── List Item ─────────────────────────────────────────────────────────────

    def list_item(self, text: str, indent: int = 0, numbered: bool = False):
        text   = sanitize(clean_md(text))
        x_pos  = 20 + (indent * 5)
        width  = 172 - (indent * 5)
        bullet = '->' if numbered else '-'

        self.set_xy(x_pos, self.get_y())
        self.set_font('Helvetica', 'B', 7.5)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(5, 4.5, bullet, align='L')

        self.set_xy(x_pos + 5, self.get_y())
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*COLOR_TEXT_DARK)
        self.multi_cell(width - 5, 4.5, text, align='L')

    # ── Blockquote ────────────────────────────────────────────────────────────

    def blockquote(self, text: str):
        text = sanitize(clean_md(text))
        if not text:
            return
        self.set_font('Helvetica', 'I', 9)
        n_lines = max(1, len(text) // 68 + text.count('\n') + 1)
        h = n_lines * 5.5 + 8
        y0 = self.get_y()
        if y0 + h > 260:
            self.add_page()
            y0 = self.get_y()
        self.set_fill_color(*COLOR_QUOTE_BG)
        self.set_draw_color(*COLOR_PRIMARY)
        self.set_line_width(0.3)
        self.rect(18, y0, 174, h, 'FD')
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(18, y0, 4, h, 'F')
        self.set_xy(26, y0 + 4)
        self.set_font('Helvetica', 'I', 9.5)
        self.set_text_color(*COLOR_PRIMARY)
        self.multi_cell(160, 5.5, text, align='L')
        self.set_y(y0 + h + 3)
        self.set_text_color(*COLOR_TEXT_DARK)

    # ── Code Block ────────────────────────────────────────────────────────────

    def code_block(self, lines_list: list):
        if not lines_list:
            return
        self.ln(2)
        MAX  = 40
        show = lines_list[:MAX]
        h    = len(show) * 4.2 + 10
        y0   = self.get_y()
        if y0 + h > 262:
            self.add_page()
            y0 = self.get_y()
        self.set_fill_color(*COLOR_CODE_BG)
        self.rect(18, y0, 174, h, 'F')
        self.set_xy(22, y0 + 5)
        self.set_font('Courier', '', 6.5)
        self.set_text_color(*COLOR_CODE_FG)
        for raw in show:
            line = sanitize(raw)[:108]
            self.set_x(22)
            self.cell(170, 4.2, line, align='L')
            self.ln(4.2)
        self.set_text_color(*COLOR_TEXT_DARK)
        self.ln(4)

    # ── Table ─────────────────────────────────────────────────────────────────

    def table(self, rows: list):
        if not rows:
            return
        self.ln(2)
        header   = rows[0]
        data     = rows[1:]
        n_cols   = len(header)
        if n_cols == 0:
            return
        col_w    = 174.0 / n_cols
        MAX_CELL = max(12, int(34 / n_cols * 3))

        # Header
        self.set_fill_color(*COLOR_PANEL)
        self.set_text_color(*COLOR_WHITE)
        self.set_font('Helvetica', 'B', 7.5)
        for cell in header:
            self.cell(col_w, 6, sanitize(clean_md(cell))[:MAX_CELL+5], border=0, fill=True, align='C')
        self.ln()

        # Data rows
        for i, row in enumerate(data):
            if self.get_y() > 262:
                self.add_page()
            self.set_fill_color(*COLOR_ROW_ALT if i % 2 == 0 else COLOR_WHITE)
            self.set_text_color(*COLOR_TEXT_DARK)
            self.set_font('Helvetica', '', 7)
            for j in range(n_cols):
                cell_raw = row[j] if j < len(row) else ''
                self.cell(col_w, 5.5, sanitize(clean_md(cell_raw))[:MAX_CELL+8],
                          border=0, fill=True, align='L')
            self.ln()

        self.set_draw_color(*COLOR_LIGHT_GRAY)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(4)

    # ── Markdown File Renderer ────────────────────────────────────────────────

    def render_md(self, filepath: str):
        full_path = PROJECT_ROOT / filepath
        if not full_path.exists():
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(200, 50, 50)
            self.cell(0, 6, f'[FILE NOT FOUND: {filepath}]', align='L')
            self.ln(6)
            return

        content      = full_path.read_text(encoding='utf-8')
        lines        = content.splitlines()
        in_code      = False
        in_table     = False
        code_lines   = []
        table_rows   = []

        for raw in lines:
            line = raw.rstrip()

            # CODE BLOCK
            if line.startswith('```'):
                if in_code:
                    self.code_block(code_lines)
                    code_lines = []
                    in_code    = False
                else:
                    in_code = True
                continue
            if in_code:
                code_lines.append(line)
                continue

            # TABLE
            if line.startswith('|'):
                if not in_table:
                    in_table   = True
                    table_rows = []
                # Skip separator
                if re.match(r'^\|[-:\s|]+\|$', line):
                    continue
                cells = [c.strip() for c in line.split('|') if c.strip()]
                table_rows.append(cells)
                continue
            else:
                if in_table:
                    self.table(table_rows)
                    table_rows = []
                    in_table   = False

            # HEADINGS
            hm = re.match(r'^(#{1,4})\s+(.*)', line)
            if hm:
                lvl  = len(hm.group(1))
                text = clean_md(hm.group(2))
                if lvl == 1:
                    pass  # H1 already in section cover
                elif lvl <= 4:
                    self.heading(text, lvl - 1)
                continue

            # HORIZONTAL RULE
            if re.match(r'^-{3,}$', line) or re.match(r'^={3,}$', line):
                self.set_draw_color(*COLOR_LIGHT_GRAY)
                self.line(18, self.get_y(), 192, self.get_y())
                self.ln(4)
                continue

            # BLOCKQUOTE
            bq = re.match(r'^>\s?(.*)', line)
            if bq:
                self.blockquote(bq.group(1))
                continue

            # UNORDERED LIST
            li = re.match(r'^(\s*)[-*]\s+(.*)', line)
            if li:
                indent = len(li.group(1)) // 2
                self.list_item(li.group(2), indent=indent)
                continue

            # TASK LIST (checkbox)
            tl = re.match(r'^\s*-\s+\[[ xX/]\]\s+(.*)', line)
            if tl:
                self.list_item(tl.group(1), indent=0)
                continue

            # ORDERED LIST
            ol = re.match(r'^\s*\d+\.\s+(.*)', line)
            if ol:
                self.list_item(ol.group(1), numbered=True)
                continue

            # PARAGRAPH
            if line.strip():
                self.para(line)
            else:
                self.ln(2)

        # Flush remaining
        if in_table and table_rows:
            self.table(table_rows)
        if in_code and code_lines:
            self.code_block(code_lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def generate():
    sep = '=' * 60
    print(sep)
    print('  CafePulse -- Project OS AI PDF Generator')
    print(sep)

    pdf = CafePulsePDF()
    pdf.set_creator('CafePulse PDF Generator')
    pdf.set_author('Youbellkey')
    pdf.set_title('CafePulse Project OS AI Documentation Suite v1.0.0')
    pdf.set_subject('Complete Project Documentation - Local-First MikroTik Operations Platform')
    pdf.set_keywords('CafePulse, MikroTik, Network, Local-First, Indonesia, Project Bible')

    print('\n[1/3] Generating cover and table of contents...')
    pdf.add_cover()
    pdf.add_toc()

    print('[2/3] Rendering all documents...\n')
    for title, filepath, num in DOCUMENTS:
        subtitle = SECTION_SUBTITLES.get(num, '')
        print(f'  [{num}] {title}')
        pdf.add_section_cover(num, title, subtitle)
        pdf.render_md(filepath)

    print(f'\n[3/3] Saving PDF to: {OUTPUT_FILE.name}')
    pdf.output(str(OUTPUT_FILE))

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f'\n{sep}')
    print(f'  [OK] PDF berhasil dibuat!')
    print(f'  File : {OUTPUT_FILE.name}')
    print(f'  Ukuran: {size_mb:.2f} MB')
    print(f'  Dokumen: {len(DOCUMENTS)} bagian')
    print(sep)


if __name__ == '__main__':
    generate()
