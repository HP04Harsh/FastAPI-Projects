from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import analyze
from app.core.config import settings
import os

app = FastAPI(
    title="Netra Vision API (Groq Edition)",
    description="Free AI-powered crop disease detection using Groq Vision API.",
    version="1.0.0"
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(analyze.router)

@app.get("/")
async def root():
    return {
        "app": "Netra Vision API (Groq Free Edition)",
        "status": "running",
        "endpoints": ["/analyze", "/analyze/batch"]
    }