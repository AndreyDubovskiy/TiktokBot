import datetime
import sys

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
import Services.Logger as log
import Services.AsyncTasks as tasks
import asyncio

from Services.download.instagramm.InstaManager import static_insta_manager

tokkey = '6784215022:AAEq6bC7yBjUS6wEV6wcToHXisb00sFbJLo'
#tokkey = '6338019607:AAGtmGTAKAZSSnNkQ3BbO0gkJm1_huVvhqI'

bot = AsyncTeleBot(tokkey)

tasks.bot = bot

list_user_cheked = []
list_user_left = []
list_user_unsubscribe = {}

state_list = {}

@bot.message_handler(commands=['get_time'])
async def off(message):
    await bot.send_message(chat_id=message.chat.id, text=str(datetime.datetime.now())+"\n"+str(datetime.datetime.now() + datetime.timedelta(hours=3)))

@bot.message_handler(commands=['get_log'])
async def off(message):
    with open(log.get_log(), 'rb') as file:
        await bot.send_document(chat_id=message.chat.id, document=file)

@bot.message_handler(commands=['log'])
async def off(message):
    tmp = ""
    if len(log.LOGGER_LIST) < 15:
        for i in range(0, len(log.LOGGER_LIST)):
            tmp += log.LOGGER_LIST[i]+"\n"
        await bot.send_message(chat_id=message.chat.id, text=tmp)
    else:
        for i in range(15, 1):
            tmp += log.LOGGER_LIST[-i]+"\n"
        await bot.send_message(chat_id=message.chat.id, text=tmp)

@bot.message_handler(commands=['log1'])
async def off(message):
    tmp = ""
    for i in range(31, 16):
        tmp += log.LOGGER_LIST[-i]+"\n"
    await bot.send_message(chat_id=message.chat.id, text=tmp)

@bot.chat_join_request_handler(func= lambda chat_invite: str(chat_invite.chat.id) in config_controller.get_list_id_subscribe() )
async def request_join(chat_invite: types.ChatJoinRequest):
    id_chanell = str(chat_invite.chat.id)
    user_id = str(chat_invite.from_user.id)
    if not (user_id in config_controller.LIST_SUBSCRIBE[config_controller.get_name_by_id_subscribe(id_chanell)]['request']):
        config_controller.LIST_SUBSCRIBE[config_controller.get_name_by_id_subscribe(id_chanell)]['request'].append(user_id)
        config_controller.write_ini()



@bot.message_handler(commands=['passwordadmin','help', 'passwordmoder', 'helpadmin', 'log', 'textafter', 'start', 'texthelp', 'texthello', 'textcontact','menu'])
async def passwordadmin(message):
    await handle_message(message)

@bot.message_handler(func=lambda message: message.text.startswith("https://www.instagram.com"), content_types=['text'])
async def download(message: types.Message):
    try:
        if await is_subscribe(message.from_user.id):
            chat_id = str(message.from_user.id) + str(message.chat.id)
            msg_del = await bot.send_message(chat_id=message.chat.id, text="Відео готується, декілька секунд...")
            files = await static_insta_manager.download(message.text, str(chat_id))
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)

            max_files = 10
            current_files = 0
            media_group = []
            file_rb_s = []
            for i in files:

                file_rb_s.append(open(i[1], 'rb'))
                if i[0] == "image":
                    media_group.append(types.InputMediaPhoto(media=file_rb_s[-1]))
                else:
                    media_group.append(types.InputMediaVideo(media=file_rb_s[-1]))
                current_files += 1
                if current_files >= max_files:
                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                    media_group = []
                    current_files = 0
            if current_files > 0:
                await bot.send_media_group(chat_id=message.chat.id, media=media_group)
            if config_controller.IS_SEND_AFTERVIDEO:
                await bot.send_message(chat_id=message.chat.id, text=config_controller.TEXT_AFTER_VIDEO,
                                       parse_mode="HTML")
            for i in file_rb_s:
                i.close()
            for i in files:
                try:
                    os.remove(i[1])
                except:
                    pass
        else:
            await bot.send_message(chat_id=message.chat.id, text="Ви не підписані на канал!\nДля користування ботом підпишіться на канали:", reply_markup=markups.generate_markup_subscribe())
    except Exception as ex:
        print(ex)
        await bot.reply_to(message, config_controller.CONTACT_HELP)
        await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)

@bot.message_handler(func=lambda message: message.text.startswith("https://www.tiktok.com") or message.text.startswith("https://vm.tiktok.com") or message.text.startswith("https://vt.tiktok.com"), content_types=['text'])
async def download(message: types.Message):
    try:
        if await is_subscribe(message.from_user.id):
            chat_id = str(message.from_user.id) + str(message.chat.id)
            msg_del = await bot.send_message(chat_id=message.chat.id, text="Відео готується, декілька секунд...")
            print("Start DOWNLOAD")
            what, this, music = None, None, None
            iter_num = 0
            iter_max = 5
            while(True):
                if iter_num > iter_max:
                    break
                try:
                    what, this, music = await downloader.down_async(message.text, str(chat_id))
                except:
                    iter_num += 1
                    continue
                break
            print("END DOWNLOAD", what, this, music)
            await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)
            if what == 'video':
                with open(str(chat_id) + ".mp4", 'rb') as file:
                    print("try send ", message.chat.id)
                    await bot.send_video(chat_id=message.chat.id, video=file)
                if config_controller.IS_SEND_AFTERVIDEO:
                    await bot.send_message(chat_id=message.chat.id, text=config_controller.TEXT_AFTER_VIDEO, parse_mode="HTML")
                os.remove(str(chat_id) + ".mp4")
            elif what == 'photo':
                media_group = []
                for photo in this:
                    if len(media_group)+1 > 10:
                        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                        media_group = []
                    media_group.append(types.InputMediaPhoto(media=open(photo, 'rb')))
                await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                with open(music, 'rb') as mus:
                    await bot.send_audio(chat_id=message.chat.id, audio=mus)
                if config_controller.IS_SEND_AFTERVIDEO:
                    await bot.send_message(chat_id=message.chat.id, text=config_controller.TEXT_AFTER_VIDEO, parse_mode="HTML")
                for photo in this:
                    os.remove(photo)
                os.remove(music)
            elif what == None:
                await bot.reply_to(message, config_controller.CONTACT_HELP)
        else:
            await bot.send_message(chat_id=message.chat.id, text="Ви не підписані на канал!\nДля користування ботом підпишіться на канали:", reply_markup=markups.generate_markup_subscribe())
    except Exception as ex:
        print(ex)
        await bot.reply_to(message, config_controller.CONTACT_HELP)
        await bot.delete_message(chat_id=msg_del.chat.id, message_id=msg_del.id)

@bot.callback_query_handler(func= lambda call: True)
async def callback(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    chat_id = str(call.message.chat.id)
    text = call.data
    id_list = user_id+chat_id
    if call.data == '/check':
        if await is_subscribe(str(call.from_user.id)):
            await bot.send_message(call.message.chat.id, "Ви підписались! Тепер можете користуватись ботом")
        else:
            await bot.send_message(call.message.chat.id, "Ви ще не підписались!")
            return
    if state_list.get(id_list, None) != None:
        state: UserState = state_list[id_list]
        res: Response = await state.next_btn_clk(text)
        await chek_response(chat_id, user_id, id_list, res)
    else:
        builder = BuilderState(bot)
        if not text.startswith("/geturl"):
            state = builder.create_state(text, user_id, chat_id, bot)
        else:
            state = builder.create_state("/geturl", user_id, chat_id, bot)
        state_list[id_list] = state
        if not text.startswith("/geturl"):
            res: Response = await state.start_msg()
            await chek_response(chat_id, user_id, id_list, res)
        else:
            res: Response = await state.next_btn_clk_message(text, call.message)
            await chek_response(chat_id, user_id, id_list, res)
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
        await chek_response(user_chat_id, user_id, id_list, res)

async def get_list_unsubscribe(user_id):
    res_list = []
    for i in config_controller.LIST_SUBSCRIBE:
        try:
            res = await bot.get_chat_member(chat_id=int(config_controller.LIST_SUBSCRIBE[i]['id']), user_id=int(user_id))
            if res.status == "left" and not(str(user_id) in config_controller.LIST_SUBSCRIBE[i]['request']):
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
            if res.status == "left" and not(str(chat_id) in config_controller.LIST_SUBSCRIBE[i]['request']):
                list_user_left.append(chat_id)
                list_user_unsubscribe[str(chat_id)] = await get_list_unsubscribe(chat_id)
                return False
            else:
                if str(chat_id) in config_controller.LIST_SUBSCRIBE[i]['request'] and res.status != "left":
                    config_controller.LIST_SUBSCRIBE[i]['request'].remove(str(chat_id))
                    config_controller.write_ini()
        if chat_id in list_user_left:
            if not db.is_created_user(user_tg_id=chat_id):
                db.create_user(user_tg_id=chat_id, user_name="None")
            for i in list_user_unsubscribe[str(chat_id)]:
                db.add_user_event_by_tg_id(user_tg_id=chat_id, event_name="joinFromNeed_"+str(i))
            list_user_left.remove(chat_id)
            list_user_unsubscribe.pop(str(chat_id))
        return True
    except Exception as ex:
        print("error", ex)
        return True

async def chek_response(user_chat_id, user_id, id_list, res: Response = None):
    if res != None:
        await res.send(user_chat_id, bot)
        if res.is_end:
            state_list.pop(id_list)
        if res.redirect != None:
            builder = BuilderState(bot)
            state = builder.create_state(res.redirect, user_id, user_chat_id, bot)
            state_list[id_list] = state
            res: Response = await state.start_msg()
            await chek_response(user_chat_id, user_id, id_list, res)
    else:
        state_list.pop(id_list)
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    id_list = user_id+user_chat_id
    text = message.text
    if state_list.get(id_list, None) == None:
        builder = BuilderState(bot)
        state = builder.create_state(text, user_id, user_chat_id, bot)
        state.message_obj = message
        state_list[id_list] = state
        res: Response = await state.start_msg()
        await chek_response(user_chat_id, user_id, id_list, res)
    else:
        state: UserState = state_list[id_list]
        state.message_obj = message
        res: Response = await state.next_msg(text)
        await chek_response(user_chat_id, user_id, id_list, res)



config_controller.preload_config()


async def main_fun():
    tmp1 = asyncio.create_task(bot.polling())
    tmp2 = asyncio.create_task(tasks.one_minute())
    print("START")
    try:
        await tmp1
        sys.exit()
    except Exception as ex:
        sys.exit()
    await tmp2


asyncio.run(main_fun())