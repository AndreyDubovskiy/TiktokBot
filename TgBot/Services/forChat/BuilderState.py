from telebot.async_telebot import AsyncTeleBot
from TgBot.Services.forChat.UserState import UserState
from TgBot.Services.forChat.StartState import StartState
from TgBot.Services.forChat.LogState import LogState
from TgBot.Services.forChat.HelpAdminState import HelpAdminState
from TgBot.Services.forChat.PasswordModerState import PasswordModerState
from TgBot.Services.forChat.PasswordAdminState import PasswordAdminState
from TgBot.Services.forChat.TextAfterState import TextAfterState
from TgBot.Services.forChat.TextHelpState import TextHelpState
from TgBot.Services.forChat.TextHelloState import TextHelloState
from TgBot.Services.forChat.TextContactState import TextContactState
from TgBot.Services.forChat.HelpState import HelpState
from TgBot.Services.forChat.MenuState import MenuState
from TgBot.Services.forChat.ListSubscribeState import ListSubscribeState
from TgBot.Services.forChat.PostState import PostState
from TgBot.Services.forChat.GeturlState import GeturlState
from TgBot.Services.forChat.BoolafterState import BoolafterState
from TgBot.Services.forChat.TasksState import TasksState
from TgBot.Services.forChat.TasksClearState import TasksClearState
from TgBot.Services.forChat.YoutubeState import YoutubeState
from TgBot.Services.forChat.StatusSendState import StatusSendState

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
            "/intro": MenuState,
            "/listsubscribe": ListSubscribeState,
            "/postlist": PostState,
            "/geturl": GeturlState,
            "/boolafter": BoolafterState,
            "/tasks": TasksState,
            "/tasksclear": TasksClearState,
            "/youtube": YoutubeState,
            "/status_send": StatusSendState,
        }
        return clssses[data_txt](user_id, user_chat_id, bot)