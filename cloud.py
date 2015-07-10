# coding: utf-8

from leancloud import Engine

from app import app

from qiniu import Auth

q = Auth('ETRZmSoIoK-VUPMXBwNLF89xjLUM8qNEp8gIB4HQ',
'fIvu13JBUbWhQ5FetU-v5aLlVuT5HePap0ZnSu0q')

engine = Engine(app)

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
