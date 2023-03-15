from bs4 import BeautifulSoup
from selenium import webdriver
import keyboard
import time


while True:
    choise = input("Do you want to search for space news or videos? \nNews - for news, videos - for videos: ")
    if choise == "news" or choise == "News":
        pagecount = int(input("How many pages do you want to parse (max 9)?: "))
        newsFile = open("news.txt", "w", encoding="utf-8")
        driver = webdriver.Chrome()

        for i in range(1, pagecount+1):
            url = f"https://www.space.com/news/{i}"
            driver.get(url)
            scroll_count = 5

            soup = BeautifulSoup(driver.page_source, "html.parser")
            for news in soup.find_all("a", class_="article-link"):
                print(news)
                if 'href' in news.attrs:
                    newsName = news['aria-label']
                    newsUrl = news['href']
                    if "deal" in newsName or newsUrl:
                        newsFile.write(f"{newsName} | {newsUrl}\n")

        driver.quit()
        newsFile.close()
        break
    elif choise == "Videos" or choise == "videos":
        search = input("Enter your search: ")
        url = f"https://www.youtube.com/results?search_query={search}"
        # url = "http://hdrezkasrskk.net/"
        videosFile = open("videos.txt", "w", encoding="utf-8")
        driver = webdriver.Chrome()
        driver.get(url)

        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        # while True:
        # Scroll down to bottom
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        # time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        # break
        # last_height = new_height
        # driver.execute_script("window.scrollTo(0, 1080)")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for video in soup.select('a#video-title'):
            if 'href' in video.attrs:
                videoName = video['title']
                videoUrl = f"https://www.youtube.com{video['href']}"
                videosFile.write(f"{videoName} | {videoUrl}\n")

        driver.quit()
        videosFile.close()
        break
    else:
        print("Incorrect user input, looping back.")
        continue
