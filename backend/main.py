from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import status, data, simulate

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

app.include_router(status.router, tags=["status"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(simulate.router, tags=["simulation"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to UrbanPulse API",
        "docs": "/docs",
        "version": "1.0.0"
    }
