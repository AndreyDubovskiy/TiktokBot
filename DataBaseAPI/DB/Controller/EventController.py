import datetime

from DataBaseAPI.DB.Model.EventModel import EventModel

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from typing import List

class EventController:
    async def create_event(self,session: AsyncSession, user_id: int, event_name: str):
        event = EventModel(event_name, user_id)
        session.add(event)
        await session.commit()

    async def get_user_events(self, session: AsyncSession, user_id: int) -> List[EventModel]:
        query = select(EventModel).where(EventModel.user_id==user_id)
        res: List[EventModel] = (await session.scalars(query)).all()
        return res

    async def delete_event(self, session: AsyncSession, event_id: int):
        query = select(EventModel).where(EventModel.id==event_id)
        res: EventModel = await session.scalar(query)
        if res:
            await session.delete(res)
            await session.commit()

    async def get_event(self, session: AsyncSession, event_id: int) -> EventModel | None:
        query = select(EventModel).where(EventModel.id==event_id)
        res: EventModel = await session.scalar(query)
        return res

    async def get_events_by_datetime_and_filter(self, session: AsyncSession, start: datetime.datetime = None, end: datetime.datetime = None, filter: str = None) -> List[EventModel]:
        query = select(EventModel)
        if start:
            query = query.where(EventModel.date_event >= start)
        if end:
            query = query.where(EventModel.date_event <= end)
        if filter:
            query = query.where(EventModel.name.startswith(filter))
        res: List[EventModel] = (await session.scalars(query)).all()
        return res