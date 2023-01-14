import os
import json
import requests
from bs4 import BeautifulSoup


#Webscrapes todays sunrise time from google search
def Sunrise()-> str: 
    url = "https://www.google.com/search?q="+"sunrise"

    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    sunriseTime = temp.split()

    return sunriseTime[0]


#Webscrapes todays sunset time from google search
def Sunset():

    #Decrements sunset time 33 minutes to get start of sunset 
    def startTime(hour, minute):
        hour = hour + 12
        
        if(minute < 33):
            hour = hour - 1
            minute = 60 - (33 - minute)
        else:
            minute = minute - 33

        if(minute < 10):    
            return str(hour) + ":0" + str(minute)
        else:
            return str(hour) + ":" + str(minute)


    url = "https://www.google.com/search?q="+"sunset"

    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    temp = temp.replace(":", " ")
    temp = temp.split()
    hour = int(temp[0])
    minute = int(temp[1])
    militaryStartTime = startTime(hour, minute)

    return militaryStartTime


#Changes the sunrise and sunset time in the config.json file
def updateJSON(sunrise, sunset):
    with open('D:\Steam Library\steamapps\common\wallpaper_engine\config.json', 'r') as f:
        json_object = json.load(f)
        f.close()

    json_object['Quick']['wproperties']['D:/Steam Library/steamapps/workshop/content/431960/1685364754/background.html']['//?/DISPLAY#SAM099C#5&1b4f727d&0&UID33025#{e6f07b5f-ee97-4a90-b076-33f57bf4eaa7}']['sunrise'] = sunrise
    json_object['Quick']['wproperties']['D:/Steam Library/steamapps/workshop/content/431960/1685364754/background.html']['//?/DISPLAY#SAM099C#5&1b4f727d&0&UID33025#{e6f07b5f-ee97-4a90-b076-33f57bf4eaa7}']['sunset'] = sunset

    with open('D:\Steam Library\steamapps\common\wallpaper_engine\config.json', 'w+') as f:
        f.write(json.dumps(json_object, indent=4))
        f.close


#Updates times and launches Wallpaper Engine
startCommand = '"start "" /d D:\"Steam Library"\steamapps\common\wallpaper_engine wallpaper64.exe"'

sunrise = Sunrise()
sunset = Sunset()
updateJSON(sunrise, sunset)

os.system('cmd /c ' + startCommand)
