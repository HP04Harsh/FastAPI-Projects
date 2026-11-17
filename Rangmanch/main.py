from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP ----
    create_db_and_tables()
    print("✅ Database tables created")
    yield
    # ---- SHUTDOWN ----
    print("🛑 Application shutdown")

app = FastAPI(
    title="Rangmanch Reviews API",
    description="Theatre reviews API for Pune's Rangmanch",
    lifespan=lifespan,
)
app.include_router(reviews_router)

@app.get("/")
def root():
    return {"message": "Welcome to Rangmanch Reviews API"}
