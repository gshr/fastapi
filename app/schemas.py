from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
    
    #rating: Optional[int] =None

    
class CreatePost(Post):
    pass


class UserCreateResponse(BaseModel):
    id:int
    email :EmailStr
    created_at : datetime
    
    class Config:
        orm_mode =True
        
        
class PostResponse(Post):
    id :int
    owner_id : int
    created_at : datetime
    owner : UserCreateResponse
    
    class Config:
        orm_mode =True
        
        
class UserCreate(BaseModel):
    email :EmailStr
    password:str
    

        
class UserLogin(BaseModel):
    email :EmailStr
    password:str
   
    
class Token(BaseModel):
    access_token :str
    token_type :str
 
    
class TokenData(BaseModel):
    id:Optional[str] =None
    

class Vote(BaseModel):
    post_id:int
    dir:int
    

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes:int
    
    
    class Config:
        orm_mode =True
    

    
    
    

    

        