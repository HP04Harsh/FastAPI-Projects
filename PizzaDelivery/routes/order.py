from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from database import get_session
from models import Pizza, ReadStock, CreatePizza


router = APIRouter(
    prefix="/order",
    tags=["Order"]
)

@router.post("/",response_model=ReadStock)
def create_stock(pizza:CreatePizza,session:Session=Depends(get_session)):
    db = Pizza.model_validate(pizza)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/stock",response_model=ReadStock)
def get_stock(id:int,session:Session=Depends(get_session)):
    result = session.get(Pizza,id)
    return result