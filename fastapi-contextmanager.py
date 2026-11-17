from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app:FastAPI):
    # ---- STARTUP (yield se pehle) ----
    print("🚀 Application startup: DB connect, tables create...")
    # create_tables()  # jaise SQLModel me
    yield                       # ← server ab requests serve karta hai
    # ---- SHUTDOWN (yield ke baad) ----
    print("🛑 Application shutdown: DB close, cleanup...")
app = FastAPI(title="Dabbewala Delivery", lifespan=lifespan)   

@app.get("/")
def display():
    return {
        "Health is Okay"
    }
