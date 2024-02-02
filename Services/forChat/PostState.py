import datetime

from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from Services.forStatistic.StatisticObj import StatisticObj
import markups
import config_controller
import db.database as db

class PostState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
        self.current_page = 0
        self.max_on_page = 5
        self.edit = None
        self.current_name = None
        self.newname = None
        self.newurls = None
        self.newphotos = None
        self.newvideos = None
        self.newtext = None
    async def start_msg(self):
        if self.user_id in config_controller.list_is_loggin_admins or self.user_id in config_controller.list_is_loggin_moders:
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page, self.max_on_page))
        else:
            return Response(text="У вас недостатньо прав!", is_end=True)

    async def next_msg(self, message: str):
        if not (self.user_id in config_controller.list_is_loggin_admins or self.user_id in config_controller.list_is_loggin_moders):
            return Response(text="У вас недостатньо прав!", is_end=True)
        if self.edit == "addname":
            self.newname = message
            self.edit = "addpost"
            return Response(text="Відправте пост одним повідомленням (можна з фото або відео, та текстом, але одним повідомленням):")
        elif self.edit == "addpost":
            self.newtext = message
            self.edit = "addurls"
            return Response(
                text="Напишіть посилання, які потрібно додати до поста (якщо не одне посилання, то кожне посилання з нового рядка. Але одним повідомленням):", buttons=markups.generate_cancel())
        elif self.edit == "addurls":
            self.newurls = message.split("\n")
            self.edit = None
            if config_controller.add_or_edit_post(self.newname, text=self.newtext, urls=self.newurls, photos=self.newphotos, videos=self.newvideos):
                return Response(text="Успішно додано!", is_end=True, redirect="/postlist")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/postlist")
        elif self.edit == "statstart":
            self.edit = "statend"
            if message.count("-") > 0:
                day = int(message.split("-")[0])
                month = int(message.split("-")[1])
                year = int(message.split("-")[2])
            else:
                day = int(message.split(".")[0])
                month = int(message.split(".")[1])
                year = int(message.split(".")[2])
            self.start = datetime.datetime(year=year, month=month, day=day)
            return Response(text="Уведіть кінцеву дату для статистики у фарматі дд-мм-рррр", buttons=markups.generate_cancel())
        elif self.edit == "statend":
            self.edit = None
            if message.count("-") > 0:
                day = int(message.split("-")[0])
                month = int(message.split("-")[1])
                year = int(message.split("-")[2])
            else:
                day = int(message.split(".")[0])
                month = int(message.split(".")[1])
                year = int(message.split(".")[2])
            self.end = datetime.datetime(year=year, month=month, day=day)
            return Response(text="Оберіть інтервал для статистики", buttons=markups.generate_markup_day_month_year())

    async def generate_stat(self):
        list_files_name = []
        list_files_count = []
        obj_stat = StatisticObj()
        index = 0
        for url in config_controller.LIST_POSTS[self.current_name]['urls']:
            namefile, count = obj_stat.get_file_name_and_count_statistic(self.start, self.end, self.user_id, by=self.typestat, filtr="joinFrom_"+self.current_name+"_"+str(index))
            list_files_name.append(namefile)
            list_files_count.append(count)
            index+=1
        index = 0
        for i in list_files_name:
            with open(i, 'rb') as file:
                await self.bot.send_photo(chat_id=self.user_id, photo=file, caption="Переходи по посиланню "+config_controller.LIST_POSTS[self.current_name]['urls'][index] + "\nВсього кліків за цей проміжок: " + str(list_files_count[index]))
                index+=1
    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_name == None:
                return Response(is_end=True, redirect="/menu")
            else:
                return Response(is_end=True, redirect="/postlist")
        elif data_btn == "/day":
            self.typestat = "day"
            await self.generate_stat()
            return Response(is_end=True, redirect="/postlist")
        elif data_btn == "/month":
            self.typestat = "month"
            await self.generate_stat()
            return Response(is_end=True, redirect="/postlist")
        elif data_btn == "/year":
            self.typestat = "year"
            await self.generate_stat()
            return Response(is_end=True, redirect="/postlist")
        elif data_btn == "/next":
            if len(config_controller.LIST_POSTS)-((self.current_page+1)*self.max_on_page) > 0:
                self.current_page+=1
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page*self.max_on_page, self.max_on_page))
        elif data_btn =="/prev":
            if self.current_page > 0:
                self.current_page-=1
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page*self.max_on_page, self.max_on_page))
        elif data_btn in config_controller.LIST_POSTS:
            self.current_name = data_btn
            print(config_controller.LIST_POSTS[self.current_name])
            text = ""
            if config_controller.LIST_POSTS[self.current_name]['photos'] != None:
                text+= "\nКількість прикріплених фото: " + str(len(config_controller.LIST_POSTS[self.current_name]['photos'])) + "\n"
            if config_controller.LIST_POSTS[self.current_name]['videos'] != None:
                text+= "\nКількість прикріплених відео: " + str(len(config_controller.LIST_POSTS[self.current_name]['videos'])) + "\n"
            if config_controller.LIST_POSTS[self.current_name]['text'] != None:
                text+="\nТекст поста:\n" + config_controller.LIST_POSTS[self.current_name]['text']
            return Response(text="Назва поста: " + self.current_name + text, buttons=markups.generate_post_semimenu())
        elif data_btn == "/add":
            self.edit = "addname"
            return Response(text="Напишіть назву поста наступним повідомленням (для себе, користувачам не надсилається):", buttons=markups.generate_cancel())
        elif data_btn == "/delete":
            if config_controller.del_post(self.current_name):
                return Response(text="Успішно видалено!", is_end=True, redirect="/postlist")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/postlist")
        elif data_btn == "/stat":
            self.edit = "statstart"
            return Response(text="Уведіть початкову дату для статистики у фарматі дд-мм-рррр", buttons=markups.generate_cancel())
        elif data_btn == "/send":
            list_users = db.get_all_users()
            count = 0
            error = 0
            await self.bot.send_message(chat_id=self.user_id, text="Розсилка розпочата, очікуйте повідомлення про закінчення")
            for user in list_users:
                try:
                    chat_id = user.tg_id
                    text_post = config_controller.LIST_POSTS[self.current_name]['text']
                    list_photos = config_controller.LIST_POSTS[self.current_name]['photos']
                    list_videos = config_controller.LIST_POSTS[self.current_name]['videos']
                    list_urls = config_controller.LIST_POSTS[self.current_name]['urls']
                    markup_tpm = types.InlineKeyboardMarkup(row_width=2)
                    current_url = 0
                    for i in list_urls:
                        markup_tpm.add(types.InlineKeyboardButton(text="Перейти за посиланням", callback_data="/geturl_"+self.current_name+"_"+str(current_url)))
                        current_url+=1
                    if list_photos and len(list_photos) == 1 and text_post:
                        with open(list_photos[0], 'rb') as photo_file:
                            await self.bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text_post, reply_markup=markup_tpm)
                    elif list_photos and len(list_photos) == 1:
                        with open(list_photos[0], 'rb') as photo_file:
                            await self.bot.send_photo(chat_id=chat_id, photo=photo_file, reply_markup=markup_tpm)
                    elif list_photos and len(list_photos) > 1 and text_post:
                        media = []
                        for i in list_photos:
                            with open(i, 'rb') as photo_file:
                                media.append(types.InputMediaPhoto(media=photo_file))
                        await self.bot.send_media_group(chat_id=chat_id, media=media)
                        await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                    elif list_videos and len(list_videos) == 1 and text_post:
                        with open(list_videos[0], 'rb') as video_file:
                            await self.bot.send_video(chat_id=chat_id, video=photo_file, caption=text_post, reply_markup=markup_tpm)
                    elif list_videos and len(list_videos) == 1:
                        with open(list_videos[0], 'rb') as video_file:
                            await self.bot.send_video(chat_id=chat_id, video=photo_file, reply_markup=markup_tpm)
                    elif text_post:
                        await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                    count+=1
                except Exception as ex:
                    error+=1
            return Response(text="Розсилка закінчена!\nРозіслано людям: "+str(count)+"\nПомилок: "+str(error), is_end=True, redirect="/postlist")






    async def next_msg_photo_and_video(self, message: types.Message):
        if self.edit == "addpost":
            self.newtext = message.caption
            if message.photo:
                self.newphotos = []
                i = message.photo[-1]
                file_info = await self.bot.get_file(i.file_id)
                file_path = file_info.file_path
                bytess = await self.bot.download_file(file_path)
                with open(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.jpg', 'wb') as file:
                    file.write(bytess)
                self.newphotos.append(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.jpg')
            if message.video:
                self.newvideos = []
                i = message.video
                file_info = await self.bot.get_file(i.file_id)
                file_path = file_info.file_path
                bytess = await self.bot.download_file(file_path)
                with open(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.mp4', 'wb') as file:
                    file.write(bytess)
                self.newvideos.append(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.mp4')
            self.edit = "addurls"
            return Response(text="Напишіть посилання, які потрібно додати до поста (якщо не одне посилання, то кожне посилання з нового рядка. Але одним повідомленням):", buttons=markups.generate_cancel())