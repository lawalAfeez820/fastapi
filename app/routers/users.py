from .. import models, utils, database
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status, APIRouter
import sqlalchemy
from typing import Dict

router = APIRouter(
    prefix="/users",
    tags= ["USERS"]
)

@router.post("/", response_model= Dict | models.UserOut, status_code= status.HTTP_201_CREATED)
async def create_user(post: models.CreateUser, db: Session = Depends(database.get_session)):

    try:
        post.password = utils.hash(post.password)
        user_data = models.Users.from_orm(post)
        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)
    except sqlalchemy.exc.IntegrityError:
        return {"detail": f"User with {post.email} already exist"}
    return user_data

@router.get("/{id}", response_model=models.UserOut)
async def get_user(id: int ,db: Session = Depends(database.get_session)):
    user = await db.get(models.Users, id)
    print(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user


