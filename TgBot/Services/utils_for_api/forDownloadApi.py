import httpx
import os

class DownloadApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def send_download_request(self, url: str, user_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/download/", params={"url": url, "tg_id": user_id})
            if response.status_code == 200:
                return response.json()
            else:
                return None

    async def get_file(self, user_id: int) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/get_file/", params={"tg_id": user_id})
            return response

#static_download_api = DownloadApi(base_url="http://127.0.0.1:8001")
static_download_api = DownloadApi(base_url=os.getenv("DOWNLOAD_API_BASE_URL", "http://127.0.0.1:8001"))