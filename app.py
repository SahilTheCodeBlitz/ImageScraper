from io import BytesIO
import zipfile
import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen as uReq
from flask import Flask, request,render_template,send_file

# trying to save all the images we get in a folder

# creating a folder image to store images

app = Flask(__name__)


@app.route('/')
def display():
    return render_template('index.html')


@app.route('/submitdata', methods=['POST'])
def imageSave():
    # saveDir = '/Images'
    # if not os.path.exists(saveDir):

    #     os.makedirs(saveDir)

    queryi = request.form.get('query')
    print(queryi)

    response = requests.get(f'https://www.google.com/search?q={queryi}&sca_esv=582023809&tbm=isch&sxsrf=AM9HkKnH5teYD17Ys7dmgSthZKav63xUWA%3A1699908195952&source=hp&biw=693&bih=650&ei=Y4pSZei_OKPcseMPyuyqyAc&iflsig=AO6bgOgAAAAAZVKYc4FsXuMEQ5MA8ZZZzCOw8hWHEuPe&ved=0ahUKEwio_azB68GCAxUjbmwGHUq2CnkQ4dUDCAc&uact=5&oq=sudhansu+kum+ar&gs_lp=EgNpbWciD3N1ZGhhbnN1IGt1bSBhckijL1C3D1ifLnACeACQAQCYAagCoAGpFKoBBjAuMTEuM7gBA8gBAPgBAYoCC2d3cy13aXotaW1nqAIGwgIHECMY6gIYJ8ICBBAjGCfCAgsQABiABBixAxiDAcICCBAAGLEDGIMBwgIFEAAYgATCAggQABiABBixA8ICBhAAGAgYHsICBxAAGBgYgATCAgkQABgYGIAEGAo&sclient=img')  

# request is used to get data from url or body i.e form

    soup = BeautifulSoup(response.content, 'html.parser')
    imagesTag = soup.find_all('img')
    del imagesTag[0]

# storing all this data in images folder by converting in jpg format

    # for i in imagesTag:
    #   imageurl = i['src']
    #   imagedata = requests.get(imageurl).content  # src link me jake content lao
    #   with open(os.path.join(saveDir, f"{queryi}_{imagesTag.index(i)}.jpg"), 'wb') as f:
    #      f.write(imagedata)

# Create a BytesIO object to store the zip file
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i in imagesTag:
            image_url = i['src']
            image_data = requests.get(image_url).content
            zip_file.writestr(f"{queryi}_{imagesTag.index(i)}.jpg", image_data)

    # Seek to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        download_name=f"{queryi}_images.zip",
        as_attachment=True
    )
        

      
      

if __name__ == "__main__":
    app.run(host="0.0.0.0")


# Certainly! Let's break down the code snippet step by step:

# python
# Copy code
# # Create a BytesIO object to store the zip file
# zip_buffer = BytesIO()
# Here, we create a BytesIO object, which is an in-memory binary stream. It allows you to treat binary data as if it were a file on disk. In this case, it will be used to store the contents of the zip file.

# python
# Copy code
# with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
# This line initializes a ZipFile object (zip_file) using the zip_buffer as the target to which the zip file will be written. The mode 'w' indicates that it's being opened for writing.

# python
# Copy code
#     for i in imagesTag:
#         image_url = i['src']
#         image_data = requests.get(image_url).content
#         zip_file.writestr(f"{queryi}_{imagesTag.index(i)}.jpg", image_data)
# Here, a loop iterates through each image URL in the imagesTag list. For each image, it retrieves the image data using requests.get(image_url).content. The writestr method is then used to write this image data to the zip file with a specific filename. The filename is generated based on the query and the index of the image in the imagesTag list.

# python
# Copy code
# # Seek to the beginning of the BytesIO buffer
# zip_buffer.seek(0)
# After writing all the images to the zip file, we use seek(0) to move the position of the cursor to the beginning of the zip_buffer. This ensures that when we later read from the buffer (for sending the file), we start reading from the beginning.

# python
# Copy code
# return send_file(
#     zip_buffer,
#     download_name=f"{queryi}_images.zip",
#     as_attachment=True
# )
# Finally, the send_file function is used to send the contents of zip_buffer as a file to the user's browser. The download_name parameter suggests the default filename for the download, and as_attachment=True indicates that the browser should treat it as a downloadable attachment.