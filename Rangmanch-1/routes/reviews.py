from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from database import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# 1. Create a Review (POST)
@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)
):
    db_review = Review.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

# 2. Get All Reviews with Pagination & Play Name Filter (GET)
@router.get("/", response_model=list[ReviewRead])
def list_reviews(play_name: str | None = Query(None, description="Filter reviews by play name"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max items per page"),
    session: Session = Depends(get_session)
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)
    reviews = session.exec(query).all()
    return reviews

# 3. Get Average Rating & Total Count for a Play (GET)
@router.get("/average/{play_name}")
def get_average_rating(
    play_name: str,
    session: Session = Depends(get_session)
):
    statement = select(
        func.avg(Review.rating),
        func.count(Review.id)
    ).where(Review.play_name == play_name)

    avg_rating, total_reviews = session.exec(statement).first()

    if not total_reviews:
        raise HTTPException(
            status_code=404,
            detail=f"No reviews found for play '{play_name}'"
        )

    return {
        "play_name": play_name,
        "average_rating": round(avg_rating, 2),
        "total_reviews": total_reviews
    }

# 4. Get Single Review by ID (GET)
@router.get("/{review_id}", response_model=ReviewRead)
def get_review(
    review_id: int,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# 5. Update Review Partially (PATCH)
@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: Session = Depends(get_session)
):
    db_review = session.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Extract only fields explicitly sent by client
    update_data = review_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_review, key, value)

    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

# 6. Delete Review (DELETE)
@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    session.delete(review)
    session.commit()
    return {"message": "Review deleted successfully"}
