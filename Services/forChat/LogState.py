from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller

class LogState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
        self.is_login = False
    async def start_msg(self):
        self.is_login = True
        return Response(text="Введіть наступним повідомленням ваш пароль", buttons=markups.generate_cancel())

    async def next_msg(self, message: str):
        if self.is_login:
            res = config_controller.log(self.user_id, message)
            if res == 1:
                return Response(text="Ви успішно залогінились як модер!", is_end=True, redirect="/menu")
            elif res == 2:
                return Response(text="Ви успішно залогінились як адмін!", is_end=True, redirect="/menu")
            else:
                return Response(text="Не правильний пароль! Спробуте знову!", buttons=markups.generate_cancel())

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return None