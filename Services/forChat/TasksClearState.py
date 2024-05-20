from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller
import Services.AsyncTasks as tasks

class TasksClearState(UserState):
    async def start_msg(self):
        tasks.tasks_controller.tasks = []
        tasks.tasks_controller.save()
        return Response(text="Список очищено!", is_end=True, redirect="/menu")


