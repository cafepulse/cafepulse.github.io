import logging
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QMessageBox, QDialog, QLineEdit, QFormLayout,
    QFileDialog, QDialogButtonBox, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from core.licensing.licensing_manager import LicensingManager
from ui.widgets.toast_notification import ToastNotification

logger = logging.getLogger("cafepulse.ui.license")

_LICENSE_STYLE = """
QWidget {
    font-family: 'Segoe UI', -apple-system, sans-serif;
    color: #E2E8F0;
    background: transparent;
}
QLabel#SectionTitle {
    font-size: 15px;
    font-weight: 700;
    color: #38BDF8;
    background: transparent;
    padding-bottom: 2px;
}
QFrame#Divider {
    background: #1E293B;
    border: none;
    max-height: 1px;
    min-height: 1px;
}
QWidget#SectionCard {
    background: #1E293B;
    border: 1px solid #2D3748;
    border-radius: 10px;
}
QLabel#InfoLabel {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 500;
}
QLabel#ValueLabel {
    color: #F8FAFC;
    font-size: 12px;
    font-weight: 600;
}
QPushButton {
    background: #1E293B;
    color: #E2E8F0;
    border: 1px solid #2D3748;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton:hover {
    background: #2D3748;
    border-color: #38BDF8;
    color: #38BDF8;
}
QPushButton#PrimaryBtn {
    background: #38BDF8;
    color: #0F172A;
    border: none;
}
QPushButton#PrimaryBtn:hover {
    background: #7DD3FC;
}
QPushButton#DangerBtn {
    background: #2D1515;
    color: #FC8181;
    border: 1px solid #742A2A;
}
QPushButton#DangerBtn:hover {
    background: #E53E3E;
    color: white;
    border-color: #E53E3E;
}
"""

class LicensePage(QWidget):
    """
    License Management Center Page.
    Provides complete license status reporting, activation management (online/offline),
    leap-safe counting, and premium visual layout matching the cyber-dark theme.
    """
    
    # Emitted when license is successfully activated or deactivated to refresh global state
    license_changed = pyqtSignal(bool)

    def __init__(self, app_state=None, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self.setStyleSheet(_LICENSE_STYLE)
        self._build_ui()
        self.refresh_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        from PyQt6.QtWidgets import QScrollArea, QWidget
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        container.setObjectName("LicenseScrollContainer")
        container.setStyleSheet("background: transparent;")
        container.setMinimumWidth(450)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 12, 0)  # Right padding for scrollbar
        layout.setSpacing(20)

        # ─── HEADER ───────────────────────────────────────────────────────────
        header = QVBoxLayout()
        header.setSpacing(4)
        title = QLabel("License Management")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #F8FAFC; background: transparent;")
        subtitle = QLabel("Verify machine entitlements, offline activations, and future update privileges.")
        subtitle.setStyleSheet("font-size: 11px; color: #64748B; background: transparent;")
        subtitle.setWordWrap(True)
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # ─── 1. LICENSE HEALTH CARD ──────────────────────────────────────────
        self.health_frame = QFrame()
        self.health_frame.setObjectName("SectionCard")
        self.health_frame.setStyleSheet("""
            QFrame#SectionCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #111827, stop:1 #1E293B);
                border: 1px solid #2D3748;
                border-left: 4px solid #38BDF8;
                border-radius: 8px;
            }
        """)
        health_layout = QHBoxLayout(self.health_frame)
        health_layout.setContentsMargins(20, 16, 20, 16)
        
        self.health_glow = QLabel("🔒")
        self.health_glow.setStyleSheet("font-size: 32px; background: transparent;")
        health_layout.addWidget(self.health_glow)
        health_layout.addSpacing(10)

        health_details = QVBoxLayout()
        health_details.setSpacing(4)
        self.health_status_lbl = QLabel("STATUS: NOT ACTIVATED")
        self.health_status_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #EF4444; background: transparent;")
        self.health_countdown_lbl = QLabel("Masa Dukungan Update: -")
        self.health_countdown_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; background: transparent;")
        self.health_countdown_lbl.setWordWrap(True)
        self.health_action_lbl = QLabel("Next Action: Activate Professional License")
        self.health_action_lbl.setStyleSheet("font-size: 10px; color: #38BDF8; font-weight: 600; background: transparent;")
        self.health_action_lbl.setWordWrap(True)
        health_details.addWidget(self.health_status_lbl)
        health_details.addWidget(self.health_countdown_lbl)
        health_details.addWidget(self.health_action_lbl)
        health_layout.addLayout(health_details)
        health_layout.addStretch()

        layout.addWidget(self.health_frame)

        # ─── 2. LICENSE INFORMATION ───────────────────────────────────────────
        info_section = QVBoxLayout()
        info_section.setSpacing(10)
        
        info_title = QLabel("Informasi Lisensi")
        info_title.setObjectName("SectionTitle")
        info_section.addWidget(info_title)

        info_div = QFrame()
        info_div.setObjectName("Divider")
        info_section.addWidget(info_div)

        self.info_frame = QFrame()
        self.info_frame.setObjectName("SectionCard")
        info_grid = QFormLayout(self.info_frame)
        info_grid.setContentsMargins(18, 16, 18, 16)
        info_grid.setVerticalSpacing(12)
        info_grid.setHorizontalSpacing(30)
        info_grid.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Build labels
        self.val_type = QLabel("CafePulse Professional")
        self.val_type.setObjectName("ValueLabel")
        
        # License key layout (with mask and copy)
        key_row = QHBoxLayout()
        key_row.setSpacing(8)
        self.val_key = QLabel("NOT_ACTIVATED")
        self.val_key.setObjectName("ValueLabel")
        self.btn_copy_inline = QPushButton("Salin")
        self.btn_copy_inline.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_inline.setFixedSize(60, 24)
        self.btn_copy_inline.setStyleSheet("font-size: 10px; padding: 2px;")
        self.btn_copy_inline.clicked.connect(self._copy_key)
        key_row.addWidget(self.val_key)
        key_row.addWidget(self.btn_copy_inline)
        key_row.addStretch()

        self.val_status = QLabel("Inactive")
        self.val_status.setObjectName("ValueLabel")
        self.val_status.setStyleSheet("color: #EF4444; font-weight: bold;")
        
        self.val_activated = QLabel("-")
        self.val_activated.setObjectName("ValueLabel")
        
        self.val_expires = QLabel("-")
        self.val_expires.setObjectName("ValueLabel")
        
        self.val_days = QLabel("-")
        self.val_days.setObjectName("ValueLabel")
        
        self.val_eligibility = QLabel("Updates No Longer Available")
        self.val_eligibility.setObjectName("ValueLabel")
        self.val_eligibility.setStyleSheet("color: #E2E8F0;")
        
        self.val_dev_name = QLabel("-")
        self.val_dev_name.setObjectName("ValueLabel")
        
        self.val_dev_os = QLabel("-")
        self.val_dev_os.setObjectName("ValueLabel")
        
        self.val_dev_hwid = QLabel("-")
        self.val_dev_hwid.setObjectName("ValueLabel")
        self.val_dev_hwid.setStyleSheet("color: #38BDF8; font-family: monospace; font-size: 11px;")

        self.val_owner = QLabel("-")
        self.val_owner.setObjectName("ValueLabel")
        
        self.val_founder_id = QLabel("-")
        self.val_founder_id.setObjectName("ValueLabel")
        
        self.val_beta_cohort = QLabel("-")
        self.val_beta_cohort.setObjectName("ValueLabel")

        # Add to form
        def create_info_lbl(text):
            lbl = QLabel(text)
            lbl.setObjectName("InfoLabel")
            return lbl

        info_grid.addRow(create_info_lbl("Owner:"), self.val_owner)
        info_grid.addRow(create_info_lbl("Tipe Lisensi:"), self.val_type)
        info_grid.addRow(create_info_lbl("Founder ID:"), self.val_founder_id)
        info_grid.addRow(create_info_lbl("Beta Cohort:"), self.val_beta_cohort)
        info_grid.addRow(create_info_lbl("Serial Key:"), key_row)
        info_grid.addRow(create_info_lbl("Status:"), self.val_status)
        info_grid.addRow(create_info_lbl("Tanggal Aktivasi:"), self.val_activated)
        info_grid.addRow(create_info_lbl("Entitlement Expire:"), self.val_expires)
        info_grid.addRow(create_info_lbl("Sisa Hari Update:"), self.val_days)
        info_grid.addRow(create_info_lbl("Update Eligibility:"), self.val_eligibility)
        info_grid.addRow(create_info_lbl("Activated Device:"), self.val_dev_name)
        info_grid.addRow(create_info_lbl("Device OS:"), self.val_dev_os)
        info_grid.addRow(create_info_lbl("Hardware ID:"), self.val_dev_hwid)

        info_section.addWidget(self.info_frame)
        layout.addLayout(info_section)

        # ─── 3. ACTIVATION MANAGEMENT ────────────────────────────────────────
        mgmt_section = QVBoxLayout()
        mgmt_section.setSpacing(10)
        
        mgmt_title = QLabel("Activation Management")
        mgmt_title.setObjectName("SectionTitle")
        mgmt_section.addWidget(mgmt_title)

        mgmt_div = QFrame()
        mgmt_div.setObjectName("Divider")
        mgmt_section.addWidget(mgmt_div)

        mgmt_btns = QHBoxLayout()
        mgmt_btns.setSpacing(12)
        
        self.btn_offline_imp = QPushButton("Import License File (.lic)")
        self.btn_offline_imp.setObjectName("PrimaryBtn")
        self.btn_offline_imp.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_offline_imp.clicked.connect(self._on_offline_import_clicked)

        self.btn_offline_req = QPushButton("Generate License Request")
        self.btn_offline_req.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_offline_req.clicked.connect(self._on_offline_req_clicked)

        self.btn_activate = QPushButton("Manual Activation (Legacy)")
        self.btn_activate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_activate.clicked.connect(self._on_activate_clicked)

        self.btn_deactivate = QPushButton("Deactivate License")
        self.btn_deactivate.setObjectName("DangerBtn")
        self.btn_deactivate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_deactivate.clicked.connect(self._on_deactivate_clicked)

        mgmt_btns.addWidget(self.btn_offline_imp)
        mgmt_btns.addWidget(self.btn_offline_req)
        mgmt_btns.addWidget(self.btn_activate)
        mgmt_btns.addWidget(self.btn_deactivate)
        mgmt_btns.addStretch()
        mgmt_section.addLayout(mgmt_btns)
        layout.addLayout(mgmt_section)

        # ─── 4. ACTIONS ───────────────────────────────────────────────────────
        act_section = QVBoxLayout()
        act_section.setSpacing(10)
        
        act_title = QLabel("License Actions")
        act_title.setObjectName("SectionTitle")
        act_section.addWidget(act_title)

        act_div = QFrame()
        act_div.setObjectName("Divider")
        act_section.addWidget(act_div)

        act_btns = QHBoxLayout()
        act_btns.setSpacing(12)

        self.btn_refresh = QPushButton("🔄  Refresh License")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_ui)

        self.btn_check = QPushButton("🔍  Check License Status")
        self.btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check.clicked.connect(self._on_check_status_clicked)

        self.btn_copy_key = QPushButton("📋  Copy License Key")
        self.btn_copy_key.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_key.clicked.connect(self._copy_key)

        act_btns.addWidget(self.btn_refresh)
        act_btns.addWidget(self.btn_check)
        act_btns.addWidget(self.btn_copy_key)
        act_btns.addStretch()
        act_section.addLayout(act_btns)
        layout.addLayout(act_section)

        # ─── 5. UPDATE INFORMATION SECTION ──────────────────────────────────
        update_section = QVBoxLayout()
        update_section.setSpacing(10)
        
        update_title = QLabel("Update Information")
        update_title.setObjectName("SectionTitle")
        update_section.addWidget(update_title)

        update_div = QFrame()
        update_div.setObjectName("Divider")
        update_section.addWidget(update_div)

        self.update_card = QFrame()
        self.update_card.setObjectName("SectionCard")
        self.update_card.setStyleSheet("""
            QFrame#SectionCard {
                background: #111827;
                border: 1px solid #1E293B;
                border-left: 3px solid #64748B;
                border-radius: 8px;
            }
        """)
        card_l = QVBoxLayout(self.update_card)
        card_l.setContentsMargins(16, 14, 16, 14)
        card_l.setSpacing(6)

        self.val_update_status = QLabel("Update Support Status: -")
        self.val_update_status.setStyleSheet("font-size: 13px; font-weight: 700; color: #E2E8F0; background: transparent;")
        self.val_update_status.setWordWrap(True)
        
        msg_lbl1 = QLabel("Your software will continue to work after update support expires.")
        msg_lbl1.setStyleSheet("font-size: 11px; color: #94A3B8; background: transparent;")
        msg_lbl1.setWordWrap(True)
        
        msg_lbl2 = QLabel("Only future updates will require renewal.")
        msg_lbl2.setStyleSheet("font-size: 11px; color: #64748B; background: transparent;")
        msg_lbl2.setWordWrap(True)

        card_l.addWidget(self.val_update_status)
        card_l.addWidget(msg_lbl1)
        card_l.addWidget(msg_lbl2)

        update_section.addWidget(self.update_card)
        layout.addLayout(update_section)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def refresh_ui(self):
        """Reloads license files and repopulates all text fields dynamically."""
        is_pro = LicensingManager.check_license()
        info = LicensingManager.get_license_info()
        health_status, countdown, action = LicensingManager.get_license_health()

        # Update summary card
        self.health_countdown_lbl.setText(f"Masa Dukungan Update: {countdown}")
        self.health_action_lbl.setText(f"Next Action: {action}")

        if not is_pro:
            self.health_frame.setStyleSheet("""
                QFrame#SectionCard {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2A1010, stop:1 #1E293B);
                    border: 1px solid #742A2A;
                    border-left: 4px solid #EF4444;
                    border-radius: 8px;
                }
            """)
            self.health_glow.setText("🔒")
            self.health_status_lbl.setText(f"STATUS: {health_status.upper()}")
            self.health_status_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #EF4444; background: transparent;")
            
            self.val_key.setText("NOT_ACTIVATED")
            self.val_type.setText("CafePulse Free Edition")
            self.val_type.setStyleSheet("color: #94A3B8; font-weight: bold;")
            self.val_status.setText(health_status)
            self.val_status.setStyleSheet("color: #EF4444; font-weight: bold;")
            self.val_activated.setText("-")
            self.val_expires.setText("-")
            self.val_days.setText("-")
            self.val_eligibility.setText("Updates No Longer Available")
            self.val_eligibility.setStyleSheet("color: #EF4444; font-weight: bold;")
            
            self.val_dev_name.setText(LicensingManager.get_device_name())
            self.val_dev_os.setText(LicensingManager.get_os_info())
            self.val_dev_hwid.setText(LicensingManager.get_hwid())
            
            self.val_owner.setText("-")
            self.val_founder_id.setText("-")
            self.val_beta_cohort.setText("-")
            
            self.val_update_status.setText("Update Support: Not Active")
            self.update_card.setStyleSheet("QFrame#SectionCard { background: #111827; border: 1px solid #1E293B; border-left: 3px solid #EF4444; border-radius: 8px; }")
            
            self.btn_deactivate.setEnabled(False)
            self.btn_copy_inline.setEnabled(False)
            self.btn_copy_key.setEnabled(False)
        else:
            is_eligible = LicensingManager.is_eligible_for_updates()
            key_raw = info.get("license_key", "")
            # Mask Key: e.g. CP-PRO-OWNER-XXXX
            masked = key_raw
            if len(key_raw) > 8:
                masked = f"{key_raw[:7]}-XXXX-XXXX-{key_raw[-4:]}" if "-" in key_raw else f"{key_raw[:6]}XXXX{key_raw[-4:]}"

            # Format Dates
            act_date = "-"
            exp_date = "-"
            days_rem = "0 Hari"
            
            try:
                act_dt = datetime.fromisoformat(info.get("activated_at", ""))
                act_date = act_dt.strftime("%d %B %Y, %H:%M WIB")
            except Exception:
                pass
                
            try:
                exp_dt = datetime.fromisoformat(info.get("expires_at", ""))
                exp_date = exp_dt.strftime("%d %B %Y, %H:%M WIB")
                
                # Sisa Hari
                delta = exp_dt - datetime.now()
                if delta.days > 0:
                    days_rem = f"{delta.days} Hari"
                else:
                    days_rem = "Update Entitlement Expired"
            except Exception:
                pass

            if is_eligible:
                self.health_frame.setStyleSheet("""
                    QFrame#SectionCard {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #062015, stop:1 #1E293B);
                        border: 1px solid #10B981;
                        border-left: 4px solid #10B981;
                        border-radius: 8px;
                    }
                """)
                self.health_glow.setText("🛡️")
                self.health_status_lbl.setText("STATUS: ACTIVE")
                self.health_status_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #10B981; background: transparent;")
                
                self.val_status.setText("Active")
                self.val_status.setStyleSheet("color: #10B981; font-weight: bold;")
                self.val_eligibility.setText("Eligible for Updates")
                self.val_eligibility.setStyleSheet("color: #10B981; font-weight: bold;")
                
                self.val_update_status.setText(f"Update Support Active (Until: {exp_dt.strftime('%d %B %Y')})")
                self.update_card.setStyleSheet("QFrame#SectionCard { background: #111827; border: 1px solid #1E293B; border-left: 3px solid #10B981; border-radius: 8px; }")
            else:
                lic_type = info.get("license_type", "professional").upper()
                if lic_type == "BETA" or lic_type == "BETA_EXPIRED":
                    self.health_frame.setStyleSheet("""
                        QFrame#SectionCard {
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2D1A0A, stop:1 #1E293B);
                            border: 1px solid #EF4444;
                            border-left: 4px solid #EF4444;
                            border-radius: 8px;
                        }
                    """)
                    self.health_glow.setText("⚠️")
                    self.health_status_lbl.setText("STATUS: BETA EXPIRED")
                    self.health_status_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #EF4444; background: transparent;")
                    
                    self.val_status.setText("Beta Expired")
                    self.val_status.setStyleSheet("color: #EF4444; font-weight: bold;")
                    self.val_eligibility.setText("App Locked")
                    self.val_eligibility.setStyleSheet("color: #EF4444; font-weight: bold;")
                    
                    self.val_update_status.setText(f"Beta Period Ended ({exp_date})")
                    self.update_card.setStyleSheet("QFrame#SectionCard { background: #111827; border: 1px solid #1E293B; border-left: 3px solid #EF4444; border-radius: 8px; }")
                else:
                    self.health_frame.setStyleSheet("""
                        QFrame#SectionCard {
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2D1A0A, stop:1 #1E293B);
                            border: 1px solid #D97706;
                            border-left: 4px solid #D97706;
                            border-radius: 8px;
                        }
                    """)
                    self.health_glow.setText("⚠️")
                    self.health_status_lbl.setText("STATUS: EXPIRED UPDATE ENTITLEMENT")
                    self.health_status_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #F59E0B; background: transparent;")
                    
                    self.val_status.setText("Expired Update Entitlement")
                    self.val_status.setStyleSheet("color: #F59E0B; font-weight: bold;")
                    self.val_eligibility.setText("Updates No Longer Available")
                    self.val_eligibility.setStyleSheet("color: #F59E0B; font-weight: bold;")
                    
                    self.val_update_status.setText(f"Update Support Expired ({exp_date})")
                    self.update_card.setStyleSheet("QFrame#SectionCard { background: #111827; border: 1px solid #1E293B; border-left: 3px solid #F59E0B; border-radius: 8px; }")

            # Edition Styling
            lic_type = info.get("license_type", "professional").upper()
            self.val_owner.setText(info.get("owner", "-"))
            
            if lic_type == "FOUNDER":
                self.val_type.setText(f"{info.get('edition', 'PROFESSIONAL')} - FOUNDER EDITION")
                self.val_type.setStyleSheet("color: #FBBF24; font-weight: bold;")
                self.val_founder_id.setText(info.get("founder_id", "-"))
                self.val_founder_id.setStyleSheet("color: #FBBF24; font-weight: bold;")
                self.val_beta_cohort.setText("-")
                self.val_beta_cohort.setStyleSheet("color: #E2E8F0;")
            elif lic_type == "BETA" or lic_type == "BETA_EXPIRED":
                self.val_type.setText(f"{info.get('edition', 'PROFESSIONAL')} - BETA TESTER")
                self.val_type.setStyleSheet("color: #F97316; font-weight: bold;")
                self.val_beta_cohort.setText(info.get("beta_cohort", "-"))
                self.val_beta_cohort.setStyleSheet("color: #F97316; font-weight: bold;")
                self.val_founder_id.setText("-")
                self.val_founder_id.setStyleSheet("color: #E2E8F0;")
            else:
                self.val_type.setText(f"{info.get('edition', 'PROFESSIONAL')} - COMMERCIAL")
                self.val_type.setStyleSheet("color: #38BDF8; font-weight: bold;")
                self.val_founder_id.setText("-")
                self.val_founder_id.setStyleSheet("color: #E2E8F0;")
                self.val_beta_cohort.setText("-")
                self.val_beta_cohort.setStyleSheet("color: #E2E8F0;")

            # Base info
            self.val_key.setText(masked)
            self.val_activated.setText(act_date)
            self.val_expires.setText(exp_date)
            self.val_days.setText(days_rem)
            
            # Display current or bound info
            self.val_dev_name.setText(info.get("device_name", LicensingManager.get_device_name()))
            self.val_dev_os.setText(info.get("os", LicensingManager.get_os_info()))
            self.val_dev_hwid.setText(info.get("hwid", LicensingManager.get_hwid()))
            
            self.btn_deactivate.setEnabled(True)
            self.btn_copy_inline.setEnabled(True)
            self.btn_copy_key.setEnabled(True)

    def _copy_key(self):
        """Copies masked or unmasked license key safely to clipboard."""
        info = LicensingManager.get_license_info()
        key = info.get("license_key")
        if key:
            clipboard = QApplication.clipboard()
            clipboard.setText(key)
            ToastNotification.show_toast(self, "📋  Serial Key berhasil disalin ke clipboard!", 2500)
        else:
            QMessageBox.warning(self, "Gagal", "Tidak ada serial key aktif yang dapat disalin.")

    def _on_check_status_clicked(self):
        """Performs mock status check and displays elegant notification."""
        is_pro = LicensingManager.check_license()
        if is_pro:
            is_eligible = LicensingManager.is_eligible_for_updates()
            status_desc = "Eligible for all future updates!" if is_eligible else "Software fully valid, updates ended."
            ToastNotification.show_toast(self, f"🔍  Lisensi Valid! {status_desc}", 3000)
        else:
            ToastNotification.show_toast(self, "❌  Lisensi Tidak Ditemukan / Belum Aktif.", 3000)

    # ─── ACTIVATION DIALOGS & SLOTS ──────────────────────────────────────────

    def _on_activate_clicked(self):
        """Shows popup dialog for direct activation."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Aktivasi Lisensi CafePulse")
        dlg.setFixedWidth(400)
        dlg.setStyleSheet("QDialog { background: #0F172A; } QLabel { color: #E2E8F0; }")
        
        vlayout = QVBoxLayout(dlg)
        vlayout.setContentsMargins(24, 24, 24, 24)
        vlayout.setSpacing(16)
        
        title = QLabel("Aktivasi Lisensi CafePulse")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #38BDF8;")
        vlayout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        edit_owner = QLineEdit()
        edit_owner.setPlaceholderText("Nama Pemilik Lisensi")
        edit_owner.setStyleSheet("background: #1E293B; color: #E2E8F0; border: 1px solid #4A5568; border-radius: 5px; padding: 6px;")
        
        edit_key = QLineEdit()
        edit_key.setPlaceholderText("CP-PRO-XXXX-XXXX-XXXX")
        edit_key.setStyleSheet("background: #1E293B; color: #E2E8F0; border: 1px solid #4A5568; border-radius: 5px; padding: 6px;")
        
        form.addRow("Nama Pemilik:", edit_owner)
        form.addRow("Serial Key:", edit_key)
        vlayout.addLayout(form)
        
        err_lbl = QLabel("")
        err_lbl.setStyleSheet("color: #EF4444; font-size: 11px;")
        vlayout.addWidget(err_lbl)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self._proc_direct_activate(dlg, edit_owner.text(), edit_key.text(), err_lbl))
        buttons.rejected.connect(dlg.reject)
        buttons.setStyleSheet("QPushButton { background: #1E293B; color: #E2E8F0; border: 1px solid #2D3748; padding: 6px 16px; border-radius: 6px; } QPushButton:hover { border-color: #38BDF8; }")
        vlayout.addWidget(buttons)
        
        dlg.exec()

    def _proc_direct_activate(self, dlg, owner, key, err_lbl):
        owner = owner.strip()
        key = key.strip().upper()
        if not owner or not key:
            err_lbl.setText("⚠ Kolom input tidak boleh kosong!")
            return
            
        success = LicensingManager.activate_license(raw_key=key, owner_name=owner)
        if success:
            dlg.accept()
            self.refresh_ui()
            self.license_changed.emit(True)
            if self.app_state:
                self.app_state.check_license_status()
            QMessageBox.information(self, "Aktivasi Sukses", "Lisensi CafePulse Professional berhasil diaktifkan pada mesin ini!")
        else:
            err_lbl.setText("⚠ Kode Lisensi tidak cocok atau format salah.")

    def _on_deactivate_clicked(self):
        """Shows danger warning and deletes license."""
        reply = QMessageBox.question(
            self, "Deaktivasi Lisensi",
            "Apakah Anda yakin ingin men-deaktivasi lisensi Pro pada komputer ini?\n\n"
            "Aplikasi akan kembali ke edisi Free Edition dan membatasi akses modifikasi.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            LicensingManager.deactivate()
            self.refresh_ui()
            self.license_changed.emit(False)
            if self.app_state:
                self.app_state.check_license_status()
            ToastNotification.show_toast(self, "🔓  Lisensi berhasil dinonaktifkan dari perangkat ini.", 3000)

    def _on_offline_req_clicked(self):
        """Generates *.licreq offline activation file."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Generate License Request (.licreq)")
        dlg.setFixedWidth(400)
        dlg.setStyleSheet("QDialog { background: #0F172A; } QLabel { color: #E2E8F0; }")
        
        vlayout = QVBoxLayout(dlg)
        vlayout.setContentsMargins(24, 24, 24, 24)
        vlayout.setSpacing(16)
        
        title = QLabel("Generate License Request (.licreq)")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #38BDF8;")
        vlayout.addWidget(title)
        
        info = QLabel("Request file ini mengikat kode lisensi dengan Hardware ID PC Anda saat ini, agar dapat ditukarkan luring.")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 11px; color: #94A3B8;")
        vlayout.addWidget(info)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        edit_owner = QLineEdit()
        edit_owner.setPlaceholderText("Nama Pemilik")
        edit_owner.setStyleSheet("background: #1E293B; color: #E2E8F0; border: 1px solid #4A5568; border-radius: 5px; padding: 6px;")
        
        edit_email = QLineEdit()
        edit_email.setPlaceholderText("Email (Opsional)")
        edit_email.setStyleSheet("background: #1E293B; color: #E2E8F0; border: 1px solid #4A5568; border-radius: 5px; padding: 6px;")
        
        form.addRow("Nama Pemilik:", edit_owner)
        form.addRow("Email:", edit_email)
        vlayout.addLayout(form)
        
        err_lbl = QLabel("")
        err_lbl.setStyleSheet("color: #EF4444; font-size: 11px;")
        vlayout.addWidget(err_lbl)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self._proc_offline_req(dlg, edit_owner.text(), edit_email.text(), err_lbl))
        buttons.rejected.connect(dlg.reject)
        buttons.setStyleSheet("QPushButton { background: #1E293B; color: #E2E8F0; border: 1px solid #2D3748; padding: 6px 16px; border-radius: 6px; } QPushButton:hover { border-color: #38BDF8; }")
        vlayout.addWidget(buttons)
        
        dlg.exec()

    def _proc_offline_req(self, dlg, owner, email, err_lbl):
        owner = owner.strip()
        email = email.strip()
        if not owner:
            err_lbl.setText("⚠ Nama pemilik tidak boleh kosong!")
            return
            
        try:
            req_content = LicensingManager.generate_activation_request(owner, email)
            
            # Open File dialog to save
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Offline Request File",
                os.path.join(os.path.expanduser("~"), f"CP_Activation_{owner.replace(' ', '_')}.licreq"),
                "License Request Files (*.licreq)"
            )
            
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(req_content)
                dlg.accept()
                QMessageBox.information(
                    self, "Request File Dibuat",
                    f"File request berhasil disimpan di:\n{file_path}\n\n"
                    "Kirimkan file ini ke Founder CafePulse atau upload di Portal Pelanggan untuk ditukar dengan berkas aktivasi (.lic)."
                )
        except ValueError as ve:
            err_lbl.setText(f"⚠ {ve}")
        except Exception as e:
            err_lbl.setText(f"⚠ Gagal membuat file request: {e}")

    def _on_offline_import_clicked(self):
        """Imports an activation file *.lic."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File Aktivasi CafePulse (.lic)",
            os.path.expanduser("~"),
            "License Files (*.lic)"
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                success = LicensingManager.import_activation_file(content)
                if success:
                    self.refresh_ui()
                    self.license_changed.emit(True)
                    if self.app_state:
                        self.app_state.check_license_status()
                    QMessageBox.information(self, "Aktivasi Luring Sukses", "File lisensi Pro luring berhasil diimpor! CafePulse Professional telah diaktifkan di PC ini.")
                else:
                    QMessageBox.critical(self, "Aktivasi Gagal", "File lisensi tidak valid atau tidak cocok dengan Hardware ID PC ini!")
            except Exception as e:
                QMessageBox.critical(self, "Aktivasi Gagal", f"Gagal membaca file lisensi:\n{e}")
