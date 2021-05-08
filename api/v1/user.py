#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: user.py
"""

from flask_restx import Namespace, Resource

user_namespace = Namespace("user", description="user manager!")

class User(Resource):
    pass