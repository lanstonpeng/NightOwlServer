#!/usr/bin/env python
# encoding: utf-8
import urllib, urllib2
import tempfile
import base64
from PIL import Image
import os

# 全局变量
API_URL = 'http://apis.baidu.com/apistore/idlocr/ocr'
API_KEY = "0c69d1b8ec1c96561cb9ca3c037d7225"


def get_image_text(img_url=None):
    headers = {}
    # download image
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    #img_request = urllib2.Request(img_url, headers=headers)
    #img_data = urllib2.urlopen(img_request).read()
    response = opener.open(img_url)
    img_data = response.read()

    # save image to some place
    origin_img = tempfile.NamedTemporaryFile(delete=False)

    save_img = tempfile.NamedTemporaryFile(delete=False)

    origin_img.write(img_data)
    origin_img.flush()

    # convert image
    im = Image.open(origin_img.name)
    im.convert('RGB').save(save_img.name, "JPEG")


    with open(save_img.name, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    data = {}
    data['fromdevice'] = "pc"
    data['clientip'] = "10.10.10.0"
    data['detecttype'] = "LocateRecognize"
    data['languagetype'] = "CHN_ENG"
    data['imagetype'] = "1"
    data['image'] = encoded_image

    decoded_data = urllib.urlencode(data)
    req = urllib2.Request(API_URL, data = decoded_data)

    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("apikey", API_KEY)

    resp = urllib2.urlopen(req)
    content = resp.read()

    # remove useless files
    os.unlink(origin_img.name)
    os.unlink(save_img.name)

    if(content):
        return content

    return None


if __name__ == "__main__":
    print get_image_text("http://www.liantu.com/tiaoma/eantitle.php?title=enl2dnhtUHNPMzQ0TUFpRk5sOTZseEZpYk1PeFYwWlBFQlc2a1dtZjcwaz0=")
