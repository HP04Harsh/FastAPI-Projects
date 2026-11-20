from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from auth import verify_api_key
from models.user import User, UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])

# --- Create User (Protected by API Key Header) ---
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)  # Header Auth Dependency
):
    # Check for duplicate email
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email address is already registered."
        )

    db_user = User.model_validate(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# --- List Users (Public Read Endpoint) ---
@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users