from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import Services.Logger as log

import markups
import config_controller
import db.database as db

class GeturlState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot):
        super().__init__(user_id, user_chat_id, bot)
    async def start_msg(self):
        pass

    async def next_msg(self, message: str):
        pass

    async def next_btn_clk(self, data_btn: str):
        pass

    async def next_btn_clk_message(self, data_btn:str, message: types.Message):
        try:
            name = data_btn.split("_")[1]
            url_ind = int(data_btn.split("_")[2])
            buttons_dict = []
            print("WORK", name, url_ind)
            if name in config_controller.LIST_POSTS:
                dict_list = message.reply_markup.to_dict()['inline_keyboard']
                for row in dict_list:
                    for btn in row:
                        buttons_dict.append(btn)
            markup_tpm = types.InlineKeyboardMarkup(row_width=2)
            for i in buttons_dict:
                if data_btn == i.get("callback_data", None):
                    markup_tpm.add(types.InlineKeyboardButton(text=i['text'], url=config_controller.LIST_POSTS[name]['urls'][url_ind]))
                    db.add_user_event_by_tg_id(user_tg_id=self.user_id, event_name="joinFrom_"+name+"_"+str(url_ind))
                else:
                    if i.get("callback_data", None) != None:
                        markup_tpm.add(types.InlineKeyboardButton(text=i['text'], callback_data=i['callback_data']))
                    else:
                        markup_tpm.add(types.InlineKeyboardButton(text=i['text'], url=i['url']))

            await self.bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup=markup_tpm)
        except Exception as ex:
            print(ex)
            log.add_log(str(ex))
        return None
