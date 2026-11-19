from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Pizza(SQLModel,table=True):
    id:Optional[int]=Field(None,ge=1,primary_key=True)
    flavour:str=Field(index=True)
    stock:int

class CreatePizza(SQLModel):
    id: int
    flavour: str
    stock:int

class ReadStock(SQLModel):
    flavour:str
    stock:int

