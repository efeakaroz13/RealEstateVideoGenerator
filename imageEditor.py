from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class ImageEditor:
    def __init__(self,fontName,text,imageName,font_size=50,font_secondary="fonts/CaviarDreams_Bold.ttf",secondary_text=None):
        self.fontName = fontName
        self.text = text
        self.imageName = imageName
        self.fontSize = font_size

        self.img = Image.open(self.imageName)
        self.drawImage = ImageDraw.Draw(self.img)

        if len(text)>len(secondary_text):
            longer_text=text
        else:
            longer_text = secondary_text
        self.drawImage.rectangle([(30, 30), (len(longer_text)*22+20,170)],fill="#2f4c8c")
        self.drawImage.rectangle([(40, 40), (len(longer_text)*22+20,170)],fill="#ffffff")
        self.font = ImageFont.truetype(self.fontName, font_size)
        self.font_secondary = ImageFont.truetype(font_secondary,font_size)
        self.drawImage.text((50, 50), self.text, font=self.font, fill =(47, 76, 140))
        self.drawImage.text((50, 100), secondary_text, font=self.font_secondary, fill =(47, 76, 140))
        
    def save(self,filename):
        self.img.save(filename)
        return filename
class DetailsEditor:
    def __init__(self,listPrice,Address,baths,sqfeet,lotsqfeet,list_date,image_name):
        self.fontName = "fonts/CaviarDreams_Bold.ttf"

        self.imageName = image_name
        self.fontSize = 40

        self.img = Image.open(self.imageName)
        self.drawImage = ImageDraw.Draw(self.img)


        
        
        self.drawImage.rectangle([(30, 30), (570+20,370)],fill="#2f4c8c")
        self.drawImage.rectangle([(40, 40), (570+20,370)],fill="#ffffff")
        self.font = ImageFont.truetype(self.fontName, self.fontSize)
        self.drawImage.text((50, 85), f"{Address}", font=self.font, fill =(47, 76, 140))
        self.drawImage.text((48, 135), f"{listPrice:,}$", font=self.font, fill =(47, 76, 140))
        self.drawImage.text((270, 135), f"{sqfeet:,} sqfeet", font=self.font, fill =(47, 76, 140))
        self.drawImage.text((50, 185), f"List Date:{list_date}", font=self.font, fill =(47, 76, 140))
        self.drawImage.text((50, 235),f"{baths} Bathrooms", font=self.font, fill =(47, 76, 140))

    def save(self,filename):
        self.img.save(filename)
        return filename
    
if __name__ == "__main__":
    editor = DetailsEditor(listPrice=124234,Address="Address",baths=3,sqfeet=1231,lotsqfeet=1231,list_date="2022/12/02",image_name="images/XyHzTWr4hv1KMn3.jpg")
    editor.save("hello.jpg")
