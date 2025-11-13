import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import status, data, simulate, predict

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="UrbanPulse API",
    description="AI-Powered Sustainable City Twin API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preload ML model at startup
@app.on_event("startup")
async def startup_event():
    """Preload ML model on application startup"""
    try:
        from ml.model_loader import get_model
        model = get_model()
        print("✓ ML model loaded successfully")
    except FileNotFoundError:
        print("⚠ ML model not found. Train the model first using 'python backend/ml/train_model.py'")
    except Exception as e:
        print(f"⚠ Error loading ML model: {e}")

app.include_router(status.router, tags=["status"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(predict.router, prefix="/predict", tags=["prediction"])
app.include_router(simulate.router, tags=["simulation"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to UrbanPulse API",
        "docs": "/docs",
        "version": "1.0.0"
    }
