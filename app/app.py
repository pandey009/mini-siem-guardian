from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core', 'siem.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    stats = {
        'total_events': conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],
        'total_alerts': conn.execute('SELECT COUNT(*) FROM alerts').fetchone()[0],
        'severity_counts': {
            'HIGH': conn.execute('SELECT COUNT(*) FROM alerts WHERE severity="HIGH"').fetchone()[0],
            'MEDIUM': conn.execute('SELECT COUNT(*) FROM alerts WHERE severity="MEDIUM"').fetchone()[0]
        },
        'top_ips': [dict(row) for row in conn.execute('SELECT ip, COUNT(*) as count FROM events GROUP BY ip ORDER BY count DESC LIMIT 5').fetchall()]
    }
    conn.close()
    return jsonify(stats)

@app.route('/api/alerts')
def get_alerts():
    conn = get_db_connection()
    alerts = [dict(row) for row in conn.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10').fetchall()]
    conn.close()
    return jsonify(alerts)

@app.route('/api/events')
def get_events():
    conn = get_db_connection()
    events = [dict(row) for row in conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT 20').fetchall()]
    conn.close()
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
