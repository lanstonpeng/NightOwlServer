# coding: utf-8
from leancloud import Engine
from app import app
from qiniu import Auth
import urllib, urllib2
import tempfile
import base64
import os
from PIL import Image

q = Auth('ETRZmSoIoK-VUPMXBwNLF89xjLUM8qNEp8gIB4HQ',
'fIvu13JBUbWhQ5FetU-v5aLlVuT5HePap0ZnSu0q')

engine = Engine(app)

API_URL = 'http://apis.baidu.com/apistore/idlocr/ocr'
API_KEY = "0c69d1b8ec1c96561cb9ca3c037d7225"

@engine.define
def get_image_text(**params):
	headers = {}
	# download image
	img_url = params['img_url']
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
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

@engine.define
def get_upload_token(**params):
    token = q.upload_token('nightowl', params['key'])
    return token



@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'
