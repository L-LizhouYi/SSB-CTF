#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: main.py
"""
from dotenv import load_dotenv

import server

# 加载环境变量
load_dotenv()

app = server.create_app()


if __name__ == '__main__':
    app.run()
