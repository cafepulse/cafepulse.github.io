"""
CafePulse — Network DNA Radar Widget
A premium, custom polar radar chart drawing the 5 dimensions of network health using QPainter.
Highly optimized, high-aesthetic, cyber-clean design with glowing translucent polygons.
"""

import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygonF, QFont, QBrush
from PyQt6.QtCore import Qt, QPointF, QTimer


class NetworkDNARadar(QWidget):
    """
    Custom polar radar chart representing the network fingerprint.
    Dimensions:
    1. Latency (Ping Stability)
    2. Load (Bandwidth Utilization)
    3. Congestion (Packet Loss / Collision)
    4. Devices (Network Load Density)
    5. System (CPU/RAM Strain on Router)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(260, 260)
        self.setSizePolicy(self.sizePolicy().Policy.Expanding, self.sizePolicy().Policy.Expanding)
        
        # Default metric scores (0.0 to 1.0)
        self._latency = 0.9
        self._load = 0.8
        self._congestion = 0.95
        self._devices = 0.85
        self._system = 0.9
        
        # Animation targets and steps
        self._target_values = [0.9, 0.8, 0.95, 0.85, 0.9]
        self._current_values = [0.5, 0.5, 0.5, 0.5, 0.5]
        
        # Setup animation timer for smooth micro-transitions
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(30)
        self._anim_timer.timeout.connect(self._animate_step)
        self._anim_timer.start()

    def set_metrics(self, latency: float, load: float, congestion: float, devices: float, system: float) -> None:
        """
        Set target metric scores (0.0 - 1.0) for the 5 axes.
        Smoothly animates towards the target values.
        """
        self._target_values = [
            max(0.0, min(1.0, latency)),
            max(0.0, min(1.0, load)),
            max(0.0, min(1.0, congestion)),
            max(0.0, min(1.0, devices)),
            max(0.0, min(1.0, system))
        ]

    def _animate_step(self) -> None:
        changed = False
        for i in range(5):
            diff = self._target_values[i] - self._current_values[i]
            if abs(diff) > 0.01:
                self._current_values[i] += diff * 0.15  # Smooth interpolation factor
                changed = True
            else:
                self._current_values[i] = self._target_values[i]
                
        if changed:
            self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        cx = width / 2.0
        cy = height / 2.0
        
        # Radar layout constants
        padding = 35
        max_radius = min(cx, cy) - padding
        if max_radius < 50:
            return
            
        # 5 Axes Names
        labels = ["Latency", "Load", "Congestion", "Devices", "System"]
        
        # Draw concentric polygon grids (5 layers for 20%, 40%, 60%, 80%, 100%)
        grid_color = QColor(30, 41, 59, 120)  # Dark cyber slate
        painter.setPen(QPen(grid_color, 1, Qt.PenStyle.SolidLine))
        
        for layer in range(1, 6):
            r = max_radius * (layer / 5.0)
            poly = QPolygonF()
            for i in range(5):
                angle = -math.pi / 2.0 + i * (2 * math.pi / 5.0)
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                poly.append(QPointF(px, py))
            
            # Draw grid pentagon
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPolygon(poly)
            
            # Subtle grid concentric text labels
            if layer in (3, 5):
                painter.setPen(QPen(QColor(71, 85, 105, 100), 1))
                painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Medium))
                # Put it on the top axis
                painter.drawText(int(cx + 4), int(cy - r + 3), f"{layer*20}%")
                painter.setPen(QPen(grid_color, 1))

        # Draw spoke axes radiating from center
        for i in range(5):
            angle = -math.pi / 2.0 + i * (2 * math.pi / 5.0)
            px = cx + max_radius * math.cos(angle)
            py = cy + max_radius * math.sin(angle)
            
            # Draw spoke line
            painter.setPen(QPen(QColor(30, 41, 59, 160), 1, Qt.PenStyle.DashLine))
            painter.drawLine(QPointF(cx, cy), QPointF(px, py))
            
            # Draw axis text labels
            label_dist = max_radius + 15
            lx = cx + label_dist * math.cos(angle)
            ly = cy + label_dist * math.sin(angle)
            
            painter.setPen(QPen(QColor(148, 163, 184), 1))  # Cool grey text
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            
            # Adjust label alignment depending on quadrant
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(labels[i])
            th = fm.height()
            
            adj_x = lx - (tw / 2.0)
            adj_y = ly + (th / 3.0)
            
            # Micro adjustments for perfect polar alignment
            if abs(lx - cx) < 5:  # Top
                adj_y = ly - 2
            elif lx < cx:  # Left quadrant
                adj_x = lx - tw + 5
            else:  # Right quadrant
                adj_x = lx - 5
                
            painter.drawText(int(adj_x), int(adj_y), labels[i])

        # ─── Draw the DNA Shape (Translucent Filled Polygon) ──────────────────
        dna_poly = QPolygonF()
        for i in range(5):
            angle = -math.pi / 2.0 + i * (2 * math.pi / 5.0)
            score = self._current_values[i]
            r = max_radius * score
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            dna_poly.append(QPointF(px, py))

        # Fill DNA polygon (Translucent glowing cyan/blue)
        fill_color = QColor(56, 189, 248, 40)  # #38BDF8 with 15% opacity
        painter.setBrush(QBrush(fill_color))
        
        # Border pen (Vibrant neon cyan)
        border_color = QColor(56, 189, 248, 220)  # Glowing cyan
        painter.setPen(QPen(border_color, 2, Qt.PenStyle.SolidLine))
        painter.drawPolygon(dna_poly)

        # Draw glowing vertex nodes
        painter.setBrush(QBrush(QColor(14, 165, 233)))  # Deep cyan
        painter.setPen(QPen(QColor(248, 250, 252), 1.5))  # White outline
        for i in range(5):
            angle = -math.pi / 2.0 + i * (2 * math.pi / 5.0)
            score = self._current_values[i]
            r = max_radius * score
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            painter.drawEllipse(QPointF(px, py), 4.5, 4.5)
            
        # Draw center hub
        painter.setBrush(QBrush(QColor(30, 41, 59)))
        painter.setPen(QPen(QColor(71, 85, 105), 1))
        painter.drawEllipse(QPointF(cx, cy), 5, 5)
