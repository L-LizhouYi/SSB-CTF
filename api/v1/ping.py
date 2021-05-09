#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: ping.py
"""
from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping", description="服务器心跳检测")


@ping_namespace.route("")
class Ping(Resource):
    def get(self):
        return {
            "Ping": "Pong"
        }
