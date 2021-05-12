#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: main.py
"""
from dotenv import load_dotenv
load_dotenv()

import sys
import server
from server.util import createSuperUser

# 加载环境变量

app = server.create_app()

if __name__ == '__main__':
    try:
        if sys.argv[1] == "createsuperuser":
            createSuperUser()
        else:
            print("not this command")
    except:
        app.run(host="0.0.0.0", port=5000)