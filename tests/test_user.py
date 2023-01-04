import pytest
from app import models, schemas
from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_user(
    async_client: AsyncClient
):
    data ={"email": "lawalafeez820@gmail.com", "password":"password"}
    res = await async_client.post("/users/", json=data)
    user = schemas.UserOuts(**res.json())
    assert user.email == data["email"]
    assert res.status_code == 201


@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient, User1
):
    res = await async_client.post("/login", data={"username": User1["email"], "password": User1["password"]})

    output = schemas.Token(**res.json())
    assert output.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", 
[
    (None, None, 422),
    ("adekunle@gmail.com", "incorrect", 403),
    ("incorrect", "test", 403)
]
)
@pytest.mark.asyncio
async def test_incorrect_login(
    async_client, User1, email, password, status_code
):
    res = await async_client.post("/login", data={"username": email, 
    "password": password})
    assert res.status_code == status_code
















"""@pytest.mark.asyncio
async def test_root(
       async_client: AsyncClient
       
):
    res = await async_client.get("/")
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_create_user(
       async_client: AsyncClient,
):
    res = await async_client.post("/users/", json={"email": "le@gmail.com", "password": "password123"})
    print(res)

    assert res.status_code == 201"""





