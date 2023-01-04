from pydantic import BaseSettings, EmailStr

class Setting(BaseSettings):
    database_driver: str
    database_user: str
    database_password: str
    database_port: str
    database_name: str
    database_host: str
    secret_key: str
    localhost: str
    email: EmailStr
    email_password: str
   

    access_token_expire_minutes: int
    algorithm: str
    


    class Config:
        env_file =".env"

settings = Setting()