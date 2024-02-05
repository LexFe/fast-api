from sqlalchemy import Column, Integer, Boolean, ForeignKey,NVARCHAR,BLOB, LargeBinary , DateTime , func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(NVARCHAR(150))
    email = Column(NVARCHAR(255), unique=True, index=True)
    password = Column(NVARCHAR(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(NVARCHAR(255), nullable=True, default=None)
    updated_at = Column(NVARCHAR(255), nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(NVARCHAR(255), nullable=False, server_default=func.now())
    
    tokens = relationship("UserToken", back_populates="user")

    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()
    
    

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(NVARCHAR(250), nullable=True, index=True, default=None)
    refresh_key = Column(NVARCHAR(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")
    


# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), primary_key=True)
#     post_id = Column(Integer, ForeignKey(
#         "posts.id", ondelete="CASCADE"), primary_key=True)
    
class ImageUser(Base):
    __tablename__ = "image_users"
    image_id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(NVARCHAR(100),nullable=False)
    content = Column(LargeBinary,nullable=False)