from .. import models, utils, database, auth2, config, schemas
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status, APIRouter, File, UploadFile, BackgroundTasks
import sqlalchemy
from typing import Dict
import secrets
import os
from app.mail import Mail_Manager

from PIL import Image


router = APIRouter(
    prefix="/users",
    tags= ["USERS"]
)



@router.post("/", response_model=schemas.UserOuts, status_code= status.HTTP_201_CREATED)
async def create_user(post: schemas.CreateUser, db: Session = Depends(database.get_session)):

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

@router.get("/{id}", response_model=schemas.UserOuts)
async def get_user(id: int ,db: Session = Depends(database.get_session)):
    user = await db.get(models.Users, id)
    print(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user

@router.post("/profilepics")
async def upload_pics(file: UploadFile = File(...), current_user: models.Users =  Depends(auth2.get_current_user), db: Session = Depends(database.get_session)):

    file_path = __file__.split(".")[0] + "static/images/"
    
    file_name = file.filename
    file_extension  = file_name.split(".")[-1]
    token = secrets.token_hex(10) + "." + current_user.email
    
    
    file_content = await file.read()
    if file_extension not in ["jpg", "png"]:
        raise HTTPException(status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail = "Unsupported file format")
    
    for image in os.listdir(file_path):
        email = image.split(".")[-3]
        if email + ".com" == current_user.email:
            os.remove(file_path + "/" + image)
            break

    generated_file_name = file_path + token + "." + file_extension
    with open(generated_file_name, "wb") as file:
        file.write(file_content)
    img = Image.open(generated_file_name)
    img = img.resize((200, 200))
    img.save(generated_file_name)

    file.close()
    file_name = config.settings.localhost +"/static/images/" + token + "." + file_extension
    user = await db.exec(select(models.Users).where(models.Users.email == current_user.email))
    user: models.Users = user.first()
    user.profile_pics = file_name
    db.add(user)
    await db.commit()
    return {"file_name": file_name}

@router.put("/updatepassword")
async def update_passsword(detail: schemas.PasswordReset,current_user: models.Users =  Depends(auth2.get_current_user), db: Session = Depends(database.get_session)):
    if not utils.verify_hash(detail.old_password, current_user.password):
        raise HTTPException(status_code = 409, detail = "Old password is incorrect")
    if detail.confirm_new_password != detail.new_password:
        raise HTTPException(status_code = 409, detail = "The two new password field do not match")
    current_user.password = utils.hash(detail.new_password)  
    db.add(current_user)
    await db.commit()
    return {"detail": "Your password has been reset"}

@router.put("/forgetpassword")
async def forget_password(background_task: BackgroundTasks, detail: schemas.ForgetPassword, db: Session = Depends(database.get_session)):

    user = await db.exec(select(models.Users).where(models.Users.email == detail.email))
    user: models.Users = user.first()
    if not user:
        raise HTTPException(status_code = 404, detail = f"No user with email {detail.email}")
    new_password = await Mail_Manager.get_new_password()
    print(new_password)
    background_task.add_task(Mail_Manager.get_new_password_mail, detail.email)
    user.password = utils.hash(new_password)
    db.add(user)
    await db.commit()
    return {"detail": "Check your mail for password update"}
    

    




    



