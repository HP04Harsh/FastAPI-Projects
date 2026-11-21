import io
import os
import uuid
import base64
from PIL import Image
from fastapi import HTTPException
from app.core.config import settings

def validate_image(content: bytes, content_type: str) -> dict:
    if content_type.lower() not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{content_type}'. Allowed: {settings.ALLOWED_IMAGE_TYPES}"
        )

    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size_mb:.2f}MB) exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB"
        )

    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
        img = Image.open(io.BytesIO(content))
        width, height = img.size
        return {
            "valid": True,
            "width": width,
            "height": height,
            "size_mb": round(size_mb, 2),
            "format": img.format
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Corrupted or invalid image file: {str(e)}"
        )


def resize_if_needed(content: bytes) -> tuple[bytes, str]:
    img = Image.open(io.BytesIO(content))
    width, height = img.size
    max_dim = settings.MAX_IMAGE_DIMENSION

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    if width > max_dim or height > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    output_buffer = io.BytesIO()
    img.save(output_buffer, format="JPEG", quality=85)
    resized_bytes = output_buffer.getvalue()
    
    return resized_bytes, "image/jpeg"


def encode_to_base64(content: bytes) -> str:
    return base64.b64encode(content).decode("utf-8")


def save_image_to_disk(content: bytes, original_filename: str) -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(original_filename)[1] or ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path