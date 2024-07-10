import time

import requests as req
import shutil
import asyncio
from fake_useragent import UserAgent

ua = UserAgent()

async def down_async(url, outfile):
    return await asyncio.to_thread(down, url, outfile)

def down(url, filename):
    try:
        user_agent = ua.random
        session_data = None
        resp = req.get("https://musicaldown.com/en",
                       headers={
                           "User-Agent": user_agent,
                       })
        inputs_str = resp.text.split("<input ")
        inputs = [inputs_str[1].split(">")[0], inputs_str[2].split(">")[0], inputs_str[3].split(">")[0]]

        name_url = inputs[0].split("name=\"")[1].split("\"")[0]
        name_tok = inputs[1].split("name=\"")[1].split("\"")[0]
        value_tok = inputs[1].split("value=\"")[1].split("\"")[0]
        coockie = resp.cookies
        session_data = coockie['session_data']

        resp = req.post("https://musicaldown.com/download",
                        data={name_url: url,
                              name_tok: value_tok,
                              "verify": "1"},
                        headers={
                            'Cookie': f"session_data={session_data}",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "User-Agent": user_agent,
                            "Referer": "https://musicaldown.com/en"},
                        cookies=coockie,
                        allow_redirects=False)
        coockie = resp.cookies

        if resp.headers.get("location", None) == "/en":
            resp = req.get("https://musicaldown.com/en",
                           headers={
                               "User-Agent": user_agent,
                               'Cookie': f"session_data={session_data}",
                               "Referer": "https://musicaldown.com/download"
                           },
                           cookies=coockie)
            inputs_str = resp.text.split("<input ")
            inputs = [inputs_str[1].split(">")[0], inputs_str[2].split(">")[0], inputs_str[3].split(">")[0]]

            name_url = inputs[0].split("name=\"")[1].split("\"")[0]
            name_tok = inputs[1].split("name=\"")[1].split("\"")[0]
            value_tok = inputs[1].split("value=\"")[1].split("\"")[0]
            coockie = resp.cookies

            resp = req.post("https://musicaldown.com/download",
                            data={name_url: url,
                                  name_tok: value_tok,
                                  "verify": "1"},
                            headers={
                                'Cookie': f"session_data={session_data}",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "User-Agent": user_agent,
                                "Referer": "https://musicaldown.com/en"},
                            cookies=coockie,
                            allow_redirects=False)
            coockie = resp.cookies
        if resp.headers.get("location", None) == None:
            url_vid = resp.text.split("<a style=\"margin-top:10px;\" href=\"")[1].split("\"")[0]
            get_from_url(url_vid, filename + ".mp4", user_agent)
            return "video", filename + ".mp4", None
        elif resp.headers.get("location", None) == "/photo/download":
            resp = req.get("https://musicaldown.com/photo/download",
                           headers={
                               'Cookie': f"session_data={session_data}",
                               "Content-Type": "application/x-www-form-urlencoded",
                               "User-Agent": user_agent,
                               "Referer": "https://musicaldown.com/en"},
                           cookies=coockie,
                           allow_redirects=False)
            url_music = resp.text.split("<a style=\"margin-top:10px;margin-bottom:10px\" href=\"")[1].split("\"")[0]
            urls_photos = resp.text.split("<div class=\"card-image\"><img src=\"")
            urls_photos.pop(0)
            final_photos_url = []
            imgs_paths = []
            for i in urls_photos:
                final_photos_url.append(i.split("\"")[0])
            index = 0
            for i in final_photos_url:
                get_from_url(i, filename + "_" + str(index) + ".png", user_agent)
                imgs_paths.append(filename + "_" + str(index) + ".png")
                index += 1
            get_from_url(url_music, filename + ".mp3", user_agent)
            return "photo", imgs_paths, filename + ".mp3"
    except Exception as ex:
        print(ex)
        return get_foto_or_video_tiktok(url, filename)


def get_text_video(url):
    res = req.get(url=url,
                  headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    return res.text.split(',"desc":"')[1].split('"')[0]

def get_from_url(url, file_name, user_agent = ua.random):
    resp = req.get(url=url,
                   headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                               "User-Agent": user_agent})
    with open(file_name, 'wb') as f:
        f.write(resp.content)

def get_foto_or_video_tiktok(url, outfile):
    try:
        user = ua.random
        resp = req.post("https://ssstik.io/abc?url=dl",
                        data={"id": url,
                              "locale": "en",
                              "tt": "UGh1UGtk"},
                        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                 "User-Agent": user,
                                 "Hx-Current-Url": "https://ssstik.io/en-1",
                                 "Hx-Request": "true",
                                 "Hx-Target": "target",
                                 "Hx-Trigger": "_gcaptcha_pt"})
        link_to_video = resp.text.split('<a href="')[1].split('"')[0]
        filereq = req.get(link_to_video, stream=True, headers={"User-Agent": user})
        file_size = int(filereq.headers.get('Content-Length', 0))
        if (file_size <= 0):
            raise
        with open(outfile + ".mp4", "wb") as receive:
            shutil.copyfileobj(filereq.raw, receive)
        del filereq
        return 'video', outfile + ".mp4", None
    except Exception as ex:
        print("ERROR",ex)
        return None, None, None

def print_dict(d, name = "test"):
    print("------",name,"------")
    for i in d:
        print(i, ":", d[i])
    print("---------------------")