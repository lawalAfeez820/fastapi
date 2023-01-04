import pytest
from app import models, schemas
from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_all_post_but_zero_post(
   Autorized_Client1
):

    res =await Autorized_Client1.get("/posts/")

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_get_all_post(Autorized_Client1, post1):
    res =await Autorized_Client1.get("/posts/")

    assert res.status_code == 200

@pytest.mark.asyncio
async def test_get_all_post_unauthorized(
   async_client
):

    res =await async_client.get("/posts/")

    assert res.status_code == 401

    

@pytest.mark.asyncio
async def test_create_post(
   Autorized_Client1
):
    data = {"title": "food", "content": "food is life"}
    res =await Autorized_Client1.post("/posts/", json = data)

    assert res.status_code == 201

@pytest.mark.asyncio
async def test_create_post_unathorized(
   async_client
):
    data = {"title": "food", "content": "food is life"}
    res =await async_client.post("/posts/", json = data)

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_update_post(Autorized_Client1, post1):
    res=await Autorized_Client1.put("/posts/1", json = {"title":"foodsss"})

    res = schemas.ResponseType(**res.json())

    assert res.title == "foodsss"

@pytest.mark.asyncio
async def test_retrieve_post(Autorized_Client1, post1):
    res=await Autorized_Client1.get("/posts/getone/1")

    assert res.status_code == 200

@pytest.mark.asyncio
async def test_retrieve_post_unauthorized(async_client):
    res = await async_client.get("/posts/getone/1")


    assert res.status_code == 401

@pytest.mark.asyncio
async def test_retrieve_post_with_invalid_id(Autorized_Client1, post1):
    res=await Autorized_Client1.get("/posts/getone/2")

   

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_post(Autorized_Client1, post1):
    res=await Autorized_Client1.delete("/posts/1")


    assert res.status_code == 204

@pytest.mark.asyncio
async def test_delete_post_unathorized(async_client):
    res=await async_client.delete("/posts/1")

    assert res.status_code == 401

@pytest.mark.asyncio
async def test_delete_post_that_does_not_exist(Autorized_Client1, post1):
    res=await Autorized_Client1.delete("/posts/2")

    assert res.status_code == 404 












