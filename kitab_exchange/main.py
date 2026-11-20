from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from models import User, Book  # Trigger model relationship resolution
from routes.users import router as users_router
from routes.books import router as books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("🚀 Kitab Exchange DB initialized.")
    yield
    print("🛑 Shutting down Kitab Exchange application.")

app = FastAPI(
    title="Kitab Exchange API",
    description="DU Textbook buying/selling microservice backend",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Welcome to Kitab Exchange API"}

# Mount Modular Routers
app.include_router(users_router)
app.include_router(books_router)