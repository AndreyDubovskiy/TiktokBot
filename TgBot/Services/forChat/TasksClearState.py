from TgBot.Services.forChat.UserState import UserState
from TgBot.Services.forChat.Response import Response
import TgBot.Services.AsyncTasks as tasks

class TasksClearState(UserState):
    async def start_msg(self):
        tasks.tasks_controller.tasks = []
        tasks.tasks_controller.save()
        return Response(text="Список очищено!", is_end=True, redirect="/menu")


