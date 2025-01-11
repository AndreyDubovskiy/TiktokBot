
from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip
from pyffmpeg import FFmpeg
import time


strat_time = time.time()

url = "https://www.youtube.com/watch?v=lvOP16MBK6s"


yt = YouTube(url)

print(yt.length, "Length in seconds")
print(yt.title)
tmp = yt.streams
for i in tmp:
    print(i)

strim = yt.streams.filter(mime_type="video/mp4", res="720p").first()

strim.download(filename="video.mp4")
print(strim.filesize_mb, "Size in MB")
strim_audio = yt.streams.filter(mime_type="audio/mp4").last()

print(strim_audio.filesize_mb, "Size in MB (AUDIO)")
strim_audio.download(filename="audio.mp4")

# video_clip = VideoFileClip("video.mp4")
# audio_clip = AudioFileClip("audio.mp4")
# final_clip = video_clip.with_audio(audio_clip)
# final_clip.write_videofile("final.mp4",
#                             codec = "libx264",
#                            preset = "ultrafast",)

ff = FFmpeg()
video_path = "video.mp4"
audio_path = "audio.mp4"
output_path = "final.mp4"
command = f"-i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}"
ff.options(command)

end_time = time.time()
print(end_time - strat_time, "Seconds")