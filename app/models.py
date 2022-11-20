from typing import List
from sqlalchemy.sql.expression import text
from .database import SQLModel
from sqlmodel import Field, Relationship
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column,Boolean,String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Users(SQLModel, table= True):
    email: str = Field(sa_column = (Column(String,unique=True, nullable=False)))
    password: str
    id: Optional[int] = Field(primary_key = True, default = None)
    created_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True), 
    server_default=text("now()")))
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
    owner: Optional[Users] = Relationship(back_populates="posts")


class CreatePost(SQLModel):
    published: Optional[bool] = True
    title: str
    content: str

class UpdatePost(SQLModel):
    published: Optional[bool]
    title: Optional[str]
    content: Optional[str]


class CreateUser(SQLModel):
    email: EmailStr
    password: str

class UserOuts(SQLModel):
    email: str
    id: int
    created_at: datetime
    

class ResponseType(CreatePost):
    user_id: int
    owner: UserOuts

class TokenData(SQLModel):
    id: int

class Token(SQLModel):
    access_token: str
    token_type:str

class Voters(SQLModel):
    post_id: int
    vote_dir: int #need to make it to accept just 0 for downvote and 1 for upvote later

class Vote(SQLModel, table = True):
    post_id: int = Field(sa_column= Column(Integer,
     ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))
    user_id: int = Field(sa_column= Column(Integer,
     ForeignKey("users.id", ondelete="CASCADE"), primary_key=True))

