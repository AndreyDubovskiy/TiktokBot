import json

class UserModel():

    def __init__(self,id:int = None, tg_id: str = None, tg_name: str = None):
        self.id = id
        self.tg_id = tg_id
        self.tg_name = tg_name

    def to_json(self):
        return json.dumps(self.__dict__)