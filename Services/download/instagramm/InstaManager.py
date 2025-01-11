import asyncio

from fake_useragent import UserAgent
import time
import Services.download.instagramm.downloader as insta_downloader


# async def down_async(url, outfile):
#     return await asyncio.to_thread(down, url, outfile)


class InstaManager:
    def __init__(self, count_limit: int = 0, limit_memory_mb: int = 0):
        self.count_limit = count_limit
        self.limit_memory_mb = limit_memory_mb
        self.max_memory_mb = limit_memory_mb*1.5
        self.count = 0
        self.memory_mb = 0
        self.ua = UserAgent()

        self.queue = []

        self.avg_time = 0

    def is_dont_limited(self):
        count_bool = self.count_limit == 0 or self.count < self.count_limit
        memory_bool = self.limit_memory_mb == 0 or self.memory_mb < self.limit_memory_mb
        return count_bool and memory_bool

    def get_id_queue(self):
        index = 0
        while(True):
            if not (index in self.queue):
                self.queue.append(index)
                return index
            index += 1


    async def download_reels(self, url, file_name):
        self.count += 1
        start_time = time.time()

        files = await asyncio.to_thread(insta_downloader.download_reels_new, url, file_name)

        end_time = time.time()
        full_time = end_time - start_time
        if self.avg_time == 0:
            self.avg_time = full_time
        else:
            self.avg_time = (self.avg_time + full_time) / 2

        self.count -= 1
        return files

    async def download(self, url, file_name):
        if self.is_dont_limited() and len(self.queue) == 0:
            return await self.download_reels(url, file_name)
        else:
            id_queue = self.get_id_queue()
            while(True):
                if self.queue[0] == id_queue:
                    if self.is_dont_limited():
                        self.queue.pop(0)
                        return await self.download_reels(url, file_name)
                if self.avg_time == 0:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(self.avg_time)


static_insta_manager = InstaManager()




