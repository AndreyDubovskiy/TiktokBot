from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller

class MenuState(UserState):
    async def start_msg(self):
        return Response(text="Меню для адмінів та модераторів", buttons=markups.generate_markup_menu(), is_end=True)
