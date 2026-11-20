from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from database import get_session
from auth import verify_api_key
from models.book import Book, BookCreate, BookRead, BookUpdate
from models.user import User

router = APIRouter(prefix="/books", tags=["Books"])

# --- 1. Public Search / List Available Books ---
@router.get("/", response_model=list[BookRead])
def list_books(
    title: str | None = Query(None, description="Search by title substring"),
    author: str | None = Query(None, description="Search by author substring"),
    session: Session = Depends(get_session)
):
    # Default Rule: Show only unsold books
    query = select(Book).where(Book.is_sold == False)

    if title:
        query = query.where(Book.title.contains(title))
    if author:
        query = query.where(Book.author.contains(author))

    return session.exec(query).all()

# --- 2. Create Book Listing (Protected) ---
@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    # Verify owner exists
    owner = session.get(User, book_data.user_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner User ID not found.")

    db_book = Book.model_validate(book_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# --- 3. Partial Update Book Details (Protected) ---
@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found.")

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# --- 4. Mark Book as Sold (Quick Action Endpoint - Protected) ---
@router.patch("/{book_id}/sold", response_model=BookRead)
def mark_as_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found.")

    db_book.is_sold = True
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book