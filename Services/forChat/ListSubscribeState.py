from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller
import datetime
from Services.forStatistic.StatisticObj import StatisticObj

class ListSubscribeState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
        self.is_list = False
        self.name_suscribe = None
        self.edit = None
        self.newname = None
        self.newid = None
        self.newlink = None
    async def start_msg(self):
        if self.user_id in config_controller.list_is_loggin_admins or self.user_id in config_controller.list_is_loggin_moders:
            self.is_list = True
            return Response(text="УВАГА! Для перевірки підписок потрібно щоб бот був доданий у канал.\n\nОберіть, який канал хочете редагувати чи видалити:", buttons=markups.generate_subscribe_menu())
        else:
            return Response(text="У вас недостатньо прав!", is_end=True)

    async def next_msg(self, message: str):
        if self.edit == "link":
            if message == ".":
                self.newlink = config_controller.LIST_SUBSCRIBE[self.name_suscribe]['url']
            else:
                self.newlink = message
            self.edit = "id"
            return Response(text="Поточне id:\n"+config_controller.LIST_SUBSCRIBE[self.name_suscribe]['id']+"\n\nНапишіть наступним повідомленням нове id (Його можна дізнатись переславши будь-який пост канала, наприклад у бота https://t.me/getmyid_bot) (відішліть крапку, якщо хочете залишити минуле):", buttons=markups.generate_cancel())
        elif self.edit == "id":
            if message == ".":
                self.newid = config_controller.LIST_SUBSCRIBE[self.name_suscribe]['id']
            else:
                self.newid = message
            self.edit = None
            if config_controller.add_or_edit_subscribe(self.name_suscribe, self.newlink, self.newid):
                return Response(text="Успішно збережено!", is_end=True, redirect="/listsubscribe")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/listsubscribe")
        elif self.edit == "newname":
            self.newname = message
            self.edit = "newlink"
            return Response(text="Напишіть наступним повідомленням нове посилання:", buttons=markups.generate_cancel())
        elif self.edit == "newlink":
            self.newlink = message
            self.edit = "newid"
            return Response(text="Напишіть наступним повідомленням нове id (Його можна дізнатись переславши будь-який пост канала, наприклад у бота https://t.me/getmyid_bot):", buttons=markups.generate_cancel())
        elif self.edit == "newid":
            self.newid = message
            self.edit = None
            if config_controller.add_or_edit_subscribe(self.newname, self.newlink, self.newid):
                return Response(text="Успішно!", is_end=True, redirect="/listsubscribe")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/listsubscribe")
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
        obj_stat = StatisticObj()
        namefile, count = obj_stat.get_file_name_and_count_statistic(self.start, self.end, self.user_id, by=self.typestat, filtr="joinFromNeed_"+str(config_controller.LIST_SUBSCRIBE[self.name_suscribe]['id']))
        with open(namefile, 'rb') as file:
            await self.bot.send_photo(chat_id=self.user_id, photo=file, caption="Переходи по посиланню "+config_controller.LIST_SUBSCRIBE[self.name_suscribe]['url'] + "\nВсього кліків за цей проміжок: " + str(count))

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.is_list:
                return Response(is_end=True, redirect="/listsubscribe")
            else:
                return Response(is_end=True, redirect="/menu")
        if self.is_list:
            if data_btn == "/edit" and self.name_suscribe != None:
                self.edit = "link"
                return Response(text="Поточне посилання:\n"+config_controller.LIST_SUBSCRIBE[self.name_suscribe]['url']+"\n\nНапишіть наступним повідомленням нове посилання (відішліть крапку, якщо хочете залишити минуле):", buttons=markups.generate_cancel())
            elif data_btn == "/day":
                self.typestat = "day"
                await self.generate_stat()
                return Response(is_end=True, redirect="/listsubscribe")
            elif data_btn == "/month":
                self.typestat = "month"
                await self.generate_stat()
                return Response(is_end=True, redirect="/listsubscribe")
            elif data_btn == "/year":
                self.typestat = "year"
                await self.generate_stat()
                return Response(is_end=True, redirect="/listsubscribe")
            elif data_btn == "/stat":
                self.edit = "statstart"
                return Response(text="Уведіть початкову дату для статистики у фарматі дд-мм-рррр",
                                buttons=markups.generate_cancel())
            elif data_btn == "/delete" and self.name_suscribe != None:
                if config_controller.del_subscribe(self.name_suscribe):
                    return Response(text="Успішно видалено!", is_end=True, redirect="/listsubscribe")
                else:
                    return Response(text="Помилка!", is_end=True, redirect="/listsubscribe")
            elif data_btn == "/add":
                self.edit = "newname"
                return Response(text="Напишіть наступним повідомленням нову назву:", buttons=markups.generate_cancel())
            elif data_btn in config_controller.LIST_SUBSCRIBE:
                self.name_suscribe = data_btn
                return Response(text="Назва: "+data_btn+"\nUrl: "+config_controller.LIST_SUBSCRIBE[data_btn]['url']+"\nID: " + str(config_controller.LIST_SUBSCRIBE[data_btn]['id']), buttons=markups.generate_subscribe_semimenu())

