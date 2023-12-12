import requests as req
import shutil

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