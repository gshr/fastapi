from fastapi import FastAPI ,Response ,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import  Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating: Optional[int] =None

my_posts = [{
    "title":"Top Gun",
    "content":"Checkout this awesome movie",
    "id": 1
},
 {  "title":"Fav Food",
    "content":"Pizza",
    "id": 2 
}]

@app.get("/")
async def root():
    return {"message":"Hello, world!!!"} 


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")   #{id} is path parameter
async def get_post(id:int,response:Response):
    for i in my_posts:
        if i['id'] == id:
            return {"data": i}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
@app.delete("/posts/{id}")   #{id} is path parameter
async def delete_post(id:int,response:Response):
    for index,i  in enumerate(my_posts):
        if i['id'] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
    
@app.put("/posts/{id}") 
async def update_post(id:int,post:Post):
    print(post)
    
    for index,i  in enumerate(my_posts):
        if i['id'] == id:
            post_dict = post.dict()
            post_dict['id'] =id
            my_posts[index] = post_dict
            return {"data": post_dict}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} was not found")
    
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:Post) :
    post_dict = post.dict()
    post_dict["id"] =   randrange(1,1000000)
    my_posts.append(post_dict)
    return ({"data":post_dict})