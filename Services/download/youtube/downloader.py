import os

from pytubefix import YouTube, StreamQuery, Stream
from pyffmpeg import FFmpeg


def get_length_in_sec_and_size(url: str, res, progressive: bool = False):
    yt = YouTube(url)
    return yt.length, yt.streams.filter(mime_type="video/mp4", res=res, progressive=progressive).first().filesize_mb

def get_res(url: str) -> StreamQuery:
    yt = YouTube(url)
    return yt.streams

def get_res_with_audio(url: str) -> StreamQuery:
    yt = YouTube(url)
    strims = yt.streams.filter(mime_type="video/mp4", progressive=True)
    return strims

def get_res_without_audio(url: str) -> StreamQuery:
    yt = YouTube(url)
    strims = yt.streams.filter(mime_type="video/mp4", progressive=False)
    return strims

def get_res_with_and_without_audio(url: str):
    yt = YouTube(url)
    strims_audio = yt.streams.filter(mime_type="video/mp4", progressive=True)
    strims_witout = yt.streams.filter(mime_type="video/mp4", progressive=False)

    for i in strims_audio:
        print(i)
    for i in strims_witout:
        print(i)

    return [strims_audio,
            strims_witout]

def get_url(url: str, res: str, mime_type: str, progressive: bool = True) -> str:
    yt = YouTube(url)
    if mime_type == "audio":
        strim = yt.streams.filter(mime_type="audio/mp4").last()
    else:
        strim = yt.streams.filter(mime_type="video/mp4", res=res, progressive=progressive).first()
    return strim.url

def get_file_from_url(url: str, res: str, mime_type: str, filename: str, progressive: bool = True) -> str:
    yt = YouTube(url)
    if mime_type == "audio":
        strim = yt.streams.filter(mime_type="audio/mp4").last()
    else:
        strim = yt.streams.filter(mime_type="video/mp4", res=res, progressive=progressive).first()
    filename = filename + ".mp4"
    strim.download(filename=filename)
    return filename

def download(url: str, file_name: str, res: str, streams: StreamQuery = None) -> str:
    if streams == None:
        streams = get_res(url)

    strim = streams.filter(mime_type="video/mp4", res=res).first()
    strim_audio = streams.filter(mime_type="audio/mp4").last()
    strim.download(filename=file_name+".mp4")
    strim_audio.download(filename=file_name+"_a.mp4")
    ff = FFmpeg()
    video_path = file_name+".mp4"
    audio_path = file_name+"_a.mp4"
    output_path = file_name+"_f.mp4"
    command = f"-i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -movflags +faststart -fflags +genpts {output_path}"
    ff.options(command)
    try:
        os.remove(video_path)
        os.remove(audio_path)
    except:
        pass
    return output_path



from yt_dlp import YoutubeDL
import yt_dlp

def get_res_and_urls_and_size_and_time_new(url: str):
    ydl_opts = {
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Получение информации о видео
        quality = []
        quality_f = []
        audio_quality = []
        audio_quality_f = []
        for fmt in info.get('formats', []):
            if fmt.get('ext') == 'mp4' and fmt.get('format_note'):
                if fmt.get('audio_channels') == None:
                    if fmt.get('format_note') not in quality and fmt.get('format_note') != "Default":
                        quality.append(fmt.get('format_note'))
                        quality_f.append([fmt.get('format_note'), fmt.get('url'), fmt.get('filesize')])
                else:
                    if (fmt.get('format_note') + "_a") not in quality and fmt.get('format_note') != "Default":
                        quality.append(fmt.get('format_note') + "_a")
                        quality_f.append([fmt.get('format_note') + "_a", fmt.get('url'), fmt.get('filesize')])
            if fmt.get('audio_channels') != None and fmt.get('ext') == "m4a":
                if fmt.get('format_note') not in audio_quality and fmt.get('format_note') != "Default":
                    audio_quality.append(fmt.get('format_note'))
                    audio_quality_f.append([fmt.get('format_note'), fmt.get('url'), fmt.get('filesize')])
        return quality, quality_f, audio_quality, audio_quality_f, info['duration']


def download_new(url: str, file_name: str, res: str) -> str:

    quality, quality_f, audio_quality, audio_quality_f, duration = get_res_and_urls_and_size_and_time_new(url)
    if res.count("_a") > 0:
        arr = []
        for i in quality_f:
            if i[0] == res:
                arr = i
        get_from_url(arr[1], file_name+"_f.mp4")
        return file_name+"_f.mp4"
    else:
        arr = []
        for i in quality_f:
            if i[0] == res:
                arr = i
        get_from_url(arr[1], file_name+".mp4")
        arr = audio_quality_f[-1]
        get_from_url(arr[1], file_name+"_a.mp4")

    ff = FFmpeg()
    video_path = file_name+".mp4"
    audio_path = file_name+"_a.mp4"
    output_path = file_name+"_f.mp4"
    command = f"-i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -movflags +faststart -fflags +genpts {output_path}"
    ff.options(command)
    try:
        os.remove(video_path)
        os.remove(audio_path)
    except:
        pass
    return output_path

from fake_useragent import UserAgent
import requests as req

ua = UserAgent()

def get_from_url(url, file_name, user_agent = ua.random):
    resp = req.get(url=url,
                   headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                               "User-Agent": user_agent})
    with open(file_name, 'wb') as f:
        f.write(resp.content)

URLS = ['https://www.youtube.com/watch?v=h5-oLUesGhQ']
