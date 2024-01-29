from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller

class BoolafterState(UserState):
    async def start_msg(self):
        config_controller.change_sended_aftervideo()
        return Response(text="Меню для адмінів та модераторів", buttons=markups.generate_markup_menu(), is_end=True)

    async def next_msg(self, message: str):
        pass

    async def next_btn_clk(self, data_btn: str):
        pass