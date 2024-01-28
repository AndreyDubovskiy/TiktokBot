import requests as req
import shutil
from moviepy.editor import AudioFileClip
from moviepy.editor import ImageClip, concatenate_videoclips
import os

def down(url, outfile):
  resp = req.post("https://ssstik.io/abc?url=dl",
                  data={"id":url,
                        "locale":"en",
                        "tt":"UGh1UGtk"},
                  headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
  link_to_video = resp.text.split('href="')[1].split('"')[0]
  filereq = req.get(link_to_video, stream=True)
  file_size = int(filereq.headers.get('Content-Length', 0))
  #print(file_size, filereq.status_code)
  if (file_size <= 0):
      raise
  with open(outfile, "wb") as receive:
    shutil.copyfileobj(filereq.raw, receive)
  del filereq

def get_text_video(url):
    res = req.get(url=url,
                  headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    return res.text.split(',"desc":"')[1].split('"')[0]

def get_from_url(url, file_name):
    resp = req.get(url=url,
                   headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
    with open(file_name, 'wb') as f:
        f.write(resp.content)


def get_video_from_foto_tiktok(url, filename):
    resp = req.get(url=url,
                    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
    str_urls = resp.text.split("\"imagePost\":")[1].split("\"locationCreated\"")[0]
    music_url = resp.text.split("\"playUrl\":\"")[1].split("\",")[0].replace("\\u002F", "/")
    urls = []
    for i in str_urls.split("\"urlList\":[\""):
        if i.count("https") == 0:
            continue
        urls.append(i.split("\"]}")[0].replace("\\u002F", "/"))
    index = 0
    image_paths = []
    for i in urls:
        get_from_url(i, filename+"_"+str(index)+".png")
        image_paths.append(filename+"_"+str(index)+".png")
        index+=1
    get_from_url(music_url, filename+".mp3")
    music_path = filename+".mp3"
    audio = AudioFileClip(music_path)
    duration = audio.duration
    clips = []
    for i in image_paths:
        clips.append(ImageClip(i, duration=duration/len(image_paths), transparent=False))
    clip = concatenate_videoclips(clips, method='compose')
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile(filename+".mp4", codec="libx264", fps=1)
    os.remove(music_path)
    for i in image_paths:
        os.remove(i)