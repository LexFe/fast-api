from fastapi import APIRouter ,Depends ,HTTPException ,status ,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.model import User
from app.schema import user_schema 
from app.util import hash
from app.core import security


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/",response_model= user_schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm =Depends(),db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not hash.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = security.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
    


