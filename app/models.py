from typing import List
from sqlalchemy.sql.expression import text
from .database import SQLModel
from sqlmodel import Field, Relationship
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column,Boolean,String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func


class Users(SQLModel, table= True):
    email: EmailStr = Field(sa_column = (Column(String,unique=True, nullable=False)))
    password: str
    id: Optional[int] = Field(primary_key = True, default = None)
    created_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True), 
    server_default=text("now()")))
    profile_pics: Optional[str] = None
    updated_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=func.current_timestamp()))
    posts: List["Posts"] = Relationship(back_populates= "owner")


class Posts(SQLModel,table= True):

    id: Optional[int] = Field(primary_key = True, default = None)
    title: str 
    content: str
    published: bool = Field(sa_column= Column(Boolean,server_default= "true"))
    created_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True),
     server_default=text("now()")))
    user_id: int = Field(sa_column= Column(Integer, 
    ForeignKey("users.id", ondelete="CASCADE"), nullable= False), default = None)
    creator_email: Optional[EmailStr] = None
    owner: Optional[Users] = Relationship(back_populates="posts")



    


class Vote(SQLModel, table = True):
    post_id: int = Field(sa_column= Column(Integer,
     ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))
    user_id: int = Field(sa_column= Column(Integer,
     ForeignKey("users.id", ondelete="CASCADE"), primary_key=True))




