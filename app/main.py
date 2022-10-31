from fastapi import FastAPI 
from .database import engine
from . import models,schemas
models.Base.metadata.create_all(bind=engine)
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}



@app.get("/")
async def root():
    return {"message":"Hello, world!!!"} 

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)







    