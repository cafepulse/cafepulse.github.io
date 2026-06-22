"""
CafePulse — Home WiFi Page Aliasing Wrapper
Maintains backward-compatibility by mapping HomeWifiPage imports to the new PersonalNetworkPage.
"""

from ui.widgets.personal_network_page import PersonalNetworkPage as HomeWifiPage, InfoRow
