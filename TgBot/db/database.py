import datetime
import httpx
import os

URL = os.getenv("DATABASE_API_BASE_URL", "http://127.0.0.1:8000")

from TgBot.db.models.UserModel import UserModel
from TgBot.db.models.EventModel import EventModel
from typing import List

async def delete_user(user_id:int) -> bool:
    async with httpx.AsyncClient() as client:
        res = await client.post(URL+"/users/delete/",
                                json={"id": user_id})
        if res.status_code != 200:
            return False
        return True

async def get_all_users_new(offset:int = 0,
                        limit:int = 100) -> List[UserModel]:
    async with httpx.AsyncClient() as client:
        res = await client.get(URL+"/users/all/",
                               params={"offset": offset,
                                       "limit": limit})
        if res.status_code != 200:
            return []
        return [UserModel(**user) for user in res.json()]

async def get_all_users() -> List[UserModel]:
    async with httpx.AsyncClient() as client:
        offset = 0
        limit = 100
        result = []
        while True:
            res = await client.get(URL+"/users/all/",
                                   params={
                                       "offset": 0,
                                       "limit": 100
                                   })
            if res.status_code != 200:
                return []
            else:
                result.extend([UserModel(**user) for user in res.json()])
                offset += limit
                if len(res.json()) < 1:
                    break
        return result

async def is_created_user(user_name=None,
                          user_tg_id=None,
                          user_id=None
                          ) -> bool:
    async with httpx.AsyncClient() as client:
        params = {}
        if user_name:
            params["user_name"] = user_name
        if user_tg_id:
            params["user_tg_id"] = str(user_tg_id)
        if user_id:
            params["user_id"] = user_id
        res = await client.get(URL+"/users/",
                               params=params)
        if res.json() == None:
            print("ERROR CHECK USER")
            return False
        print(res.json())
        return True


async def create_user(user_name: str, user_tg_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        print("CREATE USER",URL+"/users/create/" , {"tg_name": user_name,
                                      "tg_id": user_tg_id})
        res = await client.post(URL+"/users/create/",
                                json={"tg_name": user_name,
                                      "tg_id": str(user_tg_id)})
        if res.status_code != 200:
            return False
        return True

async def get_user(user_name: str = None,
                   user_tg_id: str = None,
                   user_id: int = None) -> UserModel | None:
    async with httpx.AsyncClient() as client:
        params = {}
        if user_name:
            params["user_name"] = user_name
        if user_tg_id:
            params["user_tg_id"] = str(user_tg_id)
        if user_id:
            params["user_id"] = user_id
        res = await client.get(URL+"/users/", params=params)
        if res.status_code != 200:
            return None
        return UserModel(**res.json())

async def get_user_events(user_id: int) -> List[EventModel]:
    async with httpx.AsyncClient() as client:
        res = await client.get(URL+"/events/",
                               params={"user_id": user_id})
        if res.status_code != 200:
            return []
        return [EventModel(**event) for event in res.json()]

async def add_user_event(user_id: int, event_name: str) -> bool:
    async with httpx.AsyncClient() as client:
        res = await client.post(URL+"/events/create/",
                                json={"user_id": user_id,
                                      "name": event_name})
        if res.status_code != 200:
            return False
        return True

async def add_user_event_by_tg_id(user_tg_id: str, event_name: str) -> bool:
    async with httpx.AsyncClient() as client:
        res = await client.post(URL+"/events/create/",
                                json={"user_id": (await get_user(user_tg_id=str(user_tg_id))).id,
                                      "name": event_name})
        if res.status_code != 200:
            return False
        return True

async def get_events_by_datetime(start: datetime.datetime = None, end: datetime.datetime = None, filter:str = None) -> List[EventModel]:
    async with httpx.AsyncClient() as client:
        params = {}
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()
        if filter:
            params["filter"] = filter
        res = await client.get(URL+"/events/by_datetime_and_filter/", params=params)
        if res.status_code != 200:
            return []
        return [EventModel(**event) for event in res.json()]