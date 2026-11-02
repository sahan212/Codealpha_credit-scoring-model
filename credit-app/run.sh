#!/usr/bin/env bash
cd "$(dirname "$0")"

echo "=================================================="
echo " Starting CrediShield AI Full Stack Platform      "
echo "=================================================="

# Check Python and uvicorn
python3 -m pip install -q -r requirements.txt

echo "[✓] Dependencies installed."
echo "[+] Launching FastAPI Server on http://127.0.0.1:8000"
echo "=================================================="

python3 -m uvicorn backend.main:app --reload --port 8000
