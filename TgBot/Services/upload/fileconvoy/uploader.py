import requests as req
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = "https://www.fileconvoy.com/"

def upload_file(filename) -> str:
    headers = {
        "User-Agent": UserAgent().random
    }
    resp = req.get(URL, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    url_upload = soup.find("form", {"name": "form_upload"}).get("action")

    with open(filename, 'rb') as f:
        files = {'upfile_0': f}
        data = {
            "upload_range": 2,
            "language": "en",
            "NoGoogleAds": 0,
            "retentionPeriod": 2,
            "receiversemail": "",
            "usermessage": "",
            "senderemail": "",
            "charset": "utf8",
            "readTermsOfUse": 1
        }
        response = req.post(URL+url_upload, data, headers=headers, files=files)
        soup = BeautifulSoup(response.text, "html.parser")
        url_download = soup.find_all("p", {"class": "GeneralText"})[1].find("b").text
        #return url_download
    response = req.get(url_download, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    url_real_file = soup.find("table").find("a").get("href")
    return url_real_file
