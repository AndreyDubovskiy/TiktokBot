import downloader
import markups
import config_controller
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import os
import db.database as db
from Services.forChat.BuilderState import BuilderState
from Services.forChat.UserState import UserState
from Services.forChat.Response import Response

tokkey = '6784215022:AAEq6bC7yBjUS6wEV6wcToHXisb00sFbJLo'

bot = AsyncTeleBot(tokkey)

list_user_cheked = []
list_user_left = []
list_user_unsubscribe = {}

state_list = {}

@bot.message_handler(commands=['passwordadmin','help', 'passwordmoder', 'helpadmin', 'log', 'textafter', 'start', 'texthelp', 'texthello', 'textcontact','menu'])
async def passwordadmin(message):
    await handle_message(message)

@bot.message_handler(func=lambda message: message.text.startswith("https://www.tiktok.com") or message.text.startswith("https://vm.tiktok.com") or message.text.startswith("https://vt.tiktok.com"), content_types=['text'])
async def download(message: types.Message):
    try:
        if await is_subscribe(message.from_user.id):
            chat_id = str(message.from_user.id) + str(message.chat.id)
            msg_del = await bot.send_message(chat_id=message.chat.id, text="Відео готується, декілька секунд...")
            downloader.down(message.text, str(chat_id)+".mp4")
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)
            with open(str(chat_id) + ".mp4", 'rb') as file:
                await bot.send_video(chat_id=message.chat.id, video=file)
            await bot.send_message(chat_id=message.chat.id, text=config_controller.TEXT_AFTER_VIDEO)
            os.remove(str(chat_id) + ".mp4")
        else:
            await bot.send_message(chat_id=message.chat.id, text="Ви не підписані на канал!\nДля користування ботом підпишіться на канали:", reply_markup=markups.generate_markup_subscribe())
    except Exception as ex:
        try:
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)
            await bot.reply_to(message, config_controller.CONTACT_HELP)
            return
            chat_id = str(message.from_user.id) + str(message.chat.id)
            print("Start Foto", chat_id, message.text)
            downloader.get_video_from_foto_tiktok(message.text, chat_id)
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)
            with open(str(chat_id) + ".mp4", 'rb') as file:
                await bot.send_video(chat_id=message.chat.id, video=file)
            os.remove(str(chat_id) + ".mp4")
            await bot.send_message(chat_id=message.chat.id, text=config_controller.TEXT_AFTER_VIDEO)
        except Exception as ex:
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)
            await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.callback_query_handler(func= lambda call: True)
async def callback(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    chat_id = str(call.message.chat.id)
    text = call.data
    id_list = user_id+chat_id
    print(text, user_id, state_list.get(id_list, None))
    if call.data == '/check':
        if await is_subscribe(str(call.from_user.id)):
            await bot.send_message(call.message.chat.id, "Ви підписались! Тепер можете користуватись ботом")
        else:
            await bot.send_message(call.message.chat.id, "Ви ще не підписались!")
            return
    if state_list.get(id_list, None) != None:
        state: UserState = state_list[id_list]
        res: Response = await state.next_btn_clk(text)
        if res != None:
            await res.send(chat_id, bot)
            if res.is_end:
                state_list.pop(id_list)
        else:
            state_list.pop(id_list)
    else:
        builder = BuilderState(bot)
        if not text.startswith("/geturl"):
            state = builder.create_state(text, user_id, chat_id, bot)
        else:
            state = builder.create_state("/geturl", user_id, chat_id, bot)
        state_list[id_list] = state
        if not text.startswith("/geturl"):
            res: Response = await state.start_msg()
            if res != None:
                await res.send(chat_id, bot)
                if res.is_end:
                    state_list.pop(id_list)
            else:
                state_list.pop(id_list)
        else:
            res: Response = await state.next_btn_clk_message(text, call.message)
            if res != None:
                await res.send(chat_id, bot)
                if res.is_end:
                    state_list.pop(id_list)
            else:
                state_list.pop(id_list)
    if not text.startswith("/geturl"):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

@bot.message_handler(func=lambda message: True, content_types=['text'])
async def comand(message: types.Message):
    await handle_message(message)

@bot.message_handler(func=lambda message: True, content_types=["photo", "video"])
async def comand(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    id_list = user_id + user_chat_id
    if state_list.get(id_list, None) == None:
        return
    else:
        state: UserState = state_list[id_list]
        res: Response = await state.next_msg_photo_and_video(message)
        if res != None:
            await res.send(user_chat_id, bot)
            if res.is_end:
                state_list.pop(id_list)
        else:
            state_list.pop(id_list)

async def get_list_unsubscribe(user_id):
    res_list = []
    for i in config_controller.LIST_SUBSCRIBE:
        try:
            res = await bot.get_chat_member(chat_id=int(config_controller.LIST_SUBSCRIBE[i]['id']), user_id=int(user_id))
            if res.status == "left":
                res_list.append(config_controller.LIST_SUBSCRIBE[i]['id'])
        except Exception as ex:
            print(ex)
    return res_list

async def is_subscribe(chat_id):
    global list_user_cheked, list_user_left, list_user_unsubscribe
    try:
        if chat_id in config_controller.list_is_loggin_admins or chat_id in config_controller.list_is_loggin_moders:
            return True
        if not(chat_id in list_user_cheked):
            if not db.is_created_user(user_tg_id=chat_id):
                db.create_user(user_tg_id=chat_id, user_name="None")
            list_user_cheked.append(chat_id)
        for i in config_controller.LIST_SUBSCRIBE:
            res = await bot.get_chat_member(chat_id=int(config_controller.LIST_SUBSCRIBE[i]['id']), user_id=int(chat_id))
            if res.status == "left":
                list_user_left.append(chat_id)
                list_user_unsubscribe[str(chat_id)] = await get_list_unsubscribe(chat_id)
                return False
        if chat_id in list_user_left:
            if not db.is_created_user(user_tg_id=chat_id):
                db.create_user(user_tg_id=chat_id, user_name="None")
            for i in list_user_unsubscribe[str(chat_id)]:
                db.add_user_event_by_tg_id(user_tg_id=chat_id, event_name="joinFromNeed_"+str(i))
            list_user_left.remove(chat_id)
            list_user_unsubscribe.pop(str(chat_id))
        return True
    except Exception as ex:
        print("error")
        return True


async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    id_list = user_id+user_chat_id
    text = message.text
    print(text, user_id, state_list.get(id_list, None))
    if state_list.get(id_list, None) == None:
        builder = BuilderState(bot)
        state = builder.create_state(text, user_id, user_chat_id, bot)
        state_list[id_list] = state
        res: Response = await state.start_msg()
        if res != None:
            await res.send(user_chat_id, bot)
            if res.is_end:
                state_list.pop(id_list)
        else:
            state_list.pop(id_list)
    else:
        state: UserState = state_list[id_list]
        res: Response = await state.next_msg(text)
        if res != None:
            await res.send(user_chat_id, bot)
            if res.is_end:
                state_list.pop(id_list)
        else:
            state_list.pop(id_list)



config_controller.preload_config()

import asyncio
asyncio.run(bot.polling())