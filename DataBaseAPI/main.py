import datetime
from typing import List

import uvicorn
import asyncio

from DataBaseAPI.DB.Controller.EventController import EventController
from DataBaseAPI.DB.Controller.UserController import UserController
from DataBaseAPI.DB.db import create_all_tables, get_async_session, start_database
from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from DataBaseAPI.Scheme.UserScheme import (UserScheme,
                                           UserWithIdScheme,
                                           UserOnlyIdScheme,
                                           UserAllOptional )
from DataBaseAPI.Scheme.EventScheme import (EventScheme,
                                            EventWithTimeScheme,
                                            EventWithIdScheme,
                                            EventOnlyIdScheme,
                                            EventStartEndFilterScheme)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_database()
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/ok")
async def ok():
    return "OK"

@app.get("/users/all/",
         tags=["Users"],
         summary="Get all users")
async def get_all_users(offset:int = 0,
                        limit:int = 100,
                        session: AsyncSession = Depends(get_async_session)
                        ) -> List[UserWithIdScheme]:
    controller = UserController()
    users = await controller.get_all_users(session=session,
                                           offset=offset,
                                           limit=limit)
    return [UserWithIdScheme(id=user.id,
                            tg_id=user.tg_id,
                            tg_name=user.tg_name) for user in users]

@app.get("/users/",
         tags=["Users"],
         summary="Get user by name, tg_id or id")
async def get_users(user_name: str = None,
                    user_tg_id: str = None,
                    user_id: int = None,
                    session: AsyncSession = Depends(get_async_session)
                    ) -> UserWithIdScheme | None:
    controller = UserController()
    user = await controller.get_user(session=session,
                                     user_name=user_name,
                                     user_tg_id=user_tg_id,
                                     user_id=user_id)
    if user:
        return UserWithIdScheme(id=user.id,
                                tg_id=user.tg_id,
                                tg_name=user.tg_name)
    else:
        return None


@app.post("/users/create/",
          tags=["Users"],
          summary="Create new user")
async def create_user(user: UserScheme,
                      session: AsyncSession = Depends(get_async_session)
                      ) -> UserScheme:
    controller = UserController()
    await controller.create_user(session=session,
                                 user_name=user.tg_name,
                                 user_tg_id=user.tg_id)
    return UserScheme(tg_id=user.tg_id,
                      tg_name=user.tg_name)

@app.post("/users/update/",
          tags=["Users"],
          summary="Update user by id")
async def update_user(user: UserWithIdScheme,
                      session: AsyncSession = Depends(get_async_session)
                      ) -> UserWithIdScheme | None:
    controller = UserController()
    await controller.update_user(session=session,
                                 user_id=user.id,
                                 user_name=user.tg_name,
                                 user_tg_id=user.tg_id)
    user = await controller.get_user(session=session,
                                     user_id=user.id)
    if user:
        return UserWithIdScheme(id=user.id,
                                tg_id=user.tg_id,
                                tg_name=user.tg_name)
    else:
        return None

@app.post("/users/delete/",
          tags=["Users"],
          summary="Delete user by id")
async def delete_user(user: UserOnlyIdScheme,
                      session: AsyncSession = Depends(get_async_session)
                      ) -> bool:
    controller = UserController()
    await controller.delete_user(session=session,
                                 user_id=user.id)
    return True

@app.post("/events/create/",
          tags=["Events"],
          summary="Create new event")
async def create_event(event: EventScheme,
                       session: AsyncSession = Depends(get_async_session)
                       ) -> EventScheme:
    controller = EventController()
    await controller.create_event(session=session,
                                  user_id=event.user_id,
                                  event_name=event.name)
    return EventScheme(name=event.name,
                       user_id=event.user_id)

@app.get("/events/",
         tags=["Events"],
         summary="Get user events")
async def get_user_events(user_id: int,
                          session: AsyncSession = Depends(get_async_session)
                          ) -> List[EventWithIdScheme]:
    controller = EventController()
    events = await controller.get_user_events(session=session,
                                              user_id=user_id)
    return [EventWithIdScheme(id=event.id,
                              name=event.name,
                              user_id=event.user_id,
                              date_event=event.date_event) for event in events]

@app.post("/events/delete/",
          tags=["Events"],
          summary="Delete event by id")
async def delete_event(event: EventOnlyIdScheme,
                       session: AsyncSession = Depends(get_async_session)
                       ) -> None:
    controller = EventController()
    await controller.delete_event(session=session,
                                  event_id=event.id)
    return None

@app.get("/events/by_datetime_and_filter/",
         tags=["Events"],
         summary="Get events by datetime and filter")
async def get_events_by_datetime_and_filter(start: datetime.datetime = None,
                                            end: datetime.datetime = None,
                                            filter: str = None,
                                            session: AsyncSession = Depends(get_async_session)
                                            ) -> List[EventWithTimeScheme]:
    controller = EventController()
    events = await controller.get_events_by_datetime_and_filter(session=session,
                                                               start=start,
                                                               end=end,
                                                               filter=filter)
    return [EventWithTimeScheme(name=event.name,
                                user_id=event.user_id,
                                date_event=event.date_event) for event in events]








if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)