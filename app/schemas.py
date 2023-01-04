from sqlmodel import SQLModel
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class PasswordReset(SQLModel):
    old_password: str
    new_password: str
    confirm_new_password: str

class ForgetPassword(SQLModel):
    email: EmailStr


class TokenData(SQLModel):
    email: EmailStr

class Token(SQLModel):
    access_token: str
    token_type:str

class Voters(SQLModel):
    post_id: int
    vote_dir: int #need to make it to accept just 0 for downvote and 1 for upvote later

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
    id: int
    owner: UserOuts