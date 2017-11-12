#coding:utf-8
from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap

import os
import ConfigParser

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hugesoft mmx 1978113'
    #app.config['DEBUG'] = True
    app.debug = True

    basedir = os.path.abspath(os.path.dirname(__file__))
    #数据库配置
    if app.debug == True:
        print 'debug'
        app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'user_db.sqlit')
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    else:
        print 'no debug'
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'mysql://root:enter0087!@127.0.0.1/hzrb_search'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        #app.config.from_object(config[config_name])
        #config[config_name].init_app(app)

    app.config['templates_name'] = read_cfg('config.ini')

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def read_cfg(cfg_name):
    cf = ConfigParser.ConfigParser()
    cf.read(cfg_name)

    temp_name = cf.get("global", "temples_name")

    return temp_name