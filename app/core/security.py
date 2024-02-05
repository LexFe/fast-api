from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, status, HTTPException

from app.core import database , model
from app.schema import user_schema 
from app.core.config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# class JWTAuthenticationBackend:
#     async def authenticate(self,conn):
#         token = await self.oauth2_scheme(request)
#         credentials_exception = HTTPException(
#             status_code = status.HTTP_401_UNAUTHORIZED,
#             detail = "Could not validate credentials",
#             headers = {"WWW-Authenticate": "Bearer"},
#         )
#         return verify_access_token(token, credentials_exception)
    
    

async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# async def create_refresh_token(data):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# def get_token_payload(token):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         return None
#     return payload

def verify_access_token(token :str ,credentials_expeption):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms = [ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_expeption
        token_data = user_schema.TokenData(id = id)
    except JWTError :
        return credentials_expeption
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    creaentails_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    
    token =verify_access_token(token,creaentails_exception)
    
    user = db.query(model.User).filter(model.User.id == token.id).first()
    
    return user




SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True