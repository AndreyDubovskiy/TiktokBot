import json

import httpx
import os

class SendApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def send_message(self, user_id: int, text: str = None, photos: list = None, videos: list = None, buttons: list = None, entities: list = None):
        data = {
            "user_id": user_id,
            "text": text,
            "buttons": json.dumps(buttons) if buttons else None,
            "entities": json.dumps(entities) if entities else None
        }
        files = {}
        if photos:
            for i, photo in enumerate(photos):
                files[f"photos[{i}]"] = open(photo, "rb")
        if videos:
            for i, video in enumerate(videos):
                files[f"videos[{i}]"] = open(video, "rb")

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/send_message/", data=data, files=files)
            if response.status_code == 200:
                return 200
            else:
                return 500

    async def send_message_to_all(self, text: str = None, photos: list = None, videos: list = None,
                                  buttons: list = None, entities: list = None):
        data = {
            "text": text,
            "buttons": json.dumps(buttons) if buttons else None,
            "entities": json.dumps(entities) if entities else None
        }

        files = []
        if photos:
            for photo in photos:
                files.append(("photos", open(photo, "rb")))
        if videos:
            for video in videos:
                files.append(("videos", open(video, "rb")))

        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            response = await client.post(
                f"{self.base_url}/send_message_to_all/",
                data=data,
                files=files if files else None
            )
            return 200 if response.status_code == 200 else 500

    async def get_broadcast_status(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/send_message_to_all_status/")
            if response.status_code == 200:
                return response.json()
            else:
                return None

static_send_api = SendApi(base_url=os.getenv("SEND_API_BASE_URL", "http://127.0.0.1:8002"))