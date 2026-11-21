import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_VISION_MODEL: str = "qwen/qwen3.8-27b"  # Free Groq Vision Model
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    UPLOAD_DIR: str = "uploads"
    MAX_IMAGE_DIMENSION: int = 2048

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()