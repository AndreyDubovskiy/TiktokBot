from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
import config_controller

class StartState(UserState):
    async def start_msg(self):
        return Response(text=config_controller.TEXT_HELLO, is_end=True)