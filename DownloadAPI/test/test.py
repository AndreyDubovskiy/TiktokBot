import pytest
from httpx import AsyncClient, ASGITransport
import time

from DownloadAPI.main import app

TEST_URL_VIDEO = "https://vt.tiktok.com/ZSHUASECY/"
TEST_URL_PHOTO = "https://vt.tiktok.com/ZSH5kDBVT/"

@pytest.mark.asyncio
async def test_download_video():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.get("/download/", params={"url": TEST_URL_VIDEO, "tg_id": "123"})
        assert res.status_code == 200
        assert res.json() == 1
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.status_code == 200
        assert res2.headers["content-type"] == "video/mp4"
        data = b"".join([chunk async for chunk in res2.aiter_bytes()])
        assert len(data) > 0
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.json() == None

@pytest.mark.asyncio
async def test_download_photo():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as client:
        res = await client.get("/download/", params={"url": TEST_URL_PHOTO, "tg_id": "123"})
        assert res.status_code == 200
        assert res.json() == 3
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.status_code == 200
        assert res2.headers["content-type"] == "image/png"
        data = b"".join([chunk async for chunk in res2.aiter_bytes()])
        assert len(data) > 0
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.status_code == 200
        assert res2.headers["content-type"] == "image/png"
        data = b"".join([chunk async for chunk in res2.aiter_bytes()])
        assert len(data) > 0
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.status_code == 200
        assert res2.headers["content-type"] == "audio/mp3"
        data = b"".join([chunk async for chunk in res2.aiter_bytes()])
        assert len(data) > 0
        res2 = await client.get("/get_file/", params={"tg_id": "123"})
        assert res2.json() == None