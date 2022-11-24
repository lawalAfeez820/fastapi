from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.orm import sessionmaker
from . import config




SQLMODEL_DATABASE_URL= f"""postgresql+{config.settings.database_driver}://{config.settings.database_user}:{
    config.settings.database_password}@{config.settings.database_host}:{config.settings.database_port}/{config.settings.database_name}"""
#SQLMODEL_ALEMBIC_URL= f"postgresql+{config.settings.database_driver}://{config.settings.database_user}:{config.settings.alembic_password}@{config.settings.database_host}:{config.settings.database_port}/{config.settings.database_name}"

engine = create_async_engine(SQLMODEL_DATABASE_URL,future= True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(engine,class_= AsyncSession,expire_on_commit= False)
    async with async_session() as session:
        yield session




