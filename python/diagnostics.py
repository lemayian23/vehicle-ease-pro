class VehicleDiagnostics:
    def __init__(self):
        self.alerts = []
        self.alert_history = []
        
    def check_alerts(self, data):
        current_alerts = []
        
        # Overheating alert
        if data['coolant'] > 105:
            current_alerts.append({
                'type': 'CRITICAL',
                'message': f'ENGINE OVERHEATING: {data["coolant"]}°C',
                'color': '#ff0000'
            })
        
        # High RPM warning
        if data['rpm'] > 6500:
            current_alerts.append({
                'type': 'WARNING', 
                'message': f'HIGH RPM: {data["rpm"]}',
                'color': '#ffaa00'
            })
        
        # Low coolant temp (cold engine)
        if data['coolant'] < 70 and data['rpm'] > 1500:
            current_alerts.append({
                'type': 'INFO',
                'message': 'Engine cold - avoid high RPM',
                'color': '#00aaff'
            })
            
        # Gear mismatch detection
        if data.get('gear') != 'N' and data['speed'] == 0 and data['rpm'] > 1200:
            current_alerts.append({
                'type': 'WARNING',
                'message': 'Vehicle stationary with high RPM',
                'color': '#ffaa00'
            })
        
        self.alerts = current_alerts
        if current_alerts:
            self.alert_history.extend(current_alerts)
            
        return current_alerts
    
    def get_health_score(self, data):
        score = 100
        
        # Deduct points for issues
        if data['coolant'] > 100: score -= 30
        if data['coolant'] > 90: score -= 10
        if data['rpm'] > 6000: score -= 15
        if data.get('gear') == 'N' and data['speed'] > 5: score -= 20
        
        return max(0, score)