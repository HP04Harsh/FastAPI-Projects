from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    create_db_and_tables()
    print("🚀 Database tables created.")
    yield
    # --- Shutdown Logic ---
    print("🛑 Application shutting down.")

app = FastAPI(
    title="Rang Manch Review API",
    lifespan=lifespan
)

# Register Modular Routers
app.include_router(reviews_router)