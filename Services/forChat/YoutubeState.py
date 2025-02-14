import requests

from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller
from Services.download.youtube.YoutubeManager import static_youtube_manager
import os

class YoutubeState(UserState):
    async def start_msg(self):
        self.url = self.message_obj.text
        rrrr = await static_youtube_manager.get_buttons_res_with_and_without_audio(self.url)
        self.with_audio = []
        self.without_audio = []

        for i in rrrr:
            if i.count("_a") > 0:
                self.with_audio.append(i)
            else:
                self.without_audio.append(i)



        return Response(text="Виберіть бажану якість:", buttons=markups.generate_markup_resolution(self.with_audio, self.without_audio))

    async def next_msg(self, message: str):
        raise Exception("Not implemented")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return Response(is_end=True)
        elif data_btn in self.with_audio:
            url_video = await static_youtube_manager.download_url(self.url, data_btn)
            try:
                await self.bot.send_video(self.user_chat_id, url_video)
            except:
                if len(static_youtube_manager.queue) > 0:
                    time_in_sec = static_youtube_manager.avg_time
                    total_in_sec = time_in_sec * len(static_youtube_manager.queue)
                    minutes = round(total_in_sec // 60)
                    seconds = round(total_in_sec % 60)
                    msg = await self.bot.send_message(
                        text=f"Через перенавантаження бота, ви у черзі на скачування\n\nПриблизний час очікування: {minutes}хв. {seconds}с.",
                        chat_id=self.user_chat_id)
                    file_name_video = await static_youtube_manager.download_url_file(self.url, self.user_chat_id, data_btn,
                                                                            self.bot, self.user_chat_id)
                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                    msg = await self.bot.send_message(chat_id=self.user_chat_id,
                                                      text="Відео завантажується у чат, трішки часу...")
                    file_size = os.path.getsize(file_name_video) / (1024 * 1024)
                    if file_size < 50:
                        with open(file_name_video, 'rb') as f:
                            await self.bot.send_video(self.user_chat_id, f)
                    else:
                        mm = await self.bot.send_message(chat_id=self.user_chat_id,
                                                         text="Відео більше 50мб, вивантажується, трішки зачекайте...")
                        url_uploaded_file = await static_youtube_manager.upload_file(file_name_video)
                        await self.bot.delete_message(chat_id=self.user_chat_id, message_id=mm.message_id)
                        await self.bot.send_message(self.user_chat_id,
                                                    text="Завантаження:\n<a href='" + url_uploaded_file + "'>Завантажити відео</a>",
                                                    parse_mode='HTML')

                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                    try:
                        os.remove(file_name_video)
                    except:
                        pass
                    static_youtube_manager.memory_mb -= \
                    (await static_youtube_manager.get_length_video(self.url, data_btn, True))[1]
                else:
                    msg = await self.bot.send_message(
                        text=f"Завантаження відео...",
                        chat_id=self.user_chat_id)
                    file_name_video = await static_youtube_manager.download_url_file(self.url, self.user_chat_id, data_btn,
                                                                            self.bot,
                                                                            self.user_chat_id)
                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                    msg = await self.bot.send_message(chat_id=self.user_chat_id,
                                                      text="Відео вивантажується, трішки часу...")
                    file_size = os.path.getsize(file_name_video) / (1024 * 1024)
                    if file_size < 50:
                        with open(file_name_video, 'rb') as f:
                            await self.bot.send_video(self.user_chat_id, f)
                    else:
                        mm = await self.bot.send_message(chat_id=self.user_chat_id, text="Відео більше 50мб, вивантажується, трішки зачекайте...")
                        url_uploaded_file = await static_youtube_manager.upload_file(file_name_video)
                        await self.bot.delete_message(chat_id=self.user_chat_id, message_id=mm.message_id)
                        await self.bot.send_message(self.user_chat_id, text="Завантаження:\n<a href='" + url_uploaded_file + "'>Завантажити відео</a>", parse_mode='HTML')
                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                    try:
                        os.remove(file_name_video)
                    except:
                        pass
                    static_youtube_manager.memory_mb -= \
                    (await static_youtube_manager.get_length_video(self.url, data_btn, True))[1]

            if config_controller.IS_SEND_AFTERVIDEO:
                return Response(text=config_controller.TEXT_AFTER_VIDEO, is_end=True)
            else:
                return Response(is_end=True)
        elif data_btn in self.without_audio:
            if len(static_youtube_manager.queue) > 0:
                time_in_sec = static_youtube_manager.avg_time
                total_in_sec = time_in_sec * len(static_youtube_manager.queue)
                minutes = round(total_in_sec // 60)
                seconds = round(total_in_sec % 60)
                msg = await self.bot.send_message(text=f"Через перенавантаження бота, ви у черзі на скачування\n\nПриблизний час очікування: {minutes}хв. {seconds}с.", chat_id=self.user_chat_id)
                file_name_video = await static_youtube_manager.download(self.url, self.user_chat_id, data_btn, self.bot, self.user_chat_id)
                await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                msg = await self.bot.send_message(chat_id=self.user_chat_id, text="Відео завантажується у чат, трішки часу...")
                file_size = os.path.getsize(file_name_video) / (1024 * 1024)
                if file_size < 50:
                    with open(file_name_video, 'rb') as f:
                        await self.bot.send_video(self.user_chat_id, f)
                else:
                    mm = await self.bot.send_message(chat_id=self.user_chat_id,
                                                     text="Відео більше 50мб, вивантажується, трішки зачекайте...")
                    url_uploaded_file = await static_youtube_manager.upload_file(file_name_video)
                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=mm.message_id)
                    await self.bot.send_message(self.user_chat_id,
                                                text="Завантаження:\n<a href='" + url_uploaded_file + "'>Завантажити відео</a>",
                                                parse_mode='HTML')

                await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                try:
                    os.remove(file_name_video)
                except:
                    pass
                static_youtube_manager.memory_mb -= (await static_youtube_manager.get_length_video(self.url, data_btn))[1]
                if config_controller.IS_SEND_AFTERVIDEO:
                    return Response(text=config_controller.TEXT_AFTER_VIDEO, is_end=True)
                else:
                    return Response(is_end=True)
            else:
                file_name_video = await static_youtube_manager.download(self.url, self.user_chat_id, data_btn, self.bot,
                                                                        self.user_chat_id)
                msg = await self.bot.send_message(chat_id=self.user_chat_id,
                                                  text="Відео завантажується у чат, трішки часу...")
                file_size = os.path.getsize(file_name_video) / (1024 * 1024)
                if file_size < 50:
                    with open(file_name_video, 'rb') as f:
                        await self.bot.send_video(self.user_chat_id, f)
                else:
                    mm = await self.bot.send_message(chat_id=self.user_chat_id,
                                                     text="Відео більше 50мб, вивантажується, трішки зачекайте...")
                    url_uploaded_file = await static_youtube_manager.upload_file(file_name_video)
                    await self.bot.delete_message(chat_id=self.user_chat_id, message_id=mm.message_id)
                    await self.bot.send_message(self.user_chat_id,
                                                text="Завантаження:\n<a href='" + url_uploaded_file + "'>Завантажити відео</a>",
                                                parse_mode='HTML')
                await self.bot.delete_message(chat_id=self.user_chat_id, message_id=msg.message_id)
                try:
                    os.remove(file_name_video)
                except:
                    pass
                static_youtube_manager.memory_mb -= (await static_youtube_manager.get_length_video(self.url, data_btn))[1]
                if config_controller.IS_SEND_AFTERVIDEO:
                    return Response(text=config_controller.TEXT_AFTER_VIDEO, is_end=True)
                else:
                    return Response(is_end=True)

