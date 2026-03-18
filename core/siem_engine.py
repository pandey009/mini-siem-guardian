import time
import json
from datetime import datetime, timedelta

class DetectionEngine:
    def __init__(self):
        # In-memory store for correlation (e.g., tracking failed logins by IP)
        self.state = {}
        # Simple security rules
        self.rules = [
            {
                'name': 'Brute Force Attempt',
                'type': 'auth_failed',
                'threshold': 3,
                'window_seconds': 60,
                'message': 'Multiple failed login attempts detected from IP: {ip}'
            },
            {
                'name': 'Suspicious Web Status',
                'type': 'web_access',
                'condition': lambda event: int(event.get('status', 0)) >= 400,
                'message': 'Client {ip} encountered error {status} on {path}'
            }
        ]

    def process_event(self, event):
        alerts = []
        if not event:
            return alerts

        ip = event.get('ip', 'unknown')
        event_type = event.get('type')

        # Check rules
        for rule in self.rules:
            if rule['type'] != event_type:
                continue

            # Check threshold-based rules (Correlation)
            if 'threshold' in rule:
                key = f"{rule['name']}:{ip}"
                now = datetime.now()
                
                if key not in self.state:
                    self.state[key] = []
                
                # Cleanup old events in window
                self.state[key] = [t for t in self.state[key] if now - t < timedelta(seconds=rule['window_seconds'])]
                self.state[key].append(now)

                if len(self.state[key]) >= rule['threshold']:
                    alerts.append({
                        'rule': rule['name'],
                        'severity': 'HIGH',
                        'message': rule['message'].format(**event),
                        'timestamp': now.isoformat(),
                        'ip': ip
                    })
            
            # Check simple condition-based rules
            elif 'condition' in rule:
                if rule['condition'](event):
                    alerts.append({
                        'rule': rule['name'],
                        'severity': 'MEDIUM',
                        'message': rule['message'].format(**event),
                        'timestamp': datetime.now().isoformat(),
                        'ip': ip
                    })

        return alerts

if __name__ == "__main__":
    engine = DetectionEngine()
    test_event = {'type': 'auth_failed', 'ip': '1.2.3.4', 'user': 'admin'}
    print(f"Processing event: {test_event}")
    for _ in range(3):
        print(engine.process_event(test_event))
