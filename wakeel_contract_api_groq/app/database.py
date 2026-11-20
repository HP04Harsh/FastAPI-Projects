from pymongo import MongoClient
from app.config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

contracts_collection = db["contracts"]
analysis_collection = db["analysis"]


def init_db():
    """Create indexes for faster search."""
    try:
        contracts_collection.create_index("file_name", unique=True)
        analysis_collection.create_index("contract_id")
        print("✅ MongoDB Indexes Initialized Successfully.")
    except Exception as e:
        print(f"⚠️ Index Warning: {e}")