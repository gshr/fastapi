from fastapi import FastAPI ,Response ,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import  Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    #rating: Optional[int] =None

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='admin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(10)



@app.get("/")
async def root():
    return {"message":"Hello, world!!!"} 


@app.get("/posts")
async def get_posts():
    query = """ SELECT * FROM posts """
    cursor.execute(query)
    posts=cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")   #{id} is path parameter
async def get_post(id:int,response:Response):
    query = f"SELECT * FROM posts WHERE  id = {id}"
    cursor.execute(query)
    post=cursor.fetchone()
    
    if post:
            return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
   
    
@app.delete("/posts/{id}")   #{id} is path parameter
async def delete_post(id:int,response:Response):
    query = f"DELETE  FROM posts WHERE  id = {id} RETURNING *"
    cursor.execute(query)
    post=cursor.fetchone()
    conn.commit()
    if post:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
    
@app.put("/posts/{id}") 
async def update_post(id:int,post:Post):
    cursor.execute("UPDATE posts SET title = %s , content = %s, published = %s WHERE id = %s RETURNING *",(post.title,post.content,post.published,str(id)))
    updated_post =cursor.fetchone()
    conn.commit()
    if updated_post :
        return {"detail": updated_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:Post) :
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return ({"data":new_post})