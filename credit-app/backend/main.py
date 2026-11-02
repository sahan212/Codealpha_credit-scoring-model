import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from .schemas import ApplicantInput, AssessmentResponse
    from .model import get_or_train_model, predict_applicant
except ImportError:
    from schemas import ApplicantInput, AssessmentResponse
    from model import get_or_train_model, predict_applicant

app = FastAPI(
    title="CrediShield AI - Credit Assessment API",
    description="Intelligent Creditworthiness and Default Risk Assessment Engine",
    version="1.0.0"
)

# Allow Cross-Origin Requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def startup_event():
    global model
    model = get_or_train_model()

@app.post("/api/assess", response_model=AssessmentResponse)
def assess_credit(applicant: ApplicantInput):
    result = predict_applicant(applicant.dict(), model)
    return result

@app.get("/api/health")
def health():
    return {"status": "online", "model_loaded": model is not None}

# Mount Frontend static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
