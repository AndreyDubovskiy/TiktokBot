import datetime

from sqlalchemy import create_engine
from db.models.BaseModel import BaseModel
from db.models.UserModel import UserModel
from db.models.EventModel import EventModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

engine = create_engine("sqlite:///mainbase.db", echo=False)

BaseModel.metadata.create_all(engine)


def get_all_users():
    with Session(engine) as session:
        query = select(UserModel)
        res: List[UserModel] = session.scalars(query).all()

    return res


def is_created_user(user_name=None, user_tg_id=None, user_id=None):
    with Session(engine) as session:
        query = select(UserModel)
        if user_name:
            query = query.where(UserModel.tg_name==user_name)
        if user_tg_id:
            query = query.where(UserModel.tg_id==user_tg_id)
        if user_id:
            query = query.where(UserModel.id==user_id)

        res: UserModel = session.scalar(query)

    if res:
        return True
    else:
        return False



def create_user(user_name, user_tg_id):
    with Session(engine) as session:
        user = UserModel(user_tg_id, user_name)
        session.add(user)
        session.commit()

def get_user(user_name=None, user_tg_id=None, user_id=None):
    with Session(engine) as session:
        query = select(UserModel)
        if user_name:
            query = query.where(UserModel.tg_name==user_name)
        if user_tg_id:
            query = query.where(UserModel.tg_id==user_tg_id)
        if user_id:
            query = query.where(UserModel.id==user_id)

        res: UserModel = session.scalar(query)

    return res

def get_user_events(user_id):
    with Session(engine) as session:
        query = select(EventModel).where(EventModel.user_id==user_id)
        res: List[EventModel] = session.scalars(query).all()

    return res

def add_user_event(user_id, event_name):
    with Session(engine) as session:
        event = EventModel(event_name, user_id)
        session.add(event)
        session.commit()

def add_user_event_by_tg_id(user_tg_id, event_name):
    user = get_user(user_tg_id=user_tg_id)
    add_user_event(user.id, event_name)

def get_events_by_datetime(start: datetime.datetime, end: datetime.datetime, filter:str = None):
    with Session(engine) as session:
        if filter:
            query = select(EventModel).where(EventModel.name.startswith(filter)).where(EventModel.date_event >= start).where(EventModel.date_event<=end)
        else:
            query = select(EventModel).where(EventModel.date_event >= start).where(EventModel.date_event <= end)
        res: List[EventModel] = session.scalars(query).all()

    return res