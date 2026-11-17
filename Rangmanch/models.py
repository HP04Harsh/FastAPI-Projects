from sqlmodel import SQLModel, Field
from typing import Optional

# ---------- DB TABLE ----------
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)     
    comment: Optional[str] = None

# ---------- REQUEST / RESPONSE SHAPES ----------
class ReviewCreate(SQLModel):          
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class ReadReview(SQLModel):            
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: Optional[str] = None

class ReviewUpdate(SQLModel):         
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
