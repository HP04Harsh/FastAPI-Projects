import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
import groq

load_dotenv()

router = APIRouter(prefix="/query", tags=["RAG Search & Query"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "RAG-AI")

# Shared Groq Client and Hugging Face Embeddings
client = groq.Client(api_key=GROQ_API_KEY)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize Qdrant Store Connection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL
)


# Schemas
class QueryRequest(BaseModel):
    question: str = Field(..., example="What is network communication test?")


class SearchChunk(BaseModel):
    page: int
    content: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    referenced_pages: List[int]


@router.post("/", response_model=QueryResponse, status_code=status.HTTP_200_OK)
def query_rag_pipeline(payload: QueryRequest):
    """
    Retrieves top 3 matching chunks from Qdrant, synthesizes prompt context,
    and returns LLM response with exact page citations.
    """
    try:
        # 1. Similarity Search in Qdrant
        search_results = vector_db.similarity_search(payload.question, k=3)

        if not search_results:
            return QueryResponse(
                question=payload.question,
                answer="I don't know based on the provided document.",
                referenced_pages=[]
            )

        # 2. Extract context text and page numbers
        context_blocks = []
        referenced_pages = set()

        for doc in search_results:
            page_num = doc.metadata.get("page", 0) + 1  # 0-indexed to 1-indexed
            referenced_pages.add(page_num)
            context_blocks.append(f"[Page {page_num}]:\n{doc.page_content}")

        combined_context = "\n\n---\n\n".join(context_blocks)

        # 3. System Prompt Creation
        system_prompt = (
            "You are an AI assistant answering questions based strictly on the provided context.\n"
            "If the context does not contain the answer, reply with: 'I don't know based on the provided document.'\n"
            "Always reference exact page numbers where information is sourced.\n\n"
            f"Context:\n{combined_context}"
        )

        # 4. Generate LLM Answer
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload.question}
            ],
            temperature=0.2
        )

        llm_answer = completion.choices[0].message.content

        return QueryResponse(
            question=payload.question,
            answer=llm_answer,
            referenced_pages=sorted(list(referenced_pages))
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG search: {str(e)}"
        )