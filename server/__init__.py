#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: __init__.py.py
"""

import os
from flask import Flask
from api import api

from model import db

# create_app 实例化Flask实例
def create_app():
    app = Flask(__name__)

    # 设置环境变量之类的东西
    app.env = os.getenv("FLASK_ENV")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")   # 数据库连接配置
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 注册蓝图
    app.register_blueprint(api)

    # 数据库连接相关
    db.init_app(app)

    # 创建表
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
