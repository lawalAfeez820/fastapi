import pytest
from app import models
from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_all_post(
   Autorized_Client
):

    res =await Autorized_Client.get("/posts/")

    assert res.status_code == 200

    

@pytest.mark.asyncio
async def test_creat_post(
   Autorized_Client
):
    data = {"title": "food", "content": "food is life"}
    res =await Autorized_Client.post("/posts/", json = data)

    assert res.status_code == 201


@pytest.mark.asyncio
async def test_update_post(Autorized_Client, post):
    res=await Autorized_Client.put("/posts/1", json = {"title":"foodsss"})

    res = models.ResponseType(**res.json())

    assert res.title == "foodsss"

@pytest.mark.asyncio
async def test_retrieve_post(Autorized_Client, post):
    res=await Autorized_Client.get("/posts/1")

    res = models.ResponseType(**res.json())

    assert res.title == "food"
    assert res.content == "food is life"

@pytest.mark.asyncio
async def test_delete_post(Autorized_Client, post):
    res=await Autorized_Client.delete("/posts/1")


    assert res.status_code == 204







