#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-09
@ FileName: test.py
"""
from flask_restx import Namespace, Resource

test_namespace = Namespace("test", description="test")


@test_namespace.route("/mysql")
class Test_MySQL(Resource):
    pass