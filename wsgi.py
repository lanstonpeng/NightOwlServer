# coding: utf-8

import os

import leancloud
from wsgiref import simple_server

from app import app
from cloud import engine

APP_ID = os.environ.get('LC_APP_ID','glshx16vyhkcmgr65d0utt6byfo94i7231vjx5en6ycsjasw')
MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY','gtqjuop42d6ws092y4b57nzayp3kk6b164bu1pqw0491mo9f')
PORT = int(os.environ.get('LC_APP_PORT',3000))


leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', PORT, application)
    server.serve_forever()
