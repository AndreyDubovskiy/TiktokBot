import datetime

from pydantic import BaseModel
from typing import Optional

class EventScheme(BaseModel):
    name: str
    user_id: int

class EventWithTimeScheme(EventScheme):
    date_event: datetime.datetime

class EventWithIdScheme(EventWithTimeScheme):
    id: int

class EventOnlyIdScheme(BaseModel):
    id: int

class EventStartEndFilterScheme(BaseModel):
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]
    filter: Optional[str]