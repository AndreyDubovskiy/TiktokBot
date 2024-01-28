from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller

class HelpAdminState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
    async def start_msg(self):
        return Response(text="/log <пароль> - для логіну адміна або модера\n/passwordmoder <пароль> - зміна паролю для модера\n/passwordadmin <пароль> - зміна паролю для адміна\n/textafter <текст> - зміна тексту, що відправляється після відео\n/texthelp <текст> - зміна тексту допомоги\n/texthello <текст> - зміна тексту при старті\n/textcontact <текст> - текст що висвічується під час помилок (контакти допомоги тощо)", is_end=True)