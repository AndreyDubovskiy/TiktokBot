from datetime import datetime
import json

class EventModel():

    def __init__(self, id:int = None, name: str = None, user_id: int = None, date_event: datetime = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.date_event = date_event

    def to_json(self):
        return json.dumps(self.__dict__)