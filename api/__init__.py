#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: __init__.py
"""

from .v1.ping import ping_namespace

from flask import Blueprint, current_app
from flask_restx import Api

# api
api = Blueprint("api", __name__, url_prefix="/api/v1")

SSB_API_v1 = Api(api, version="v1", title="SSB_API", description="SSB_API Server!", terms_url="/api/v1", contact="Hel1antHu5 1984441370@qq.com")
SSB_API_v1.add_namespace(ping_namespace, "/ping")


