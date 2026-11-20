from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("🚀 Database tables initialized.")
    yield
    print("🛑 Application shutting down.")

app = FastAPI(
    title="Dabbawala Tiffin Delivery API",
    description="Order status tracking & daily metrics engine",
    lifespan=lifespan
)

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to Dabbawala Order Tracking API"}

# Mount Router Modules
app.include_router(orders_router)
app.include_router(stats_router)