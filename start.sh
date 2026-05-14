#!/bin/bash
# ─── Eliran CRM Startup Script ───────────────────────────────────────────────
cd /a0/usr/projects/eliran || exit 1

# Install deps in /opt/venv if missing
/opt/venv/bin/pip install flask pyairtable python-dotenv requests -q 2>/dev/null

# Kill any existing stable/runtime instances
pkill -f '/opt/venv/bin/python run_stable.py' 2>/dev/null
pkill -f 'python run_stable.py' 2>/dev/null
sleep 1

# Start Flask using stable entrypoint and /opt/venv (project venv is on noexec volume)
nohup /opt/venv/bin/python run_stable.py > /tmp/flask.log 2>&1 &
echo "Flask started via run_stable.py (PID $!)"
echo "Access at: http://localhost:5000"
echo "Logs: /tmp/flask.log"
