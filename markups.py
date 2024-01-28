from telebot import types
import config_controller

def generate_markup_subscribe():
    markup = types.InlineKeyboardMarkup(row_width=2)
    list_btn = []
    for i in config_controller.LIST_SUBSCRIBE:
        list_btn.append(types.InlineKeyboardButton(text="➕️ ПІДПИСАТИСЯ", url=config_controller.LIST_SUBSCRIBE[i]['url']))
    while len(list_btn) > 0:
        if len(list_btn) > 1:
            markup.add(list_btn[0], list_btn[1], row_width=2)
            del list_btn[1]
            del list_btn[0]
        else:
            markup.add(list_btn[0])
            del list_btn[0]
    markup.add(types.InlineKeyboardButton(text="👉 ПЕРЕВІРИТИ ПІДПИСКУ 👈", callback_data="/check"))
    return markup

def generate_post_menu(offset: int=0, max:int = 5):
    if offset > len(config_controller.LIST_POSTS):
        offset = 0
    current_elem = 0
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in config_controller.LIST_POSTS:
        current_elem+=1
        if current_elem > offset and current_elem-offset <= max:
            markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
        else:
            pass
    if len(config_controller.LIST_POSTS) >= max:
        markup.add(types.InlineKeyboardButton(text="-->", callback_data="/next"))
        markup.add(types.InlineKeyboardButton(text="<--", callback_data="/prev"))
    markup.add(types.InlineKeyboardButton(text="Додати", callback_data="/add"))
    markup.add(types.InlineKeyboardButton(text="Відмінити", callback_data="/cancel"))
    return markup

def generate_post_semimenu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Видалити", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="Розіслати", callback_data="/send"))
    markup.add(types.InlineKeyboardButton(text="Статистика", callback_data="/stat"))
    markup.add(types.InlineKeyboardButton(text="Відмінити", callback_data="/cancel"))
    return markup


def generate_cancel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Відмінити", callback_data="/cancel"))
    return markup

def generate_subscribe_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in config_controller.LIST_SUBSCRIBE:
        markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
    if config_controller.get_size_subscribe() < 10:
        markup.add(types.InlineKeyboardButton(text="Додати", callback_data="/add"))
    markup.add(types.InlineKeyboardButton(text="Відмінити", callback_data="/cancel"))
    return markup

def generate_subscribe_semimenu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Редагувати", callback_data="/edit"))
    markup.add(types.InlineKeyboardButton(text="Видалити", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="Статистика", callback_data="/stat"))
    markup.add(types.InlineKeyboardButton(text="Відмінити", callback_data="/cancel"))
    return markup

def generate_markup_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Ввести пароль", callback_data="/log"))
    markup.add(types.InlineKeyboardButton(text="Змінити пароль модера", callback_data="/passwordmoder"))
    markup.add(types.InlineKeyboardButton(text="Змінити пароль адміна", callback_data="/passwordadmin"))
    markup.add(types.InlineKeyboardButton(text="Змінити текст після відео", callback_data="/textafter"))
    markup.add(types.InlineKeyboardButton(text="Змінити текст /help", callback_data="/texthelp"))
    markup.add(types.InlineKeyboardButton(text="Змінити текст при старті", callback_data="/texthello"))
    markup.add(types.InlineKeyboardButton(text="Змінити текст при помилках", callback_data="/textcontact"))
    markup.add(types.InlineKeyboardButton(text="Список підписок", callback_data="/listsubscribe"))
    markup.add(types.InlineKeyboardButton(text="Список постів", callback_data="/postlist"))
    return markup

def generate_markup_day_month_year():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="По дням", callback_data="/day"))
    markup.add(types.InlineKeyboardButton(text="По місяцям", callback_data="/month"))
    markup.add(types.InlineKeyboardButton(text="По рокам", callback_data="/year"))
    markup.add(types.InlineKeyboardButton(text="Відміна", callback_data="/cancel"))
    return markup