from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import analysis_collection, contracts_collection
from app.models import AnalysisResult, ContractStatus
from app.services.groq_analysis import run_groq_analysis   # ⭐ CHANGED IMPORT

router = APIRouter(prefix="/analysis", tags=["AI Contract Analysis (Groq)"])


@router.post("/{contract_id}", response_model=AnalysisResult, status_code=status.HTTP_200_OK)
def analyze_contract(contract_id: str):
    """Triggers Groq (Qwen3) AI analysis and saves insights to MongoDB."""
    if not ObjectId.is_valid(contract_id):
        raise HTTPException(status_code=400, detail="Invalid contract ID format.")

    # 1. Fetch Contract
    contract_doc = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not contract_doc:
        raise HTTPException(status_code=404, detail="Contract not found.")

    text_content = contract_doc.get("text_content", "")
    if not text_content:
        raise HTTPException(status_code=400, detail="Contract has no extractable text.")

    # 2. Status → IN_PROGRESS
    contracts_collection.update_one(
        {"_id": ObjectId(contract_id)},
        {"$set": {"status": ContractStatus.IN_PROGRESS.value}}
    )

    try:
        # 3. ⭐ Run Groq AI Pipeline (Gemini ki jagah)
        analysis_result = run_groq_analysis(
            contract_id=contract_id,
            contract_text=text_content
        )

        # 4. Save to MongoDB
        analysis_dict = analysis_result.model_dump()
        insert_result = analysis_collection.insert_one(analysis_dict)
        analysis_id = str(insert_result.inserted_id)

        # 5. Status → ANALYZED
        contracts_collection.update_one(
            {"_id": ObjectId(contract_id)},
            {"$set": {"status": ContractStatus.ANALYZED.value}}
        )

        analysis_result.id = analysis_id
        return analysis_result

    except Exception as e:
        contracts_collection.update_one(
            {"_id": ObjectId(contract_id)},
            {"$set": {"status": ContractStatus.FAILED.value}}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/all", response_model=List[AnalysisResult])
def list_all_analyses():
    reports = []
    for doc in analysis_collection.find():
        doc["id"] = str(doc.pop("_id"))
        reports.append(AnalysisResult(**doc))
    return reports


@router.get("/{analysis_id}", response_model=AnalysisResult)
def get_analysis_by_id(analysis_id: str):
    if not ObjectId.is_valid(analysis_id):
        raise HTTPException(status_code=400, detail="Invalid analysis ID format.")

    doc = analysis_collection.find_one({"_id": ObjectId(analysis_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Analysis report not found.")

    doc["id"] = str(doc.pop("_id"))
    return AnalysisResult(**doc)


@router.get("/contract/{contract_id}", response_model=List[AnalysisResult])
def get_analysis_by_contract_id(contract_id: str):
    reports = []
    for doc in analysis_collection.find({"contract_id": contract_id}):
        doc["id"] = str(doc.pop("_id"))
        reports.append(AnalysisResult(**doc))
    return reports