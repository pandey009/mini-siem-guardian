import os
import time
import sqlite3
from siem_parser import LogParser
from siem_engine import DetectionEngine

class Collector:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'siem.db')
        self.parser = LogParser()
        self.engine = DetectionEngine()
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                ip TEXT,
                message TEXT,
                raw TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                rule TEXT,
                severity TEXT,
                message TEXT,
                ip TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def store_event(self, event):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (timestamp, type, ip, message, raw)
            VALUES (?, ?, ?, ?, ?)
        ''', (event.get('parsed_at'), event.get('type'), event.get('ip'), event.get('message', event.get('raw')), event.get('raw')))
        conn.commit()
        conn.close()

    def store_alert(self, alert):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, rule, severity, message, ip)
            VALUES (?, ?, ?, ?, ?)
        ''', (alert['timestamp'], alert['rule'], alert['severity'], alert['message'], alert['ip']))
        conn.commit()
        conn.close()

    def tail_file(self, filename):
        print(f"[*] Starting tail on {filename}")
        # Ensure file exists
        if not os.path.exists(filename):
            open(filename, 'a').close()

        with open(filename, 'r') as f:
            # Go to the end of the file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                line = line.strip()
                if not line: continue

                # Try to parse with all known patterns
                event = None
                for ltype in self.parser.PATTERNS.keys():
                    event = self.parser.parse_line(line, ltype)
                    if event: break

                if event:
                    self.store_event(event)
                    # Detect
                    alerts = self.engine.process_event(event)
                    for alert in alerts:
                        print(f"[!] ALERT: {alert['rule']} - {alert['message']}")
                        self.store_alert(alert)

if __name__ == "__main__":
    # For testing, we'll monitor a local file
    collector = Collector()
    # Resolve project root (one level up from core/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(project_root, 'logs', 'test.log')
    collector.tail_file(log_file)
