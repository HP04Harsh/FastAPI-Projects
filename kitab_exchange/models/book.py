from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User

# 1. Database Table Model
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float
    is_sold: bool = Field(default=False)

    # Foreign Key pointing to User table
    user_id: int = Field(foreign_key="user.id")

    # Relationship back-link to owner User
    owner: Optional["User"] = Relationship(back_populates="books")

# 2. Input Schema for Book Creation
class BookCreate(SQLModel):
    title: str
    author: str
    price: float
    user_id: int

# 3. Output Schema for Book Information
class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int

# 4. Input Schema for Partial Updates (PATCH)
class BookUpdate(SQLModel):
    price: Optional[float] = None
    is_sold: Optional[bool] = None