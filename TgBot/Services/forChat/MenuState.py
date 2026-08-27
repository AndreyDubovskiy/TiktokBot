from Services.forChat.UserState import UserState
from Services.forChat.Response import Response
import markups


class MenuState(UserState):
    async def start_msg(self):
        return Response(text="Меню для адмінів та модераторів", buttons=markups.generate_markup_menu(), is_end=True)

