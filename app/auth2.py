from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, database, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session



oauth2_schema= OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict):
    payload= data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp":expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)
    return token


def verify_access_token(token: str, CredentialException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if not id:
            raise CredentialException
        token_data = models.TokenData(id = id)
    except JWTError as e:
        raise CredentialException
    return token_data

async def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_session)):
    redentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    
    token_data= verify_access_token(token, redentials_exception)

    user = await db.get(models.Users,token_data.id)

    return user


