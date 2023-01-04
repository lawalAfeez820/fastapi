import asyncio
from typing import Generator
from app import models, schemas
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session


from .db import async_engine
from app.main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
   session = sessionmaker(
       async_engine, class_=AsyncSession, expire_on_commit=False
   )

   async with async_engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.drop_all)

   async with session() as s:
       async with async_engine.begin() as conn:
           await conn.run_sync(SQLModel.metadata.create_all)

       yield s

   

   #await async_engine.dispose()

@pytest_asyncio.fixture
async def async_client(async_session):

    async def override_get_db():
        try:
            yield async_session
        finally:
            async_session.close()
    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
           app=app,
           base_url=f"http://"
   ) as client:
       yield client

@pytest_asyncio.fixture
async def User1(async_client):
    data = {"email":"adekunle@gmail.com","password": "test"}
    res = await async_client.post("/users/", json= data)
    res = res.json()
    res["password"] = data["password"]
    return res

@pytest_asyncio.fixture
async def Login1(async_client, User1):
    res = await async_client.post("/login",  data={"username": User1["email"], "password": User1["password"]})

    res = schemas.Token(**res.json())

    return res.access_token

@pytest_asyncio.fixture
async def Autorized_Client1(async_client, Login1):
    async_client.headers = {**async_client.headers, "Authorization": f"Bearer {Login1}"}
    return async_client

@pytest_asyncio.fixture
async def post1(Autorized_Client1):
    data = {"title": "food", "content": "food is life"}
    res = await Autorized_Client1.post("/posts/", json = data)
    res = schemas.ResponseType(** res.json())
    return res

@pytest_asyncio.fixture
async def User2(async_client):
    data = {"email":"adekunl@gmail.com","password": "test"}
    res = await async_client.post("/users/", json= data)
    res = res.json()
    res["password"] = data["password"]
    return res

@pytest_asyncio.fixture
async def Login2(async_client, User2):
    res = await async_client.post("/login",  data={"username": User2["email"], "password": User2["password"]})

    res = schemas.Token(**res.json())

    return res.access_token

@pytest_asyncio.fixture
async def Autorized_Client2(async_client, Login2):
    async_client.headers = {**async_client.headers, "Authorization": f"Bearer {Login2}"}
    return async_client






