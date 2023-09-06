# -*- coding:utf-8 -*-
#Author: TURKZEN

from PIL import Image,ImageDraw,ImageFont
from sys import argv
import requests
from os import makedirs

class Color:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'    
    NC ='\x1b[0m'

def usage():
    print()
    print("Usage: {}python headerChecker.py [TXT_FILE] {}".format(Color.FAIL,Color.NC))
    print()
    print("{}[TXT_FILE]{} ---> {}Directory where the URL list is located{}".format(Color.FAIL,Color.NC,Color.OKBLUE,Color.NC))
    print()
    quit()

def Main():
    try:
        urlList = argv[1]
    except:
        usage()

    with open("{}".format(urlList),"r") as dosya:
        urlListesi = dosya.readlines()



    for URL in urlListesi:
        URL = URL.strip()
        URL = URL.strip("/")

        if URL[0:4] == "http":
            pass
        else:
            print("{}{}{} ---> {}The URL must start with HTTP or HTTPS.{} ".format(Color.WARNING,URL,Color.NC,Color.FAIL,Color.NC))
            continue

        try:

            req = requests.get("{}".format(URL))

        except requests.exceptions.RequestException:
            print("{}{}{} ---> {}The server is unreachable ! {}".format(Color.WARNING,URL,Color.NC,Color.FAIL,Color.NC))
            continue

        Strict_Transport_Security = req.headers.get("Strict-Transport-Security")
        X_Frame_Options = req.headers.get("X-Frame-Options")
        X_XSS_Protection = req.headers.get("X-XSS-Protection")
        Content_Security_Policy = req.headers.get("Content-Security-Policy")
        X_Content_Type_Options= req.headers.get("X-Content-Type-Options")
        

        Non_Headers = []

        font = ImageFont.truetype("Roboto-Black.ttf", size=50)
        im = Image.new("RGBA",(1920,1080),("Black"))

        draw = ImageDraw.Draw(im)
        draw.text( (0,0),"URL : {}".format(URL),fill="White",font=font)

        draw.text( (0,50),"")

        if Strict_Transport_Security == None:
            Non_Headers.append("Strict-Transport-Security")
            draw.text( (0,100), "Strict-Transport-Security : {}".format(Strict_Transport_Security),fill="Red",font=font)
        else:
            draw.text( (0,100), "Strict-Transport-Security : {}".format(Strict_Transport_Security),fill="Green",font=font)
        
        draw.text( (0,150),"")

        if X_Frame_Options == None:
            Non_Headers.append("X-Frame-Options")
            draw.text( (0,200), "X-Frame-Options : {}".format(X_Frame_Options),fill="Red",font=font)
        else:
            draw.text( (0,200), "X-Frame-Options : {}".format(X_Frame_Options),fill="Green",font=font)
        
        draw.text( (0,250),"")

        if X_XSS_Protection == None:
            Non_Headers.append("X-XSS-Protection")
            draw.text( (0,300),"X-XSS-Protection : {}".format(X_XSS_Protection),fill="Red",font=font)
        else:
            draw.text( (0,300),"X-XSS-Protection : {}".format(X_XSS_Protection),fill="Green",font=font)

        draw.text( (0,350),"")

        if Content_Security_Policy == None:
            Non_Headers.append("Content-Security-Policy")
            draw.text( (0,400),"Content-Security-Policy : {}".format(Content_Security_Policy),fill="Red",font=font)
        else:
            draw.text( (0,400),"Content-Security-Policy : {}".format(Content_Security_Policy),fill="Green",font=font)

        draw.text( (0,450),"")

        if X_Content_Type_Options == None:
            Non_Headers.append("X-Content-Type-Options")
            draw.text( (0,500),"X-Content-Type-Options : {}".format(X_Content_Type_Options),fill="Red",font=font)
        else:
            draw.text( (0,500),"X-Content-Type-Options : {}".format(X_Content_Type_Options),fill="Green",font=font)

        del draw

        URL = URL.split("//")
        URL = URL[1]
        try:
            im.save('screenshots/{}.png'.format(URL), "PNG")
        except FileNotFoundError:
            makedirs("screenshots")
            im.save('screenshots/{}.png'.format(URL), "PNG")
        if len(Non_Headers) == 0:
            pass
        else:
            with open("Non-headers.txt","a") as dosya2:
                dosya2.writelines("""
    {} ---> {}
                """.format(URL,Non_Headers))

def banner():
    
    print("""
          {}
 _   _                _           _____ _               _             
| | | |              | |         /  __ \ |             | |            
| |_| | ___  __ _  __| | ___ _ __| /  \/ |__   ___  ___| | _____ _ __ 
|  _  |/ _ \/ _` |/ _` |/ _ \ '__| |   | '_ \ / _ \/ __| |/ / _ \ '__|
| | | |  __/ (_| | (_| |  __/ |  | \__/\ | | |  __/ (__|   <  __/ |   
\_| |_/\___|\__,_|\__,_|\___|_|   \____/_| |_|\___|\___|_|\_\___|_|                                                                                                                                                 
          {}
          """.format(Color.HEADER,Color.NC))



if __name__ == "__main__":
    try:
        banner()
        Main()
        print()
        print("{}Completed !{}".format(Color.OKGREEN,Color.NC))
        print("Check the {}'screenshots'{} folder and {}'Non-headers.txt'{} file.".format(Color.UNDERLINE,Color.NC,Color.UNDERLINE,Color.NC))
        print()
    except KeyboardInterrupt:
        print("{}Exit Executed !{}".format(Color.FAIL,Color.NC))
