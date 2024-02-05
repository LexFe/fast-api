from fastapi import APIRouter ,Response ,status ,HTTPException ,Depends ,Response ,File ,UploadFile 
from sqlalchemy.orm import Session 
from typing import Optional
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from io import BytesIO
from starlette.middleware.authentication import AuthenticationMiddleware

from app.schema import auth_schema ,user_schema
from app.util import hash
from app.core.model import User ,ImageUser
from app.core.database import get_db
from app.core import security
from app.service import user_service 


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
    #dependencies= [Depends(security.oauth2_scheme)]
)


@router.post('/create-user',response_model=auth_schema.UserOut)
async def create_user(data :user_schema.UserCreate, db: Session = Depends(get_db)):
    return await user_service.create_user_account(data, db)

@router.post('/create', response_model=auth_schema.UserOut)
def create(user: user_schema.UserCreate ,db :Session= Depends(get_db)):
   
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = hash.hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/' , response_model=auth_schema.UserOut)
def get_user(id :int ,db :Session= Depends(get_db) , current_user: int = Depends(security.get_current_user)):
    user =db.query(User).filter(User.id == id , User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authoerized")
    return user

@router.get('/all' , response_model=list[auth_schema.UserOut])
def get_all_user(db:Session= Depends(get_db),limit:int =10 , skip:int = 0 , search:Optional[str] = '',current_user : int = Depends(security.get_current_user)):
    
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   
    getAll = db.query(User).filter(User.email.contains(search)).limit(limit).offset(skip).all()
    
    return getAll

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db) , current_user: int = Depends(security.get_current_user)):
    user = db.query(User).filter(User.id == id , User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{id}', response_model=auth_schema.UserOut)  # Fix the route decorator
def patch_user( user_patch: user_schema.UserPatch, db: Session = Depends(get_db)):
    # Retrieve the user from the database based on the provided id
    user = db.query(User).filter(User.id == user_patch.id).first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db.query(User).filter(User.email == user_patch.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Update the user's email and password if provided in the patch
    user.email = user_patch.email if user_patch.email else user.email
    user.password = hash.hash_password(user_patch.password) if user_patch.password else user.password

    db.commit()

    db.refresh(user)

    return user

@router.put('/{id}', response_model=auth_schema.UserOut)  # Fix the route decorator
def put_user( user_patch: user_schema.UserPatch, db: Session = Depends(get_db)):
    # Retrieve the user from the database based on the provided id
    user = db.query(User).filter(User.id == user_patch.id).first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db.query(User).filter(User.email == user_patch.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Update the user's email and password if provided in the patch
    user.email = user_patch.email if user_patch.email else user.email
    user.password = hash.hash_password(user_patch.password) if user_patch.password else user.password

    db.commit()

    db.refresh(user)

    return user

@router.post('/uploadfile/')
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the content as bytes
        content = await file.read()
        filename = file.filename
        new_image = ImageUser(filename=filename, content=content)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {"filename": filename}
    except Exception as e:
        # Handle specific exceptions if needed
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/get-image/{image_id}" , response_class=FileResponse)
def get_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(ImageUser).filter(ImageUser.image_id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return StreamingResponse(BytesIO(db_image.content), media_type="image/jpeg")


@router.patch('/update_image/{image_id}')
async def update_image(image_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_image = db.query(ImageUser).filter(ImageUser.image_id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    db_image.content = await file.read()
    db.commit()
    db.refresh(db_image)
    
    return {"filename": db_image.filename}


@router.get('/user-password/{id}' , response_model=auth_schema.UserPassword)
async def user_pw(id :int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return user
# Fix the route decorator

# @router.get("/get_image")
# async def get_image(db: Session = Depends(get_db)):
#     image = db.query(ImageUser).filter(ImageUser.image_id == 8).first()
#     print(image.filename)
#     image_path = Path(image.filename)
#     if not image_path.is_file():
#         return {"error": "Image not found on the server"}
#     return FileResponse(image_path)
  
# @router.get('/image/{id}')
# async  def get_image(id: int, db: Session = Depends(get_db)):
#     image = db.query(ImageUser).filter(ImageUser.image_id == id).first()
#     if not image:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
#     image_content_base64 = base64.b64encode(image.content).decode('utf-8')
    
#     # Return the image data as JSON
#     return {"image_id": image.image_id, "filename": image.filename, "content": image_content_base64}





# @router.get('/tea')
# def tea():
#     content = """
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>HTML Image Example</title>
#         </head>
#         <body>
           
#         </body>
#         </html>
#     """
#     return HTMLResponse(content=content)
