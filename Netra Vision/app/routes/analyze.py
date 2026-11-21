from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image import (
    validate_image,
    resize_if_needed,
    encode_to_base64,
    save_image_to_disk
)
from app.services.vision import analyze_crop_image

router = APIRouter(prefix="/analyze", tags=["Crop Analysis"])


@router.post("")
async def analyze_single_image(file: UploadFile = File(...)):
    """
    Upload a single crop photo to detect diseases using Groq Free Vision AI.
    """
    contents = await file.read()
    metadata = validate_image(contents, file.content_type)
    processed_bytes, final_content_type = resize_if_needed(contents)
    file_path = save_image_to_disk(processed_bytes, file.filename)

    b64_str = encode_to_base64(processed_bytes)
    ai_diagnosis = analyze_crop_image(b64_str, final_content_type)

    return {
        "status": "success",
        "provider": "Groq Cloud AI (Free)",
        "filename": file.filename,
        "saved_path": file_path,
        "image_metadata": metadata,
        "diagnosis": ai_diagnosis
    }


@router.post("/batch")
async def analyze_batch_images(files: List[UploadFile] = File(...)):
    """
    Batch processing endpoint using Groq Vision API.
    """
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided.")

    results = []
    
    for file in files:
        try:
            contents = await file.read()
            metadata = validate_image(contents, file.content_type)
            processed_bytes, content_type = resize_if_needed(contents)
            saved_path = save_image_to_disk(processed_bytes, file.filename)
            b64_str = encode_to_base64(processed_bytes)
            diagnosis = analyze_crop_image(b64_str, content_type)

            results.append({
                "filename": file.filename,
                "status": "success",
                "saved_path": saved_path,
                "metadata": metadata,
                "diagnosis": diagnosis
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return {
        "status": "completed",
        "total_processed": len(files),
        "batch_results": results
    }