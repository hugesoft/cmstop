#coding:utf-8
import os
from werkzeug.serving import run_with_reloader
from app import create_app
from flask.ext.script import Manager
import ConfigParser

app = create_app('cmstop')
manager = Manager(app)

if __name__ == '__main__':
    #run_with_reloader是为了在修改模板后自动加载
    config = ConfigParser.ConfigParser()
    config.readfp(open("config.ini", "rb"))
    print config.get("global", "temples_name")

    manager = Manager(app)

    run_with_reloader(manager.run())