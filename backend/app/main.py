from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import data, predict, simulate
from app.config import settings

app = FastAPI(
    title="UrbanPulse API",
    description="AI-Powered Sustainable City Twin",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(predict.router, prefix="/predict", tags=["predict"])
app.include_router(simulate.router, prefix="/simulate", tags=["simulate"])

@app.get("/")
async def root():
    return {
        "message": "UrbanPulse API - Sustainable City Twin",
        "demo_mode": settings.DEMO_MODE,
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
