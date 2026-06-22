import os
import logging
from pathlib import Path
from PyQt6.QtGui import QPdfWriter, QPainter, QFont, QPen, QColor, QPageSize, QPageLayout
from PyQt6.QtCore import Qt, QMarginsF, QRectF, QPointF

logger = logging.getLogger("cafepulse.voucher.pdf")

class VoucherPDFGenerator:
    """
    Native PDF Generator for Hotspot Vouchers using PyQt6 QPdfWriter.
    Zero external dependencies (No ReportLab needed).
    Supports customizable sizes: Small, Medium, Large.
    Renders beautiful high-contrast vouchers with cutting guides.
    """
    
    @classmethod
    def generate_pdf(cls, output_path: str, vouchers: list[dict], size_mode: str = "medium") -> bool:
        """
        Generates a premium grid-based PDF of print-ready vouchers.
        vouchers: list of dict, e.g., [{"code": "CAFE-AB12", "profile": "1 Jam", "limit_uptime": "1h", "comment": "Budi"}]
        size_mode: 'small', 'medium', 'large'
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. Initialize QPdfWriter
            writer = QPdfWriter(str(output_file))
            writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            writer.setPageOrientation(QPageLayout.Orientation.Portrait)
            writer.setResolution(300) # 300 DPI High Resolution
            
            # Setup Layout Dimensions (A4 at 300 DPI is 2480 x 3508 pixels)
            # Safe printable area
            margin = 120 # 10mm margin at 300 DPI
            writer.setPageMargins(QMarginsF(margin, margin, margin, margin))
            
            painter = QPainter()
            if not painter.begin(writer):
                logger.error("Failed to begin painting on QPdfWriter.")
                return False
            
            # Define grid layout dimensions based on size_mode
            # A4 printable width: 2480 - 240 = 2240 pixels
            # A4 printable height: 3508 - 240 = 3268 pixels
            if size_mode == "small":
                cols = 4
                rows_per_page = 7
                v_width = 540
                v_height = 430
            elif size_mode == "large":
                cols = 2
                rows_per_page = 4
                v_width = 1100
                v_height = 780
            else: # "medium"
                cols = 3
                rows_per_page = 5
                v_width = 720
                v_height = 620
                
            x_spacing = 20
            y_spacing = 20
            
            # Fonts definition
            font_title = QFont("Segoe UI", 11, QFont.Weight.Bold)
            font_code = QFont("Consolas", 13, QFont.Weight.Bold)
            font_meta = QFont("Segoe UI", 8, QFont.Weight.Medium)
            
            curr_col = 0
            curr_row = 0
            
            for idx, voucher in enumerate(vouchers):
                if idx > 0 and curr_col == 0 and curr_row == 0:
                    # New Page
                    writer.newPage()
                    
                # Calculate coordinates
                x = curr_col * (v_width + x_spacing)
                y = curr_row * (v_height + y_spacing)
                
                # Render Single Voucher Card Box
                cls._draw_voucher_card(painter, x, y, v_width, v_height, voucher, font_title, font_code, font_meta)
                
                # Move Grid Pointer
                curr_col += 1
                if curr_col >= cols:
                    curr_col = 0
                    curr_row += 1
                    if curr_row >= rows_per_page:
                        curr_row = 0
                        
            painter.end()
            logger.info("Successfully generated PDF voucher sheets at %s", output_path)
            return True
        except Exception as e:
            logger.error("Failed to generate native PDF vouchers: %s", e)
            return False
            
    @classmethod
    def _draw_voucher_card(cls, painter: QPainter, x: int, y: int, w: int, h: int, 
                           voucher: dict, f_title: QFont, f_code: QFont, f_meta: QFont) -> None:
        """Helper to draw a single voucher card with high-contrast borders and text."""
        # 1. Outer Border QPen
        border_pen = QPen(QColor("#475569"))
        border_pen.setWidth(2)
        border_pen.setStyle(Qt.PenStyle.DashLine) # Dash line as cutting guide
        painter.setPen(border_pen)
        painter.setBrush(QColor("#F8FAFC")) # White/Light Gray background for print readability
        
        # Draw Voucher Boundary
        painter.drawRect(x, y, w, h)
        
        # 2. Draw Voucher Header Band
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#0F172A")) # Solid dark slate header band
        painter.drawRect(x + 2, y + 2, w - 4, 110)
        
        # Header Text
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(f_title)
        painter.drawText(QRectF(x + 10, y + 10, w - 20, 90), Qt.AlignmentFlag.AlignCenter, "CafePulse WiFi")
        
        # 3. Draw Voucher Code (Middle Section)
        painter.setPen(QColor("#0F172A")) # High contrast dark text for code
        painter.setFont(f_code)
        code_str = voucher.get("code", "VOUCHER-CODE")
        painter.drawText(QRectF(x + 10, y + 130, w - 20, 100), Qt.AlignmentFlag.AlignCenter, code_str)
        
        # 4. Draw Divider line
        divider_pen = QPen(QColor("#E2E8F0"))
        divider_pen.setWidth(1)
        painter.setPen(divider_pen)
        painter.drawLine(QPointF(x + 10, y + h - 110), QPointF(x + w - 10, y + h - 110))
        
        # 5. Draw Metadata Footer (Speed Limit / Profile)
        painter.setPen(QColor("#475569"))
        painter.setFont(f_meta)
        
        profile = voucher.get("profile", "Default")
        uptime = voucher.get("limit_uptime", "Unlimited")
        
        meta_str = f"Profil: {profile}  |  Durasi: {uptime}"
        painter.drawText(QRectF(x + 10, y + h - 90, w - 20, 80), Qt.AlignmentFlag.AlignCenter, meta_str)
