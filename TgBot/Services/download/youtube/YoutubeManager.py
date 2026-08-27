import asyncio

from fake_useragent import UserAgent
import time
import Services.download.youtube.downloader as youtube_downloader
from Services.upload.fileconvoy.uploader import upload_file


# async def down_async(url, outfile):
#     return await asyncio.to_thread(down, url, outfile)


class YoutubeManager:
    def __init__(self, count_limit: int = 0, limit_memory_mb: int = 0):
        self.count_limit = count_limit
        self.limit_memory_mb = limit_memory_mb
        self.max_memory_mb = limit_memory_mb*1.5
        self.count = 0
        self.memory_mb = 0
        self.ua = UserAgent()

        self.queue = []

        self.avg_time = 60
        self.avg_time_per_sec = 0.1

    async def get_length_video(self, url, res, progressive: bool = False):

        quality, quality_f, audio_quality, audio_quality_f, info = await asyncio.to_thread(youtube_downloader.get_res_and_urls_and_size_and_time_new, url)

        filesize = None
        for i in quality_f:
            if i[0] == res:
                filesize = i[2]
                break
        return info, filesize

    async def upload_file(self, filename) -> str:
        return await asyncio.to_thread(upload_file, filename)

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

    async def get_buttons_res_with_and_without_audio(self, url):
        quality, quality_f, audio_quality, audio_quality_f, info = await asyncio.to_thread(youtube_downloader.get_res_and_urls_and_size_and_time_new, url)
        return quality


    async def download_video(self, url, file_name, res):
        self.count += 1

        files = await asyncio.to_thread(youtube_downloader.download_new, url, file_name, res)

        self.count -= 1
        return files

    async def download_url(self, url, res):
        quality, quality_f, audio_quality, audio_quality_f, info = await asyncio.to_thread(youtube_downloader.get_res_and_urls_and_size_and_time_new, url)
        url = None
        for i in quality_f:
            if i[0] == res:
                url = i[1]
                break
        return url

    async def download_url_file(self, url, file_name, res, bot = None, chat_id = None):
        if self.is_dont_limited() and len(self.queue) == 0:
            time_sec, filesize = await self.get_length_video(url, res)
            if filesize > (self.max_memory_mb - self.memory_mb) and self.max_memory_mb != 0:
                raise Exception("File size is too big")
            self.memory_mb += filesize
            quality, quality_f, audio_quality, audio_quality_f, info = await asyncio.to_thread(youtube_downloader.get_res_and_urls_and_size_and_time_new, url)
            for i in quality_f:
                if i[0] == res:
                    url = i[1]
                    break
            respons = await asyncio.to_thread(youtube_downloader.get_from_url, url, file_name)
            return respons
        else:
            id_queue = self.get_id_queue()
            while (True):
                if self.queue[0] == id_queue:
                    if self.is_dont_limited():
                        self.queue.pop(0)
                        time_video, file_size = await self.get_length_video(url, res)
                        if file_size > (self.max_memory_mb - self.memory_mb) and self.max_memory_mb != 0:
                            raise Exception("File size is too big")
                        self.memory_mb += file_size
                        msg = await bot.send_message(chat_id=chat_id,
                                                     text=f"Відео завантажується...")
                        ttt = await self.download_video(url, file_name, res)
                        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                        return ttt
                if self.avg_time == 0:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(self.avg_time)

    async def download(self, url, file_name, res, bot = None, chat_id = None):
        if self.is_dont_limited() and len(self.queue) == 0:
            start_time = time.time()
            time_video, file_size = await self.get_length_video(url, res)
            if file_size > (self.max_memory_mb - self.memory_mb) and self.max_memory_mb != 0:
                raise Exception("File size is too big")
            print("file_size", file_size)
            self.memory_mb += file_size
            total_video_in_sec = time_video * self.avg_time_per_sec
            minutes = round(total_video_in_sec // 60)
            seconds = round(total_video_in_sec % 60)
            msg = await bot.send_message(chat_id=chat_id, text=f"Відео завантажується...\n\nПриблизний час очікування: {minutes}хв. {seconds}с.")
            ttt = await self.download_video(url, file_name, res)
            end_time = time.time()
            full_time = end_time - start_time
            if self.avg_time == 0:
                self.avg_time = full_time
            else:
                self.avg_time = (self.avg_time + full_time) / 2
            if self.avg_time_per_sec == 0:
                self.avg_time_per_sec = full_time / total_video_in_sec
            else:
                self.avg_time_per_sec = (self.avg_time_per_sec + full_time / total_video_in_sec) / 2
            await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
            return ttt
        else:
            id_queue = self.get_id_queue()
            while(True):
                if self.queue[0] == id_queue:
                    if self.is_dont_limited():
                        self.queue.pop(0)
                        start_time = time.time()
                        time_video, file_size = await self.get_length_video(url, res)
                        if file_size > (self.max_memory_mb - self.memory_mb) and self.max_memory_mb != 0:
                            raise Exception("File size is too big")
                        self.memory_mb += file_size
                        total_video_in_sec = time_video * self.avg_time_per_sec
                        minutes = round(total_video_in_sec // 60)
                        seconds = round(total_video_in_sec % 60)
                        msg = await bot.send_message(chat_id=chat_id,
                                                     text=f"Відео завантажується...\n\nПриблизний час очікування: {minutes}хв. {seconds}с.")
                        ttt = await self.download_video(url, file_name, res)
                        end_time = time.time()
                        full_time = end_time - start_time
                        if self.avg_time == 0:
                            self.avg_time = full_time
                        else:
                            self.avg_time = (self.avg_time + full_time) / 2
                        if self.avg_time_per_sec == 0:
                            self.avg_time_per_sec = full_time / total_video_in_sec
                        else:
                            self.avg_time_per_sec = (self.avg_time_per_sec + full_time / total_video_in_sec) / 2
                        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                        return ttt
                if self.avg_time == 0:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(self.avg_time)


static_youtube_manager = YoutubeManager()





