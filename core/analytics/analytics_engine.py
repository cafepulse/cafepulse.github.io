import logging
import time

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    def __init__(self, max_bandwidth_mbps=50, max_users=100):
        self.max_bandwidth_mbps = max_bandwidth_mbps
        self.max_users = max_users
        self.bandwidth_history = []
        self.reconnect_counts = {}
        
    def calculate_health_score(self, current_bandwidth_mbps, active_users, error_rate=0.0):
        score = 100
        bw_utilization = current_bandwidth_mbps / max(self.max_bandwidth_mbps, 1)
        if bw_utilization > 0.8:
            score -= (bw_utilization - 0.8) * 100
        user_load = active_users / max(self.max_users, 1)
        if user_load > 0.9:
            score -= 10
        score -= min(error_rate * 50, 40)
        return max(0, min(100, int(score)))

    def estimate_congestion(self, current_bandwidth_mbps, active_users):
        bw_load = (current_bandwidth_mbps / max(self.max_bandwidth_mbps, 1)) * 100
        user_load = (active_users / max(self.max_users, 1)) * 100
        congestion_pct = max(bw_load, user_load)
        
        if congestion_pct >= 90:
            return 'Severe', congestion_pct
        elif congestion_pct >= 75:
            return 'High', congestion_pct
        elif congestion_pct >= 50:
            return 'Moderate', congestion_pct
        else:
            return 'Low', congestion_pct

    def analyze_reconnects(self, mac_address):
        now = time.time()
        if mac_address not in self.reconnect_counts:
            self.reconnect_counts[mac_address] = []
        
        self.reconnect_counts[mac_address].append(now)
        self.reconnect_counts[mac_address] = [t for t in self.reconnect_counts[mac_address] if now - t < 3600]
        
        count = len(self.reconnect_counts[mac_address])
        if count >= 5:
            return 'This device reconnects unusually often ({} times in the last hour).'.format(count)
        return None

    def update_bandwidth_trend(self, current_mbps):
        self.bandwidth_history.append(current_mbps)
        if len(self.bandwidth_history) > 10:
            self.bandwidth_history.pop(0)
            
        if len(self.bandwidth_history) < 2:
            return 'Stable'
            
        avg_recent = sum(self.bandwidth_history[-3:]) / 3
        avg_older = sum(self.bandwidth_history[:3]) / max(1, min(3, len(self.bandwidth_history[:3])))
        
        if avg_recent > avg_older * 1.2:
            return 'Increasing'
        elif avg_recent < avg_older * 0.8:
            return 'Decreasing'
        return 'Stable'

    def generate_insights(self, health_score, congestion_level, active_users):
        insights = []
        if health_score < 70:
            insights.append('Network health is degrading. Check connection stability.')
        if congestion_level in ('High', 'Severe'):
            insights.append('Network congestion likely caused by high simultaneous activity.')
        if active_users > self.max_users * 0.9:
            insights.append('Approaching maximum user capacity.')
        return insights

    def generate_basic_insights(self, active_users: int, new_devices_count: int, missing_devices_count: int) -> list[str]:
        """Generate topology-based insights without relying on bandwidth."""
        insights = []
        if active_users > self.max_users * 0.9:
            insights.append('Approaching maximum network capacity based on active MAC addresses.')
            
        if new_devices_count >= 5:
            insights.append('Sudden burst of new devices detected. Possible MAC spoofing or intrusion scan.')
            
        if missing_devices_count >= 5:
            insights.append('Multiple devices abruptly dropped off. Check Access Point stability.')
            
        return insights