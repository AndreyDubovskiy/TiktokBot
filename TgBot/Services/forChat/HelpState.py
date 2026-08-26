from TgBot.Services.forChat.UserState import UserState
from TgBot.Services.forChat.Response import Response
from TgBot import config_controller


class HelpState(UserState):
    async def start_msg(self):
        return Response(text=config_controller.TEXT_HELP, is_end=True)

    async def next_msg(self, message: str):
        pass

    async def next_btn_clk(self, data_btn: str):
        pass