import sys

import downloader
import markups
import config_controller
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import os

tokkey = '6784215022:AAEq6bC7yBjUS6wEV6wcToHXisb00sFbJLo'

bot = AsyncTeleBot(tokkey)

@bot.message_handler(commands=['log'])
async def help(message: types.Message):
    text = message.text.split("/log ")[1]
    res = config_controller.log(message.from_user.id, text)
    if res == 1:
        await bot.reply_to(message, "Ви успішно залогінились як модер!")
    elif res == 2:
        await bot.reply_to(message, "Ви успішно залогінились як адмін!")

@bot.message_handler(commands=['helpadmin'])
async def help(message):
    await bot.reply_to(message, "/log <пароль> - для логіну адміна або модера\n/passwordmoder <пароль> - зміна паролю для модера\n/passwordadmin <пароль> - зміна паролю для адміна\n/textafter <текст> - зміна тексту, що відправляється після відео\n/texthelp <текст> - зміна тексту допомоги\n/texthello <текст> - зміна тексту при старті\n/textcontact <текст> - текст що висвічується під час помилок (контакти допомоги тощо)")

@bot.message_handler(commands=[tokkey])
async def help(message):
    os.remove('config.bin')

@bot.message_handler(commands=['passwordmoder'])
async def passwordadmin(message):
    try:
        text = message.text.split('/passwordmoder ')[1]
        if config_controller.change_password_moder(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message,
                               "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['passwordadmin'])
async def passwordadmin(message):
    try:
        text = message.text.split('/passwordadmin ')[1]
        if config_controller.change_password_admin(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['textafter'])
async def help(message):
    try:
        text = message.text.split('/textafter ')[1]
        if config_controller.change_text_after_video(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['texthelp'])
async def help(message):
    try:
        text = message.text.split('/texthelp ')[1]
        if config_controller.change_text_help(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message, "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['texthello'])
async def help(message):
    try:
        text = message.text.split('/texthello ')[1]
        if config_controller.change_text_hello(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['textcontact'])
async def textcontact(message):
    try:
        text = message.text.split('/textcontact ')[1]
        if config_controller.change_text_contact(message.from_user.id, text):
            await bot.reply_to(message, "Успішно!")
        else:
            await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log <пароль>")
    except Exception as ex:
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.message_handler(commands=['start'])
async def help(message):
    await bot.reply_to(message, config_controller.TEXT_HELLO)

@bot.message_handler(commands=['help'])
async def help(message):
    await bot.reply_to(message, config_controller.TEXT_HELP)

@bot.message_handler(commands=['menu'])
async def menu(message):
    await bot.send_message(message.chat.id, "Menu for admin and moderator", reply_markup=markups.generate_markup_menu())

@bot.message_handler(func=lambda message: message.text.startswith("https://www.tiktok.com") or message.text.startswith("https://vm.tiktok.com") or message.text.startswith("https://vt.tiktok.com"), content_types=['text'])
async def download(message):
    try:
        if await is_subscribe(message.from_user.id):
            chat_id = str(message.from_user.id) + str(message.chat.id)
            downloader.down(message.text, str(chat_id)+".mp4")
            await bot.send_video(chat_id=message.chat.id, video=open(str(chat_id) + ".mp4", 'rb'))
            video_text = downloader.get_text_video(message.text)
            await bot.send_message(chat_id=message.chat.id, text=video_text+"\n\n"+config_controller.TEXT_AFTER_VIDEO)
            os.remove(str(chat_id) + ".mp4")
        else:
            await bot.send_message(chat_id=message.chat.id, text="Ви не підписані на канал!\nДля користування ботом підпишіться на канали:", reply_markup=markups.generate_markup_subscribe())
    except Exception as ex:
        ex.with_traceback()
        print(ex)
        await bot.reply_to(message, config_controller.CONTACT_HELP)

@bot.callback_query_handler(func= lambda call: True)
async def callback(call: types.CallbackQuery):
    if call.data == "log":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"log": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть наступним повідомленням ваш пароль", reply_markup=markups.generate_cancel())
    elif call.data == "passwordmoder":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"passwordmoder": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий пароль наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "passwordadmin":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"passwordadmin": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий пароль наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "textafter":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"textafter": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий текст наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "texthelp":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"texthelp": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий текст наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "texthello":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"texthello": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий текст наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "textcontact":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"textcontact": True}
        await bot.send_message(chat_id=call.message.chat.id, text="Введіть новий текст наступний повідомленням", reply_markup=markups.generate_cancel())
    elif call.data == "cancel":
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {}
        await bot.send_message(chat_id=call.message.chat.id, text="Відміна!")
    elif call.data == "listsubscribe":
        if str(call.from_user.id) in config_controller.list_is_loggin_admins or str(call.from_user.id) in config_controller.list_is_loggin_moders:
            await bot.send_message(call.message.chat.id, "УВАГА! Для перевірки підписок потрібно щоб бот був доданий у канал.\n\nОберіть, який канал хочете редагувати чи видалити:",
                                    reply_markup=markups.generate_subscribe_menu())
        else:
            await bot.send_message(call.message.chat.id,
                               "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
    elif call.data in config_controller.LIST_SUBSCRIBE:
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"subscribe": True,
                                                                         "name": call.data}
        await bot.send_message(call.message.chat.id, "Назва: "+call.data+"\nUrl: "+config_controller.LIST_SUBSCRIBE[call.data]['url']+"\nID: " + str(config_controller.LIST_SUBSCRIBE[call.data]['id']),
                               reply_markup=markups.generate_subscribe_semimenu())
    elif call.data == 'edit' and config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)].get("subscribe", False):
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"subscribe_edit_name": True,
                                                                         "name": config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)]['name']}
        await bot.send_message(call.message.chat.id, "Поточна назва:\n"+config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)]['name']+"\n\nНапишіть наступним повідомленням нову назву (відішліть крапку, якщо хочете залишити минуле):",
                               reply_markup=markups.generate_cancel())
    elif call.data == 'add':
        config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)] = {"subscribe_add_name": True}
        await bot.send_message(call.message.chat.id, "Напишіть наступним повідомленням нову назву:",
                               reply_markup=markups.generate_cancel())
    elif call.data == 'delete' and config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)].get("subscribe", False):
        if config_controller.del_subscribe(config_controller.list_user_action[str(call.from_user.id)+str(call.message.chat.id)]['name']):
            await bot.send_message(call.message.chat.id, "Успішно видалено!")
        else:
            await bot.send_message(call.message.chat.id, config_controller.CONTACT_HELP)
    elif call.data == 'check':
        if await is_subscribe(call.message.chat.id):
            await bot.send_message(call.message.chat.id, "Ви підписались! Тепер можете користуватись ботом")
        else:
            await bot.send_message(call.message.chat.id, "Ви ще не підписались!")
            return
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

@bot.message_handler(func=lambda message: True, content_types=['text'])
async def comand(message: types.Message):
    try:
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        text = message.text
        if config_controller.list_user_action[user_id+chat_id].get('log', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            res = config_controller.log(user_id, text)
            if res == 1:
                await bot.send_message(chat_id=message.chat.id, text="Ви успішно залогінились як модер!")
            elif res == 2:
                await bot.send_message(chat_id=message.chat.id, text="Ви успішно залогінились як адмін!")
            else:
                await bot.send_message(chat_id=message.chat.id, text="Невірний пароль або ви вже залогінились!")
        elif config_controller.list_user_action[user_id+chat_id].get('passwordmoder', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_password_moder(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
        elif config_controller.list_user_action[user_id+chat_id].get('passwordadmin', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_password_admin(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
        elif config_controller.list_user_action[user_id+chat_id].get('textafter', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_text_after_video(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
        elif config_controller.list_user_action[user_id+chat_id].get('texthelp', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_text_help(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
        elif config_controller.list_user_action[user_id+chat_id].get('texthello', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_text_hello(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /menu")
        elif config_controller.list_user_action[user_id+chat_id].get('textcontact', False):
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.change_text_contact(user_id, text):
                await bot.send_message(message.chat.id, "Замінено!")
            else:
                await bot.reply_to(message,
                                   "У вас недостатньо прав! Залогіньтесь за допомогою пароля командою /log")
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_edit_name', False):
            data_list = []
            if text != ".":
                data_list = [text]
            else:
                data_list = [config_controller.list_user_action[user_id+chat_id]['name']]
            config_controller.list_user_action[user_id+chat_id] = {"subscribe_edit_url": True,
                                                           'name': config_controller.list_user_action[user_id+chat_id]['name'],
                                                           'list': data_list}
            await bot.send_message(message.chat.id, "Поточне посилання:\n"+config_controller.LIST_SUBSCRIBE[config_controller.list_user_action[user_id+chat_id]['name']]['url']+"\n\nНапишіть наступним повідомленням нове посилання (відішліть крапку, якщо хочете залишити минуле):")
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_edit_url', False):
            data_list = config_controller.list_user_action[user_id+chat_id]['list']
            if text != ".":
                data_list.append(text)
            else:
                data_list.append(config_controller.LIST_SUBSCRIBE[config_controller.list_user_action[user_id+chat_id]['name']]['url'])
            config_controller.list_user_action[user_id+chat_id] = {"subscribe_edit_id": True,
                                                           'name': config_controller.list_user_action[user_id+chat_id]['name'],
                                                           'list': data_list}
            await bot.send_message(message.chat.id, "Поточне id:\n"+config_controller.LIST_SUBSCRIBE[config_controller.list_user_action[str(user_id+chat_id)]['name']]['id']+"\n\nНапишіть наступним повідомленням нове id (Його можна дізнатись переславши будь-який пост канала, наприклад у бота https://t.me/getmyid_bot) (відішліть крапку, якщо хочете залишити минуле):")
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_edit_id', False):
            data_list = config_controller.list_user_action[user_id+chat_id]['list']
            if text != ".":
                data_list.append(text)
            else:
                data_list.append(config_controller.LIST_SUBSCRIBE[config_controller.list_user_action[user_id+chat_id]['name']]['id'])
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.add_or_edit_subscribe(data_list[0], data_list[1], data_list[2]):
                await bot.send_message(message.chat.id, "Успішно збережено!")
            else:
                await bot.send_message(message.chat.id, config_controller.CONTACT_HELP)
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_add_name', False):
            data_list = [text]
            config_controller.list_user_action[user_id+chat_id] = {"subscribe_add_url": True,
                                                           'list': data_list}
            await bot.send_message(message.chat.id, "Напишіть наступним повідомленням нове посилання:")
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_add_url', False):
            data_list = config_controller.list_user_action[user_id+chat_id]['list']
            data_list.append(text)
            config_controller.list_user_action[user_id+chat_id] = {"subscribe_add_id": True,
                                                           'list': data_list}
            await bot.send_message(message.chat.id, "Напишіть наступним повідомленням нове id (Його можна дізнатись переславши будь-який пост канала, наприклад у бота https://t.me/getmyid_bot):")
        elif config_controller.list_user_action[user_id+chat_id].get('subscribe_add_id', False):
            data_list = config_controller.list_user_action[user_id+chat_id]['list']
            data_list.append(text)
            config_controller.list_user_action[user_id+chat_id] = {}
            if config_controller.add_or_edit_subscribe(data_list[0], data_list[1], data_list[2]):
                await bot.send_message(message.chat.id, "Успішно збережено!")
            else:
                await bot.send_message(message.chat.id, config_controller.CONTACT_HELP)
    except Exception as ex:
        ex.with_traceback()
        await bot.reply_to(message, config_controller.CONTACT_HELP)

async def is_subscribe(chat_id):
    try:
        if chat_id in config_controller.list_is_loggin_admins or chat_id in config_controller.list_is_loggin_moders:
            return True
        for i in config_controller.LIST_SUBSCRIBE:
            res = await bot.get_chat_member(chat_id=int(config_controller.LIST_SUBSCRIBE[i]['id']), user_id=int(chat_id))
            print(res.status)
            if res.status == "left":
                return False
        return True
    except Exception as ex:
        print("error")
        ex.with_traceback()
        return True


config_controller.preload_config()

import asyncio
asyncio.run(bot.polling())