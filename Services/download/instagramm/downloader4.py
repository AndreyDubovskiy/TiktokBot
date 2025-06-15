from playwright.sync_api import sync_playwright
import requests as req

url_servis = "https://snapinsta.to/ru"
url_post = "https://indown.io/download"



def download_reels_new(url: str, file_name: str):
    #print("down4 https://snapinsta.to/ru")
    files = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://snapinsta.to/ru")

        page.fill('input[id="s_input"]', url)

        page.click('button[class="btn btn-default"]')

        page.wait_for_selector('div[class="download-items__btn"]')

        page.click('button[id="closeModalBtn"]')
        all_download_btn = page.query_selector_all('div[class="download-items__btn"]')
        yy = 0
        for i in all_download_btn:
            el = i.query_selector('a')
            url = el.get_attribute("href")
            title_text = el.get_attribute("title")
            response = req.get(url)
            if title_text != "Download Video":
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
