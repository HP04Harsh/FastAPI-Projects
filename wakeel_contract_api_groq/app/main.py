from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routes.analysis import router as analysis_router
from app.routes.contracts import router as contracts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Wakeel - Legal Contract AI Analysis API (Groq Edition)",
    description="AI contract analysis using FREE Groq + Qwen3-32B. Fast, structured, reliable.",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(contracts_router)
app.include_router(analysis_router)


@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "service": "Wakeel Legal Tech API",
        "ai_provider": "Groq (qwen/qwen3-32b)",
        "documentation": "/docs"
    }