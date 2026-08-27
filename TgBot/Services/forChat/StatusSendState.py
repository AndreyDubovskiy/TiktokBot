from Services.forChat.UserState import UserState
from Services.forChat.Response import Response

from Services.utils_for_api.forSendApi import static_send_api

class StatusSendState(UserState):
    async def start_msg(self):
        res = await static_send_api.get_broadcast_status()
        ttt = "Статус розсилки:\n"
        active = "active"
        history = "history"
        ttt += "Активні розсилки:\n"
        iii = 0
        for i in res[active]:
            iii+=1
            ttt += str(iii) + " | " + str(res[active][i]) + "\n"
        ttt += "Виконані розсилки:\n"
        iii = 0
        for i in res[history]:
            iii+=1
            ttt += str(iii) + " | " + str(res[history][i]) + "\n"
        return Response(text=ttt, is_end=True)