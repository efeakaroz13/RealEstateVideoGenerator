import requests
import os
import json
import random
from gtts import gTTS
import string 

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

if __name__ =="__main__":
    myanton = Anton()
    allData= myanton.getData()
    for d in allData:
        images = myanton.downloadAllImages(d)
    
