from fastapi import FastAPI ,Response ,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import  Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..database import engine,get_db
from sqlalchemy.orm import Session
from .. import models
from ..schemas import UserCreate,UserCreateResponse
from ..utils import hash


router = APIRouter(
    prefix = "/users",
    tags =['Users']
)




@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserCreateResponse)
async def create_user(user:UserCreate,db:Session =Depends(get_db)):
    
    #Hash the password
    
    user.password=hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=UserCreateResponse)
def get_user(id:int,db:Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"User with id {id} was not found")
    
    
    
    

