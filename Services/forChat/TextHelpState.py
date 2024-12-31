from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller

class TextHelpState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
        self.is_login = False
    async def start_msg(self):
        self.is_login = True
        return Response(text="Введіть наступним повідомленням текст для допомоги", buttons=markups.generate_cancel())

    async def next_msg(self, message: str):
        if self.is_login:
            res = config_controller.change_text_help(self.user_id, self.message_obj.html_text)
            if res:
                return Response(text="Ви замінили текст!", is_end=True, redirect="/menu")
            else:
                return Response(text="У вас недостатньо прав!", is_end=True, redirect="/menu")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return None