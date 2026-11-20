import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "RAG-AI")


def run_indexing(pdf_path: str):
    file_path = Path(pdf_path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF File not found at {pdf_path}")

    print(f"Loading PDF: {pdf_path}...")
    loader = PyPDFLoader(str(file_path))
    documents = loader.load()
    print(f"Loaded {len(documents)} document pages.")

    print("Splitting document into text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # 2. Embedding Model Setup
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 3. Ensure Collection Exists in Qdrant
    client = QdrantClient(url=QDRANT_URL)
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)

    if exists:
        collection = client.get_collection(collection_name=COLLECTION_NAME)
        vector_config = collection.config.params.vectors
        vector_size = getattr(vector_config, "size", None)
        if vector_size != 384:
            print(
                f"Recreating collection '{COLLECTION_NAME}' "
                f"with 384-dimensional vectors (current size: {vector_size})."
            )
            client.delete_collection(collection_name=COLLECTION_NAME)
            exists = False

    if not exists:
        print(f"Creating collection '{COLLECTION_NAME}' in Qdrant...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    # 4. Upsert vectors to Qdrant Vector DB
    print("Generating embeddings and upserting into Qdrant...")
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )
    print("Indexing completed successfully!")


if __name__ == "__main__":
    # Ensure sample PDF is in data directory
    sample_pdf_location = Path(__file__).parent.parent / "data" / "Sample.pdf"
    run_indexing(str(sample_pdf_location))