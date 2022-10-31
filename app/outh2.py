from jose import JWTError,jwt
from datetime   import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import setting
oauth_schemes = OAuth2PasswordBearer(tokenUrl = 'login')


#SECRET KEY
#ALgorithm
#Expiration Time ()

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data:dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,cred_exception):
    
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM)
        token_id:str=payload.get('user_id')
        if id is None:
            return cred_exception
        
        token_data = schemas.TokenData(id=token_id)
        
    except JWTError:
        raise cred_exception
    
    return token_data
    
def current_user(token:str = Depends(oauth_schemes),db:Session =Depends(database.get_db)):
    cred_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail=f"token not validate Credentails",
                                  headers={"WWW-Authenticate":'Bearer '})
    
    token=verify_access_token(token, cred_exception)
    user=db.query(models.User).filter(models.User.id == token.id).first()
    
    print(user.email)
    
    return user
    
    
    
    
    
    
    
    
    
    
    
    
    