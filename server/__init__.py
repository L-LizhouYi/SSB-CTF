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

# create_app 实例化Flask实例
def create_app():
    app = Flask(__name__)

    # 设置环境变量之类的东西
    app.env = os.getenv("FLASK_ENV")

    # 注册蓝图
    app.register_blueprint(api)

    return app
