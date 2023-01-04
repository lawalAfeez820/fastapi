from typing import Optional, List
from app import models
from app.database import get_session
from sqlmodel import SQLModel, Session, select
from pydantic import EmailStr
from jose import jwt, JWTError
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException, Depends, status
from datetime import datetime, timedelta
import secrets
from app.config import settings

class EmailSchema(SQLModel):
    email: EmailStr

SECRET = settings.secret_key
ALGORITHM = settings.algorithm
EXP = settings.access_token_expire_minutes




class Mail:

    def __init__(self):

        self.password = secrets.token_hex(8)


    async def get_new_password(self):

        new_password = secrets.token_hex(8)
        if len(new_password) > 6:
            new_password = new_password[:6]
        self.password = new_password
        return self.password


    async def get_new_password_mail(self, email: EmailStr):

        me = settings.email
        you = email
        _password =settings.email_password

    
        html = f"""\
        <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <div>
                    <p>Your new password is {self.password}</p>
                
                </div>
            </body>
            </html>
        """
        msg = MIMEMultipart()

        msg['Subject'] = "New Password Notification"
        msg['From'] = me
        msg['To'] = you

        msg.attach(MIMEText(html,"html"))
        msg_string = msg.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as server:
            server.login(me, _password)
            server.sendmail(me, you, msg_string)


Mail_Manager = Mail()

    