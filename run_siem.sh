#!/bin/bash

# Get the directory where this script is located
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[*] Starting Guardian SIEM System..."
echo "[*] Project Root: $PROJECT_ROOT"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"
touch "$PROJECT_ROOT/logs/test.log"

# Kill any existing SIEM processes
pkill -f "python3.*mini-siem" 2>/dev/null

# Start the Log Collector
echo "[*] Launching Log Collector..."
python3 "$PROJECT_ROOT/core/collector.py" > "$PROJECT_ROOT/logs/collector.log" 2>&1 &

# Start the Mock Log Generator
echo "[*] Launching Mock Log Generator..."
python3 "$PROJECT_ROOT/gen_logs.py" > "$PROJECT_ROOT/logs/gen_logs.log" 2>&1 &

# Start the Flask Dashboard
echo "[*] Launching Dashboard API..."
export FLASK_APP="$PROJECT_ROOT/app/app.py"
python3 -m flask run --port 5001 > "$PROJECT_ROOT/logs/app.log" 2>&1 &

echo ""
echo "===================================================="
echo "🛡️  Guardian SIEM is now running!"
echo "===================================================="
echo "Dashboard: http://127.0.0.1:5001"
echo "Logs:      $PROJECT_ROOT/logs/"
echo "===================================================="
echo "Press Ctrl+C to stop this script and kill processes."

# Wait for Ctrl+C
trap "echo '[*] Stopping SIEM...'; pkill -f 'python3.*mini-siem'; exit" INT
wait
