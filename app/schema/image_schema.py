from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ImageUpload(BaseModel):
    filename: str
    content: bytes

    class Config:
        orm_mode = True