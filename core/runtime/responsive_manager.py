"""
CafePulse — Responsive Layout Manager
Unified coordinator tracking breakpoints and orchestrating adaptive adjustments across all pages.
"""

import logging
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger("cafepulse.core.responsive")

class ResponsiveManager(QObject):
    """
    Enterprise-grade global Responsive Layout Coordinator.
    Monitors window size updates, classifies breakpoints, and triggers layout adaptations.
    """
    breakpoint_changed = pyqtSignal(str) # Emits ("large" | "medium" | "small" | "compact" | "minimal")
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self._main_window = main_window
        self.current_breakpoint = "large"
        self._registered_tables = []
        self._registered_splitters = []
        
    def handle_resize(self, width: int, height: int) -> None:
        """
        Processes real-time window resizing.
        """
        # Determine breakpoint based on specifications
        if width >= 1600:
            bp = "large"
        elif width >= 1200:
            bp = "medium"
        elif width >= 900:
            bp = "small"
        elif width >= 700:
            bp = "compact"
        else:
            bp = "minimal"
            
        if bp != self.current_breakpoint:
            logger.info("Responsive Breakpoint Transition: %s -> %s (Width: %dpx)", self.current_breakpoint, bp, width)
            old_bp = self.current_breakpoint
            self.current_breakpoint = bp
            self.breakpoint_changed.emit(bp)
            self._apply_adaptations(bp, old_bp)
            
        self._apply_realtime_adjustments(width, height, bp)
        
    def register_table(self, table_widget, column_visibility_map: dict) -> None:
        """
        Registers a QTableWidget for adaptive column visibility.
        column_visibility_map format:
        {
            "large": [col_idx, ...],  # columns to show in large mode
            "medium": [col_idx, ...],
            "small": [col_idx, ...],
            "compact": [col_idx, ...],
            "minimal": [col_idx, ...]
        }
        """
        self._registered_tables.append((table_widget, column_visibility_map))
        # Apply current state instantly
        self._adapt_table(table_widget, column_visibility_map, self.current_breakpoint)
        
    def register_splitter(self, splitter, collapse_at_breakpoints: list) -> None:
        """
        Registers a QSplitter to automatically collapse its secondary pane (index 1)
        at specific breakpoints.
        """
        self._registered_splitters.append((splitter, collapse_at_breakpoints))
        self._adapt_splitter(splitter, collapse_at_breakpoints, self.current_breakpoint)

    def _apply_adaptations(self, bp: str, old_bp: str) -> None:
        # Adapt all registered tables
        for table, col_map in self._registered_tables:
            try:
                self._adapt_table(table, col_map, bp)
            except Exception as e:
                logger.error("Error adapting table column visibility: %s", e)
                
        # Adapt all registered splitters
        for splitter, collapse_bps in self._registered_splitters:
            try:
                self._adapt_splitter(splitter, collapse_bps, bp)
            except Exception as e:
                logger.error("Error adapting splitter: %s", e)
                
        # Trigger Main Window custom adaptations
        if hasattr(self._main_window, "_apply_responsive_state"):
            self._main_window._apply_responsive_state(bp)

    def _apply_realtime_adjustments(self, width: int, height: int, bp: str) -> None:
        # MainWindow specific drawer repositioning
        if hasattr(self._main_window, "_reposition_responsive_drawer"):
            self._main_window._reposition_responsive_drawer(width, height, bp)

    def _adapt_table(self, table, col_map: dict, bp: str) -> None:
        # Retrieve columns list that should be visible
        visible_cols = col_map.get(bp, col_map.get("large", []))
        total_cols = table.columnCount()
        for i in range(total_cols):
            should_hide = (i not in visible_cols)
            table.setColumnHidden(i, should_hide)

    def _adapt_splitter(self, splitter, collapse_bps: list, bp: str) -> None:
        if bp in collapse_bps:
            # Collapse index 1 (right details pane) completely by setting sizes to [left, 0]
            sizes = splitter.sizes()
            if len(sizes) >= 2 and sizes[1] > 0:
                splitter.setProperty("last_right_size", sizes[1])
                splitter.setSizes([sizes[0] + sizes[1], 0])
        else:
            # Restore size or set standard ratio
            sizes = splitter.sizes()
            if len(sizes) >= 2 and sizes[1] == 0:
                last_size = splitter.property("last_right_size") or 320
                splitter.setSizes([max(10, sizes[0] - last_size), last_size])
