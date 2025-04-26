import requests as req
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url_servis = "https://indown.io/"
url_post = "https://indown.io/download"

ua = UserAgent()

def download_reels_new(url, file_name):
    useragent = ua.random
    headers = {
        "User-Agent": useragent
    }
    resp = req.get(url_servis, headers=headers)

    coockie = resp.cookies

    soup = BeautifulSoup(resp.text, "html.parser")

    referer = soup.find("input", {"name": "referer",
                                  "type": "hidden"}).get("value")
    locale = soup.find("input", {"name": "locale",
                                 "type": "hidden"}).get("value")
    p = soup.find("input", {"name": "i",
                            "type": "hidden"}).get("value")
    _token = soup.find("input", {"name": "_token",
                                 "type": "hidden"}).get("value")
    link = url

    data_post = {
        "referer": referer,
        "locale": locale,
        "i": p,
        "_token": _token,
        "link": link
    }
    resp_tmp = req.post(url_post, headers=headers, data=data_post, allow_redirects=True, cookies=coockie)
    soup = BeautifulSoup(resp_tmp.text, "html.parser")

    files = []

    a_href = soup.find_all(name="div", attrs={"class": "image-link"})

    imgs = []

    for component in a_href:
        imgs.append(component.find(name="img", attrs={"class": "img-fluid"}).get("src"))

    videos = []

    a_href = soup.find_all(name="video", attrs={"class": "img-fluid"})

    for component in a_href:
        videos.append(component.find(name="source").get("src"))

    def download_file_url(url, file):
        resp = req.get(url=url,
                       headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "User-Agent": useragent},
                       cookies=coockie)
        with open(file, 'wb') as f:
            f.write(resp.content)

    for img in imgs:
        tmp_name = file_name+str(len(files)) + ".png"
        download_file_url(img, tmp_name)
        files.append(["image", tmp_name])

    for video in videos:
        tmp_name = file_name+str(len(files)) + ".mp4"
        download_file_url(video, tmp_name)
        files.append(["video", tmp_name])

    return files

