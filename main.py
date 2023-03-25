from bs4 import BeautifulSoup
from selenium import webdriver
import tkinter as tk
import requests
from tkinter import messagebox


def update_mode():
    if mode_var.get():
        mode_label.config(text="News mode")
        search_button.pack_forget()
        pagecount_entry.pack()
        search_entry.pack_forget()
        search_button.pack()
        search_button.config(command=search_news)
    else:
        mode_label.config(text="Video mode")
        search_button.pack_forget()
        pagecount_entry.pack_forget()
        search_entry.pack()
        search_button.pack()
        search_button.config(command=search_videos)


def search_news():
    pagecount = int(pagecount_entry.get())

    if not 1 <= pagecount <= 9:
        messagebox.showerror("Error", "Please enter a number between 1 and 9.")
        return

    newsFile = open("news.txt", "w", encoding="utf-8")
    dictionary = {
        'class': ['listingResult small result1', 'listingResult small result2', 'listingResult small result3',
                  'listingResult small result4', 'listingResult small result5', 'listingResult small result6',
                  'listingResult small result7', 'listingResult small result8', 'listingResult small result9',
                  'listingResult small result10', 'listingResult small result11', 'listingResult small result12',
                  'listingResult small result13', 'listingResult small result14', 'listingResult small result15',
                  'listingResult small result16', 'listingResult small result17', 'listingResult small result18',
                  'listingResult small result19', 'listingResult small result20', 'listingResult small result21']}

    for i in range(1, pagecount + 1):
        url = f"https://www.space.com/news/{i}"
        responce = requests.get(url)

        soup = BeautifulSoup(responce.content, "html.parser")
        for articleParent in soup.find_all("div", dictionary):
            articleDeal = articleParent.find(class_='category-link')
            if articleDeal is not None:
                continue
            articleChild = articleParent.find("a", class_='article-link')
            if articleChild is not None and 'href' in articleChild.attrs:
                articleName = articleChild['aria-label']
                articleUrl = articleChild['href']
                newsFile.write(f"{articleName} | {articleUrl}\n")

    newsFile.close()


def search_videos():
    url = f"https://www.youtube.com/results?search_query={search_entry.get()}"
    videosFile = open("videos.txt", "w", encoding="utf-8")
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for video in soup.select('a#video-title'):
        if 'href' in video.attrs:
            videoName = video['title']
            videoUrl = f"https://www.youtube.com{video['href']}"
            videosFile.write(f"{videoName} | {videoUrl}\n")

    driver.quit()
    videosFile.close()


window = tk.Tk()
window.title("DaddyScrapeLegs")
window.geometry("250x150")

mode_label = tk.Label(window, text="News mode", font=("Aerial", 16))
mode_label.pack()

mode_var = tk.BooleanVar()
mode_var.set(True)
mode_switch = tk.Checkbutton(window, text="Switch mode", variable=mode_var, command=update_mode)
mode_switch.pack()

pagecount_entry = tk.Entry(window, width=30, validate="key")
pagecount_entry.config(validate="key", validatecommand=(
pagecount_entry.register(lambda s: s.isdigit() and int(s) in range(1, 10) or s == ''), "%P"))
pagecount_entry.pack()

search_entry = tk.Entry(window, width=30)
search_button = tk.Button(window, text="Search", width=10)
search_button.pack()
search_button.config(command=search_news)

window.mainloop()
