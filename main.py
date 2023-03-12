from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

url = "https://www.youtube.com/"
driver.get(url)
file = open("videos.txt", "w", encoding="utf-8")


soup = BeautifulSoup(driver.page_source, "html.parser")

for video in soup.select('a#video-title-link'):
    if 'href' in video.attrs:
        videoName = video['title']
        videoUrl = f"https://www.youtube.com/{video['href']}"
        file.write(f"{videoName} | {videoUrl}\n")

driver.quit()
file.close()
