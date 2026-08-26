from TgBot.Services.forChat.UserState import UserState
from TgBot.Services.forChat.Response import Response
from TgBot import config_controller, markups


class BoolafterState(UserState):
    async def start_msg(self):
        config_controller.change_sended_aftervideo()
        return Response(text="Меню для адмінів та модераторів", buttons=markups.generate_markup_menu(), is_end=True)

    async def next_msg(self, message: str):
        pass

    async def next_btn_clk(self, data_btn: str):
        pass