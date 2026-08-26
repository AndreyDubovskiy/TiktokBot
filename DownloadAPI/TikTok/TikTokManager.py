import asyncio

import time
import random
from typing import List

from DownloadAPI.TikTok.download1 import static_downloader1
from DownloadAPI.TikTok.download2 import static_downloader2

class TikTokManager:
    def __init__(self, count_limit: int = 0):
        self.count_limit = count_limit
        self.count = 0
        self.queue = []
        self.retry_queue = []
        self.times_to_retry = 3
        self.time_wait_retry = 2

        self.avg_time = 0

    def is_dont_limited(self):
        count_bool = self.count_limit == 0 or self.count < self.count_limit
        return count_bool

    def get_id_queue(self):
        index = 0
        while(True):
            if not (index in self.queue):
                self.queue.append(index)
                return index
            index += 1


    async def down(self, url: str) -> dict | List[dict] | None:
        self.count += 1
        start_time = time.time()
        list_downloaders = [
            static_downloader1.download,
            static_downloader2.download,
        ]
        res = None
        while(True):
            if len(list_downloaders) == 0:
                raise Exception("Error all")
            down = random.choice(list_downloaders)
            list_downloaders.remove(down)
            try:
                resp = await down(url)
                if resp is None:
                    continue
                res = resp
                break
            except Exception as ex:
                continue
        self.count -= 1
        end_time = time.time() - start_time
        if self.avg_time == 0:
            self.avg_time = end_time
        else:
            self.avg_time = (self.avg_time + end_time) / 2
        return res

    async def download(self, url: str) -> dict | List[dict] | None:
        if self.is_dont_limited() and len(self.queue) == 0:
            return await self.down(url)
        else:
            id_queue = self.get_id_queue()
            while(True):
                if self.queue[0] == id_queue:
                    if self.is_dont_limited():
                        self.queue.pop(0)
                        return await self.down(url)
                if self.avg_time == 0:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(self.avg_time)


static_tiktok_manager = TikTokManager()