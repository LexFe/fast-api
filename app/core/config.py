import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings 


load_dotenv()

class Settings(BaseSettings):
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    HOST :str = os.getenv("HOST")
    PORT :int = os.getenv("PORT")

    # SQLAlchemy specific environment variables.
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_ENGINE:str = "mysql+mysqlconnector"
    DB_DATABASE:str = "my_test"
    DATABASE_URL:str ="{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}".format(
        DB_ENGINE=DB_ENGINE,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_DATABASE = DB_DATABASE
    )
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # find query
    PAGE :int = 1
    PAGE_SIZE :int = 20
    ORDERING : str = "-id"
    
    class Config:
        case_sensitive = True
        
settings = Settings()
