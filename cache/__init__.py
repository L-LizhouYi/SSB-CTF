#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-12
@ FileName: __init__.py.py
"""
import redis
import os


redisClient = redis.Redis.from_url(os.getenv("REDIS_URI"))

def redisInit():
    return redisClient.ping()

