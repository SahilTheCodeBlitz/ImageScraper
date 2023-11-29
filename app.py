import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen as uReq
from flask import Flask, request,render_template

# trying to save all the images we get in a folder

# creating a folder image to store images

app = Flask(__name__)


@app.route('/')
def display():
    return render_template('index.html')


@app.route('/submitdata', methods=['POST'])
def imageSave():
    saveDir = 'Image Scraper/images/'
    if not os.path.exists(saveDir):

        os.makedirs(saveDir)

    queryi = request.form.get('query')
    print(queryi)

    response = requests.get(f'https://www.google.com/search?q={queryi}&sca_esv=582023809&tbm=isch&sxsrf=AM9HkKnH5teYD17Ys7dmgSthZKav63xUWA%3A1699908195952&source=hp&biw=693&bih=650&ei=Y4pSZei_OKPcseMPyuyqyAc&iflsig=AO6bgOgAAAAAZVKYc4FsXuMEQ5MA8ZZZzCOw8hWHEuPe&ved=0ahUKEwio_azB68GCAxUjbmwGHUq2CnkQ4dUDCAc&uact=5&oq=sudhansu+kum+ar&gs_lp=EgNpbWciD3N1ZGhhbnN1IGt1bSBhckijL1C3D1ifLnACeACQAQCYAagCoAGpFKoBBjAuMTEuM7gBA8gBAPgBAYoCC2d3cy13aXotaW1nqAIGwgIHECMY6gIYJ8ICBBAjGCfCAgsQABiABBixAxiDAcICCBAAGLEDGIMBwgIFEAAYgATCAggQABiABBixA8ICBhAAGAgYHsICBxAAGBgYgATCAgkQABgYGIAEGAo&sclient=img')  

# request is used to get data from url or body i.e form

    soup = BeautifulSoup(response.content, 'html.parser')
    imagesTag = soup.find_all('img')
    del imagesTag[0]

# storing all this data in images folder by converting in jpg format

    for i in imagesTag:
      imageurl = i['src']
      imagedata = requests.get(imageurl).content  # src link me jake content lao
      with open(os.path.join(saveDir, f"{queryi}_{imagesTag.index(i)}.jpg"), 'wb') as f:
         f.write(imagedata)

         

    return f'query ={queryi} '     
      

if __name__ == "__main__":
    app.run(host="0.0.0.0")
