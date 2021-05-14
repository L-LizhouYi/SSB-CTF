#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-09
@ FileName: __init__.py.py
"""

USER_INPUT_ERROR = 40001
JWT_TOKEN_ERROR = 40002
JWT_FORMAT_ERROR = 40003
JWT_EXPIRED_ERROR = 40004
USER_EXIST_ERROR = 40005
SERVER_DATABASE_ERROR = 50001

import time

# Response 基础响应序列化器
class Response():
    """
    基础响应序列化器
    :return: {
        "code": 0,
        "data": {},
        "msg": "",
        "timestamp": 1620565098
    }

    """
    result = {
        "code": 0,
        "data": None,
        "msg": "",
        "timestamp": None
    }

    def __init__(self, code, data, msg):
        self.result["code"] = code
        self.result["data"] = data
        self.result["msg"] = msg
        self.result["timestamp"] = int(time.time())


    def Return(self):
        return self.result