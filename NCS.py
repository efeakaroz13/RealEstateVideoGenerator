import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import json
import os
import random

print("INFO | Fetching page...")
page = requests.get("https://yewtu.be/playlist?list=PL7pkSK1xbGD6Jua6GhFN72kClZfobdnCV")
soup = BeautifulSoup(page.content,"html.parser")
print("INFO | Fetch completed, Scraping page")

allThumbnails = soup.find_all("img",{"class":"thumbnail"})
allUrls = []
for a in allThumbnails:
    url = str("https://youtube.com"+a.parent.parent.get("href"))
    allUrls.append(url)

def downloader(length):
    try:
        os.listdir("ncs")
    except:
        os.system("mkdir ncs")
    selectedUrls = random.sample(allUrls,length)
    for s in selectedUrls:
        yt = YouTube(s)
        video = yt.streams.filter(only_audio=True).first()

        print("INFO| Download Started")
        out_file = video.download(output_path="ncs")
        base, ext = os.path.splitext(out_file)
        os.system(f"ffmpeg -y -i '{base}.mp4' -b:a 192K -vn '{base}.mp3'")
        os.system(f"rm '{base}.mp4'")

        print(f"SUCCESS | {base} ")

if __name__ == "__main__":
    downloader(2)
