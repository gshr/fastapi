from fastapi import FastAPI ,Response ,status,HTTPException,Depends
from .database import engine
from . import models,schemas
from .schemas import Post,CreatePost,PostResponse,UserCreate,UserCreateResponse
models.Base.metadata.create_all(bind=engine)
from .routers import post,user,auth

app = FastAPI()




@app.get("/")
async def root():
    return {"message":"Hello, world!!!"} 

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)







    