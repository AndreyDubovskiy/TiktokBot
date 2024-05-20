from telebot.async_telebot import AsyncTeleBot
from telebot import types
from Services.forChat.UserState import UserState
from Services.forChat.StartState import StartState
from Services.forChat.LogState import LogState
from Services.forChat.HelpAdminState import HelpAdminState
from Services.forChat.PasswordModerState import PasswordModerState
from Services.forChat.PasswordAdminState import PasswordAdminState
from Services.forChat.TextAfterState import TextAfterState
from Services.forChat.TextHelpState import TextHelpState
from Services.forChat.TextHelloState import TextHelloState
from Services.forChat.TextContactState import TextContactState
from Services.forChat.HelpState import HelpState
from Services.forChat.MenuState import MenuState
from Services.forChat.ListSubscribeState import ListSubscribeState
from Services.forChat.PostState import PostState
from Services.forChat.GeturlState import GeturlState
from Services.forChat.BoolafterState import BoolafterState
from Services.forChat.TasksState import TasksState
from Services.forChat.TasksClearState import TasksClearState

class BuilderState:
    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot

    def create_state(self, data_txt: str, user_id: str, user_chat_id: str, bot: AsyncTeleBot) -> UserState:
        clssses = {
            "/start": StartState,
            "/log": LogState,
            "/help": HelpState,
            "/helpadmin": HelpAdminState,
            "/passwordmoder": PasswordModerState,
            "/passwordadmin": PasswordAdminState,
            "/textafter": TextAfterState,
            "/texthelp": TextHelpState,
            "/texthello": TextHelloState,
            "/textcontact": TextContactState,
            "/menu": MenuState,
            "/listsubscribe": ListSubscribeState,
            "/postlist": PostState,
            "/geturl": GeturlState,
            "/boolafter": BoolafterState,
            "/tasks": TasksState,
            "/tasksclear": TasksClearState
        }
        return clssses[data_txt](user_id, user_chat_id, bot)