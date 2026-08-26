
from typing import List

from fake_useragent import UserAgent
from httpx import AsyncClient
import DownloadAPI.utils.media_type as mt
import time

ua = UserAgent()

class Downloader1:
    def __init__(self):
        self.name_service = "ssstik"
        self.name_method = "httpx"
        self.ua = UserAgent()
        self.last_time = 0

    async def download(self, url) -> dict | List[dict] | None:
        if (time.time()-self.last_time) >= 10:
            self.last_time = time.time()
        else:
            raise Exception()
        async with AsyncClient() as client:
            user_agent = self.ua.random
            resp = await client.post("https://ssstik.io/abc?url=dl",
                                     data={"id": url,
                                           "locale": "en",
                                           "tt": "UGh1UGtk"},
                                     headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                              "User-Agent": user_agent,
                                              "Hx-Current-Url": "https://ssstik.io/en-1",
                                              "Hx-Request": "true",
                                              "Hx-Target": "target",
                                              "Hx-Trigger": "_gcaptcha_pt"})
            if resp.text.count('<li class="splide__slide" style="') > 0:
                text_split = resp.text.split('<li class="splide__slide" style="')
                text_split.pop(0)
                urls = []
                resps = []

                for i in text_split:
                    urls.append(i.split('<a href="')[1].split('"')[0])
                if len(urls) == 0:
                    return None
                for i in urls:
                    resps.append({"url": i,
                                  "media_type": mt.png,
                                  "user_agent": user_agent})

                url_music = resp.text.split('Download MP3</a>')[0].split('<a href="')[-1].split('"')[0]
                resps.append({"url": url_music,
                              "media_type": mt.mp3,
                              "user_agent": user_agent})
                return resps
            link_to_video = resp.text.split('<a href="')[1].split('"')[0]
            if len(link_to_video) == 0:
                return None
            return {"url": link_to_video,
                    "media_type": mt.mp4,
                    "user_agent": user_agent}

static_downloader1 = Downloader1()