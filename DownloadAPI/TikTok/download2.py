from typing import List

from fake_useragent import UserAgent
import utils.media_type as mt
import utils.main_browser as browser
import time

class Downloader2:
    def __init__(self):
        self.name_service = "ssstik"
        self.name_method = "playwright"
        self.ua = UserAgent()
        self.last_time = 0

    async def download(self, url) -> dict | List[dict] | None:
        if (time.time()-self.last_time) >= 10:
            self.last_time = time.time()
        else:
            raise Exception()
        page = await browser.get_page()
        ua = self.ua.random
        try:
            await page.goto("https://ssstik.io")

            tag_input = "#main_page_text"
            button = "button#submit"
            await page.wait_for_selector(selector=tag_input)
            await page.fill(selector=tag_input,
                            value=url)
            cok_tag = ".fc-button.fc-cta-consent.fc-primary-button"
            try:
                await page.click(selector=cok_tag, timeout=2000)
            except:
                pass
            await page.click(selector=button)

            await page.wait_for_selector(selector="#target")

            elem = page.locator(".without_watermark")
            if await elem.count() == 0:
                fotos_elem = page.locator(
                    selector=".pure-button.pure-button-primary.is-center.u-bl.dl-button.download_link.slide.notranslate")
                len_photos = await fotos_elem.count()
                pp = []
                for i in range(len_photos):
                    link = await fotos_elem.nth(i).get_attribute("href")
                    if not (link in pp):
                        pp.append(link)
                music_link = (page.locator(selector="a.music"))
                music_link = await music_link.get_attribute("href")
                res = []
                for i in pp:
                    res.append({"url": i,
                                "media_type": mt.png,
                                "user_agent": ua})
                res.append({"url": music_link,
                            "media_type": mt.mp3,
                            "user_agent": ua})
                for i in res:
                    print(i)
                return res
            else:
                res = await elem.get_attribute("href")
                print(res)
                return {"url": res,
                            "media_type": mt.mp4,
                            "user_agent": ua}
        except:
            return None
        finally:
            await page.close()



#{"url": i, "media_type": mt.png, "user_agent": user_agent}
static_downloader2 = Downloader2()
