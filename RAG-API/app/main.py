from fastapi import FastAPI
from app.routes.query import router as query_router

app = FastAPI(
    title="RAG PDF Knowledgebase API",
    description="Retrieval Augmented Generation backend using LangChain, Qdrant Vector DB, and OpenAI.",
    version="1.0.0"
)

# Include Routers
app.include_router(query_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "active", "message": "RAG API service is up and running."}