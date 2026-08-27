import datetime
from typing import List

import uvicorn
import asyncio

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from httpx import AsyncClient

from TikTok.TikTokManager import static_tiktok_manager

app = FastAPI()

cash = {}

async def file_stream(url: str, user_agent):
    async with AsyncClient() as client:
        async with client.stream("GET", url, headers={"User-Agent": user_agent}) as r:
            print(r.headers)
            print(r.status_code)
            r.raise_for_status()
            async for chunk in r.aiter_bytes(1024 * 1024):
                yield chunk

@app.get("/ok")
async def ok():
    return "OK"

@app.get("/download/",
         tags=["TikTok"],
         summary="Download TikTok video or images and music.\nReturn 1 when download video, 2 and greater when download images and music")
async def download(url: str, tg_id: str) -> int:
    if tg_id in cash:
        cash.pop(tg_id)
    res = await static_tiktok_manager.download(url)
    if res is None:
        return None
    if isinstance(res, dict):
        cash[tg_id] = [res]
    elif isinstance(res, List):
        cash[tg_id] = res
    return len(cash[tg_id])

@app.get("/get_file/",
         tags=["TikTok"],
         summary="Get downloaded TikTok file after download")
async def get_file(tg_id: str) -> StreamingResponse:
    if tg_id not in cash:
        return None
    res = cash[tg_id].pop(0)
    if len(cash[tg_id]) == 0:
        cash.pop(tg_id)
    print(res["url"])
    return StreamingResponse(file_stream(res["url"], res["user_agent"]), media_type=res["media_type"])



if __name__ == "__main__":
    uvicorn.run("main:app", reload = True, port=8001)