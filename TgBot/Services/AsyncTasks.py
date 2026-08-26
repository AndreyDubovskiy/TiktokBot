import asyncio
import datetime
import pickle

from TgBot import config_controller
import TgBot.Services.Logger as log
from telebot.async_telebot import AsyncTeleBot
from TgBot.Services.utils_for_api.forSendApi import static_send_api

bot: AsyncTeleBot = None

class Task:
    def __init__(self, date_time, data):
        self.time = date_time
        self.data = data


class AsyncTasksController:
    def __init__(self):
        self.tasks = []
        self.load()

    def save(self):
        with open('tasks.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)

    def load(self):
        try:
            with open('tasks.pickle', 'rb') as f:
                self.tasks = pickle.load(f)
        except Exception as ex:
            self.tasks = []

    def add_task(self, date_time, data):
        self.tasks.append(Task(date_time, data))
        self.save()

    def get_task_by_time_now(self):
        tmp = []
        time_now = datetime.datetime.now() + datetime.timedelta(hours=3)
        for i in self.tasks:
            if time_now >= i.time:
                tmp.append(i)
                self.tasks.remove(i)
        self.save()
        return tmp


tasks_controller = AsyncTasksController()


async def send(current_name, user_id):
    try:
        text_post = config_controller.LIST_POSTS[current_name]['text']
        list_photos = config_controller.LIST_POSTS[current_name]['photos']
        list_videos = config_controller.LIST_POSTS[current_name]['videos']
        list_entities = config_controller.LIST_POSTS[current_name]['entities']
        list_urls = config_controller.LIST_POSTS[current_name]['urls']
        list_buttons = []
        for i in list_urls:
            list_buttons.append({"text": "Показати посилання",
                                 "callback_data": "/geturl_" + current_name + "_" + str(list_urls.index(i))})
        res = await static_send_api.send_message_to_all(text=text_post, photos=list_photos, videos=list_videos,
                                                        buttons=list_buttons, entities=list_entities)

    except Exception as ex:
        log.add_log("FATAL ERROR - " + str(ex))

async def one_minute():
    while True:
        await asyncio.sleep(60)
        tmp = tasks_controller.get_task_by_time_now()
        if len(tmp) > 0:
            for i in tmp:
                await send(i.data['current_name'], i.data['user_id'])

