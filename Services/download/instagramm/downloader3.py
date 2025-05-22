from playwright.sync_api import sync_playwright
import requests as req

url_servis = "https://indown.io/"
url_post = "https://indown.io/download"



def download_reels_new(url: str, file_name: str):
    files = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://sssinstagram.com/ru")

        page.fill('input[class="form__input"]', url)

        page.click('button[class="form__submit"]')

        page.wait_for_selector('a[class="button button--filled button__download"]')
        all_download_btn = page.query_selector_all('a[class="button button--filled button__download"]')
        yy = 0
        for i in all_download_btn:
            url = i.get_attribute("href")
            response = req.get(url)
            if url.endswith(".jpg"):
                filename = f"{file_name}_{yy}.jpg"
                yy+=1
                with open(filename, "wb") as f:
                    f.write(response.content)
                files.append(["image", filename])
            else:
                filename = f"{file_name}_{yy}.mp4"
                yy += 1
                with open(filename, "wb") as f:
                    f.write(response.content)
                files.append(["video", filename])
        browser.close()
    return files
