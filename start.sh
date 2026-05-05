#!/bin/bash
# ─── Eliran CRM Startup Script ───────────────────────────────────────────────
cd /a0/usr/projects/eliran

# Install deps in /opt/venv if missing
/opt/venv/bin/pip install flask pyairtable python-dotenv -q 2>/dev/null

# Kill any existing Flask instance
pkill -f 'python app.py' 2>/dev/null
sleep 1

# Start Flask using /opt/venv (project venv is on noexec volume)
nohup /opt/venv/bin/python app.py > /tmp/flask.log 2>&1 &
echo "Flask started (PID $!)"
echo "Access at: http://localhost:5000"
