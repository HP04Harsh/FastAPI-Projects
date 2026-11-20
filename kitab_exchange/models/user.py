from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.book import Book

# 1. Database Table Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    # 1-to-Many Relationship: One User -> Many Books
    books: list["Book"] = Relationship(back_populates="owner")

# 2. Input Schema for Registration
class UserCreate(SQLModel):
    name: str
    email: str
    college: str

# 3. Output Schema for User Info
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str