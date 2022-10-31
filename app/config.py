from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_USERNAME:str
    DATABASE_HOSTNAME:str
    DATABASE_PASSWORD:str
    DATABASE_POST:str
    DATABASE_USER:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    class Config:
        env_file = '.env'
    
    
    
    
setting =Settings()