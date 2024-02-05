from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional , List




    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    
    class Config:
        orm_mode = True
        
class UserPassword(BaseModel):
    password: str
    user :List[UserOut] = []
    
    class Config:
        orm_mode = True
        
class UserLogin (BaseModel):
    email: EmailStr
    password: str