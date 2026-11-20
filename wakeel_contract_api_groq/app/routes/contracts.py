import os
import uuid
from typing import List
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import ALLOWED_FILE_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_DIR
from app.database import contracts_collection
from app.models import ContractRead, ContractStatus
from app.services.document_parser import extract_text

router = APIRouter(prefix="/contracts", tags=["Contract Ingestion"])


@router.post("/upload", response_model=ContractRead, status_code=status.HTTP_201_CREATED)
async def upload_contract(file: UploadFile = File(...)):
    """Upload PDF/TXT contract, extract content, save metadata to MongoDB."""
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {ALLOWED_FILE_EXTENSIONS}"
        )

    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds {MAX_FILE_SIZE_MB} MB limit."
        )

    unique_file_name = f"{uuid.uuid4()}{ext}"
    saved_file_path = UPLOAD_DIR / unique_file_name

    with open(saved_file_path, "wb") as f:
        f.write(content)

    text_content, page_count, word_count = extract_text(str(saved_file_path))

    contract_doc = {
        "file_name": unique_file_name,
        "original_file_name": file.filename,
        "page_count": page_count,
        "word_count": word_count,
        "text_content": text_content,
        "status": ContractStatus.UPLOADED.value
    }

    result = contracts_collection.insert_one(contract_doc)

    return ContractRead(
        id=str(result.inserted_id),
        file_name=unique_file_name,
        original_file_name=file.filename,
        page_count=page_count,
        word_count=word_count,
        status=ContractStatus.UPLOADED
    )


@router.get("/list", response_model=List[ContractRead])
def list_contracts():
    """List all contracts (without raw text)."""
    contracts = []
    cursor = contracts_collection.find({}, {"text_content": 0})
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        contracts.append(ContractRead(**doc))
    return contracts


@router.get("/{contract_id}")
def get_contract_by_id(contract_id: str):
    """Get full contract by ID."""
    if not ObjectId.is_valid(contract_id):
        raise HTTPException(status_code=400, detail="Invalid contract ID format.")

    doc = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Contract not found.")

    doc["id"] = str(doc.pop("_id"))
    return doc