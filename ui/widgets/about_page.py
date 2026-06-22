import os
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGridLayout, QPushButton
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap, QDesktopServices, QPainter, QPainterPath
from PyQt6.QtCore import QUrl
from core.licensing.licensing_manager import LicensingManager
from core.app_paths import LOGO_PATH, BRANDING_DIR
from core.utils.version import __version__

logger = logging.getLogger("cafepulse.ui.about")

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

class AboutPage(QWidget):
    """
    A commercial-grade, responsive About Page for CafePulse.
    Displays product version info, developer bio, development philosophy,
    dynamic licensing status, and official contacts with a premium card layout.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentArea")
        
        # Base layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Scroll Area for responsiveness on small screens
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(40, 40, 40, 40)
        self.scroll_layout.setSpacing(24)
        
        self._build_ui()
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        
        # Read the initial theme status if configured
        self.update_theme("dark")

    def get_circular_avatar(self, path: str, size: int) -> QPixmap:
        """Crops and scales a rectangular image to a perfect high-definition circle."""
        src = QPixmap(path)
        if src.isNull():
            return QPixmap()
            
        scaled = src.scaled(
            size, size, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        out = QPixmap(size, size)
        out.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(out)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path_clip = QPainterPath()
        path_clip.addEllipse(0, 0, size, size)
        painter.setClipPath(path_clip)
        
        offset_x = (size - scaled.width()) // 2
        offset_y = (size - scaled.height()) // 2
        painter.drawPixmap(offset_x, offset_y, scaled)
        painter.end()
        
        return out

    def _build_ui(self) -> None:
        # 1. HEADER SECTION (Logo, Title, Version)
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(8)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.logo_lbl = QLabel()
        logo_path = str(LOGO_PATH)
        if not os.path.exists(logo_path):
            logo_path = str(LOGO_PATH.parent.parent / "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            pixmap = crop_image_padding(pixmap)
            # Scale to 288x288 square keeping aspect ratio
            pixmap = pixmap.scaled(288, 288, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_lbl.setPixmap(pixmap)
        self.logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.logo_lbl)
        
        self.title_lbl = QLabel("CafePulse")
        self.title_lbl.setStyleSheet("font-size: 32px; font-weight: 800; color: #38BDF8;")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_lbl)
        
        self.version_lbl = QLabel(f"Version {__version__} — Offline-First Network Observability")
        self.version_lbl.setStyleSheet("font-size: 13px; color: #94A3B8; font-weight: 500;")
        self.version_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.version_lbl)
        
        self.scroll_layout.addWidget(header_container)

        # 2. PRODUCT OVERVIEW & VISION CARDS (Horizontal Split)
        overview_container = QWidget()
        overview_layout = QHBoxLayout(overview_container)
        overview_layout.setContentsMargins(0, 0, 0, 0)
        overview_layout.setSpacing(20)
        
        # Product Card
        self.prod_card = QFrame()
        self.prod_card.setObjectName("AboutCard")
        prod_layout = QVBoxLayout(self.prod_card)
        prod_layout.setContentsMargins(20, 20, 20, 20)
        prod_title = QLabel("About CafePulse")
        prod_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;")
        prod_text = QLabel(
            "CafePulse adalah platform operasi jaringan modern yang membantu teknisi, "
            "operator hotspot, dan pemilik usaha mengelola jaringan secara lebih sederhana, "
            "efisien, dan terukur. Memberikan visibilitas mendalam tanpa ketergantungan awan."
        )
        prod_text.setWordWrap(True)
        prod_text.setStyleSheet("font-size: 12px; line-height: 1.5; color: #94A3B8;")
        prod_layout.addWidget(prod_title)
        prod_layout.addWidget(prod_text)
        prod_layout.addStretch()
        overview_layout.addWidget(self.prod_card)
        
        # Vision Card
        self.vision_card = QFrame()
        self.vision_card.setObjectName("AboutCard")
        vision_layout = QVBoxLayout(self.vision_card)
        vision_layout.setContentsMargins(20, 20, 20, 20)
        vision_title = QLabel("Product Vision")
        vision_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;")
        vision_text = QLabel(
            "Menyederhanakan operasi jaringan tanpa mengorbankan kapabilitas profesional. "
            "Kami berkomitmen pada privasi data, efisiensi lokal, serta performa diagnostik real-time "
            "yang tangguh."
        )
        vision_text.setWordWrap(True)
        vision_text.setStyleSheet("font-size: 12px; line-height: 1.5; color: #94A3B8;")
        vision_layout.addWidget(vision_title)
        vision_layout.addWidget(vision_text)
        vision_layout.addStretch()
        overview_layout.addWidget(self.vision_card)
        
        self.scroll_layout.addWidget(overview_container)

        # 3. THE STORY BEHIND CAFEPULSE CARD
        self.story_card = QFrame()
        self.story_card.setObjectName("AboutCard")
        story_layout = QVBoxLayout(self.story_card)
        story_layout.setContentsMargins(20, 20, 20, 20)
        story_title = QLabel("The Story Behind CafePulse")
        story_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;")
        story_text = QLabel(
            "Dalam operasional jaringan nyata seperti cafe dan area hotspot publik, administrator "
            "sering kali dihadapkan pada kesulitan monitoring dan minimnya analitik tanpa infrastruktur "
            "cloud yang mahal. CafePulse dikembangkan untuk memberikan kemudahan penggunaan maksimal "
            "dengan menghubungkan langsung terminal diagnostik lokal ke interface API MikroTik, "
            "menjadikan monitoring jaringan lebih terjangkau, cepat, dan 100% luring."
        )
        story_text.setWordWrap(True)
        story_text.setStyleSheet("font-size: 12px; line-height: 1.5; color: #94A3B8;")
        story_layout.addWidget(story_title)
        story_layout.addWidget(story_text)
        self.scroll_layout.addWidget(self.story_card)

        # 4. FOUNDER PROFILE CARD
        self.founder_card = QFrame()
        self.founder_card.setObjectName("AboutCard")
        founder_layout = QHBoxLayout(self.founder_card)
        founder_layout.setContentsMargins(24, 24, 24, 24)
        founder_layout.setSpacing(24)
        
        # Circular Avatar Widget
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(120, 120)
        avatar_path = str(BRANDING_DIR / "founder_youbellkey.png")
        
        if os.path.exists(avatar_path):
            self.avatar_lbl.setPixmap(self.get_circular_avatar(avatar_path, 120))
        else:
            self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avatar_lbl.setText("YB")
            self.avatar_lbl.setStyleSheet("""
                font-size: 28px; 
                font-weight: bold; 
                color: #38BDF8; 
                background-color: #1E293B; 
                border-radius: 60px; 
                border: 2px solid #374151;
            """)
            
        avatar_layout = QVBoxLayout()
        avatar_layout.addWidget(self.avatar_lbl)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        founder_layout.addLayout(avatar_layout)
        
        # Bio details
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        f_badge = QLabel("FOUNDER")
        f_badge.setStyleSheet("""
            font-size: 9px; 
            font-weight: 800; 
            color: #38BDF8; 
            background-color: rgba(56, 189, 248, 0.12); 
            border: 1px solid rgba(56, 189, 248, 0.3); 
            border-radius: 4px; 
            padding: 2px 8px;
        """)
        f_badge.setSizePolicy(
            f_badge.sizePolicy().horizontalPolicy(), 
            f_badge.sizePolicy().verticalPolicy()
        )
        info_layout.addWidget(f_badge, alignment=Qt.AlignmentFlag.AlignLeft)
        
        f_name = QLabel("Youbellkey")
        f_name.setStyleSheet("font-size: 20px; font-weight: 800; color: #F8FAFC;")
        
        f_role = QLabel("Founder & Solo Developer")
        f_role.setStyleSheet("font-size: 13px; font-weight: 600; color: #94A3B8;")
        
        f_country = QLabel("🇮🇩  Indonesia")
        f_country.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748B;")
        
        f_bio = QLabel(
            "Yubelki Yosef Pusli (Youbellkey) adalah seorang independent software engineer "
            "asal Indonesia. Berdedikasi penuh untuk merancang aplikasi jaringan local-first "
            "dan luring yang tangguh, efisien, serta berorientasi pada kebutuhan operasional bisnis nyata."
        )
        f_bio.setWordWrap(True)
        f_bio.setStyleSheet("font-size: 12px; line-height: 1.5; color: #94A3B8; margin-top: 4px;")
        
        info_layout.addWidget(f_name)
        info_layout.addWidget(f_role)
        info_layout.addWidget(f_country)
        info_layout.addWidget(f_bio)
        
        founder_layout.addLayout(info_layout, stretch=1)
        self.scroll_layout.addWidget(self.founder_card)

        # 5. PHILOSOPHY GRID (6 items in 3x2 Grid)
        philosophy_container = QWidget()
        philosophy_layout = QVBoxLayout(philosophy_container)
        philosophy_layout.setContentsMargins(0, 0, 0, 0)
        philosophy_layout.setSpacing(10)
        
        phil_section_title = QLabel("Development Philosophy")
        phil_section_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #64748B; letter-spacing: 1px;")
        philosophy_layout.addWidget(phil_section_title)
        
        self.phil_grid_widget = QWidget()
        phil_grid = QGridLayout(self.phil_grid_widget)
        phil_grid.setContentsMargins(0, 0, 0, 0)
        phil_grid.setHorizontalSpacing(16)
        phil_grid.setVerticalSpacing(16)
        
        philosophies = [
            ("Local First", "Prioritas penyimpanan dan pengolahan data secara lokal di komputer admin."),
            ("Practical", "Fungsionalitas siap guna tanpa proses pendaftaran atau konfigurasi rumit."),
            ("Maintainable", "Arsitektur kode berbasis Python modular yang bersih dan mudah dirawat."),
            ("Business Oriented", "Membantu menekan biaya operasional dengan efisiensi pengelolaan akses."),
            ("Operator Friendly", "UI intuitif yang dirancang untuk operator lapangan maupun pemilik bisnis."),
            ("Offline First", "Dapat beroperasi sepenuhnya tanpa koneksi internet atau server luar.")
        ]
        
        self.phil_cards = []
        for index, (p_title, p_desc) in enumerate(philosophies):
            card = QFrame()
            card.setObjectName("PhilosophyCard")
            c_lay = QVBoxLayout(card)
            c_lay.setContentsMargins(16, 16, 16, 16)
            c_lay.setSpacing(6)
            
            ct = QLabel(f"●  {p_title}")
            ct.setStyleSheet("font-size: 13px; font-weight: 700; color: #38BDF8;")
            cd = QLabel(p_desc)
            cd.setWordWrap(True)
            cd.setStyleSheet("font-size: 11px; color: #94A3B8; line-height: 1.4;")
            
            c_lay.addWidget(ct)
            c_lay.addWidget(cd)
            
            row = index // 3
            col = index % 3
            phil_grid.addWidget(card, row, col)
            self.phil_cards.append(card)
            
        philosophy_layout.addWidget(self.phil_grid_widget)
        self.scroll_layout.addWidget(philosophy_container)

        # 6. SPLIT DETAILS SECTION (Tech Stack & Community & Developer)
        details_container = QWidget()
        details_layout = QHBoxLayout(details_container)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(20)
        
        # Tech Card
        self.tech_card = QFrame()
        self.tech_card.setObjectName("AboutCard")
        tech_lay = QVBoxLayout(self.tech_card)
        tech_lay.setContentsMargins(20, 20, 20, 20)
        tech_title = QLabel("Technology Stack")
        tech_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;")
        tech_lay.addWidget(tech_title)
        
        techs = [
            ("Core Logic", "Python 3.12+"),
            ("Interface", "PyQt6 (Qt 6.7.1)"),
            ("Local DB", "SQLite Database"),
            ("Router API", "MikroTik RouterOS API"),
            ("Supported OS", "Windows 10/11"),
            ("Planned OS", "Linux & macOS")
        ]
        for label, val in techs:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600;")
            value = QLabel(val)
            value.setStyleSheet("font-size: 11px; color: #E2E8F0; font-weight: bold;")
            value.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(lbl)
            row.addWidget(value)
            tech_lay.addLayout(row)
        tech_lay.addStretch()
        details_layout.addWidget(self.tech_card)

        # Developer & Community Card
        self.dev_card = QFrame()
        self.dev_card.setObjectName("AboutCard")
        dev_lay = QVBoxLayout(self.dev_card)
        dev_lay.setContentsMargins(20, 20, 20, 20)
        dev_title = QLabel("Developer & Community")
        dev_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;")
        dev_lay.addWidget(dev_title)
        
        dev_details = [
            ("Developer", "Founder & Solo Developer"),
            ("Country", "Indonesia"),
            ("Channels", "Discord Community"),
            ("Testing", "Beta Tester Program"),
            ("Early Program", "Founder Program"),
            ("Advisors", "Community Advisor Program")
        ]
        for label, val in dev_details:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600;")
            value = QLabel(val)
            value.setStyleSheet("font-size: 11px; color: #E2E8F0; font-weight: bold;")
            value.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(lbl)
            row.addWidget(value)
            dev_lay.addLayout(row)
        dev_lay.addStretch()
        details_layout.addWidget(self.dev_card)
        
        self.scroll_layout.addWidget(details_container)

        # 7. DYNAMIC SYSTEM METADATA & LICENSING (Professional View)
        self.license_card = QFrame()
        self.license_card.setObjectName("AboutCard")
        self.license_card.setStyleSheet("""
            QFrame#AboutCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0B0F19, stop:1 #171E2E);
                border: 1px solid #1E293B;
                border-left: 4px solid #38BDF8;
                border-radius: 8px;
            }
        """)
        lic_layout = QVBoxLayout(self.license_card)
        lic_layout.setContentsMargins(24, 24, 24, 24)
        lic_layout.setSpacing(12)
        
        lic_title = QLabel("License Verification & Software Metadata")
        lic_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #38BDF8;")
        lic_layout.addWidget(lic_title)
        
        # Metadata grids
        meta_layout = QGridLayout()
        meta_layout.setSpacing(10)
        
        # Read parameters from LicensingManager
        is_pro = LicensingManager.check_license()
        edition_str = "Professional Edition" if is_pro else "Free Edition"
        status_str = "Activated (Machine Entitled)" if is_pro else "Inactive (Evaluation Mode)"
        
        # Support end dates
        exp_txt = "N/A"
        info = LicensingManager.get_license_info()
        if is_pro and info.get("expires_at"):
            try:
                exp_dt = datetime.fromisoformat(info.get("expires_at"))
                exp_txt = exp_dt.strftime("%d %B %Y")
            except Exception:
                pass
        
        metadata_vals = [
            ("Application Version:", __version__, 0, 0),
            ("Build Number:", "Build #2026.06.02", 0, 1),
            ("Product Edition:", edition_str, 1, 0),
            ("License Status:", status_str, 1, 1),
            ("Update Entitlement Expiry:", exp_txt, 2, 0),
            ("Build Compile Date:", "June 2, 2026", 2, 1)
        ]
        
        for name, value, r, c in metadata_vals:
            cell = QHBoxLayout()
            n_lbl = QLabel(name)
            n_lbl.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600;")
            v_lbl = QLabel(value)
            v_lbl.setStyleSheet("font-size: 11px; color: #F1F5F9; font-weight: bold;")
            cell.addWidget(n_lbl)
            cell.addWidget(v_lbl)
            cell.addStretch()
            meta_layout.addLayout(cell, r, c)
            
        lic_layout.addLayout(meta_layout)
        
        # Horizontal divider
        div = QFrame()
        div.setStyleSheet("background-color: #1E293B; max-height: 1px; min-height: 1px; border: none; margin: 8px 0;")
        lic_layout.addWidget(div)
        
        # Dynamic detailed terms display
        terms_label = QLabel()
        terms_label.setWordWrap(True)
        if is_pro:
            terms_label.setText(
                "<b>PROFESSIONAL EDITION TERMS:</b> One-time purchase license. Active for 1 workstation (Machine ID Bound). "
                "Online & Offline activation supported. Includes 5-Year Update Entitlement. The Software remains fully "
                "functional after the update entitlement expires."
            )
            terms_label.setStyleSheet("font-size: 11px; color: #10B981; line-height: 1.4;")
        else:
            terms_label.setText(
                "<b>FREE EDITION TERMS:</b> Free for personal and commercial network diagnostics according to the standard license terms. "
                "Advanced MikroTik integrations, data backup scheduling, and white-labeled analytics require unlocking a Professional license key."
            )
            terms_label.setStyleSheet("font-size: 11px; color: #E2E8F0; line-height: 1.4;")
        lic_layout.addWidget(terms_label)
        
        # Source code and trademark disclaimers
        disclaimer_txt = QLabel(
            "<b>SOURCE CODE PROTECTION:</b> Redistribution of source code, compiled binaries, modified versions, "
            "or commercial repackaging is prohibited without prior written permission from CafePulse.<br/>"
            "<b>TRADEMARK NOTICE:</b> CafePulse name, branding, logos, icons, and visual identities are protected "
            "intellectual property of CafePulse. Unauthorized use is prohibited."
        )
        disclaimer_txt.setWordWrap(True)
        disclaimer_txt.setStyleSheet("font-size: 10px; color: #64748B; line-height: 1.4;")
        lic_layout.addWidget(disclaimer_txt)
        
        self.scroll_layout.addWidget(self.license_card)

        # 8. OFFICIAL CONTACT BUTTONS (Horizontal Row)
        contact_container = QWidget()
        contact_layout = QHBoxLayout(contact_container)
        contact_layout.setContentsMargins(0, 0, 0, 0)
        contact_layout.setSpacing(16)
        
        self.btn_web = QPushButton("🌐  Official Website")
        self.btn_web.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_web.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://cafepulse.com")))
        
        self.btn_email = QPushButton("✉️  Support Email")
        self.btn_email.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_email.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("mailto:support@cafepulse.com")))
        
        self.btn_discord = QPushButton("💬  Discord Community")
        self.btn_discord.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_discord.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://discord.gg/cafepulse")))
        
        self.btn_github = QPushButton("💻  GitHub Hub")
        self.btn_github.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/cafepulse")))
        
        contact_layout.addWidget(self.btn_web)
        contact_layout.addWidget(self.btn_email)
        contact_layout.addWidget(self.btn_discord)
        contact_layout.addWidget(self.btn_github)
        contact_layout.addStretch()
        
        self.scroll_layout.addWidget(contact_container)

        # 9. FOOTER COPYRIGHT SUMMARY
        self.footer = QLabel("Copyright (c) CafePulse. All rights reserved. CafePulse — Network Operations Platform. Copyright (c) 2026 CafePulse")
        self.footer.setStyleSheet("color: #475569; font-size: 11px;")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.footer)

    def update_theme(self, theme: str) -> None:
        """Style-match the page layout and components according to the selected theme."""
        if theme == "light":
            card_style = """
                QFrame#AboutCard {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                }
            """
            phil_card_style = """
                QFrame#PhilosophyCard {
                    background-color: #F1F5F9;
                    border: 1px solid #E2E8F0;
                    border-radius: 6px;
                }
            """
            btn_style = """
                QPushButton {
                    background-color: #F1F5F9;
                    color: #475569;
                    border: 1px solid #CBD5E1;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    color: #0284C7;
                    border-color: #0284C7;
                }
            """
            self.version_lbl.setStyleSheet("font-size: 13px; color: #475569; font-weight: 500;")
            self.footer.setStyleSheet("color: #64748B; font-size: 11px;")
        else:
            card_style = """
                QFrame#AboutCard {
                    background-color: #1E293B;
                    border: 1px solid #374151;
                    border-radius: 8px;
                }
            """
            phil_card_style = """
                QFrame#PhilosophyCard {
                    background-color: #111827;
                    border: 1px solid #1E293B;
                    border-radius: 6px;
                }
            """
            btn_style = """
                QPushButton {
                    background-color: #1E293B;
                    color: #CBD5E1;
                    border: 1px solid #374151;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #374151;
                    color: #38BDF8;
                    border-color: #38BDF8;
                }
            """
            self.version_lbl.setStyleSheet("font-size: 13px; color: #94A3B8; font-weight: 500;")
            self.footer.setStyleSheet("color: #475569; font-size: 11px;")

        # Apply styles to subcomponents
        self.prod_card.setStyleSheet(card_style)
        self.vision_card.setStyleSheet(card_style)
        self.story_card.setStyleSheet(card_style)
        self.tech_card.setStyleSheet(card_style)
        self.dev_card.setStyleSheet(card_style)
        self.founder_card.setStyleSheet(card_style)
        
        for card in self.phil_cards:
            card.setStyleSheet(phil_card_style)
            
        self.btn_web.setStyleSheet(btn_style)
        self.btn_email.setStyleSheet(btn_style)
        self.btn_discord.setStyleSheet(btn_style)
        self.btn_github.setStyleSheet(btn_style)
        
        # Distinct light styling for the license card to keep readable contrast
        if theme == "light":
            self.license_card.setStyleSheet("""
                QFrame#AboutCard {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F1F5F9, stop:1 #E2E8F0);
                    border: 1px solid #CBD5E1;
                    border-left: 4px solid #0284C7;
                    border-radius: 8px;
                }
            """)
        else:
            self.license_card.setStyleSheet("""
                QFrame#AboutCard {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0B0F19, stop:1 #171E2E);
                    border: 1px solid #1E293B;
                    border-left: 4px solid #38BDF8;
                    border-radius: 8px;
                }
            """)
