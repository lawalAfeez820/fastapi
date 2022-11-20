from .. import models, utils, database
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status, APIRouter
import sqlalchemy
from typing import Dict

router = APIRouter(
    prefix="/users",
    tags= ["USERS"]
)

@router.post("/", response_model=models.UserOuts, status_code= status.HTTP_201_CREATED)
async def create_user(post: models.CreateUser, db: Session = Depends(database.get_session)):

    query = await db.exec(select(models.Users).where(models.Users.email == post.email.lower()))
    query = query.first()
    if query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"User with {post.email} already exist")

    post.password = utils.hash(post.password)
    post.email = post.email.lower()
    user_data = models.Users.from_orm(post)
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data

@router.get("/{id}", response_model=models.UserOuts)
async def get_user(id: int ,db: Session = Depends(database.get_session)):
    user = await db.get(models.Users, id)
    print(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user


