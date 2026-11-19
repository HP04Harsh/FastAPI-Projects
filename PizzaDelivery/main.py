from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.order import router as order_router

# Lifespan context manager for application startup and shutdown hooks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    create_tables()
    print("🚀 Database tables created successfully.")
    yield
    # --- Shutdown ---
    print("🛑 Shutting down Rang Munch API application.")

app = FastAPI(
    title="Pizza Stock API",
    description="Pizza Stock API for Harsh cafe",
    lifespan=lifespan
)

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to harsh cafe"}

# Include modular route definitions
app.include_router(order_router)