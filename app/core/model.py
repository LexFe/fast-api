from sqlalchemy import Column, Integer, Boolean, ForeignKey,NVARCHAR,BLOB, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(NVARCHAR(50), nullable=False)
    content = Column(NVARCHAR(50), nullable=False)
    published = Column(Boolean, nullable=False, server_default='1')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(NVARCHAR(50), nullable=False, unique=True)
    password = Column(NVARCHAR(200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    
class ImageUser(Base):
    __tablename__ = "image_users"
    image_id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(NVARCHAR(100),nullable=False)
    content = Column(LargeBinary,nullable=False)