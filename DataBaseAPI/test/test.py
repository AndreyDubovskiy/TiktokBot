import pytest
from httpx import AsyncClient, ASGITransport
import datetime

from DataBaseAPI.main import app
from DataBaseAPI.DB.db import start_database, create_all_tables, drop_all_tables

@pytest.mark.asyncio
async def test_get_user_zero():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        await start_database("testbase")
        await drop_all_tables()
        await create_all_tables()
        res = await client.get("/users/")
        assert res.status_code == 200
        assert res.json() is None

@pytest.mark.asyncio
async def test_add_user():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.post("/users/create/", json={"tg_name": "test", "tg_id": "123"})
        assert res.status_code == 200
        assert res.json()["tg_name"] == "test"
        assert res.json()["tg_id"] == "123"

@pytest.mark.asyncio
async def test_add_bad_user():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.post("/users/create/", json={"tg_name": "test", "tg_id": None})
        assert res.status_code != 200
        res2 = await client.post("/users/create/", json={"tg_name": "test", "tg_id": ""})
        assert res2.status_code != 200


@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.get("/users/", params={"user_tg_id": "123"})
        assert res.status_code == 200
        assert res.json()["tg_name"] == "test"
        assert res.json()["tg_id"] == "123"
        assert res.json().get("id") is not None
        res2 = await client.get("/users/", params={"user_id": res.json()["id"]})
        assert res2.status_code == 200
        assert res2.json()["tg_name"] == "test"
        assert res2.json()["tg_id"] == "123"
        assert res2.json().get("id") == res.json()["id"]
        res3 = await client.get("/users/", params={"user_name": res2.json()["tg_name"]})
        assert res3.status_code == 200
        assert res3.json()["tg_name"] == "test"
        assert res3.json()["tg_id"] == "123"
        assert res3.json().get("id") == res.json()["id"]

@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.get("/users/", params={"user_tg_id": "123"})
        res2 = await client.post("/users/update/", json={"id": res.json()["id"], "tg_name": "test2", "tg_id": "123"})
        assert res2.status_code == 200
        assert res2.json()["tg_name"] == "test2"
        assert res2.json()["tg_id"] == "123"
        assert res2.json().get("id") == res.json()["id"]

@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.get("/users/", params={"user_tg_id": "123"})
        res2 = await client.post("/users/delete/", json={"id": res.json()["id"]})
        assert res2.status_code == 200
        res3 = await client.get("/users/", params={"user_tg_id": "123"})
        assert res3.status_code == 200
        assert res3.json() is None

@pytest.mark.asyncio
async def test_add_five_users():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        for i in range(5):
            res = await client.post("/users/create/", json={"tg_name": f"test{i}", "tg_id": f"idtest{i}"})
            assert res.status_code == 200
            assert res.json()["tg_name"] == f"test{i}"
            assert res.json()["tg_id"] == f"idtest{i}"

@pytest.mark.asyncio
async def test_add_events():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        for i in range(5):
            res_user = await client.get("/users/", params={"user_tg_id": f"idtest{i}"})
            res = await client.post("/events/create/", json={"user_id": res_user.json()["id"], "name": f"event{i}"})
            assert res.status_code == 200
            assert res.json()["name"] == f"event{i}"
            assert res.json()["user_id"] == res_user.json()["id"]

@pytest.mark.asyncio
async def test_get_events():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res_user = await client.get("/users/", params={"user_tg_id": "idtest1"})
        res = await client.get("/events/", params={"user_id": res_user.json()["id"]})
        assert res.status_code == 200
        assert len(res.json()) == 1
        assert res.json()[0]["name"] == "event1"

@pytest.mark.asyncio
async def test_delete_event():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res_user = await client.get("/users/", params={"user_tg_id": "idtest1"})
        res_event = await client.get("/events/", params={"user_id": res_user.json()["id"]})
        res = await client.post("/events/delete/", json={"id": res_event.json()[0]["id"]})
        assert res.status_code == 200
        res2 = await client.get("/events/", params={"user_id": res_user.json()["id"]})
        assert res2.status_code == 200
        assert len(res2.json()) == 0

@pytest.mark.asyncio
async def test_get_events_by_datetime_and_filter():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res3 = await client.get("/events/by_datetime_and_filter/", params={"start": datetime.datetime.now(), "filter": "event"})
        assert res3.status_code == 200
        assert len(res3.json()) == 0
        res4 = await client.get("/events/by_datetime_and_filter/", params={"start": datetime.datetime.fromisoformat("2023-01-01T00:00:00"), "end": datetime.datetime.now(), "filter": "event"})
        assert res4.status_code == 200
        assert len(res4.json()) > 0
        res5 = await client.get("/events/by_datetime_and_filter/", params={"filter": "eventasd"})
        assert res5.status_code == 200
        assert len(res5.json()) == 0













