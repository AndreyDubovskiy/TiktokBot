from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller
import Services.AsyncTasks as tasks

class TasksState(UserState):
    async def start_msg(self):
        if len(tasks.tasks_controller.tasks) == 0:
            return Response(text="Список пустий!", is_end=True, redirect="/menu")
        try:
            text = ""
            for i in tasks.tasks_controller.tasks:
                text += f"{i.time} - {i.data['current_name']}\n"
            return Response(text=text, is_end=True, redirect="/menu")
        except Exception as ex:
            text = ""
            for i in range(0, 15):
                text += f"{tasks.tasks_controller.tasks[i].time} - {tasks.tasks_controller.tasks[i].data['current_name']}\n"
            text += "Та інші..."
            return Response(text=text, is_end=True, redirect="/menu")


