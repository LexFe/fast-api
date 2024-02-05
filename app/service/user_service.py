from fastapi import HTTPException 
from datetime import datetime

from app.util.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
from app.core.security import  is_password_strong_enough
from app.util.hash import hash_password
from app.core.model import User


async def create_user_account(data, session):
    
    user_exist = session.query(User).filter(User.email == data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email is already exists.")
    
    if not is_password_strong_enough(data.password):
        raise HTTPException(status_code=400, detail="Please provide a strong password.")
    
    
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    user.is_active = False
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Account Verification Email
    # await send_account_verification_email(user, background_tasks=background_tasks)
    return user