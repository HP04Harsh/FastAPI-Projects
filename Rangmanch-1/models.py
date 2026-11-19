from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone  # <--- timezone add kiya hai

# 1. Database Table Model
class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)  # <--- Fix here!
    )

# 2. Input Validation Schema
class ReviewCreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

# 3. Output Schema
class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: Optional[str]
    created_at: datetime

# 4. Update Schema
class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None