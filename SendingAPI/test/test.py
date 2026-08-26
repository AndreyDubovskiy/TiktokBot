import httpx
import asyncio
import json
import os


BASE_URL = "http://127.0.0.1:8002"
URL = BASE_URL + "/send_message/"

async def send_only_text(user_id: int):
    data = {
        "user_id": user_id,
        "text": f"Hello, user {user_id}!"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def send_only_photo(user_id: int, photo_path: str):
    data = {
        "user_id": user_id,
        "text": f"Hello, user {user_id}!"
    }
    files = {
        "photos": open(photo_path, "rb")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data, files=files)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def send_only_video(user_id: int, video_path: str):
    data = {
        "user_id": user_id,
        "text": f"Hello, user {user_id}!"
    }
    files = {
        "videos": open(video_path, "rb")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data, files=files)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def send_text_and_photo(user_id: int, photo_path: str):
    data = {
        "user_id": user_id,
        "text": f"Hello, user {user_id}!"
    }
    files = {
        "photos": open(photo_path, "rb")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data, files=files)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def send_text_and_video(user_id: int, video_path: str):
    data = {
        "user_id": user_id,
        "text": f"Hello, user {user_id}!"
    }
    files = {
        "videos": open(video_path, "rb")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data, files=files)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def send_text_buttons(user_id: int):
    data = {
        "user_id": str(user_id),
        "text": f"Hello, user {user_id}!",
        "buttons": json.dumps([
            {"text": "Button 1", "callback_data": "button_1"},
            {"text": "Button 2", "callback_data": "button_2"}
        ])
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(URL, data=data)
        print(f"User {user_id}: {response.status_code}, {response.text}")

async def main():
    #await send_only_text(653682367)
    #await send_only_photo(653682367, "sample.png")
    #await send_only_video(653682367, "sample.mp4")
    #await send_text_and_photo(653682367, "sample.png")
    #await send_text_and_video(653682367, "sample.mp4")
    await send_text_buttons(653682367)

asyncio.run(main())
