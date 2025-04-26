import requests as req
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import instaloader
import os
import shutil

L = instaloader.Instaloader()

url_servis = "https://indown.io/"
url_post = "https://indown.io/download"

ua = UserAgent()

def download_reels_new(url: str, file_name: str):
    files = []
    is_reels = False
    if url.count("/reel/") > 0:
        is_reels = True
        url_id = url.split("/reel/")[1].split("/")[0]
        pp = instaloader.Post.from_shortcode(L.context, url_id)
        L.download_post(pp, target=file_name)
    elif url.count("/p/") > 0:
        url_id = url.split("/p/")[1].split("/")[0]
        pp = instaloader.Post.from_shortcode(L.context, url_id)
        L.download_post(pp, target=file_name)
    else:
        raise Exception("ErrorLink")

    source_folder = file_name
    destination_folder = ''

    for root, dirs, files2 in os.walk(source_folder):
        for file in files2:
            if file.endswith(('.mp4', '.png', '.jpg')):
                if is_reels:
                    if file.endswith(('.png', '.jpg')):
                        continue
                source_path = os.path.join(root, file)
                base, ext = os.path.splitext(file)
                destination_path = os.path.join(destination_folder, f"{file_name}{ext}")
                if os.path.exists(destination_path):
                    base, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(destination_path):
                        destination_path = os.path.join(destination_folder, f"{file_name}_{i}{ext}")
                        i += 1
                shutil.move(source_path, destination_path)
                if file.endswith('.mp4'):
                    files.append(["video", destination_path])
                elif file.endswith(('.png', '.jpg')):
                    files.append(["image", destination_path])

    shutil.rmtree(source_folder)



    # for img in imgs:
    #     tmp_name = file_name+str(len(files)) + ".png"
    #     download_file_url(img, tmp_name)
    #     files.append(["image", tmp_name])
    #
    # for video in videos:
    #     tmp_name = file_name+str(len(files)) + ".mp4"
    #     download_file_url(video, tmp_name)
    #     files.append(["video", tmp_name])

    return files
