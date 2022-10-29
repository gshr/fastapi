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
from ..schemas import Post,CreatePost,PostResponse

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/",response_model=List[PostResponse])
async def get_posts(db:Session =Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@router.get("/{id}",response_model=PostResponse)   #{id} is path parameter
async def get_post(id:int,db:Session =Depends(get_db),):
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if post:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
   
    
@router.delete("/{id}")   #{id} is path parameter
async def delete_post(id:int,response:Response,db:Session =Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
    
@router.put("/{id}",response_model=PostResponse) 
async def update_post(id:int,post:CreatePost ,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    updated_post = post_query.first()
    if updated_post :
        post_query.update(post.dict(),synchronize_session=False)
        db.commit()
        return post_query.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
async def create_post(post:CreatePost,db:Session =Depends(get_db)) :
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post