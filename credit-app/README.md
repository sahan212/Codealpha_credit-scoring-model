# CrediShield AI - Full-Stack Creditworthiness Assessment System

CrediShield AI is an intelligent credit scoring and default risk underwriting platform built with **FastAPI**, **scikit-learn**, and a modern **FinTech web dashboard**.

---

## Folder Structure

```
credit-app/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI REST API & Static File Server
│   ├── model.py         # ML Pipeline, Auto-Training & Prediction Engine
│   └── schemas.py       # Pydantic Request/Response Data Validation
├── frontend/
│   ├── index.html       # Modern Dashboard UI (Tailwind CSS, FontAwesome)
│   └── app.js           # Client Logic, Fetch API & Real-time Underwriting
├── finance.csv          # Training Dataset (tab-separated)
├── requirements.txt     # Python Dependencies
└── run.sh               # One-click start script
```

---

## Quick Start (Run in 2 Steps)

### Step 1: Open Terminal in VS Code
Open the `credit-app` folder on your Desktop in VS Code or your terminal:
```bash
cd /Users/pranithreddy/Desktop/credit-app
```

### Step 2: Run the Application
You can run the startup script:
```bash
chmod +x run.sh
./run.sh
```

Or run manually:
```bash
pip install -r requirements.txt
python3 -m uvicorn backend.main:app --reload --port 8000
```

---

## Using the Dashboard
1. Open your browser and go to:
   ```
   http://127.0.0.1:8000
   ```
2. **Instant Testing**: Click **Low-Risk Preset** or **High-Risk Preset** to populate applicant details in one click.
3. Click **Evaluate Creditworthiness** to see:
   - Underwriting Verdict (`APPROVED` vs `REJECTED`)
   - Default Risk Probability gauge
   - Debt-to-Income (DTI) and Loan-to-Income (LTI) ratios
   - Key underwriting risk drivers

---

## Interactive API Documentation
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc UI: `http://127.0.0.1:8000/redoc`
