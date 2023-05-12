import requests
import os
import json
import random
from gtts import gTTS
import string
from imageEditor import DetailsEditor
from moviepy.editor import *

agents=open("agents.txt","r").readlines()

class Anton:
    def __init__(self):
        self.logger = open("history/en.old.txt","a")
    def FileNameCreate(self,length):
        output = ""
        for i in range(length):
            dec1 = random.randint(1,2)
            dec2 = random.randint(0,3)
            if dec1 == 1:
                output = output+random.choice(string.ascii_uppercase).lower()
            else:
                output = output+random.choice(string.ascii_uppercase)
            if dec2 == 1:
                output = output+str(random.randint(1,5))
        return output
    def getData(self,city="Seattle",state="WA",limit=4):

        URL = f"https://www.realtor.com/api/v1/browse_modules_hestia?limit={limit}&client_id=rdc-home&types=around_median_homes_for_sale&types=new_listings_for_sale&types=open_houses_for_sale&types=affordable_homes_for_sale&types=luxury_homes_for_sale&feps_version=v2&postal_code=&city={city}&state_code={state}"
        headers= {
            "User-Agent":random.choice(agents).replace("\n","")
        }
        page = requests.get(URL)
        data= json.loads(page.content)

        around_median_homes_for_sale = data["result"]["results"]["around_median_homes_for_sale"]["properties"]
        new_listings_for_sale = data["result"]["results"]["new_listings_for_sale"]["properties"]
        open_houses_for_sale = data["result"]["results"]["open_houses_for_sale"]["properties"]
        affordable_homes_for_sale = data["result"]["results"]["affordable_homes_for_sale"]["properties"]
        luxury_homes_for_sale = data["result"]["results"]["luxury_homes_for_sale"]["properties"]
        output = []
        for a_ in around_median_homes_for_sale:
            a_["from___"] = "around_median_homes_for_sale"
            output.append(a_)
        for a_ in new_listings_for_sale:
            a_["from___"] = "new_listings_for_sale"
            output.append(a_)

        for a_ in open_houses_for_sale:
            a_["from___"] = "open_houses_for_sale"
            output.append(a_)

        for a_ in affordable_homes_for_sale:
            a_["from___"] = "affordable_homes_for_sale"
            output.append(a_)

        for a_ in luxury_homes_for_sale:
            a_["from___"] = "luxury_homes_for_sale"
            output.append(a_)

        return output

    def getZillowData(self,city="Seattle",state="WA"):
        searchData = {
            "pagination": {
                "currentPage": 1
            },
            "usersSearchTerm": f"{city},%20{state}",
            "mapBounds": {
                "west": -122.465159,
                "east": -122.224433,
                "south": 47.491912,
                "north": 47.734145
            },
            "regionSelection": [
                {
                    "regionId": 16037,
                    "regionType": 6
                }
            ],
            "isMapVisible": True,
            "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                },
                "isAllHomes": {
                    "value": True
                }
            },
            "isListVisible": True
        }
        searchData = json.dumps(searchData).replace('\n','').replace(" ","")
        wantsdata = {"cat1":["listResults"],"cat2":["total"]}
        wantsdata = json.dumps(wantsdata).replace('\n','').replace(" ","")
        page = requests.get(f"https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={searchData}&wants={wantsdata}",headers={"User-Agent":random.choice(agents).replace("\n","")})

        data = json.loads(page.content)
        try:
            output = data["cat1"]["searchResults"]["listResults"]
        except:
            output = []

        return output


    def speak(self,text):
        filename =f"OUT{random.randint(1,23423434543)}.mp3"
        tts = gTTS(text)
        tts.save(filename)

        return filename

    def downloadAllImages(self,productData):
        photos = productData["photos"]
        output = []
        try:
            allimgs = os.listdir("images")
        except:
            os.system("mkdir images")

        for p in photos:
            filename = "images/"+self.FileNameCreate(12)
            page = requests.get(p["href"].replace(".jpg","-w1920_h1080_x5.jpg"))
            with open(filename+".jpg","wb") as f:
                output.append(filename+".jpg")
                f.write(page.content)

        return output

    def ZillowImageDownloader(self,productData):
        images = []
        try:
            os.listdir("images")
        except:
            os.system("mkdir images")

        try:
            givenImages = productData["carouselPhotos"]
            for g in givenImages:
                url = g["url"]
                url = url.replace("-p_e.jpg","-cc_ft_1536.jpg")
                ImageGet=requests.get(url)
                filename = self.FileNameCreate(12)
                filename = f"images/{filename}.jpg"
                with open(filename,"wb") as f:
                    f.write(ImageGet.content)
                images.append(filename)
        except:
            pass
        return images

    def videoGenRealtor(self,data):
        baths = data["description"]["baths"]
        sqfeet =data["description"]["sqft"]
        Address = data["location"]["address"]["state_code"]+" "+data["location"]["address"]["city"]+" "+data["location"]["address"]["line"]
        
        list_price = data["list_price"]
        list_date = data["list_date"].split("T")[0].replace("-","/")

        images = self.downloadAllImages(data)
        editedImages = []

        for i in images:
            fname = f"images/{self.FileNameCreate(15)}.jpg"
            editor = DetailsEditor(listPrice=list_price,Address=Address,baths=baths,sqfeet=sqfeet,lotsqfeet=data["description"]["lot_sqft"],list_date=list_date,image_name=i)
            editor.save(fname)
            os.system(f"rm {i}")
            editedImages.append(fname)

        clips = []
        for e in editedImages:

            clips.append(ImageClip(e).set_duration(5))
        
        video = concatenate(clips, method="compose")

        try:
            allSounds = os.listdir("ncs")
            allSounds2 = []
            for a2 in allSounds:
                try:
                    a2.split(".mp3")[1]
                    allSounds2.append(a2)
                except:
                    pass

            allSounds = allSounds2

        except:
            allSounds = []

        if len(allSounds)>0:
            audioSelected = random.choice(allSounds)
            audioclip = AudioFileClip(f"ncs/{audioSelected}").subclip(0,len(editedImages)*5)

            new_audioclip = CompositeAudioClip([audioclip])
            video.audio = new_audioclip
        videoname = f"static/{self.FileNameCreate(12)}.mp4"
        video.write_videofile(videoname, fps=30)
        for e in editedImages:
            os.system(f"rm '{e}'")
        return videoname

        

    def videoGenZillow(self,data):
        baths = data["hdpData"]["homeInfo"]["bedrooms"]
        sqfeet =data["area"]
        Address = data["address"]
        
        list_price = data["unformattedPrice"]
        list_date = data["openHouseEndDate"].split("T")[0].replace("-","/")

        images = self.ZillowImageDownloader(data)
        editedImages = []

        for i in images:
            fname = f"images/{self.FileNameCreate(15)}.jpg"
            editor = DetailsEditor(listPrice=list_price,Address=Address,baths=baths,sqfeet=sqfeet,lotsqfeet=0,list_date=list_date,image_name=i)
            editor.save(fname)
            os.system(f"rm {i}")
            editedImages.append(fname)

        clips = []
        for e in editedImages:

            clips.append(ImageClip(e).set_duration(5))
        
        video = concatenate(clips, method="compose")

        try:
            allSounds = os.listdir("ncs")
            allSounds2 = []
            for a2 in allSounds:
                try:
                    a2.split(".mp3")[1]
                    allSounds2.append(a2)
                except:
                    pass

            allSounds = allSounds2

        except:
            allSounds = []

        if len(allSounds)>0:
            audioSelected = random.choice(allSounds)
            audioclip = AudioFileClip(f"ncs/{audioSelected}").subclip(0,len(editedImages)*5)

            new_audioclip = CompositeAudioClip([audioclip])
            video.audio = new_audioclip
        videoname = f"static/{self.FileNameCreate(12)}.mp4"
        video.write_videofile(videoname, fps=30)
        for e in editedImages:
            os.system(f"rm '{e}'")
        return videoname

        

        

if __name__ =="__main__":
    myanton = Anton()
    allData= myanton.getData()
    print(myanton.videoGenRealtor(allData[0]))

    
