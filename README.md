# Guardian Mini SIEM

A lightweight Security Information and Event Management (SIEM) system built with Python, Flask, and JavaScript.

## Features
- **Real-time Log Monitoring**: Tails log files to detect security events.
- **Regex-based Parser**: Parses `syslog`, `auth_failed`, and `web_access` events.
- **Rule Engine**: Correlates events to detect threats like SSH Brute Force and Web Probing.
- **Premium Dashboard**: Glassmorphic UI with Chart.js visualization for real-time alerts.

## Getting Started

1. Ensure you have Python 3 installed.
2. Install required packages (Flask is required) if you haven't already:
```bash
pip install flask
```
3. Run the complete stack (Collector, Generator, Dashboard):
```bash
./run_siem.sh
```
4. Open your browser and navigate to `http://127.0.0.1:5001`.

## Architecture
- **Backend**: Flask API (`app.py`), SQLite Database (`siem.db`), Collector (`collector.py`), Rule Engine (`siem_engine.py`), and Parser (`siem_parser.py`).
- **Frontend**: HTML5/CSS3 Dashboard with vanilla JS (`dashboard.js`) and Chart.js.
- **Testing**: Includes a mock log generator (`gen_logs.py`) to simulate attacks.
