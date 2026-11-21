from fastapi import FastAPI
from app.routes.planner import router as planner_router
from app.routes.stream import router as stream_router

app = FastAPI(
    title="Yatra Planner API",
    description="Data aggregation engine with SSE streaming and in-memory TTL caching.",
    version="1.0.0"
)

# Register Routers
app.include_router(planner_router)
app.include_router(stream_router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "service": "Yatra Planner API Engine",
        "status": "online",
        "documentation": "/docs"
    }