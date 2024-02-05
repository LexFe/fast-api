from typing import List, Optional
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str

    
class TokenData(BaseModel):
    id: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserPatch(BaseModel):
    id : int
    email: Optional[EmailStr]
    password: Optional[str]
    


class UserImage(BaseModel):
    filename: str
    content : bytes
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    
    
    
    
    
    
    