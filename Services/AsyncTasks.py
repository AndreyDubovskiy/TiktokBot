import asyncio
import datetime
import time
import pickle

import markups
import config_controller
import db.database as db
import Services.Logger as log
from telebot.async_telebot import AsyncTeleBot
from telebot import types

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
        list_users = db.get_all_users()
        count = 0
        error = 0
        len_users = len(list_users)
        SLEEP_AFTER_SEC = 10
        MAX_COUNT = 50
        log.add_log("Start sending messages")
        for user in list_users:
            if count % MAX_COUNT == 0 and count != 0:
                await asyncio.sleep(SLEEP_AFTER_SEC)
            try:
                chat_id = user.tg_id
                text_post = config_controller.LIST_POSTS[current_name]['text']
                list_photos = config_controller.LIST_POSTS[current_name]['photos']
                list_videos = config_controller.LIST_POSTS[current_name]['videos']
                list_urls = config_controller.LIST_POSTS[current_name]['urls']
                markup_tpm = types.InlineKeyboardMarkup(row_width=2)
                current_url = 0
                for i in list_urls:
                    markup_tpm.add(types.InlineKeyboardButton(text="Перейти за посиланням",
                                                              callback_data="/geturl_" + current_name + "_" + str(
                                                                  current_url)))
                    current_url += 1
                if list_photos and len(list_photos) == 1 and text_post:
                    with open(list_photos[0], 'rb') as photo_file:
                        await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text_post,
                                                  reply_markup=markup_tpm)
                elif list_photos and len(list_photos) == 1:
                    with open(list_photos[0], 'rb') as photo_file:
                        await bot.send_photo(chat_id=chat_id, photo=photo_file, reply_markup=markup_tpm)
                elif list_photos and len(list_photos) > 1 and text_post:
                    media = []
                    for i in list_photos:
                        with open(i, 'rb') as photo_file:
                            media.append(types.InputMediaPhoto(media=photo_file))
                    await bot.send_media_group(chat_id=chat_id, media=media)
                    await bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                elif list_videos and len(list_videos) == 1 and text_post:
                    with open(list_videos[0], 'rb') as video_file:
                        await bot.send_video(chat_id=chat_id, video=video_file, caption=text_post,
                                                  reply_markup=markup_tpm)
                elif list_videos and len(list_videos) == 1:
                    with open(list_videos[0], 'rb') as video_file:
                        await bot.send_video(chat_id=chat_id, video=video_file, reply_markup=markup_tpm)
                elif text_post:
                    await bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                count += 1
            except Exception as ex:
                error += 1
                log.add_log(ex)
        await bot.send_message(chat_id=user_id, text="Розсилка закінчена!\nРозіслано людям: " + str(count) + "\nПомилок: " + str(error))
        log.add_log("Finish sending messages "+str(count) + "\nПомилок: " + str(error))
    except Exception as ex:
        log.add_log("FATAL ERROR - " + str(ex))

async def one_minute():
    while True:
        await asyncio.sleep(60)
        tmp = tasks_controller.get_task_by_time_now()
        if len(tmp) > 0:
            for i in tmp:
                await send(i.data['current_name'], i.data['user_id'])

