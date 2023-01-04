from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, database, utils, auth2, schemas
from typing import Dict

router = APIRouter(
    tags= ["AUTH"]
)

@router.post("/login", response_model=schemas.Token)
async def login(detail: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_session)):

    
    users = await db.exec(select(models.Users).where(models.Users.email == detail.username.lower()))
    user: models.Users = users.first()
    

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify_hash(detail.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    token = auth2.create_access_token(data= {"user_email":user.email})

    data = schemas.Token(access_token= token, token_type= "bearer")

    return data

    

