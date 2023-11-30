import os
import pickle

TEXT_HELLO = "Щоб завантажити відео з TikTok просто відправте боту посилання на відео.\n\nПриклад:\nhttps://vt.tiktok.com/ZSNuePTTP/"
TEXT_HELP = "Щоб завантажити відео з TikTok просто відправте боту посилання на відео.\n\nПриклад:\nhttps://vt.tiktok.com/ZSNuePTTP/"
TEXT_AFTER_VIDEO = "‼️ Хто хоче купить або продать ТікТок ак, то вам сюди  - @tik_tok_om 🤝"
CONTACT_HELP = "Нажаль виникла помилка"

PASSWORD_ADMIN = "admin"
PASSWORD_MODER = "moder"

LIST_SUBSCRIBE = {"Канал 1": {"url": "https://t.me/forexcrypta",
                              "id": "-1001759220899"}}

list_is_loggin_admins = []
list_is_loggin_moders = []

list_user_action = {}

def preload_config():
    if os.path.exists("config.bin"):
        read_ini()
    else:
        write_ini()
def write_ini():
    config = {}
    config["TEXT_HELLO"] = TEXT_HELLO
    config["TEXT_HELP"] = TEXT_HELP
    config["TEXT_AFTER_VIDEO"] = TEXT_AFTER_VIDEO
    config["CONTACT_HELP"] = CONTACT_HELP
    config["PASSWORD_ADMIN"] = PASSWORD_ADMIN
    config["PASSWORD_MODER"] = PASSWORD_MODER
    config["LIST_SUBSCRIBE"] = LIST_SUBSCRIBE
    with open('config.bin', 'wb') as configfile:
        pickle.dump(config, configfile)

def read_ini():
    global TEXT_HELLO, TEXT_HELP, TEXT_AFTER_VIDEO, CONTACT_HELP, PASSWORD_ADMIN, PASSWORD_MODER, LIST_SUBSCRIBE
    with open('config.bin', 'rb') as configfile:
        config = pickle.load(configfile)
        TEXT_HELLO = str(config["TEXT_HELLO"])
        TEXT_HELP = str(config["TEXT_HELP"])
        TEXT_AFTER_VIDEO = str(config["TEXT_AFTER_VIDEO"])
        CONTACT_HELP = str(config["CONTACT_HELP"])
        PASSWORD_ADMIN = str(config["PASSWORD_ADMIN"])
        PASSWORD_MODER = str(config["PASSWORD_MODER"])
        LIST_SUBSCRIBE = config.get("LIST_SUBSCRIBE", LIST_SUBSCRIBE)

def log(chat_id, password):
    global list_is_loggin_admins, list_is_loggin_moders
    if password == PASSWORD_MODER and (not chat_id in list_is_loggin_moders):
        list_is_loggin_moders.append(chat_id)
        return 1
    if password == PASSWORD_ADMIN and (not chat_id in list_is_loggin_admins):
        list_is_loggin_admins.append(chat_id)
        return 2
    return None

def change_password_moder(chat_id, password):
    global PASSWORD_MODER, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_admins:
        PASSWORD_MODER = password
        write_ini()
        list_is_loggin_moders = []
        return True
    else:
        return False

def change_password_admin(chat_id, password):
    global PASSWORD_ADMIN, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_admins:
        PASSWORD_ADMIN = password
        write_ini()
        list_is_loggin_admins = []
        return True
    else:
        return False

def change_text_after_video(chat_id, text):
    global TEXT_AFTER_VIDEO, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_moders or chat_id in list_is_loggin_admins:
        TEXT_AFTER_VIDEO = text
        write_ini()
        return True
    else:
        return False

def change_text_help(chat_id, text):
    global TEXT_HELP, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_moders or chat_id in list_is_loggin_admins:
        TEXT_HELP = text
        write_ini()
        return True
    else:
        return False

def change_text_hello(chat_id, text):
    global TEXT_HELLO, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_moders or chat_id in list_is_loggin_admins:
        TEXT_HELLO = text
        write_ini()
        return True
    else:
        return False

def change_text_contact(chat_id, text):
    global CONTACT_HELP, list_is_loggin_moders, list_is_loggin_admins
    if chat_id in list_is_loggin_moders or chat_id in list_is_loggin_admins:
        CONTACT_HELP = text
        write_ini()
        return True
    else:
        return False

def del_subscribe(key):
    global LIST_SUBSCRIBE
    if LIST_SUBSCRIBE.get(key, None) != None:
        LIST_SUBSCRIBE.__delitem__(key)
        write_ini()
        return True
    else:
        return False

def add_or_edit_subscribe(key, tg_link, tg_id):
    global LIST_SUBSCRIBE
    try:
        if get_size_subscribe() < 11:
            v_key = str(key)
            v_tg_id = tg_id
            v_tg_link = str(tg_link)
            LIST_SUBSCRIBE[v_key] = {'url': v_tg_link,
                                     'id': v_tg_id}
            write_ini()
            return True
        else:
            return False
    except Exception as ex:
        return False

def get_size_subscribe():
    return len(LIST_SUBSCRIBE)