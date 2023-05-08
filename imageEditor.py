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
    
if __name__ == "__main__":
    editor = ImageEditor("fonts/CaviarDreams.ttf","Hello","images/tn1ckxjT5wO2f3MH.jpg",font_size=40,secondary_text="This is a secondary Text")
    editor.save("hello.jpg")
